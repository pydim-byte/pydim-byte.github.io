---
title: Main loop
date: 2025-08-03
feed: show
---
```
# завантажуємо бібліотеку pygame
import pygame 

# Задаємо значення кольорам
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (100, 255, 50)
RED = (255, 0, 0)
 
pygame.init()

# Екран
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

#Задаємо FPS грі 
clock = pygame.time.Clock()


# Цикл гри
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((GREEN))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

```

