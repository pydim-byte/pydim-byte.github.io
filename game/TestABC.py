import pygame

# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("TextBox with Adjustable Width and Height")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Set up font
font = pygame.font.SysFont('Arial', 30)

# TextBox class with adjustable width and height
class TextBox:
    def __init__(self, text, font, font_color, box_color, padding=10, width=None, height=None, x=0, y=0):
        # Store the text and colors
        self.text = text
        self.font = font
        self.font_color = font_color
        self.box_color = box_color
        self.padding = padding
        self.width = width  # Custom width for the box (None for dynamic width)
        self.height = height  # Custom height for the box (None for dynamic height)
        self.x = x
        self.y = y

        # Split the text into lines
        self.lines = self.text.split("\n")
        
        # Create a list of text surfaces for each line
        self.text_surfaces = [self.font.render(line, True, self.font_color) for line in self.lines]
        
        # Calculate the width of the box based on the longest line (or custom width)
        max_line_width = max(surface.get_width() for surface in self.text_surfaces)
        
        if self.width:
            # Use the specified width, but keep the longest line's height
            box_width = self.width
        else:
            # Automatically adjust width to fit the longest line
            box_width = max_line_width + 2 * self.padding
        
        # Calculate total height based on the number of lines and their heights
        total_text_height = sum(surface.get_height() for surface in self.text_surfaces) + (len(self.text_surfaces) - 1) * self.padding
        if self.height:
            # Use the specified height, but keep the longest line's width
            box_height = self.height
        else:
            # Automatically adjust height based on the lines
            box_height = total_text_height + 2 * self.padding

        # Define the box rect based on width and height
        self.box_rect = pygame.Rect(self.x - self.padding, self.y - self.padding, box_width, box_height)

        # Update text positioning
        self.update_position()

    def update_position(self):
        """Update the position of the text and the surrounding box."""
        self.text_rect_tops = []
        current_y = self.y + self.padding
        for line_surface in self.text_surfaces:
            self.text_rect_tops.append(pygame.Rect(self.x + self.padding, current_y, line_surface.get_width(), line_surface.get_height()))
            current_y += line_surface.get_height() + self.padding  # Move down for the next line

    def draw(self, screen):
        # Draw the box (background rectangle)
        pygame.draw.rect(screen, self.box_color, self.box_rect)

        # Draw each line of text in the box
        for i, line_surface in enumerate(self.text_surfaces):
            screen.blit(line_surface, self.text_rect_tops[i])


   ### STOP


# Create an instance of the TextBox class with adjustable width and height
text_box = TextBox("This is a line.\nThis is another line.\nAnd a third line!", font, BLACK, BLUE, padding=10, width=300, height=120, x=50, y=50)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color
    screen.fill(WHITE)

    # Draw the TextBox
    text_box.draw(screen)

    # Update the screen
    pygame.display.flip()

# Quit pygame
pygame.quit()
