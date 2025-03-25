import pygame 

class GameWindow:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Star Fighter')

    def update(self):
        pygame.display.flip()
    
    def clear(self):
        self.screen.fill((0, 0, 0))

    def draw_text(self, text, font, color, position):
        rendered_text = font.render(text, True, color)
        self.screen.blit(rendered_text, position)