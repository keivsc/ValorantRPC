import json
import os
from .filepath import Filepath
import requests

defaultConfig = {
    "version": "v1.0",
    "regions":["", "na","eu","latam","br","ap","kr","pbe"],
    "clientID": 876945941628858398,
    "presenceRefreshRate": 3,
    "presence":{
        "show_rank": True
    },
    "startup":{
        "launch_timeout":60,
    }

}

class Config:

    @staticmethod
    def fetchConfig():
        try:
            with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), "config.json"))) as f:
                config = json.load(f)
            
                return config
        except:
            return Config.createConf()
    
    @staticmethod
    def createConf():
        if not os.path.exists(Filepath.get_appdata_folder()):
            os.mkdir(Filepath.get_appdata_folder())
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), "config.json")), "w") as f:
            json.dump(defaultConfig, f, indent=4)
        return Config.fetchConfig()

    @staticmethod
    def updateConf(data):
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), "config.json")), "w") as f:
            json.dump(data, f, indent=4)
        return Config.fetchConfig()
