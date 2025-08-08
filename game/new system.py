import pygame
import sys

# --- Level configurations ---
LEVELS = {
    1: {"with_spikes": True, "enemy_count": 3, "time_limit": 60, "skin_type": "red_rect"},
    2: {"with_spikes": True, "enemy_count": 5, "time_limit": 50, "skin_type": "blue_circle"},
}

# Initialize Pygame & global screen
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Mushroom Collector")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# --- Assets class ---
class Assets:
    def __init__(self, config):
        self.with_spikes = config.get("with_spikes", False)
        self.enemy_count = config.get("enemy_count", 0)
        self.time_limit = config.get("time_limit", 60)
        self.skin_type = config.get("skin_type", "red_rect")

    def spike_skins(self):
        """Defines all spike shapes and returns them as a dict."""
        return {
            "red_rect": lambda: pygame.draw.rect(screen, (200, 0, 0), (300, 200, 40, 40)),
            "blue_circle": lambda: pygame.draw.circle(screen, (0, 0, 200), (320, 220), 20),
        }

    def draw_spikes(self):
        """Draw spikes if this level has them."""
        if self.with_spikes:
            skins = self.spike_skins()
            draw_func = skins.get(self.skin_type)
            if draw_func:
                draw_func()

# --- Game loop ---
def GameLoop(level_num):
    config = LEVELS[level_num]
    assets = Assets(config)

    # Player rectangle
    player = pygame.Rect(50, 50, 40, 40)
    player_speed = 5

    start_ticks = pygame.time.get_ticks()

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player.x += player_speed
        if keys[pygame.K_UP]:
            player.y -= player_speed
        if keys[pygame.K_DOWN]:
            player.y += player_speed

        # Calculate remaining time
        elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = max(0, assets.time_limit - elapsed_seconds)
        if remaining_time <= 0:
            running = False  # End level when time is up

        # Draw everything
        screen.fill((30, 30, 30))

        # Draw player
        pygame.draw.rect(screen, (0, 200, 0), player)

        # Draw spikes via Assets method
        assets.draw_spikes()

        # Info text
        info = f"Level {level_num} | Spikes: {assets.with_spikes} | Enemies: {assets.enemy_count} | Time: {remaining_time}"
        text_surface = font.render(info, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        pygame.display.flip()
        clock.tick(60)

# --- Test run ---
if __name__ == "__main__":
    GameLoop(2)
