import numpy as np
import pygame as game
import sys

class Button:
    def __init__(self, x_pos, y_pos, color, hcolor, i_text, font, value):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.hcolor = hcolor
        self.i_text = i_text
        self.font = font
        self.value = value

        self.text = self.font.render(self.i_text, True, self.color)

        self.rect = game.Rect(0, 0, 150, 50)
        self.rect.center = (self.x_pos, self.y_pos)

        self.text_rect = self.text.get_rect(center=self.rect.center)


    def update(self, screen):
        self.hover(game.mouse.get_pos())
        screen.blit(self.text, self.text_rect)

    def checkInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        else:
            return False
        
    def hover(self, position):
        if self.checkInput(position):
            self.text = self.font.render(self.i_text, True, self.hcolor)
        else:
            self.text = self.font.render(self.i_text, True, self.color)

    def handleClick(self, event, callback):
        if self.checkInput(event.pos):
            callback(self.value)