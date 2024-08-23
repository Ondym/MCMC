P = [1, 3, 5, 17, 257, 65537]

consts = []

for p1 in P:
    for p2 in P:
        if p1 != p2 or p1 == 1:
            for i in range(3):
                consts.append(2**i*p1*p2)

consts.sort()
print(*consts[::2], sep="\n")