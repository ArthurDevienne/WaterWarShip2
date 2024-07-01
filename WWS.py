import pandas as pd
import Human
import AI
from utils import convert_board_to_ints, plot_heatmap  # Importer les fonctions utilitaires

class WWS:
    def __init__(self):
        print("Game created")
        self.endGame = False
        self.game_data = []
        self.player1 = None
        self.player2 = None
        self.num_games = 1  # Default to 1 game
        self.initialize_players()

    def _get_next_game_id(self):
        try:
            existing_df = pd.read_csv('game_data.csv')
            last_game_id = existing_df['game_id'].max()
            return last_game_id + 1
        except FileNotFoundError:
            return 1

    def initialize_players(self):
        print("Choose game mode:")
        print("1. Player vs AI")
        print("2. AI vs AI")
        choice = int(input("Enter choice (1 or 2): "))

        if choice == 1:
            self.player1 = Human.Human("Jonny")
            self.player2 = AI.AI()
        elif choice == 2:
            self.num_games = int(input("Enter number of games to play: "))
            self.player1 = AI.AI()
            self.player2 = AI.AI()
        else:
            print("Invalid choice, defaulting to Player vs AI.")
            self.player1 = Human.Human("Jonny")
            self.player2 = AI.AI()

    def start(self):
        print("Starting Game")
        if isinstance(self.player1, AI.AI) and isinstance(self.player2, AI.AI):
            for game_num in range(self.num_games):
                print(f"Starting Game {game_num + 1}")
                self.game_id = self._get_next_game_id()  # Update game_id for each new game
                self.player1.update_heatmaps()  # Update heatmaps before each game
                self.player2.update_heatmaps()  # Update heatmaps before each game
                self.player1.reset_fire_history()
                self.player2.reset_fire_history()
                self.play_game()
                self.save_game_data()  # Save data after each game
        else:
            self.game_id = self._get_next_game_id()
            if isinstance(self.player1, AI.AI):
                self.player1.update_heatmaps()  # Update heatmaps before the game
            if isinstance(self.player2, AI.AI):
                self.player2.update_heatmaps()  # Update heatmaps before the game
            self.player1.reset_fire_history()
            self.player2.reset_fire_history()
            self.play_game()
            self.save_game_data()  # Save data after the game

    def play_game(self):
        self.player1.reset()
        if isinstance(self.player1, AI.AI):
            if self._has_enough_data():
                self.player1.create_ships_with_heatmap()  # Use heatmap-based ship placement
            else:
                self.player1.create_ships()  # Use random placement
        else:
            self.player1.create_ships()  # Use default ship placement

        self.player2.reset()
        if isinstance(self.player2, AI.AI):
            if self._has_enough_data():
                self.player2.create_ships_with_heatmap()  # Use heatmap-based ship placement
            else:
                self.player2.create_ships()  # Use random placement
        else:
            self.player2.create_ships()  # Use default ship placement

        self.endGame = False  # Reset end game flag for each game
        self.game_data = []  # Reset game data for each game
        turn = 1

        while not self.endGame:
            self.play_turn(self.player1, self.player2, turn)
            if self.updateEndGame():
                break
            self.play_turn(self.player2, self.player1, turn)
            if self.updateEndGame():
                break
            turn += 1

    def play_turn(self, current_player, opponent, turn):
        print(f"{current_player.name}'s turn:")
        current_player.displayRoundGame()  # Display the game board for the current player
        try:
            x, y, result = current_player.shoot(opponent)  # Current player shoots at the opponent
            self.log_turn(turn, current_player.name, x, y, result)
        except RuntimeError as e:
            print(e)
            self.endGame = True

    def log_turn(self, turn, player, x, y, result):
        remaining_ships_player1 = sum(not ship.isShipDestroy() for ship in self.player1.ships)
        remaining_ships_player2 = sum(not ship.isShipDestroy() for ship in self.player2.ships)
        self.game_data.append({
            'game_id': self.game_id,
            'turn': turn,
            'player': player,
            'x': x,
            'y': y,
            'result': result,
            'remaining_ships_player1': remaining_ships_player1,
            'remaining_ships_player2': remaining_ships_player2
        })

    def updateEndGame(self):
        if self.player1.isAllShipDestroy():
            print(f"{self.player2.name} wins!")
            self.endGame = True
        elif self.player2.isAllShipDestroy():
            print(f"{self.player1.name} wins!")
            self.endGame = True
        return self.endGame

    def save_game_data(self):
        df = pd.DataFrame(self.game_data)
        try:
            existing_df = pd.read_csv('game_data.csv')
            df = pd.concat([existing_df, df], ignore_index=True)
        except FileNotFoundError:
            pass
        df.to_csv('game_data.csv', index=False)
        self.save_boards()
        print("Game data saved to game_data.csv")

    def save_boards(self):
        board_data = {
            'game_id': [],
            'player': [],
            'board': []
        }
        for player, name in [(self.player1, 'player1'), (self.player2, 'player2')]:
            board_data['game_id'].append(self.game_id)
            board_data['player'].append(name)
            board_data['board'].append(convert_board_to_ints(player.board))

            board_data['game_id'].append(self.game_id)
            board_data['player'].append(f'{name}_fire')
            board_data['board'].append(convert_board_to_ints(player.fireBoard))

        df = pd.DataFrame(board_data)
        try:
            existing_df = pd.read_csv('boards_data.csv')
            df = pd.concat([existing_df, df], ignore_index=True)
        except FileNotFoundError:
            pass
        df.to_csv('boards_data.csv', index=False)
        print("Board data saved to boards_data.csv")

    def _has_enough_data(self):
        try:
            game_data = pd.read_csv('game_data.csv')
            return len(game_data['game_id'].unique()) >= 100
        except FileNotFoundError:
            return False
