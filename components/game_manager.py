import pygame
from components.Player import Player
from components.game_window import GameWindow
from components.register_screen import RegisterScreen
from utils.game_utils import handleEvents, updateGameLogic, drawGameObjects
from components.login_screen import LoginScreen
from utils.database import getHighscore, updateHighscore
from components.leaderboard_screen import LeaderboardScreen
import sys

WIDTH, HEIGHT = 800, 600

def main():
    pygame.init()
    window = GameWindow(WIDTH, HEIGHT)
    font = pygame.font.Font(None, 36)

    username = showLoginScreen(window)
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
        
        # if score > high_score:
        #     updateHighscore(username, score)

        play_again = showGameOverScreen(window, font, score, username)
        if not play_again:
            running = False

    pygame.quit()
    sys.exit()

# Shows login screen and retuns username
def showLoginScreen(window):
    login_screen = LoginScreen(window)
    register_screen = RegisterScreen(window)
    current_screen = 'login'

    while True:
        window.clear()
        if current_screen == 'login':
            login_screen.draw()
        elif current_screen == 'register':
            register_screen.draw()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if current_screen == 'login':
                result = login_screen.handleEvent(event)
                if result == 'register':
                    current_screen = 'register'
                elif login_screen.message == 'Login successful!':
                    return login_screen.username  # Return the username after successful login
            elif current_screen == 'register':
                result = register_screen.handleEvent(event)
                if result == 'login':
                    current_screen = 'login'


def showGameOverScreen(window, font, score, username):
    """Displays an improved Game Over screen with centered elements."""
    high_score = getHighscore(username)

    high_score_sound = pygame.mixer.Sound('sounds/new_high.mp3')
    lose_sound = pygame.mixer.Sound('sounds/gameover.wav')
    high_score_sound.set_volume(0.5)

    # Define button dimensions
    button_width = 200
    button_height = 50
    button_spacing = 20  # Space between buttons

    # Calculate positions dynamically
    title_y = HEIGHT // 4
    score_y = title_y + 80
    high_score_y = score_y + 40
    play_again_y = high_score_y + 80
    leaderboard_y = high_score_y + 80
    play_again_y = leaderboard_y + button_height + button_spacing
    quit_y = play_again_y + button_height + button_spacing

    leaderboard_rect = pygame.Rect(WIDTH // 2 - button_width // 2, leaderboard_y, button_width, button_height)
    play_again_rect = pygame.Rect(WIDTH // 2 - button_width // 2, play_again_y, button_width, button_height)
    quit_rect = pygame.Rect(WIDTH // 2 - button_width // 2, quit_y, button_width, button_height)

    if score > high_score:
        high_score_sound.play()
    else:
        lose_sound.play()

    while True:
        # Clear the screen and set a background color
        window.screen.fill((30, 30, 30))  # Dark gray background

        # Draw the "Game Over" title
        title_font = pygame.font.Font(None, 72)  # Larger font for the title
        window.draw_text("GAME OVER", title_font, (255, 0, 0), (WIDTH // 2, title_y), center=True)

        # Display the score and high score
        if score > high_score:
            window.draw_text("New High Score!", font, (255, 255, 0), (WIDTH // 2, score_y), center=True)
            window.draw_text(f"Final Score: {score}", font, (255, 255, 255), (WIDTH // 2, high_score_y), center=True)
            updateHighscore(username, score)  # Update high score in the database
        else:
            window.draw_text(f"Final Score: {score}", font, (255, 255, 255), (WIDTH // 2, score_y), center=True)
            window.draw_text(f"High Score: {high_score}", font, (255, 255, 255), (WIDTH // 2, high_score_y), center=True)

        
        # Draw the "Leaderboard" button
        pygame.draw.rect(window.screen, (0, 0, 200), leaderboard_rect, border_radius=10)  # Blue button with rounded corners
        window.draw_text("Leaderboard", font, (255, 255, 255), leaderboard_rect.center, center=True)

        # Draw the "Play Again" button
        pygame.draw.rect(window.screen, (0, 200, 0), play_again_rect, border_radius=10)  # Green button with rounded corners
        window.draw_text("Play Again", font, (255, 255, 255), play_again_rect.center, center=True)

        # Draw the "Quit" button
        pygame.draw.rect(window.screen, (200, 0, 0), quit_rect, border_radius=10)  # Red button with rounded corners
        window.draw_text("Quit", font, (255, 255, 255), quit_rect.center, center=True)

        # Update the display
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if leaderboard_rect.collidepoint(mouse_x, mouse_y):
                    leaderboard_screen = LeaderboardScreen(window)
                    leaderboard_screen.show()  # Show the leaderboard screen
                if play_again_rect.collidepoint(mouse_x, mouse_y):
                    return True  # Restart the game
                if quit_rect.collidepoint(mouse_x, mouse_y):
                    return False  # Quit the game

if __name__ == "__main__":
    main()