from Box import *
from Ship import *
import numpy as np
class Player():
    def __self__(self):
        self.board = np.full((10,10), Box.VIDE)
        self.porteAvion = Ship(5) # Constructor will ask himself for board position
        self.destroyer1 = Ship(2)
        self.destroyer2 = Ship(2)
        self.destroyer3 = Ship(2)
        self.croiser1 = Ship(3)
        self.croiser2 = Ship(3)
        self.sousMarin = Ship(3)
        self.ships = np.array([self.porteAvion, self.destroyer1, self.destroyer2, self.destroyer3, self.croiser1, self.croiser2, self.sousMarin])
