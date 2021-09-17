from .utils.matchLoader import Valorant
from .utils.imageBuilder import Builder
from plyer import notification
import os
from colorama import Fore
class Stats:
    def __init__(self, region, appdata):
        self.appdata = appdata
        self.region = region

    def loadImage(self):
        data = self.getData()
        if data == False:
            notification.notify(
                title='Unable to create Match Sheet!',
                message='Your last 5 games were DEATHMATCHES!',
                app_icon=os.path.join(os.path.join(os.getenv('APPDATA'), 'ValorantRPC'), 'favicon.ico')
            )
            return False

        if f"{data['match_id']}.png" in os.listdir(os.path.join(os.getenv('APPDATA'), 'ValorantRPC/matchStats/output')):
            path = os.path.join(os.getenv('APPDATA'), 'ValorantRPC/matchStats/output/')+f"{data['match_id']}.png"
            print(f"\n{Fore.RED}Match Report Already Exist in {path}")
            return path.replace("/","\\")
        else:
            builder = Builder(data, self.appdata)
            path = builder.build_image()
            path = path.replace('/', '\\')
            print(f"\n{Fore.GREEN}Latest Match Report Created: {path}")
            return path.replace("/","\\")
    
    def getData(self):
        data = Valorant(region=self.region).load_match_data()
        return data

