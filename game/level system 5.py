import sys
import random
import pygame

pygame.init()
clock = pygame.time.Clock()

# Window
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mushroom Collector")

# Colors
BLUE = (100, 100, 200)
YELLOW = (200, 200, 100)
GREEN = (100, 200, 100)
BROWN = (139, 69, 19)
RED = (220, 50, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)

# Fonts
font_large = pygame.font.SysFont("arial", 60)
font_medium = pygame.font.SysFont("arial", 40)

class Assets:
    def __init__(self):   
        self.player_size = 40
        self.player = pygame.Rect(100, 100, self.player_size, self.player_size)
        self.player_speed = 10
        self.mushroom_radius = 15
        self.mushrooms = []

    def Player(self):
        """Draw the player and return the player rect."""
        player = self.player
        player_size = self.player_size
        player_speed = self.player_speed
        pygame.draw.circle(win, WHITE, player.center, self.player_size // 2)
        pygame.draw.circle(win, BLACK, (player.centerx - 10, player.centery - 10), 5)
        pygame.draw.circle(win, BLACK, (player.centerx + 10, player.centery - 10), 5)
        pygame.draw.arc(win, BLACK, (player.centerx - 10, player.centery - 5, 20, 15), 3.14, 0, 2)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.x < WIDTH - player_size:
            player.x += player_speed
        if keys[pygame.K_UP] and player.y > 0:
            player.y -= player_speed
        if keys[pygame.K_DOWN] and player.y < HEIGHT - player_size:
            player.y += player_speed

        return self.player  # Return the player rect for collision detection

    def Mushroom(self):
        """Create mushrooms and return the list of mushrooms."""
        if not self.mushrooms:  # Only generate mushrooms once
            for _ in range(5):  # Reduce the number of mushrooms to 50 for performance
                x = random.randint(50, WIDTH - 50)
                y = random.randint(50, HEIGHT - 50)
                self.mushrooms.append(pygame.Rect(x, y, self.mushroom_radius * 2, self.mushroom_radius * 2))

        for m in self.mushrooms:
            pygame.draw.rect(win, BROWN, (m.centerx - 3, m.bottom - 10, 6, 10))  # Mushroom stem
            pygame.draw.ellipse(win, RED, (m.x, m.y, self.mushroom_radius * 2, self.mushroom_radius))  # Mushroom cap
        
        return self.mushrooms  # Return the mushrooms list for collision detection


class Assets2:
    def __init__(self):   
        self.player_size = 40
        self.player = pygame.Rect(100, 100, self.player_size, self.player_size)
        self.player_speed = 10
        self.mushroom_radius = 15
        self.mushrooms = []

    def Player(self):
        """Draw the player and return the player rect."""
        player = self.player
        player_size = self.player_size
        player_speed = self.player_speed
        pygame.draw.circle(win, WHITE, player.center, self.player_size // 2)
        pygame.draw.circle(win, BLACK, (player.centerx - 10, player.centery - 10), 5)
        pygame.draw.circle(win, BLACK, (player.centerx + 10, player.centery - 10), 5)
        pygame.draw.arc(win, BLACK, (player.centerx - 10, player.centery - 5, 20, 15), 3.14, 0, 2)
        pygame.draw.rect(win, BLACK, (player.centerx - 7, player.centery - 10, 14, 2) )
 

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.x < WIDTH - player_size:
            player.x += player_speed
        if keys[pygame.K_UP] and player.y > 0:
            player.y -= player_speed
        if keys[pygame.K_DOWN] and player.y < HEIGHT - player_size:
            player.y += player_speed

        return self.player  # Return the player rect for collision detection

    def Mushroom(self):
        """Create mushrooms and return the list of mushrooms."""
        if not self.mushrooms:  # Only generate mushrooms once
            for _ in range(5):  # Reduce the number of mushrooms to 50 for performance
                x = random.randint(50, WIDTH - 50)
                y = random.randint(50, HEIGHT - 50)
                self.mushrooms.append(pygame.Rect(x, y, self.mushroom_radius * 2, self.mushroom_radius * 2))

        for m in self.mushrooms:
            pygame.draw.rect(win, BROWN, (m.centerx - 3, m.bottom - 10, 6, 10))  # Mushroom stem
            pygame.draw.ellipse(win, RED, (m.x, m.y, self.mushroom_radius * 2, self.mushroom_radius))  # Mushroom cap
        
        return self.mushrooms  # Return the mushrooms list for collision detection


class Assets3:
    def __init__(self):   
        self.player_size = 40
        self.player = pygame.Rect(100, 100, self.player_size, self.player_size)
        self.player_speed = 10
        self.mushroom_radius = 15
        self.mushrooms = []

    def Player(self):
        """Draw the player and return the player rect."""
        player = self.player
        player_size = self.player_size
        player_speed = self.player_speed
        pygame.draw.circle(win, WHITE, player.center, self.player_size // 2)
        pygame.draw.circle(win, BLACK, (player.centerx - 10, player.centery - 10), 5)
        pygame.draw.circle(win, BLACK, (player.centerx + 10, player.centery - 10), 5)
        pygame.draw.arc(win, BLACK, (player.centerx - 10, player.centery - 5, 20, 15), 3.14, 0, 2)
        #pygame.draw.ellipse(win, (BLACK), (player.centerx - 15, player.centery - 25, 30, 15))  
        #pygame.draw.rect(win, (BLACK), (player.centerx - 10, player.centery - 15, 20, 5)) 
        pygame.draw.ellipse(win, (YELLOW), (player.centerx - 15, player.centery - 30, 30, 15), 4)
        

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.x < WIDTH - player_size:
            player.x += player_speed
        if keys[pygame.K_UP] and player.y > 0:
            player.y -= player_speed
        if keys[pygame.K_DOWN] and player.y < HEIGHT - player_size:
            player.y += player_speed

        return self.player  # Return the player rect for collision detection

    def Mushroom(self):
        """Create mushrooms and return the list of mushrooms."""
        if not self.mushrooms:  # Only generate mushrooms once
            for _ in range(5):  # Reduce the number of mushrooms to 50 for performance
                x = random.randint(50, WIDTH - 50)
                y = random.randint(50, HEIGHT - 50)
                self.mushrooms.append(pygame.Rect(x, y, self.mushroom_radius * 2, self.mushroom_radius * 2))

        for m in self.mushrooms:
            pygame.draw.rect(win, BROWN, (m.centerx - 3, m.bottom - 10, 6, 10))  # Mushroom stem
            pygame.draw.ellipse(win, RED, (m.x, m.y, self.mushroom_radius * 2, self.mushroom_radius))  # Mushroom cap
        
        return self.mushrooms  # Return the mushrooms list for collision detection

class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        text_surface = font_medium.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)



def Next_level(current_level):
    running = True
    pygame.event.clear()
    start_ticks = pygame.time.get_ticks()

    while running:
        elapsed_time = pygame.time.get_ticks() - start_ticks

        win.fill(GREEN)
        title_text = font_large.render("Level complete", True, BLACK)
        press_key = font_medium.render("Press any key to continue", True, BLACK)
        
        win.blit(title_text, title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
        win.blit(press_key, press_key.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))
        
        pygame.display.flip()

        if elapsed_time > 1000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    running = False
                    if current_level == 1:
                        Game2()
                    elif current_level == 2:
                        Game3()
                    
                   




def Menu():
    running = True
    play_button = Button("Play", WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 60)
    quit_button = Button("Quit", WIDTH // 2 - 100, HEIGHT // 2 + 30, 200, 60)
    
    clock = pygame.time.Clock()  # Create a clock to control frame rate
    while running:
        win.fill(WHITE)  # Fill the screen with white color

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the loop if the window is closed

            # Handle mouse click events for buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # Get mouse position
                if play_button.is_clicked(mouse_pos):
                    # Change the game state to Game and break out of the menu
                    state = Game()  # Call Game function when "Play" is clicked
                    running = False  # Exit the menu loop
                elif quit_button.is_clicked(mouse_pos):
                    running = False  # Exit the loop if "Quit" is clicked

        # Draw buttons
        play_button.draw(win)  # Ensure you draw the play button
        quit_button.draw(win)  # Ensure you draw the quit button

        

        # Limit the frame rate to avoid flickering and to make sure the menu is smooth
        clock.tick(60)  # Limiting to 60 frames per second


       
        menu_text = font_large.render("Main Menu", True, BLACK)
        win.blit(menu_text, menu_text.get_rect(center=(WIDTH // 2, 100)))
        pygame.display.flip()  # Update the display once per loop


    

       



def Game():
    running = True
    assets = Assets()
    score = 0
    font = pygame.font.Font(None, 36)  # Set font for score display
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



        # Check for player collision with mushrooms
        win.fill(GREEN)
        player = assets.Player()
        mushrooms = assets.Mushroom()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            pass
        
        for m in mushrooms[:]:
            if player.colliderect(m):
                mushrooms.remove(m)  # Remove mushroom on collision
                score += 1  # Increase score


        if len(mushrooms) == 0:
            running = False
            Next_level(1)

        # Display score
        text = font.render(f"Score: {score}", True, BLACK)
        win.blit(text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Control frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()


def Game2():
    running = True
    assets = Assets2()
    score = 0
    font = pygame.font.Font(None, 36)  # Set font for score display
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



        # Check for player collision with mushrooms
        win.fill(GRAY)
        player = assets.Player()
        mushrooms = assets.Mushroom()
        
        
        for m in mushrooms[:]:
            if player.colliderect(m):
                mushrooms.remove(m)  # Remove mushroom on collision
                score += 1  # Increase score


        if len(mushrooms) == 0:
            running = True
            Next_level(2)

        # Display score
        text = font.render(f"Score: {score}", True, BLACK)
        win.blit(text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Control frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()


def Game3():
    running = True
    assets = Assets3()
    score = 0
    font = pygame.font.Font(None, 36)  # Set font for score display
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



        # Check for player collision with mushrooms
        win.fill(BLUE)
        player = assets.Player()
        mushrooms = assets.Mushroom()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            pass
        
        for m in mushrooms[:]:
            if player.colliderect(m):
                mushrooms.remove(m)  # Remove mushroom on collision
                score += 1  # Increase score


        if len(mushrooms) == 0:
            running = False
            Game()

        # Display score
        text = font.render(f"Score: {score}", True, BLACK)
        win.blit(text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Control frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()


Menu()
