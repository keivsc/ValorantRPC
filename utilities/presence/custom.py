from ..client.client import Client
import os
import time
from ..misc.config import Config

class CustomPresence():
    def __init__(self, rpcClient, valClient) -> None:
        self.Config = Config()
        self.config = self.Config.fetchConfig()
        self.client = valClient
        self.rpc = rpcClient
        self.loop = True
        self.translation = self.Config.getTranslation()[self.config['language']]
        
    def startPresence(self):
        pid = os.getpid()
        while self.loop:
            presence = self.client.fetchPresence(self.config)

            if presence == None:
                continue

            if self.loop != presence['inCustom']:
               break

            data = {
                "pid":pid,
            }

            data['start'] = presence['time']
            data['state'] = presence["partyCount"]
            data["details"] = f"{presence['queue']} | {presence['GameData']['map']}"
            data['large_image'] = presence["GameData"]["mapAsset"]
            data['large_text'] = presence["GameData"]["map"]
            
            if self.config['presence']['show_rank'] == True:
                data['small_image'] = presence['tier']['assetName']
                data['small_text'] = presence['tier']['displayName']
            
            elif presence['idle'] == True:
                data['small_image'] = "away"
                data['small_text'] = self.translation['idle']
            
            elif presence['smallImage'] != None:
                data['small_image'] = presence['smallImage']
                data['small_text'] = self.translation["party-leader"]


            self.rpc.set_activity(**data)
            time.sleep(self.config["presenceRefreshRate"])
            self.config = self.Config.fetchConfig()


