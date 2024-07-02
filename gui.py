import tkinter as tk
from tkinter import messagebox
import numpy as np
from Player import Player
from AI import AI
from Box import Box
from Ship import Ship


class BattleshipGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Battleship Game")

        self.player1 = Player()
        self.player2 = AI()
        self.player2.update_probabilities()
        self.player2.reset_fire_history()

        self.selected_x = None
        self.selected_y = None
        self.selected_orientation = None
        self.ship_size = None

        self.create_widgets()

    def create_widgets(self):
        # Create frames for player boards
        self.player1_frame = tk.Frame(self.root)
        self.player1_frame.grid(row=0, column=0, padx=10, pady=10)
        self.player1_ship_board = self.create_board_frame(self.player1_frame, "Player 1 Ships", self.player1_click)
        self.player1_fire_board = self.create_board_frame(self.player1_frame, "Player 1 Fire Board", self.player2_click)

        self.player2_frame = tk.Frame(self.root)
        self.player2_frame.grid(row=0, column=1, padx=10, pady=10)
        self.player2_ship_board = self.create_board_frame(self.player2_frame, "Player 2 Ships", self.player2_click)
        self.player2_fire_board = self.create_board_frame(self.player2_frame, "Player 2 Fire Board", self.player1_click)

        # Fire button
        self.fire_button = tk.Button(self.root, text="Fire", command=self.fire)
        self.fire_button.grid(row=1, column=0, columnspan=2)

        # Info label
        self.info_label = tk.Label(self.root, text="")
        self.info_label.grid(row=2, column=0, columnspan=2)

        # Ship placement controls
        self.ship_size_var = tk.IntVar()
        self.ship_size_var.set(5)  # Default ship size
        self.orientation_var = tk.IntVar()
        self.orientation_var.set(1)  # Default orientation: Up

        self.ship_size_label = tk.Label(self.root, text="Ship Size:")
        self.ship_size_label.grid(row=3, column=0, sticky='e')

        self.ship_size_menu = tk.OptionMenu(self.root, self.ship_size_var, 5, 4, 3, 2)
        self.ship_size_menu.grid(row=3, column=1, sticky='w')

        self.orientation_label = tk.Label(self.root, text="Orientation:")
        self.orientation_label.grid(row=4, column=0, sticky='e')

        self.orientation_menu = tk.OptionMenu(self.root, self.orientation_var, 1, 2, 3, 4)
        self.orientation_menu.grid(row=4, column=1, sticky='w')

        # Place Ship button
        self.place_ship_button = tk.Button(self.root, text="Place Ship", command=self.place_ship)
        self.place_ship_button.grid(row=5, column=0, columnspan=2)

        # Reset button
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_game)
        self.reset_button.grid(row=6, column=0, columnspan=2)

        self.reset_game()

    def create_board_frame(self, frame, title, click_handler):
        board_frame = tk.Frame(frame)
        board_frame.pack(pady=10)

        label = tk.Label(board_frame, text=title)
        label.grid(row=0, column=0, columnspan=10)

        board_buttons = [[None for _ in range(10)] for _ in range(10)]
        for i in range(10):
            for j in range(10):
                button = tk.Button(board_frame, text=".", width=2, height=1,
                                   command=lambda x=j, y=i: click_handler(x, y))
                button.grid(row=i + 1, column=j)
                board_buttons[i][j] = button

        return board_buttons

    def player1_click(self, x, y):
        self.info_label.config(text=f"Selected coordinates for ship placement: ({x + 1}, {y + 1})")
        self.selected_x, self.selected_y = x, y

    def player2_click(self, x, y):
        self.info_label.config(text=f"Selected coordinates for firing: ({x + 1}, {y + 1})")
        self.selected_x, self.selected_y = x, y

    def place_ship(self):
        if self.selected_x is not None and self.selected_y is not None:
            size = self.ship_size_var.get()
            orientation = self.orientation_var.get()
            ship = Ship(size, self.selected_x + 1, self.selected_y + 1, orientation)
            if self.player1._correct_orientation(self.selected_x + 1, self.selected_y + 1, orientation, size) and \
                    self.player1._is_position_valid(self.selected_x + 1, self.selected_y + 1, orientation, size):
                self.player1.ships.append(ship)
                self.player1.place_ship_on_board(ship)
                self.update_boards()
                self.info_label.config(
                    text=f"Placed ship of size {size} at ({self.selected_x + 1}, {self.selected_y + 1}) with orientation {orientation}")
            else:
                self.info_label.config(text="Invalid position for ship placement")
        else:
            self.info_label.config(text="Select coordinates to place the ship")

    def fire(self):
        if self.selected_x is not None and self.selected_y is not None:
            result = self.player1.fire(self.player2, self.selected_x, self.selected_y)
            self.update_boards()
            self.info_label.config(text=f"Fired at ({self.selected_x + 1}, {self.selected_y + 1}): {result}")
            if self.player2.isAllShipDestroy():
                messagebox.showinfo("Game Over", "Player 1 wins!")
                self.reset_game()
            else:
                self.ai_turn()
        else:
            self.info_label.config(text="Select coordinates to fire")

    def ai_turn(self):
        x, y, result = self.player2.shoot(self.player1)
        self.update_boards()
        self.info_label.config(text=f"AI fired at ({x + 1}, {y + 1}): {result}")
        if self.player1.isAllShipDestroy():
            messagebox.showinfo("Game Over", "AI wins!")
            self.reset_game()

    def update_boards(self):
        for i in range(10):
            for j in range(10):
                self.player1_ship_board[i][j].config(text=self.get_display_char(self.player1.board[i][j]))
                self.player1_fire_board[i][j].config(text=self.get_display_char(self.player1.fireBoard[i][j]))
                self.player2_ship_board[i][j].config(text=self.get_display_char(self.player2.board[i][j]))
                self.player2_fire_board[i][j].config(text=self.get_display_char(self.player2.fireBoard[i][j]))

    def get_display_char(self, box):
        if box == Box.VIDE:
            return "."
        elif box == Box.EAU:
            return "O"
        elif box == Box.TOUCHE:
            return "X"
        elif box == Box.COULE:
            return "C"
        return "."

    def reset_game(self):
        self.player1.reset()
        self.player2.reset()
        self.player2.create_ships_with_probabilities()
        self.update_boards()
        self.info_label.config(text="Game reset. Place your ships and start firing!")


if __name__ == "__main__":
    root = tk.Tk()
    app = BattleshipGUI(root)
    root.mainloop()
