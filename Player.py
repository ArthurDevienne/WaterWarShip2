from Box import *
from Ship import *
import numpy as np
class Player():
    def __self__(self):
        self.board = np.full((10,10), Box.VIDE)
        self.porteAvion = Ship(int(input("Enter porteAvion length"))) # Constructor will ask himself for board position
        self.destroyer1 = Ship(int(input("Enter destroyer1 length")))
        self.destroyer2 = Ship(int(input("Enter destroyer2 length")))
        self.destroyer3 = Ship(int(input("Enter destroyer3 length")))
        self.patrouiller1 = Ship(int(input("Enter patrouiller1 length")))
        self.patrouiller2 = Ship(int(input("Enter patrouiller2 length")))
        self.sousMarin = Ship(int(input("Enter sousMarin length")))
        self.ships = np.array([self.porteAvion, self.destroyer1, self.destroyer2, self.destroyer3, self.patrouiller1, self.patrouiller2, self.sousMarin])
