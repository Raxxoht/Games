import pygame as game
import sys

from config import window_x, window_y, physics_speed, fps

class Main:
    def __init__(self):
        
        game.init()
        self.screen = game.display.set_mode((window_x, window_y))
        game.display.set_caption("Molekyllagespill")

        self.running = True
    
    def quit(self):
        game.quit()
        sys.exit()

    def run(self):
        while self.running:
            self.eventHandler()
        self.quit()

    def eventHandler(self):
        for e in game.event.get():
            if e.type == game.QUIT:
                self.running = False

if __name__ == "__main__":
    main = Main()
    main.run()