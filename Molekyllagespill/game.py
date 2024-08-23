import pygame as game

from config import window_x, window_y, physics_speed, fps

def run():
    game.init()
    screen = game.display.set_mode((window_x, window_y))
    game.display.set_caption("Molekyllagespill")
