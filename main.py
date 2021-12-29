from src.utils.game import Game
from src import states
from src.tray import sysrun
from src.utils.config import Config
from src.webserver.server import webrun
from src.utils.client import Client
from src.states import *
from threading import Thread
from colorama import Fore
import os
import pypresence
import psutil
import time
import requests
import sys
import traceback

psutil.subprocess.Popen([Game.get_rcs_path(), "--launch-product=valorant", "--launch-patchline=live"])

print(f""" {Fore.RED}
________________
|  __      __  |       :::     :::     :::     :::        ::::::::  :::::::::      :::     ::::    ::: ::::::::::: 
|  \ \    / /  |      :+:     :+:   :+: :+:   :+:       :+:    :+: :+:    :+:   :+: :+:   :+:+:   :+:     :+:      
|   \ \  / /   |     +:+     +:+  +:+   +:+  +:+       +:+    +:+ +:+    +:+  +:+   +:+  :+:+:+  +:+     +:+   
|    \ \/ /    |    +#+     +:+ +#++:++#++: +#+       +#+    +:+ +#++:++#:  +#++:++#++: +#+ +:+ +#+     +#+     
|     \  /     |    +#+   +#+  +#+     +#+ +#+       +#+    +#+ +#+    +#+ +#+     +#+ +#+  +#+#+#     +#+
|      \/      |    #+#+#+#   #+#     #+# #+#       #+#    #+# #+#    #+# #+#     #+# #+#   #+#+#     #+#    
|______________|     ###     ###     ### ########## ########  ###    ### ###     ### ###    ####     ###    
""")

print(f"""{Fore.GREEN}
               |    :::::::::  :::::::::   ::::::::  
               |    :+:    :+: :+:    :+: :+:    :+: 
               |    +:+    +:+ +:+    +:+ +:+        
               |    +#++:++#:  +#++:++#+  +#+        
               |    +#+    +#+ +#+        +#+        
               |    #+#    #+# #+#        #+#    #+# 
               |    ###    ### ###         ########  
""")
config = Config()
config.check()
try:
    requests.get(f'http://127.0.0.1:{config.fetch_config()["server"]["port"]}/game').json()
    print(f"{Fore.RED}Another Instance of VALORANTRPC is already on!")
    for x in range(5, -1, -1):
        print(f"[!] Closing in {x}...", end="\r")
        time.sleep(1)
    os._exit(1)
except Exception:
    pass

game = Game(config)
game.start_game()
Thread(target=sysrun, args=(config,), name="Thread | System Tray").start()
conf = config.fetch_config()
rpc = pypresence.Client(client_id=conf['clientID'])
valorant = Client(conf['region'])
game.autoRegion(valorant.client)
Thread(target=webrun, args=(conf['server']['port'], valorant, ), name="Thread | Web Server").start()
rpc.start()
os.system('cls')
print(f""" {Fore.RED}
________________
|  __      __  |       :::     :::     :::     :::        ::::::::  :::::::::      :::     ::::    ::: ::::::::::: 
|  \ \    / /  |      :+:     :+:   :+: :+:   :+:       :+:    :+: :+:    :+:   :+: :+:   :+:+:   :+:     :+:      
|   \ \  / /   |     +:+     +:+  +:+   +:+  +:+       +:+    +:+ +:+    +:+  +:+   +:+  :+:+:+  +:+     +:+   
|    \ \/ /    |    +#+     +:+ +#++:++#++: +#+       +#+    +:+ +#++:++#:  +#++:++#++: +#+ +:+ +#+     +#+     
|     \  /     |    +#+   +#+  +#+     +#+ +#+       +#+    +#+ +#+    +#+ +#+     +#+ +#+  +#+#+#     +#+
|      \/      |    #+#+#+#   #+#     #+# #+#       #+#    #+# #+#    #+# #+#     #+# #+#   #+#+#     #+#    
|______________|     ###     ###     ### ########## ########  ###    ### ###     ### ###    ####     ###    
""")

print(f"""{Fore.GREEN}
               |    :::::::::  :::::::::   ::::::::  
               |    :+:    :+: :+:    :+: :+:    :+: 
               |    +:+    +:+ +:+    +:+ +:+        
               |    +#++:++#:  +#++:++#+  +#+        
               |    +#+    +#+ +#+        +#+        
               |    #+#    #+# #+#        #+#    #+# 
               |    ###    ### ###         ########  
""")

rpcData = {}
rpcData["details"] = "Loading..."
rpcData["buttons"] = []
rpcData["buttons"].append({"label":"View on GitHHub", "url":"https://github.com/keivsc/ValorantRPC"})
rpcData["large_image"] = "game_icon"
rpcData["large_text"] = "VALORANT"
rpcData["small_image"] = "github_icon"
rpcData["small_text"] = "keivsc/ValorantRPC"
rpc.set_activity(**rpcData)
buts = conf['presence']['buttons']
buttons = None
for x in range(2):
    button = buts[f'button{x+1}']
    try:
        if button['activate'] == True:
            if buttons == None:
                buttons = []
            button.pop('activate')
            buttons.append(button)
    except:
        pass
class RPC:
    @staticmethod
    def set_activity(data):
        rpc.set_activity(**data, buttons=buttons)

status = game.are_processes_running()

while status:
    status = game.are_processes_running()
    if status == False:
        os._exit(1)
    presence = valorant.get_presence()
    if presence == None:
        time.sleep(conf['presence']['refreshRate'])
        continue
    state = presence['sessionLoopState']
    presences = {
        "MENUS":states.MENUS.Menus(valorant, RPC, config),
        "CUSTOM_GAME_SETUP":states.MENUS.Menus(valorant, RPC, config),
        "INGAME":states.INGAME.InGame(valorant, RPC, config),
        "PREGAME":states.PREGAME.PreGame(valorant, RPC, config)
    }
    presences[state].start_presence()
    time.sleep(conf['presence']['refreshRate'])
os._exit(1)
