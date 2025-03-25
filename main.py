import pygame 
import random
from Player import Player
from game_window import GameWindow
from Asteroid import Asteroid

pygame.init()

# window settings
WIDTH, HEIGHT = 800, 600
window = GameWindow(WIDTH, HEIGHT)

# font
font = pygame.font.Font(None, 36)

#objects
player = Player(WIDTH, HEIGHT)
asteroids = []
score = 0 
clock = pygame.time.Clock()

# game loop
running = True

while running:
    window.clear()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move('left')
    if keys[pygame.K_RIGHT]:
        player.move('right')
    if keys[pygame.K_SPACE]:
        player.shoot()
    
    if random.randint(1, 40) == 1:
        asteroids.append(Asteroid(WIDTH, HEIGHT))

    for asteroid in asteroids:
        asteroid.move()
        asteroid.draw(window.screen)
    
    for bullet in player.bullets:
        bullet[1] -= 10
        pygame.draw.rect(window.screen, (255, 0, 0), (bullet[0], bullet[1], 10, 20))

    for asteroid in asteroids[:]:
        for bullet in player.bullets[:]:
            if bullet[0] in range(asteroid.x, asteroid.x + 40) and bullet[1] in range(asteroid.y, asteroid.y + 40):
                asteroids.remove(asteroid)
                player.bullets.remove(bullet)
                score += 1

    player.draw(window.screen)

    window.draw_text(f"Score: {score}", font, (255, 255, 255), (10, 10))


    window.update()
    clock.tick(30)

pygame.quit( )