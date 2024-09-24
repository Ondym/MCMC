import pygame
import math
import random
import os, re
from additional_funcs import *
import matplotlib.pyplot as plt

# user_auto_save = input("Save the images automatically? [y/n]: ")

pygame.init()

width, height = 550, 550
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Fractal Pattern')

opacity = 15

darkness_index = 1
bg_color = (255 * darkness_index, 255 * darkness_index, 255 * darkness_index)
translucent = (255, 150, 0, opacity)
fg_color = (255 - bg_color[0], 255 - bg_color[1], 255 - bg_color[2])

# point_surface = pygame.Surface((1, 1), pygame.SRCALPHA)
# point_surface.fill(translucent)

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

def last_dir(directory):
    highest_number = None
    pattern = re.compile(r'^ext_rul_(\d+)$')

    for subdir in os.listdir(directory):
        match = pattern.match(subdir)
        if match:
            number = int(match.group(1))
            if highest_number is None or number > highest_number:
                highest_number = number

    return highest_number

def get_color(value, colormap='viridis'):
    cmap = plt.get_cmap(colormap)
    return cmap(value)

def main():
    running = True
    window.fill(bg_color)
    vertex_count = 3
    last_point = [0, 0]
    v_index = 0
    frame_count = 0
    erase = False
    auto_save = False#user_auto_save == "y"
    coeff = 1/3
    render_edges = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    save_image(vertex_count, coeff, session_id, window, opc=opacity)
                if event.key == pygame.K_p:
                    print(last_point)

        if frame_count % 120 == 0:
            if (frame_count > 0):
                vertex_count += 1
                if auto_save:
                    save_image(vertex_count, coeff, session_id, window, opc=opacity)

            vertexes = setup(vertex_count)
            # coeff += 0.02
            # coeff = opt_r(vertex_count)
            last_point = list(vertexes[0])
            window.fill(bg_color) # TOHLE SE KLIDNE MUZE SMAZAT A NASTAVIT erase=True, rozdil je ocividny

            if (frame_count == 0 or True):
                colors = []
                colors.append(pygame.Surface((1, 1), pygame.SRCALPHA))
                colors[0].fill(translucent)
                
                ##### This changes the color of each generated point to visualize, which vertex was chosen for that particular point #####
                # for i in range(vertex_count):
                #     colors.append(pygame.Surface((1, 1), pygame.SRCALPHA))
                #     C = get_color(i/(vertex_count - 1))
                #     C = (int(C[0] * 255), int(C[1] * 255), int(C[2] * 255), int(opacity))
                #     colors[i].fill(C)

            vertex_text = font.render(f'Vertex Count: {vertex_count}', True, fg_color)
            coeff_text = font.render(f'Coefficient: {coeff:.3g}', True, fg_color)
            window.blit(vertex_text, (10, 10))
            window.blit(coeff_text, (10, 27))
    
            # this is just so the images look more centered
            offset_y = 80 * (vertex_count%2) * (2**int(-vertex_count/2))

        if erase:
            window.fill(bg_color)

        for _ in range(15000):
            v_index = (v_index + random.randint(-1, 1)) % len(vertexes) #################### THE RULE #####################
            last_point = gen_new_point(last_point, vertexes[v_index], coeff)
            window.blit(colors[min(len(colors)-1, v_index)], (int(last_point[0] + width / 2), int(last_point[1] + height / 2 + offset_y)))

        if (render_edges):
            for i in range(len(vertexes)):
                pygame.draw.line(window, (120, 120, 120),
                                (vertexes[i][0] + width / 2, vertexes[i][1] + height / 2 + offset_y),
                                (vertexes[(i + 1) % len(vertexes)][0] + width / 2, vertexes[(i + 1) % len(vertexes)][1] + height / 2 + offset_y))

        pygame.display.flip()

        frame_count += 1

        pygame.time.delay(10)

    pygame.quit()

session_id = last_dir("chaos-game/gen-imgs") + 1
# viridis = mpl.colormaps['viridis'].resampled(8)

if __name__ == "__main__":
    main()