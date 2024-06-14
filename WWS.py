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
            self.human1.displayRoundGame() # Display game board
            self.human1.shoot() # Shoot then display update game board
            self.ai1.shoot() # Same
            self.updateEndGame(self) # Check if players have 0 ships and in this case turn endGame to true and stop the game

    def updateEndGame(self):
        if self.human1.ships == 0 or self.ai1.ships == 0:
            self.endGame = True