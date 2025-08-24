import sys
import math
import random
import json
import pygame
import asyncio


pygame.init()
clock = pygame.time.Clock()


#Music 
try:
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.load('yoshi.mp3')
    pygame.mixer.music.play(-1)
except:
    print("No music found")

sound_effect = pygame.mixer.Sound("pickup.wav")
sound_effect.set_volume(0.3)

sound_hit = pygame.mixer.Sound("hit.wav")
sound_hit.set_volume(0.3)

sound_power = pygame.mixer.Sound("powerup.wav")
sound_power.set_volume(0.3)

# Window
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mushroom Collector")

# Colors

FOREST_GRADIENT = [
    (34, 139, 34),   # Forest green
    (0, 100, 0),     # Dark green
    (0, 70, 0),      # Deeper green
    (0, 50, 0)       # Darkest green
]

BLUE = (100, 100, 200)
YELLOW = (200, 200, 100)
GOLD = (255, 215, 0)
ORANGE = (255, 165, 0)
DARK_GREEN = (11, 46, 33)
GREEN = (100, 200, 100)
GREEN2 = (46,139,87)
GREEN3 = (60,179,113)
GREEN4 = (28,172,120)
BROWN = (139, 69, 19)
RED = (220, 50, 50)
PINK = (255, 0, 127)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
GRAY2 = (80, 80, 80)
ROCK_GREEN = (117, 129, 107)

ROCK_COLOR = (100, 100, 100)  # Medium gray
CRACKED_ROCK_COLOR = (110, 110, 110)  # Darker gray for cracked rocks
BREAKABLE_ROCK_COLOR = (80, 80, 80)  # Even darker for breakable rocks

# Fonts
font_large = pygame.font.SysFont("arial", 60)
font_medium = pygame.font.SysFont("arial", 40)

#Level system
current_skin = "none"
mushroom_inventory = 0
current_lang = 1

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

p = 3
e = 3
MODE = WHITE

LEVELS = {
    1: {"level_color": GREEN},
    2: {"level_color": GREEN3, "with_bad_mushrooms": True},
    3: {"level_color": GREEN2, "with_spikes": True},
    4: {"level_color": GREEN2, "with_chest": True},
    5: {"level_color": GREEN, "vacuum": True},
    6: {"level_color": GREEN, "moving_mushrooms": True},
    7: {"level_color": GREEN2, "sky_mushrooms": True},
    8: {"level_color": GREEN4, "with_flood": True},
    9: {"level_color": GREEN4, "with_enemy": True},
    10: {"level_color": ROCK_GREEN, "with_rocks": True, "breakable_rocks": True},
}

max_level = len(LEVELS)

class Localization:
    def __init__(self):
        self.texts = {}
        self.current_lang = 'en'  # Default to English
        
    def load_languages(self):
        """Load English and Ukrainian language files"""
        try:
            # Load English
            with open('en.json', 'r', encoding='utf-8') as f:
                self.texts['en'] = json.load(f)  # Fixed to 'en'
            
            # Load Ukrainian
            with open('ua.json', 'r', encoding='utf-8') as f:
                self.texts['ua'] = json.load(f)
        except FileNotFoundError as e:
            print(f"Language file error: {e}. Using default English texts.")
            # Create default English texts if files are missing
            self.texts['en'] = {
                "game_title": "Mushroom Collector",
                "menu_play": "Play",
                "menu_levels": "Levels",
                "menu_quit": "Quit",
                # Add other default texts here
            }
            self.texts['ua'] = self.texts['en']  # Fallback to English
    
    def set_language(self, lang_code):
        """Set current language ('en' or 'ua')"""
        if lang_code in ['en', 'ua']:
            self.current_lang = lang_code
    
    def get_text(self, key):
        """Get text in current language"""
        try:
            return self.texts[self.current_lang][key]
        except KeyError:
            # Fallback to English if key not found
            if 'en' in self.texts:  # Check if English exists
                return self.texts['en'].get(key, key)
            return key  # Ultimate fallback

loc = Localization()
loc.load_languages()

def t(key):
    """Short version of loc.get_text()"""
    return loc.get_text(key)

