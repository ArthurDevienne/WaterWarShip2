import Human
import AI
class WWS:
    def __init__(self):
        print("game created")
        self.human1 = Human.Human("Jonny")
        self.ai1 = AI.AI()
        self.endGame = False

    def start(self):
        print("Starting Game")
        while self.endGame != False:
            self.human1.displayRoundGame() # Display game board not impemented
            self.human1.shoot(self.ai1) # Shoot then display update game board not impemented
            self.ai1.shoot(self.human1) # Same not impemented
            self.updateEndGame(self) # Check if players have 0 ships and in this case turn endGame to true and stop the game

    def updateEndGame(self):
        if self.human1.ships == 0 or self.ai1.ships == 0:
            self.endGame = True