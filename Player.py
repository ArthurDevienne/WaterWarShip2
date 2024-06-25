from Box import *
from Ship import *
import numpy as np
class Player():
    def __init__(self):
        self.board = np.full((10,10), Box.VIDE)
        # Create a test system to pass creation of ship
        self.porteAvion = Ship(5) # Constructor will ask himself for board position
        self.destroyer1 = Ship(2)
        self.destroyer2 = Ship(2)
        self.destroyer3 = Ship(2)
        self.croiser1 = Ship(3)
        self.croiser2 = Ship(3)
        self.sousMarin = Ship(3)
        self.ships = np.array([self.porteAvion, self.destroyer1, self.destroyer2, self.destroyer3, self.croiser1, self.croiser2, self.sousMarin])
        self.fireListX = []
        self.fireListY = []

    def fire(self, enemy):
        pointX = int(input("X axis fire ? : "))
        pointY = int(input("y axis fire ? : "))
        
        self.fireListX.append(pointX)
        self.fireListX.append(pointY)

        state = enemy.isTouched(enemy, pointX, pointY)
        if state == 1:
            print(f"You toutch a the point : { pointX }, { pointY } ")
        elif state == 2:
            print("You Destroy the ship")
        else:
            print("You shoot in the water")

    def isTouched(self, enemy, pointX, pointY):
        for ship in enemy.ships:
            for i in range(1, len(ship)):
                if pointX == ship.shipPositionX[i] and pointY == ship.shipPositionY[i]:
                    ship.shipState[i] = True
                    if ship.isShipDestroy():
                        return 2
                    return 1
                else:
                    return 0

    def isAllShipDestroy(self):
        for ship in self.ships:
            if not ship.isShipDestroy:
                return False
            else:
                return True