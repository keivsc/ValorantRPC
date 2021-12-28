import os, sys, json, urllib

current_version = "v4.0"

default_config = {
    "version":"v4.0",
    "region":"na",
    "regions":["na", "eu", "latam", "br", "ap", "kr", "pbe"],
    "clientID": 876945941628858398,
    "presence":{
        "refreshRate": 3,
        "show_rank": True,
        "show_party_count":True,
        "show_level":True,
        "buttons":{
            "button1":{
                "label":"YouTube",
                "url":"https://www.youtube.com/channel/UCElXNqNdek9HFI3QN496C9Q",
                "activate":False
            },
            "button2":{
                "label":"Twitch",
                "url":"https://www.twitch.com/soilive",
                "activate":False
            },
            "button3":{
                "note":"You can only have 2 buttons so dont try making 3 it won't work"
            }
        }
    },
    "startup":{
        "launch_timeout":60
    },
    "server":{
        "port":6969
    }
}

class Config:
    def __init__(self):
        self.config = {}

    @staticmethod 
    def get_appdata_folder():
        return os.path.join(os.getenv('APPDATA'), 'ValorantRPC')

    def fetchConfig(self):
        try:
            with open(os.path.join(Config.get_appdata_folder(), "config.json"), 'r') as f:
                self.config = json.load(f)
        except:
            self.config = Config.create_config()

    def check(self):
        urllib.request.urlretrieve('https://raw.githubusercontent.com/keivsc/ValorantRPC/v1/favicon.ico',os.path.join(Config.get_appdata_folder(),'favicon.ico'))
        conf = self.fetch_config()
        if conf['version'] != current_version:
            os.remove(os.path.join(Config.get_appdata_folder(), "config.json"))
            Config.create_config()

    def fetch_config(self):
        if self.config == {}:
            self.fetchConfig()
            return self.config
        return self.config
    
    @staticmethod
    def create_config():
        if not os.path.exists(Config.get_appdata_folder()):
            os.mkdir(Config.get_appdata_folder())
        with open(os.path.join(Config.get_appdata_folder(), "config.json"), "a+") as f:
            json.dump(default_config, f, indent=4)
        return default_config

    @staticmethod
    def update(data):
        with open(os.path.join(Config.get_appdata_folder(), "config.json"), "w") as f:
            json.dump(data, f, indent=4)