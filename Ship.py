class Ship:
    def __init__(self, boxSize): # boxSize corresponds to the ship's size
        self.boxSize = boxSize
        self.shipState = [False] * self.boxSize # Initialize ship state

        self.shipPositionX = []
        self.shipPositionY = []

        self.shipPositionCorrect = False
        while not self.shipPositionCorrect:
            self.shipPositionX.clear()
            self.shipPositionY.clear()
            print(f"Placing a ship of size {self.boxSize}. Please enter coordinates one by one.")

            for i in range(self.boxSize):
                while True:
                    try:
                        x = int(input(f"Enter x{i+1} (1-10): "))
                        y = int(input(f"Enter y{i+1} (1-10): "))
                        if x not in range(1, 11) or y not in range(1, 11):
                            raise ValueError("Coordinates out of range. Please enter values between 1 and 10.")
                        
                        if i == 0 or (abs(self.shipPositionX[-1] - x) + abs(self.shipPositionY[-1] - y) == 1):
                            self.shipPositionX.append(x)
                            self.shipPositionY.append(y)
                            break
                        else:
                            print("Coordinates must be adjacent to the previous one.")
                    except ValueError as ve:
                        print(ve)

            self.shipPositionCorrect = self.validate_positions()
            if not self.shipPositionCorrect:
                print("Invalid ship position. Please try again.")
    
    def validate_positions(self):
        # Check for duplicates in coordinates
        positions = set(zip(self.shipPositionX, self.shipPositionY))
        if len(positions) != self.boxSize:
            return False
        return True

    def display_ship(self):
        print("Ship Coordinates:")
        for i in range(self.boxSize):
            print(f"({self.shipPositionX[i]}, {self.shipPositionY[i]})")

    def isShipDestroy(self):
        for i in range(1, len(self.boxSize)):
            if self.shipState == False:
                return False
        return True
    