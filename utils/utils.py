import os
import json
import psutil
import valclient
from .config.config import Config
import time
import logging

class Processes:

    @staticmethod
    def are_processes_running(required_processes=["VALORANT-Win64-Shipping.exe", "RiotClientServices.exe"]):
        processes = []
        for proc in psutil.process_iter():
            processes.append(proc.name())
        
        return set(required_processes).issubset(processes)

class valRPC:

    def __init__(self):
        self.conf = Config
        self.config = self.conf.fetchConfig()
        self.activated = False
        self.puuid = None
        self.region = self.config["regions"][0]
        if self.region == "":
            self.region = "na"
        self.client = valclient.Client(region=self.region)
        

    def getClient(self):
        return self.client

    def start_game(self):
        path = self.get_rcs_path()
        launch_timeout = self.config["startup"]["launch_timeout"]
        launch_timer = 0
        
        if not Processes.are_processes_running():
            psutil.subprocess.Popen([path, "--launch-product=valorant", "--launch-patchline=live"])
        while not Processes.are_processes_running():
            print(f"[...] Waiting for VALORANT ({launch_timer})", end="\r")
            launch_timer += 1
            if launch_timer >= launch_timeout:
                return False
            time.sleep(1)
        print("[√] Valorant detected and running!")
        self.client.activate()


    def get_rcs_path(self):
        riot_installs_path = os.path.expandvars("%PROGRAMDATA%\\Riot Games\\RiotClientInstalls.json")
        try:
            with open(riot_installs_path, "r") as file:
                client_installs = json.load(file)
                rcs_path = os.path.abspath(client_installs["rc_default"])
                if not os.access(rcs_path, os.X_OK):
                    return None
                return rcs_path
        except FileNotFoundError:
            return None

    def startup(self):
        sessions = self.client.riotclient_session_fetch_sessions()
        for _, session in sessions.items():
            if session["productId"] == "valorant":
                launch_args = session["launchConfiguration"]["arguments"]
                for arg in launch_args:
                    if "-ares-deployment" in arg:
                        region = arg.replace("-ares-deployment=","")
                        data = self.config
                        data["regions"][0] = region
                        _ = self.conf.updateConf(data)
                        return

    def fetch_presence(self):
        if self.activated == False:
            self.client.activate()
            self.activated = True
            self.puuid = self.client.puuid
        return self.client.fetch_presence()

    def getPartyInv(self):
        data = []
        config = self.conf.fetchConfig()
        presenceData = self.client.fetch_presence()
        base_api_url = "https://colinhartigan.github.io/valorant-rpc?redir={0}&type={1}"
        base_api_url = f"{base_api_url}&region={self.client.region}&playername={self.client.player_name}&playertag={self.client.player_tag}" # add on static values (region/playername)
        if int(presenceData["partySize"]) < int(presenceData["maxPartySize"]):
            if presenceData["partyAccessibility"] == "OPEN" and config["presence"]["show_join_button_with_open_party"]:
                logging.debug(f"join link: "+ f"https://colinhartigan.github.io/valorant-rpc?redir=/valorant/join/{presenceData['partyId']}")
                return [{"label":"Join","url":f"https://colinhartigan.github.io/valorant-rpc?redir=/valorant/join/{presenceData['partyId']}&type=join"}]
            
            if presenceData["partyAccessibility"] == "CLOSED" and config["presence"]["allow_join_requests"]:
                return [{"label":"Request to Join","url":f"https://colinhartigan.github.io/valorant-rpc?redir=/valorant/request/{presenceData['partyId']}/{self.client.puuid}&type=request"}]
        