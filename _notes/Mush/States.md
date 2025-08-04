---
title: States
date: 2025-08-04 
feed: show

---
Для програмістів

```
import os, time, pygame
# Load our scenes
from states.title import Title

class Game():
        def __init__(self):
            pygame.init()
            self.GAME_W,self.GAME_H = 480, 270
            self.SCREEN_WIDTH,self.SCREEN_HEIGHT = 960, 540
            self.game_canvas = pygame.Surface((self.GAME_W,self.GAME_H))
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
            self.running, self.playing = True, True
            self.actions = {"left": False, "right": False, "up" : False, "down" : False, "action1" : False, "action2" : False, "start" : False}
            self.dt, self.prev_time = 0, 0
            self.state_stack = []
            self.load_assets()
            self.load_states()

        def game_loop(self):
            while self.playing:
                self.get_dt()
                self.get_events()
                self.update()
                self.render()

        def get_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.playing = False
                        self.running = False
                    if event.key == pygame.K_a:
                        self.actions['left'] = True
                    if event.key == pygame.K_d:
                        self.actions['right'] = True
                    if event.key == pygame.K_w:
                        self.actions['up'] = True
                    if event.key == pygame.K_s:
                        self.actions['down'] = True
                    if event.key == pygame.K_p:
                        self.actions['action1'] = True
                    if event.key == pygame.K_o:
                        self.actions['action2'] = True    
                    if event.key == pygame.K_RETURN:
                        self.actions['start'] = True  

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.actions['left'] = False
                    if event.key == pygame.K_d:
                        self.actions['right'] = False
                    if event.key == pygame.K_w:
                        self.actions['up'] = False
                    if event.key == pygame.K_s:
                        self.actions['down'] = False
                    if event.key == pygame.K_p:
                        self.actions['action1'] = False
                    if event.key == pygame.K_o:
                        self.actions['action2'] = False
                    if event.key == pygame.K_RETURN:
                        self.actions['start'] = False  

        def update(self):
            self.state_stack[-1].update(self.dt,self.actions)

        def render(self):
            self.state_stack[-1].render(self.game_canvas)
            # Render current state to the screen
            self.screen.blit(pygame.transform.scale(self.game_canvas,(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0,0))
            pygame.display.flip()


        def get_dt(self):
            now = time.time()
            self.dt = now - self.prev_time
            self.prev_time = now

        def draw_text(self, surface, text, color, x, y):
            text_surface = self.font.render(text, True, color)
            #text_surface.set_colorkey((0,0,0))
            text_rect = text_surface.get_rect()
            text_rect.center = (x, y)
            surface.blit(text_surface, text_rect)

        def load_assets(self):
            # Create pointers to directories 
            self.assets_dir = os.path.join("assets")
            self.sprite_dir = os.path.join(self.assets_dir, "sprites")
            self.font_dir = os.path.join(self.assets_dir, "font")
            self.font= pygame.font.Font(os.path.join(self.font_dir, "PressStart2P-vaV7.ttf"), 20)

        def load_states(self):
            self.title_screen = Title(self)
            self.state_stack.append(self.title_screen)

        def reset_keys(self):
            for action in self.actions:
                self.actions[action] = False


if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()
```

Шаблон для непрограмістів

```
import sys
import pygame as pg


class Game(object):
    """
    A single instance of this class is responsible for 
    managing which individual game state is active
    and keeping it updated. It also handles many of
    pygame's nuts and bolts (managing the event 
    queue, framerate, updating the display, etc.). 
    and its run method serves as the "game loop".
    """
    def __init__(self, screen, states, start_state):
        """
        Initialize the Game object.
        
        screen: the pygame display surface
        states: a dict mapping state-names to GameState objects
        start_state: name of the first active game state 
        """
        self.done = False
        self.screen = screen
        self.clock = pg.time.Clock()
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]
        
    def event_loop(self):
        """Events are passed for handling to the current state."""
        for event in pg.event.get():
            self.state.get_event(event)
            
    def flip_state(self):
        """Switch to the next game state."""
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)
    
    def update(self, dt):
        """
        Check for state flip and update active state.
        
        dt: milliseconds since last frame
        """
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()    
        self.state.update(dt)
        
    def draw(self):
        """Pass display surface to active state for drawing."""
        self.state.draw(self.screen)
        
    def run(self):
        """
        Pretty much the entirety of the game's runtime will be
        spent inside this while loop.
        """ 
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()
            
            
class GameState(object):
    """
    Parent class for individual game states to inherit from. 
    """
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pg.display.get_surface().get_rect()
        self.persist = {}
        self.font = pg.font.Font(None, 24)
        
    def startup(self, persistent):
        """
        Called when a state resumes being active.
        Allows information to be passed between states.
        
        persistent: a dict passed from state to state
        """
        self.persist = persistent        
        
    def get_event(self, event):
        """
        Handle a single event passed by the Game object.
        """
        pass
        
    
    def update(self, dt):
        """
        Update the state. Called by the Game object once
        per frame. 
        
        dt: time since last frame
        """
        pass
        
    def draw(self, surface):
        """
        Draw everything to the screen.
        """
        pass
        
        
class SplashScreen(GameState):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.title = self.font.render("Splash Screen", True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = "black"
        self.next_state = "GAMEPLAY"
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            self.persist["screen_color"] = "gold"
            self.done = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.persist["screen_color"] = "dodgerblue"
            self.done = True
    
    def draw(self, surface):
        surface.fill(pg.Color("black"))
        surface.blit(self.title, self.title_rect)        
    
    
class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.rect = pg.Rect((0, 0), (128, 128))
        self.x_velocity = 1
        
    def startup(self, persistent):
        self.persist = persistent
        color = self.persist["screen_color"]
        self.screen_color = pg.Color(color)
        if color == "dodgerblue":
            text = "You clicked the mouse to get here"
        elif color == "gold":
            text = "You pressed a key to get here"
        self.title = self.font.render(text, True, pg.Color("gray10"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.title_rect.center = event.pos
        
    def update(self, dt):
        self.rect.move_ip(self.x_velocity, 0)
        if (self.rect.right > self.screen_rect.right
            or self.rect.left < self.screen_rect.left):
            self.x_velocity *= -1
            self.rect.clamp_ip(self.screen_rect)
                 
    def draw(self, surface):
        surface.fill(self.screen_color)
        surface.blit(self.title, self.title_rect)
        pg.draw.rect(surface, pg.Color("darkgreen"), self.rect)
        
    
if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((1280, 720))
    states = {"SPLASH": SplashScreen(),
                   "GAMEPLAY": Gameplay()}
    game = Game(screen, states, "SPLASH")
    game.run()
    pg.quit()
    sys.exit()
```
