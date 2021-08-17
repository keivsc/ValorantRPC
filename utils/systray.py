from PIL import Image
from pystray import Icon as icon, Menu as menu, MenuItem as item
import ctypes, os, urllib.request, sys, time, pyperclip
from .config.filepath import Filepath
from .config.config import Config

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hWnd = kernel32.GetConsoleWindow()

window_shown = False


class Systray:

    def __init__(self):
        self.conf = Config
        self.rank = self.conf.fetchConfig()["presence"]["show_rank"]
        
        pass

    def updateRank(self, icon, item):
        config = self.conf.fetchConfig()
        rank = config["presence"]["show_rank"]
        if rank == True:
            item.checked
            config["presence"]["show_rank"] = False
            self.conf.updateConf(config)
            self.rank = False
        else:
            config["presence"]["show_rank"] = True
            self.conf.updateConf(config)
            self.rank = True
            not item.checked
    def run(self):
        global window_shown
        Systray.generate_icon()
        systray_image = Image.open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'favicon.ico')))
        systray_menu = menu(
            item('Show window', Systray.tray_window_toggle, checked=lambda item: window_shown),
            item(f'Toggle Rank Display', self.updateRank, checked=lambda item: self.rank),
            item('Restart', Systray.restart),
            item('Exit', self.exitF)
        )
        self.systray = icon("ValorantRPC", systray_image, "ValorantRPC", systray_menu)
        self.systray.run()


    def exitF(self):
        self.systray.visible = False
        self.systray.stop()
        os._exit(1)

    def exit(self):
        return True


    @staticmethod
    def generate_icon():
        urllib.request.urlretrieve('https://raw.githubusercontent.com/colinhartigan/valorant-rpc/v2/favicon.ico',Filepath.get_path(os.path.join(Filepath.get_appdata_folder(),'favicon.ico')))


    @staticmethod
    def restart():
        user32.ShowWindow(hWnd, 1)
        os.system('cls' if os.name == 'nt' else 'clear')
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 

    @staticmethod
    def tray_window_toggle(icon,item):
        global window_shown
        try:
            window_shown = not item.checked
            if window_shown:
                user32.ShowWindow(hWnd, 1)
            else:
                user32.ShowWindow(hWnd, 0)
        except Exception as e:
            pass # oh no! bad python practices! 

