import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Player import Player
from Box import Box
from Ship import Ship

class AI(Player):
    def __init__(self):
        super().__init__()
        self.name = "AI"
        self.fire_history = set()
        self.target_mode = False
        self.target_queue = []
        self.current_target = None
        self.target_direction = None
        self.hit_probabilities = np.ones((10, 10)) / 100  # Initial probabilities
        self.ship_position_probabilities = np.ones((10, 10)) / 100  # Initial probabilities

    def create_ships_with_probabilities(self):
        self.reset()
        ship_sizes = [5, 4, 3, 3, 2]
        max_attempts = 100

        for size in ship_sizes:
            attempts = 0
            placed = False
            while attempts < max_attempts and not placed:
                # Trouve la position avec la probabilité la plus faible pour placer le bateau
                x, y = np.unravel_index(np.argmin(self.ship_position_probabilities, axis=None),
                                        self.ship_position_probabilities.shape)
                self.ship_position_probabilities[x, y] = np.max(
                    self.ship_position_probabilities) + 1  # Marque cette position comme essayée

                for orientation in range(1, 5):
                    if self._correct_orientation(x + 1, y + 1, orientation, size) and self._is_position_valid(x + 1,
                                                                                                              y + 1,
                                                                                                              orientation,
                                                                                                              size):
                        ship = Ship(size, x + 1, y + 1, orientation)
                        self.ships.append(ship)
                        self.place_ship_on_board(ship)
                        placed = True
                        break
                attempts += 1

            if attempts == max_attempts and not placed:
                print(f"Failed to place a ship of size {size} after {max_attempts} attempts. Resetting ship placement.")
                return self.create_ships()

    def create_ships(self):
        self.reset()
        ship_sizes = [5, 4, 3, 3, 2]
        for size in ship_sizes:
            attempts = 0
            while attempts < 100:
                x = np.random.randint(1, 11)
                y = np.random.randint(1, 11)
                orientation = np.random.randint(1, 5)
                if self._correct_orientation(x, y, orientation, size) and self._is_position_valid(x, y, orientation, size):
                    ship = Ship(size, x, y, orientation)
                    self.ships.append(ship)
                    self.place_ship_on_board(ship)
                    break
                attempts += 1
            if attempts == 100:
                print(f"Failed to place a ship of size {size} after 100 attempts. Exiting.")
                return self.create_ships()

    def place_ship_on_board(self, ship):
        for i in range(ship.getSize()):
            x, y = ship.shipPositionX[i], ship.shipPositionY[i]
            self.board[y-1][x-1] = Box.TOUCHE

    def displayRoundGame(self):
        self.displayBoard()
        self.displayFireBoard()

    def shoot(self, enemy):
        x, y = self.choose_shot()
        result = self.fire(enemy, x, y)
        if result == "TOUCHE":
            self.target_mode = True
            if self.current_target is None:
                self.current_target = (x, y)
                self.target_queue.extend(self.get_surrounding_positions(x, y))
        elif result == "COULE":
            self.target_mode = False
            self.current_target = None
            self.target_queue = []
            self.target_direction = None
        return x, y, result

    def choose_shot(self):
        if self.target_mode and self.target_queue:
            while self.target_queue:
                x, y = self.target_queue.pop(0)
                if (x, y) not in self.fire_history:
                    self.fire_history.add((x, y))
                    return x, y

        attempts = 0
        while attempts < 100:
            x, y = np.unravel_index(np.argmax(self.hit_probabilities, axis=None), self.hit_probabilities.shape)
            if (x, y) not in self.fire_history:
                self.fire_history.add((x, y))
                return x, y
            self.hit_probabilities[x, y] = 0  # Mark this position as tried
            attempts += 1

        print("AI could not find a valid shot with data analysis, choosing randomly.")
        while True:
            x = np.random.randint(0, 10)
            y = np.random.randint(0, 10)
            if (x, y) not in self.fire_history:
                self.fire_history.add((x, y))
                return x, y

    @staticmethod
    def convert_ints_to_board(board):
        return [[Box(val) for val in row] for row in board]

    @staticmethod
    def analyze_game_data():
        print("Analyzing game data...")
        try:
            game_data = pd.read_csv('game_data.csv')
            boards_data = pd.read_csv('boards_data.csv')
        except FileNotFoundError:
            print("No game data found.")
            return np.zeros((10, 10)), np.zeros((10, 10))

        hit_probabilities = np.zeros((10, 10))
        ship_positions = np.zeros((10, 10))

        print("Game data:")
        print(game_data.head())

        for _, shot in game_data.iterrows():
            if shot['result'] in ['TOUCHE', 'COULE']:
                hit_probabilities[shot['y'], shot['x']] += 1

        print("Boards data:")
        print(boards_data.head())

        for _, board in boards_data.iterrows():
            if '_fire' not in board['player']:
                board_array = np.array(eval(board['board']))
                ship_positions += board_array

        print("Hit Probabilities before normalization:\n", hit_probabilities)
        print("Ship Positions before normalization:\n", ship_positions)

        if hit_probabilities.sum() > 0:
            hit_probabilities /= hit_probabilities.sum()  # Normalize to get probabilities
        if ship_positions.sum() > 0:
            ship_positions /= ship_positions.sum()  # Normalize to get probabilities

        print("Hit Probabilities after normalization:\n", hit_probabilities)
        print("Ship Positions after normalization:\n", ship_positions)

        AI.plot_probabilities(hit_probabilities, 'Hit Probabilities')
        AI.plot_probabilities(ship_positions, 'Ship Position Probabilities')

        return hit_probabilities, ship_positions

    @staticmethod
    def plot_probabilities(data, title):
        print(f"Plotting probabilities: {title}")
        fig, ax = plt.subplots()
        cax = ax.matshow(data, cmap='coolwarm')
        fig.colorbar(cax)
        plt.title(title)
        plt.show()

    def update_probabilities(self):
        print("Updating probabilities...")
        if self._has_enough_data():
            hit_probabilities, ship_position_probabilities = self.analyze_game_data()
            self.hit_probabilities = hit_probabilities
            self.ship_position_probabilities = ship_position_probabilities

    def get_surrounding_positions(self, x, y):
        positions = []
        if x > 0:
            positions.append((x - 1, y))
        if x < 9:
            positions.append((x + 1, y))
        if y > 0:
            positions.append((x, y - 1))
        if y < 9:
            positions.append((x, y + 1))
        return positions

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

    def _correctFirstCoord(self, x, y, size):
        return 1 <= x <= 10 and 1 <= y <= 10

    def _correct_orientation(self, x, y, orientation, size):
        if orientation == 1:  # Up
            return y - size >= 0
        elif orientation == 2:  # Down
            return y + size <= 11
        elif orientation == 3:  # Left
            return x - size >= 0
        elif orientation == 4:  # Right
            return x + size <= 11
        return False

    def _has_enough_data(self):
        try:
            game_data = pd.read_csv('game_data.csv')
            return len(game_data['game_id'].unique()) >= 100
        except FileNotFoundError:
            return False

