from Player import *

class Human(Player):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def displayRoundGame():
        # display 2 board : place where we fire (enemy board without ship) and our board
        super().board # display current player Board
        super().displayFireBoard()