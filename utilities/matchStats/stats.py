from .utils.matchLoader import Valorant
from .utils.imageBuilder import Builder
from plyer import notification
import os

class Stats:
    def __init__(self, region, appdata):
        self.appdata = appdata
        self.region = region

    def loadImage(self):
        data = Valorant(region=self.region).load_match_data()
        if data == False:
            notification.notify(
                title='Unable to create Match Sheet!',
                message='Your last 5 games were DEATHMATCHES!',
                app_icon=os.path.join(os.path.join(os.getenv('APPDATA'), 'ValorantRPC'), 'favicon.ico')
            )
            return False
        builder = Builder(data, self.appdata)
        path = builder.build_image()
        path = path.replace('/', '\\')
        print(f"\nLatest Match Sheet Created: {path}")
        return path
