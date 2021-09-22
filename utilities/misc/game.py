import time
import psutil
import os
import json
from .config import Config
from colorama import Fore

class Game():
    def __init__(self) -> None:
        self.Config = Config()
        self.config = self.Config.fetchConfig()
        pass

    @staticmethod
    def are_processes_running(required_processes=["VALORANT-Win64-Shipping.exe", "RiotClientServices.exe"]):
        processes = []
        for proc in psutil.process_iter():
            processes.append(proc.name())
        
        return set(required_processes).issubset(processes)

    def start_game(self):
        path = self.get_rcs_path()
        launch_timeout = self.config["startup"]["launch_timeout"]
        launch_timer = 0
        running = True
        
        if not Game.are_processes_running():
            running = False
            psutil.subprocess.Popen([path, "--launch-product=valorant", "--launch-patchline=live"])
        while not Game.are_processes_running():
            print(f"{Fore.RED}[...] Waiting for VALORANT ({launch_timer}) - Timeout ({launch_timeout})", end="\r")
            launch_timer += 1
            if launch_timer >= launch_timeout:
               os._exit(1)
            time.sleep(1)
        if running == False:
            print()
            os.system('cls')
        print(f"{Fore.GREEN}[√] Valorant detected and running!")


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