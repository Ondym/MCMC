from random import random
from random import randint
import math
import matplotlib.pyplot as plt
from matplotlib import ticker 
import numpy as np
from PIL import Image
import os
import sys
from datetime import datetime

"""
 samples je mozny vyplnit i treba for cyklem, je to seznam hodnot T

 flags je seznam indexu, kolikaty T ze samples dostane obrazek
"""

iterations = 10**10
list_l = 256
list_energii = np.array([])
list_energii_ = []
standartDeviations = []
T = 5
list_T = []
skipCount = iterations * .1

samples = [0.0000001]

flags = [0]

print("Number of samples: ", len(samples))

def pi(E, T):
    if -E/T > 1:
        return 1

    return math.exp(-E / T)

timestamp = datetime.now().strftime("%H_%M_%S")
def create_grid_image(array, output_dir='generated-images', output_file='grid_image.png'):
    dir_path = os.path.join(output_dir, timestamp)
    os.makedirs(dir_path, exist_ok=True)

    rows, cols = len(array), len(array[0])
    cell_size = 500 // cols

    image = Image.new('RGB', (cols * cell_size, rows * cell_size), 'white')
    pixels = image.load()

    for i in range(rows):
        for j in range(cols):
            color = (0, 0, 0) if array[i][j] == 1 else (255, 255, 255)
            for x in range(cell_size):
                for y in range(cell_size):
                    pixels[j * cell_size + x, i * cell_size + y] = color

    image = image.resize((512, 512), Image.NEAREST)
    file_path = os.path.join(dir_path, output_file)
    image.save(file_path)
    print(f"Image saved as {file_path}")

for hh in samples:
    # print(str(hh))
    list = [[randint(0, 1) for i in range(list_l)] for j in range(list_l)]
    T = hh
    list_energii_ = []
    energie = 0
    for i in range(len(list)):
        for j in range(len(list[i])):
            if list[i][j] != list[i][(j + 1) % list_l]:
                energie += 1
            if list[i][j] != list[(i + 1) % list_l][j]:
                energie += 1

    for h in range(iterations):
        if ((h+1)%int(iterations/25) == 0):
            percent = round(h / (iterations+1) * 100) 
            bar = '#' * (h * 50 // (iterations+1))
            spaces = ' ' * (50 - len(bar))
            sys.stdout.write(f'    \r{int(percent)}% [{bar}{spaces}]')
            sys.stdout.flush()

        l_i = randint(0, list_l - 1)
        l_j = randint(0, list_l - 1)
        a = (list[l_i][l_j] + 1) % 2

        k = 0
        for i in [-1, 1]:
            if a == list[(l_i + i) % list_l][(l_j) % list_l]:
                k -= 1
            else:
                k += 1
            if a == list[(l_i) % list_l][(l_j + i) % list_l]:
                k -= 1
            else:
                k += 1

        # if randint(0, 100000)/100000 <= pi(energie + k, T)/pi(energie, T):
        if random() <= pi(k, T):
            list[l_i][l_j] = a
            energie += k
        if h > skipCount:
            list_energii_.append(energie)

    sys.stdout.write('\r' + ' ' * 60 + '\r')
    sys.stdout.flush()

    list_T.append(np.mean(np.array(list_energii_)))
    standartDeviations.append(np.array(list_energii_).std()*1)

    if samples.index(hh) in flags:
        f_name = output_file=str(int(hh*10000) / 10000).ljust(5, '0') + ".png"
        create_grid_image(list, output_file=(f_name))


x = np.array(samples)
y = np.array(list_T)
yTop = y + np.array(standartDeviations)
yBottom = y - np.array(standartDeviations)

# Define the formatter function
def thousands_formatter(x, pos):
    if x >= 1000:
        return '%1.1fk' % (x * 1e-3)
    else:
        return '%1.0f' % x

# Create the plot
fig, ax = plt.subplots()
ax.plot(x, yTop, color="orange")
ax.plot(x, yBottom, color="orange")
ax.fill_between(x, yBottom, yTop, color="orange", alpha=.5)
ax.scatter(x, y, linewidth=1, marker="^", facecolors="white", edgecolors="royalblue")

print("Showing graph")

plt.xlabel("Temperature")
plt.ylabel("Energy")

ax.yaxis.set_major_formatter(ticker.FuncFormatter(thousands_formatter))

plt.show()