import pygame
import math
import random
import os, re
from additional_funcs import *
import matplotlib.pyplot as plt

"""
 Tohle je program simulujici chaos game (https://en.wikipedia.org/wiki/Chaos_game), coz je generalizovana verze
 naseho Sierpinskiho trojuhelniku. Jelikoz je mnoho verzi chaos game a zalezi, cim se bude ridit (pocet vertexu,
 koeficient lerpu, pravidlo vybirani vrcholu...), vsechno je na ty strance na Wikipedii.

 Muzete se pokusit o nejaky zakladni zmeny parametru, treba ve funkci setup(), nebo o pravidlo vyberu vrcholu na 
 radku 74 (v_index), ale pokud si nejste uplne jisty a nebo chcete aby to bylo/nebylo nejak animovany, urcite doporucuju
 proste to zkopirovat a napsat ChatGPT, protoze tak jsem delal animace ja kdyz jsem je chtel nejak videt. Kdyby jste chteli
 nejakou inspiraci, tak ja jsem se treba koukal jak se to meni s poctem vrcholu, koeficientem lerpu (doporucuju menit
 ho, snizit pocet bodu generovanych v kazdym kole a nastavit erase=False)...
"""

# user_auto_save = input("Save the images automatically? [y/n]: ")

pygame.init()

width, height = 550, 550
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Fractal Pattern')

opacity = 255

white = (255, 255, 255)
translucent = (250, 180, 50, opacity)
black = (0, 0, 0)

# point_surface = pygame.Surface((1, 1), pygame.SRCALPHA)
# point_surface.fill(translucent)

font = pygame.font.SysFont(None, 24)

def gen_new_point(last_point, target_point, coeff):
    new_x = last_point[0] + (target_point[0] - last_point[0]) * coeff
    new_y = last_point[1] + (target_point[1] - last_point[1]) * coeff
    return (new_x, new_y)

def setup(vertex_count):
    unit = 5
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
    window.fill(white)
    vertex_count = 3
    last_point = [0, 0]
    v_index = 0
    frame_count = 0
    erase = False
    auto_save = False#user_auto_save == "y"
    coeff = 0.1

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    save_image(vertex_count, coeff, session_id, window, opc=opacity)

        if frame_count % 5000000 == 0:
            if (frame_count > 0):
                # vertex_count += 1
                if auto_save:
                    save_image(vertex_count, coeff, session_id, window, opc=opacity)

            vertexes = setup(vertex_count)
            # coeff += 0.02
            # coeff = opt_r(vertex_count)
            last_point = list(vertexes[0])
            window.fill(white) # TOHLE SE KLIDNE MUZE SMAZAT A NASTAVIT erase=True, rozdil je ocividny

            if (frame_count == 0 or True):
                colors = []
                
                for i in range(1):
                    colors.append(pygame.Surface((2, 2), pygame.SRCALPHA))
                    C = get_color(i/(vertex_count - 1))
                    C = (int(C[0] * 255), int(C[1] * 255), int(C[2] * 255), int(opacity))
                    colors[i].fill(translucent)


            vertex_text = font.render(f'Vertex Count: {vertex_count}', True, black)
            coeff_text = font.render(f'Coefficient: {coeff:.3g}', True, black)
            window.blit(vertex_text, (10, 10))
            window.blit(coeff_text, (10, 27))
    
            offset_y = 80 * (vertex_count%2) * (2**int(-vertex_count/2))


        if erase:
            window.fill(white)


        # this is just so the images look more to the center

        for _ in range(1):
            v_index = (v_index + random.randint(1, (vertex_count))) % len(vertexes) #################### THE RULE #####################
            last_point = gen_new_point(last_point, vertexes[v_index], coeff)
            print(last_point)
            window.blit(colors[min(len(colors)-1, v_index)], (int(last_point[0] + width / 2), int(last_point[1] + height / 2 + offset_y)))

        for i in range(len(vertexes)):
            pygame.draw.line(window, black,
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