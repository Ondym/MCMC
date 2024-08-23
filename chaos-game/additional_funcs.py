import numpy as np
import pygame, random, os

def opt_r(n):
    if n == 3:
        return 1/2
    if n % 4 == 0:
        return 1 / (1 + np.tan(np.pi / n))
    elif n % 4 == 1 or n % 4 == 3:
        return 1 / (1 + 2 * np.sin(np.pi / (2 * n)))
    elif n % 4 == 2:
        return 1 / (1 + np.sin(np.pi / n))

def save_image(vc, c, session_id, _window, opc = 255):
    c = f"{c:.3g}"
    des_dir = f"chaos-game/gen-imgs/ext_rul_{session_id}"
    md = os.path.join(des_dir, 'params.md')
    
    if not os.path.exists(des_dir):
        os.mkdir(des_dir)
        content = f"""## Chaos game\n### Session parameters\n\nCoefficient of LERP: r={c}\nSingle point opacity: {opc}/255\n\n*Rule for choosing the next vertex:*\nThe last chosen vertex NEZADANO ```(n+NEZADANO)```\n### Images generated"""
        
        with open(md, 'w') as file:
            file.write(content.strip())
        print(f"Created file: {md}")

    filename = f"vc{vc}_c{c}.png"
    pygame.image.save(_window, os.path.join(des_dir, filename))
    print(f"Image saved as {filename}")

    if not os.path.exists(md):
        print(f"File {md} does not exist.")
        return

    if not os.path.exists(os.path.join(des_dir, filename)):
        return

    image_description = f"""\n![Coefficient: {c} Vertex count: {vc}]({filename})"""

    with open(md, 'a') as file:
        file.write("\n\n" + image_description.strip())
    print(f"Added image description to {md}")

def neighbors():
    if random.random() < 0.5: return -1 
    else: return 1