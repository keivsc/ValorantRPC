from ..client.client import Client
import os
import time
from ..misc.config import Config

class Presence():
    def __init__(self, rpcClient) -> None:
        self.Config = Config
        self.config = self.Config.fetchConfig()
        self.client = Client()
        self.rpc = rpcClient
        self.loop = True
        self.client.client.activate()
        
    def startPresence(self):
        while self.loop:
            presence = self.client.fetchPresence()

            if self.loop != presence['inGame']:
               self.loop = presence['inGame']
               continue

            data = {
                "pid":os.getpid(),
            }

            data["details"] = f"{presence['queue']} | {presence['score']}"
            data['state'] = presence["partyCount"]
            data['start'] = presence['time']
            data['large_image'] = presence['GameData']['mapAsset']
            data['large_text'] = presence['GameData']['map']
            data['small_image'] = presence['GameData']['agentAsset']
            data['small_text'] = presence['GameData']['agent']

            self.rpc.set_activity(**data)
            time.sleep(self.config["presenceRefreshRate"])


