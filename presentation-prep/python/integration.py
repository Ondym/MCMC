from random import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize_scalar

# Define the function to integrate
def func(x):
    return np.sin(x)

# Define the range and maximum value of the function for Method 2
a = 0
b = 2

res = minimize_scalar(lambda x: -func(x), bounds=(a, b), method='bounded')
func_max = .1-res.fun


print(func_max)

exact_result = 1.4161468365471423869

# Sample number for illustrations
sample_num_illustration = 150

# Illustrate Method 1
x_points = np.random.uniform(a, b, sample_num_illustration)
y_points = func(x_points)

plt.figure(figsize=(6, 6))
for x, y in zip(x_points, y_points):
    plt.plot([x, x], [0, y], 'r-', linewidth=0.5)

plt.plot(x_points, y_points, 'ro')

x = np.linspace(a, b, 100)
plt.plot(x, func(x), 'b-')
plt.title("Illustration of Method 1")
plt.xlabel("x")
plt.ylabel("y")
plt.tight_layout()
plt.savefig("presentation-prep/int-method1.png", bbox_inches='tight')
plt.close()

# Illustrate Method 2
sample_num_illustration = 500

x_points = np.random.uniform(a, b, sample_num_illustration)
y_points = np.random.uniform(0, func_max, sample_num_illustration)
inside_points_x = []
inside_points_y = []
outside_points_x = []
outside_points_y = []

for x, y in zip(x_points, y_points):
    if y <= func(x):
        inside_points_x.append(x)
        inside_points_y.append(y)
    else:
        outside_points_x.append(x)
        outside_points_y.append(y)

plt.figure(figsize=(6, 6))
plt.plot(inside_points_x, inside_points_y, 'go')
plt.plot(outside_points_x, outside_points_y, 'ro')
x = np.linspace(a, b, 100)
plt.plot(x, func(x), 'b-')
plt.title("Illustration of Method 2")
plt.xlabel("x")
plt.ylabel("y")
plt.tight_layout()
plt.savefig("presentation-prep/int-method2.png", bbox_inches='tight')
plt.close()

# Monte Carlo Integration with 100 iterations
iterations = 100
sample_num = 10**4
method1_results = []
method2_results = []

for _ in range(iterations):
    # Method 1
    total = 0
    for i in range(sample_num):
        total += func(random() * (b - a) + a)
    result_method_1 = total / sample_num * (b - a)
    method1_results.append(result_method_1)
    
    # Method 2
    points_in = 0
    for i in range(sample_num):
        point = (random() * (b - a) + a, random() * func_max)
        if point[1] <= func(point[0]):
            points_in += 1
    result_method_2 = points_in / sample_num * (b - a) * func_max
    method2_results.append(result_method_2)

riemann = 0
for i in range(sample_num):
    riemann += func(a + (b-a)/sample_num * i)

riemann = riemann / sample_num * (b - a)

avg_method1 = np.mean(method1_results)
avg_method2 = np.mean(method2_results)
avg_riemann = np.mean(riemann)
std_method1 = np.std(method1_results)
std_method2 = np.std(method2_results)
std_riemann = np.std(riemann)

# Plotting the results

plt.figure(figsize=(12, 6))
iterations_range = range(iterations)
plt.plot(iterations_range, method1_results, 'bo-', label='Method 1')
plt.plot(iterations_range, method2_results, 'ro-', label='Method 2')
# plt.plot(iterations_range, riemann, 'go-', label='Riemann Sum')
plt.axhline(y=exact_result, color='g', linestyle='-')

# Add standard deviation shaded areas
plt.fill_between(iterations_range, avg_method1 - std_method1, avg_method1 + std_method1, color='blue', alpha=0.2)
plt.fill_between(iterations_range, avg_method2 - std_method2, avg_method2 + std_method2, color='red', alpha=0.2)
# plt.fill_between(iterations_range, avg_riemann - std_riemann, avg_riemann + std_riemann, color='green', alpha=0.2)

plt.xlabel('Iteration')
plt.ylabel('Integral Value')
plt.title('Monte Carlo Integration Results')
plt.tight_layout()
plt.savefig("presentation-prep/int-comparison.png", bbox_inches='tight')
plt.show()

rel_dev_method1 = abs(avg_method1 - exact_result) / exact_result * 100
rel_dev_method2 = abs(avg_method2 - exact_result) / exact_result * 1000

print(f"Average result from Method 1: {avg_method1}")
print(f"Average result from Method 2: {avg_method2}")
print(f"Average result from Riemann sum: {riemann}")
print(f"Relative st deviation from exact result (Method 1): {rel_dev_method1}%")
print(f"Relative deviation from exact result (Method 2): {rel_dev_method2}%")
print(f"Relative deviation from exact result (Riemann sum): {riemann}%")
print(f"Method 2 relative deviation is {rel_dev_method2 / rel_dev_method1} times the relative deviation of Method 1")
