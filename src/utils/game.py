import time
import psutil
import os
import json
from colorama import Fore
import sys

class Game():
    def __init__(self, config) -> None:
        self.Config = config
        self.config = self.Config.fetch_config()

    @staticmethod
    def are_processes_running(required_processes=["VALORANT-Win64-Shipping.exe", "RiotClientServices.exe"]):
        processes = []
        
        for proc in psutil.process_iter():
            processes.append(proc.name())
         
        return set(required_processes).issubset(processes)

    def start_game(self):
        path = Game.get_rcs_path()
        launch_timeout = self.config["startup"]["launch_timeout"]
        launch_timer = 0
        running = True
        
        if not Game.are_processes_running():
            psutil.subprocess.Popen([path, "--launch-product=valorant", "--launch-patchline=live"])
        while not Game.are_processes_running():
            print(f"{Fore.RED}[...] Waiting for VALORANT ({launch_timer}) - Timeout ({launch_timeout})", end="\r")
            launch_timer += 1
            if launch_timer >= launch_timeout:
                os._exit(1)
            time.sleep(1)
        print(" "*100, end='\r')
        print(f"{Fore.GREEN}[√] Valorant detected!")

    def autoRegion(self, client):
        config = self.Config.fetch_config()
        print(f"{Fore.GREEN}--------------------------")
        print(f"{Fore.BLUE}Auto detecting region...")
        sessions = client.riotclient_session_fetch_sessions()
        for _, session in sessions.items():
            if session["productId"] == "valorant":
                launch_args = session["launchConfiguration"]["arguments"]
                for arg in launch_args:
                    if "-ares-deployment" in arg:
                        region = arg.replace("-ares-deployment=","")
                        if region.lower() == config['region'].lower():
                            print(f"Region Correct - {Fore.GREEN}{region.upper()}")
                            print("--------------------------")
                            time.sleep(1)
                            return
                        data = config
                        data["region"] = region
                        self.Config.update(data)
                        print(f"{Fore.BLUE}Region Detected - {Fore.GREEN}{region.upper()}")
                        print("--------------------------")
                        time.sleep(1)
                        os.startfile(os.path.abspath(sys.argv[0]))
                        os._exit(1)

    @staticmethod
    def get_rcs_path():
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