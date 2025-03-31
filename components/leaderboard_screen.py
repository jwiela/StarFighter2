import pygame
import sys
from utils.database import getTopScores

class LeaderboardScreen:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.back_button = pygame.Rect(300, 500, 200, 50)  # Back button rectangle

    def draw(self):
        self.window.clear()

        self.window.screen.fill((30, 30, 30))  # Fill the screen with black

        self.window.draw_text("Leaderboard", self.title_font, (255, 255, 0),(self.window.screen.get_width() // 2, 100), center = True)

        top_scres = getTopScores()
        for i, (username, highscore) in enumerate(top_scres):
            y_position = 150 + i * 40
            self.window.draw_text(f"{i + 1}. {username}: {highscore}", self.font, (255, 255, 255), (self.window.screen.get_width() // 2, y_position), center=True)

            pygame.draw.rect(self.window.screen, (200, 0, 0), self.back_button, border_radius=10)  # Draw the back button
            self.window.draw_text("Back", self.font, (255, 255, 255), self.back_button.center, center=True)

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.back_button.collidepoint(x, y):
                return "back"
    
    def show(self):
        """Displays the leaderboard screen."""
        while True:
            self.draw()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.handleEvent(event) == "back":
                    return