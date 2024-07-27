import pygame
import random

# Pygame initialization
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [
    (156, 11, 33),
    (50, 201, 44),
    (204, 188, 12),
    (10, 39, 145),
]

# Setting up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Barnsley Fern")

# Function to transform coordinates to screen space
def transform(x, y):
    return int(WIDTH / 2 + x * WIDTH / 8), int(HEIGHT - y * HEIGHT / 8 - 50)

# Barnsley fern IFS probabilities and transformations
probabilities = [0.02, 0.84, 0.07]

def barnsley_fern(x, y):
    r = random.random()
    c = -1
    # print(probabilities[0], sum(probabilities[:2]), sum(probabilities))
    if r < probabilities[0]:
        x, y = 0, 0.25 * y
        c = 0
    elif r < sum(probabilities[:2]):
        x, y = 0.95 * x + 0.002 * y, -0.002 * x + 0.93 * y - 0.002 + 0.5
        c = 1
    elif r < sum(probabilities):
        x, y = 0.035 * x - 0.11 * y, 0.27 * x + 0.01 * y - 0.05 + 0.005
        c = 2
    else:
        x, y = -0.04 * x + 0.11 * y, 0.27 * x + 0.01 * y + 0.047 + 0.06
        c = 3
    return x, y, c

def main():
    # Initial coordinates
    x, y = 0, 0

    # Main loop
    running = True

    frm = 0

    screen.fill(WHITE)
    while running:
        frm+=1

        if (frm in [50000]):
            pygame.image.save(screen, f"fern-evolution/{frm}.png")
        


        # Generate points and plot them
        for _ in range(100):
            x, y, c = barnsley_fern(x, y)
            screen_x, screen_y = transform(x, y)
            screen.set_at((screen_x, screen_y), COLORS[c])

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
