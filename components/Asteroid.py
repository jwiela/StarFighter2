import pygame
import random

class Asteroid:
    def __init__(self, width, height):
        self.x = random.randint(0, width - 40)
        self.y = -40
        self.speed = random.randint(2, 5)
        self.width = 40
        self.height = 40
        self.image = pygame.image.load('images/asteroid.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
    
    def move(self):
        self.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))