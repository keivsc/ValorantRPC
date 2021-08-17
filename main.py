try:
    from utils.systray import sys
    import time
    import os
    import traceback
    from utils.main import main
    import PIL
    from pystray._base import MenuItem as item
    import pystray._win32
    import pyperclip
    import plyer
    import requests
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


    main(__file__)
except Exception as e:
    input(e)

