import pygame
import time

class Player:
    def __init__(self, width, height):
        self.x = width // 2
        self.y = height - 60 
        self.speed = 5
        self.bullets = []
        self.width = 50
        self.height = 50
        self.image = pygame.image.load('images/player.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.last_shot_time = 0
        self.shoot_cooldown = 0.2
        self.screen_width = width
        self.screen_height = height

        self.shoot_sound = pygame.mixer.Sound('sounds/gun.mp3')
    
    def move(self, direction):
        if direction == 'left' and self.x>0:
            self.x -= self.speed
        if direction == 'right' and self.x < self.width * 15:
            self.x += self.speed
        if direction == 'up' and self.y > 0:
            self.y -= self.speed
        if direction == 'down' and self.y < self.width * 11:
            self.y += self.speed
    
    def shoot(self):
        current_time = time.time()
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            self.bullets.append([self.x + 20, self.y])
            self.last_shot_time = current_time
            self.shoot_sound.play()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))