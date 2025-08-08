import sys
import math
import random
import pygame


pygame.init()
clock = pygame.time.Clock()

#Music 
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.load('yoshi.mp3')
pygame.mixer.music.play(-1)


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
PINK = (255, 192, 203)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
GRAY2 = (80, 80, 80)

# Fonts
font_large = pygame.font.SysFont("arial", 60)
font_medium = pygame.font.SysFont("arial", 40)

LEVELS = {
    1: {"level_color": GREEN, "skin_type": "none", "with_spikes": False},
    2: {"level_color": GRAY, "skin_type": "glases", "with_spikes": True},
    3: {"level_color": BLUE, "skin_type": "angel", "with_spikes": False},
    4: {"level_color": YELLOW, "skin_type": "bro", "with_spikes": False},
}

class Assets:
    def __init__(self, config):   
        self.player_size = 40
        self.player = pygame.Rect(100, 100, self.player_size, self.player_size)
        self.player_speed = 12
        self.mushroom_radius = 15
        self.mushrooms = []
        self.spike = []
        self.spike_rects = []
        self.safe_distance = 60
        self.spikes_generated = False
        self.level_color = config.get("level_color", GREEN)
        self.skin_type = config.get("skin_type", "none")
        self.with_spikes = config.get("with_spikes", False)

    def Player(self):
        """Draw the player and return the player rect."""
        player = self.player
        player_size = self.player_size
        player_speed = self.player_speed
        self.Player_skin()

        #drawing Player
        skins = self.Player_skin()
        draw_func = skins.get(self.skin_type)
        if draw_func:
            pygame.draw.circle(win, WHITE, player.center, self.player_size // 2)
            pygame.draw.circle(win, BLACK, (player.centerx - 10, player.centery - 10), 5)
            pygame.draw.circle(win, BLACK, (player.centerx + 10, player.centery - 10), 5)
            pygame.draw.arc(win, BLACK, (player.centerx - 10, player.centery - 5, 20, 15), 3.14, 0, 2)
            draw_func()

        #controll
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.x < WIDTH - player_size:
            player.x += player_speed
        if keys[pygame.K_UP] and player.y > 0:
            player.y -= player_speed
        if keys[pygame.K_DOWN] and player.y < HEIGHT - player_size:
            player.y += player_speed
        if keys[pygame.K_ESCAPE]:
            Menu()

        return self.player
              



    def Player_skin(self):
        player = self.player
        return {
            "none": lambda: None,
            "glases": lambda: pygame.draw.rect(win, BLACK, (player.centerx - 7, player.centery - 10, 14, 2)),
            "angel": lambda: pygame.draw.ellipse(win, (YELLOW), (player.centerx - 15, player.centery - 30, 30, 15), 4),
            "bro": lambda: pygame.draw.ellipse(win, (BLACK), (player.centerx - 15, player.centery - 25, 30, 15)),
        }


    def Mushroom(self):
        """Create mushrooms and spikes, draw them, and return their rect lists."""
        # Generate mushrooms once
        if not self.mushrooms:
            for _ in range(5):
                x = random.randint(50, WIDTH - 50)
                y = random.randint(50, HEIGHT - 50)
                rect = pygame.Rect(x, y, self.mushroom_radius * 2, self.mushroom_radius * 2)
                self.mushrooms.append(rect)

        # Draw mushrooms
        for m in self.mushrooms:
            pygame.draw.rect(win, BROWN, (m.centerx - 3, m.bottom - 10, 6, 10))  # stem
            pygame.draw.ellipse(win, RED, (m.x, m.y, self.mushroom_radius * 2, self.mushroom_radius))  # cap

        # Generate spikes once (if needed)
        if self.with_spikes :
            start_ticks = pygame.time.get_ticks()
            for _ in range(1):
                elapsed_time = pygame.time.get_ticks() - start_ticks
                if elapsed_time > 1000:
                    while True:
                        x = random.randint(50, WIDTH - 50)
                        y = random.randint(50, HEIGHT - 50)
                        too_close = False

                        # Too close to a mushroom?
                        for m in self.mushrooms:
                            dist = math.sqrt((x - m.centerx) ** 2 + (y - m.centery) ** 2)
                            if dist < self.safe_distance:
                                too_close = True
                                break

                        # Too close to player?
                        if not too_close:
                            px, py = self.player.center
                            dist_to_player = math.sqrt((x - px) ** 2 + (y - py) ** 2)
                            if dist_to_player < self.safe_distance:
                                too_close = True

                        if not too_close:
                            vertices = [(x, y), (x - 15, y + 30), (x + 15, y + 30)]
                            self.spike.append(vertices)
                            self.spike_rects.append(pygame.Rect(x - 15, y, 30, 30))  # collision rect
                            break

                self.spikes_generated = True
            
        # Draw spikes
        for s in self.spike:
            pygame.draw.polygon(win, BLACK, s)

        return self.mushrooms, self.spike_rects


def Game(level_num):
    config = LEVELS[level_num]
    assets = Assets(config)
    max_level = 4
    running = True
    score = 0
    font = pygame.font.Font(None, 36)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        win.fill(assets.level_color)
        player = assets.Player()

        mushrooms, spikes = assets.Mushroom()  # Now always two lists

        # Mushroom collision
        for m in mushrooms[:]:
            if player.colliderect(m):
                mushrooms.remove(m)
                score += 1

        # Spike collision
        for rect in spikes:
            if player.colliderect(rect):
                Over()

        # Level complete
        if len(mushrooms) == 0:
            if level_num == max_level:
                Victory()
            else:
                running = False
                Next_level(level_num)

        # HUD
        win.blit(font.render(f"Score: {score}", True, BLACK), (10, 10))
        win.blit(font.render(f"Level: {level_num}", True, BLACK), (10, 30))

        pygame.display.flip()
        clock.tick(60)


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


class Button2:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY2, self.rect)
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
        press_key = font_medium.render("Press SPACE to continue", True, BLACK)
        
        win.blit(title_text, title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
        win.blit(press_key, press_key.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))
        
        pygame.display.flip()

        if elapsed_time > 1000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
                        if current_level == 1:
                            Game(2)
                        elif current_level == 2:
                            Game(3)
                        elif current_level == 3:
                            Game(4)


