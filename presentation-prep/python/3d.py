import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from PIL import Image
import os
import sys
from datetime import datetime
from random import randint

iterations = 4*10**5
list_l = 10  # Reduced size for 3D grid to manage memory
skipCount = int(iterations * 0.1)

samples = [0.005, 0.01, 0.2, 0.5, 0.8, 1, 1.1, 1.2, 1.35, 1.5, 1.7, 1.9, 2.2, 2.6, 3, 3.5, 4, 4.5, 5]

samples.reverse()
flags = list(range(len(samples)))

timestamp = datetime.now().strftime("%H_%M_%S")

def init_energy(grid):
    energy = 0
    for i in range(list_l):
        for j in range(list_l):
            for k in range(list_l):
                if grid[i, j, k] != grid[i, (j + 1) % list_l, k]:
                    energy += 1
                if grid[i, j, k] != grid[(i + 1) % list_l, j, k]:
                    energy += 1
                if grid[i, j, k] != grid[i, j, (k + 1) % list_l]:
                    energy += 1
    return energy

def delta_energy(grid, i, j, k):
    a = 1 - grid[i, j, k]
    delta = 0
    for di, dj, dk in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
        ni, nj, nk = (i + di) % list_l, (j + dj) % list_l, (k + dk) % list_l
        if a == grid[ni, nj, nk]:
            delta -= 1
        else:
            delta += 1
    return delta

def save_grid(grid, filename="saved_grid.npy"):
    os.makedirs(f'presentation-prep/3D-saved/{timestamp}', exist_ok=True)
    np.save(f'presentation-prep/3D-saved/{timestamp}/{filename}.npy', grid)
    print(f"Grid saved as {filename}")

def load_grid(filename="saved_grid.npy"):
    grid = np.load(filename)
    print(f"Grid loaded from {filename}")
    return grid

def create_grid_image(array, output_dir='images', output_file='grid_image.png'):
    dir_path = os.path.join(output_dir, timestamp)
    os.makedirs(dir_path, exist_ok=True)

    # For 3D, we will create slices
    depth = array.shape[2]
    for d in range(depth):
        slice_2d = array[:, :, d]
        rows, cols = slice_2d.shape
        cell_size = 500 // cols

        image = Image.new('RGB', (cols * cell_size, rows * cell_size), 'white')
        pixels = image.load()

        for i in range(rows):
            for j in range(cols):
                color = (0, 0, 0) if slice_2d[i, j] == 1 else (255, 255, 255)
                for x in range(cell_size):
                    for y in range(cell_size):
                        pixels[j * cell_size + x, i * cell_size + y] = color

        image = image.resize((512, 512), Image.NEAREST)
        file_path = os.path.join(dir_path, f"{output_file}_slice_{d}.png")
        image.save(file_path)
        print(f"Image saved as {file_path}")

list_T = []
standartDeviations = []

# Initialisation is outside of loop: The pictures are dependent!
grid = np.random.randint(2, size=(list_l, list_l, list_l))

energie = init_energy(grid)

for T in samples:
    print(f"Processing T={T}")
    list_energii_ = []

    for h in range(iterations):
        if ((h + 1) % (iterations // 25) == 0):
            percent = round(h / (iterations + 1) * 100)
            bar = '#' * (h * 50 // (iterations + 1))
            spaces = ' ' * (50 - len(bar))
            sys.stdout.write(f'\r{int(percent)}% [{bar}{spaces}]')
            sys.stdout.flush()

        l_i, l_j, l_k = randint(0, list_l - 1), randint(0, list_l - 1), randint(0, list_l - 1)
        a = 1 - grid[l_i, l_j, l_k]
        delta = delta_energy(grid, l_i, l_j, l_k)

        if delta < 0 or np.random.exponential() > delta / T:
            grid[l_i, l_j, l_k] = a
            energie += delta

        if h > skipCount:
            list_energii_.append(energie)

    sys.stdout.write('\r' + ' ' * 60 + '\r')
    sys.stdout.flush()

    list_T.append(np.mean(list_energii_))
    standartDeviations.append(np.std(list_energii_))

    if samples.index(T) in flags:
        f_name = f"{T:.3f}"
        save_grid(grid, filename=f_name)

x = np.array(samples)
y = np.array(list_T)
yTop = y + np.array(standartDeviations)
yBottom = y - np.array(standartDeviations)

# Theoretical function for energy for large temperatures
yTeor = (list_l**3) * np.minimum(1,np.maximum(0, 1 - (1/2) * x**(-1) - (5/24) * x**(-3)- (1/15) * x**(-5)))
yError = (1/(list_l*np.sqrt(2)))*yTeor * (1+(1/2) * x**(-1)+(7/8) * x**(-2)+(31/48) * x**(-3)+(217/384) * x**(-4))
yTeorPlus = np.minimum(list_l**3,yTeor + yError)
yTeorMinus = np.minimum(list_l**3,np.maximum(0,yTeor - yError))

def thousands_formatter(x, pos):
    if x >= 1000:
        return f'{x * 1e-3:1.1f}k'
    else:
        return f'{x:1.0f}'

fig, ax = plt.subplots()
ax.plot(x, yTop, color="orange")
ax.plot(x, yBottom, color="orange")
ax.fill_between(x, yBottom, yTop, color="orange", alpha=0.5)
ax.plot(x, yTeor, color="blue")
ax.plot(x, yTeorPlus, color="green")
ax.plot(x, yTeorMinus, color="green")

ax.scatter(x, y, linewidth=1, marker="^", facecolors="white", edgecolors="royalblue", zorder=10)

plt.xlabel("Temperature")
plt.ylabel("Energy")
ax.yaxis.set_major_formatter(ticker.FuncFormatter(thousands_formatter))

output_dir = os.path.join('images', timestamp)
os.makedirs(output_dir, exist_ok=True)
plot_path = os.path.join(output_dir, "plot.png")
plt.savefig(plot_path)
print(f"Plot saved as {plot_path}")