# Assets methods (only the parts we change)
class Assets:
    def __init__(self, config):
        ...
        self.key = pygame.Rect(690, 100, 18, 50)
        self.chest = pygame.Rect(678, 400, self.player_size, self.player_size)
        ...

    def Key(self):
        # Safe draw (no error if key has been removed)
        if not self.key:
            return None
        k = self.key
        pygame.draw.circle(win, GOLD, (k.centerx, k.top + 10), self.player_size // 5)
        pygame.draw.rect(win, GOLD, (k.centerx - 3, k.y + 16, 6, 30)) 
        pygame.draw.rect(win, GOLD, (k.centerx - 9, k.bottom - 6, 12, 6))
        pygame.draw.rect(win, GOLD, (k.centerx - 9, k.bottom - 18, 12, 6))
        return k

    def Chest(self):
        # Safe draw
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

    def Control(self):
        keys = pygame.key.get_pressed()
        ...
        # compute move_x, move_y, normalize, new_player_rect as before
        new_player_rect = self.player.copy()
        new_player_rect.x += move_x * self.player_speed
        new_player_rect.y += move_y * self.player_speed

        # --- CHEST is always solid: cancel move if we would hit it
        if self.chest and new_player_rect.colliderect(self.chest):
            # blocked by chest
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
                    # move player into the spot (optional)
                    self.player = new_player_rect
                else:
                    # blocked: do nothing (player doesn't move)
                    return
        else:
            # No key collision: normal move allowed
            self.player = new_player_rect

        # Keep player in bounds as you had before...
        ...



For GAME()
while running:
    ...
    win.fill(assets.level_color)
    player = assets.Player()
    assets.Control()            # this updates assets.player and assets.key if pushed
    mushrooms, spikes, bad_mushrooms = assets.Mushroom()
    enemy = assets.Enemy()

    # Draw key/chest safely (these return None if removed)
    assets.Key()
    assets.Chest()

    # If you still want to check key & chest collision here (redundant if done in Control),
    # do it using assets.key / assets.chest and guard for None:
    if assets.key and assets.chest and assets.key.colliderect(assets.chest):
        assets.key = None
        assets.chest = None

    ...
    pygame.display.flip()
    clock.tick(60)