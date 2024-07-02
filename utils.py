import numpy as np
import matplotlib.pyplot as plt
from Box import Box

def convert_board_to_ints(board):
    return [[box.value for box in row] for row in board]

def convert_ints_to_board(int_board):
    return np.array([[Box(val) for val in row] for row in int_board])

def convert_board_to_ints_ship(board):
    return [[1 if cell == Box.TOUCHE else 0 for cell in row] for row in board]
