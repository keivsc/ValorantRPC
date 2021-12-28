import requests, time
import dateutil.parser as dp

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
def iso8601_to_epoch(Time):
    if Time == "0001.01.01-00.00.00":
        return None
    parsed = dp.parse(Time).timestamp()
    return parsed
class Content:
    def __init__(self):
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
            "gamemodes":{
                "newmap": "New Map",
                "competitive": "Competitive",
                "unrated": "Unrated",
                "spikerush": "Spike Rush",
                "deathmatch": "Deathmatch",
                "ggteam": "Escalation",
                "onefa": "Replication",
                "custom": "Custom",
                "snowball": "Snowball Fight",
                "": "Custom"
            }
        }

    def fetch(self, endpoint="/"):
        res = requests.get(f"https://valorant-api.com/v1{endpoint}", params={"language":"en-US"})
        return res.json()

    def fetch_data(self):
        agents = self.fetch("/agents")
        maps = self.fetch("/maps")
        compTiers = self.fetch("/competitivetiers")['data'][-1]['tiers']
        seasons = self.fetch("/seasons")['data']

        for agent in agents["data"]:
            self.data["agents"][agent["uuid"]] = {}
            self.data["agents"][agent["uuid"]]["displayName"] = agent["displayName"].capitalize()
            self.data["agents"][agent["uuid"]]["assetName"] = f"agent_{(agent['displayName']).lower()}"

        for item in maps["data"]:

            self.data["maps"][item["mapUrl"]] = {}
            self.data["maps"][item["mapUrl"]]["displayName"] = item["displayName"].capitalize()
            self.data["maps"][item["mapUrl"]]["assetName"] = f"splash_{(item['displayName']).lower()}_square"
            if item['mapUrl'] == "/Game/Maps/Poveglia/Range":
                self.data["maps"][item["mapUrl"]]["assetName"] = "splash_range_square"
                self.data["maps"][item["mapUrl"]]["displayName"] = "The Range"

        for item in compTiers:
            tier = str(item["tier"])
            self.data["competitiveTiers"][tier] = {}
            tierName = item["tierName"]
            if 21 <= int(tier) < 24:
                tierName = tierName[:-1]
            self.data["competitiveTiers"][tier]["displayName"] = convertNumeral(tierName.capitalize())
            self.data["competitiveTiers"][tier]["assetName"] = f"rank_{tier}"
        Time = time.time()

        for season in seasons:
            start = iso8601_to_epoch(season['startTime'])
            end = iso8601_to_epoch(season['endTime'])
            if start < Time < end:
                self.data['season'] = {
                    "season_uuid":season['uuid']
                }
            
