from .utils.matchLoader import Valorant
from .utils.imageBuilder import Builder

class Stats:
    def __init__(self, region, appdata):
        self.appdata = appdata
        self.region = region

    def loadImage(self):
        data = Valorant(region=self.region).load_match_data()
        builder = Builder(data, self.appdata)
        path = builder.build_image()
        path = path.replace('/', '\\')
        print(f"\nLatest Match Sheet Created: {path}")
        return path
