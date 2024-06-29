from random import randint
import math
import matplotlib.pyplot as plt
import numpy as np
from perkolace_f import perk
from matplotlib import ticker

iterations = 500000
iterations_T = 10
konstnta = 500
list_l = 50
list_energii = np.array([])
list_energii_ = []
blobs_ = []
T = 5
min_T = 0.01
max_T = 1.5
list_T = []
list = [[randint(0, 1) for i in range(list_l)] for j in range(list_l)]
#list = [[0 for i in range(list_l)] for j in range(list_l)]

def pi(E, T):
    return math.exp(-E / T)


for hh in range(iterations_T):
    list = [[randint(0, 1) for i in range(list_l)] for j in range(list_l)]
    perkolace_list=[]
    print(hh)
    T = min_T + (max_T-min_T)*hh/iterations_T
    list_energii_ = []
    energie = 0
    for i in range(len(list)):
        for j in range(len(list[i])):
            if list[i][j] != list[i][(j + 1) % list_l]:
                energie += 1
            if list[i][j] != list[(i + 1) % list_l][j]:
                energie += 1

    for h in range(iterations):
        if h % 100000 == 0:
            print(h)
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
        if randint(0, 100000) / 100000 <= pi(k, T):
            list[l_i][l_j] = a
            energie += k
            # print(energie)
            # list_energii=np.append(list_energii, energie)
            list_energii_.append(energie)

        if h%500==0:
            perkolace_list.append(perk(list))
    list_T.append(np.mean(np.array(perkolace_list)))
    print(np.mean(np.array(perkolace_list)), "p")
    print(perkolace_list)
print(list)
for i in range(1,len(list_T)):
    if abs(list_T[i] -list_T[i-1])>0.6:
        list_T[i] = list_T[i-1]-0.03
s_d = []
# for p in list_T:
#     s_d.append(min(max(math.sqrt(p*(1-p)), 0), 1))
x = np.linspace(min_T, max_T, num=len(list_T))
y = np.array(list_T)
# ytop = y + np.array(s_d)
# ybottom = y - np.array(s_d)

# for i in range(len(ybottom)):
#     ybottom[i] = max(0, ybottom[i])

# for i in range(len(ytop)):
#     ytop[i] = min(1, ytop[i])

print(x, y)
fig, ax = plt.subplots()
# ax.plot(x, ytop, color="yellow")
# ax.plot(x, ybottom, color="yellow")
# ax.fill_between(x,ybottom, ytop, color="yellow", alpha=0.5)
ax.scatter(x,y, linewidth=1, marker="^", facecolors= "white",edgecolors="royalblue")
print(np.mean(y))
plt.xlabel("Temperature")
plt.ylabel("Percolation propability")
def percent_formatter(x, pos):
    return '%1.1f%%' % (x * 100)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(percent_formatter))
plt.show()