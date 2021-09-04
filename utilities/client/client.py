from os import stat
import valclient
from ..misc.config import Config, configActivate
from .contentLoader import Loader
import traceback
from InquirerPy import inquirer
from ..systray import systray
import iso8601
import time
import os

def iso8601_to_epoch(time):
    if time == "0001.01.01-00.00.00":
        return None
    split = time.split("-")
    split[0] = split[0].replace(".","-")
    split[1] = split[1].replace(".",":")
    split = "T".join(i for i in split)
    split = iso8601.parse_date(split).timestamp() #converts iso8601 to epoch
    return split


class prompt:
    @staticmethod
    def promptLanguage(config, Config):
        choice = inquirer.select(
            message="Select your language (Use arrow keys): ",
            default="en-US",
            choices={option:option for option in config["languages"]},
            pointer=">"
        )
        choice.execute()
        config["language"] = choice.result_name
        Config.updateConf(config)


class Client():
    def __init__(self) -> None:
        regions = ["na", "eu", "latam", "br", "ap", "kr", "pbe"]
        self.Config = Config()
        self.config = self.Config.fetchConfig()
        self.Loader = Loader()
        try:
            self.region = self.config["region"]
        except:
            self.region = ""
            config = self.config
            config['region'] = ""
            self.config = self.Config.updateConf(config)

        if self.region not in regions:
            self.region = "na"

        self.client = valclient.Client(region=self.region)
        self.autoDetectRegion()
        configActivate()
        self.Loader.activate()
        self.GameTime = 0
        self.language = self.config["language"]
        if self.language not in self.config["languages"]:
            self.language = "en-US"
        self.language = self.Config.getTranslation()[self.language]
    

    def autoDetectRegion(self):
        if self.config["region"] not in ["na","eu","latam","br","ap","kr","pbe"]:
            self.client.activate()
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
                            data["region"] = region
                            self.Config.updateConf(data)
                            print(f"Region Detected - {region.upper()}")
                            print("--------------------------")
                            time.sleep(1)
                            systray.restart()
                            return region
    
    def activate(self):
        try:
            self.client.activate()
        except:
            traceback.print_exc()


    def fetchPresence(self):
        data = {
            "sessionLoopState":None,
            "time":None,
            "inGame":False,
            "inPregame":False,
            "inMenus":False,
            "inCustom":False,
            "queue":None,
            "idle":False,
            "ShowRank":None,
            "partySize":1,
            "partyMax":0,
            "partyAccess":False,
            "GameData":{
                "agent":None,
                "map":None,
                "score":None,
                "agentAsset":None,
                "mapAsset":None
            },
            "tier":{}
        }
        try:
            gamePresence = self.client.fetch_presence()
        except:
            os._exit(1)

        if gamePresence == None:
            return None

        data['sessionLoopState'] = gamePresence["sessionLoopState"]
        state = gamePresence["sessionLoopState"]
        partyState = gamePresence['partyState']
        data["partySize"] = gamePresence["partySize"]
        data["partyMax"] = gamePresence["maxPartySize"]
        data["tier"] = self.Loader.data["competitiveTiers"][f"{gamePresence['competitiveTier']}"]
        data['queue'] = self.Loader.data["gamemodes"][gamePresence["queueId"]]

        if self.config["show_party_count"] == True:
            if data['partySize'] == 1:
                data['partyCount'] = self.language['solo']

            elif data['partySize'] == 2:
                data['partyCount'] = self.language['duo']

            elif gamePresence["partyAccessibility"] == "OPEN":
                data["partyAccess"] = True
                data["partyCount"] += self.language["open-party"]
                data["partyCount"] += f" | {data['partySize']} / {data['partyMax']}"

            else:
                data["partyCount"] += self.language["close-party"]
                data["partyCount"] += f" | {data['partySize']} / {data['partyMax']}"
        else:
            data["partyCount"] = False
        
        
        if state == "INGAME" or state == "PREGAME":
            data["GameData"]["agent"] = self.Loader.data["agents"][""]["displayName"]
            data["GameData"]["agentAsset"] = self.Loader.data["agents"][""]["assetName"]
            data["GameData"]["map"] = self.Loader.data["maps"][gamePresence["matchMap"]]["displayName"]
            data["GameData"]["mapAsset"] = self.Loader.data["maps"][gamePresence["matchMap"]]["assetName"]

            if state == "PREGAME":
                
                data["inPregame"] = True
                user = self.client.pregame_fetch_player()
                if user == None:
                    data ["time"] = 80 + time.time()
                    data["GameData"]["agent"] = self.Loader.data["agents"][""]["displayName"]
                    data["GameData"]["agentAsset"] = self.Loader.data["agents"][""]["assetName"]

                else:
                    Match = self.client.pregame_fetch_match(user["matchID"])
                    data["time"] = (Match['PhaseTimeRemainingNS'] // 1000000000) + time.time()
                    for team in Match["Teams"]:

                        for player in team["Players"]:
                            if player == None:
                                data["GameData"]["agent"] = self.Loader.data["agents"][""]["displayName"]

                            if player["Subject"] == user["Subject"]:
                                data["GameData"]["agent"] = self.Loader.data["agents"][player["CharacterID"]]["displayName"]
                                data["GameData"]["agentAsset"] = self.Loader.data["agents"][player["CharacterID"]]["assetName"]
            else:
                if self.GameTime == 0:
                    self.GameTime = time.time()
                data["time"] = self.GameTime
                data["inGame"] = True
                data["GameData"]["score"] = f"{gamePresence['partyOwnerMatchScoreAllyTeam']} : {gamePresence['partyOwnerMatchScoreEnemyTeam']}"
                user = self.client.coregame_fetch_player()
                if user == None:
                    data["GameData"]["agent"] = self.Loader.data["agents"][""]["displayName"]
                    data["GameData"]["agentAsset"] = self.Loader.data["agents"][""]["assetName"]

                else:
                    Match = self.client.coregame_fetch_match(user["MatchID"])

                    for player in Match["Players"]:
                        if player["Subject"] == user["Subject"]:
                            data["GameData"]["agent"] = self.Loader.data["agents"][player["CharacterID"]]["displayName"]
                            data["GameData"]["agentAsset"] = self.Loader.data["agents"][player["CharacterID"]]["assetName"]


        
        elif partyState == "MATCHMAKING":
            data["time"] = iso8601_to_epoch(gamePresence["queueEntryTime"])

        elif state == "MENUS":
            if self.GameTime != 0:
                self.GameTime = 0
            
            data["inMenus"] = True

        if partyState == "CUSTOM_GAME_SETUP":
            data["inCustom"] = True
        
        if gamePresence["isIdle"] == True:
            data["idle"] = True
        
        return data

        

        



        