def LanguageMenu():
    def set_english():
        global current_lang
        current_lang = 1
        loc.set_language('en')
        Menu()
    
    def set_ukrainian():
        global current_lang
        current_lang = 2
        loc.set_language('ua')
        Menu()
    
    # Use the same colors and styling as your main menu
    button_color = (139, 69, 19)  # Brown color for buttons
    text_color = (255, 255, 255)  # White text
    
    # Create buttons with same style as Menu()
    english_btn = Button(t("Eglish"), WIDTH//2-100, HEIGHT//2-100, 200, 60, button_color, set_english, text_color)
    ukrainian_btn = Button(t("Ukrainian"), WIDTH//2-100, HEIGHT//2, 200, 60, button_color, set_ukrainian, text_color)
    back_btn = Button(t("menu_quit"), WIDTH//2-100, HEIGHT//2+100, 200, 60, button_color, Menu, text_color)
    
    # Add decorative elements to match main menu style
    def draw_decorations():
        # Same trees as in main menu
        tree_color = (101, 67, 33)  # Brown trunk
        leaf_color = (34, 139, 34)  # Green leaves
        
        # Left side trees
        pygame.draw.rect(win, tree_color, (50, 300, 20, 100))
        pygame.draw.polygon(win, leaf_color, [
            (30, 300), (90, 300), (60, 250)
        ])
        
        # Right side trees
        pygame.draw.rect(win, tree_color, (730, 400, 20, 100))
        pygame.draw.polygon(win, leaf_color, [
            (710, 400), (770, 400), (740, 350)
        ])
    
    # Create and run menu with same styling
    menu = BaseMenu(
        win, 
        font_medium, 
        font_large, 
        t("Select your language"), 
        [english_btn, ukrainian_btn, back_btn],
        use_gradient=True,
        extra_draw=draw_decorations
    )
    menu.run()

class Assets:
    def __init__(self, config):
        global MODE
        self.enemy_speed = 8
        # Initialize with the config data first
        self.with_chest = config.get("with_chest", False)  
        self.with_rocks = config.get("with_rocks", False)
        self.breakable_rocks = config.get("breakable_rocks", False)
        self.rocks = []  # List of rock rectangles
        self.rock_states = {}  # Track state of each rock (intact, cracked, broken)
        self.rock_hit_count = {}  # Track how many times each rock has been hit
        self.space_pressed = False

        self.rect_coords = []
        blockSize = 40

        # Now initialize the rest of the attributes
        self.player_size = 40
        self.player = pygame.Rect(90, 90, self.player_size, self.player_size)

        self.knockback = pygame.Vector2(0, 0)

        self.enemy = pygame.Rect(690, 100, self.player_size, self.player_size)
        self.key = None
        self.chest = None
        self.mushroom_inside_chest = None  # New attribute to store mushroom inside the chest

        # Only set key and chest if with_chest is True
        if self.with_chest:
            self.key = pygame.Rect(690, 100, 18, 50)
            self.chest = pygame.Rect(678, 400, self.player_size, self.player_size)

        self.min_speed = 1  # Starting speed when key is pressed
        self.max_speed = 12  # Maximum speed
        self.acceleration_rate = 1  # How fast speed increases over time
        self.player_speed = self.min_speed  # Current player speed
        self.mushroom_radius = 15
        self.mushrooms = []  # Mushrooms currently visible on the screen
        
        self.mushrooms_spawned = 0

        self.pre_spawned_mushrooms = []  # Mushrooms that are generated but not yet visible
        self.bad_mushrooms = []
        self.spike = []
        self.spike_rects = []
        self.super_m = []
        self.safe_distance = 60
        self.spikes_generated = False
        self.bad_mushrooms_generated = False
        self.level_color = config.get("level_color", GREEN)
        self.with_spikes = config.get("with_spikes", False)
        self.with_bad_mushrooms = config.get("with_bad_mushrooms", False)
        self.with_enemy = config.get("with_enemy", False)
        self.moving_mushrooms = config.get("moving_mushrooms", False)
        self.sky_mushrooms = config.get("sky_mushrooms", False)
        self.with_flood = config.get("with_flood", False)
        self.vacuum = config.get("vacuum", False)

        self.boss_start_time = pygame.time.get_ticks()
        self.phase_start = pygame.time.get_ticks()
        self.boss_cooldown = 60
        self.not_super = True
        self.super_state = False  # Add this line
        self.first_chase = True
        self.super_timer = 0      # Timer for super state duration
        self.projectiles = []
        self.boss_shot_offset = 0 

        self.last_spawn_time = 0  # Time of the last mushroom spawn (in ms)
        self.spawn_interval = 500  # 2 seconds in milliseconds
        self.mushroom_count = 20  # Total number of mushrooms to spawn
        self.spawned_mushrooms = 0  # Track how many mushrooms have been spawned

        self.flood = []

        # Loop through the grid and get coordinates
        for x in range(50, WIDTH - 50, blockSize):
            for y in range(50, HEIGHT - 50, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                self.rect_coords.append((x, y))  

        # MOVE ROCK GENERATION HERE - AFTER rect_coords IS POPULATED
        if self.with_rocks:
            self._generate_rocks()  

    def _generate_rocks(self):
        """Generate rocks that contain mushrooms"""
        num_rocks = 15  # Number of rocks to generate
        
        # Make sure we don't try to generate more rocks than available positions
        num_rocks = min(num_rocks, len(self.rect_coords))
        
        for _ in range(num_rocks):
            if self.rect_coords:
                # Get a random position
                random_rects = random.sample(self.rect_coords, 1)
                rand_x, rand_y = random_rects[0]
                x, y = rand_x, rand_y
                
                # Create rock rectangle (slightly larger than mushrooms)
                rock_size = self.mushroom_radius * 2 + 10
                rock_rect = pygame.Rect(x, y, rock_size, rock_size)
                
                # Remove this coordinate from available positions
                try:
                    self.rect_coords.remove((rand_x, rand_y))
                except ValueError:
                    pass
                
                # Add rock to the list
                self.rocks.append(rock_rect)
                self.rock_states[id(rock_rect)] = "intact"  # Track rock state
                self.rock_hit_count[id(rock_rect)] = 0  # Track hit count
                
                # Create a mushroom inside the rock (centered within the rock)
                mushroom_x = x + (rock_size - self.mushroom_radius * 2) // 2
                mushroom_y = y + (rock_size - self.mushroom_radius * 2) // 2
                mushroom_rect = pygame.Rect(mushroom_x, mushroom_y, 
                                          self.mushroom_radius * 2, self.mushroom_radius * 2)
                
                # Store the mushroom with its rock reference
                self.pre_spawned_mushrooms.append({
                    "rect": mushroom_rect,
                    "rock_id": id(rock_rect)
                })

    def Rocks(self):
        """Draw and handle rock interactions"""
        if not self.with_rocks:
            return []
            
        player = self.player
        
        for rock in self.rocks[:]:  # Iterate over a copy to allow removal
            rock_id = id(rock)
            state = self.rock_states.get(rock_id, "intact")
            
            # Draw the rock based on its state
            if state == "intact":
                pygame.draw.ellipse(win, ROCK_COLOR, rock)

                    
            elif state == "cracked":
                pygame.draw.ellipse(win, CRACKED_ROCK_COLOR, rock)
                # Draw cracks
                pygame.draw.line(win, (50, 50, 50), 
                                (rock.x + 5, rock.y + 5), 
                                (rock.x + rock.width - 5, rock.y + rock.height - 5), 2)
                pygame.draw.line(win, (50, 50, 50), 
                                (rock.x + rock.width - 5, rock.y + 5), 
                                (rock.x + 5, rock.y + rock.height - 5), 2)
                
            elif state == "broken":
                # Rock is broken, remove it and release the mushroom
                if rock in self.rocks:
                    self.rocks.remove(rock)
                    # Find and add the mushroom that was inside this rock
                    for mushroom_data in self.pre_spawned_mushrooms[:]:
                        if mushroom_data["rock_id"] == rock_id:
                            self.mushrooms.append(mushroom_data["rect"])
                            self.pre_spawned_mushrooms.remove(mushroom_data)
                            sound_effect.play()  # Play breaking sound
                            break
            
            # Check for player interaction with rock (for breaking)
            if self.breakable_rocks:
                # Calculate distance between player center and rock center
                player_center = player.center
                rock_center = rock.center
                distance = math.sqrt((player_center[0] - rock_center[0])**2 + (player_center[1] - rock_center[1])**2)
                
                # Define a "near" threshold (adjust as needed)
                near_threshold = 100  # pixels
                
                if distance < near_threshold:                    
                    # Player is near a breakable rock
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE] and not self.space_pressed:  # Check if space was just pressed
                        # Set flag to indicate space is pressed
                        self.space_pressed = True
                        
                        # Increase hit count
                        self.rock_hit_count[rock_id] += 1
                        
                        # Change state based on hit count
                        if self.rock_hit_count[rock_id] >= 3:
                            self.rock_states[rock_id] = "broken"
                        elif self.rock_hit_count[rock_id] >= 1:
                            self.rock_states[rock_id] = "cracked"
                    
                    # Reset flag when space is released
                    if not keys[pygame.K_SPACE]:
                        self.space_pressed = False
        
        
        return self.rocks

    def draw(self):
        """Basic draw method for cutscene rendering"""
        # Draw player (simplified version for cutscene)
        pygame.draw.rect(win, (255, 0, 0), self.player)
        
        # Draw any other elements needed for the cutscene
        if hasattr(self, 'npc'):
            pygame.draw.rect(win, (0, 0, 255), self.npc)
        
        # Draw bad mushrooms if they exist
        if hasattr(self, 'bad_mushrooms'):
            for b in self.bad_mushrooms:
                pygame.draw.ellipse(win, RED, b)
                # Draw stems and spots as needed

    def Key(self):
        # Safe draw (no error if key has been removed)
        if self.with_chest:
            if not self.key:
                return None
            k = self.key
            pygame.draw.circle(win, GOLD, (k.centerx, k.top + 10), self.player_size // 5)
            pygame.draw.rect(win, GOLD, (k.centerx - 3, k.y + 16, 6, 30)) 
            pygame.draw.rect(win, GOLD, (k.centerx - 9, k.bottom - 6, 12, 6))
            pygame.draw.rect(win, GOLD, (k.centerx - 9, k.bottom - 18, 12, 6))
            return k
        else:
            return None

    def Chest(self):
        # Safe draw
        if self.with_chest:
            if not self.chest:
                return None
            c = self.chest
            pygame.draw.rect(win, BROWN, (c.centerx - 20, c.y, 40, 40)) 
            pygame.draw.rect(win, BLACK, (c.centerx - 20, c.y + 15, 40, 5)) 
            pygame.draw.rect(win, BLACK, (c.centerx - 20, c.y , 5, 40)) 
            pygame.draw.rect(win, BLACK, (c.centerx + 15, c.y , 5, 40)) 
            pygame.draw.rect(win, BLACK, (c.centerx - 20, c.y, 40, 5)) 
            pygame.draw.rect(win, BLACK, (c.centerx - 20, c.y + 40, 40, 5))
            pygame.draw.rect(win, GOLD, (c.centerx - 3, c.centery - 5, 6, 5)) 
            return c
        else:
            return None

    def Enemy(self):
        enemy = self.enemy
        with_enemy = self.with_enemy

        player = self.player
        player_invincible = False
        invincible_timer = 0
        INVINCIBLE_TIME = 1000  # milliseconds (1 second of invincibility)

        enemy_size = self.player_size
        global p
        global e
        first_chase = self.first_chase

        center_x = WIDTH / 2
        center_y = HEIGHT / 2 - 20

        if with_enemy:
            if True:
                pygame.draw.ellipse(win, RED, (enemy.centerx - 30, enemy.centery - 40, 60, 50))
                pygame.draw.circle(win, ORANGE, enemy.center, self.player_size // 2)

                pygame.draw.circle(win, GOLD, (enemy.centerx - 22, enemy.centery - 18), 6) #mushroom spot
                pygame.draw.circle(win, GOLD, (enemy.centerx + 24, enemy.centery - 12), 5) #mushroom spot
                pygame.draw.circle(win, GOLD, (enemy.centerx - 14, enemy.centery - 32), 4) #mushroom spot
                pygame.draw.circle(win, GOLD, (enemy.centerx - 4, enemy.centery - 26), 5) #mushroom spot
                pygame.draw.circle(win, GOLD, (enemy.centerx + 13, enemy.centery - 28), 6) #mushroom spot
                
                pygame.draw.circle(win, BLACK, (enemy.centerx - 10, enemy.centery - 10), 5)
                pygame.draw.circle(win, BLACK, (enemy.centerx + 10, enemy.centery - 10), 5)
                pygame.draw.arc(win, BLACK, (enemy.centerx - 10, enemy.centery + 0, 20, 15), 0, 3.14, 2)


            # Total cycle duration in seconds
            cycle_duration = 21  # 10 + 10 + 1
            chase_duration = 10
            run_duration = 10
            pause_duration = 1
            shooting = False
            super = False
            

            elapsed = (pygame.time.get_ticks() - self.boss_start_time) / 1000
            cycle_time = elapsed % cycle_duration


            if elapsed > 1:
                if cycle_time < chase_duration:
                    shooting = False
                    if not self.first_chase:
                        super = True  # Only set super to True after the first chase
                    self.boss_cooldown = 60

                    # --- Chase phase ---
                    x_dist = enemy.centerx - player.centerx
                    y_dist = enemy.centery - player.centery
                    dist = (x_dist ** 2 + y_dist ** 2) ** 0.5 + 1
                    x_vel = x_dist / dist * self.enemy_speed
                    y_vel = y_dist / dist * self.enemy_speed

                    enemy.centerx -= x_vel
                    enemy.centery -= y_vel

                    


                elif cycle_time < chase_duration + run_duration:
                    shooting = True
                    self.first_chase = False
                    self.not_super = True
                    # Run to center
                    x2 = center_x - enemy.centerx
                    y2 = center_y - enemy.centery
                    dist_c = (x2**2 + y2**2)**0.5

                    if dist_c > 5:  # far from center
                        xc_vel = x2 / dist_c * self.enemy_speed
                        yc_vel = y2 / dist_c * self.enemy_speed
                        enemy.centerx = round(enemy.centerx + xc_vel)
                        enemy.centery = round(enemy.centery + yc_vel)
                    else:  # close enough, snap to center
                        enemy.centerx = center_x
                        enemy.centery = center_y
                else:
                    # --- Pause phase ---
                    pass  # do nothing, enemy stays in place



            dx = player.centerx - enemy.centerx
            dy = player.centery - enemy.centery
            dist = (dx ** 2 + dy ** 2) ** 0.5 + 0.1

            proj = {
                "rect": pygame.Rect(enemy.centerx, enemy.centery, 10, 10),
                "vx": dx / dist * 6,
                "vy": dy / dist * 6
            }

            for proj in self.projectiles[:]:
                proj["rect"].x += proj["vx"]
                proj["rect"].y += proj["vy"]
                pygame.draw.circle(win, RED, proj["rect"].center, 10)
                if not win.get_rect().colliderect(proj["rect"]):
                    self.projectiles.remove(proj)
            
            if not self.super_state:
                if not player_invincible:
                    for proj in self.projectiles[:]:
                        if player.colliderect(proj["rect"]):
                            if not player_invincible:
                                p -= 1  # reduce health
                                sound_hit.play()
                                player_invincible = True
                                invincible_timer = pygame.time.get_ticks()
                            # Remove or ignore this projectile after collision
                            self.projectiles.remove(proj)
                            break  # stop checking other projectiles this frame
            #Boss atack
            if shooting:
                self.boss_cooldown -= 1
                if self.boss_cooldown <= 0:
                    num_shots = 20
                    spread = 0.6  # radians
                    angle_to_player = math.atan2(dy, dx)
                    
                    # Randomly shift the center of the spread by up to 15 degrees
                    center_offset = random.uniform(-0.2, 0.2)  # ~±11.5 degrees
                    for i in range(num_shots):
                        angle = angle_to_player + (i - num_shots//2) * spread + center_offset
                        vx = math.cos(angle) * 6
                        vy = math.sin(angle) * 6
                        self.projectiles.append({
                            "rect": pygame.Rect(enemy.centerx, enemy.centery, 10, 10),
                            "vx": vx,
                            "vy": vy
                        })
                    self.boss_cooldown = 40

            if super and self.not_super:
                self.not_super = False
                super = False
                if self.rect_coords:  # Check if there are still available positions
                    random_rects = random.sample(self.rect_coords, 1)
                    rand_x, rand_y = random_rects[0]
                    x, y = rand_x, rand_y
                    rect = pygame.Rect(x, y, self.mushroom_radius * 2, self.mushroom_radius * 2)
                    self.super_m.append(rect)


            for m in self.super_m:
                pygame.draw.rect(win, BROWN, (m.centerx - 3, m.bottom - 10, 6, 10))  # stem
                pygame.draw.ellipse(win, GOLD, (m.x, m.y + 5, self.mushroom_radius * 2, self.mushroom_radius))  # cap
                    
            for m in self.super_m[:]:
                if player.colliderect(m):
                    self.super_m.remove(m)
                    sound_power.play()
                    self.super_state = True
                    self.super_timer = pygame.time.get_ticks()  # Start timer



            # Prevent mushrooms from going out of bounds (considering mushroom size)
            if enemy.left < 0:  # Left boundary
                enemy.left = 0
            elif enemy.right > win.get_width():  # Right boundary
                enemy.right = win.get_width()

            if enemy.top < 40:  # Upper boundary (prevent going above 40 pixels)
                enemy.top = 40
            elif enemy.bottom > win.get_height():  # Bottom boundary
                enemy.bottom = win.get_height()



            return enemy
        else:
            return None

    def Merchant(self):
        screen_center_x = WIDTH // 2 
        screen_center_y = HEIGHT // 2 - 175

        pygame.draw.ellipse(win, GOLD, (screen_center_x - 30, screen_center_y - 40, 60, 50))
        pygame.draw.circle(win, BROWN, (screen_center_x, screen_center_y), self.player_size // 2)
        pygame.draw.circle(win, BLACK, (screen_center_x - 10, screen_center_y - 10), 5)
        pygame.draw.circle(win, BLACK, (screen_center_x + 10, screen_center_y - 10), 5)
        pygame.draw.arc(win, BLACK, (screen_center_x - 10, screen_center_y - 5, 20, 15), 3.14, 0, 2)
        
    def Player(self):
        player = self.player
        player_size = self.player_size
        player_speed = self.player_speed
        self.skin_type = current_skin
        skins = self.Player_skin()
        self.Player_skin()

        # Drawing Player
        # Handle super state timeout (e.g., 10 seconds)
        if self.super_state and pygame.time.get_ticks() - self.super_timer > 10000:
            self.super_state = False

        # Drawing Player - use GOLD color if in super state
        current_color = GOLD if self.super_state else MODE
        pygame.draw.circle(win, current_color, player.center, self.player_size // 2)
        pygame.draw.circle(win, BLACK, (player.centerx - 10, player.centery - 10), 5)
        pygame.draw.circle(win, BLACK, (player.centerx + 10, player.centery - 10), 5)
        pygame.draw.arc(win, BLACK, (player.centerx - 10, player.centery - 5, 20, 15), 3.14, 0, 2)

        draw_func = skins.get(self.skin_type)
        if draw_func:
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
        keys = pygame.key.get_pressed()

        # Apply knockback
        if self.knockback.length_squared() > 0:
            self.player.x += self.knockback.x
            self.player.y += self.knockback.y

            # Decay knockback each frame (friction)
            self.knockback *= 0.8  
            if self.knockback.length() < 0.5:
                self.knockback = pygame.Vector2(0, 0)

        # Handle speed
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            if self.player_speed < self.max_speed:
                self.player_speed += self.acceleration_rate
                self.player_speed = min(self.player_speed, self.max_speed)
        else:
            self.player_speed = self.min_speed

        move_x, move_y = 0, 0
        if keys[pygame.K_LEFT]:  move_x -= 1
        if keys[pygame.K_RIGHT]: move_x += 1
        if keys[pygame.K_UP]:    move_y -= 1
        if keys[pygame.K_DOWN]:  move_y += 1

        if move_x != 0 and move_y != 0:
            length = math.sqrt(move_x ** 2 + move_y ** 2)
            move_x /= length
            move_y /= length

        # Predict player movement
        new_player_rect = self.player.copy()
        new_player_rect.x += move_x * self.player_speed
        new_player_rect.y += move_y * self.player_speed

        # --- ROCK COLLISION DETECTION (using chest approach) ---
        if self.with_rocks:
            for rock in self.rocks:
                if new_player_rect.colliderect(rock):
                    # Block movement if player would hit a rock
                    return

        # --- CHEST is always solid: cancel move if we would hit it
        if self.chest and new_player_rect.colliderect(self.chest):
            # blocked by chest
            return

        # --- FLOOD is solid: cancel move if we would hit a flood
        for flood in self.flood:
            if new_player_rect.colliderect(flood):  # If player collides with a flood rectangle
                # blocked by flood, do not allow movement
                return

        # --- KEY pushing (only if key exists)
        if self.key and new_player_rect.colliderect(self.key):
            new_key_rect = self.key.copy()
            new_key_rect.x += move_x * self.player_speed
            new_key_rect.y += move_y * self.player_speed

            # Check bounds
            within_bounds = (
                0 <= new_key_rect.x <= WIDTH - self.player_size and
                40 <= new_key_rect.y <= HEIGHT - self.player_size
            )

            # Also don't push key into other obstacles (like chest, rocks or spikes)
            collides_with_chest = (self.chest and new_key_rect.colliderect(self.chest))
            collides_with_rocks = False
            if self.with_rocks:
                for rock in self.rocks:
                    if new_key_rect.colliderect(rock):
                        collides_with_rocks = True
                        break

            if within_bounds and not collides_with_chest and not collides_with_rocks:
                # move both player and key
                self.key = new_key_rect
                self.player = new_player_rect
            else:
                # If the key WOULD land on the chest, we can make them vanish:
                if collides_with_chest:
                    sound_effect.play()
                    self.key = None
                    self.chest = None
                    # trigger mushroom release (when the chest is opened)
                    self.release_mushrooms()  # Call the method to release mushrooms
                    # move player into the spot (optional)
                    self.player = new_player_rect
                else:
                    # blocked: do nothing (player doesn't move)
                    return
        else:
            # No key collision: normal move allowed
            self.player = new_player_rect

        # Boundaries for player
        if self.player.x < 0:
            self.player.x = 0
        if self.player.x > WIDTH - self.player_size:
            self.player.x = WIDTH - self.player_size
        if self.player.y < 40:
            self.player.y = 40
        if self.player.y > HEIGHT - self.player_size:
            self.player.y = HEIGHT - self.player_size

        if keys[pygame.K_ESCAPE]:
            Menu()

    def Mushroom(self):
        """Main method to handle all mushroom-related elements."""
        self._handle_mushroom_spawning()
        self._draw_mushrooms()
        self._handle_spikes()
        self._handle_bad_mushrooms()

        if self.with_rocks:
            self.Rocks()
            
        self._draw_mushrooms()
        self._handle_spikes()
        self._handle_bad_mushrooms()

        return self.mushrooms, self.spike_rects, self.bad_mushrooms

    def _handle_mushroom_spawning(self):
        """Handle spawning of mushrooms based on level conditions."""
        mushroom_count = 20
        mushroom_time = pygame.time.get_ticks()

        if not self.with_chest and not self.with_enemy and self.mushrooms_spawned < mushroom_count:
            if self.sky_mushrooms:
                self._spawn_sky_mushrooms(mushroom_time)
            else:
                self._spawn_normal_mushrooms()

    def _spawn_sky_mushrooms(self, current_time):
        """Spawn mushrooms one by one with delay for sky mushrooms."""
        if len(self.mushrooms) == 0:
            self.last_spawn_time = current_time - self.spawn_interval
            
        if current_time - self.last_spawn_time >= self.spawn_interval:
            possible_y_coords = [50, 100, 150]
            if self.mushrooms_spawned < 20 and self.rect_coords:
                random_rects = random.sample(self.rect_coords, 1)
                rand_x, _ = random_rects[0]
                rand_y = random.choice(possible_y_coords)
                x, y = rand_x, rand_y
                rect = pygame.Rect(x, y, self.mushroom_radius * 2, self.mushroom_radius * 2)
                self.mushrooms.append(rect)
                self.mushrooms_spawned += 1
                try:
                    self.rect_coords.remove((rand_x, rand_y))
                except ValueError:
                    pass
                self.last_spawn_time = current_time

    def _spawn_normal_mushrooms(self):
        """Spawn all mushrooms at once for normal levels."""
        # Add a flag to track if initial mushrooms have been spawned
        if not hasattr(self, 'initial_mushrooms_spawned'):
            self.initial_mushrooms_spawned = False
        
        if not self.initial_mushrooms_spawned and len(self.mushrooms) == 0:
            # Calculate how many mushrooms we need to spawn (20 minus those in rocks)
            mushrooms_to_spawn = 20 - len(self.pre_spawned_mushrooms)
            
            for _ in range(mushrooms_to_spawn):
                if self.rect_coords:
                    # Get a position that's not occupied by a rock
                    valid_position = False
                    attempts = 0
                    max_attempts = 50  # Prevent infinite loop
                    
                    while not valid_position and self.rect_coords and attempts < max_attempts:
                        random_rects = random.sample(self.rect_coords, 1)
                        rand_x, rand_y = random_rects[0]
                        x, y = rand_x, rand_y
                        rect = pygame.Rect(x, y, self.mushroom_radius * 2, self.mushroom_radius * 2)
                        
                        # Check if this position overlaps with any rock
                        valid_position = True
                        for rock in self.rocks:
                            if rect.colliderect(rock):
                                valid_position = False
                                # Remove this coordinate if it conflicts with a rock
                                try:
                                    self.rect_coords.remove((rand_x, rand_y))
                                except ValueError:
                                    pass
                                break
                        
                        attempts += 1
                        
                        if valid_position:
                            self.mushrooms.append(rect)
                            try:
                                self.rect_coords.remove((rand_x, rand_y))
                            except ValueError:
                                pass
                            break
            
            # Mark that initial mushrooms have been spawned
            self.initial_mushrooms_spawned = True

    def _draw_mushrooms(self):
        """Draw and update mushroom positions."""
        for m in self.mushrooms:
            # Falling code for sky mushrooms
            if self.sky_mushrooms:
                m.y += 2
                if m.y > 600:
                    sound_hit.play()
                    Over(7)
                    
                    
            # Draw mushroom
            if self.vacuum:
                pygame.draw.rect(win, BROWN, (m.centerx - 3, m.bottom - 15, 6, 10))  # stem
                pygame.draw.ellipse(win, RED, (m.x, m.y, self.mushroom_radius * 2, self.mushroom_radius))  # cap
                pygame.draw.arc(win, GRAY2, (m.centerx - 10, m.centery - 26, 20, 20), 3.14, 0, 2)
            elif self.moving_mushrooms:
                pygame.draw.ellipse(win, RED, (m.x, m.y, self.mushroom_radius * 2, self.mushroom_radius))  # cap
                pygame.draw.rect(win, BROWN, (m.centerx - 7, m.bottom - 15, 6, 10))  # stem
                pygame.draw.rect(win, BROWN, (m.centerx + 1, m.bottom - 15, 6, 10))  # stem
                pygame.draw.rect(win, BROWN, (m.centerx - 12, m.bottom - 10, 6, 5))  # stem
                pygame.draw.rect(win, BROWN, (m.centerx + 6, m.bottom - 10, 6, 5))  # stem
            elif self.sky_mushrooms:
                pygame.draw.rect(win, BROWN, (m.centerx - 3, m.bottom - 10, 6, 10))  # stem
                pygame.draw.ellipse(win, RED, (m.x, m.y + 5, self.mushroom_radius * 2, self.mushroom_radius))  # cap
                pygame.draw.ellipse(win, (GOLD), (m.centerx - 12, m.centery - 24, 24, 10), 4)
            else:
                pygame.draw.rect(win, BROWN, (m.centerx - 3, m.bottom - 10, 6, 10))  # stem
                pygame.draw.ellipse(win, RED, (m.x, m.y + 5, self.mushroom_radius * 2, self.mushroom_radius))  # cap





            # Handle mushroom movement
            self._update_mushroom_movement(m)

    def _update_mushroom_movement(self, m):
        """Update mushroom position based on game mechanics."""
        # Calculate direction to move mushroom towards player
        x_dist = m.centerx - self.player.centerx
        y_dist = m.centery - self.player.centery
        dist = (x_dist ** 2 + y_dist ** 2) ** .5 + 1
        x_vel = x_dist / dist * 1
        y_vel = y_dist / dist * 1

        if self.vacuum:
            m.centerx -= x_vel
            m.centery -= y_vel

        if self.moving_mushrooms:
            # Update position
            m.centerx += x_vel
            m.centery += y_vel

            # Prevent mushrooms from going out of bounds
            if m.left < 0:
                m.left = 0
            elif m.right > win.get_width():
                m.right = win.get_width()

            if m.top < 40:
                m.top = 40
            elif m.bottom > win.get_height():
                m.bottom = win.get_height()

    def _handle_spikes(self):
        """Handle spike generation and drawing."""
        if self.with_spikes and not self.spikes_generated:
            self._generate_spikes()
            self.spikes_generated = True

        # Draw spikes
        for s in self.spike:
            pygame.draw.polygon(win, BLACK, s)

    def _generate_spikes(self):
        """Generate spike positions ensuring they don't overlap with other objects."""
        for _ in range(50):
            if self.rect_coords:
                random_rects = random.sample(self.rect_coords, 1)
                rand_x, rand_y = random_rects[0]
                x, y = rand_x, rand_y
                rect = pygame.Rect(x, y, self.mushroom_radius * 2, self.mushroom_radius * 2)
                self.rect_coords.remove((rand_x, rand_y))

                too_close = False

                # Check for overlap with mushrooms
                for m in self.mushrooms:
                    dist = math.sqrt((x - m.centerx) ** 2 + (y - m.centery) ** 2)
                    if dist < self.safe_distance:
                        too_close = True
                        break

                # Check for overlap with the player
                if not too_close:
                    px, py = self.player.center
                    dist_to_player = math.sqrt((x - px) ** 2 + (y - py) ** 2)
                    if dist_to_player < self.safe_distance:
                        too_close = True

                # If it's safe, create a spike
                if not too_close:
                    vertices = [
                        (x, y),  # Base point
                        (x - 10, y + 25),  # Left point
                        (x - 5, y + 15),   # Left middle
                        (x - 15, y + 30),  # Left outer
                        (x + 2, y + 20),   # Center middle
                        (x + 15, y + 30),  # Right outer
                        (x + 5, y + 15),   # Right middle
                        (x + 10, y + 25)   # Right point
                    ]
                    self.spike.append(vertices)
                    self.spike_rects.append(pygame.Rect(x - 15, y, 30, 30))

    def _handle_bad_mushrooms(self):
        """Handle bad mushroom generation and drawing."""
        if self.with_bad_mushrooms and not self.bad_mushrooms:
            self._generate_bad_mushrooms()
            self.spikes_generated = True

        # Draw bad mushrooms
        for b in self.bad_mushrooms:
            pygame.draw.rect(win, BROWN, (b.centerx - 3, b.bottom - 15, 6, 10))  # stem
            pygame.draw.ellipse(win, RED, (b.x, b.y, self.mushroom_radius * 2, self.mushroom_radius))  # cap
            pygame.draw.ellipse(win, BLACK, (b.x + 5, b.y + 3, self.mushroom_radius // 3, self.mushroom_radius // 3))
            pygame.draw.ellipse(win, BLACK, (b.x + 20, b.y + 3, self.mushroom_radius // 3, self.mushroom_radius // 3))

    def _generate_bad_mushrooms(self):
        """Generate bad mushroom positions ensuring they don't overlap with other objects."""
        for _ in range(20):
            while True:
                if self.rect_coords:
                    random_rects = random.sample(self.rect_coords, 1)
                    rand_x, rand_y = random_rects[0]
                    x, y = rand_x, rand_y
                    rect = pygame.Rect(x, y, self.mushroom_radius * 2, self.mushroom_radius * 2)
                    self.rect_coords.remove((rand_x, rand_y))

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
                    self.bad_mushrooms.append(pygame.Rect(x - 15, y, 30, 30))  # collision rect
                    break

    def Flood(self):
        """Generate flooding effect by spawning rectangles, checking overlap, and drawing them."""
        if self.with_flood:
            current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
            
            # Spawn flood effect every 500 ms
            if current_time - self.last_spawn_time >= 500:
                for _ in range(5):  # Spawn 5 floods at once
                    if self.rect_coords:  # Ensure there are available positions for the flood
                        random_rects = random.sample(self.rect_coords, 1)
                        rand_x, rand_y = random_rects[0]
                        x, y = rand_x, rand_y
                        rect = pygame.Rect(x, y, self.mushroom_radius * 2, self.mushroom_radius * 2)
                        self.rect_coords.remove((rand_x, rand_y))  # Remove this coordinate to avoid overlap

                        too_close = False

                        # Check for overlap with mushrooms
                        for m in self.mushrooms:
                            dist = math.sqrt((x - m.centerx) ** 2 + (y - m.centery) ** 2)
                            if dist < self.safe_distance:
                                too_close = True
                                break

                        # Check for overlap with the player
                        if not too_close:
                            px, py = self.player.center
                            dist_to_player = math.sqrt((x - px) ** 2 + (y - py) ** 2)
                            if dist_to_player < self.safe_distance:
                                too_close = True

                        # If it's safe, create a flood rectangle and add to the list
                        if not too_close:
                            flood_rect = pygame.Rect(x - 15, y, 30, 10)  # Adjust size for flood
                            self.flood.append(flood_rect)  # Add the flood rectangle to the list
                self.last_spawn_time = current_time  # Update spawn time after flood generation

            # Draw floods (rectangles)
            for f in self.flood:
                pygame.draw.rect(win, BLUE, (f.centerx - 20, f.centery - 20, 40, 40))  # Draw each flood as a blue rectangle

    def release_mushrooms(self):
        """This method releases mushrooms inside the chest when the key and chest collide."""
        if self.with_chest:  # Release mushrooms only if there is a chest
            for _ in range(20):  # Release 5 mushrooms for example
                if self.rect_coords:
                    rand_pos = random.choice(self.rect_coords)  # Get a random empty position
                    new_mushroom = pygame.Rect(rand_pos[0], rand_pos[1], self.mushroom_radius * 2, self.mushroom_radius * 2)
                    self.mushrooms.append(new_mushroom)  # Add it to the list of mushrooms
                    self.rect_coords.remove(rand_pos)  # Remove the position from available coordinates
  
    def handle_mushroom_collection(self, player):
        for m in self.mushrooms[:]:  # Iterating over a copy of the list
            if player.colliderect(m):
                self.mushrooms.remove(m)
                return True  # Or update score, collected, etc. here
        return False


def draw_hud(win, font, level_num, score, collected, config, player_health=3, boss_health=3):
    TEXT_COLOR = (255, 255, 255)
    LINE_COLOR = (0, 0, 0)

    pygame.draw.rect(win, LINE_COLOR, (0, 0, WIDTH, 40))
    with_enemy = config.get("with_enemy", False)

    if with_enemy:
        # Text
        level_text = font.render(f"{t("hud_boss_player")}", True, TEXT_COLOR)
        collected_text = font.render(f"{t("hud_boss_boss")}: ", True, TEXT_COLOR)
        boss_text_width = collected_text.get_width() - 70
        win.blit(level_text, (20, 10))
        win.blit(collected_text, (615 - boss_text_width, 10))
        

        # Player hearts
        player_text_width = level_text.get_width()
        heart_start_x = 20 + player_text_width + 20  # 10px padding after text
        for i in range(player_health):
            pygame.draw.circle(win, RED, (heart_start_x + i*35, 20), 15)

        # Boss hearts
        for i in range(boss_health):
            pygame.draw.circle(win, RED, (700 + i*35, 20), 15)

    else:
        # Normal HUD layout
        level_text = font.render(f"{t('hud_level')}: {level_num}", True, TEXT_COLOR)
        goal_text = font.render(f"{t('hud_goal')}: {score}/20", True, TEXT_COLOR)
        collected_text = font.render(f"{t('hud_collected')}: {score}/20", True, TEXT_COLOR)
        
        # Left-aligned level text
        win.blit(level_text, (20, 10))
        
        # Perfectly centered goal text
        #goal_x = WIDTH // 2 - goal_text.get_width() // 2
        #win.blit(goal_text, (goal_x, 10))
        
        # Right-aligned collected text (with 20px right margin)
        collected_x = WIDTH - collected_text.get_width() - 20
        win.blit(collected_text, (collected_x, 10))


def Game(level_num, skip_cutscene=False):
    Cutscene.needs_reset = True
    if level_num != 10:
        if not skip_cutscene:
            Cutscene(level_num)
    config = LEVELS[level_num]
    assets = Assets(config)
    running = True
    score = 0
    global p
    global e 
    e_damaged = False
    damage_timer = 0

    player_invincible = False
    invincible_timer = 0
    INVINCIBLE_TIME = 200  # milliseconds (1 second of invincibility)

    font = pygame.font.Font(None, 36)
    # Flag to track if level_goal has been set
    level_goal_set = False
    level_goal = 0  # Initialize level_goal, but don't set it yet
    global mushroom_inventory
    collected = mushroom_inventory

    # Colors
    TEXT_COLOR = (255, 255, 255)  # White text
    LINE_COLOR = (0, 0, 0)  # Black background for top line

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        win.fill(assets.level_color)  # Fill the screen with level background color
        flood = assets.Flood()
        player = assets.Player()
        control = assets.Control()
        mushrooms, spikes, bad_mushrooms = assets.Mushroom()  # Now always two lists
        enemy = assets.Enemy()


        # Safely handle key and chest (may be None)
        key = assets.Key()  # Will be None if with_chest == False
        chest = assets.Chest()  # Will be None if with_chest == False

        if not level_goal_set:
            level_goal = len(mushrooms)  # Set level_goal once when the level starts
            level_goal_set = True  # Set the flag to True, preventing further updates


        rocks = assets.Rocks() 

        # Mushroom collision
        if assets.handle_mushroom_collection(player):
            score += 1
            collected += 1
            sound_effect.play()
            

        for b in bad_mushrooms[:]:
            if player.colliderect(b):
                running = False
                sound_hit.play()
                Over(level_num)

        # Spike collision
        for rect in spikes:
            if player.colliderect(rect):
                running = False
                sound_hit.play()
                Over(level_num)

        

        if (pygame.time.get_ticks() - damage_timer) > 500:
            assets.enemy_speed = 8
            

        if enemy and player.colliderect(enemy):
            if assets.super_state:
                e -= 1
                sound_hit.play()
                assets.enemy_speed = -16
                damage_timer = pygame.time.get_ticks()
                assets.super_state = False
                
                # --- Push both away from each other ---
                dx = enemy.centerx - player.centerx
                dy = enemy.centery - player.centery
                dist = math.hypot(dx, dy) or 1  # avoid division by zero
                push_distance = 50  # how far to push

                # normalize vector
                nx, ny = dx / dist, dy / dist

                # push enemy
                enemy.centerx += int(nx * push_distance)
                enemy.centery += int(ny * push_distance)

                assets.knockback = pygame.Vector2(-nx * 10, -ny * 10)  # adjust strength

                # clamp to screen
                assets.player.clamp_ip(win.get_rect())
                enemy.clamp_ip(win.get_rect())
            elif not assets.super_state and not player_invincible:
                p -= 1
                sound_hit.play()

                assets.enemy_speed = -12
                damage_timer = pygame.time.get_ticks()
                assets.super_state = False
                
                # --- Push both away from each other ---
                dx = enemy.centerx - player.centerx
                dy = enemy.centery - player.centery
                dist = math.hypot(dx, dy) or 1  # avoid division by zero
                push_distance = 50  # how far to push

                # normalize vector
                nx, ny = dx / dist, dy / dist

                # push enemy
                enemy.centerx += int(nx * push_distance)
                enemy.centery += int(ny * push_distance)

                assets.knockback = pygame.Vector2(-nx * 10, -ny * 10)  # adjust strength

                player_invincible = True
                invincible_timer = pygame.time.get_ticks()

        if (invincible_timer - pygame.time.get_ticks()):
            pass

        
        if p <= 0:
            #pass
            Over(9)

        if e <= 0:
            #pass
            Victory()

        # Check for key and chest collision only if both exist
        if assets.key and assets.chest:  # Check if both key and chest exist
            if key.colliderect(chest):
                assets.key = None
                assets.chest = None

        if (pygame.time.get_ticks()- invincible_timer) > INVINCIBLE_TIME:
            player_invincible = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:
            running = False
            Over(level_num)



        # Level complete check
        #if len(mushrooms) == 0:
        if score == 20:
            mushroom_inventory = collected
            if not Levels_completed.get(level_num, {}).get("completed", False):
                Levels_completed[level_num] = {"completed": True}
                running = False
                
                if level_num in (1,3,5,8,9,10):
                    # For level 1, skip skin unlock, just go to next level or victory
                    if level_num == 9:
                        Victory()
                    elif level_num == 10:
                        Chapter_Victory()
                    else:
                        Next_level(level_num)
                else:
                    # Unlock the skin for this level before showing New_skin screen
                    My_skins[level_num]["unlocked"] = True
                    New_skin(level_num, level_num)
            elif level_num == max_level:
                running = False
                Victory()
            else:
                Next_level(level_num)

        draw_hud(win, font, level_num, score, collected, config, p, e)

        pygame.display.flip()
        clock.tick(60)


def handle_shop_exit(return_to_level):
    """Handle exiting the shop and returning to appropriate screen"""
    if return_to_level >= max_level:
        Victory()
    else:
        Game(return_to_level + 1)

def Shop(return_to_level):
    global mushroom_inventory, My_skins, current_skin
    running = True
    assets = Assets(LEVELS[1])
    
    # Colors
    STALL_COLOR = (139, 69, 19)  # Rich wood brown
    COUNTER_COLOR = (101, 67, 33)  # Darker wood
    PANEL_COLOR = (0, 0, 0, 180)  # Semi-transparent black
    BORDER_COLOR = (160, 82, 45, 220)  # Lighter wood border

    purchasable = [sid for sid, data in My_skins.items() if not data["unlocked"]]
    if not purchasable:
        handle_shop_exit(return_to_level)
        return

    skin_id = purchasable[0]
    skin_name = My_skins[skin_id]["skin"]
    cost = 50

    # Create styled buttons
    buy_button = Button(
        f"{t('shop_buy')} ({cost})", 
        WIDTH//2 - 300, HEIGHT-100, 
        250, 60, 
        STALL_COLOR,
        text_color=WHITE
    )
    skip_button = Button(
        t("shop_skip"), 
        WIDTH//2 + 50, HEIGHT-100, 
        250, 60, 
        STALL_COLOR,
        text_color=WHITE
    )

    def draw_merchant_stall():
        # Stall base (3 posts with roof)
        pygame.draw.rect(win, STALL_COLOR, (WIDTH//2-200, HEIGHT//2-50, 400, 20))  # Roof
        pygame.draw.polygon(win, STALL_COLOR, [
            (WIDTH//2-200, HEIGHT//2-50),
            (WIDTH//2, HEIGHT//2-120),
            (WIDTH//2+200, HEIGHT//2-50)
        ])
        
        # Stall counter
        pygame.draw.rect(win, COUNTER_COLOR, (WIDTH//2-180, HEIGHT//2-30, 360, 30))
        pygame.draw.rect(win, BORDER_COLOR, (WIDTH//2-180, HEIGHT//2-30, 360, 30), 3)
        
        # Stall posts
        for x in [WIDTH//2-175, WIDTH//2+175]:
            pygame.draw.rect(win, STALL_COLOR, (x-5, HEIGHT//2, 10, 100))
        pygame.draw.rect(win, GRAY2, (x - 350, HEIGHT//2 + 0, 350, 100))
        pygame.draw.rect(win, STALL_COLOR, (x - 350, HEIGHT//2 + 95, 350, 5))


        # Draw merchant behind counter
        assets.player.center = (WIDTH//2, HEIGHT//2 + 20)
        assets.Merchant()


    def draw_current_mushrooms():
        text = font_medium.render(f"{t("shop_current_mushrooms")}: {mushroom_inventory}", True, WHITE)
        pygame.draw.rect(win, PANEL_COLOR, (20, 20, text.get_width()+20, text.get_height()+10), border_radius=5)
        pygame.draw.rect(win, BORDER_COLOR, (20, 20, text.get_width()+20, text.get_height()+10), 2, border_radius=5)
        win.blit(text, (30, 25))

    while running:
        # Draw scene
        draw_forest_gradient(win, FOREST_GRADIENT)
        draw_merchant_stall()
        #draw_skin_display()
        draw_current_mushrooms()
        
        # Draw skin preview
        current_skin_backup = current_skin
        current_skin = skin_name
        assets.player.center = (WIDTH//2, HEIGHT//2 + 50)
        assets.Player()
        current_skin = current_skin_backup
        
        # Draw buttons
        buy_button.draw(win)
        skip_button.draw(win)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buy_button.is_clicked(event.pos) and mushroom_inventory >= cost:
                    mushroom_inventory -= cost
                    My_skins[skin_id]["unlocked"] = True
                    running = False
                    New_skin(skin_id, return_to_level)
                elif skip_button.is_clicked(event.pos):
                    handle_shop_exit(return_to_level)

        pygame.display.flip()
        clock.tick(60)


def New_skin(skin_id, return_to_level):
    global current_skin, My_skins
    assets = Assets(LEVELS[1])
    previous_skin = current_skin
    new_skin_name = My_skins[skin_id]["skin"]

    def equip_action():
        global current_skin
        current_skin = new_skin_name
        exit_to_next()

    def collect_action():
        global current_skin
        current_skin = previous_skin
        exit_to_next()

    def exit_to_next():
        if return_to_level >= max_level:
            Victory()
        else:
            Game(return_to_level + 1)

    # Create styled buttons
    equip_button = Button(
        t("new_skin_equip"), 
        WIDTH//2 - 320, HEIGHT//2 + 150, 
        250, 60, 
        (139, 69, 19),  # Brown
        equip_action,
        (255, 255, 255)  # White text
    )
    
    collect_button = Button(
        t("new_skin_collect"),
        WIDTH//2 + 70, HEIGHT//2 + 150,
        250, 60,
        (139, 69, 19),
        collect_action,
        (255, 255, 255)
    )

    # Custom drawing for skin preview
    def draw_skin_preview():
        # Title text
        title = font_large.render(f"{t('new_skin_unlock')}!", True, BLACK)
        win.blit(title, (WIDTH//2 - title.get_width()//2, 80))
        
        # Skin name

        


    # Create menu instance
    skin_menu = BaseMenu(
        win,
        font_medium,
        font_large,
        "",  # Empty title since we're drawing custom
        [equip_button, collect_button],
        use_gradient=True,
        extra_draw=draw_skin_preview
    )

    # Main loop with keyboard support
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Handle mouse events
            skin_menu.handle_events(event)
            
            # Keyboard support
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Equip
                    equip_action()
                    running = False
                elif event.key == pygame.K_2:  # Collect
                    collect_action()
                    running = False
                elif event.key == pygame.K_ESCAPE:  # Default to collect
                    collect_action()
                    running = False
        
        # Draw everything
        skin_menu.draw()
        
        # Draw skin preview
        current_skin_backup = current_skin
        current_skin = new_skin_name
        assets.player.center = (WIDTH//2, HEIGHT//2)
        assets.Player()
        current_skin = current_skin_backup
        
        pygame.display.flip()
        clock.tick(60)


def Next_level(current_level):
    global mushroom_inventory
    
    def continue_action():
        if current_level >= 3 and mushroom_inventory >= 50:
            Shop(current_level)
        elif current_level == max_level:
            Victory()
        else:
            Game(current_level + 1)
    
    def menu_action():
        Menu()

    # Create buttons
    continue_button = Button(
        t("next_level_continue"), 
        WIDTH//2 - 100, HEIGHT//2 - 30, 
        200, 60, 
        (139, 69, 19),  # Brown
        continue_action,
        (255, 255, 255)  # White text
    )
    
    menu_button = Button(
        t("next_level_menu"),
        WIDTH//2 - 100, HEIGHT//2 + 170,
        200, 60,
        (139, 69, 19),
        menu_action,
        (255, 255, 255)
    )

    # Custom drawing for level complete screen
    def draw_level_complete():
        # Simple black title
        title = font_large.render(t("next_level_complete"), True, BLACK)
        win.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 200))
        

    # Create menu instance
    level_complete_menu = BaseMenu(
        win,
        font_medium,
        font_large,
        "",  # Empty title since we're drawing custom
        [continue_button, menu_button],
        use_gradient=True,
        extra_draw=draw_level_complete
    )

    # Main loop with keyboard support
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Handle mouse events
            level_complete_menu.handle_events(event)
            
            # Keyboard support
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    continue_action()
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    menu_action()
                    running = False
        
        # Draw everything
        level_complete_menu.draw()
        pygame.display.flip()
        clock.tick(60)
    
 
def Over(current_level):
    global p
    global e

    p = 3
    e = 3
    def retry_action():
        Game(current_level, skip_cutscene=True)
    
    def menu_action():
        Menu()

    # Create buttons
    retry_button = Button(
        t("over_again"), 
        WIDTH//2 - 100, HEIGHT//2 - 30, 
        200, 60, 
        (139, 69, 19),  # Brown
        retry_action,
        (255, 255, 255)  # White text
    )
    
    menu_button = Button(
        t("over_menu"),
        WIDTH//2 - 100, HEIGHT//2 + 170,
        200, 60,
        (139, 69, 19),
        menu_action,
        (255, 255, 255)
    )

    # Custom drawing for game over screen
    def draw_game_over():
        # Simple black title centered
        title = font_large.render(t("over_over"), True, BLACK)
        win.blit(title, (WIDTH//2 - title.get_width()//2 - 0, HEIGHT//2 - 200))
        


    # Create menu instance
    game_over_menu = BaseMenu(
        win,
        font_medium,
        font_large,
        "",  # Empty title since we're drawing custom
        [retry_button, menu_button],
        use_gradient=True,
        extra_draw=draw_game_over
    )

    # Main loop with keyboard support
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Handle mouse events
            game_over_menu.handle_events(event)
            
            # Keyboard support
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    retry_action()
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    menu_action()
                    running = False
                elif event.key == pygame.K_m:  # Alternate key for menu
                    menu_action()
                    running = False
        
        # Draw everything
        game_over_menu.draw()
        pygame.display.flip()
        clock.tick(60)           


class Button:
    def __init__(self, text, x, y, width, height, color=GRAY, action=None, text_color=BLACK):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.action = action
        self.text_color = text_color
        
    def draw(self, screen):
        # Draw button background & border
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        # Start with a base font size
        font_size = 40
        font = pygame.font.SysFont("arial", font_size)
        text_surface = font.render(self.text, True, self.text_color)

        # Scale down until it fits with padding
        while text_surface.get_width() > self.rect.width - 10 and font_size > 5:
            font_size -= 1
            font = pygame.font.SysFont("arial", font_size)
            text_surface = font.render(self.text, True, self.text_color)

        # Center text in button
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def draw_forest_gradient(surface, gradient_colors, rect=None):
    """Draw a vertical forest gradient background"""
    if rect is None:
        rect = surface.get_rect()
    
    height = rect.height
    segment_height = height // (len(gradient_colors) - 1)
    
    for i, color in enumerate(gradient_colors):
        # Calculate y positions for each gradient segment
        y_start = i * segment_height
        y_end = (i + 1) * segment_height
        
        # For the last color, extend to bottom of screen
        if i == len(gradient_colors) - 1:
            y_end = height
        
        pygame.draw.rect(surface, color, (rect.x, y_start, rect.width, y_end - y_start))


class BaseMenu:
    def __init__(self, screen, font_medium, font_large, title_text, buttons,
                 background_color=None, extra_draw=None, use_gradient=True,
                 gradient_colors=None):
        """
        Initialize a menu with consistent styling
        
        Parameters:
        - screen: The pygame surface to draw on
        - font_medium: Medium font for buttons
        - font_large: Large font for title
        - title_text: Text to display (empty string for no title)
        - buttons: List of Button objects
        - background_color: Solid color if not using gradient
        - extra_draw: Function for additional drawing
        - use_gradient: Whether to use gradient background
        - gradient_colors: Custom gradient colors if needed
        """
        self.screen = screen
        self.font_medium = font_medium
        self.font_large = font_large
        self.title_text = title_text
        self.buttons = buttons
        self.background_color = background_color
        self.extra_draw = extra_draw
        self.use_gradient = use_gradient
        self.gradient_colors = gradient_colors or FOREST_GRADIENT

    def draw(self):
        """Draw the menu with all elements"""
        # Draw background
        if self.use_gradient:
            draw_forest_gradient(self.screen, self.gradient_colors)
        elif self.background_color:
            self.screen.fill(self.background_color)
        
        # Draw additional decorations if provided
        if self.extra_draw:
            self.extra_draw()
        
        # Draw all buttons
        for button in self.buttons:
            button.draw(self.screen)
        
        # Draw title only if text was provided
        if self.title_text:
            self._draw_title()

    def _draw_title(self):
        """Internal method to draw the title with styling"""
        # Create text surface
        title_font = pygame.font.SysFont("Arial", 72, bold=True)
        title = title_font.render(self.title_text, True, (255, 255, 255))  # White
        
        # Create background panel
        panel_width = title.get_width() + 40
        panel_height = title.get_height() + 20
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        
        # Draw panel with styled border
        pygame.draw.rect(panel, (0, 0, 0, 180), (0, 0, panel_width, panel_height), 
                        border_radius=10)
        pygame.draw.rect(panel, (139, 69, 19, 220), (0, 0, panel_width, panel_height), 
                        width=3, border_radius=10)
        
        # Position and draw elements
        panel_rect = panel.get_rect(center=(WIDTH//2, 100))
        title_rect = title.get_rect(center=panel_rect.center)
        
        self.screen.blit(panel, panel_rect)
        self.screen.blit(title, title_rect)

    def handle_events(self, event):
        """Handle menu events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for button in self.buttons:
                if button.is_clicked(mouse_pos):
                    button.action()

    def run(self):
        """Run the menu loop"""
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_events(event)

            self.draw()
            pygame.display.flip()
            clock.tick(60)

def Menu():
    global p
    global e
    p = 3
    e = 3
    def play_action():
        ChapterMenu()  
    def quit_action():
        pygame.quit()
        sys.exit()
    def level_action():
        Level_select()
    def skin_action():
        Skin_menu()

    # Create buttons with more forest-appropriate colors
    button_color = (139, 69, 19)  # Brown color for buttons
    text_color = (255, 255, 255)  # White text
    
    play_button = Button(t("menu_play"), WIDTH//2-100, HEIGHT//2-100, 200, 60, button_color, play_action, text_color)
    level_button = Button(t("menu_levels"), WIDTH//2-100, HEIGHT//2, 200, 60, button_color, level_action, text_color)
    skin_button = Button(t("menu_skins"), WIDTH//2-100, HEIGHT//2+100, 200, 60, button_color, skin_action, text_color)
    quit_button = Button(t("menu_quit"), WIDTH//2-100, HEIGHT//2+200, 200, 60, button_color, quit_action, text_color)

    # Add some decorative elements function
    def draw_forest_decorations():
        # Draw some simple trees in the background
        tree_color = (101, 67, 33)  # Brown trunk
        leaf_color = (34, 139, 34)  # Green leaves
        
        # Left side trees
        pygame.draw.rect(win, tree_color, (50, 300, 20, 100))  # Trunk
        pygame.draw.polygon(win, leaf_color, [
            (30, 300), (90, 300), (60, 250)
        ])
        
        # Right side trees
        pygame.draw.rect(win, tree_color, (730, 400, 20, 100))
        pygame.draw.polygon(win, leaf_color, [
            (710, 400), (770, 400), (740, 350)
        ])

        


    # Create menu with gradient and decorations
    menu = BaseMenu(
        win, 
        font_medium, 
        font_large, 
        "Mushroom Collector", 
        [play_button, level_button, skin_button, quit_button],
        use_gradient=True,
        extra_draw=draw_forest_decorations
    )
    menu.run()

def ChapterMenu():
    """Display a chapter selection menu"""
    def chapter1_action():
        Game(1)
    
    def chapter2_action():
        Game(10)

    def back_action():
        Menu()  # Return to main menu
    
    # Forest-themed colors
    button_color = (139, 69, 19)  # Brown
    text_color = (255, 255, 255)  # White
    
    # Create buttons for chapters (you can add more as needed)
    chapter1_button = Button(t("chapter_1"), WIDTH//2-100, HEIGHT//2-100, 200, 60, 
                            button_color, chapter1_action, text_color)
    chapter2_button = Button(t("chapter_2"), WIDTH//2-100, HEIGHT//2-0, 200, 60, 
                        button_color, chapter2_action, text_color)
    back_button = Button(t("chapter_back"), WIDTH//2-100, HEIGHT//2+100, 200, 60, 
                        button_color, back_action, text_color)
    

    
    # Create menu with gradient and decorations
    chapter_menu = BaseMenu(
        win, 
        font_medium, 
        font_large, 
        t("chapter_select"), 
        [chapter1_button, chapter2_button, back_button],
        use_gradient=True,
    )
    chapter_menu.run()

def Skin_menu():
    global current_skin

    def find_current_pos(skin, skins):
        for k, v in skins.items():
            if v["skin"] == skin:
                return k
        return 1

    def get_next_pos(pos, skins, forward=True):
        while True:
            pos = pos + 1 if forward else pos - 1
            if pos > len(skins):
                pos = 1
            if pos < 1:
                pos = len(skins)
            if skins[pos]["unlocked"]:
                return pos

    pos = find_current_pos(current_skin, My_skins)
    assets = Assets(LEVELS[1])

    def previous_skin_action():
        nonlocal pos
        pos = get_next_pos(pos, My_skins, forward=False)

    def next_skin_action():
        nonlocal pos
        pos = get_next_pos(pos, My_skins, forward=True)

    def back_action():
        Menu()

    prev_button = Button(t("skin_menu_prev"), WIDTH // 2 - 350, HEIGHT // 2 + 150, 150, 100, GRAY, previous_skin_action)
    next_button = Button(t("skin_menu_next"), WIDTH // 2 + 200, HEIGHT // 2 + 150, 150, 100, GRAY, next_skin_action)
    back_button = Button(t("skin_menu_menu"), WIDTH // 2 - 75, HEIGHT // 2 + 150, 150, 100, GRAY, back_action)

    def draw_preview():
        global current_skin
        if My_skins[pos]["unlocked"]:
            current_skin = My_skins[pos]["skin"]
        else:
            current_skin = "none"

        assets.player.x = WIDTH // 2 - assets.player_size // 2
        assets.player.y = HEIGHT // 2 - assets.player_size // 2
        assets.Player()

    skin_menu = BaseMenu(
        win, font_medium, font_large, "Select your skin",
        [prev_button, next_button, back_button],
        background_color=GREEN,
        extra_draw=draw_preview
    )
    skin_menu.run()


def Level_select():
    def level_action(num):
        Game(num)

    def back_action():
        Menu()

    def show_page(page):
        """Update menu buttons based on page number."""
        buttons.clear()
        if page == 1:
            buttons.extend([
                Button(t("level_select_1"), WIDTH//2-100, HEIGHT//2-270, 200, 60, button_color, lambda: level_action(1), text_color),
                Button(t("level_select_2"), WIDTH//2-100, HEIGHT//2-160, 200, 60, button_color, lambda: level_action(2), text_color),
                Button(t("level_select_3"), WIDTH//2-100, HEIGHT//2-60, 200, 60, button_color, lambda: level_action(3), text_color),
                Button(t("level_select_4"), WIDTH//2-100, HEIGHT//2+40, 200, 60, button_color, lambda: level_action(4), text_color),
                Button(t("level_next_button"), WIDTH//2-100, HEIGHT//2+130, 200, 60, button_color, lambda: show_page(2), text_color),
                Button(t("level_back_button"), WIDTH//2-100, HEIGHT//2+220, 200, 60, button_color, back_action, text_color)
            ])
        elif page == 2:
            buttons.extend([
                Button(t("level_select_5"), WIDTH//2-100, HEIGHT//2-270, 200, 60, button_color, lambda: level_action(5), text_color),
                Button(t("level_select_6"), WIDTH//2-100, HEIGHT//2-160, 200, 60, button_color, lambda: level_action(6), text_color),
                Button(t("level_select_7"), WIDTH//2-100, HEIGHT//2-60, 200, 60, button_color, lambda: level_action(7), text_color),
                Button(t("level_select_8"), WIDTH//2-100, HEIGHT//2+40, 200, 60, button_color, lambda: level_action(8), text_color),
                Button(t("level_select_9"), WIDTH//2-100, HEIGHT//2+130, 200, 60, button_color, lambda: level_action(9), text_color),
                Button(t("level_back_button"), WIDTH//2-100, HEIGHT//2+220, 200, 60, button_color, lambda: show_page(1), text_color)
            ])

    # Forest-themed colors
    button_color = (139, 69, 19)
    text_color = (255, 255, 255)
    buttons = []

    # Create initial menu
    show_page(1)

    # Menu object (uses dynamic `buttons` list)
    level_menu = BaseMenu(
        win,
        font_medium,
        font_large,
        "",
        buttons,
        use_gradient=True
    )

    # Keyboard mapping
    key_mapping = {
        pygame.K_1: 1,
        pygame.K_2: 2,
        pygame.K_3: 3,
        pygame.K_4: 4,
        pygame.K_5: 5,
        pygame.K_6: 6,
        pygame.K_7: 7,
        pygame.K_8: 8,
        pygame.K_9: 9,
    }

    # Main loop
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle mouse clicks
            level_menu.handle_events(event)

            # Handle keyboard
            if event.type == pygame.KEYDOWN:
                if event.key in key_mapping:
                    level_action(key_mapping[event.key])
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    back_action()
                    running = False

        level_menu.draw()
        pygame.display.flip()
        clock.tick(60)


def Victory():
    global p
    global e
    p = 3
    e = 3
    def play_again_action():
        Game(10)
    
    def quit_action():
        pygame.quit()
        sys.exit()

    # Create buttons with consistent styling
    play_button = Button(
        t("victory_play"), 
        WIDTH//2 - 100, HEIGHT//2 - 30, 
        200, 60, 
        (139, 69, 19),  # Brown
        play_again_action,
        (255, 255, 255)  # White text
    )
    
    quit_button = Button(
        t("victory_quit"),
        WIDTH//2 - 100, HEIGHT//2 + 170,
        200, 60,
        (139, 69, 19),
        quit_action,
        (255, 255, 255)
    )

    # Custom drawing for victory screen
    def draw_victory():
        # Title text
        title = font_large.render(t("victory_won"), True, BLACK)
        win.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        


    # Create menu instance
    victory_menu = BaseMenu(
        win,
        font_medium,
        font_large,
        "",  # Empty title since we're drawing custom
        [play_button, quit_button],
        use_gradient=True,
        extra_draw=draw_victory
    )

    # Main loop with keyboard support
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_action()
            
            # Handle mouse events
            victory_menu.handle_events(event)
            
            # Keyboard support
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play_again_action()
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    quit_action()
                elif event.key == pygame.K_RETURN:
                    play_again_action()
                    running = False
        
        # Draw everything
        victory_menu.draw()
        pygame.display.flip()
        clock.tick(60)

def Chapter_Victory():
    global p
    global e
    p = 3
    e = 3
    def play_again_action():
        Game(10)
    
    def quit_action():
        pygame.quit()
        sys.exit()

    # Create buttons with consistent styling
    play_button = Button(
        t("victory_play"), 
        WIDTH//2 - 100, HEIGHT//2 - 30, 
        200, 60, 
        (139, 69, 19),  # Brown
        play_again_action,
        (255, 255, 255)  # White text
    )
    
    quit_button = Button(
        t("victory_quit"),
        WIDTH//2 - 100, HEIGHT//2 + 170,
        200, 60,
        (139, 69, 19),
        quit_action,
        (255, 255, 255)
    )

    # Custom drawing for victory screen
    def draw_victory():
        # Title text
        title = font_large.render(t("victory_won2"), True, BLACK)
        win.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        


    # Create menu instance
    victory_menu = BaseMenu(
        win,
        font_medium,
        font_large,
        "",  # Empty title since we're drawing custom
        [play_button, quit_button],
        use_gradient=True,
        extra_draw=draw_victory
    )

    # Main loop with keyboard support
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_action()
            
            # Handle mouse events
            victory_menu.handle_events(event)
            
            # Keyboard support
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play_again_action()
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    quit_action()
                elif event.key == pygame.K_RETURN:
                    play_again_action()
                    running = False
        
        # Draw everything
        victory_menu.draw()
        pygame.display.flip()
        clock.tick(60)

def get_enemy_dialogue():
    return {
        "with_spikes": [
            t("dialogue_3_1"),
            t("dialogue_3_2")
        ],
        "with_bad_mushrooms": [
            t("dialogue_2_1"),
            t("dialogue_2_2")
        ],
        "with_chest": [
            t("dialogue_4_1"),
            t("dialogue_4_2"),
        ],
        "vacuum": [
            t("dialogue_5_1"),
            t("dialogue_5_2")
        ],
        "moving_mushrooms": [
            t("dialogue_6_1"),
        ],
        "sky_mushrooms": [
            t("dialogue_7_1"),
            t("dialogue_7_2")
        ],
        "with_flood": [
            t("dialogue_8_1"),
            t("dialogue_8_2")
        ],
        "with_enemy": [
            t("dialogue_9_1"),
            t("dialogue_9_2"),
            t("dialogue_9_3"),
            t("dialogue_9_4"),
            t("dialogue_9_5"),
        ]
    }



def draw_enemy_demo(win, x=100, y=250):
    """Draw a simplified enemy mushroom boss for cutscenes"""
    enemy_size = 40
    enemy = pygame.Rect(x - enemy_size//2, y - enemy_size//2, enemy_size, enemy_size)  # Use x and y parameters

    pygame.draw.ellipse(win, RED, (x - 30, y - 40, 60, 50))  # Use x and y
    pygame.draw.circle(win, ORANGE, (x, y), enemy_size // 2)  # Center at x,y

    pygame.draw.circle(win, GOLD, (x - 22, y - 18), 6)  # mushroom spot
    pygame.draw.circle(win, GOLD, (x + 24, y - 12), 5)  # mushroom spot
    pygame.draw.circle(win, GOLD, (x - 14, y - 32), 4)  # mushroom spot
    pygame.draw.circle(win, GOLD, (x - 4, y - 26), 5)  # mushroom spot
    pygame.draw.circle(win, GOLD, (x + 13, y - 28), 6)  # mushroom spot
    
    pygame.draw.circle(win, BLACK, (x - 10, y - 10), 5)  # eye
    pygame.draw.circle(win, BLACK, (x + 10, y - 10), 5)  # eye
    pygame.draw.arc(win, BLACK, (x - 10, y + 0, 20, 15), 0, 3.14, 2)  # mouth

def draw_player_demo(win, x=400, y=300):
    """Draw a simplified enemy mushroom boss for cutscenes"""
    
    player_size = 40
    player = pygame.Rect(x, y, player_size, player_size)

    pygame.draw.circle(win, WHITE, player.center, player_size // 2)
    pygame.draw.circle(win, BLACK, (player.centerx - 10, player.centery - 10), 5)
    pygame.draw.circle(win, BLACK, (player.centerx + 10, player.centery - 10), 5)
    pygame.draw.arc(win, BLACK, (player.centerx - 10, player.centery - 5, 20, 15), 3.14, 0, 2)


def draw_master_demo(win, x=400, y=300):
    """Draw a simplified enemy mushroom boss for cutscenes"""
    
    player_size = 40
    player = pygame.Rect(x, y, player_size, player_size)

    #Body
    pygame.draw.circle(win, WHITE, player.center, player_size // 2)
    # Eyes
    pygame.draw.circle(win, BLACK, (player.centerx - 10, player.centery - 1), 5)
    pygame.draw.circle(win, BLACK, (player.centerx + 10, player.centery - 1), 5)

    # Wizard Beard (big triangle starting from cheeks, going down)
    vertices = [
        (player.centerx - 20, player.centery + 5),   # left cheek
        (player.centerx + 20, player.centery + 5),   # right cheek
        (player.centerx, player.centery + 32)        # pointy end of beard
    ]
    pygame.draw.polygon(win, GRAY2, vertices)
    

    #Wizerd Hat
    vertices2 = [
        (player.centerx - 20, player.centery - 10),   # left cheek
        (player.centerx + 20, player.centery - 10),   # right cheek
        (player.centerx, player.centery - 35)        # pointy end of beard
    ]
    pygame.draw.rect(win, BROWN, (player.centerx - 20, player.centery - 13, 40, 6))
    pygame.draw.polygon(win, BROWN, vertices2)


def draw_spike_demo(win, x=600, y=100):
    """Draw falling spike demo using same shape as Level 3"""
    # Use same vertices style as actual game spikes
    vertices = [
        (x, y),          # Base point
        (x - 10, y + 25),  # Left point
        (x - 5, y + 15),   # Left middle
        (x - 15, y + 30),  # Left outer
        (x + 2, y + 20),   # Center middle
        (x + 15, y + 30),  # Right outer
        (x + 5, y + 15),   # Right middle
        (x + 10, y + 25)   # Right point
    ]

    pygame.draw.polygon(win, BLACK, vertices)


def draw_bad_mushroom_demo(win, x=550, y=300):
    """Draw a bad mushroom demo"""
    cap_width, cap_height = 30, 15
    stem_width, stem_height = 6, 10

    # Cap
    pygame.draw.ellipse(win, RED, (x - 3, y - 10, cap_width, cap_height))
    # Stem
    pygame.draw.rect(win, BROWN, (x + 9, y + 5, stem_width, stem_height))
    # Evil eyes
    eye_radius = 5
    pygame.draw.ellipse(win, BLACK, (x + 2, y - 6, eye_radius, eye_radius))
    pygame.draw.ellipse(win, BLACK, (x + 16, y - 6, eye_radius, eye_radius))

def draw_golden_mushroom_demo(win, x=380, y=250):
    """Draw a bad mushroom demo"""
    cap_width, cap_height = 30, 15
    stem_width, stem_height = 6, 10

    # Cap
    pygame.draw.ellipse(win, GOLD, (x - 3, y - 10, cap_width, cap_height))
    # Stem
    pygame.draw.rect(win, BROWN, (x + 9, y + 5, stem_width, stem_height))

def draw_vacuum_mushroom_demo(win, x=380, y=250):
    """Draw a bad mushroom demo"""
    cap_width, cap_height = 30, 15
    stem_width, stem_height = 6, 10

    # Cap
    pygame.draw.ellipse(win, RED, (x - 3, y - 10, cap_width, cap_height))
    # Stem
    pygame.draw.rect(win, BROWN, (x + 9, y + 5, stem_width, stem_height))
    #Magnet
    pygame.draw.arc(win, GRAY2, (x + 1, y - 24, 20, 20), 3.14, 0, 2)

def draw_normal_mushroom_demo(win, x=380, y=250):
    """Draw a bad mushroom demo"""
    cap_width, cap_height = 30, 15
    stem_width, stem_height = 6, 10

    # Cap
    pygame.draw.ellipse(win, RED, (x - 3, y - 10, cap_width, cap_height))
    # Stem
    pygame.draw.rect(win, BROWN, (x + 9, y + 5, stem_width, stem_height))

def draw_sky_mushroom_demo(win, x=380, y=250):
    """Draw a bad mushroom demo"""
    cap_width, cap_height = 30, 15
    stem_width, stem_height = 6, 10

    # Cap
    pygame.draw.ellipse(win, RED, (x - 3, y - 10, cap_width, cap_height))
    # Stem
    pygame.draw.rect(win, BROWN, (x + 9, y + 5, stem_width, stem_height))
    #Fly
    pygame.draw.ellipse(win, (GOLD), (x, y - 16, 24, 10), 4)

def draw_moving_mushroom_demo(win, x=380, y=250):
    """Draw a bad mushroom demo"""
    cap_width, cap_height = 30, 15
    stem_width, stem_height = 6, 10

    # Cap
    pygame.draw.ellipse(win, RED, (x - 3, y - 10, cap_width, cap_height))
    # Stem
    pygame.draw.rect(win, BROWN, (x + 3, y + 2, 6, 10))  # stem
    pygame.draw.rect(win, BROWN, (x + 14, y + 2, 6, 10))  # stem
    pygame.draw.rect(win, BROWN, (x - 3, y + 7, 6, 5))  # stem
    pygame.draw.rect(win, BROWN, (x + 19, y + 7, 6, 5))  # stem

def draw_flood_demo(win, x=500, y=400):
    """Draw rising flood demo"""
    width, max_height = 120, 200
    h = (pygame.time.get_ticks() // 20 % max_height)
    pygame.draw.rect(win, BLUE, (x, y - h, width, h))

# Add to your drawing functions
def draw_floodgate(win, x, y, width, height, open_progress):
    """Draw wooden floodgate with vertical planks"""
    # Gate frame
    pygame.draw.rect(win, (101, 67, 33), (x, y, width, height))
    
    # Vertical planks (fewer as gate opens)
    plank_count = max(3, int(10 * (1 - open_progress)))
    plank_width = width / (plank_count + 1)
    for i in range(plank_count):
        plank_x = x + (i+1)*plank_width
        pygame.draw.rect(win, (139, 69, 19), (plank_x-3, y, 6, height))

def draw_lever(win, x, y, pulled):
    """Draw lever with base and handle"""
    # Base
    pygame.draw.rect(win, (160, 82, 45), (x-10, y-20, 20, 40))
    
    # Handle
    handle_y = y - 10 if pulled else y - 30
    pygame.draw.line(win, (101, 67, 33), (x, y), (x, handle_y), 8)
    pygame.draw.circle(win, (139, 69, 19), (x, handle_y), 10)

def draw_chest_demo(win, x=678, y=400):

    c = pygame.Rect(x, y, 40, 40)

    pygame.draw.rect(win, BROWN, (c.centerx - 20, c.y, 40, 40)) 
    pygame.draw.rect(win, BLACK, (c.centerx - 20, c.y + 15, 40, 5)) 
    pygame.draw.rect(win, BLACK, (c.centerx - 20, c.y , 5, 40)) 
    pygame.draw.rect(win, BLACK, (c.centerx + 15, c.y , 5, 40)) 
    pygame.draw.rect(win, BLACK, (c.centerx - 20, c.y, 40, 5)) 
    pygame.draw.rect(win, BLACK, (c.centerx - 20, c.y + 40, 40, 5))
    pygame.draw.rect(win, GOLD, (c.centerx - 3, c.centery - 5, 6, 5)) 


def draw_key_demo(win, x=690, y=100):

    k = pygame.Rect(x, y, 18, 50)

    pygame.draw.circle(win, GOLD, (k.centerx, k.top + 10), 40 // 5)
    pygame.draw.rect(win, GOLD, (k.centerx - 3, k.y + 16, 6, 30)) 
    pygame.draw.rect(win, GOLD, (k.centerx - 9, k.bottom - 6, 12, 6))
    pygame.draw.rect(win, GOLD, (k.centerx - 9, k.bottom - 18, 12, 6))


def draw_water_spray(win, x, y, intensity):
    """Draw water spray effect from gate"""
    # Base splash
    for i in range(int(5 * intensity)):
        drop_y = y - random.randint(0, int(30 * intensity))
        drop_x = x + random.randint(-20, 20)
        pygame.draw.circle(win, (200, 200, 255), (drop_x, drop_y), random.randint(2, 5))
    
    # Bigger droplets
    for i in range(int(3 * intensity)):
        drop_y = y - random.randint(0, int(50 * intensity))
        drop_x = x + random.randint(-30, 30)
        pygame.draw.circle(win, (150, 200, 255), (drop_x, drop_y), random.randint(3, 7))

def Cutscene(level_num):
    """Show enemy cutscene with dialogue + gimmick demo before each level"""
    config = LEVELS[level_num]
    enemy_dialogue = get_enemy_dialogue()
    running = True

    # Collect enemy dialogue for this level
    messages = []
    for gimmick, lines in enemy_dialogue.items():
        if config.get(gimmick, False):
            messages.extend(lines)

    if not messages:
        global current_lang
        if current_lang == 1:
            messages = ["Collect 20 mushrooms to go further",
                        "But be careful",
                        "If you go to far",
                        "You will meet THE BOSS",    
                            ]
        elif current_lang == 2:
            messages = ["Збери 20 грибів щоб пройти далі",
                        "Але будь обережним",
                        "Якщо зайдеш занадто далеко",
                        "Ти зустрінешся з БОСОМ"    
                            ]


    current_msg = 0

    if config.get("with_chest"):
        chest_pos = (678, 400)
        mushrooms = [(200, 280), (200, 180), (250, 230), (300, 280), (300, 180)]
        enemy_pos = [WIDTH / 2 + 200, HEIGHT / 2 - 80]  # starting enemy
        held_mushrooms = []
        state = "approach_mushrooms"
        target_mushroom_index = 0
        speed = 2  # pixels per frame
        Cutscene.needs_reset = True


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    if current_msg < len(messages) - 1:
                        current_msg += 1
                    else:
                        running = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.time.wait(200)
                    running = False
                    Game(level_num, skip_cutscene=True)

        # Background
        win.fill(GREEN3)

        # --- Enemy drawing (always shown) ---
        if level_num in(2,3,5,6,7):
            draw_enemy_demo(win, WIDTH / 2 + 200, HEIGHT / 2 - 80)
        elif level_num == 1:
            draw_player_demo(win, x=380, y=300)
            draw_master_demo(win, x=380, y=100)
        elif level_num == 9:
            draw_player_demo(win, x=380, y=300)
            draw_master_demo(win, x=380, y=100)
            draw_golden_mushroom_demo(win, x=388, y=220)


        # --- Gimmick demos ---
        if config.get("with_spikes"):
            draw_spike_demo(win, x=200, y=280)
            draw_spike_demo(win, x=200, y=230)
            draw_spike_demo(win, x=200, y=180)

            draw_spike_demo(win, x=250, y=280)
            draw_spike_demo(win, x=250, y=230)
            draw_spike_demo(win, x=250, y=180)

            draw_spike_demo(win, x=300, y=280)
            draw_spike_demo(win, x=300, y=230)
            draw_spike_demo(win, x=300, y=180)

        if config.get("with_bad_mushrooms"):
            draw_bad_mushroom_demo(win, x=200, y=280)
            draw_bad_mushroom_demo(win, x=200, y=230)
            draw_bad_mushroom_demo(win, x=200, y=180)

            draw_bad_mushroom_demo(win, x=250, y=280)
            draw_bad_mushroom_demo(win, x=250, y=230)
            draw_bad_mushroom_demo(win, x=250, y=180)

            draw_bad_mushroom_demo(win, x=300, y=280)
            draw_bad_mushroom_demo(win, x=300, y=230)
            draw_bad_mushroom_demo(win, x=300, y=180)

        if config.get("with_chest"):
            # Update enemy movement
            if state == "approach_mushrooms":
                if target_mushroom_index < len(mushrooms):
                    target = mushrooms[target_mushroom_index]
                    dx, dy = target[0] - enemy_pos[0], target[1] - enemy_pos[1]
                    dist = (dx ** 2 + dy ** 2) ** 0.5
                    if dist < speed:
                        enemy_pos[0], enemy_pos[1] = target
                        held_mushrooms.append(target)
                        target_mushroom_index += 1
                        if target_mushroom_index >= len(mushrooms):
                            state = "move_to_chest"
                    else:
                        enemy_pos[0] += (dx / dist) * speed
                        enemy_pos[1] += (dy / dist) * speed

            elif state == "move_to_chest":
                dx, dy = chest_pos[0] - enemy_pos[0], chest_pos[1] - enemy_pos[1]
                dist = (dx ** 2 + dy ** 2) ** 0.5
                if dist < 30:  # enemy is near the chest
                    state = "near_the_chest"
                else:
                    enemy_pos[0] += (dx / dist) * speed
                    enemy_pos[1] += (dy / dist) * speed

            elif state == "near_the_chest":
                enemy_pos[0], enemy_pos[1] = chest_pos
                held_mushrooms = []  # mushrooms disappear

            # Draw all elements
            # Draw mushrooms that are still on the ground
            for m in mushrooms:
                if m not in held_mushrooms:
                    draw_normal_mushroom_demo(win, *m)

            # Draw enemy
            draw_enemy_demo(win, x=enemy_pos[0], y=enemy_pos[1])
            
            # Draw mushrooms held by enemy
            if state in ["approach_mushrooms", "move_to_chest"]:
                for i, m in enumerate(held_mushrooms):
                    draw_normal_mushroom_demo(win, enemy_pos[0] - 30 + i * 10, enemy_pos[1] - 60)
            elif state == "near_the_chest":
                mushrooms = []
            
            # Draw chest
            draw_chest_demo(win, x=chest_pos[0], y=chest_pos[1])

        # In your cutscene code:
        if config.get("with_flood"):
            # Initialize or reset all variables
            if not hasattr(Cutscene, 'flood_initialized') or getattr(Cutscene, 'needs_reset', True):
                # First-time initialization
                Cutscene.flood_initialized = True
                Cutscene.needs_reset = False
                Cutscene.enemy_pos = [WIDTH//2, HEIGHT - 320]
                Cutscene.lever_pos = (WIDTH - 150, HEIGHT - 300)
                Cutscene.gate_pos = (0, HEIGHT - 250)
                Cutscene.flood_state = "approach_lever"
                Cutscene.water_level = 0
                Cutscene.gate_open_progress = 0
                Cutscene.lever_pulled = False
                Cutscene.lever_start_time = 0
                Cutscene.gate_start_time = 0
                Cutscene.enemy_speed = 3
            
            # Local references for cleaner code
            flood_state = Cutscene.flood_state
            enemy_pos = Cutscene.enemy_pos
            lever_pos = Cutscene.lever_pos
            gate_pos = Cutscene.gate_pos
            water_level = Cutscene.water_level
            gate_open_progress = Cutscene.gate_open_progress
            lever_pulled = Cutscene.lever_pulled

            # Update logic
            if flood_state == "approach_lever":
                target_x = lever_pos[0] - 50
                target_y = lever_pos[1]
                
                dx = target_x - enemy_pos[0]
                dy = target_y - enemy_pos[1]
                distance = (dx**2 + dy**2)**0.5
                
                if distance > 5:
                    enemy_pos[0] += (dx/distance) * Cutscene.enemy_speed
                    enemy_pos[1] += (dy/distance) * Cutscene.enemy_speed
                else:
                    flood_state = "pulling_lever"
                    Cutscene.lever_start_time = pygame.time.get_ticks()

            elif flood_state == "pulling_lever":
                if not lever_pulled:
                    if pygame.time.get_ticks() > Cutscene.lever_start_time + 500:
                        lever_pulled = True
                        Cutscene.lever_pulled = True
                        Cutscene.gate_start_time = pygame.time.get_ticks()
                else:
                    elapsed = pygame.time.get_ticks() - Cutscene.gate_start_time
                    gate_open_progress = min(1.0, elapsed / 2000)
                    Cutscene.gate_open_progress = gate_open_progress
                    
                    if gate_open_progress >= 1.0:
                        flood_state = "flood_rising"

            elif flood_state == "flood_rising":
                water_level = min(300, water_level + 1.5)
                Cutscene.water_level = water_level
                if water_level >= 220:
                    flood_state = "complete"

            # Update the stored state
            Cutscene.flood_state = flood_state

            # Drawing code (same as before)
            if water_level > 0:
                pygame.draw.rect(win, (70, 130, 180), (0, HEIGHT - water_level, WIDTH, water_level))

            draw_floodgate(win, gate_pos[0], gate_pos[1], WIDTH, 40, gate_open_progress)
            draw_lever(win, *lever_pos, lever_pulled)
            draw_enemy_demo(win, *enemy_pos)

            if flood_state == "flood_rising" and water_level < 50:
                spray_x = random.randint(100, WIDTH-100)
                pygame.draw.circle(win, (200, 230, 255), (spray_x, HEIGHT - water_level), random.randint(5, 15))
            
        if config.get("vacuum"):
            draw_vacuum_mushroom_demo(win, x=200, y=280)
            draw_vacuum_mushroom_demo(win, x=200, y=230)
            draw_vacuum_mushroom_demo(win, x=200, y=180)

            draw_vacuum_mushroom_demo(win, x=250, y=280)
            draw_vacuum_mushroom_demo(win, x=250, y=230)
            draw_vacuum_mushroom_demo(win, x=250, y=180)

            draw_vacuum_mushroom_demo(win, x=300, y=280)
            draw_vacuum_mushroom_demo(win, x=300, y=230)
            draw_vacuum_mushroom_demo(win, x=300, y=180)

        if config.get("moving_mushrooms"):
            draw_moving_mushroom_demo(win, x=200, y=280)
            draw_moving_mushroom_demo(win, x=200, y=230)
            draw_moving_mushroom_demo(win, x=200, y=180)

            draw_moving_mushroom_demo(win, x=250, y=280)
            draw_moving_mushroom_demo(win, x=250, y=230)
            draw_moving_mushroom_demo(win, x=250, y=180)

            draw_moving_mushroom_demo(win, x=300, y=280)
            draw_moving_mushroom_demo(win, x=300, y=230)
            draw_moving_mushroom_demo(win, x=300, y=180)

        if config.get("sky_mushrooms"):
            draw_sky_mushroom_demo(win, x=200, y=280)
            draw_sky_mushroom_demo(win, x=200, y=230)
            draw_sky_mushroom_demo(win, x=200, y=180)

            draw_sky_mushroom_demo(win, x=250, y=280)
            draw_sky_mushroom_demo(win, x=250, y=230)
            draw_sky_mushroom_demo(win, x=250, y=180)

            draw_sky_mushroom_demo(win, x=300, y=280)
            draw_sky_mushroom_demo(win, x=300, y=230)
            draw_sky_mushroom_demo(win, x=300, y=180)


        # --- Dialogue text ---
        text = font_medium.render(messages[current_msg], True, WHITE)
        win.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT - 150))
    

        if current_lang == 1:
            hint_text = "Press SPACE to continue"  # fallback text
        elif current_lang ==2:
            hint_text = "Натисніть ПРОБІЛ щоб продовжити"


        hint_surface = font_medium.render(hint_text, True, GOLD)
        win.blit(hint_surface, (WIDTH//2 - hint_surface.get_width()//2, HEIGHT - 60))
        win.blit(hint_surface, (WIDTH//2 - hint_surface.get_width()//2, HEIGHT - 60))

        pygame.display.flip()
        clock.tick(60)

def Title():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        win.fill(WHITE)
        logo_font = pygame.font.Font("Fondamento-Regular.ttf", 48)
        logo = logo_font.render("Mushroom Duo", True, BLACK)
        win.blit(logo, (WIDTH/2 - 170, HEIGHT/2 + 50))


        pygame.draw.arc(win, BLACK, (0,HEIGHT/4, 400,400), 0, 0.6, 20)
        pygame.draw.ellipse(win, RED, (WIDTH/2 - 90,HEIGHT/2 - 90,100,50) )
        pygame.draw.arc(win, BLACK, (WIDTH/2 - 18, HEIGHT/4 + 50, 400, 300), math.pi - 0.6, math.pi, 20)
        pygame.draw.ellipse(win, RED, (WIDTH/2 - 9,HEIGHT/4 + 100,60,35) )
        pygame.draw.ellipse(win, BLACK, (WIDTH/2 - 100,HEIGHT/4 + 23,180,180),3)
        pygame.display.flip()
        clock.tick(60)


#Title()
#Menu()
#Shop(1)


LanguageMenu()

