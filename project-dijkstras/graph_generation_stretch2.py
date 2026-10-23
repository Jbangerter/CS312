import math
import random
import sys
import os
import matplotlib.pyplot as plt

# Ensure the project root is on the path to import from other files
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

from plotting import plot_points, draw_path, circle_point, plot_weights, title
from network_routing import find_shortest_path_with_heap


def generate_grid_graph(width: int, height: int, missing_edge_prob: float = 0.1):
    """
    Generates a 2D grid graph representing city blocks.
    Nodes only connect to immediate horizontal/vertical neighbors.
    """
    positions = []
    weights = {}

    # 1. Create positions
    for y in range(height):
        for x in range(width):
            positions.append((x, y))
            weights[y * width + x] = {}

    # 2. Create edges (only to adjacent nodes)
    size = width * height
    for i in range(size):
        x, y = positions[i]

        # Potential neighbors: Right, Left, Down, Up
        neighbors = []
        if x < width - 1:  neighbors.append(i + 1)
        if x > 0:          neighbors.append(i - 1)
        if y < height - 1: neighbors.append(i + width)
        if y > 0:          neighbors.append(i - width)

        for n in neighbors:
            # Randomly drop some streets to simulate road closures/dead ends
            if random.random() > missing_edge_prob:
                weights[i][n] = 1.0 + random.uniform(0, 0.5)

        # FIX: Ensure no node is completely isolated to prevent plotting.py from crashing
        if len(weights[i]) == 0 and len(neighbors) > 0:
            forced_neighbor = random.choice(neighbors)
            weights[i][forced_neighbor] = 1.0 + random.uniform(0, 0.5)

    return positions, weights


def run_and_save(width, height, name):
    print(f"--- Generating {name} Grid Graph ({width}x{height}) ---")
    positions, weights = generate_grid_graph(width, height, missing_edge_prob=0.2)

    source = 0
    target = (width * height) - 1

    path, cost = find_shortest_path_with_heap(weights, source, target)

    print(f"Cost: {cost:.2f}")

    # Create a fresh figure for each plot
    plt.figure()

    plot_points(positions, c='k', s=10)

    if width * height <= 400:
        plot_weights(positions, weights, c='gray')

    circle_point(positions[source], c='r')
    circle_point(positions[target], c='b')
    draw_path(positions, path, c='green')
    title(f"{name} Grid - Cost: {cost:.2f}")

    # Automatically save the plot as a PNG in the project root
    filename = f"{name.lower()}.png"
    filepath = os.path.join(project_root, filename)
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()  # Close the figure to avoid overlapping data
    print(f"Successfully saved {filepath}\n")


if __name__ == '__main__':
    run_and_save(10, 10, "Small")
    run_and_save(20, 20, "Medium")
    run_and_save(40, 40, "Large")