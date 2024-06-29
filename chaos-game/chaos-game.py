import pygame
import math
import random

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

def main():
    running = True
    window.fill(white)
    vertex_count = 2
    last_point = [0, 0]
    v_index = 0
    frame_count = 0
    erase = False
    coeff = 1 / 2

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if frame_count % 80 == 0:
            vertex_count += 1
            vertexes = setup(vertex_count)
            last_point = list(vertexes[0])
            window.fill(white) # TOHLE SE KLIDNE MUZE SMAZAT A NASTAVIT erase=True, rozdil je ocividny

        if erase:
            window.fill(white)

        for _ in range(10000):
            v_index = (v_index + random.randint(1, 3)) % len(vertexes)
            last_point = gen_new_point(last_point, vertexes[v_index], coeff)
            pygame.draw.circle(window, blue, (int(last_point[0] + width / 2), int(last_point[1] + height / 2)), 1)

        for i in range(len(vertexes)):
            pygame.draw.line(window, black,
                             (vertexes[i][0] + width / 2, vertexes[i][1] + height / 2),
                             (vertexes[(i + 1) % len(vertexes)][0] + width / 2, vertexes[(i + 1) % len(vertexes)][1] + height / 2))

        vertex_text = font.render(f'Vertex Count: {vertex_count}', True, black)
        window.blit(vertex_text, (10, 10))

        pygame.display.flip()

        frame_count += 1

        pygame.time.delay(10)

    pygame.quit()

if __name__ == "__main__":
    main()
