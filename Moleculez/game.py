import pygame as game
import sys
import random as rand
from components import Button

from config import window_x, window_y, physics_speed, fps

class Atom: # Atom, has id, a type and can soon do stuff
    def __init__(self, id, type):
        self.id = id
        self.type = type

class AtomHandler: # Keeps track of atoms and creates new atoms
    def __init__(self):
        self.aList = []
        self.inc = 0
    def createAtom(self, type):
        obj = Atom(self.inc, type)
        self.aList.append(obj)
        self.inc = self.inc+1


class MoleculeHandler: # Class to handle molecules, keeps track of every molecule and combination as well as the current molecule you are supposed to make
    def __init__(self):
        self.molecules = ["Water", "CarbonDioxide", "Methane", "Ethanol", "Glucose"]
        self.combinations = {"Water": ["Hydrogen", "Hydrogen", "Oxygen"],
                             "CarbonDioxide": ["Carbon", "Oxygen", "Oxygen"],
                             "Methane": ["Carbon", "Hydrogen", "Hydrogen", "Hydrogen", "Hydrogen"],
                             "Ethanol": ["Carbon", "Carbon", "Oxygen", "Hydrogen", "Hydrogen", "Hydrogen", "Hydrogen", "Hydrogen",  "Hydrogen"],
                             "Glucose": ["Carbon", "Carbon", "Carbon", "Carbon", "Carbon", "Carbon", "Oxygen", "Oxygen", "Oxygen",  "Oxygen", "Oxygen", "Oxygen", "Hydrogen", "Hydrogen", "Hydrogen", "Hydrogen", "Hydrogen", "Hydrogen",  "Hydrogen", "Hydrogen", "Hydrogen", "Hydrogen", "Hydrogen", "Hydrogen"]
        }
        self.curMol = self.molecules[rand.randint(0,len(self.molecules)-1)]

    def newMol(self):
        self.curMol = self.molecules[rand.randint(0,len(self.molecules)-1)]
        self.curComb = self.combinations[self.curMol]
        print(self.curComb)

class Main: # Class definition of the main program.
    def __init__(self): # Starts on initialization of an object
        
        game.init()
        self.molecule = MoleculeHandler()
        self.atom = AtomHandler()
        self.screen = game.display.set_mode((window_x, window_y))
        game.display.set_caption("Moleculez")
        self.fontM = game.font.SysFont("Arial", 48) # Define a game font variable
        self.fontS = game.font.SysFont("Arial", 24)

        self.paused = False

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

            welcome_rect = welcome_text.get_rect(center=(window_x // 2 - 110, window_y // 2))
            to_rect = to_text.get_rect(center=(window_x // 2, window_y // 2))
            moleculez_rect = moleculez_text.get_rect(center=(window_x // 2 + 120, window_y // 2))
            if self.paused == False:
                press_text = self.fontS.render("Press any key to start", True, (255,255,255))
                press_rect = press_text.get_rect(center=(window_x // 2, window_y//2 + 200))
            else:
                press_text = self.fontS.render("PAUSED! Press Esc to quit, any other key to continue", True, (255,255,255))
                press_rect = press_text.get_rect(center=(window_x // 2, window_y//2 + 200))

            self.screen.blit(welcome_text, welcome_rect) # Separate blitting for axis transformation
            self.screen.blit(to_text, to_rect)
            self.screen.blit(moleculez_text, moleculez_rect)
            self.screen.blit(press_text, press_rect)

            self.update()

    def game(self):
        game.display.set_caption("Game")
        self.score = 0
        self.selAtom = "None"

        self.atom1Button = Button(window_x - 200, window_y // 4, "blue", "green", "Hydrogen", self.fontM, "Hydrogen")
        self.atom2Button = Button(window_x - 200, window_y // 2, "blue", "green", "Oxygen", self.fontM, "Oxygen")

        while self.state == "Game":

            self.screen.fill("black")
            self.eventHandler()
            # Texts, Text rects and Blitting
            game_text = self.fontM.render(self.molecule.curMol, True, (50, 205, 50))
            score_text = self.fontM.render("Score", True, (0, 100, 1+ self.score % 255))

            game_rect = game_text.get_rect(center=(window_x // 2, window_y // 6))
            score_rect = score_text.get_rect(center =(window_x // 6, window_y // 6 ))

            self.screen.blit(game_text, game_rect)
            self.screen.blit(score_text, score_rect)

            # Buttons and blitting
            self.atom1Button.update(self.screen)
            self.atom2Button.update(self.screen)




            self.update()


    def selectAtom(self, atom):
        self.selAtom = atom
        print("You have selected " , atom)

    def eventHandler(self): # Handling of events, mouseclicks, mousepositions and keyclicks
        for e in game.event.get():
            if e.type == game.QUIT:
                self.state = False
                self.quit()

            if self.state == "Menu":

                if e.type == game.KEYDOWN:
                    if e.key == game.K_ESCAPE:
                        self.state = False
                        self.quit()
                    else:
                        self.state = "Game"
                        self.paused = False
                        self.game()


            if self.state == "Game":

                if e.type == game.KEYDOWN:
                    if e.key == game.K_ESCAPE:
                        self.state = "Menu"
                        self.paused = True
                        self.mainMenu()
                    self.molecule.newMol()
                    
                if e.type == game.MOUSEBUTTONDOWN:
                    for button in [self.atom1Button, self.atom2Button]:
                        button.handleClick(e, self.selectAtom)
    

    def update(self): # Main update functions. Updates variables such as: Positions, speeds and object lists
        game.display.flip()
        self.clock.tick(fps)

if __name__ == "__main__":  # Main instantiator
    Main = Main()
    Main.mainMenu()