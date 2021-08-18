import valclient
from .utils import valRPC, Processes
from .rpc import RPC
from .config.config import Config
import time
import os
import iso8601
import logging
from .systray import Systray
import threading, asyncio
import ctypes
import psutil


clientClose = False
Presence = True
kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hWnd = kernel32.GetConsoleWindow()
maps = {
    "Range":"The Range",
    "Ascent":"Ascent",
    "Bonsai":"Split",
    "Duality":"Bind",
    "Foxtrot":"Breeze",
    "Port":"Icebox",
    "Triad":"Haven",
}

queue = {
    "newmap": "New Map",
    "competitive": "Competitive",
    "unrated": "Unrated",
    "spikerush": "Spike Rush",
    "deathmatch": "Deathmatch",
    "ggteam": "Escalation",
    "onefa": "Replication",
    "custom": "Custom",
    "snowball": "Snowball Fight",
    "": "Custom",
}

agents = {
    "5F8D3A7F-467B-97F3-062C-13ACF203C006": "agent_breach",
    "F94C3B30-42BE-E959-889C-5AA313DBA261": "agent_raze",
    "601DBBE7-43CE-BE57-2A40-4ABD24953621": "agent_kayo",
    "6F2A04CA-43E0-BE17-7F36-B3908627744D": "agent_skye",
    "117ED9E3-49F3-6512-3CCF-0CADA7E3823B": "agent_cypher",
    "DED3520F-4264-BFED-162D-B080E2ABCCF9": "agent_sova",
    "320B2A48-4D9B-A075-30F1-1F93A9B638FA": "agent_sova",
    "1E58DE9C-4950-5125-93E9-A0AEE9F98746": "agent_killjoy",
    "707EAB51-4836-F488-046A-CDA6BF494859": "agent_viper",
    "EB93336A-449B-9C1B-0A54-A891F7921D69": "agent_phoenix",
    "41FB69C1-4189-7B37-F117-BCAF1E96F1BF": "agent_astra",
    "9F0D8BA9-4140-B941-57D3-A7AD57C6B417": "agent_brimstone",
    "7F94D92C-4234-0A36-9646-3A87EB8B5C89": "agent_yoru",
    "569FDD95-4D10-43AB-CA70-79BECC718B46": "agent_sage",
    "A3BFB853-43B2-7238-A4F1-AD90E9E46BCC": "agent_reyna",
    "8E253930-4C05-31DD-1B6C-968525494517": "agent_omen",
    "ADD6443A-41BD-E414-F6AD-E58D267F4E95": "agent_jett",
    "36FB82AF-409D-C0ED-4B49-57B1EB08FBD5": "unknown",
    "":"unknown"
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
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

files = None

def stop(s):
    global Presence
    global clientClose

    try:
        Presence = False
        clientClose = True
        s.visible = False
        s.stop()
        os._exit(1)
    except:
        Presence = False
        os._exit(1)

def main(file):
    global Presence
    global files
    global clientClose

    Config.checkConfig()
    files = file
    s = Systray()
    x = threading.Thread(target=presence, args=(s,))
    x.start()
    s.run()
    Stop = s.exit()
    if Stop == True:
        stop(s)
        


def presence(s):
    asyncio.set_event_loop(asyncio.new_event_loop())

    client = valRPC()
    rpc = RPC()
    rpc.start()
    pid = os.getpid()
    rpc.clear(pid)
    datas = {
        "pid":pid,
        "state":"Loading...",
        "large_image":"game_icon",
        "small_image":"github_icon",
        "large_text":"keivsc/ValorantRPC",
        "small_text":"https://github.com/keivsc",
        "buttons":[{"label":"View on GitHub", "url":"https://github.com/keivsc/ValorantRPC"}]
    }
    rpc.update(datas)
    x = client.start_game()
    if x == False:
        stop(s)
    client.startup()
    time.sleep(2)
    client = valRPC()
    for x in range(5, -1, -1):
        print(f"[...] RPC Started! Hiding window in ({x})", end="\r")
        time.sleep(1)
    print()
    print("Hiding Window! Have fun playing!!")
    time.sleep(.5)
    user32.ShowWindow(hWnd, 0)
    presenceLoop(client, rpc, pid, s)


def presenceLoop(client, rpc, pid, s):
    global Presence
    global clientClose
    


    if Presence == False:
        rpc.start()

    pastPresence = None
    matchmaking = False
    matchTimer = None
    matchFinished = True
    showRank = False
    matchAgent = None
    appOn = True
    while appOn:

        config = Config.fetchConfig()
        data = {
            "pid":pid,
        }
        try:
            presenceData = client.fetch_presence()
        except:
            stop(s)
        if presenceData == None:
            datas = {
                "pid":pid,
                "state":"Loading...",
                "large_image":"game_icon",
                "small_image":"github_icon",
                "large_text":"keivsc/ValorantRPC",
                "small_text":"https://github.com/keivsc",
                "buttons":[{"label":"View on GitHub", "url":"https://github.com/keivsc/ValorantRPC"}]
            }
            rpc.update(datas)
            time.sleep(config["presenceRefreshRate"])
            continue
        queueId = presenceData["queueId"]
        userState = presenceData["sessionLoopState"]
        partySize = presenceData["partySize"]

        state = None
        largeText=None
        largeImage=None
        if matchFinished == True:
            largeImage = "game_icon"
        smallImage = None
        smallText = None

        if matchAgent != None and userState != "INGAME":
            matchAgent = None

        if partySize == 1:
            state = "Solo"

        elif partySize == 2:
            state = "Duo"

        elif partySize > 2:
            state = f"In a party | {partySize} of {presenceData['maxPartySize']}"
            if presenceData["isPartyOwner"] == True:
                smallImage = "partyOwner"
                smallText = "Party Owner"

        if presenceData["partyAccessibility"] == "OPEN" and partySize < presenceData['maxPartySize']:
            state+=" | Open Party"
            


        if presenceData['partyState'] != "MATCHMAKING" and matchmaking == True:
            matchmaking = False

        elif presenceData['partyState'] == "MATCHMAKING" and matchmaking == False:
            if matchFinished == False:
                matchFinished == True
            matchmaking = True
            data["start"] = Utilities.iso8601_to_epoch(presenceData['queueEntryTime'])
            dots = ""
            state = f"In Queue | {queue[queueId]}{dots}"
            dots+"."
            if len(dots) >= 3:
                dots = ""

        elif userState == "PREGAME":
            user = client.client.pregame_fetch_player()
            data["end"] = (client.client.pregame_fetch_match(user["MatchID"])['PhaseTimeRemainingNS'] // 1000000000) + time.time()
            details = f"Pregame - {queue[queueId]}"
            mapAsset = presenceData["matchMap"].rsplit("/", 1)[1]
            Map = maps[mapAsset]
            largeImage = "splash_"+Map.lower()+"_square"
            largeText = Map
            smallImage = getSmallImage(client.getClient(), userState)
            try:
                smallText = smallImage.split("_")[1].capitalize()
            except:
                smallText = smallImage.capitalize()
            

        elif userState == "INGAME":
            if matchTimer == None:
                matchTimer = time.time()

            data["start"] = matchTimer

    
            if presenceData["matchMap"] == "/Game/Maps/Poveglia/Range":
                largeImage = "splash_range_square"
                details = "The Range"
                largeText = "Range"
            
            else:
                details = f"{queue[queueId]} | {presenceData['partyOwnerMatchScoreAllyTeam']} : {presenceData['partyOwnerMatchScoreEnemyTeam']}"
                mapAsset = presenceData["matchMap"].rsplit("/", 1)[1]
                Map = maps[mapAsset]
                largeImage = "splash_"+Map.lower()+"_square"
                matchAgent = getSmallImage(client.getClient(), userState)
                largeText = Map
                matchFinished = False
                try:
                    smallText = matchAgent.split("_")[1].capitalize()
                except:
                    smallText = matchAgent.capitalize()

                if config["presence"]["show_rank"] == True:
                    if showRank == True:
                        rankID = "rank_"+str(presenceData["competitiveTier"])
                        smallImage = rankID
                        rank = rankName[rankID]
                        if rank == "Radiant" or rank == "Immortal":
                            leadPos = presenceData["leaderboardPosition"]
                            rank = f"Immortal #{leadPos}"
                            if leadPos >= 500:
                                rank = f"Radiant #{leadPos}"
                        try:
                            mmr = client.client.fetch_mmr()["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][Loader.load_all_content(client.client)["season"]["season_uuid"]]
                            smallText = rank + f" ~ {mmr['RankedRating']} RR"
                        except:
                            smallText = "Unranked"
                        showRank = False

        elif presenceData['partyState'] == "CUSTOM_GAME_SETUP":
            if matchFinished == False:
                matchFinished == True
                matchAgent = None
            matchmaking = True
            if matchTimer == None:
                matchTimer = time.time()
            dots = ""
            details = f"Setting Up a Custom Game{dots}"
            mapAsset = presenceData["matchMap"].rsplit("/", 1)[1]
            Map = maps[mapAsset]
            largeImage = "splash_"+Map.lower()+"_square"
            largeText = Map
            dots+"."
            if len(dots) >= 3:
                dots = ""

        elif userState == "MENUS":
            matchAgent = None
            if matchFinished == False:
                Presence = False
                matchFinished == True
            matchTimer = None
            details = f"Lobby - {queue[queueId]}"
            if presenceData["isIdle"] == True:
                state = "Away"
                smallImage = "away"

        else:
            time.sleep(config["presenceRefreshRate"])
            continue


        if state != None:
            data["state"] = state
        data["details"] = details
        data["large_image"] = largeImage
        data["large_text"] = largeText

        if smallImage != None:
            data["small_image"] = smallImage
        if smallText != None:
            data["small_text"] = smallText
        if matchTimer != None:
            data["start"] = matchTimer

        if smallImage == None and smallText == None:
            if config["presence"]["show_rank"] == True:
                rankID = "rank_"+str(presenceData["competitiveTier"])
                smallImage = rankID
                rank = rankName[rankID]
                if rank == "Radiant" or rank == "Immortal":
                    leadPos = presenceData["leaderboardPosition"]
                    rank = f"Immortal #{leadPos}"
                    if leadPos >= 500:
                        rank = f"Radiant #{leadPos}"
                try:
                    mmr = client.client.fetch_mmr()["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][Loader.load_all_content(client.client)["season"]["season_uuid"]]
                    smallText = rank + f" ~ {mmr['RankedRating']} RR"
                except:
                    smallText = "Unranked"
                data["small_image"] = smallImage
                data["small_text"] = smallText

        if data != pastPresence and Presence == True:
            rpc.update(data)
            pastPresence = data

        time.sleep(config["presenceRefreshRate"])
        appOn = "RiotClientServices.exe" in (p.name() for p in psutil.process_iter())
    rpc.clear(pid)
    rpc.close(pid)
    os._exit(0)
            



def getSmallImage(client:valclient.Client, userState):
    if userState == "PREGAME":
        user = client.pregame_fetch_player()
        if user == None:
            return agents[""]
        match = client.pregame_fetch_match(user["MatchID"])

        for team in match["Teams"]:
            for player in team["Players"]:
                if player == None:
                    return ""
                if player["Subject"] == user["Subject"]:
                    return agents[player["CharacterID"].upper()]
    if userState == "INGAME":
        user = client.coregame_fetch_player()
        if user == None:
            return agents[""]
        match = client.coregame_fetch_match(user["MatchID"])
        for player in match["Players"]:
            if player["Subject"] == user["Subject"]:
                return agents[player["CharacterID"].upper()]
    


class Utilities:

    @staticmethod 
    def iso8601_to_epoch(time):
        if time == "0001.01.01-00.00.00":
            return None
        split = time.split("-")
        split[0] = split[0].replace(".","-")
        split[1] = split[1].replace(".",":")
        split = "T".join(i for i in split)
        split = iso8601.parse_date(split).timestamp() #converts iso8601 to epoch
        return split

import requests

class Loader:

    @staticmethod 
    def fetch(endpoint="/"):
        data = requests.get(f"https://valorant-api.com/v1{endpoint}")
        return data.json()

    @staticmethod 
    def load_all_content(client):
        content_data = {
            "agents": [],
            "maps": [],
            "modes": [],   
            "comp_tiers": [],
            "season": {},
            "queue_aliases": { #i'm so sad these have to be hardcoded but oh well :(
                "newmap": "New Map",
                "competitive": "Competitive",
                "unrated": "Unrated",
                "spikerush": "Spike Rush",
                "deathmatch": "Deathmatch",
                "ggteam": "Escalation",
                "onefa": "Replication",
                "custom": "Custom",
                "snowball": "Snowball Fight",
                "": "Custom",
            },
            "team_aliases": {
                "TeamOne": "Defender",
                "TeamTwo": "Attacker",
                "TeamSpectate": "Observor",
                "TeamOneCoaches": "Defender Coach",
                "TeamTwoCoaches": "Attacker Coach",
                "Red": ""
            },
            "team_image_aliases": {
                "TeamOne": "team_defender",
                "TeamTwo": "team_attacker",
                "Red": "team_defender",
                "Blue": "team_attacker",
            },
            "modes_with_icons": ["ggteam","onefa","snowball","spikerush","unrated","deathmatch"]
        }
        all_content = client.fetch_content()
        agents = Loader.fetch("/agents")["data"]
        maps = Loader.fetch("/maps")["data"]
        modes = Loader.fetch("/gamemodes")["data"]
        comp_tiers = Loader.fetch("/competitivetiers")["data"][-1]["tiers"]
        

        for season in all_content["Seasons"]:
            if season["IsActive"] and season["Type"] == "act":
                for comp_season in all_content["CompetitiveSeasons"]:
                    if comp_season["SeasonID"] == season["ID"]:
                        content_data["season"] = {
                            "competitive_uuid": comp_season["ID"],
                            "season_uuid": season["ID"],
                            "display_name": season["Name"]
                        }
        
        for agent in agents:
            content_data["agents"].append({
                "uuid": agent["uuid"],
                "display_name": agent["displayName"],
                "internal_name": agent["developerName"]
            })

        for game_map in maps:
            content_data["maps"].append({
                "uuid": game_map["uuid"],
                "display_name": game_map["displayName"],
                "path": game_map["mapUrl"],
                "internal_name": game_map["mapUrl"].split("/")[-1]
            })

        for mode in modes:
            content_data["modes"].append({
                "uuid": mode["uuid"],
                "display_name": mode["displayName"],
            })

        for tier in comp_tiers:
            content_data["comp_tiers"].append({
                "display_name": tier["tierName"],
                "id": tier["tier"],
            })

        return content_data
