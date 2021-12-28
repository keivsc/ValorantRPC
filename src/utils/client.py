import valclient
from .content import Content
import time

class Client:
    def __init__(self, region):
        self.client = valclient.Client(region=region)
        self.client.activate()
        self.content = Content()
        self.content.fetch_data()
        self.data = self.content.data
        
    
    def get_state(self, presence=None):
        if presence:
            return presence['sessionLoopState']
        presence = self.get_presence()
        if presence:
            return presence['sessionLoopState']
        return None

    def get_presence(self):
        try:
            return self.client.fetch_presence()
        except:
            return None
    
    def get_rank(self):
        try:
            mmr = self.client.fetch_mmr()
            mmr = mmr["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][self.data["season"]["season_uuid"]]
        except:
            return {"assetName":"rank_0","displayName":"UNRANKED | 0RR"}

        return {"assetName":f"rank_{mmr['CompetitiveTier']}", "displayName":self.data["competitiveTiers"][str(mmr['CompetitiveTier'])]['displayName']+f" | {mmr['RankedRating']}RR"}

    def get_level(self):
        return self.client.fetch_account_xp()['Progress']['Level']
    
    def api(self):
        presence = self.get_presence()
        data = {
            "state":self.get_state(),
            "level":self.get_level(),
            "rank":self.get_rank(),
            "match":{}
        }
        try:
            player = self.client.coregame_fetch_player()
        except:
            pass
        else:
            Match = self.client.coregame_fetch_match(player["MatchID"])
            data["match"] = {}
            data["match"]["points"] = {"ally":presence['partyOwnerMatchScoreAllyTeam'], "enemy": presence['partyOwnerMatchScoreEnemyTeam']}
            data["match"]["mode"] = self.data["gamemodes"][presence["queueId"]]
            data["match"]["map"] = self.data["maps"][Match["MapID"]]['displayName']
            for player in Match["Players"]:
                if player["Subject"] == player["Subject"]:
                    data["match"]["agent"] = self.data["agents"][player["CharacterID"].lower()]["displayName"]
        
        return data


    def get_agent(self, players, subject):
        for player in players:
            if player['Subject'] == subject:
                try:
                    data = self.data['agents'][player['CharacterID'].lower()]
                    data['state'] = player['CharacterSelectionState']
                    return data
                except:
                    return self.data['agents'][player['CharacterID'].lower()]


    def get_coregame(self, presence):
        if presence['sessionLoopState'] == "INGAME":
            try:
                player = self.client.coregame_fetch_player()
                match = self.client.coregame_fetch_match(player['MatchID'])
                if self.data['maps'][match['MapID']]['displayName'] == "The Range":
                    data = {
                        "practice":True,
                        "players":match['Players'],
                        "subject":player['Subject'],
                        "matchID":player['MatchID'],
                        "agent": self.get_agent(match["Players"], player['Subject']),
                        "map": self.data['maps'][match['MapID']],
                        "queue": self.data['gamemodes'][presence['queueId']]
                    }
                    return data
                data = {
                    "practice":False,
                    "players":match['Players'],
                    "subject":player['Subject'],
                    "matchID":player['MatchID'],
                    "agent": self.get_agent(match["Players"], player['Subject']),
                    "allyScore": presence['partyOwnerMatchScoreAllyTeam'],
                    "enemyScore": presence['partyOwnerMatchScoreEnemyTeam'],
                    "map": self.data['maps'][match['MapID']],
                    "queue": self.data['gamemodes'][presence['queueId']]
                }
                return data
            except:
                return None
        else:
            return None

    def get_pregame(self, presence):
        if presence['sessionLoopState'] == "PREGAME":
            try:
                player = self.client.pregame_fetch_player()
                match = self.client.pregame_fetch_match(player['MatchID'])
                data = {
                    "players":match['AllyTeam']['Players'],
                    "subject":player['Subject'],
                    "matchID":player['MatchID'],
                    "agent":self.get_agent(match['AllyTeam']['Players'], player['Subject']),
                    "time_left":(match['PhaseTimeRemainingNS'] // 1000000000) + time.time(),
                    "map": self.data['maps'][match['MapID']],
                    "queue": self.data['gamemodes'][presence['queueId']]
                }
                return data
            except Exception as e:
                return None
        else:
            return None

    def parse_gamemode(self, ID):
        return self.data['gamemodes'][ID]

