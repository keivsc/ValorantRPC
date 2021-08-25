import json
import os
import requests
import sys
import urllib

configVers = "v1.2"
ClientVers = "v2.0"



class Filepath:
    @staticmethod 
    def get_path(relative_path):
        if hasattr(sys, '_MEIPASS'): 
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    @staticmethod 
    def get_appdata_folder():
        return Filepath.get_path(os.path.join(os.getenv('APPDATA'), 'ValorantRPC'))


defaultConfig = {
    "version": ClientVers,
    "configVers":configVers,
    "regions":["", "na", "eu", "latam", "br", "ap", "kr", "pbe"],
    "clientID": 876945941628858398,
    "language":"",
    "languages":["ar-AE","de-DE","en-US","es-ES","es-MX","fr-FR","id-ID","it-IT","ja-JP","ko-KR","pl-PL","pt-BR","ru-RU","th-TH","tr-TR","vi-VN","zh-CN","zh-TW"],
    "presenceRefreshRate": 3,
    "presence":{
        "show_rank": True,
    },
    "startup":{
        "launch_timeout":60,
    }

}

class Config:

    @staticmethod
    def createTranslation(language=None):
        if not os.path.exists(Filepath.get_appdata_folder()):
            os.mkdir(Filepath.get_appdata_folder())
        urllib.request.urlretrieve('https://raw.githubusercontent.com/keivsc/ValorantRPC/v2/translations.json',Filepath.get_path(os.path.join(Filepath.get_appdata_folder(),'translations.json')))

        return Config.getTranslation(language)

    @staticmethod
    def getTranslation(language=None):
        if language == None:
            language = Config.fetchConfig()["language"]
        try:
            with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), "translation.json"))) as f:
                trans = json.load(f)
                return trans[language]
        except:
            return Config.createTranslation(language)

    @staticmethod
    def checkConfig():
        config = Config.fetchConfig()
        try:
            if config["configVers"] != defaultConfig["configVers"]:
                conf = defaultConfig
                conf["regions"] = config["regions"]
                conf["clientID"] = config["clientID"]
                conf["presenceRefreshRate"] = config["presenceRefreshRate"]
                conf["presence"]["show_rank"] = config["presence"]["show_rank"]
                conf["startup"]["launch_timeout"] = config["startup"]["launch_timeout"]
                try:
                    conf["language"] = config["language"]
                except:
                    pass
                with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), "config.json")), "w") as f:
                    f.truncate(0)
                    json.dump(conf, f, indent=4)
                return False
            else:
                return True
        except:
            Config.createConf()
            return False



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


