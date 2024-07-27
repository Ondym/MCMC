import numpy as np
import matplotlib.pyplot as plt

# Define the rings' parameters
outer_radius = 12
inner_radius = 10
centers = [(0, 0), (26, 0), (13, -11), (52, 0), (39, -11)]

# Number of points to use for the Monte Carlo simulation
total_points = 10**8  # Use 10 million points for a reasonable estimate
chunk_size = 10**6  # Process 1 million points at a time

# Generate random points within a bounding box that contains all rings
x_min = min(center[0] - outer_radius for center in centers)
x_max = max(center[0] + outer_radius for center in centers)
y_min = min(center[1] - outer_radius for center in centers)
y_max = max(center[1] + outer_radius for center in centers)

def estimate_union_area(chunk_size, total_points):
    points_inside_any_ring = 0

    for _ in range(total_points // chunk_size):
        x_random = np.random.uniform(x_min, x_max, chunk_size)
        y_random = np.random.uniform(y_min, y_max, chunk_size)

        # Check if points are inside any of the rings
        inside_any_ring = np.zeros(chunk_size, dtype=bool)
        for center in centers:
            distance_squared = (x_random - center[0])**2 + (y_random - center[1])**2
            inside_outer_circle = distance_squared <= outer_radius**2
            outside_inner_circle = distance_squared >= inner_radius**2
            inside_ring = inside_outer_circle & outside_inner_circle
            inside_any_ring |= inside_ring

        points_inside_any_ring += np.sum(inside_any_ring)

    # Estimate the area of the union
    area_of_union = points_inside_any_ring / total_points * (x_max - x_min) * (y_max - y_min)
    return area_of_union

area_of_union = estimate_union_area(chunk_size, total_points)
print(f"Estimated area of union: {area_of_union}")

# Optional: Plot the rings (only for a small sample, as plotting 10^7 points is impractical)
sample_points = min(10000, chunk_size)
x_random = np.random.uniform(x_min, x_max, sample_points)
y_random = np.random.uniform(y_min, y_max, sample_points)

inside_any_ring = np.zeros(sample_points, dtype=bool)
for center in centers:
    distance_squared = (x_random - center[0])**2 + (y_random - center[1])**2
    inside_outer_circle = distance_squared <= outer_radius**2
    outside_inner_circle = distance_squared >= inner_radius**2
    inside_ring = inside_outer_circle & outside_inner_circle
    inside_any_ring |= inside_ring

plt.figure(figsize=(10, 10))
theta = np.linspace(0, 2*np.pi, 300)
colors = ['b', 'orange', 'g', 'r', 'k']
for center, color in zip(centers, colors):
    plt.plot(center[0] + outer_radius * np.cos(theta), center[1] + outer_radius * np.sin(theta), color, label=f'Outer Circle {color}')
    plt.plot(center[0] + inner_radius * np.cos(theta), center[1] + inner_radius * np.sin(theta), color, linestyle='dashed', label=f'Inner Circle {color}')
plt.scatter(x_random[inside_any_ring], y_random[inside_any_ring], s=1, c='green', label='Union points')
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
