from valclient.client import Client 
import os, json, datetime

from .contentLoader import Loader


class Valorant:

    def __init__(self, region):
        self.client = Client(region)
        self.client.activate()

    def load_match_data(self):
        # agent images are from https://playvalorant.com/page-data/en-us/agents/page-data.json
        
        content = Loader.load_all_content(self.client)
        matches = self.client.fetch_match_history()["History"]
        tries = 0
        while tries < 5:
            matchid = matches[tries]["MatchID"]
            match_data = self.client.fetch_match_details(matchid)
            if match_data["matchInfo"]["queueID"] != "deathmatch":
                break
            else:
                tries+=1
        if tries > 5:
            return False

        total_rounds = len(match_data["roundResults"])

        if match_data["matchInfo"]["queueID"] != "deathmatch":
            payload = {
                "match_id": match_data["matchInfo"]["matchId"],
                "match_map": match_data["matchInfo"]["mapId"],
                "match_mode": match_data["matchInfo"]["queueID"],
                "timestamp": datetime.datetime.fromtimestamp(match_data["matchInfo"]["gameStartMillis"]//1000).strftime('%m/%d/%Y %H:%M:%S'),
                "match_mode_display_name": content["queue_aliases"][match_data["matchInfo"]["queueID"]],
                "match_map_display_name": [gmap for gmap in content["maps"] if match_data["matchInfo"]["mapId"] in gmap["path"]][0]["display_name"],
                "teams": [
                    {
                        "team_name": team["teamId"],
                        "team_alias": "ATK" if team["teamId"] == "Red" else "DEF",
                        "won_bool": team["won"],
                        "won": "WIN" if team["won"] else "LOSS",
                        "rounds_won": team["roundsWon"],
                    } for team in match_data["teams"]
                ],
                "players": [
                    [
                        {
                            "puuid": player["subject"],
                            "display_name": player["gameName"],
                            "team_id": player["teamId"],
                            "agent_id": player["characterId"],
                            "agent_display_name": [agent for agent in content["agents"] if player["characterId"] in agent["uuid"]][0]["display_name"],
                            "kd": str(round(player["stats"]["kills"] / (player["stats"]["deaths"] if player["stats"]["deaths"] != 0 else 1),1)),
                            "kills": player["stats"]["kills"],
                            "combat_score": player["stats"]["score"] // total_rounds,
                        } for player in match_data["players"] if player["teamId"] == team["teamId"]
                    ] for team in match_data["teams"]
                ],
            }
        
        
            # sort players by combat score
            payload["players"] = [sorted(team, key=lambda k: k["combat_score"], reverse=True) for team in payload["players"]]

            # sort teams by red/blue
            backup = payload["teams"].copy()
            team_blue = [team for team in backup if team["team_name"] == "Blue"]
            team_red = [team for team in backup if team["team_name"] == "Red"]
            payload["teams"] = [team_red[0],team_blue[0]]

        

        #print(payload)
        return payload