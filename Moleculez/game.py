import pygame as game
import sys
import random as rand
import numpy as np
import math
from components import Button

from config import window_x, window_y, physics_speed, fps, aSize, mSize, Hitboxes

class Atom: # Atom, has id, a type and can soon do stuff
    def __init__(self, id, type, color, x_pos, y_pos):
        self.id = id
        self.type = type
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.dx = rand.choice([i for i in np.arange(-0.75, 0.75, 0.3) if i != 0])
        self.dy = rand.choice([i for i in np.arange(-0.75, 0.75, 0.3) if i != 0])
        self.rect = game.Rect(0, 0, 3*aSize, 3*aSize)
        self.rect.center = (self.x_pos, self.y_pos)
        self.update_position

    def update_position(self):
        self.rect.center = (self.x_pos, self.y_pos)

class AtomHandler: # Keeps track of atoms and creates new atoms
    def __init__(self):
        self.aColors = {"Hydrogen": (255, 255, 255),
            "Oxygen": (255, 0, 0),
            "Carbon": (0, 0, 255)}
        self.aList = []
        self.inc = 0

    def createAtom(self, type, color, x_pos, y_pos):
        obj = Atom(self.inc, type, color, x_pos, y_pos)
        self.aList.append(obj)
        self.inc = self.inc+1

    def updateAtom(self, screen, surface):
        for atom in self.aList:
            if atom.x_pos + atom.dx - aSize <= screen.left or atom.x_pos + atom.dx + aSize >= screen.right:
                atom.dx = -(atom.dx)
            if atom.y_pos + atom.dy - aSize <= screen.top or atom.y_pos + atom.dy + aSize >= screen.bottom:
                atom.dy = -(atom.dy)
            atom.x_pos += atom.dx
            atom.y_pos += atom.dy
        self.handleCollisions(surface)

    def drawAtoms(self, screen):
        for atom in self.aList:
            game.draw.circle(screen, atom.color, (atom.x_pos, atom.y_pos), aSize)

    def handleCollisions(self, surface):
        for atom in self.aList:
            atom.update_position()
            tmpList = self.aList.copy()
            tmpList.remove(atom)
            rects = [a.rect for a in tmpList]
            if atom.rect.collidelist(rects) >=0:
                if math.isclose(0, atom.dx):
                    atom.dx = rand.randint(-2,2)
                color = "Red"
                atom.dx = -atom.dx
                atom.dy = -atom.dy
            else:
                color = "Green"
            if Hitboxes == "Enabled":
                game.draw.rect(surface, color, atom.rect)

