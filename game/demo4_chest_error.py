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
BLUE = (100, 100, 200)
YELLOW = (200, 200, 100)
GOLD = (255, 215, 0)
ORANGE = (255, 165, 0)
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


LEVELS = {
    1: {"level_color": GREEN, "with_spikes": False, "with_bad_mushrooms": False, "moving_mushrooms": False, "with_enemy": False},
    2: {"level_color": GREEN2, "with_spikes": True, "with_bad_mushrooms": False, "moving_mushrooms": False, "with_enemy": False},
    3: {"level_color": GREEN3, "with_spikes": False, "with_bad_mushrooms": True, "moving_mushrooms": False, "with_enemy": False},
    4: {"level_color": GREEN4, "with_spikes": False, "with_bad_mushrooms": False, "moving_mushrooms": False, "with_enemy": True},
    5: {"level_color": GREEN, "with_spikes": False, "with_bad_mushrooms": False, "moving_mushrooms": True, "with_enemy": False},
}

max_level = len(LEVELS)

class Assets:
    def __init__(self, config):
        self.player_size = 40
        self.player = pygame.Rect(90, 90, self.player_size, self.player_size)
        self.enemy = pygame.Rect(690, 100, self.player_size, self.player_size)
        self.key = pygame.Rect(690, 100, 18, 50)
        self.chest = pygame.Rect(678, 400, self.player_size, self.player_size)
        self.min_speed = 1  # Starting speed when key is pressed
        self.max_speed = 12  # Maximum speed
        self.acceleration_rate = 1  # How fast speed increases over time
        self.player_speed = self.min_speed  # Current player speed
        self.mushroom_radius = 15
        self.mushrooms = []
        self.bad_mushrooms = []
        self.spike = []
        self.spike_rects = []
        self.safe_distance = 60
        self.spikes_generated = False
        self.bad_mushrooms_generated = False
        self.level_color = config.get("level_color", GREEN)
        self.with_spikes = config.get("with_spikes", False)
        self.with_bad_mushrooms = config.get("with_bad_mushrooms", False)
        self.with_enemy = config.get("with_enemy", False)
        self.moving_mushrooms = config.get("moving_mushrooms", False)

        self.rect_coords = []
        blockSize = 40

        # Loop through the grid and get coordinates
        for x in range(50, WIDTH - 50, blockSize):
            for y in range(50, HEIGHT - 50, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                self.rect_coords.append((x, y))

        

    def Key(self):
        key = self.key
        #with_key = self.with_key
        player = self.player
        key_size = self.player_size
        pygame.draw.circle(win, GOLD, (key.centerx, key.top + 10), self.player_size // 5)
        pygame.draw.rect(win, GOLD, (key.centerx - 3, key.y + 16, 6, 30)) 
        pygame.draw.rect(win, GOLD, (key.centerx - 9, key.bottom - 6, 12, 6))
        pygame.draw.rect(win, GOLD, (key.centerx - 9, key.bottom - 18, 12, 6))

        return key

    def Chest(self):
        chest = self.chest
        #with_key = self.with_key
        player = self.player
        chest_size = self.player_size
        pygame.draw.rect(win, BROWN, (chest.centerx - 20, chest.y, 40, 40)) 
        pygame.draw.rect(win, BLACK, (chest.centerx - 20, chest.y + 15, 40, 5)) 
        pygame.draw.rect(win, BLACK, (chest.centerx - 20, chest.y , 5, 40)) 
        pygame.draw.rect(win, BLACK, (chest.centerx + 15, chest.y , 5, 40)) 
        pygame.draw.rect(win, BLACK, (chest.centerx - 20, chest.y, 40, 5)) 
        pygame.draw.rect(win, BLACK, (chest.centerx - 20, chest.y + 40, 40, 5))
        pygame.draw.rect(win, GOLD, (chest.centerx - 3, chest.centery - 5, 6, 5)) 

        return chest


    def Enemy(self):
        enemy = self.enemy
        with_enemy = self.with_enemy
        enemy_speed = 8
        player = self.player
        enemy_size = self.player_size


        if with_enemy:
            pygame.draw.ellipse(win, RED, (enemy.centerx - 30, enemy.centery - 40, 60, 50))
            pygame.draw.circle(win, ORANGE, enemy.center, self.player_size // 2)

            pygame.draw.circle(win, GOLD, (enemy.centerx - 22, enemy.centery - 18), 6) #mushroom spot
            pygame.draw.circle(win, GOLD, (enemy.centerx + 24, enemy.centery - 12), 5) #mushroom spot
            pygame.draw.circle(win, GOLD, (enemy.centerx - 14, enemy.centery - 32), 4) #mushroom spot
            pygame.draw.circle(win, GOLD, (enemy.centerx - 4, enemy.centery - 26), 5) #mushroom spot
            pygame.draw.circle(win, GOLD, (enemy.centerx + 13, enemy.centery - 28), 6) #mushroom spot
            
            pygame.draw.circle(win, BLACK, (enemy.centerx - 10, enemy.centery - 10), 5)
            pygame.draw.circle(win, BLACK, (enemy.centerx + 10, enemy.centery - 10), 5)
            pygame.draw.arc(win, BLACK, (enemy.centerx - 10, enemy.centery - 5, 20, 15), 3.14, 0, 2)

            x_dist = enemy.centerx - player.centerx
            y_dist = enemy.centery - player.centery
            dist = (x_dist ** 2 + y_dist ** 2) ** .5 + 1
            x_vel = x_dist / dist * enemy_speed 
            y_vel = y_dist / dist * enemy_speed

            enemy.centerx -= x_vel
            enemy.centery -= y_vel

            # Prevent the enemy from going above the upper 40px border
            if enemy.y < 40:  # Enforce the 40px border restriction
                enemy.y = 40

            return enemy
        else:
            return None


    def Merchant(self):
        screen_center_x = WIDTH // 2 - 200
        screen_center_y = HEIGHT // 2 - 100

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

        # ----- CHEST COLLISION (always solid) -----
        if new_player_rect.colliderect(self.chest):
            # Cancel movement if hitting chest
            return

        # ----- KEY COLLISION (pushable) -----
        if new_player_rect.colliderect(self.key):
            new_key_rect = self.key.copy()
            new_key_rect.x += move_x * self.player_speed
            new_key_rect.y += move_y * self.player_speed

            can_move_key = (
                0 <= new_key_rect.x <= WIDTH - self.player_size and
                40 <= new_key_rect.y <= HEIGHT - self.player_size
            )

            if can_move_key:
                # Move both player and key
                self.key = new_key_rect
                self.player = new_player_rect
            else:
                # Can't push — block movement
                return
        else:
            # No collision with key → move normally
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
        
        # Generate mushrooms once
        if not self.mushrooms:
            for _ in range(20):
                if self.rect_coords:  # Check if there are still available positions
                    random_rects = random.sample(self.rect_coords, 1)
                    rand_x, rand_y = random_rects[0]
                    x, y = rand_x, rand_y
                    rect = pygame.Rect(x, y, self.mushroom_radius * 2, self.mushroom_radius * 2)
                    self.mushrooms.append(rect)
                    self.rect_coords.remove((rand_x, rand_y))

        # Draw mushrooms
        for m in self.mushrooms:
            pygame.draw.rect(win, BROWN, (m.centerx - 3, m.bottom - 10, 6, 10))  # stem
            pygame.draw.ellipse(win, RED, (m.x, m.y, self.mushroom_radius * 2, self.mushroom_radius))  # cap

            # Calculate direction to move mushroom towards player
            x_dist = m.centerx - self.player.centerx
            y_dist = m.centery - self.player.centery
            dist = (x_dist ** 2 + y_dist ** 2) ** .5 + 1
            x_vel = x_dist / dist * 1
            y_vel = y_dist / dist * 1

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



def Game(level_num):
    config = LEVELS[level_num]
    assets = Assets(config)
    running = True
    score = 0
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
        player = assets.Player()
        control = assets.Control()
        mushrooms, spikes, bad_mushrooms = assets.Mushroom()  # Now always two lists
        enemy = assets.Enemy()
        key = assets.Key()
        chest = assets.Chest()

        if not level_goal_set:
            level_goal = len(mushrooms)  # Set level_goal once when the level starts
            level_goal_set = True  # Set the flag to True, preventing further updates

        # Mushroom collision
        for m in mushrooms[:]:
            if player.colliderect(m):
                mushrooms.remove(m)
                score += 1
                collected += 1




        for b in bad_mushrooms[:]:
            if player.colliderect(b):
                running = False
                Over(3)

        # Spike collision
        for rect in spikes:
            if player.colliderect(rect):
                running = False
                Over(2)

        if enemy and player.colliderect(enemy):
            running = False
            Over(4)

        if key.colliderect(chest):
            assets.chest = None
            assets.key = None



        # Level complete check
        if len(mushrooms) == 0:
            mushroom_inventory = collected
            if not Levels_completed.get(level_num, {}).get("completed", False):
                Levels_completed[level_num] = {"completed": True}
                running = False
                
                if level_num in (1,3,5):
                    # For level 1, skip skin unlock, just go to next level or victory
                    if level_num == max_level:
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


        # HUD Design - Top Line (50px thick)
        # Draw a thin line at the top of the screen
        pygame.draw.rect(win, LINE_COLOR, (0, 0, WIDTH, 40))  # 50px thick line

        # Displaying level, goal, and mushroom collected info
        level_text = font.render(f"LEVEL: {level_num}", True, TEXT_COLOR)
        goal_text = font.render(f"GOAL: {score}/{level_goal}", True, TEXT_COLOR)
        collected_text = font.render(f"MUSHROOMS COLLECTED: {collected}", True, TEXT_COLOR)

        # Positioning the text inside the 50px top line
        # Adjusting the text positions for better alignment within the top strip
        win.blit(level_text, (20, 10))  # Positioning the level text
        win.blit(goal_text, (200, 10))  # Positioning the goal text
        win.blit(collected_text, (400, 10))  # Positioning the collected text

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


class TextBox:
    def __init__(self, text, font, font_color, box_color, padding=10, width=None, height=None, x=0, y=0):
        self.text = text
        self.font = font
        self.font_color = font_color
        self.box_color = box_color
        self.padding = padding
        self.width = width
        self.height = height
        self.x = x
        self.y = y

        # Split into lines
        self.lines = self.text.split("\n")

        # Render each line
        self.text_surfaces = [self.font.render(line, True, self.font_color) for line in self.lines]

        # Find longest line width
        max_line_width = max(surface.get_width() for surface in self.text_surfaces)

        # Calculate box width dynamically
        if self.width is None:
            box_width = max_line_width + 2 * self.padding
        else:
            box_width = max(self.width, max_line_width + 2 * self.padding)

        # Total text height
        total_text_height = sum(surface.get_height() for surface in self.text_surfaces) + (len(self.text_surfaces) - 1) * self.padding

        # Calculate box height dynamically
        if self.height is None:
            box_height = total_text_height + 2 * self.padding
        else:
            box_height = max(self.height, total_text_height + 2 * self.padding)

        # Box rect
        self.box_rect = pygame.Rect(self.x - self.padding, self.y - self.padding, box_width, box_height)

        # Update positions
        self.update_position()

    def update_position(self):
        """Update the position of the text inside the box."""
        self.text_rect_tops = []
        current_y = self.y + self.padding
        for line_surface in self.text_surfaces:
            self.text_rect_tops.append(
                pygame.Rect(self.x + self.padding, current_y, line_surface.get_width(), line_surface.get_height())
            )
            current_y += line_surface.get_height() + self.padding

    def draw(self, screen):
        pygame.draw.rect(screen, self.box_color, self.box_rect)
        for i, line_surface in enumerate(self.text_surfaces):
            screen.blit(line_surface, self.text_rect_tops[i])



def Shop(return_to_level):
    global mushroom_inventory, My_skins, current_skin
    running = True
    assets = Assets(LEVELS[1])
    pygame.event.clear()

    # List of skins you can buy (locked ones)
    purchasable = [sid for sid, data in My_skins.items() if not data["unlocked"]]

    # If nothing to buy, just go to next step
    if not purchasable:
        if return_to_level >= max_level:
            Victory()
        else:
            Game(return_to_level + 1)
        return

    skin_id = purchasable[0]
    skin_name = My_skins[3]["skin"]
    cost = 50

    buy_button = Button(f"Buy ({cost})", WIDTH // 2 - 350, HEIGHT // 2 + 150, 300, 100)
    skip_button = Button("Skip shop", WIDTH // 2 + 50, HEIGHT // 2 + 150, 300, 100)

    previous_skin = current_skin

    while running:
        win.fill(GREEN)
        assets.Merchant()  # Draw merchant in background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buy_button.is_clicked(event.pos) and mushroom_inventory >= cost:
                    mushroom_inventory -= cost
                    My_skins[skin_id]["unlocked"] = True
                    running = False
                    New_skin(skin_id, return_to_level)  # Go to equip/add screen
                    return
                elif skip_button.is_clicked(event.pos):
                    running = False
                    if return_to_level >= max_level:
                        Victory()
                    else:
                        Game(return_to_level + 1)
                    return

        buy_button.draw(win)
        skip_button.draw(win)

        # Text box with offer
        text_box = TextBox(
            f"I can sell you this\n   skin for {cost}\n",
            font_medium, BLACK, GRAY, padding=10, width=300, height=200,
            x=460, y=100
        )
        text_box.draw(win)

        # Draw wooden stand / shop graphics (same as before)
        pygame.draw.rect(win, BROWN, (90, 100, 220, 40))
        pygame.draw.rect(win, BROWN, (120, 140, 30, 100))
        pygame.draw.rect(win, BROWN, (250, 140, 30, 100))
        pygame.draw.rect(win, BROWN, (70, 240, 260, 60))

        pygame.draw.ellipse(win, BROWN, (668, 185, 40, 30))  # cap
        pygame.draw.ellipse(win, RED, (663, 160, 50, 35))  # cap
        for cx, cy in [(668, 182), (669, 174), (676, 188), (676, 168),
                       (680, 178), (708, 178), (688, 188), (699, 185),
                       (690, 179), (688, 169), (705, 170), (697, 170)]:
            pygame.draw.circle(win, WHITE, (cx, cy), 3)

        # Preview the new skin on player in center
        current_skin_backup = current_skin
        current_skin = skin_name
        assets.player.center = (WIDTH // 2 + 200, HEIGHT // 2 - 55)
        assets.Player()
        current_skin = current_skin_backup

        pygame.display.flip()
        clock.tick(60)



def New_skin(skin_id, return_to_level):
    global current_skin, My_skins
    running = True
    assets = Assets(LEVELS[1])  # or any config you want
    previous_skin = current_skin
    new_skin_name = My_skins[skin_id]["skin"]

    equip_button = Button("Equip", WIDTH // 2 - 350, HEIGHT // 2 + 150, 300, 100)
    add_button = Button("Add to collection", WIDTH // 2 + 50, HEIGHT // 2 + 150, 300, 100)

    while running:
        win.fill(GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if equip_button.is_clicked(event.pos):
                    current_skin = new_skin_name
                    running = False
                elif add_button.is_clicked(event.pos):
                    current_skin = previous_skin
                    running = False

        equip_button.draw(win)
        add_button.draw(win)

        menu_text = font_large.render(f"New skin unlocked: {new_skin_name}", True, BLACK)
        win.blit(menu_text, menu_text.get_rect(center=(WIDTH // 2, 100)))

        # Temporarily set current_skin to new skin for preview
        current_skin_backup = current_skin
        current_skin = new_skin_name

        # Position player
        assets.player.center = (WIDTH // 2, HEIGHT // 2)
        assets.Player()  # This draws the player with the current_skin on the win surface

        # Restore current_skin in case it changed elsewhere
        current_skin = current_skin_backup

        pygame.display.flip()
        clock.tick(60)

    # Continue to next level or victory
    if return_to_level >= max_level:
        Victory()
    else:
        Game(return_to_level + 1)



def Skin_menu():
    running = True
    pos = 1
    assets = Assets(LEVELS[1])
    global current_skin
    global My_skins
    previous_skin = current_skin
    prev_button = Button("Previous", WIDTH // 2 - 350, HEIGHT // 2 + 150, 150, 100)
    next_button = Button("Next", WIDTH // 2 + 200, HEIGHT // 2 + 150, 150, 100)
    back_button = Button("Back", WIDTH // 2 - 75, HEIGHT // 2 + 150, 150, 100)
    pygame.event.clear()

    # Find the current position based on the current_skin
    def find_current_pos(current_skin, skins):
        for key, value in skins.items():
            if value["skin"] == current_skin:
                return key
        return 1  # Default to 1 if the skin is not found (shouldn't happen)

    # Get the initial position based on current_skin
    pos = find_current_pos(current_skin, My_skins)

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
        if My_skins[pos]["unlocked"]:
            current_skin = My_skins[pos]["skin"]
        else:
            current_skin = "none"  # If not unlocked, reset to "none"

        # Draw buttons
        prev_button.draw(win)  
        next_button.draw(win)  
        back_button.draw(win) 

        # Draw menu text
        menu_text = font_large.render("Select your skin", True, BLACK)
        win.blit(menu_text, menu_text.get_rect(center=(WIDTH // 2, 100)))

        # Position player in center and draw the selected skin
        assets.player.x = WIDTH // 2 - assets.player_size // 2
        assets.player.y = HEIGHT // 2 - assets.player_size // 2
        player = assets.Player()

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS


def Next_level(current_level):
    global mushroom_inventory
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
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        running = False  # always stop the loop on space

                        # Shop check first
                        if current_level >= 3 and mushroom_inventory >= 50:
                            Shop(current_level)
                            break  # shop handles what happens next

                        # Then victory check
                        if current_level == max_level:
                            Victory()
                            break

                        # Otherwise go to next level
                        Game(current_level + 1)
                        break
    
 

def Over(current_level):
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
                        Game(current_level)                 



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