def Over():
    running = True
    pygame.event.clear()
    start_ticks = pygame.time.get_ticks()

    while running:
        elapsed_time = pygame.time.get_ticks() - start_ticks

        win.fill(GREEN)
        title_text = font_large.render("Game over", True, BLACK)
        press_key = font_medium.render("Press SPACE to try again", True, BLACK)
        
        win.blit(title_text, title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
        win.blit(press_key, press_key.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))
        
        pygame.display.flip()

        if elapsed_time > 1000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
                        Game(2)                 




def Menu():
    running = True
    play_button = Button("Play", WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 60)
    level_button = Button("Levels", WIDTH // 2 - 100, HEIGHT // 2 , 200, 60)
    quit_button = Button("Quit", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 60)
    
    
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
                    Game(1)  # Call Game function when "Play" is clicked
                    running = False  # Exit the menu loop
                elif quit_button.is_clicked(mouse_pos):
                    running = False  # Exit the loop if "Quit" is clicked
                    pygame.quit()
                    sys.exit()
                elif level_button.is_clicked(mouse_pos):
                    running = False  # Exit the loop if "Quit" is clicked
                    Level_select()

        # Draw buttons
        play_button.draw(win)  # Ensure you draw the play button
        quit_button.draw(win)  # Ensure you draw the quit button
        level_button.draw(win)

        

        # Limit the frame rate to avoid flickering and to make sure the menu is smooth
        clock.tick(60)  # Limiting to 60 frames per second


       
        menu_text = font_large.render("Mushroom Collector", True, BLACK)
        win.blit(menu_text, menu_text.get_rect(center=(WIDTH // 2, 100)))
        pygame.display.flip()  # Update the display once per loop


def Level_select():
    running = True
    L1_button = Button("Level 1", WIDTH // 2 - 100, HEIGHT // 2 - 250, 200, 60)
    L2_button = Button("Level 2", WIDTH // 2 - 100, HEIGHT // 2 - 150 , 200, 60)
    L3_button = Button("Level 3", WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 60)
    L4_button = Button("Level 4", WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 60)
    Back_button = Button("Back", WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 60)
    
    
    clock = pygame.time.Clock()  # Create a clock to control frame rate
    while running:
        win.fill(WHITE)  # Fill the screen with white color

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  


            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # Get mouse position
                if  L1_button.is_clicked(mouse_pos):
                    Game(1)  # Call Game function when "Play" is clicked
                    running = False  # Exit the menu loop
                elif L2_button.is_clicked(mouse_pos):
                    Game(2)
                    running = False  # Exit the loop if "Quit" is clicked
                elif L3_button.is_clicked(mouse_pos):
                    Game(3)
                    running = False  # Exit the loop if "Quit" is clicked
                elif L4_button.is_clicked(mouse_pos):
                    Game(4)
                    running = False  # Exit the loop if "Quit" is clicked
                elif Back_button.is_clicked(mouse_pos):
                    Menu()
                    running = False  # Exit the loop if "Quit" is clicked


        # Draw buttons
        L1_button.draw(win)  # Ensure you draw the play button
        L2_button.draw(win)  # Ensure you draw the quit button
        L3_button.draw(win)
        L4_button.draw(win)
        Back_button.draw(win)

        

        # Limit the frame rate to avoid flickering and to make sure the menu is smooth
        clock.tick(60)  # Limiting to 60 frames per second


       
        #menu_text = font_large.render("Mushroom Collector", True, BLACK)
        #win.blit(menu_text, menu_text.get_rect(center=(WIDTH // 2, 100)))
        pygame.display.flip()  # Update the display once per loop



def Victory():
    running = True
    play_button = Button("Play again", WIDTH // 2 - 250, HEIGHT // 2 - 45 , 200, 150)
    quit_button = Button("Quit", WIDTH // 2 + 50, HEIGHT // 2 - 45 , 200, 150)
    
    clock = pygame.time.Clock()  # Create a clock to control frame rate
    while running:
        win.fill(GREEN)  # Fill the screen with white color

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the loop if the window is closed

            # Handle mouse click events for buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # Get mouse position
                if play_button.is_clicked(mouse_pos):
                    state = Game(1)  
                    running = False  
                elif quit_button.is_clicked(mouse_pos):
                    running = False  # Exit the loop if "Quit" is clicked
                    pygame.quit()
                    sys.exit()

        # Draw buttons
        play_button.draw(win)  # Ensure you draw the play button
        quit_button.draw(win)  # Ensure you draw the quit button

        

        # Limit the frame rate to avoid flickering and to make sure the menu is smooth
        clock.tick(60)  # Limiting to 60 frames per second


       
        menu_text = font_large.render("YOU WON", True, BLACK)
        win.blit(menu_text, menu_text.get_rect(center=(WIDTH // 2, 100)))
        pygame.display.flip()  # Update the display once per loop



Menu()