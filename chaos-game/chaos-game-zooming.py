import pygame
import math
import random

pygame.init()

width, height = 550, 550
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Fractal Pattern')

white = (255, 255, 255)
blue = (50, 50, 250)
black = (0, 0, 0)

font = pygame.font.SysFont(None, 24)

def gen_new_point(last_point, target_point, coeff):
    new_x = last_point[0] + (target_point[0] - last_point[0]) * coeff
    new_y = last_point[1] + (target_point[1] - last_point[1]) * coeff
    return (new_x, new_y)

def setup(vertex_count):
    unit = 250
    rotation = math.pi * (1 / vertex_count + 0.5)

    vertexes = [
        (
            math.cos(2 * math.pi / vertex_count * i + rotation) * unit,
            math.sin(2 * math.pi / vertex_count * i + rotation) * unit
        )
        for i in range(vertex_count)
    ]

    return vertexes

def zoom_points(points, zoom_factor, offset_x, offset_y):
    return [
        ((point[0] - offset_x) * zoom_factor + width / 2, (point[1] - offset_y) * zoom_factor + height / 2)
        for point in points
    ]

def main():
    running = True
    generating = True
    vertex_count = 4
    vertexes = setup(vertex_count)
    last_point = [0, 0]
    frame_count = 0
    erase = False
    coeff = 2 / 3
    points = []
    draw_points = []

    zoom_factor = 1.0
    offset_x = 0
    offset_y = 0

    draw_surface = pygame.Surface((width, height))
    draw_surface.fill(white)

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in {4, 5} or event.button == 1:  # Scroll up, Scroll down or Left click
                    generating = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in {4, 5} or event.button == 1:  # Scroll up, Scroll down or Left click
                    generating = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    generating = not generating

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    zoom_factor *= 1.1
                    erase = True
                elif event.button == 5:  # Scroll down
                    zoom_factor /= 1.1
                    erase = True
                elif event.button == 1:  # Left click
                    offset_x += (event.pos[0] - width / 2) / zoom_factor
                    offset_y += (event.pos[1] - height / 2) / zoom_factor
                    erase = True

        if erase:
            draw_surface.fill(white)
            erase = False
            draw_points = zoom_points(points, zoom_factor, offset_x, offset_y)
            for point in draw_points:
                pygame.draw.circle(draw_surface, blue, (int(point[0]), int(point[1])), 1)  # 1 makes the dot size one

        if generating:
            for _ in range(1000):
                choice = random.random()
                if choice < 0.8:  # 80% chance to move towards a vertex
                    v_index = random.randint(0, vertex_count - 1)
                    target_point = vertexes[v_index]
                else:  # 20% chance to move towards the center
                    target_point = [0, 0]

                last_point = gen_new_point(last_point, target_point, coeff)
                points.append(last_point)
                screen_point = ((last_point[0] - offset_x) * zoom_factor + width / 2, 
                                (last_point[1] - offset_y) * zoom_factor + height / 2)
                pygame.draw.circle(draw_surface, blue, (int(screen_point[0]), int(screen_point[1])), 1)

        window.blit(draw_surface, (0, 0))

        # Draw the shape outline with offset and zoom applied
        for i in range(len(vertexes)):
            pygame.draw.line(window, black,
                             ((vertexes[i][0] - offset_x) * zoom_factor + width / 2, 
                              (vertexes[i][1] - offset_y) * zoom_factor + height / 2),
                             ((vertexes[(i + 1) % len(vertexes)][0] - offset_x) * zoom_factor + width / 2,
                              (vertexes[(i + 1) % len(vertexes)][1] - offset_y) * zoom_factor + height / 2))

        vertex_text = font.render(f'Vertex Count: {vertex_count}', True, black)
        window.blit(vertex_text, (10, 10))

        pygame.display.flip()

        frame_count += 1

        pygame.time.delay(10)

    pygame.quit()

if __name__ == "__main__":
    main()
