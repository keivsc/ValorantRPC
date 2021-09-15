import requests
import json
import os
import sys

latestVersion = "v3"
latestConfig = {}
translationFile = {}

def configActivate():
    globals()['latestConfig'] = (requests.get(f"https://raw.githubusercontent.com/keivsc/ValorantRPC/{latestVersion}/configExample.json")).json()
    globals()['translationFile'] = (requests.get(f"https://raw.githubusercontent.com/keivsc/ValorantRPC/{latestVersion}/translations.json")).json()



class Config:
    def __init__(self) -> None:
        configActivate()

    @staticmethod 
    def get_path(relative_path):
        if hasattr(sys, '_MEIPASS'): 
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    @staticmethod
    def checkConfig():
        config = Config().fetchConfig()
        newConf = latestConfig
        if config["configVers"] != latestConfig["configVers"] or config["version"] != latestConfig["version"]:
            items = ["version", "configVers", "regions", "languages"]
            for x in items:
                newConf[x] = latestConfig[x]

            items = ["region", "clientID", "language", "presenceRefreshRate", "matchSheet"]
            for item in items:
                try:
                    newConf[item] = config[item] 
                except:
                    newConf[item] = newConf[item]

            try:
                newConf["presence"]["show_rank"] = config["presence"]["show_rank"] 
            except:
                newConf["presence"]["show_rank"] = True

            try:
                newConf["startup"]["launch_timeout"] = config["startup"]["launch_timeout"]
            except:
                newConf["startup"]["launch_timeout"] = 60
            
            config = Config().updateConf(newConf)
            
        return config

    @staticmethod 
    def get_appdata_folder():
        return Config().get_path(os.path.join(os.getenv('APPDATA'), 'ValorantRPC'))

    @staticmethod
    def fetchConfig():
        try:
            with open(Config().get_path(os.path.join(Config().get_appdata_folder(), "config.json"))) as f:
                config = json.load(f)
                return config
        except:
            return Config().createConf()
    
    @staticmethod
    def getTranslation():
        return translationFile

    @staticmethod
    def createConf():
        if not os.path.exists(Config().get_appdata_folder()):
            os.mkdir(Config().get_appdata_folder())
        with open(Config().get_path(os.path.join(Config().get_appdata_folder(), "config.json")), "w") as f:
            json.dump(latestConfig, f, indent=4)
        return Config().fetchConfig()

    @staticmethod
    def updateConf(data):
        with open(Config().get_path(os.path.join(Config().get_appdata_folder(), "config.json")), "w") as f:
            json.dump(data, f, indent=4)
        return Config().fetchConfig()
