from ..client.client import Client
import os
import time
from ..misc.config import Config

class Presence():
    def __init__(self, rpcClient) -> None:
        self.Config = Config()
        self.config = self.Config.fetchConfig()
        self.client = Client()
        self.rpc = rpcClient
        self.loop = True
        self.translation = self.Config.getTranslation()[self.config['language']]
        self.client.client.activate()
        
    def startPresence(self):
        pid = os.getpid()
        while self.loop:
            presence = self.client.fetchPresence(self.config)

            if presence == None:
                continue

            if self.loop != presence['inMenus']:
               break

            data = {
                "pid":pid,
            }

            
            data['state'] = presence["partyCount"]

            if presence['matchMaking'] == True: 
                data["details"] = f"{self.translation['in-queue']} - {presence['queue']}"
                data['start'] = presence['time']

            else:
                data["details"] = f"{self.translation['lobby']} - {presence['queue']}"


            data['large_image'] = "game_icon"
            data['large_text'] = "VALORANT"
            
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


