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
        self.fontM = game.font.SysFont("Arial", 48)
        self.fontS = game.font.SysFont("Arial", 32)

        self.state = "Menu"
    
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

    def update(self): # Main update functions. Updates variables such as: Positions, speeds and object lists
        game.display.flip() 

if __name__ == "__main__":  # Main instantiator
    Main = Main()
    Main.mainMenu()