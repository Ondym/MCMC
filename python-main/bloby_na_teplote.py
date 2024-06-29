from random import randint
import math
import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np


iterations = 1000
iterations_T = 30
list_l = 50
neighbors = [[-1, 0], [1, 0], [0, 1], [0, -1]]
standartDeviations = []

blobs_ = []
min_T = 1
max_T = 40
list_T = []

samples = [(min_T + (max_T - min_T) * i / iterations_T) for i in range(iterations_T)]


def n_n(listik, l_i, l_j):
    return listik[(l_i+1)%list_l][(l_j)%list_l]+list[(l_i-1)%list_l][(l_j)%list_l]+listik[(l_i)%list_l][(l_j+1)%list_l]+listik[(l_i)%list_l][(l_j-1)%list_l]


def nnn(listik, i, j):
    a = 0

    listik[i][j] = 0
    for n, m in neighbors:
        neigh = n_n(list, i, j)
        if listik[(i+n)%list_l][(j+m)%list_l] == 1:
            listik = blobs(listik,(i + n)%list_l,(j + m)%list_l)
            a += ((neigh - n_n(list, i, j)) - 1)

    return a


def blobs(listik, i, j):
    listik[i][j] = 0
    for k in [-1, 1]:
        if listik[(i + k) % list_l][j] == 1:
            listik = blobs(listik,(i+k)%list_l, j)
        if listik[i][(j + k) % list_l] == 1:
            listik = blobs(listik, i, (j+k)%list_l)
    return listik

def blops(listik):
    index = 0
    for i in range(len(listik)):
        for j in range(len(listik)):
            if listik[i][j] == 1:
                listik=blobs(listik, i, j)
                index += 1

    return listik, index
def pi(E, T):
    return math.exp(-E/T)

for hh in range(iterations_T):
    list = [[randint(0, 1) for i in range(list_l)] for j in range(list_l)]

    #if hh%10000 == 0:
    #print(hh)
    T = min_T + (max_T - min_T) * hh / iterations_T
    blobs_ = []
    #blb = blops(list)[1]
    energie = 0
    for i in range(len(list)):
        for j in range(len(list[i])):
            if list[i][j] != list[i][(j+1)%list_l]:
                energie+=1
            if list[i][j] != list[(i+1)%list_l][j]:
                energie+=1

    for h in range(iterations):
        l_i = randint(0, list_l-1)
        l_j = randint(0,list_l-1)
        a = (list[l_i][l_j]+1)%2

        k = 0

        f = list[(l_i+1)%list_l][(l_j)%list_l]+list[(l_i-1)%list_l][(l_j)%list_l]+list[(l_i)%list_l][(l_j+1)%list_l]+list[(l_i)%list_l][(l_j-1)%list_l]
        #f = n_n(list, l_i, l_j)


        for i in [-1,1]:
            if a == list[(l_i+i)%list_l][(l_j)%list_l]:
                k-=1
            else:
                k+=1
            if a == list[(l_i)%list_l][(l_j+i)%list_l]:
                k-=1
            else:
                k+=1


        #if randint(0, 100000)/100000 <= pi(energie + k, T)/pi(energie, T):
        if randint(0, 100000)/100000 <= pi(k, T):
                list[l_i][l_j] = a
                energie += k


    list_T.append(blops(list)[1])
    standartDeviations.append(np.array(last_blobs).std()*1)
    
    # print(blops(list)[1])

x = np.array(samples)
y = np.array(list_T)
# yTop = y + np.array(standartDeviations)
# yBottom = y - np.array(standartDeviations)

# Define the formatter function
def thousands_formatter(x, pos):
    if x >= 1000:
        return '%1.1fk' % (x * 1e-3)
    else:
        return '%1.0f' % x

# Create the plot
fig, ax = plt.subplots()
# ax.plot(x, yTop, color="orange")
# ax.plot(x, yBottom, color="orange")
# ax.fill_between(x, yBottom, yTop, color="orange", alpha=.5)
ax.scatter(x, y, linewidth=1, marker="^", facecolors="white", edgecolors="royalblue")

# Print the mean of y
print(np.mean(y))

# Set the labels
plt.xlabel("Temperature")
plt.ylabel("Final blob count")

# Set the formatter for the y-axis
ax.yaxis.set_major_formatter(ticker.FuncFormatter(thousands_formatter))

# Show the plot
plt.show()