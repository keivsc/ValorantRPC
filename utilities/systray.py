from PIL import Image
from pystray import Icon as icon, Menu as menu, MenuItem as item
import ctypes, os, urllib.request, sys, time, pyperclip
from .misc.config import Config
from .matchStats.stats import Stats
from plyer import notification
from .misc.game import Game
from PIL import Image

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hWnd = kernel32.GetConsoleWindow()

window_shown = False

class systray:
    def __init__(self):
        self.Config = Config()
        self.config = self.Config.fetchConfig()
        self.systray = None
        self.showRank = self.config["presence"]["show_rank"]
        self.party = self.config["presence"]["show_party_count"]
        self.game = Game()
        self.stat = Stats(self.config['region'], self.Config)

    def updateRank(self, icon, item):
        config = self.Config.fetchConfig()
        rank = config["presence"]["show_rank"]
        if rank == True:
            item.checked
            config["presence"]["show_rank"] = False
            self.Config.updateConf(config)
            self.showRank = False
        else:
            config["presence"]["show_rank"] = True
            self.Config.updateConf(config)
            self.showRank = True
            not item.checked

    def updateParty(self, icon, item):
        config = self.Config.fetchConfig()
        party = config["presence"]["show_party_count"]
        if party == True:
            item.checked
            config["presence"]["show_party_count"] = False
            self.Config.updateConf(config)
            self.party = False
        else:
            config["presence"]["show_party_count"] = True
            self.Config.updateConf(config)
            self.party = True
            not item.checked

    def matchStatsImage(self):
        if self.game.are_processes_running() == True:
            if self.config['matchSheet'] == True:
                notification.notify(
                    title='Creating Match Report!',
                    message='Match Report will be created in a few seconds!',
                    app_icon=self.Config.get_path(os.path.join(self.Config.get_appdata_folder(), 'favicon.ico'))
                )
                path = self.stat.loadImage()
                notification.notify(
                    title='Match Report Created!',
                    message='You can get the path in the console window!',
                    app_icon=self.Config.get_path(os.path.join(self.Config.get_appdata_folder(), 'favicon.ico'))
                )
                Image.open(path).show()
            else:
                notification.notify(
                    title='Unable to create match report',
                    message='Enable matchSheet creation in the config file!',
                    app_icon=self.Config.get_path(os.path.join(self.Config.get_appdata_folder(), 'favicon.ico'))
                )
        else:
            notification.notify(
                title='Unable to create match report',
                message='Please wait until VALORANT is opened!',
                app_icon=self.Config.get_path(os.path.join(self.Config.get_appdata_folder(), 'favicon.ico'))
            )

    def run(self):
        global window_shown
        self.generate_icon()
        systray_image = Image.open(self.Config.get_path(os.path.join(self.Config.get_appdata_folder(), 'favicon.ico')))
        systray_menu = menu(
            item('Show window', systray.tray_window_toggle, checked=lambda item: window_shown),
            item('Create Latest Match Report (Image)', self.matchStatsImage),
            item('RPC Settings', menu(
                item(f'Toggle Rank Display', self.updateRank, checked=lambda item: self.showRank),
                item(f'Toggle Party Display', self.updateParty, checked=lambda item: self.party),
            )),
            item('Restart', systray.restart),
            item('Exit', self.exitF)
        )
        self.systray = icon("ValorantRPC", systray_image, "ValorantRPC", systray_menu)
        self.systray.run()

    def exitF(self):
        self.systray.visible = False
        self.systray.stop()
        os._exit(1)

    def generate_icon(self):
        urllib.request.urlretrieve('https://raw.githubusercontent.com/keivsc/ValorantRPC/v1/favicon.ico',self.Config.get_path(os.path.join(self.Config.get_appdata_folder(),'favicon.ico')))

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
        except:
            pass 