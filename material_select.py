import pygame
import pygame_menu
from pygame_menu.widgets.widget.dropselect import DropSelect
from game_assets import icon_images

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Load images (replace 'path_to_image' with actual paths to your images)
images = {
    'a': icon_images[0],
    'b': icon_images[1],
    'c': icon_images[2]
}

# Variable to keep track of the current image key ('a', 'b', or 'c')
current_image_key = 'a'

# Function to change the current image based on the dropdown selection
def change_image(selected, value):
    global current_image_key
    current_image_key = value
    print(f"Selected: {selected} - {value}")

# Set up pygame-menu
menu = pygame_menu.Menu('Menu Example', 800, 600, theme=pygame_menu.themes.THEME_BLUE)

dropdown: DropSelect = menu.add.dropselect('Select Option:', [('a', 'a'), ('b', 'b'), ('c', 'c')], onchange=change_image)
dropdown.set_font("arial", 12, (0, 0, 0), (100, 100, 100), (200, 200, 200), (200, 200, 200), (255, 255, 0))
menu.add.text_input('Name :', default='John Doe')
# Note: Pygame-menu doesn't directly support image widgets, so we handle image display in the Pygame loop.

# Main loop
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Update and draw the menu
    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)
    else:
        # If not in menu, display the current image
        screen.fill((0, 0, 0))  # Clear screen
        screen.blit(images[current_image_key], (250, 150))  # Draw the current image

    pygame.display.update()
    clock.tick(60)  # Cap at 60 FPS

pygame.quit()
