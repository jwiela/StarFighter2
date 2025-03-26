import pygame 

BACKGROUND_IMAGE_PATH = 'images/background.jpg'

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
        self.screen.fill((0, 0, 0))

    def draw_text(self, text, font, color, position):
        rendered_text = font.render(text, True, color)
        self.screen.blit(rendered_text, position)
    