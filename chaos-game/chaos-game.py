import pygame
import random
import sys
import datetime

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chaos Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Vertex and point lists
vertexes = [(400, 100), (200, 500), (600, 500)]
points = []

# Function to draw everything
def draw():
    window.fill(WHITE)
    
    # Draw vertexes
    for vertex in vertexes:
        pygame.draw.circle(window, RED, vertex, 5)
    
    # Draw points
    for point in points:
        pygame.draw.circle(window, BLACK, point, 1)

    pygame.display.flip()

# Function to generate the next point
def generate_point():
    if not points:
        return random.choice(vertexes)
    last_point = points[-1]
    next_vertex = random.choice(vertexes)
    new_point = ((last_point[0] + next_vertex[0]) // 2, (last_point[1] + next_vertex[1]) // 2)
    return new_point

# Function to save the current screen as an image
def save_image():
    current_time = datetime.datetime.now().strftime("%H_%M_%S")
    filename = f"chaos-game/gen-imgs/{current_time}.png"
    pygame.image.save(window, filename)
    print(f"Image saved as {filename}")

    

# Main loop
running = True
moving_vertex = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                for i, vertex in enumerate(vertexes):
                    if pygame.Rect(vertex[0]-5, vertex[1]-5, 10, 10).collidepoint(event.pos):
                        moving_vertex = i
                        break
            elif event.button == 3:  # Right click
                vertexes.append(event.pos)
                points = []  # Reset points
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                moving_vertex = None
        elif event.type == pygame.MOUSEMOTION:
            if moving_vertex is not None:
                vertexes[moving_vertex] = event.pos
                points = []  # Reset points
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_image()

    # Generate new points
    if len(points) < 3*10**5:  # Limit the number of points for performance
        for _ in range(100):
            points.append(generate_point())

    # Draw everything
    draw()

# Quit Pygame
pygame.quit()
sys.exit()
