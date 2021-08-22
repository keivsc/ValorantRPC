import requests
from .config.config import Config

def fetch(endpoint='/', params=None):
    data = requests.get(f"https://valorant-api.com/v1{endpoint}", params=params)
    return data.json()

class Loader():
    def __init__(self):
        self.content = {}
        self.Config = Config
        self.config = self.Config.fetchConfig()

    
    
    def activate(self):
        lang = self.config["language"]
        if not lang in self.config["languages"]:
            lang = "en-US"
        params = {"language":lang}

        data = {
            "agents":{
                "":"unknown"
            },
            "agentAssets":{
                "":"unknown"
            },
            "maps":{},
            "mapAssets":{},
            "queueAliases":{

            }
        }

        agents = fetch("/agents", params)["data"]
        maps = fetch("/maps", params)["data"]
        mapAssets = fetch("/maps", params={"language":"en-US"})['data']
        agentAssets = fetch("/agents", params={"language":"en-US"})['data']
        data["queueAliases"] = self.Config.getTranslation(lang)["queueAliases"]


        for agent in agents:
            data["agents"][f"{agent['uuid']}"] = agent["displayName"].replace('/', '')
        
        for agent in agentAssets:
            data["agentAssets"][f"{agent['uuid']}"] = agent["displayName"].replace('/', '')

        for Map in maps:
            data["maps"][f"{Map['mapUrl']}"] = Map["displayName"]

        for Map in mapAssets:
            data["mapAssets"][f"{Map['mapUrl']}"] = Map["displayName"]

        if not lang in self.config["languages"]:
            lang = "en-US"
            update = self.config
            update["language"] = lang
            self.Config.updateConf(update)
        self.content = data
    
    def fetchAgentName(self, uuid):
        return self.content["agents"][uuid]

    def fetchAgentAsset(self, uuid):
        return self.content["agentAssets"][uuid]

    def fetchMapAsset(self, path):
        return self.content["mapAssets"][path]
    
    def fetchMaps(self, path):
        return self.content["maps"][path]
    
    def fetchMode(self, mode):
        return self.content["queueAliases"][mode]

    def fetchSeason(self, client):
        all_content = client.fetch_content()
        data = {}
        for season in all_content["Seasons"]:
            if season["IsActive"] and season["Type"] == "act":
                for comp_season in all_content["CompetitiveSeasons"]:
                    if comp_season["SeasonID"] == season["ID"]:
                        data["season"] = {
                            "competitive_uuid": comp_season["ID"],
                            "season_uuid": season["ID"],
                            "display_name": season["Name"]
                        }
        return data

    def fetchAllData(self):
        return self.content

