import pygame as game
import sys
import random as rand

from config import window_x, window_y, physics_speed, fps

class Atom:
    def __init__(self):
        pass


class Molecule:
    def __init__(self):
        self.molecules = ["Water", "CarbonDioxide", "Methane", "Ethanol", "Glucose"]
        self.combinations = {"Water": ["Hydrogen", "Hydrogen", "Oxygen"],
                             "CarbonDioxide": ["Carbon", "Oxygen", "Oxygen"],
                             "Ethanol": ["Carbon", "Carbon", "Oxygen", "Hydrogen", "Hydrogen", "Hydrogen", "Hydrogen", "Hydrogen",  "Hydrogen"],
                             "Glucose": ["Carbon", "Carbon", "Carbon", "Carbon", "Carbon", "Carbon", "Oxygen", "Oxygen", "Oxygen",  "Oxygen", "Oxygen", "Oxygen", "Hydrogen", "Hydrogen", "Hydrogen", "Hydrogen", "Hydrogen", "Hydrogen",  "Hydrogen", "Hydrogen", "Hydrogen", "Hydrogen", "Hydrogen", "Hydrogen"]
        }
        self.curMol = self.molecules[rand.randint(0,len(self.molecules)-1)]

    def newMol(self):
        self.curMol = self.molecules[rand.randint(0,len(self.molecules)-1)]

class Main: # Class definition of the main program.
    def __init__(self): # Starts on initialization of an object
        
        game.init()
        self.molecule = Molecule()
        self.screen = game.display.set_mode((window_x, window_y))
        game.display.set_caption("Moleculez")
        self.fontM = game.font.SysFont("Arial", 48) # Define a game font variable
        self.fontS = game.font.SysFont("Arial", 24)

        self.state = "Menu" # Set a base state for the main menu

        self.clock = game.time.Clock()
    
    def quit(self): # Quits the game and exits the window
        game.quit()
        sys.exit()

    def mainMenu(self): # Main menu function to display a main menu while the state says so
        game.display.set_caption("Main Menu")
        while self.state == "Menu":
            self.screen.fill("black")
            self.eventHandler()

            welcome_text = self.fontM.render("Welcome", True, (50, 205, 50)) # Cool text formatting
            to_text = self.fontM.render("to", True, (173, 216, 230))
            moleculez_text = self.fontM.render("Moleculez!", True, (255, 0, 255))
            press_text = self.fontS.render("Press any key to start", True, (255,255,255))

            welcome_rect = welcome_text.get_rect(center=(window_x // 2 - 120, window_y // 2))
            to_rect = to_text.get_rect(center=(window_x // 2, window_y // 2))
            moleculez_rect = moleculez_text.get_rect(center=(window_x // 2 + 120, window_y // 2))
            press_rect = press_text.get_rect(center=(window_x // 2, window_y//2 + 200))

            self.screen.blit(welcome_text, welcome_rect) # Separate blitting for axis transformation
            self.screen.blit(to_text, to_rect)
            self.screen.blit(moleculez_text, moleculez_rect)
            self.screen.blit(press_text, press_rect)

            self.update()

    def game(self):
        game.display.set_caption("Game")
        while self.state == "Game":

            self.screen.fill("black")
            self.eventHandler()

            game_text = self.fontM.render(self.molecule.curMol, True, (50, 205, 50))
            game_rect = game_text.get_rect(center=(window_x // 2, window_y // 2))
            self.screen.blit(game_text, game_rect)
            self.update()


    def eventHandler(self): # Handling of events, mouseclicks, mousepositions and keyclicks
        for e in game.event.get():
            if e.type == game.QUIT:
                self.state = False
                self.quit()
            if e.type == game.KEYDOWN:
                if self.state == "Menu":
                    self.state = "Game"
                    self.game()
                if self.state == "Game":
                    self.molecule.newMol()
    

    def update(self): # Main update functions. Updates variables such as: Positions, speeds and object lists
        game.display.flip()
        self.clock.tick(fps)

if __name__ == "__main__":  # Main instantiator
    Main = Main()
    Main.mainMenu()