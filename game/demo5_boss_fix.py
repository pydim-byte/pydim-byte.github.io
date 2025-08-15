import sys
import math
import random
import pygame


pygame.init()
clock = pygame.time.Clock()

#Music 
try:
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.load('yoshi.mp3')
    pygame.mixer.music.play(-1)
except:
    print("No music found")


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

# Fonts
font_large = pygame.font.SysFont("arial", 60)
font_medium = pygame.font.SysFont("arial", 40)

#Level system
current_skin = "none"
mushroom_inventory = 0

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
    1: {"level_color": GREEN, "with_spikes": False, "with_bad_mushrooms": False, "moving_mushrooms": False, "with_enemy": False, "with_chest": False, "sky_mushrooms": False, "with_flood": False, "vacuum": False},
    2: {"level_color": GREEN3, "with_spikes": False, "with_bad_mushrooms": True, "moving_mushrooms": False, "with_enemy": False, "with_chest": False, "sky_mushrooms": False, "with_flood": False, "vacuum": False},
    3: {"level_color": GREEN2, "with_spikes": True, "with_bad_mushrooms": False, "moving_mushrooms": False, "with_enemy": False, "with_chest": False, "sky_mushrooms": False, "with_flood": False, "vacuum": False},
    4: {"level_color": GREEN2, "with_spikes": False, "with_bad_mushrooms": False, "moving_mushrooms": False, "with_enemy": False, "with_chest": True, "sky_mushrooms": False, "with_flood": False, "vacuum": False},
    5: {"level_color": GREEN, "with_spikes": False, "with_bad_mushrooms": False, "moving_mushrooms": False, "with_enemy": False, "with_chest": False, "sky_mushrooms": False, "with_flood": False, "vacuum": True},
    6: {"level_color": GREEN, "with_spikes": False, "with_bad_mushrooms": False, "moving_mushrooms": True, "with_enemy": False, "with_chest": False, "sky_mushrooms": False, "with_flood": False, "vacuum": False},
    7: {"level_color": GREEN2, "with_spikes": False, "with_bad_mushrooms": False, "moving_mushrooms": False, "with_enemy": False, "with_chest": False, "sky_mushrooms": True, "with_flood": False, "vacuum": False},
    8: {"level_color": GREEN4, "with_spikes": False, "with_bad_mushrooms": False, "moving_mushrooms": False, "with_enemy": False, "with_chest": False, "sky_mushrooms": False, "with_flood": True}, "vacuum": False,
    9: {"level_color": GREEN4, "with_spikes": False, "with_bad_mushrooms": False, "moving_mushrooms": False, "with_enemy": True, "with_chest": False, "sky_mushrooms": False, "with_flood": False, "vacuum": False},

}

max_level = len(LEVELS)

