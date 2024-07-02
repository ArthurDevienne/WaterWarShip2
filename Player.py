import numpy as np
from Box import Box
from Ship import Ship

class Player:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = np.full((10, 10), Box.VIDE)
        self.fireBoard = np.full((10, 10), Box.VIDE)
        self.ships = []
        self.fireList = set()
        self.reset_fire_history()

    def reset_fire_history(self):
        self.fire_history = set()

    def place_ship_on_board(self, ship):
        for i in range(ship.getSize()):
            x, y = ship.shipPositionX[i], ship.shipPositionY[i]
            if 0 <= x-1 < 10 and 0 <= y-1 < 10:  # Verify position is within bounds
                self.board[y-1][x-1] = Box.TOUCHE

    def fire(self, enemy, pointX, pointY):
        if (pointX, pointY) in self.fireList:
            print("You have already fired at this position. Try again.")
            return self.fire(enemy, pointX, pointY)

        self.fireList.add((pointX, pointY))
        state = enemy.isTouched(self, pointX, pointY)
        if state == 1:
            print(f"You touched a ship at the point: {pointX + 1}, {pointY + 1}")
            self.fireBoard[pointY][pointX] = Box.TOUCHE
            return "TOUCHE"
        elif state == 2:
            print("You destroyed the ship")
            self.update_sunk_ship(enemy, pointX, pointY)
            return "COULE"
        else:
            print("You shot in the water")
            self.fireBoard[pointY][pointX] = Box.EAU
            return "RATE"

    def update_sunk_ship(self, enemy, pointX, pointY):
        for ship in enemy.ships:
            if ship.isShipDestroy():
                for i in range(ship.getSize()):
                    x, y = ship.shipPositionX[i], ship.shipPositionY[i]
                    self.fireBoard[y-1][x-1] = Box.COULE

    def isTouched(self, player, pointX, pointY):
        for ship in self.ships:
            for i in range(ship.getSize()):
                if pointX+1 == ship.shipPositionX[i] and pointY+1 == ship.shipPositionY[i]:
                    ship.shipState[i] = True
                    if ship.isShipDestroy():
                        player.update_sunk_ship(self, pointX, pointY)
                        return 2
                    return 1
        return 0

    def isAllShipDestroy(self):
        for ship in self.ships:
            if not ship.isShipDestroy():
                return False
        return True

    def _correctFirstCoord(self, x, y, size):
        if x < 1 or x > 10 or y < 1 or y > 10:
            print("Invalid position. Please try again.")
            return False
        for ship in self.ships:
            for i in range(ship.getSize()):
                if x == ship.shipPositionX[i] and y == ship.shipPositionY[i]:
                    print("Invalid position. Please try again.")
                    return False
        return True

    def _chooseFirstCoord(self, size):
        print(f"Please choose the first coordinate of the ship of size {size}:")
        x = int(input("Enter x (1-10): "))
        y = int(input("Enter y (1-10): "))
        if self._correctFirstCoord(x, y, size):
            return x, y
        else:
            return self._chooseFirstCoord(size)

    def _choose_orientation(self, x, y, size):
        print("Please choose the orientation of the ship:")
        print("1. Up")
        print("2. Down")
        print("3. Left")
        print("4. Right")
        orientation = int(input())
        if self._correct_orientation(x, y, orientation, size):
            return orientation
        else:
            return self._choose_orientation(x, y, size)

    def _correct_orientation(self, x, y, orientation, size):
        if orientation == 1:  # Up
            if y - size < 1:
                print("Invalid position. Please try again.")
                return False
            for i in range(size):
                if not self._correctFirstCoord(x, y - i, size):
                    return False
        elif orientation == 2:  # Down
            if y + size - 1 > 10:
                print("Invalid position. Please try again.")
                return False
            for i in range(size):
                if not self._correctFirstCoord(x, y + i, size):
                    return False
        elif orientation == 3:  # Left
            if x - size < 1:
                print("Invalid position. Please try again.")
                return False
            for i in range(size):
                if not self._correctFirstCoord(x - i, y, size):
                    return False
        elif orientation == 4:  # Right
            if x + size - 1 > 10:
                print("Invalid position. Please try again.")
                return False
            for i in range(size):
                if not self._correctFirstCoord(x + i, y, size):
                    return False
        else:
            print("Invalid orientation. Please try again.")
            return False
        return True

    def displayFireBoard(self):
        print("Fire Board:")
        for i in range(10):
            for j in range(10):
                if self.fireBoard[i][j] == Box.VIDE:
                    print(".", end=" ")
                elif self.fireBoard[i][j] == Box.EAU:
                    print("O", end=" ")
                elif self.fireBoard[i][j] == Box.TOUCHE:
                    print("X", end=" ")
                elif self.fireBoard[i][j] == Box.COULE:
                    print("C", end=" ")
            print()
        print()

    def displayBoard(self):
        print("Board:")
        for i in range(10):
            for j in range(10):
                if self.board[i][j] == Box.VIDE:
                    print(".", end=" ")
                elif self.board[i][j] == Box.TOUCHE:
                    print("S", end=" ")  # 'S' to represent ship
            print()
        print()

    def create_ships(self):
        ship_sizes = [5, 4, 3, 3, 2]
        for size in ship_sizes:
            while True:
                x = np.random.randint(1, 11)
                y = np.random.randint(1, 11)
                orientation = np.random.randint(1, 5)
                if self._correct_orientation(x, y, orientation, size) and self._is_position_valid(x, y, orientation, size):
                    ship = Ship(size, x, y, orientation)
                    self.ships.append(ship)
                    self.place_ship_on_board(ship)
                    break

    def _is_position_valid(self, x, y, orientation, size):
        if orientation == 1:  # Up
            for i in range(size):
                if y - 1 - i < 0 or self.board[y - 1 - i][x - 1] != Box.VIDE:
                    return False
        elif orientation == 2:  # Down
            for i in range(size):
                if y - 1 + i > 9 or self.board[y - 1 + i][x - 1] != Box.VIDE:
                    return False
        elif orientation == 3:  # Left
            for i in range(size):
                if x - 1 - i < 0 or self.board[y - 1][x - 1 - i] != Box.VIDE:
                    return False
        elif orientation == 4:  # Right
            for i in range(size):
                if x - 1 + i > 9 or self.board[y - 1][x - 1 + i] != Box.VIDE:
                    return False
        return True
