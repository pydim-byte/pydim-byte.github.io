---
title: ReFactor
date: 2025-08-04
feed: show
---
```
import pygame

import sys

  

class Game():

    def __init__(self, W, H, screen, colors, text, states, start_state):

        pygame.init()

        self.done = False

        self.W,self.H = W, H

        W, H = 800, 600

        self.screen = screen

        self.game_canvas = pygame.Surface((W, H))

        self.colors = colors

        colors = {

            "WHITE": (255, 255, 255),

            "BLACK": (0, 0, 0),

            "BLUE": (50, 150, 255),

            "GRAY": (180, 180, 180),

            "GREEN": (100, 200, 0)}

        self.text = text

        text ={

            "font_large": pygame.font.SysFont("arial", 60),

            "font_medium": pygame.font.SysFont("arial", 40)}

        self.running, self.playing = True, True

        self.dt, self.prev_time = 0, 0

        self.states = states

        self.state_name = start_state

        self.state = self.states[self.state_name]

  

    def event_loop(self):

    #Events are passed for handling to the current state.

        for event in pygame.event.get():

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

    # Check for state flip and update active state.dt: milliseconds since last frame

        if self.state.quit:

            self.done = True

        elif self.state.done:

            self.flip_state()    

        self.state.update(dt)

    def draw(self):

    #Pass display surface to active state for drawing.

        self.state.draw(self.screen)

    def run(self):

    # Pretty much the entirety of the game's runtime will be spent inside this while loop.

        while not self.done:

            dt = self.clock.tick(self.fps)

            self.event_loop()

            self.update(dt)

            self.draw()

            pygame.display.update()

  

class GameState(object):

    """

    Parent class for individual game states to inherit from.

    """

    def __init__(self):

        self.done = False

        self.quit = False

        self.next_state = None

        self.screen_rect = pygame.display.get_surface().get_rect()

        self.persist = {}

        self.font = pygame.font.Font(None, 24)

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

  
  
  

class Button(GameState):

    def __init__(self, text, x, y, width, height):

        self.text = text

        self.rect = pygame.Rect(x, y, width, height)

  

    def draw(self, screen):

        pygame.draw.rect(screen, Game.colors["GRAY"], self.rect)

        text_surface = Game.text["font_medium"].render(self.text, True, Game.colors["BLACK"])

        text_rect = text_surface.get_rect(center=self.rect.center)

        screen.blit(text_surface, text_rect)

  

    def is_clicked(self, pos):

        return self.rect.collidepoint(pos)

  
  
  
  
  
  
  

class Menu(GameState):

    def __init__(self):

        play_button = Button("Play", Game.W // 2 - 100, Game.H // 2 - 50, 200, 60)

        quit_button = Button("Quit", Game.W // 2 - 100, Game.H // 2 + 30, 200, 60)

        running = True

        while running:

                for event in pygame.event.get():

                    mouse_pos = event.pos

                    if play_button.is_clicked(mouse_pos):

                        Gameplay()

                    elif quit_button.is_clicked(mouse_pos):

                        running = False

  

                menu_text = Game.text["font_medium"].render("Main Menu", True, Game.colors["BLACK"])

                Game.screen.blit(menu_text, menu_text.get_rect(center=(Game.W // 2, 100)))

                play_button.draw(Game.screen)

                quit_button.draw(Game.screen)

  
  
  
  
  

class Gameplay(GameState):

    def __init__(self):

        pass

  
  

if __name__ == "__Factor__":

    pygame.init()

    screen = pygame.display.set_mode((1280, 720))

    states = {"MENU": Menu(),

                   "GAMEPLAY": Gameplay()}

    game = Game(screen, states, "MENU")

    game.run()

    pygame.quit()

    sys.exit()
```