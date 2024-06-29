import os
from PIL import Image, ImageTk
from random import randint
import numpy as np
import cv2
from copy import deepcopy
import tkinter as tk

image_path = 'qr-img/QR.png'

def display_image(img_path):
    root = tk.Tk()
    root.title("Image Viewer")

    img = Image.open(img_path)
    tk_img = ImageTk.PhotoImage(img)

    label = tk.Label(root, image=tk_img, borderwidth=0, highlightthickness=0)
    label.pack(padx=0, pady=0)

    root.geometry(f"{img.width}x{img.height}")

    root.mainloop()

    root.mainloop()

def scale_up_array(array, scale_factor=10):
    array_np = np.array(array)
    scaled_array = np.kron(array_np, np.ones((scale_factor, scale_factor)))
    return scaled_array.astype(int)

def is_border(x, y):
    neigbour = -1

    if code_array[x][y] == 1: return False

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if (abs(dx) + abs(dy) == 1):
                if (x+dx > 0 and x+dx < size_x and y+dy > 0 and y+dy < size_y):
                    if neigbour > -1:
                        if neigbour != code_array[x+dx][y+dy]:
                            return True
                    else:
                        neigbour = code_array[x+dx][y+dy]
    return False

def create_grid_image(array, output_dir='qr-img', output_file='qr_image.png'):
    dir_path = os.path.join(output_dir)
    os.makedirs(dir_path, exist_ok=True)

    rows, cols = len(array), len(array[0])
    cell_size = 500 // cols

    image = Image.new('RGB', (cols * cell_size, rows * cell_size), 'white')
    pixels = image.load()

    for i in range(rows):
        for j in range(cols):
            color = (0, 0, 0) if array[i][j] == 0 else (255, 255, 255)
            for x in range(cell_size):
                for y in range(cell_size):
                    pixels[j * cell_size + x, i * cell_size + y] = color

    image = image.resize((512, 512), Image.NEAREST)
    file_path = os.path.join(dir_path, output_file)
    image.save(file_path)
    print(f"Image saved as {file_path}")


def qr_to_list(img_path):
    qr_image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    if qr_image is None:
        raise ValueError("Image not found or unable to load.")

    _, binary_image = cv2.threshold(qr_image, 128, 255, cv2.THRESH_BINARY)

    binary_list = (binary_image // 255).tolist()
    
    return binary_list


code_array = qr_to_list(image_path)


code_array = scale_up_array(code_array, scale_factor=5)

size_x, size_y = len(code_array), len(code_array[0])

changed_array = deepcopy(code_array)

for i in range(size_x):
    for j in range(size_y):
        if (randint(0, 10) < 4 and is_border(i, j)):
            ch_x, ch_y = i, j
            changed_array[ch_x][ch_y] = (code_array[ch_x][ch_y] + 1) % 2

create_grid_image(changed_array)
display_image("qr-img/qr_image.png")