class Assets:
    def __init__(self, config):
        global MODE
        self.enemy_speed = 8
        # Initialize with the config data first
        self.with_chest = config.get("with_chest", False)  # First, initialize with_chest from config

        # Now initialize the rest of the attributes
        self.player_size = 40
        self.player = pygame.Rect(90, 90, self.player_size, self.player_size)
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

        self.last_spawn_time = 0  # Time of the last mushroom spawn (in ms)
        self.spawn_interval = 500  # 2 seconds in milliseconds
        self.mushroom_count = 20  # Total number of mushrooms to spawn
        self.spawned_mushrooms = 0  # Track how many mushrooms have been spawned

        self.flood = []

        self.rect_coords = []
        blockSize = 40

        # Loop through the grid and get coordinates
        for x in range(50, WIDTH - 50, blockSize):
            for y in range(50, HEIGHT - 50, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                self.rect_coords.append((x, y))  

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
                                player_invincible = True
                                invincible_timer = pygame.time.get_ticks()
                            # Remove or ignore this projectile after collision
                            self.projectiles.remove(proj)
                            break  # stop checking other projectiles this frame

            if shooting:
                self.boss_cooldown -= 1
                if self.boss_cooldown <= 0:
                    num_shots = 20
                    spread = 0.6  # radians
                    angle_to_player = math.atan2(dy, dx)
                    for i in range(num_shots):
                        angle = angle_to_player + (i - num_shots//2) * spread
                        vx = math.cos(angle) * 6
                        vy = math.sin(angle) * 6
                        self.projectiles.append({
                            "rect": pygame.Rect(enemy.centerx, enemy.centery, 10, 10),
                            "vx": vx,
                            "vy": vy
                        })
                    self.boss_cooldown = 40  # 1 burst/sec

            if super and self.not_super:
                self.not_super = False
                if self.rect_coords:  # Check if there are still available positions
                    random_rects = random.sample(self.rect_coords, 1)
                    rand_x, rand_y = random_rects[0]
                    x, y = rand_x, rand_y
                    rect = pygame.Rect(x, y, self.mushroom_radius * 2, self.mushroom_radius * 2)
                    self.super_m.append(rect)


            for m in self.super_m:
                pygame.draw.rect(win, BROWN, (m.centerx - 3, m.bottom - 10, 6, 10))  # stem
                pygame.draw.ellipse(win, GOLD, (m.x, m.y, self.mushroom_radius * 2, self.mushroom_radius))  # cap
                    
            for m in self.super_m[:]:
                if player.colliderect(m):
                    self.super_m.remove(m)
                    #MODE = GOLD
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

            # Also don't push key into other obstacles (like chest or spikes)
            collides_with_chest = (self.chest and new_key_rect.colliderect(self.chest))
            # (Add any other obstacle checks here)

            if within_bounds and not collides_with_chest:
                # move both player and key
                self.key = new_key_rect
                self.player = new_player_rect
            else:
                # If the key WOULD land on the chest, we can make them vanish:
                if collides_with_chest:
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
        """Create mushrooms and spikes, draw them, and return their rect lists."""
        mushroom_count = 20
        mushroom_time = pygame.time.get_ticks()

        # If mushrooms should spawn immediately, generate them
        if not self.with_chest and not self.with_enemy and self.mushrooms_spawned < mushroom_count: # Only spawn until we reach mushroom_count
            if self.sky_mushrooms:
                # For sky mushrooms, spawn one by one with a delay
                if len(self.mushrooms) == 0:  # First mushroom needs to wait for the delay
                    self.last_spawn_time = mushroom_time - self.spawn_interval  # Set last_spawn_time to allow first mushroom to spawn immediately
                if mushroom_time - self.last_spawn_time >= self.spawn_interval:
                    # Spawn mushrooms only on y-coordinates 50, 100, 150
                    possible_y_coords = [50, 100, 150]
                    if self.mushrooms_spawned < mushroom_count and self.rect_coords:  # Check if we still need mushrooms and available positions
                        random_rects = random.sample(self.rect_coords, 1)
                        rand_x, _ = random_rects[0]
                        rand_y = random.choice(possible_y_coords)  # Pick a random y from the allowed y-values
                        x, y = rand_x, rand_y
                        rect = pygame.Rect(x, y, self.mushroom_radius * 2, self.mushroom_radius * 2)
                        self.mushrooms.append(rect)
                        self.mushrooms_spawned += 1
                        try:
                            # Try to remove the coordinate if it exists in rect_coords
                            self.rect_coords.remove((rand_x, rand_y))
                        except ValueError:
                            # If the coordinate is not found, skip the removal and move to the next mushroom
                            pass
                        self.last_spawn_time = mushroom_time  # Update last spawn time after mushroom spawn
            else:
                # Normal mushroom spawning (all at once)
                if len(self.mushrooms) == 0:  # Only spawn once at the start of the level
                    for _ in range(mushroom_count):
                        if self.rect_coords:  # Check if there are still available positions
                            random_rects = random.sample(self.rect_coords, 1)
                            rand_x, rand_y = random_rects[0]
                            x, y = rand_x, rand_y
                            rect = pygame.Rect(x, y, self.mushroom_radius * 2, self.mushroom_radius * 2)
                            self.mushrooms.append(rect)
                            try:
                                # Try to remove the coordinate if it exists in rect_coords
                                self.rect_coords.remove((rand_x, rand_y))
                            except ValueError:
                                pass

        # Draw mushrooms as usual
        for m in self.mushrooms:
            #Basicly fall code
            if self.sky_mushrooms:
                m.y += 2
                if m.y > 600:
                    Over(8)
            pygame.draw.rect(win, BROWN, (m.centerx - 3, m.bottom - 10, 6, 10))  # stem
            pygame.draw.ellipse(win, RED, (m.x, m.y, self.mushroom_radius * 2, self.mushroom_radius))  # cap



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

                # Prevent mushrooms from going out of bounds (considering mushroom size)
                if m.left < 0:  # Left boundary
                    m.left = 0
                elif m.right > win.get_width():  # Right boundary
                    m.right = win.get_width()

                if m.top < 40:  # Upper boundary (prevent going above 40 pixels)
                    m.top = 40
                elif m.bottom > win.get_height():  # Bottom boundary
                    m.bottom = win.get_height()

       



        # Generate spikes once (if needed)
        if self.with_spikes and not self.spikes_generated:
            for _ in range(50):
                if self.rect_coords:  # Ensure there are available positions for spikes
                    random_rects = random.sample(self.rect_coords, 1)
                    rand_x, rand_y = random_rects[0]
                    x, y = rand_x, rand_y
                    rect = pygame.Rect(x, y, self.mushroom_radius * 2, self.mushroom_radius * 2)
                    # Remove the selected coordinates for spikes to avoid overlap
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
                        vertices = [(x, y), (x - 15, y + 30), (x + 15, y + 30)]
                        self.spike.append(vertices)
                        self.spike_rects.append(pygame.Rect(x - 15, y, 30, 30))  # collision rect

            self.spikes_generated = True

        # Draw spikes
        for s in self.spike:
            pygame.draw.polygon(win, BLACK, s)



        # Generate bad mushrooms (if needed)
        if self.with_bad_mushrooms and not self.bad_mushrooms:
            for _ in range(20):
                while True:
                    if self.rect_coords:  # Ensure there are available positions for spikes
                        random_rects = random.sample(self.rect_coords, 1)
                        rand_x, rand_y = random_rects[0]
                        x, y = rand_x, rand_y
                        rect = pygame.Rect(x, y, self.mushroom_radius * 2, self.mushroom_radius * 2)
                        # Remove the selected coordinates for spikes to avoid overlap
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

            self.spikes_generated = True

        # Draw bad mushrooms
        for b in self.bad_mushrooms:
            pygame.draw.rect(win, BROWN, (b.centerx - 3, b.bottom - 10, 6, 10))  # stem
            pygame.draw.ellipse(win, RED, (b.x, b.y, self.mushroom_radius * 2, self.mushroom_radius))  # cap
            pygame.draw.ellipse(win, BLACK, (b.x + 5, b.y + 3, self.mushroom_radius // 3, self.mushroom_radius // 3))
            pygame.draw.ellipse(win, BLACK, (b.x + 20, b.y + 3, self.mushroom_radius // 3, self.mushroom_radius // 3))

        return self.mushrooms, self.spike_rects, self.bad_mushrooms

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
        level_text = font.render(f"Player: ", True, TEXT_COLOR)
        goal_text = font.render(f"GOAL: {score}/20", True, TEXT_COLOR)
        collected_text = font.render(f"Boss: ", True, TEXT_COLOR)
        win.blit(level_text, (20, 10))
        win.blit(goal_text, (330, 10))
        win.blit(collected_text, (615, 10))

        # Player hearts
        for i in range(player_health):
            pygame.draw.circle(win, RED, (120 + i*35, 20), 15)

        # Boss hearts
        for i in range(boss_health):
            pygame.draw.circle(win, RED, (700 + i*35, 20), 15)

    else:
        # Normal HUD
        level_text = font.render(f"LEVEL: {level_num}", True, TEXT_COLOR)
        goal_text = font.render(f"GOAL: {score}/{20}", True, TEXT_COLOR)
        collected_text = font.render(f"MUSHROOMS COLLECTED: {collected}", True, TEXT_COLOR)
        win.blit(level_text, (20, 10))
        win.blit(goal_text, (200, 10))
        win.blit(collected_text, (400, 10))


def Game(level_num):
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
    INVINCIBLE_TIME = 1000  # milliseconds (1 second of invincibility)

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

        # Mushroom collision
        if assets.handle_mushroom_collection(player):
            score += 1
            collected += 1
            

        for b in bad_mushrooms[:]:
            if player.colliderect(b):
                running = False
                Over(level_num)

        # Spike collision
        for rect in spikes:
            if player.colliderect(rect):
                running = False
                Over(level_num)

        
        
       
        if (pygame.time.get_ticks() - damage_timer) > 1000:
            assets.enemy_speed = 8
            

        if enemy and player.colliderect(enemy):
            if assets.super_state:
                e -= 1
                assets.enemy_speed = -8
                assets.super_state = False
                damage_timer = pygame.time.get_ticks()
                
            elif not assets.super_state and not player_invincible:
                p -= 1
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
                
                if level_num in (1,3,5,8, 9):
                    # For level 1, skip skin unlock, just go to next level or victory
                    if level_num == 9:
                        Victory()
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
        f"Purchase ({cost})", 
        WIDTH//2 - 300, HEIGHT-100, 
        250, 60, 
        STALL_COLOR,
        text_color=WHITE
    )
    skip_button = Button(
        "Maybe Later", 
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

    def draw_skin_display():
        # Skin display panel
        panel = pygame.Surface((300, 150), pygame.SRCALPHA)
        pygame.draw.rect(panel, PANEL_COLOR, (0, 0, 300, 150), border_radius=10)
        pygame.draw.rect(panel, BORDER_COLOR, (0, 0, 300, 150), 3, border_radius=10)
        
        # Skin name
        name_text = font_large.render(skin_name, True, GOLD)
        panel.blit(name_text, (150 - name_text.get_width()//2, 20))
        
        # Cost
        cost_text = font_medium.render(f"{cost} Mushrooms", True, WHITE)
        panel.blit(cost_text, (150 - cost_text.get_width()//2, 80))
        
        win.blit(panel, (WIDTH//2 - 150, 100))

    def draw_current_mushrooms():
        text = font_medium.render(f"Mushrooms: {mushroom_inventory}", True, WHITE)
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
        "Equip Now", 
        WIDTH//2 - 320, HEIGHT//2 + 150, 
        250, 60, 
        (139, 69, 19),  # Brown
        equip_action,
        (255, 255, 255)  # White text
    )
    
    collect_button = Button(
        "Add to Collection",
        WIDTH//2 + 70, HEIGHT//2 + 150,
        250, 60,
        (139, 69, 19),
        collect_action,
        (255, 255, 255)
    )

    # Custom drawing for skin preview
    def draw_skin_preview():
        # Title text
        title = font_large.render(f"New Skin Unlocked!", True, BLACK)
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
        "Continue", 
        WIDTH//2 - 100, HEIGHT//2 - 30, 
        200, 60, 
        (139, 69, 19),  # Brown
        continue_action,
        (255, 255, 255)  # White text
    )
    
    menu_button = Button(
        "Main Menu",
        WIDTH//2 - 100, HEIGHT//2 + 170,
        200, 60,
        (139, 69, 19),
        menu_action,
        (255, 255, 255)
    )

    # Custom drawing for level complete screen
    def draw_level_complete():
        # Simple black title
        title = font_large.render("Level Complete", True, BLACK)
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
        Game(current_level)
    
    def menu_action():
        Menu()

    # Create buttons
    retry_button = Button(
        "Try Again", 
        WIDTH//2 - 100, HEIGHT//2 - 30, 
        200, 60, 
        (139, 69, 19),  # Brown
        retry_action,
        (255, 255, 255)  # White text
    )
    
    menu_button = Button(
        "Main Menu",
        WIDTH//2 - 100, HEIGHT//2 + 170,
        200, 60,
        (139, 69, 19),
        menu_action,
        (255, 255, 255)
    )

    # Custom drawing for game over screen
    def draw_game_over():
        # Simple black title centered
        title = font_large.render("Game Over", True, BLACK)
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
    def play_action():
        Game(1)
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
    
    play_button = Button("Play", WIDTH//2-100, HEIGHT//2-100, 200, 60, button_color, play_action, text_color)
    level_button = Button("Levels", WIDTH//2-100, HEIGHT//2, 200, 60, button_color, level_action, text_color)
    skin_button = Button("Skins", WIDTH//2-100, HEIGHT//2+100, 200, 60, button_color, skin_action, text_color)
    quit_button = Button("Quit", WIDTH//2-100, HEIGHT//2+200, 200, 60, button_color, quit_action, text_color)

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

    prev_button = Button("Previous", WIDTH // 2 - 350, HEIGHT // 2 + 150, 150, 100, GRAY, previous_skin_action)
    next_button = Button("Next", WIDTH // 2 + 200, HEIGHT // 2 + 150, 150, 100, GRAY, next_skin_action)
    back_button = Button("Back", WIDTH // 2 - 75, HEIGHT // 2 + 150, 150, 100, GRAY, back_action)

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

    # Forest-themed colors
    button_color = (139, 69, 19)  # Brown
    text_color = (255, 255, 255)  # White

    # Buttons with consistent forest styling
    L1_button = Button("Level 1", WIDTH//2-100, HEIGHT//2-200, 200, 60, 
                      button_color, lambda: level_action(1), text_color)
    L2_button = Button("Level 2", WIDTH//2-100, HEIGHT//2-100, 200, 60,
                      button_color, lambda: level_action(2), text_color)
    L3_button = Button("Level 3", WIDTH//2-100, HEIGHT//2, 200, 60,
                      button_color, lambda: level_action(3), text_color)
    L4_button = Button("Level 4", WIDTH//2-100, HEIGHT//2+100, 200, 60,
                      button_color, lambda: level_action(4), text_color)
    Back_button = Button("Back", WIDTH//2-100, HEIGHT//2+200, 200, 60,
                        button_color, back_action, text_color)

    # Create menu instance
    level_menu = BaseMenu(
        win,
        font_medium,
        font_large,
        "",  # Empty title string
        [L1_button, L2_button, L3_button, L4_button, Back_button],
        use_gradient=True,
    )

    # Key to level mapping
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
            
            # Handle mouse events
            level_menu.handle_events(event)
            
            # Handle keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key in key_mapping:
                    level_action(key_mapping[event.key])
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    back_action()
                    running = False
        
        # Draw everything
        level_menu.draw()
        pygame.display.flip()
        clock.tick(60)


def Victory():
    def play_again_action():
        Game(1)
    
    def quit_action():
        pygame.quit()
        sys.exit()

    # Create buttons with consistent styling
    play_button = Button(
        "Play Again", 
        WIDTH//2 - 100, HEIGHT//2 - 30, 
        200, 60, 
        (139, 69, 19),  # Brown
        play_again_action,
        (255, 255, 255)  # White text
    )
    
    quit_button = Button(
        "Quit Game",
        WIDTH//2 - 100, HEIGHT//2 + 170,
        200, 60,
        (139, 69, 19),
        quit_action,
        (255, 255, 255)
    )

    # Custom drawing for victory screen
    def draw_victory():
        # Title text
        title = font_large.render("YOU WON!", True, BLACK)
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



CUTSCENE_SPEED = 3  # Pixels per frame

class Cutscene:
    def __init__(self, actions):
        self.actions = actions
        self.current_action = 0
        self.timer = 0
        self.is_running = False
        self.active_entities = {}  # Track moving entities
    
    def start(self, assets):
        self.assets = assets
        self.is_running = True
        self._start_next_action()
    
    def _start_next_action(self):
        if self.current_action < len(self.actions):
            action = self.actions[self.current_action]
            self.timer = action.get("duration", 0)
            
            # Initialize movement targets if needed
            if "move_to" in action:
                entity = action.get("entity", "player")
                self.active_entities[entity] = {
                    'target': action["move_to"],
                    'speed': action.get("speed", CUTSCENE_SPEED)
                }
            
            self.current_action += 1
    
    def update(self):
        if not self.is_running:
            return False
        
        action_completed = False
        current_action = self.actions[self.current_action - 1]  # Get current action (0-based vs 1-based)
        
        # Handle movement actions
        if "move_to" in current_action:
            entity_name = current_action.get("entity", "player")
            entity = getattr(self.assets, entity_name)
            target_x, target_y = current_action["move_to"]
            
            # Calculate movement
            dx = target_x - entity.centerx
            dy = target_y - entity.centery
            distance = (dx**2 + dy**2)**0.5
            
            if distance > 0:
                # Move toward target
                speed = current_action.get("speed", CUTSCENE_SPEED)
                move_x = dx/distance * speed
                move_y = dy/distance * speed
                
                # Prevent overshooting
                if abs(dx) < abs(move_x):
                    entity.centerx = target_x
                else:
                    entity.centerx += move_x
                    
                if abs(dy) < abs(move_y):
                    entity.centery = target_y
                else:
                    entity.centery += move_y
            else:
                action_completed = True
        
        # Handle timed actions
        elif "duration" in current_action:
            self.timer -= 1
            if self.timer <= 0:
                action_completed = True
        
        # Default completion for instant actions
        else:
            action_completed = True
        
        # Progress to next action if current is done
        if action_completed:
            if self.current_action < len(self.actions):
                self._start_next_action()
            else:
                self.is_running = False
        
        return self.is_running

    def draw(self, win):
        # Draw speech bubbles if needed
        if self.is_running and "text" in self.actions[self.current_action-1]:
            text = self.actions[self.current_action-1]["text"]
            self._draw_speech_bubble(win, text)
    
    def _draw_speech_bubble(self, win, text):
        # Constants
        bubble_padding = 20  # Space between text and bubble edge
        max_width = 300     # Maximum bubble width
        line_spacing = 5    # Space between text lines
        pointer_height = 15 # Height of the pointer triangle
        
        # Word wrapping (same as before)
        font = font_medium
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width - 2*bubble_padding:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        # Calculate dimensions
        text_surfs = [font.render(line, True, BLACK) for line in lines]
        max_line_width = max(surf.get_width() for surf in text_surfs)
        text_height = sum(font.get_height() for _ in lines) + (len(lines)-1)*line_spacing
        
        # Bubble dimensions with descender space
        bubble_width = min(max_line_width + 2*bubble_padding, max_width)
        bubble_height = text_height + 2*bubble_padding + font.get_descent()
        
        # Position bubble - KEY FIX IS HERE
        bubble_x = self.assets.player.centerx
        # Position just above player's head with small gap
        bubble_y = self.assets.player.y - self.assets.player.height//2 - pointer_height
        
        # Keep on screen
        bubble_x = max(bubble_width//2, min(bubble_x, WIDTH - bubble_width//2))
        bubble_y = max(bubble_height + pointer_height, min(bubble_y, HEIGHT - 20))
        
        # Draw bubble
        bubble_rect = pygame.Rect(
            bubble_x - bubble_width//2,
            bubble_y - bubble_height - pointer_height,  # Account for pointer
            bubble_width,
            bubble_height
        )
        pygame.draw.rect(win, WHITE, bubble_rect)
        pygame.draw.rect(win, BLACK, bubble_rect, 2)
        
        # Draw pointer triangle (now properly connected)
        pygame.draw.polygon(win, WHITE, [
            (bubble_x, bubble_y),
            (bubble_x - 15, bubble_y - pointer_height),
            (bubble_x + 15, bubble_y - pointer_height)
        ])
        pygame.draw.polygon(win, BLACK, [
            (bubble_x, bubble_y),
            (bubble_x - 15, bubble_y - pointer_height),
            (bubble_x + 15, bubble_y - pointer_height)
        ], 2)
        
        # Draw text
        y_offset = bubble_y - bubble_height - pointer_height + bubble_padding
        for i, text_surf in enumerate(text_surfs):
            win.blit(text_surf, (
                bubble_x - text_surf.get_width()//2,
                y_offset + i*(font.get_height() + line_spacing)
            ))


def TEST():
    # Initialize pygame
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    # Simple assets with player and NPC
    class TestAssets:
        def __init__(self):
            self.player = pygame.Rect(100, HEIGHT//2, 32, 32)
            self.npc1 = pygame.Rect(500, HEIGHT//2, 32, 32)
        
        def draw(self):
            pygame.draw.rect(win, (255, 0, 0), self.player)  # Red player
            pygame.draw.rect(win, (0, 0, 255), self.npc1)    # Blue NPC
    
    assets = TestAssets()
    
    # Test cutscene with all steps
    cutscene = Cutscene([
        {"entity": "npc1", "move_to": (WIDTH//2, HEIGHT//2), "text": "NPC moves first", "duration": 60},
        {"entity": "player", "move_to": (WIDTH//3, HEIGHT//2), "text": "Now I move!", "duration": 60},
        {"entity": "npc1", "move_to": (WIDTH//4, HEIGHT//3), "speed": 2, "text": "Going to meeting point"},
        {"entity": "player", "move_to": (WIDTH//4, HEIGHT//3), "text": "Let's meet here!", "duration": 120}
    ])
    
    cutscene.start(assets)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update cutscene
        running = cutscene.update()
        
        # Draw
        win.fill((240, 240, 240))
        assets.draw()
        cutscene.draw(win)
        
        # Debug info
        font = pygame.font.SysFont(None, 24)
        debug_text = [
            f"Current action: {cutscene.current_action}/{len(cutscene.actions)}",
            f"NPC: ({assets.npc1.x}, {assets.npc1.y})",
            f"Player: ({assets.player.x}, {assets.player.y})"
        ]
        for i, text in enumerate(debug_text):
            win.blit(font.render(text, True, (0,0,0)), (10, 10 + i*25))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

#TEST()
Menu()
#Shop(1)

