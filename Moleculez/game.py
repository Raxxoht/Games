import pygame as game
import sys

from config import window_x, window_y, physics_speed, fps

class Atom:
    def __init__(self):
        pass


class Molecule:
    def __init__(self):
        pass

class Main: # Class definition of the main program.
    def __init__(self): # Starts on initialization of an object
        
        game.init()
        self.screen = game.display.set_mode((window_x, window_y))
        game.display.set_caption("Moleculez")

        self.running = True
    
    def quit(self): # Quits the game and exits the window
        game.quit()
        sys.exit()

    def run(self): # Running functions that need to be updated per tick
        while self.running:
            self.eventHandler()
        self.quit()

    def eventHandler(self): # Handling of events, mouseclicks, mousepositions and keyclicks
        for e in game.event.get():
            if e.type == game.QUIT:
                self.running = False

    def update(self): # Main update functions. Updates variables such as: Positions, speeds and object lists
        pass

if __name__ == "__main__":  # Main instantiator
    Main = Main()
    Main.run()