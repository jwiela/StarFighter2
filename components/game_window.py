import pygame 
import os

BACKGROUND_IMAGE_PATH = os.path.join(os.path.dirname(__file__), '..', 'images', 'background.jpg')

class GameWindow:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Star Fighter')


        self.background = pygame.image.load(BACKGROUND_IMAGE_PATH)
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

    def update(self):
        pygame.display.flip()
    
    def clear(self):
        self.screen.blit(self.background, (0, 0))

    def draw_text(self, text, font, color, position, center=False):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = position
        else:
            text_rect.topleft = position
        self.screen.blit(text_surface, text_rect)
    