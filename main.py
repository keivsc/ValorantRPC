from utilities.main import main
import traceback
from utilities.client import client, contentLoader
from utilities.misc import config, game
from utilities.presence import menus, ingame, pregame
from utilities import systray
import pystray._win32
import requests, time, psutil, ctypes, PIL, valclient, threading, os, json, sys, InquirerPy, iso8601, pyperclip, plyer
from colorama import Fore
from utilities.instancesManager import ProgramInstanceManager, OtherInstanceError

try:
    p = ProgramInstanceManager()
except OtherInstanceError:
    print(f"{Fore.RED}There is already another RPC running | Closing in 5 seconds")
    time.sleep(5)
    os._exit(1)

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

try:
    main(p)
except:
    print(f"{Fore.RED}An Exception has occured, save this error ask for help in the support discord")
    input(Fore.GREEN+traceback.format_exc())
