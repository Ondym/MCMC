import numpy as np

def opt_r(n):
    if n % 4 == 0:
        return 1 / (1 + np.tan(np.pi / n))
    elif n % 4 == 1 or n % 4 == 3:
        return 1 / (1 + 2 * np.sin(np.pi / (2 * n)))
    elif n % 4 == 2:
        return 1 / (1 + np.sin(np.pi / n))