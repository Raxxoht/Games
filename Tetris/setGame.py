import pygame

# Game Pad Size
columns = 10
rows = 20 
cell_size = 20
game_width, game_height = columns * cell_size, rows*cell_size

# Sidebar size
sidebar_width = 200
preview_height_fraction = 0.7
score_height_fraction = 1 - preview_height_fraction

# Window size
padding = 20
window_width = game_width + sidebar_width + padding * 3
window_height = game_height + padding * 2

# Tetromino pieces

Shapes = [
    [[1, 1, 1, 1]], # I block
    
    [[1,1],
    [1,1]], # O block

    [[0,1,0],
    [1,1,1]], # T block

    [[1,0,0],
    [1,1,1]], # L block

    [[0,0,1],
    [1,1,1]], # J block

    [[0,1,1],
     [1,1,0]], # S block

    [[1,1,0],
     [0,1,1]] # Z block
]

shape_colors = [
    (0, 255, 255),  # Cyan for I
    (255, 255, 0),  # Yellow for O
    (128, 0, 128),  # Purple for T
    (255, 165, 0),  # Orange for L
    (0, 0, 255),  # Blue for J
    (0, 255, 0),  # Green for S
    (255, 0, 0)  # Red for Z
]