class Molecule:
    def __init__(self):
        self.atomList = []
        self.x_pos = 0
        self.y_pos = 0
        self.dx = 0
        self.dy = 0

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
        self.atomH = AtomHandler()
        self.binding = False
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

            game.draw.rect(self.screen,(255,255,255), press_rect.inflate(100,100), 4)

            self.update()

    def game(self):
        game.display.set_caption("Game")
        self.score = 0
        self.selAtom = "None"
        self.binding1 = "None"
        self.binding2 = "None"
        self.gameScreen = game.Rect(window_x // 2 - 300, window_y // 2 -100,window_x // 3 + 50,window_y // 2)

        self.gameScreen = self.gameScreen.inflate(200,100)

        self.atom1Button = Button(window_x - 200, window_y // 4, "blue", "green", "Hydrogen", self.fontM, "Hydrogen")
        self.atom2Button = Button(window_x - 200, window_y // 2, "blue", "green", "Oxygen", self.fontM, "Oxygen")
        self.atom3Button = Button(window_x - 200, window_y // 1.33, "blue", "green", "Carbon", self.fontM, "Carbon")
        self.bindButton = Button(window_x - 200, window_y // 1.10, "purple", "grey", "Binding", self.fontM, "Binding")

        while self.state == "Game":

            self.screen.fill("black")
            self.eventHandler()
            # Texts, Text rects and Blitting
            game_text = self.fontM.render(self.molecule.curMol, True, (50, 205, 50))
            score_text = self.fontM.render(f"Score : {self.score}", True, (0, 100, 1+ self.score % 255))

            game_rect = game_text.get_rect(center=(window_x // 2, window_y // 6))
            score_rect = score_text.get_rect(center =(window_x // 6, window_y // 6 ))

            self.screen.blit(game_text, game_rect)
            self.screen.blit(score_text, score_rect)

            # Buttons and blitting
            self.atom1Button.update(self.screen)
            self.atom2Button.update(self.screen)
            self.atom3Button.update(self.screen)
            self.bindButton.update(self.screen)

            game.draw.rect(self.screen,(0,210,0), score_rect.inflate(100,100), 4)
            game.draw.rect(self.screen,(200,200,200), game_rect.inflate(200,100), 4)
            game.draw.rect(self.screen,(200,200,200), self.atom2Button.rect.inflate(200, window_y // 1.10), 4)
            game.draw.rect(self.screen,(200,200,200), self.gameScreen, 4)
            

            for button in [self.atom1Button, self.atom2Button, self.atom3Button]:
                game.draw.rect(self.screen,(100,200,100), button.rect.inflate(100, 100), 4)

            self.atomH.drawAtoms(self.screen)
            self.atomH.updateAtom(self.gameScreen, self.screen)
            if self.binding == True and self.binding1 != "None" and self.binding2 == "None":
                game.draw.line(self.screen, "White", (self.binding1.x_pos, self.binding1.y_pos), game.mouse.get_pos(), 5)
            elif self.binding1 != "None" and self.binding2 != "None":
                game.draw.line(self.screen, "White", (self.binding1.x_pos, self.binding1.y_pos), (self.binding2.x_pos, self.binding2.y_pos), 5)

            self.update()

    def selectAtom(self, atom):
        self.binding = False
        self.score += 1
        self.selAtom = atom
        print("You have selected " , atom)

    def toggleBind(self, value):
        self.binding = not self.binding
        self.selAtom = "None"
        if self.binding:
            print("Now creating binding")
        else:
            print("Now stopping binding")
            self.binding1 = "None"
            self.binding2 = "None"

    def handleMouseEvents(self, pos):
        mouse_pos = pos

        if self.binding:
            for atom in self.atomH.aList:
                if atom.rect.collidepoint(mouse_pos):
                    if self.binding2 != "None":
                        self.binding1 = atom;self.binding2 = "None"
                    elif self.binding1 != "None":
                        self.binding2 = atom
                        self.binding = False
                        print("Bind made!")
                    else:
                        self.binding1 = atom
                    if self.binding1 != "None" and self.binding2 != "None":
                        print(self.binding1.id, " HELLO ", self.atomH.inc, "LASTLY", self.binding2.id)

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
                    self.handleClick()
                    self.bindButton.handleClick(e, self.toggleBind)
                    for button in [self.atom1Button, self.atom2Button, self.atom3Button]:
                        button.handleClick(e, self.selectAtom)
    

    def update(self): # Main update functions. Updates variables such as: Positions, speeds and object lists
        game.display.flip()
        self.clock.tick(fps)

    def handleClick(self):
        mouse_pos = game.mouse.get_pos()
        if mouse_pos[0] in range(self.gameScreen.left, self.gameScreen.right) and mouse_pos[1] in range(self.gameScreen.top, self.gameScreen.bottom):
            if self.selAtom != "None":
                self.atomH.createAtom(self.selAtom, self.atomH.aColors[self.selAtom], mouse_pos[0], mouse_pos[1]); print(self.selAtom, self.atomH.aColors[self.selAtom])
            else:
                self.handleMouseEvents(mouse_pos)

if __name__ == "__main__":  # Main instantiator
    Main = Main()
    Main.mainMenu()