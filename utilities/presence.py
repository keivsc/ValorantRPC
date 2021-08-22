from utilities.game import Game
from utilities.config.config import Config
import pypresence
from .clientMain import Client
from .config.config import Config
import os
import time
import traceback
import requests, urllib3

class ValRPC():
    def __init__(self, rpcClient, region=None):
        self.Config = Config
        self.config = self.Config.fetchConfig()
        self.rpcClient = rpcClient
        self.client = Client(region)
        self.client.activateClient()
        self.client.autoDetectRegion()
        self.ids = self.Config.getTranslation()

    
    def startPresence(self):
        showRank = False
        pastState = None
        matchTimer = None
        dots = ""
        rotation = 1
        past = False
        while True:

            if not Game.are_processes_running(["RiotClientServices.exe"]):
                os._exit(1)

            rpcData = {
                "pid":os.getpid()
            }
            try:
                contentData = self.client.fetchPresence()

            except:
                contentData = None

            if contentData == None:
                if len(dots) >= 3:
                    dots = ""
                rpcData["details"] = f"Loading{dots}"
                dots += "."
                rpcData["buttons"] = []
                rpcData["buttons"].append({"label":"View on GitHHub", "url":"https://github.com/keivsc/ValorantRPC"})
                rpcData["large_image"] = "game_icon"
                rpcData["large_text"] = "ValorantRPC"
                rpcData["small_image"] = "github_icon"
                rpcData["small_text"] = "https://github.com/keivsc/ValorantRPC"

            else:
                rpcData["details"] = contentData["state"]

                state = ""
                pastState = contentData["userState"]

                if contentData["userState"] == "MENUS" and contentData["inCustom"] == False:
                    matchTimer = None

                elif pastState != contentData["userState"]:
                    matchTimer = None
                    pastState = contentData["userState"]

                if contentData["isMatchmaking"] == True:
                    matchTimer = contentData["queueTime"]

                
                if contentData["userState"] == "PREGAME":
                    rpcData["end"] = contentData["pregameEndTime"]

                if contentData["userState"] == "INGAME" or contentData["inCustom"] == True:
                    
                    if matchTimer == None:
                        matchTimer=time.time()
                    
                if contentData["isPartyOpen"] == True and contentData["partySize"] > 2:
                    state += f"{self.ids['open-party']} | {contentData['partySize']} / {contentData['maxPartySize']}"

                elif contentData["isPartyOpen"] == False and contentData["partySize"] > 2:
                    state += f"{self.ids['close-party']} | {contentData['partySize']} / {contentData['maxPartySize']}"

                elif contentData["partySize"] == 2:
                    state += f"{self.ids['duo']}"
                
                else:
                    state += f"{self.ids['solo']}"
                
                

                if contentData["isIdle"] == True:
                    rpcData["small_image"] = "away"
                    rpcData["small_text"] = f"{self.ids['idle']}"

                if contentData["mapAsset"] == None:
                    rpcData["large_image"] = "game_icon"
                    rpcData["large_text"] = "VALORANT"
                else:
                    rpcData["large_image"] = contentData["mapAsset"]
                    rpcData["large_text"] = contentData["map"]

                if contentData["agent"] != None:
                    rpcData["small_image"] = contentData["agentAsset"].lower()
                    rpcData["small_text"] = contentData["agent"]
                    if past == False:
                        past = True

                if self.config["presence"]["show_rank"] == True:
                    if rotation >= 1 or contentData["userState"] == "MENUS":
                        rpcData["small_image"] = "rank_"+str(contentData["competitiveTier"])
                        rpcData["small_text"] = contentData["rank"]
                        if rotation >= 1:
                            rotation -= 1
                        past = False

                if past == True:
                    rotation += 1
            
                
                rpcData["start"] = matchTimer
                rpcData["state"] = state
                try:
                    self.rpcClient.set_activity(**rpcData)
                    time.sleep(self.config["presenceRefreshRate"])
                    self.config = self.Config.fetchConfig()
                except:
                    traceback.print_exc()



