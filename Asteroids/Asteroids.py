# This is the start of the asteroids game

import pygame
import sys
import time
import math

from pygame.math import Vector2 as v2
from settings import *

clock = pygame.time.Clock()
running = True
pygame.init()

class Player:
    def __init__(self):
        self.x = window_width // 2 - player_size.x // 2
        self.y = window_height // 2 - player_size.y // 2
        self.speed = player_speed 
        self.dx = 0
        self.dy = 0

    def draw_player(self):
        triangleCoords = [v2(player_size.x,player_size.y),v2(0,player_size.y),v2(player_size.x//2,player_size.y//2)]
        player_surface = pygame.Surface((player_size.x,player_size.y))
        pygame.draw.polygon(player_surface, player_color, triangleCoords)
        return player_surface
    
    def updatePosition(self):
        self.x += self.dx
        self.y += self.dy
        self.dx = self.dx * (1-friction)
        self.dy = self.dy * (1-friction)

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.prev_time = time.time()

    def run(self):
        clock.tick(fps)
        player = Player()
        while running:
            self.screen.fill((0,0,0))
            self.screen.blit(player.draw_player(), (player.x,player.y))
            clock.tick(fps)
            now = time.time()
            dt = now - self.prev_time
            self.prev_time = now
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        player.dy += -player_speed
                    elif event.key == pygame.K_a:
                        player.dx += -player_speed
                    elif event.key == pygame.K_d:
                        player.dx += player_speed
                    elif event.key == pygame.K_s:
                        player.dy += player_speed
            player.updatePosition()



main = Main()
main.run()