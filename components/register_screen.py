from utils.database import addUser
import pygame

class RegisterScreen:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)  # Larger font for the title
        self.input_box = pygame.Rect(300, 200, 200, 40)
        self.password_box = pygame.Rect(300, 260, 200, 40)
        self.register_button = pygame.Rect(300, 340, 200, 50)
        self.username = ''
        self.password = ''
        self.active_input = 'username'
        self.message = ''

    # Draws the register screen
    def draw(self):
        self.window.clear()

        # Background color
        self.window.screen.fill((30, 30, 30))  # Dark gray background

        # Title
        self.window.draw_text('Register', self.title_font, (255, 255, 255), (self.window.screen.get_width() // 2, 100), center=True)

        # Input boxes
        pygame.draw.rect(self.window.screen, (255, 255, 255), self.input_box, border_radius=10, width=2)
        pygame.draw.rect(self.window.screen, (255, 255, 255), self.password_box, border_radius=10, width=2)

        # Buttons
        pygame.draw.rect(self.window.screen, (0, 200, 0), self.register_button, border_radius=10)  # Green button

        # Labels
        self.window.draw_text('Username:', self.font, (255, 255, 255), (self.input_box.x - 140, self.input_box.y + 10))
        self.window.draw_text('Password:', self.font, (255, 255, 255), (self.password_box.x - 136, self.password_box.y + 10))

        # Input text
        self.window.draw_text(self.username, self.font, (255, 255, 255), (self.input_box.x + 10, self.input_box.y + 10))
        self.window.draw_text('*' * len(self.password), self.font, (255, 255, 255), (self.password_box.x + 10, self.password_box.y + 10))

        # Button text
        self.window.draw_text('Register', self.font, (255, 255, 255), self.register_button.center, center=True)

        # Error or success message
        if self.message:
            self.window.draw_text(self.message, self.font, (255, 0, 0), (self.window.screen.get_width() // 2, 500), center=True)

    # Handles events for the register screen
    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active_input == "username":
                if event.key == pygame.K_RETURN:
                    self.active_input = "password"
                elif event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                else:
                    self.username += event.unicode

            elif self.active_input == "password":
                if event.key == pygame.K_RETURN:
                    return self.handleRegister()
                elif event.key == pygame.K_BACKSPACE:
                    self.password = self.password[:-1]
                else:
                    self.password += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.input_box.collidepoint(x, y):
                self.active_input = "username"
            elif self.password_box.collidepoint(x, y):
                self.active_input = "password"
            elif self.register_button.collidepoint(x, y):
                return self.handleRegister()

    # Handles user registration
    def handleRegister(self):
        if self.username and self.password:
            addUser(self.username, self.password)
            self.message = "User registered successfully!"
            pygame.time.delay(1000)
            return 'login'  # Switch back to the login screen
        else:
            self.message = "Please fill in all fields."
            pygame.time.delay(1000)
            return None