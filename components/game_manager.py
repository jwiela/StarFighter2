import pygame
from components.Player import Player
from components.game_window import GameWindow
from components.Asteroid import Asteroid
import utils.collision as collision
from utils.game_utils import handleEvents, updateGameLogic, drawGameObjects
from components.login_screen import LoginScreen
from utils.database import getHighscore, updateHighscore
import sys

WIDTH, HEIGHT = 800, 600

def main():
    pygame.init()
    window = GameWindow(WIDTH, HEIGHT)
    font = pygame.font.Font(None, 36)

    username = showLoginScreen(window, font)
    if not username:
        pygame.quit()
        sys.exit()
    
    gameLoop(window, username)

def gameLoop(window, username):
    # Initialize the game
    running = True
    font = pygame.font.Font(None, 36)
    
    while running:  # Outer loop to allow game restart
        player = Player(WIDTH, HEIGHT)
        asteroids = []
        clock = pygame.time.Clock()
        score = 0
        gameOver = False

        high_score = getHighscore(username)
        
        while not gameOver:
            window.clear()

            running = handleEvents(player)

            if not running:
                pygame.quit()
                sys.exit()
            
            score, gameOver = updateGameLogic(player, asteroids, WIDTH, HEIGHT, score)

            drawGameObjects(window, player, asteroids, score, font, high_score)
            window.update()
            clock.tick(30)  # Limit to 30 FPS
        
        if score > high_score:
            updateHighscore(username, score)

        play_again = showGameOverScreen(window, font, score)
        if not play_again:
            running = False

    pygame.quit()
    sys.exit()

# Shows login screen and retuns username
def showLoginScreen(window, font):
    login_screen = LoginScreen(window)
    username = None

    while username is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            login_screen.handleEvent(event)
        
        login_screen.draw()

        if login_screen.message == "Login successful":
            username = login_screen.username
        elif login_screen.message == "Registration successful":
            username = login_screen.username
    
    return username

def showGameOverScreen(window, font, score):
    """Displays Game Over screen with restart or quit options."""
    play_again_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    quit_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50)
    
    while True:
        window.clear()
        window.draw_text("GAME OVER", font, (255, 0, 0), (WIDTH // 2 - 80, HEIGHT // 3))
        window.draw_text(f"Final Score: {score}", font, (255, 255, 255), (WIDTH // 2 - 80, HEIGHT // 3 + 40))
        
        # Drawing buttons
        pygame.draw.rect(window.screen, (0, 200, 0), play_again_rect)
        pygame.draw.rect(window.screen, (200, 0, 0), quit_rect)
        
        window.draw_text("Play Again", font, (255, 255, 255), (WIDTH // 2 - 80, HEIGHT // 2 + 10))
        window.draw_text("Quit", font, (255, 255, 255), (WIDTH // 2 - 40, HEIGHT // 2 + 70))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if play_again_rect.collidepoint(mouse_x, mouse_y):
                    return True  # Restart the game
                if quit_rect.collidepoint(mouse_x, mouse_y):
                    return False  # Quit the game