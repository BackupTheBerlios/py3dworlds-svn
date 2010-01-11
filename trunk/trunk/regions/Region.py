from databases.constants import constants
from utils.Utils import Utils

class Region(constants,  Utils):
    def __init__(self):
        constants.__init__(self)
        Utils.__init__(self)

    def getRegionHandle(self,  x,  y):
        return  self.make64BitInt(x * self.RegionSize,   y * self.RegionSize);

    def getRegionHandleList(self, x, y):
        liRegion = []
        liRegion.append(x*self.RegionSize)
        liRegion.append(y*self.RegionSize)
        return liRegion
        
    def getRegionHandleXY(self, x, y):
         return x*self.RegionSize,  y*self.RegionSize
         
