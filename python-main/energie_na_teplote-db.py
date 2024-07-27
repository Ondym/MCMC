import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from PIL import Image
import os
import sys
from datetime import datetime
from random import randint

iterations = 6*10**5
list_l = 256
skipCount = int(iterations * 0.1)

samples = np.linspace(0.2, 2, 550)

samples = samples.tolist()
samples = np.linspace(0.01, 0.2, 40).tolist() + samples
samples = [0.01 for _ in range(10)] + samples

samples.reverse()
flags = list(range(len(samples)))

timestamp = datetime.now().strftime("%H_%M_%S")

def init_energy(grid):
    energy = 0
    for i in range(list_l):
        for j in range(list_l):
            if grid[i, j] != grid[i, (j + 1) % list_l]:
                energy += 1
            if grid[i, j] != grid[(i + 1) % list_l, j]:
                energy += 1
    return energy

def delta_energy(grid, i, j):
    a = 1 - grid[i, j]
    k = 0
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = (i + di) % list_l, (j + dj) % list_l
        if a == grid[ni, nj]:
            k -= 1
        else:
            k += 1
    return k

def save_grid(grid, filename="saved_grid.npy"):
    np.save(filename, grid)
    print(f"Grid saved as {filename}")

def load_grid(filename="saved_grid.npy"):
    grid = np.load(filename)
    print(f"Grid loaded from {filename}")
    return grid

def create_grid_image(array, output_dir='images/anim_' + timestamp, output_file='grid_image.png'):
    dir_path = os.path.join(output_dir)
    os.makedirs(dir_path, exist_ok=True)

    rows, cols = array.shape
    cell_size = 500 // cols

    image = Image.new('RGB', (cols * cell_size, rows * cell_size), 'white')
    pixels = image.load()

    for i in range(rows):
        for j in range(cols):
            color = (0, 0, 0) if array[i, j] == 1 else (255, 255, 255)
            for x in range(cell_size):
                for y in range(cell_size):
                    pixels[j * cell_size + x, i * cell_size + y] = color

    image = image.resize((512, 512), Image.NEAREST)
    file_path = os.path.join(dir_path, output_file)
    image.save(file_path)
    print(f"Image saved as {file_path}")

list_T = []
standartDeviations = []

# Initialisation is outside of loop: The pictures are dependent!
grid = load_grid()

# f = open("GM.py", "a")
# f.close()

#grid = np.zeros((list_l, list_l), dtype=int)       # Empty grid
energie = init_energy(grid)


for T in samples:
    print(f"Processing T={T}")
    list_energii_ = []

    # Separate lists for black and white cells
    #black_cells = [(i, j) for i in range(list_l) for j in range(list_l) if grid[i][j] == 1]
    #white_cells = [(i, j) for i in range(list_l) for j in range(list_l) if grid[i][j] == 0]

    for h in range(iterations):
        if ((h + 1) % (iterations // 25) == 0):
            percent = round(h / (iterations + 1) * 100)
            bar = '#' * (h * 50 // (iterations + 1))
            spaces = ' ' * (50 - len(bar))
            sys.stdout.write(f'\r{int(percent)}% [{bar}{spaces}]')
            sys.stdout.flush()

        l_i, l_j = randint(0, list_l - 1), randint(0, list_l - 1)
        a = 1 - grid[l_i, l_j]
        k = delta_energy(grid, l_i, l_j)

        # I: retaining the number of black/white cells
        if 0==1:
            if grid[l_i][l_j] == 1:
                m_i, m_j = white_cells[randint(0, len(white_cells) - 1)]
            else:
                m_i, m_j = black_cells[randint(0, len(black_cells) - 1)]

            grid[l_i][l_j] = 1-grid[l_i][l_j]
            k += delta_energy(grid, m_i, m_j)
            grid[l_i][l_j] = 1-grid[l_i][l_j]
            if k < 0 or np.random.exponential() > k / T:
                # Swap the cells
                grid[l_i][l_j], grid[m_i][m_j] = grid[m_i][m_j], grid[l_i][l_j]
                energie += k

                # Update the black and white cell lists
                if grid[l_i][l_j] == 1:
                    black_cells.remove((m_i, m_j))
                    white_cells.append((m_i, m_j))
                    white_cells.remove((l_i, l_j))
                    black_cells.append((l_i, l_j))
                else:
                    black_cells.remove((l_i, l_j))
                    white_cells.append((l_i, l_j))
                    white_cells.remove((m_i, m_j))
                    black_cells.append((m_i, m_j))
        else: # II: Original code
            if k < 0 or np.random.exponential() > k/ T:
                grid[l_i][l_j] = a
                energie += k

        if h > skipCount:
            list_energii_.append(energie)

    sys.stdout.write('\r' + ' ' * 60 + '\r')
    sys.stdout.flush()

    list_T.append(np.mean(list_energii_))
    standartDeviations.append(np.std(list_energii_))

    if samples.index(T) in flags:
        f_name = f"{T:.3f}.png"
        create_grid_image(grid, output_file=f_name)

x = np.array(samples)
y = np.array(list_T)
yTop = y + np.array(standartDeviations)
yBottom = y - np.array(standartDeviations)

# Theoretical function for energy for large temperatures
yTeor = (list_l**2) * np.minimum(1,np.maximum(0, 1 - (1/2) * x**(-1) - (5/24) * x**(-3)- (1/15) * x**(-5)))
#yError = (list_l/np.sqrt(2))*(1+(5/8) * x**(-2))
yError = (1/(list_l*np.sqrt(2)))*yTeor * (1+(1/2) * x**(-1)+(7/8) * x**(-2)+(31/48) * x**(-3)+(217/384) * x**(-4))
yTeorPlus = np.minimum(list_l**2,yTeor + yError)
yTeorMinus = np.minimum(list_l**2,np.maximum(0,yTeor - yError))

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

initvals_path = os.path.join(output_dir, "initvals.txt")
with open(initvals_path, 'w') as f:
    f.write(f"Grid size: {list_l}x{list_l}\n")
    f.write(f"Number of iterations: {iterations}\n")
    f.write(f"Selected temperature samples: {samples}\n")
    f.write("Initial grid: Previous\n")
    
plt.show()