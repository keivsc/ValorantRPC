from .utils.matchLoader import Valorant
from .utils.imageBuilder import Builder

class Stats:
    def __init__(self, region, appdata):
        self.data = Valorant(region=region).load_match_data()
        self.appdata = appdata

    def loadImage(self):
        builder = Builder(self.data, self.appdata)
        path = builder.build_image()
        path = path.replace('/', '\\')
        print(f"\nLatest Match Sheet Created: {path}")
        return path
