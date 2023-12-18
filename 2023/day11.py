# --- Day 11: Cosmic Expansion ---
from utils.utils import read_str_grid_file
import numpy as np
import sys
from itertools import combinations
from collections import deque, defaultdict
import time

np.set_printoptions(threshold=sys.maxsize)
np.set_printoptions(edgeitems=10, linewidth=1000)

PATH = 'data/day11.txt'


# PATH = 'data/test/day11_test.txt'


def solve_part1(galaxy_grid):
    galaxies = find_galaxies(galaxy_grid)
    galaxy_pairs = set(combinations(galaxies, r=2))
    print(galaxy_grid)
    distances = []
    for galaxy_pair in galaxy_pairs:
        distances.append(calculate_euclidian_distance(galaxy_pair[0], galaxy_pair[1]))

    sum_of_distances = sum(distances)
    print(distances)
    print(sum_of_distances)
    return sum_of_distances


def solve_part2(galaxy_grid):
    """it's weird like that because sum wouldn't work with large numbers and would throw overflow"""
    empty_xs, empty_ys = get_empty_rows_and_cols(galaxy_grid)
    print('empty_xs', empty_xs)
    print('empty_ys', empty_ys)

    galaxies = find_galaxies(galaxy_grid)
    galaxy_pairs = set(combinations(galaxies, r=2))
    distances = []
    print(galaxy_grid)
    offset_size = 1000000
    total_num_of_x_gaps= 0
    total_num_of_y_gaps = 0

    for galaxy_pair in galaxy_pairs:
        x1, y1 = galaxy_pair[0]
        x2, y2 = galaxy_pair[1]
        min_x = min(x1, x2)
        min_y = min(y1, y2)
        max_x = max(x1, x2)
        max_y = max(y1, y2)

        num_of_x_gaps = len([x for x in empty_xs if x > min_x and x < max_x])
        num_of_y_gaps  = len([y for y in empty_ys if y > min_y and y < max_y])
        total_num_of_x_gaps += num_of_x_gaps
        total_num_of_y_gaps += num_of_y_gaps

        distance = calculate_euclidian_distance((min_x, min_y), (max_x - num_of_x_gaps, max_y - num_of_y_gaps))
        distances.append(distance)

    sum_of_offset_gaps = (total_num_of_x_gaps + total_num_of_y_gaps) * offset_size
    sum_of_distances = np.sum(distances, dtype=int)
    print(distances)
    print(sum_of_distances, sum_of_offset_gaps)
    return sum_of_distances + sum_of_offset_gaps


def solve_part1_bst(galaxy_grid):
    """BFS search with min distances between galaxy pairs"""

    galaxies = find_galaxies(galaxy_grid)
    galaxy_pairs = set(combinations(galaxies, r=2))
    print(galaxy_grid)
    min_distances = []
    for i, galaxy_pair in enumerate(galaxy_pairs):
        visited = []
        current_location = galaxy_pair[0]
        destination_location = galaxy_pair[1]
        location_queue = deque([current_location])
        distances_grid = np.full(galaxy_grid.shape, np.inf)
        distances_grid[current_location[1], current_location[0]] = 0
        # print(current_location, destination_location)
        while True:
            # print(current_pipe, pipe_map[current_pipe[1], current_pipe[0]], visited)
            if current_location == destination_location:
                min_distances.append(distances_grid[current_location[1], current_location[0]])
                distances_grid[destination_location[1], destination_location[0]] = -1
                # print(distances_grid)
                break

            # print(current_location, location_queue)

            current_location = location_queue.popleft()
            current_x, current_y = current_location
            locations = get_adjacent_not_visited_locations(current_location, visited, galaxy_grid)
            for location in locations:
                x, y = location
                if distances_grid[y, x] == np.inf:
                    location_queue.append(location)
                    distances_grid[y, x] = 1 + distances_grid[current_y, current_x]

        if i % 1000 == 0:
            print('Galaxy pairs:', i, ', total:', len(galaxy_pairs))
    sum_of_distances = sum(min_distances)
    print(min_distances)
    print(sum_of_distances)
    return sum_of_distances


def calculate_euclidian_distance(galaxy1, galaxy2):
    x1, y1 = galaxy1
    x2, y2 = galaxy2
    x_diff = np.abs(x1 - x2)
    y_diff = np.abs(y1 - y2)

    return x_diff + y_diff


def find_galaxies(galaxy_grid):
    galaxies = []
    for y, x in np.ndindex(galaxy_grid.shape):
        if galaxy_grid[y, x] == '#':
            galaxies.append((x, y))
    return galaxies


def get_adjacent_locations(location, grid):
    x, y = location
    locations = []
    if x - 1 >= 0:
        locations.append((x - 1, y))
    if x + 1 < grid.shape[1]:
        locations.append((x + 1, y))
    if y - 1 >= 0:
        locations.append((x, y - 1))
    if y + 1 < grid.shape[0]:
        locations.append((x, y + 1))
    return locations


def get_adjacent_not_visited_locations(location, visited, grid):
    locations = get_adjacent_locations(location, grid)
    not_visited_locations = [location for location in locations if location not in visited]
    return not_visited_locations


def expand_galaxy_grid(grid):
    new_grid_rows_list = []
    new_grid_cols_list = []

    # rows
    for y in range(grid.shape[0]):
        if '#' not in grid[y, :]:
            new_grid_rows_list.append(grid[y, :])
        new_grid_rows_list.append(grid[y, :])

    new_grid_rows_expanded = np.array(new_grid_rows_list)

    # cols
    for x in range(new_grid_rows_expanded.shape[1]):
        if '#' not in new_grid_rows_expanded[:, x]:
            new_grid_cols_list.append(new_grid_rows_expanded[:, x])
        new_grid_cols_list.append(new_grid_rows_expanded[:, x])

    new_grid_expanded = np.transpose(np.array(new_grid_cols_list))

    return new_grid_expanded


def get_empty_rows_and_cols(galaxy_grid):
    empty_rows = [y for y in range(galaxy_grid.shape[0]) if '#' not in galaxy_grid[y, :]]
    empty_cols = [x for x in range(galaxy_grid.shape[1]) if '#' not in galaxy_grid[:, x]]

    return empty_cols, empty_rows


def run():
    galaxy_grid = read_str_grid_file(PATH)
    expanded_galaxy_grid = expand_galaxy_grid(galaxy_grid)

    print(galaxy_grid.shape, expanded_galaxy_grid.shape)
    # result = solve_part1(expanded_galaxy_grid)
    result = solve_part2(galaxy_grid)

    return result


if __name__ == '__main__':
    result = run()
    print('Result:', result)
