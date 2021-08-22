import valclient
from .config.config import Config
import requests
from .content import Loader
import iso8601
import time
from .systray import Systray

maps = {
    "Ascent":"Ascent",
    "Bonsai":"Bonsai",
    "Duality":"Bind",
    "Foxtrot":"Breeze",
    "Port":"Icebox",
    "Range":"The Range",
    "Triad":"Haven",
}

rankName = {
    "rank_0": "Unranked",
    "rank_3": "Iron 1",
    "rank_4": "Iron 2",
    "rank_5": "Iron 3",
    "rank_6": "Bronze 1",
    "rank_7": "Bronze 2",
    "rank_8": "Bronze 3",
    "rank_9": "Silver 1",
    "rank_10": "Silver 2",
    "rank_11": "Silver 3",
    "rank_12": "Gold 1",
    "rank_13": "Gold 2",
    "rank_14": "Gold 3",
    "rank_15": "Platinum 1",
    "rank_16": "Platinum 2",
    "rank_17": "Platinum 3",
    "rank_18": "Diamond 1",
    "rank_19": "Diamond 2",
    "rank_20": "Diamond 3",
    "rank_21": "Immortal",
    "rank_22": "Immortal",
    "rank_23":  "Immortal",
    "rank_24":  "Radiant",
}

class exceptions:
    class UnableToActivateClient(Exception):
        pass

class Client():
    def __init__(self, region=None):
        self.Config = Config
        self.region = region
        self.config = self.Config.fetchConfig()
        self.content = Loader()
        self.content.activate()
        self.dots=""
        if self.region == None:
            self.region = self.config["regions"][0]
        if self.region not in ["na","eu","latam","br","ap","kr","pbe"]:
            self.region = "na"
        self.client = valclient.Client(region=self.region)


    ### startup use
    def autoDetectRegion(self):
        if self.config["regions"][0] not in ["na","eu","latam","br","ap","kr","pbe"]:
            print("--------------------------")
            print("Auto detecting region...")
            sessions = self.client.riotclient_session_fetch_sessions()
            for _, session in sessions.items():
                if session["productId"] == "valorant":
                    launch_args = session["launchConfiguration"]["arguments"]
                    for arg in launch_args:
                        if "-ares-deployment" in arg:
                            region = arg.replace("-ares-deployment=","")
                            data = self.config
                            data["regions"][0] = region
                            self.Config.updateConf(data)
                            self.client = valclient.Client(region=region)
                            print(f"Region Detected - {region}")
                            print("--------------------------")
                            Systray.restart()
                            return region
    
    def activateClient(self):
        try:
            self.client.activate()
        except:
            raise exceptions.UnableToActivateClient("VALORANT is not running!")

    ###

    def fetchAgentID(self,matchState):

        if matchState.lower() == "pregame":
            user = self.client.pregame_fetch_player()
            if user == None:
                return ""
            Match = self.client.pregame_fetch_match(user["MatchID"])
            for team in Match["Teams"]:
                for player in team["Players"]:
                    if player == None:
                        return "unknown"
                    if player["Subject"] == user["Subject"]:
                        return player["CharacterID"].lower()
        elif matchState.lower() == "ingame":
            user = self.client.coregame_fetch_player()
            if user == None:
                return ""
            Match = self.client.coregame_fetch_match(user["MatchID"])
            for player in Match["Players"]:
                if player["Subject"] == user["Subject"]:
                    return player["CharacterID"].lower()


    def fetchPresence(self):
        data = {
            "isMatchmaking":False,
            "isIdle":False,
            "mapAsset":None,
            "agent":None
        }

        try:
            presence = self.client.fetch_presence()
        except:
            raise self.valorantIsOffline("Valorant is offline") 

        if presence == None:
            return None
        

        userState = presence["sessionLoopState"]

        data["competitiveTier"] = presence["competitiveTier"]
        data["rank"] = rankName["rank_"+str(presence["competitiveTier"])]
        data["partySize"] = presence["partySize"]
        data["maxPartySize"] = presence["maxPartySize"]
        data["queueId"] = presence['queueId']
        data["userState"] = presence["sessionLoopState"]
        data["inCustom"] = False
        data["isPartyOpen"] = False
        

        if presence["partyAccessibility"] == "OPEN":
            data["isPartyOpen"] = True

        if presence["partyState"] == "MATCHMAKING":
            data["isMatchmaking"] = True
            data["queueTime"] = iso8601_to_epoch(presence["queueEntryTime"])
            data["state"] = f"In Queue | {presence['queueId'].capitalize()}"
        
        if userState == "INGAME" or userState == "PREGAME":
            data["map"] = self.content.fetchMaps(presence["matchMap"])
            data["mapAsset"] = f"splash_{data['map']}_square".replace("The ","").lower()
            if presence["matchMap"] == "/Game/Maps/Poveglia/Range":
                data["state"] = "The Range"
            else:
                data["state"] = f"{self.content.fetchMode(data['queueId']).capitalize()}"
                if userState == "PREGAME":
                    user = self.client.pregame_fetch_player()
                    if user == None:
                        data ["pregameEndTime"] = 80 + time.time()
                    else:
                        Match = self.client.pregame_fetch_match(user["MatchID"])
                        data["pregameEndTime"] = (Match['PhaseTimeRemainingNS'] // 1000000000) + time.time()
                    data["state"] = f"Pregame | {data['state']}"
                    data["agent"] = self.content.fetchAgentName(self.fetchAgentID(userState))

                elif userState == "INGAME":
                    data["state"] = f"{data['state']} | {presence['partyOwnerMatchScoreAllyTeam']} : {presence['partyOwnerMatchScoreEnemyTeam']}"
                    data["agent"] = self.content.fetchAgentName(self.fetchAgentID(userState))
                    if presence["partyState"] == "CUSTOM_GAME_SETUP":
                        data["inCustom"] = True

        if presence["partyState"] == "CUSTOM_GAME_SETUP" and userState != "PREGAME" and userState != "INGAME":
            if len(self.dots) >= 3:
                self.dots = ""
            data["state"] = f"Custom Game Setup{self.dots}"
            data["inCustom"] = True
            data["map"] = self.content.fetchMaps(presence["matchMap"])
            data["mapAsset"] = f"splash_{data['map']}_square".replace("The ","").lower()
            self.dots += "."

        elif userState == "MENUS" and presence["partyState"] != 'MATCHMAKING':
            data["state"] = f"Lobby - {self.content.fetchMode(data['queueId']).capitalize()}"

        if presence["isIdle"] == True:
            data["isIdle"] = True
            data["state"] += " (Idle)"
        


        return data
    ### 





def iso8601_to_epoch(time):
    if time == "0001.01.01-00.00.00":
        return None
    split = time.split("-")
    split[0] = split[0].replace(".","-")
    split[1] = split[1].replace(".",":")
    split = "T".join(i for i in split)
    split = iso8601.parse_date(split).timestamp() #converts iso8601 to epoch
    return split
