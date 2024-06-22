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
            v2(0, -player_size.y / 2), # Top
            v2(-player_size.x / 2, player_size.y / 2), # Bottom left
            v2(player_size.x / 2, player_size.y / 2)   # Bottom right
        ]
        self.translatedPoints = []

    def draw_player(self, surface):
        rotated_points = [point.rotate(self.angle) for point in self.triangleCoords]
        self.translated_points = [(self.x + point.x, self.y + point.y) for point in rotated_points]
        pygame.draw.polygon(surface, player_color, self.translated_points)
    
    def updatePosition(self, dt):
            
        self.x += self.dx * dt * target_fps
        self.y += self.dy * dt * target_fps
        self.dx = self.dx * (1-friction)
        self.dy = self.dy * (1-friction)

    def updateRotation(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        self.angle = math.degrees(math.atan2(rel_y, rel_x)) + 90

    def checkCollision(self):
        for point in self.translated_points:
            if point[0] < 0 or point[0] > window_width:
                self.dx = -self.dx
            if point[1] < 0 or point[1] > window_height:
                self.y = max(0, min(self.y, window_height))
                self.dy = -self.dy

    def shoot(self, surface):
        bullet = Bullet()
        bullet.draw_Bullet(surface, (0,0))

class Bullet:
    def __init__(self):
        self.radius = 3
        self.speed=1
        self.x = 0
        self.y = 0
        self.dx=0
        self.dy=0
    
    def draw_Bullet(self, surface, center):
        pygame.draw.circle(surface, bullet_color, center,self.radius)

    def updateBulletPosition(self, dt):
        self.x += self.dx * dt * target_fps
        self.y += self.dy * dt * target_fps



class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.prev_time = time.time()
        self.bg = pygame.image.load("Asteroids/Graphics/background.png")

    def run(self):
        clock.tick(fps)
        player = Player()
        while running:
            self.screen.blit(self.bg, (0,0))
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
                        player.dy += (-player_speed)
                    elif event.key == pygame.K_a:
                        player.dx += (-player_speed)
                    elif event.key == pygame.K_d:
                        player.dx +=( player_speed)
                    elif event.key == pygame.K_s:
                        player.dy +=( player_speed)
                    elif event.key == pygame.K_SPACE:
                        print("PEW!")
                        player.shoot(self.screen)
            player.checkCollision()
            player.updatePosition(dt)
            player.updateRotation()



main = Main()
main.run()