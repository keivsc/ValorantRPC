import json
import requests
from ..misc.config import Config

def convertNumeral(string):
    romanNumerals = {
            "1":"I",
            "2":"II",
            "3":"III"
        }
    for i in list(romanNumerals.keys()):
        if i in string:
            return string.replace(i, romanNumerals[i])
    return string


def fetch(endpoint="/", language="en-US"):
    res = requests.get(f"https://valorant-api.com/v1{endpoint}", params={"language":language})
    resp = requests.get(f"https://valorant-api.com/v1{endpoint}", params={"language":"en-US"})
    return [res.json(), resp.json()]

class Loader:
    def __init__(self) -> None:
        self.Config = Config()
        self.config = self.Config.fetchConfig()
        self.language = self.config["language"]
        if self.language not in self.config["languages"]:
            self.language = "en-US"
        self.language = [self.Config.getTranslation()[self.language], self.language]
        self.data = {
            "agents":{
                "":{
                    "displayName":"Unknown",
                    "assetName":"agent_unknown"
                }

            },
            "maps":{

            },
            "competitiveTiers":{

            },
            "gamemodes":self.language[0]['queueAliases']
        }


    def activate(self):
        agents = fetch("/agents", self.language[1])
        maps = fetch("/maps", self.language[1])
        compTiers = fetch("/competitivetiers", self.language[1])[0]['data'][-1]['tiers']

        for agent in agents[0]["data"]:
            self.data["agents"][agent["uuid"]] = {}
            self.data["agents"][agent["uuid"]]["displayName"] = agent["displayName"].capitalize()

        for item in maps[0]["data"]:
            self.data["maps"][item["mapUrl"]] = {}
            self.data["maps"][item["mapUrl"]]["displayName"] = item["displayName"].capitalize()

        for agent in agents[1]["data"]:
            self.data["agents"][agent["uuid"]]["assetName"] = f"agent_{(agent['displayName']).lower()}"

        for item in maps[1]["data"]:
            if item['mapUrl'] == "/Game/Maps/Poveglia/Range":
                self.data["maps"][item["mapUrl"]]["assetName"] = f"splash_range_square"
            else:
                self.data["maps"][item["mapUrl"]]["assetName"] = f"splash_{(item['displayName']).lower()}_square"

        for item in compTiers:
            tier = str(item["tier"])
            self.data["competitiveTiers"][tier]  = {}
            tierName = item["tierName"]
            if 21 <= int(tier) < 24:
                tierName = tierName[:-1]
            if self.config['presence']['use_roman_numerals'] == True:
                self.data["competitiveTiers"][tier]["displayName"] = convertNumeral(tierName.capitalize())
            else:
                self.data["competitiveTiers"][tier]["displayName"] = tierName.capitalize()
            self.data["competitiveTiers"][tier]["assetName"] = f"rank_{tier}"
    


