from utilities.main import main
import traceback
from utilities.client import client, contentLoader
from utilities.misc import config, game
from utilities.presence import menus, ingame, pregame
from utilities import systray
import pystray._win32
import requests, time, psutil, ctypes, PIL, valclient, threading, os, json, sys, InquirerPy, iso8601, pyperclip, plyer


print(r""" 
 __     __           __                                           __      _______   _______    ______  
/  |   /  |         /  |                                         /  |    /       \ /       \  /      \ 
$$ |   $$ | ______  $$ |  ______    ______   ______   _______   _$$ |_   $$$$$$$  |$$$$$$$  |/$$$$$$  |
$$ |   $$ |/      \ $$ | /      \  /      \ /      \ /       \ / $$   |  $$ |__$$ |$$ |__$$ |$$ |  $$/ 
$$  \ /$$/ $$$$$$  |$$ |/$$$$$$  |/$$$$$$  |$$$$$$  |$$$$$$$  |$$$$$$/   $$    $$< $$    $$/ $$ |      
 $$  /$$/  /    $$ |$$ |$$ |  $$ |$$ |  $$/ /    $$ |$$ |  $$ |  $$ | __ $$$$$$$  |$$$$$$$/  $$ |   __ 
  $$ $$/  /$$$$$$$ |$$ |$$ \__$$ |$$ |     /$$$$$$$ |$$ |  $$ |  $$ |/  |$$ |  $$ |$$ |      $$ \__/  |
   $$$/   $$    $$ |$$ |$$    $$/ $$ |     $$    $$ |$$ |  $$ |  $$  $$/ $$ |  $$ |$$ |      $$    $$/ 
    $/     $$$$$$$/ $$/  $$$$$$/  $$/       $$$$$$$/ $$/   $$/    $$$$/  $$/   $$/ $$/        $$$$$$/  
                                                                                                       
                                                                                                       
                                                                                                    """)
try:
    main()
except:
    print("An Exception has occured, save this error ask for help in the support discord")
    input(traceback.format_exc())
