import pygame 
import random
from components.Asteroid import Asteroid
import utils.collision as collision

def handleEvents(player):
    """Handle the events."""
    running = True
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move('left')
    if keys[pygame.K_RIGHT]:
        player.move('right')
    if keys[pygame.K_UP]:
        player.move('up')
    if keys[pygame.K_DOWN]:
        player.move('down')
    if keys[pygame.K_SPACE]:
        player.shoot()

    return running

def updateGameLogic(player, asteroids, width, height, score):
    """Game logic update"""
    if random.randint(1, 40) == 1:
        asteroids.append(Asteroid(width, height))

    for asteroid in asteroids:
        asteroid.move()
    
    if collision.checkPlayerAsteroidCollision(player, asteroids):
        return score, True

    for bullet in player.bullets[:]:
        bullet[1] -= 10  
        if bullet[1] < 0:  
            player.bullets.remove(bullet) 

    score = collision.checkBulletAsteroidCollision(player, asteroids, score)

    return score, False

def drawGameObjects(window, player, asteroids, score, font, high_score):
    """draw the game objects."""
    player.draw(window.screen)
    for asteroid in asteroids:
        asteroid.draw(window.screen)
    
    for bullet in player.bullets:
        pygame.draw.rect(window.screen, (255, 0, 0), (bullet[0], bullet[1], 5, 15))

    
    window.draw_text(f"Score: {score}", font, (255, 255, 255), (10, 10))
    window.draw_text(f"Highscore: {high_score}", font, (255, 255, 255), (10, 40))