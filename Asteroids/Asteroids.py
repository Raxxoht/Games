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
        self.x = window_width // 2
        self.y = window_height // 2
        self.speed = player_speed 
        self.dx = 0
        self.dy = 0
        self.angle = 0
        self.player_surface = pygame.Surface((player_size.x,player_size.y))
        self.triangleCoords = [
            v2(0, -player_size.y / 2),     # Top point of the triangle
            v2(-player_size.x / 2, player_size.y / 2),  # Bottom left point of the triangle
            v2(player_size.x / 2, player_size.y / 2)    # Bottom right point of the triangle
        ]

    def draw_player(self, surface):
        rotated_points = [point.rotate(self.angle) for point in self.triangleCoords]
        translated_points = [(self.x + point.x, self.y + point.y) for point in rotated_points]
        pygame.draw.polygon(surface, player_color, translated_points)
    
    def updatePosition(self):
        if player_speed - abs(self.dx) > speedStopMargin:
            self.dx = 0
        elif player_speed - abs(self.dy) > speedStopMargin:
            self.dy = 0
        self.x += self.dx
        self.y += self.dy
        self.dx = self.dx * (1-friction)
        self.dy = self.dy * (1-friction)

    def updateRotation(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        self.angle = math.degrees(math.atan2(rel_y, rel_x)) -270

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
            player.draw_player(self.screen)
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
            player.updateRotation()



main = Main()
main.run()