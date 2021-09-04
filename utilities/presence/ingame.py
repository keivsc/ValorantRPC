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
        while self.loop:
            presence = self.client.fetchPresence()

            if presence == None:
                continue

            if self.loop != presence['inGame']:
               self.loop = presence['inGame']
               continue

            data = {
                "pid":os.getpid(),
            }

            data["details"] = f"{presence['queue']} | {presence['GameData']['score']}"
            data['state'] = presence["partyCount"]
            data['start'] = presence['time']
            data['large_image'] = presence['GameData']['mapAsset']
            data['large_text'] = presence['GameData']['map']

            try:
                if self.config["presence"]["show_rank"] == True:
                    if self.ShowRank == False:
                        data['small_image'] = presence['GameData']['agentAsset']
                        data['small_text'] = presence['GameData']['agent']
                        self.ShowRank = True
                    else:
                        data['small_image'] = presence['tier']['assetName']
                        data['small_text'] = presence['tier']['displayName']
                        self.ShowRank = False
                else:
                    data['small_image'] = presence['GameData']['agentAsset']
                    data['small_text'] = presence['GameData']['agent']
            except:
                data['small_image'] = presence['GameData']['agentAsset']
                data['small_text'] = presence['GameData']['agent']


            self.rpc.set_activity(**data)
            time.sleep(self.config["presenceRefreshRate"])
            self.config = self.Config.fetchConfig()


