from .misc.config import Config, configActivate
from .client.client import prompt, Client
from .misc.game import Game
import os
from .presence import ingame, menus, pregame
from .systray import systray
import threading
import pypresence
import time
from pystray import Icon as icon, Menu as menu, MenuItem as item
import ctypes, os, urllib.request, sys, time, pyperclip
import traceback

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hWnd = kernel32.GetConsoleWindow()

def main():
    configActivate()
    Config().checkConfig()
    config = Config().fetchConfig()
    if config['language'] not in config['languages']:
        prompt().promptLanguage(config, Config())
    game = Game()
    thread = threading.Thread(target=systray().run)
    thread.start()
    rpcClient = pypresence.Client(client_id=config["clientID"])
    game.start_game()
    valClient = Client()
    valClient.client.activate()
    rpcClient.start()
    rpcData = {
        'pid':os.getpid()
    }
    rpcData["details"] = f"Loading..."
    rpcData["buttons"] = []
    rpcData["buttons"].append({"label":"View on GitHHub", "url":"https://github.com/keivsc/ValorantRPC"})
    rpcData["large_image"] = "game_icon"
    rpcData["large_text"] = "Valorant"
    rpcData["small_image"] = "github_icon"
    rpcData["small_text"] = "https://github.com/keivsc/ValorantRPC"
    rpcClient.set_activity(**rpcData)
    for x in range(5, -1, -1):
        print(f"[...] RPC Started! Hiding window in ({x})", end="\r")
        time.sleep(1)
    print()
    print("Hiding Window! Have fun playing!!")
    time.sleep(.5)
    user32.ShowWindow(hWnd, 0)


    while True:

        if not game.are_processes_running(["RiotClientServices.exe"]):
            os._exit(1)

        try:
            presence = valClient.fetchPresence(config)
        except:
            input(traceback.format_exc())
            os._exit(1)
        rpcData = {
            "pid":os.getpid()
        }
        if presence == None:
            rpcData["details"] = f"Loading..."
            rpcData["buttons"] = []
            rpcData["buttons"].append({"label":"View on GitHHub", "url":"https://github.com/keivsc/ValorantRPC"})
            rpcData["large_image"] = "game_icon"
            rpcData["large_text"] = "Valorant"
            rpcData["small_image"] = "github_icon"
            rpcData["small_text"] = "https://github.com/keivsc/ValorantRPC"
            try:
                rpcClient.set_activity(**rpcData)
            except:
                print("Unable to Connect to discord is discord opened?")
                pass
        else:
            presences = {
                "INGAME":ingame,
                "MENUS":menus,
                "PREGAME":pregame
            }
            try:
                presences[presence['sessionLoopState']].Presence(rpcClient).startPresence()
            except:
                pass
    
