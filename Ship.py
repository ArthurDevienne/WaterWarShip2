import numpy as np
class Ship:
    def __init__(self, boxSize): #boxSize correspond to the ship's size
        self.boxSize = boxSize
        self.shipState = []
        for i in range(0,self.boxSize): # init ship state
            self.shipState[i] = False

        self.shipPosition = {}
        for i in range(self.shipPosition): # En Chantier
            self.x = int(input(f"Enter x{i} : "))
            self.y = int(input(f"Enter y{i} : "))
            self.shipPosition[ self.x ] = self.y
