class Ship:
    def __init__(self, boxSize, x, y, orientation):  # boxSize corresponds to the ship's size
        self.boxSize = boxSize
        self.shipState = [False] * self.boxSize  # Initialize ship state

        self.shipPositionX = []
        self.shipPositionY = []

        self.shipPositionX.append(x)
        self.shipPositionY.append(y)
        print(f"First case placed at ({x}, {y})")

        if self.correct_orientation(x, y, orientation):
            self.place_ship(x, y, orientation)
            print(self.shipPositionX, self.shipPositionY)
        else:
            print("Invalid orientation or position for the ship.")

    def display_ship(self):
        print("Ship Coordinates:")
        for i in range(self.boxSize):
            print(f"({self.shipPositionX[i]}, {self.shipPositionY[i]})")

    def isShipDestroy(self):
        return all(self.shipState)

    def place_ship(self, x, y, orientation):
        for i in range(1, self.boxSize):
            if orientation == 1:  # Up
                self.shipPositionX.append(x)
                self.shipPositionY.append(y - i)
            elif orientation == 2:  # Down
                self.shipPositionX.append(x)
                self.shipPositionY.append(y + i)
            elif orientation == 3:  # Left
                self.shipPositionX.append(x - i)
                self.shipPositionY.append(y)
            elif orientation == 4:  # Right
                self.shipPositionX.append(x + i)
                self.shipPositionY.append(y)

    def correct_orientation(self, x, y, orientation):
        if orientation == 1 and y - self.boxSize + 1 < 1:
            return False
        elif orientation == 2 and y + self.boxSize - 1 > 10:
            return False
        elif orientation == 3 and x - self.boxSize + 1 < 1:
            return False
        elif orientation == 4 and x + self.boxSize - 1 > 10:
            return False
        return True

    def getSize(self):
        return self.boxSize
