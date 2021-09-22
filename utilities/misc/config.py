from plyer.facades import notification
import requests
import json
import os
import sys, time
from plyer import notification
from colorama import Fore

def fetchTag():
    req = requests.get("https://api.github.com/repos/keivsc/valorantrpc/releases/latest")
    tag = req.json()["tag_name"]
    return tag

latestVersion = fetchTag()
currentVersion = "v3.4"
latestConfig = {}
translationFile = {}

def configActivate():
    globals()['latestConfig'] = (requests.get(f"https://raw.githubusercontent.com/keivsc/ValorantRPC/v3/configExample.json")).json()
    globals()['translationFile'] = (requests.get(f"https://raw.githubusercontent.com/keivsc/ValorantRPC/v3/translations.json")).json()



class Config:
    def __init__(self) -> None:
        configActivate()

    @staticmethod 
    def get_path(relative_path):
        if hasattr(sys, '_MEIPASS'): 
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    @staticmethod
    def checkVersion():
        try:
            newConf = Config.fetchConfig()
            newConf['version'] = currentVersion
            Config.updateConf(newConf)
            if float(latestVersion) > float(currentVersion.replace('v', '')):
                print(f"{Fore.YELLOW}There is a new version of ValorantRPC ({currentVersion} -> v{latestVersion})\n{Fore.GREEN}Download it at\nhttps://github.com/keivsc/ValorantRPC/releases/latest")
                return True
        except:
            print(f"{Fore.RED}Unable to check for new versions")
            

    @staticmethod
    def checkConfig():
        config = Config().fetchConfig()
        newConf = latestConfig
        newConf['version'] = currentVersion
        if Config.checkVersion() == True:
            notification.notify(
                title='New Version of RPC is available',
                message='Check out keivsc/ValorantRPC for the new version!',
                app_icon=Config.get_path(os.path.join(Config.get_appdata_folder(), 'favicon.ico'))
            )
        else:
            print(f"{Fore.GREEN}ValorantRPC Up To Date")
        if config["configVers"] != latestConfig["configVers"]:
            items = ["configVers", "regions", "languages"]
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
        time.sleep(3)
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
            latestConfig["version"] = currentVersion
            json.dump(latestConfig, f, indent=4)
        return Config().fetchConfig()

    @staticmethod
    def updateConf(data):
        with open(Config().get_path(os.path.join(Config().get_appdata_folder(), "config.json")), "w") as f:
            json.dump(data, f, indent=4)
        return Config().fetchConfig()
