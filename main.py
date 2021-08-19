### imports for exe installer
import pypresence
import pystray._win32
import valclient
from utilities.presence import ValRPC
import traceback
from utilities.main import main
import json
import os
import requests
import sys
from PIL import Image
from pystray import Icon as icon, Menu as menu, MenuItem as item
import ctypes, os, urllib.request, sys, time, pyperclip
from utilities.config.config import Config, Filepath
from utilities.clientMain import Client
from utilities.config.config import Config
import time
from utilities.presence import ValRPC
from utilities.game import Game
import threading
import asyncio
from utilities.systray import Systray
import psutil
from utilities.content import Loader
import iso8601

### ---
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
except Exception as e:
    traceback.print_exc()
    input()