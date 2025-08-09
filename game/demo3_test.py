import sys
import math
import random
import pygame


pygame.init()
clock = pygame.time.Clock()

#Music 
#pygame.mixer.music.set_volume(0.2)
#pygame.mixer.music.load('yoshi.mp3')
#pygame.mixer.music.play(-1)


# Window
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mushroom Collector")

# Colors
BLUE = (100, 100, 200)
YELLOW = (200, 200, 100)
GOLD = (255, 215, 0)
GREEN = (100, 200, 100)
BROWN = (139, 69, 19)
RED = (220, 50, 50)
PINK = (255, 0, 127)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
GRAY2 = (80, 80, 80)

# Fonts
font_large = pygame.font.SysFont("arial", 60)
font_medium = pygame.font.SysFont("arial", 40)

#Level system
max_level = 4
cureent_skin = "none"

My_skins = {
    1: {"skin": "none", "unlocked": True},
    2: {"skin": "glases", "unlocked": False},
    3: {"skin": "angel", "unlocked": False},
    4: {"skin": "bro", "unlocked": False},
    5: {"skin": "girl", "unlocked": True},
    6: {"skin": "cat", "unlocked": True},
    7: {"skin": "nerd", "unlocked": True}
    
}


Levels_completed = {}


LEVELS = {
    1: {"level_color": GREEN, "with_spikes": False},
    2: {"level_color": GRAY, "with_spikes": True},
    3: {"level_color": BLUE, "with_spikes": False},
    4: {"level_color": YELLOW, "with_spikes": False},
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
        self.with_spikes = config.get("with_spikes", False)

    def Player(self):
        """Draw the player and return the player rect."""
        player = self.player
        player_size = self.player_size
        player_speed = self.player_speed
        self.skin_type = cureent_skin 
        skins = self.Player_skin()
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
        return self.player

    def Player_skin(self):
        player = self.player
        return {
            "none": lambda: None,
            "glases": lambda: pygame.draw.rect(win, BLACK, (player.centerx - 7, player.centery - 10, 14, 2)),
            "angel": lambda: pygame.draw.ellipse(win, (GOLD), (player.centerx - 15, player.centery - 30, 30, 15), 4),
            "bro": lambda: pygame.draw.ellipse(win, (BLACK), (player.centerx - 15, player.centery - 25, 30, 15)),
            "girl": lambda:
            (pygame.draw.polygon(win, PINK, [
        (player.centerx + 10, player.centery - 30),  # Top of the triangle
        (player.centerx , player.centery - 20),  # Bottom-left
        (player.centerx + 18, player.centery - 10)  # Bottom-right
        ]),
        pygame.draw.polygon(win, PINK, [
        (player.centerx - 10, player.centery - 30),  # Top of the triangle
        (player.centerx , player.centery - 20),  # Bottom-left
        (player.centerx - 18, player.centery - 10)  # Bottom-right
        ])),
        "cat": lambda: 
        (pygame.draw.polygon(win, BLACK, [
        (player.centerx + 10, player.centery - 30),  # Top of the triangle
        (player.centerx + 5, player.centery - 20),  # Bottom-left
        (player.centerx + 18, player.centery - 10)  # Bottom-right
        ]),
        pygame.draw.polygon(win, BLACK, [
        (player.centerx - 10, player.centery - 30),  # Top of the triangle
        (player.centerx - 5, player.centery - 20),  # Bottom-left
        (player.centerx - 18, player.centery - 10)  # Bottom-right
        ]),
        pygame.draw.rect(win, BLACK, (player.centerx - 25, player.centery + 5, 12, 2) ),
        pygame.draw.rect(win, BLACK, (player.centerx - 25, player.centery + 1, 12, 2) ),
        pygame.draw.rect(win, BLACK, (player.centerx - 25, player.centery - 3, 12, 2) ),

        pygame.draw.rect(win, BLACK, (player.centerx + 13, player.centery + 5, 12, 2) ),
        pygame.draw.rect(win, BLACK, (player.centerx + 13, player.centery + 1, 12, 2) ),
        pygame.draw.rect(win, BLACK, (player.centerx + 13, player.centery - 3, 12, 2) )),
         "nerd": lambda:
         (pygame.draw.circle(win, BLACK, (player.centerx - 10, player.centery - 10), 8, 1),
          pygame.draw.circle(win, BLACK, (player.centerx + 10, player.centery - 10), 8, 1),
          pygame.draw.rect(win, BLACK, (player.centerx - 3, player.centery - 10, 6, 2) ))
        }

    def Control(self):
        player = self.player
        player_speed = self.player_speed
        player_size = self.player_size
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





    def Mushroom(self):
        """Create mushrooms and spikes, draw them, and return their rect lists."""
        # Generate mushrooms once
        if not self.mushrooms:
            for _ in range(1):
                x = random.randint(50, WIDTH - 50)
                y = random.randint(50, HEIGHT - 50)
                rect = pygame.Rect(x, y, self.mushroom_radius * 2, self.mushroom_radius * 2)
                self.mushrooms.append(rect)

        # Draw mushrooms
        for m in self.mushrooms:
            pygame.draw.rect(win, BROWN, (m.centerx - 3, m.bottom - 10, 6, 10))  # stem
            pygame.draw.ellipse(win, RED, (m.x, m.y, self.mushroom_radius * 2, self.mushroom_radius))  # cap

        # Generate spikes once (if needed)
        if self.with_spikes and not self.spikes_generated:
            for _ in range(50):
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
        control = assets.Control()
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
            # proceed only if this level isn't already marked completed
            if not Levels_completed.get(level_num, {}).get("completed", False):
                Levels_completed[level_num] = {"completed": True}
                running = False
                New_skin(level_num)
            elif level_num == max_level:
                running = False
                Victory()
            else:
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


def Skin_menu():
    running = True
    pos = 1
    assets = Assets(LEVELS[1])
    global cureent_skin
    global My_skins
    previous_skin = cureent_skin
    prev_button = Button("Previous", WIDTH // 2 - 350, HEIGHT // 2 + 150 , 150, 100)
    next_button = Button("Next", WIDTH // 2 + 200, HEIGHT // 2 + 150 , 150, 100)
    back_button = Button("Back", WIDTH // 2 - 75, HEIGHT // 2 + 150 , 150, 100)
    pygame.event.clear()

    def get_next_pos(current_pos, skins, forward=True):
        pos = current_pos
        while True:
            if forward:
                pos += 1
                if pos > len(skins):
                    pos = 1
            else:
                pos -= 1
                if pos < 1:
                    pos = len(skins)
            if skins[pos]["unlocked"]:
                return pos

    while running:
        win.fill(GREEN)  # Fill the screen with green color
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the loop if the window is closed
                pygame.quit()
                sys.exit()

            # Handle mouse click events for buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # Get mouse position
                if prev_button.is_clicked(mouse_pos):
                    pos = get_next_pos(pos, My_skins, forward=False)
                elif next_button.is_clicked(mouse_pos):
                    pos = get_next_pos(pos, My_skins, forward=True)
                elif back_button.is_clicked(mouse_pos):
                    running = False
                    Menu()

        # Set current skin based on unlocked status
        if not My_skins[pos]["unlocked"]:
            cureent_skin = "none"
        else:
            cureent_skin = My_skins[pos]["skin"]

        # Draw buttons
        prev_button.draw(win)  
        next_button.draw(win)  
        back_button.draw(win) 

        # Draw menu text
        menu_text = font_large.render("Select your skin", True, BLACK)
        win.blit(menu_text, menu_text.get_rect(center=(WIDTH // 2, 100)))

        # Position player in center and draw
        assets.player.x = WIDTH // 2 - assets.player_size // 2
        assets.player.y = HEIGHT // 2 - assets.player_size // 2
        player = assets.Player()

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS


def Next_level(current_level):
    if current_level == max_level:
        Victory()
    else:
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
                            if current_level == max_level:
                                Victory()
                            elif current_level >= 0:
                                running = False
                                Game(current_level + 1)
    
                          

def New_skin(current_level):
    if current_level == 1:
        Next_level(1)
    else:
        running = True
        assets = Assets(LEVELS[1])
        global cureent_skin
        global My_skins
        previous_skin = cureent_skin
        cureent_skin = My_skins[current_level]["skin"]
        Equip_button = Button("Equip", WIDTH // 2 - 350, HEIGHT // 2 + 150 , 300, 100)
        add_button = Button("Add to collection", WIDTH // 2 + 50, HEIGHT // 2 + 150 , 300, 100)
        pygame.event.clear()

        while running:
            win.fill(GREEN)  # Fill the screen with white color

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # Exit the loop if the window is closed
                    pygame.quit()
                    sys.exit()

                # Handle mouse click events for buttons
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos  # Get mouse position
                    if Equip_button.is_clicked(mouse_pos):
                        if current_level == max_level:
                            Victory()
                        else:
                            Game(current_level + 1)  
                            running = False  
                    elif add_button.is_clicked(mouse_pos):
                        if current_level == max_level:
                            Victory()
                        else:
                            cureent_skin = previous_skin
                            Game(current_level + 1)
                            running = False
            
            My_skins[current_level]["unlocked"] = True

            # Draw buttons
            Equip_button.draw(win)  
            add_button.draw(win)  

            

            # Limit the frame rate to avoid flickering and to make sure the menu is smooth
            clock.tick(60)  # Limiting to 60 frames per second


        
            menu_text = font_large.render("New skin unlocked", True, BLACK)
            win.blit(menu_text, menu_text.get_rect(center=(WIDTH // 2, 100)))
            assets.player.x = WIDTH // 2 - 20
            assets.player.y = HEIGHT // 2 - 100
            player = assets.Player()
            pygame.display.flip()  
  

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
    skin_button = Button("Skins", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 60)
    quit_button = Button("Quit", WIDTH // 2 - 100, HEIGHT // 2 + 200, 200, 60)
    
    
    clock = pygame.time.Clock()  # Create a clock to control frame rate
    while running:
        win.fill(WHITE)  # Fill the screen with white color

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the loop if the window is closed
                pygame.quit()
                sys.exit()

            # Handle mouse click events for buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # Get mouse position
                if play_button.is_clicked(mouse_pos):
                    Game(1)  # Call Game function when "Play" is clicked
                    running = False  # Exit the menu loop
                elif quit_button.is_clicked(mouse_pos):
                    running = False  # Exit the loop if "Quit" is clicked
                    pygame.quit()
                    sys.exit()
                elif level_button.is_clicked(mouse_pos):
                    running = False  
                    Level_select()
                elif skin_button.is_clicked(mouse_pos):
                    running = False  
                    Skin_menu()

        # Draw buttons
        play_button.draw(win)  # Ensure you draw the play button
        quit_button.draw(win)  # Ensure you draw the quit button
        level_button.draw(win)
        skin_button.draw(win)

        

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
                pygame.quit()
                sys.exit()


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
                pygame.quit()
                sys.exit()

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