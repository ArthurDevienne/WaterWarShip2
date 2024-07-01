from Player import Player
from Box import Box
from Ship import Ship

class Human(Player):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.fire_history = set()  # Ajout de l'attribut fire_history

    def create_ships(self):
        self.reset()
        ship_sizes = [5, 4, 3, 3, 2]  # Example ship sizes
        for size in ship_sizes:
            x, y = self._chooseFirstCoord(size)
            orientation = self._choose_orientation(x, y, size)
            while not (self._correct_orientation(x, y, orientation, size) and self._is_position_valid(x, y, orientation, size)):
                print("Invalid position or orientation, please choose again.")
                x, y = self._chooseFirstCoord(size)
                orientation = self._choose_orientation(x, y, size)
            ship = Ship(size, x, y, orientation)
            self.ships.append(ship)
            self.place_ship_on_board(ship)

    def _chooseFirstCoord(self, size):
        print(f"Please choose the first coordinate of the ship of size {size}:")
        x = int(input("Enter x (1-10): "))
        y = int(input("Enter y (1-10): "))
        while not self._correctFirstCoord(x, y, size):
            print("Invalid position. Please try again.")
            x = int(input("Enter x (1-10): "))
            y = int(input("Enter y (1-10): "))
        return x, y

    def _choose_orientation(self, x, y, size):
        print("Please choose the orientation of the ship:")
        print("1. Up")
        print("2. Down")
        print("3. Left")
        print("4. Right")
        orientation = int(input())
        while not self._correct_orientation(x, y, orientation, size):
            print("Invalid orientation. Please try again.")
            orientation = int(input("Choose orientation (1-4): "))
        return orientation

    def displayRoundGame(self):
        self.displayBoard()
        self.displayFireBoard()

    def shoot(self, enemy):
        while True:
            try:
                x = int(input("Enter X coordinate (1-10): ")) - 1
                y = int(input("Enter Y coordinate (1-10): ")) - 1
                if 0 <= x < 10 and 0 <= y < 10 and (x, y) not in self.fire_history:
                    self.fire_history.add((x, y))
                    result = self.fire(enemy, x, y)
                    return x, y, result
                else:
                    print("Invalid coordinates or already fired at this position. Try again.")
            except ValueError:
                print("Invalid input. Please enter numbers between 1 and 10.")
