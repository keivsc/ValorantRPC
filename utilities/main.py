from .presence import ValRPC
import pypresence
from .config.config import Config, Filepath
from .game import Game
import os
import threading
from PIL import Image
from pystray import Icon as icon, Menu as menu, MenuItem as item
import ctypes, os, urllib.request, sys, time, pyperclip
import asyncio
from .systray import Systray

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hWnd = kernel32.GetConsoleWindow()




def close(systray=None):
    Systray.systray.stop()
    Systray.systray.visible = False
    os._exit(1)

def startup(systray=None):
    asyncio.set_event_loop(asyncio.new_event_loop())
    rpcData ={
        "pid":os.getpid()
    }
    rpcData["details"] = f"Loading..."
    rpcData["buttons"] = []
    rpcData["buttons"].append({"label":"View on GitHHub", "url":"https://github.com/keivsc/ValorantRPC"})
    rpcData["large_image"] = "game_icon"
    rpcData["large_text"] = "keivsc/ValorantRPC"
    rpcData["small_image"] = "github_icon"
    rpcData["small_text"] = "keivsc/ValorantRPC"

    rpcClient = pypresence.Client(client_id=Config.fetchConfig()["clientID"])
    rpcClient.start()
    rpcClient.set_activity(**rpcData)
    print(f"Client language: {Config.fetchConfig()['language']}")
    game = Game().start_game()
    if game == False:
        os._exit(1)
    for x in range(5, -1, -1):
        print(f"[...] RPC Started! Hiding window in ({x})", end="\r")
        time.sleep(1)
    print()
    print("Hiding Window! Have fun playing!!")
    time.sleep(.5)
    user32.ShowWindow(hWnd, 0)
    client = ValRPC(rpcClient)
    client.startPresence()
    close(systray)

def main():
    systray = Systray()
    Config.checkConfig()
    thread = threading.Thread(target=systray.run)
    thread.start()
    startup(systray)
    

