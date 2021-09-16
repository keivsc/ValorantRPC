from utilities.main import main
import traceback
from utilities.client import client, contentLoader
from utilities.misc import config, game
from utilities.presence import menus, ingame, pregame
from utilities import systray
import pystray._win32
import requests, time, psutil, ctypes, PIL, valclient, threading, os, json, sys, InquirerPy, iso8601, pyperclip, plyer
from colorama import Fore

print(f""" {Fore.RED}
__________________
|   __      __   |       :::     :::     :::     :::        ::::::::  :::::::::      :::     ::::    ::: ::::::::::: 
|   \ \    / /   |      :+:     :+:   :+: :+:   :+:       :+:    :+: :+:    :+:   :+: :+:   :+:+:   :+:     :+:      
|    \ \  / /    |     +:+     +:+  +:+   +:+  +:+       +:+    +:+ +:+    +:+  +:+   +:+  :+:+:+  +:+     +:+   
|     \ \/ /     |    +#+     +:+ +#++:++#++: +#+       +#+    +:+ +#++:++#:  +#++:++#++: +#+ +:+ +#+     +#+     
|      \  /      |    +#+   +#+  +#+     +#+ +#+       +#+    +#+ +#+    +#+ +#+     +#+ +#+  +#+#+#     +#+
|       \/       |    #+#+#+#   #+#     #+# #+#       #+#    #+# #+#    #+# #+#     #+# #+#   #+#+#     #+#    
|________________|     ###     ###     ### ########## ########  ###    ### ###     ### ###    ####     ###    
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
    main()
except:
    print(f"{Fore.RED}An Exception has occured, save this error ask for help in the support discord")
    input(Fore.GREEN+traceback.format_exc())
