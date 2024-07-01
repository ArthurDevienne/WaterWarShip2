import numpy as np
import matplotlib.pyplot as plt
from Box import Box

def convert_board_to_ints(board):
    return [[box.value for box in row] for row in board]

def convert_ints_to_board(int_board):
    return np.array([[Box(val) for val in row] for row in int_board])

def plot_heatmap(data, title):
    plt.imshow(data, cmap='hot', interpolation='nearest')
    plt.title(title)
    plt.colorbar()
    plt.show()
