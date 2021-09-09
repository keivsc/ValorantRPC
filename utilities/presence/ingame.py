from ..client.client import Client
import os
import time
from ..misc.config import Config
import traceback

class Presence():
    def __init__(self, rpcClient) -> None:
        self.Config = Config
        self.config = self.Config.fetchConfig()
        self.client = Client()
        self.rpc = rpcClient
        self.loop = True
        self.client.client.activate()
        self.ShowRank = False
        
    def startPresence(self):
        pid = os.getpid()
        while self.loop:
            presence = self.client.fetchPresence()
            if presence == None:
                continue

            if self.loop != presence['inGame']:
               break

            data = {
                "pid":pid,
            }

            if presence['GameData']['mapAsset'] == "splash_range_square":
                data["details"] = f"The Range"
                data['start'] = presence['time']
                try:
                    if self.config["presence"]["show_rank"] == True:
                        data['small_image'] = presence['GameData']['agentAsset']
                        data['small_text'] = presence['GameData']['agent']

                except:
                    data['small_image'] = None
                    data['small_text'] = None

            else:
                data["details"] = f"{presence['queue']} | {presence['GameData']['score']}"
                data['state'] = presence["partyCount"]
                data['start'] = presence['time']
                data['large_image'] = presence['GameData']['mapAsset']
                data['large_text'] = presence['GameData']['map']

                try:
                    if self.config["presence"]["show_rank"] == True:
                        if self.ShowRank == False and presence['GameData']['mapAsset'] != "splash_range_square":
                            data['small_image'] = presence['GameData']['agentAsset']
                            data['small_text'] = (presence['GameData']['agent']).capitalize()
                            self.ShowRank = True
                        else:
                            data['small_image'] = presence['tier']['assetName']
                            data['small_text'] = presence['tier']['displayName']
                            self.ShowRank = False
                    else:
                        if presence['GameData']['mapAsset'] != "splash_range_square":
                            data['small_image'] = presence['GameData']['agentAsset']
                            data['small_text'] = (presence['GameData']['agent']).capitalize()
                except:
                    if presence['GameData']['mapAsset'] != "splash_range_square":
                        data['small_image'] = presence['GameData']['agentAsset']
                        data['small_text'] = (presence['GameData']['agent']).capitalize()


            self.rpc.set_activity(**data)
            time.sleep(self.config["presenceRefreshRate"])
            self.config = self.Config.fetchConfig()


