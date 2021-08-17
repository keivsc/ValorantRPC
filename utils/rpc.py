import pypresence
import os
import time
from .config.config import Config
from .systray import Systray

class RPC():
    def __init__(self):
        self.config = Config.fetchConfig()
        self.clientID = self.config["clientID"]
        try:
            self.client = pypresence.Presence(self.clientID)
            self.client.connect()
        except pypresence.exceptions.InvalidID:
            print("[X] Invalid Application ID! Check https://discord.com/developers/applications for more info! Or use the default clientID: ()")
            input("Press enter to close...")
            quit()
        except pypresence.exceptions.InvalidPipe:
            print("[X] Invalid Pipe! Is Discord Running?")
            input("Press enter to restart...")
            Systray.restart()
        except pypresence.exceptions.ServerError:
            print("[X] Server Error! Discord Servers are down or you are not connected to the internet!")
            input("Press enter to close...")
            quit()

    def start(self):
        try:
            self.client.start()
            return True
        except Exception as e:
            return e

    def update(self, data:dict):
        try:
            self.client.update(**data)
            return True
        except Exception as e:
            return e
    
    def clear(self, pid):
        self.client.clear(pid)


    def close(self):
        self.client.close()