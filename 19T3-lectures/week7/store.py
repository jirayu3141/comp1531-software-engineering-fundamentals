class Coords:
    def __init__(self):
        self.theta = 0.13 # radians
        self.r = 9
    
    def getX(self):
        return self.r * math.cos(self.theta)

    def getY(self):
        return self.r * math.sin(self.theta)
