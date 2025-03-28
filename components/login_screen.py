import pygame 
from utils.database import addUser, authenticateUser

class LoginScreen:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.Font(None, 36)
        self.input_box = pygame.Rect(300, 200, 200, 40)
        self.password_box = pygame.Rect(300, 260, 200, 40)
        self.login_button = pygame.Rect(300, 320, 200, 50)
        self.register_button = pygame.Rect(300, 380, 200, 50)
        self.username = ''
        self.password = ''
        self.active_input = 'username'
        self.message = ''

    # Draws the login screen
    def draw(self):
        self.window.clear()
        self.window.draw_text('Login', self.font, (255, 255, 255), (360, 150))

        pygame.draw.rect(self.window.screen, (255, 255, 255), self.input_box, 2)
        pygame.draw.rect(self.window.screen, (255, 255, 255), self.password_box, 2)
        pygame.draw.rect(self.window.screen, (0, 200, 0), self.login_button)
        pygame.draw.rect(self.window.screen, (0, 0, 200), self.register_button)

        self.window.draw_text('Username', self.font, (255, 255, 255), (200, 205))
        self.window.draw_text('Password', self.font, (255, 255, 255), (200, 265))
        self.window.draw_text(self.username, self.font, (255, 255, 255), (310, 205))
        self.window.draw_text('*' * len(self.password), self.font, (255, 255, 255), (310, 265))
        self.window.draw_text('Login', self.font, (255, 255, 255), (370, 335))
        self.window.draw_text('Register', self.font, (255, 255, 255), (360, 395))

        if self.message:
            self.window.draw_text(self.message, self.font, (255, 0, 0), (300, 450))

    # Handles events for the login screen
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
                    self.handle_login()
                elif event.key == pygame.K_BACKSPACE:
                    self.password = self.password[:-1]
                else:
                    self.password += event.unicode
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x,y = event.pos
            if self.input_box.collidepoint(x, y):
                self.active_input = "username"
            elif self.password_box.collidepoint(x, y):
                self.active_input = "password"
            elif self.login_button.collidepoint(x, y):
                self.handleLogin()
            elif self.register_button.collidepoint(x, y):
                self.handleRegister()

    # Logs in the user
    def handleLogin(self):
        if authenticateUser(self.username, self.password):
            self.message = 'Login successful!'
            pygame.time.delay(1000)  # Delay to show message
            return True
        else:
            self.message = 'Invalid username or password.'

    def handleRegister(self):
        if self.username and self.password:
            addUser(self.username, self.password)
            self.message = 'User registered successfully!'
            pygame.time.delay(1000)
        else:
            self.message = 'Please enter a username and password.'
            pygame.time.delay(1000)
