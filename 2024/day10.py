# --- Day 10: Hoof It ---
import time
from collections import defaultdict

import numpy as np

from utils.utils import timeit, read_inline_sectioned_file_into_list_of_tuples, read_str_grid_file, read_int_grid_file

PATH = 'data/day10.txt'
TEST_PATH = 'data/test/day10.txt'


def solve(grid, part_mode='p1'):
    all_neighbours = calculate_all_node_neighbours(grid)
    trailheads = list(zip(*np.where(grid == 0)))
    trailhead_scores = defaultdict(int)

    for trailhead in trailheads:
        current = trailhead
        visited = []
        trailhead_scores[trailhead] = traverse_neighbours(grid, all_neighbours, visited, current, 0, part_mode=part_mode)

    return sum(v for k, v in trailhead_scores.items())


def traverse_neighbours(grid, all_neighbours, visited, current, score, part_mode):
    # time.sleep(1)
    visited.append(current)
    if grid[current] == 9:
        score += 1
        return score

    neighbours = all_neighbours[current]
    for neighbour in neighbours:
        if part_mode == 'p1' and neighbour in visited:
            continue
        score = traverse_neighbours(grid, all_neighbours, visited, neighbour, score, part_mode)
    return score


def calculate_all_node_neighbours(grid):
    all_neighbours = {}
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            all_neighbours[(y, x)] = calculate_node_neighbours(grid, x, y)

    return all_neighbours


def calculate_node_neighbours(grid, x, y):
    node_height = grid[y][x]
    neighbours = []
    if y - 1 >= 0 and grid[y - 1][x] - node_height == 1:
        neighbours.append((y - 1, x))
    if y + 1 < grid.shape[0] and grid[y + 1][x] - node_height == 1:
        neighbours.append((y + 1, x))
    if x - 1 >= 0 and grid[y][x - 1] - node_height == 1:
        neighbours.append((y, x - 1))
    if x + 1 < grid.shape[1] and grid[y][x + 1] - node_height == 1:
        neighbours.append((y, x + 1))

    return neighbours


@timeit
def run():
    grid = read_int_grid_file(PATH)
    p1 = solve(grid, 'p1')
    p2 = solve(grid, 'p2')

    return p1, p2


if __name__ == '__main__':
    p1, p2 = run()
    print('P1 result:', p1)
    print('P2 result:', p2)
