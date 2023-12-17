# --- Day 10: Pipe Maze ---
from dataclasses import dataclass
from utils.utils import read_file
import numpy as np
import time
import sys
from collections import deque

np.set_printoptions(threshold=sys.maxsize)
np.set_printoptions(edgeitems=10, linewidth=1000)

PATH = 'data/day10.txt'
# PATH = 'data/test/day10_test_part2.txt'
# PATH = 'data/test/day10_test2_part2.txt'
# PATH = 'data/test/day10_test3_part2.txt'

# [east, north, west, south], east <-> west (0, 2), north <-> south (1, 3)
pipe_connection_rules = {
    '|': [False, True, False, True],
    '-': [True, False, True, False],
    'L': [False, True, True, False],
    'J': [True, True, False, False],
    '7': [True, False, False, True],
    'F': [False, False, True, True],
    'S': [True, True, True, True],
    '.': [False, False, False, False],
    '0': [False, False, False, False]

}

connector_lookup_idx = [(-1, 0), (0, -1), (1, 0), (0, 1)]
possible_vertical_gaps_idx = [(-1, -1), (0, -1), (-1, 1), (0, 1)]
possible_horizontal_gaps_idx = [(-1, -1), (-1, 0), (1, -1), (1, 0)]


def are_pipes_connected(current_pipe, next_pipe, pipe_map):
    x1, y1 = current_pipe
    x2, y2 = next_pipe
    # print(x1, y1, x2, y2)
    if not pipe_exists(next_pipe, pipe_map):
        return False

    pipe1_connections = pipe_connection_rules[pipe_map[y1, x1]]
    pipe2_connections = pipe_connection_rules[pipe_map[y2, x2]]

    # print(pipe1_connections, pipe2_connections)
    are_connected = False
    if x1 > x2:
        are_connected = pipe1_connections[0] and pipe2_connections[2]
        # print('x1 > x2 east')
    elif x1 < x2:
        are_connected = pipe1_connections[2] and pipe2_connections[0]
        # print('x1 < x2 west')
    elif y1 > y2:
        are_connected = pipe1_connections[1] and pipe2_connections[3]
        # print('y1 > y2 north')
    elif y1 < y2:
        are_connected = pipe1_connections[3] and pipe2_connections[1]
        # print('y1 < y2 south')

    # print(pipe_map[y1, x1], '->', pipe_map[y2, x2], are_connected)
    return are_connected


def solve_part1(pipe_map):
    current_pipe = get_start_location(pipe_map)
    visited = [current_pipe]
    step = 0
    while True:
        # print(current_pipe, pipe_map[current_pipe[1], current_pipe[0]], visited)

        current_pipe = find_next_connected_pipe(current_pipe, visited, pipe_map)

        if pipe_map[current_pipe[1], current_pipe[0]] == 'S':
            break
        visited.append(current_pipe)
        step += 1

        if step % 10000 == 0:
            print('step:', step, pipe_map.shape[0] * pipe_map.shape[1], step / (pipe_map.shape[0] * pipe_map.shape[1]), len(visited))
            # print_visted_pipes(visited, pipe_map)

    path_map, path_map_mask = print_visted_pipes(visited, pipe_map)
    print(path_map)
    # print(path_map_mask)

    return len(visited) / 2, path_map, path_map_mask


def solve_part2(path_map, pipe_map):
    """0 - means outside loop (or inside if there is a path between pipes via corners),
       1 - means inside loop, no path between pipes"""
    width = path_map.shape[1]
    height = path_map.shape[0]

    path_map = pad_path_map_with_junk(path_map)

    count_junk_pipes = len([(y, x) for y, x in np.ndindex(path_map.shape) if path_map[y, x] == '.'])
    path_map = find_outside_junk_pipes_simple(path_map)
    vertical_east_pipe_gap_map, horizontal_south_pipe_gap_map = get_pipe_gap_maps(path_map)

    outside_corner_map = get_corner_map(path_map)  # corners leading to outside of the loop
    # print(outside_corner_map)

    junk_pipe_queue = deque(get_junk_pipes(path_map))

    while junk_pipe_queue:
        current_pipe_x, current_pipe_y = junk_pipe_queue.popleft()
        current_corner = current_pipe_x, current_pipe_y

        visited_pipes = []
        is_outside_loop = False
        visited_corners = []
        corner_queue = deque([current_corner])

        while corner_queue:
            if is_corner_outside(current_corner, path_map):
                is_outside_loop = True
                print(current_corner,', corner is outside!')
                break
            current_corner = corner_queue.popleft()
            visited_corners.append(current_corner)
            open_corners = get_adjacent_open_corners(current_corner, vertical_east_pipe_gap_map, horizontal_south_pipe_gap_map, outside_corner_map)
            for corner in open_corners:
                if corner not in visited_corners and corner not in corner_queue:
                    corner_queue.append(corner)

            # print('current_corner:', current_corner, 'corner_queue:', list(corner_queue), 'visited_corners:', list(visited_corners))
        visited_junk_pipes = get_adjacent_junk_pipes_to_corners(visited_corners, path_map)

        if is_outside_loop:
            for x, y in visited_junk_pipes:
                path_map[y, x] = 0
        else:
            for x, y in visited_junk_pipes:
                path_map[y, x] = 1

        # print(path_map)
        # print('junk_pipe_queue:', junk_pipe_queue)
        junk_pipe_queue = deque([pipe_idx for pipe_idx in list(junk_pipe_queue) if pipe_idx not in visited_junk_pipes])
        # print('junk_pipe_queue:', junk_pipe_queue)
    print('After=======================')
    print(path_map)
    count_outside_pipes = len([(y, x) for y, x in np.ndindex(path_map.shape) if path_map[y, x] == '0'])
    count_inside_pipes = len([(y, x) for y, x in np.ndindex(path_map.shape) if path_map[y, x] == '1'])

    print('total junk:', count_junk_pipes, 'count_inside_pipes:', count_inside_pipes, 'count_outside_pipes:', count_outside_pipes)
    return count_inside_pipes

def pad_path_map_with_junk(path_map):
    """Pad path map with junk, cuz the bst algorithm checks only if a corner is nearby a 0.. not working with borders"""
    return np.pad(path_map, [(1, 1), (1, 1)], mode='constant', constant_values=0)

def get_adjacent_junk_pipes_to_corners(corners, path_map):
    adjacent_junk_pipes = set()
    for corner in corners:
        for x, y in get_adjacent_pipe_idx_to_corner(corner):
            if path_map[y, x] == '.':
                adjacent_junk_pipes.add((x, y))
    return adjacent_junk_pipes


def get_adjacent_pipe_idx_to_corner(corner):
    x, y = corner
    return [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]


def get_adjacent_pipes_to_corner(corner, path_map):
    pipe_idx = get_adjacent_pipe_idx_to_corner(corner)
    return [path_map[y, x] for x, y in pipe_idx]


def is_corner_outside(corner, path_map):
    """Check if corner is around 0"""
    return any(pipe for pipe in get_adjacent_pipes_to_corner(corner, path_map) if pipe == '0')


def get_adjacent_corners(corner, corner_map):
    x, y = corner
    corners = {}
    if x - 1 >= 0:
        corners['west'] = (x - 1, y)
    if x + 1 < corner_map.shape[1]:
        corners['east'] = (x + 1, y)
    if y - 1 >= 0:
        corners['north'] = (x, y - 1)
    if y + 1 < corner_map.shape[0]:
        corners['south'] = (x, y + 1)
    return corners


def get_corner_map(path_map):
    width = path_map.shape[1]
    height = path_map.shape[0]
    outside_corner_map = np.full((height - 1, width - 1), False)
    for y, x in np.ndindex(outside_corner_map.shape):
        idxs = corner_to_pipe_idx(x, y)
        outside_corner_map[y, x] = any(True for x, y in idxs if path_map[y, x] == '0')

    return outside_corner_map


def corner_to_pipe_idx(x, y):
    """top_left, top_right, bottom_right, bottom_left"""
    return [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]


def get_adjacent_open_corners(current_corner, vertical_east_pipe_gap_map, horizontal_south_pipe_gap_map, corner_map):
    """ Where '.' is starting position, 8 in total
    """
    x, y = current_corner
    corners = get_adjacent_corners(current_corner, corner_map)  # dict - north, east, west, south
    open_corners = []
    # print(corners)
    if 'north' in corners and vertical_east_pipe_gap_map[y, x]:
        open_corners.append(corners['north'])
    if 'south' in corners and vertical_east_pipe_gap_map[y + 1, x]:
        open_corners.append(corners['south'])
    if 'east' in corners and horizontal_south_pipe_gap_map[y, x + 1]:
        open_corners.append(corners['east'])
    if 'west' in corners and horizontal_south_pipe_gap_map[y, x]:
        open_corners.append(corners['west'])

    return open_corners


def find_outside_junk_pipes_simple(path_map):
    width = path_map.shape[1]
    height = path_map.shape[0]
    for y in range(height):
        # go right (east)
        for x in range(width):
            if path_map[y, x] not in ['.', '0']:
                break
            path_map[y, x] = '0'
        for x in range(width - 1, -1, -1):
            if path_map[y, x] not in ['.', '0']:
                break
            path_map[y, x] = '0'

    for x in range(width):
        # go right (east)
        for y in range(height):
            if path_map[y, x] not in ['.', '0']:
                break
            path_map[y, x] = '0'
        for y in range(height - 1, -1, -1):
            if path_map[y, x] not in ['.', '0']:
                break
            path_map[y, x] = '0'

    print('Marked junk outside =============================')
    # print(path_map)
    return path_map


def print_visted_pipes(visited, pipe_map):
    path_map = np.full(pipe_map.shape, '.')
    path_map_mask = np.full(pipe_map.shape, False)
    for x, y in visited:
        path_map[y, x] = pipe_map[y, x]
        path_map_mask[y, x] = True

    return path_map, path_map_mask


def find_next_connected_pipe(current_pipe, visited, pipe_map):
    x1, y1 = current_pipe
    west_pipe = (x1 - 1, y1)
    north_pipe = (x1, y1 - 1)
    east_pipe = (x1 + 1, y1)
    south_pipe = (x1, y1 + 1)

    # print(west_pipe not in visited, north_pipe not in visited, east_pipe not in visited, south_pipe not in visited)
    # print(are_pipes_connected(current_pipe, west_pipe, pipe_map), are_pipes_connected(current_pipe, north_pipe, pipe_map), are_pipes_connected(current_pipe, east_pipe, pipe_map), are_pipes_connected(current_pipe, south_pipe, pipe_map))
    next_pipe = (-1, -1)
    if pipe_exists(west_pipe, pipe_map) and (are_pipes_connected(current_pipe, west_pipe, pipe_map) and west_pipe not in visited):
        next_pipe = west_pipe
    elif pipe_exists(north_pipe, pipe_map) and (are_pipes_connected(current_pipe, north_pipe, pipe_map) and north_pipe not in visited):
        next_pipe = north_pipe
    elif pipe_exists(east_pipe, pipe_map) and (are_pipes_connected(current_pipe, east_pipe, pipe_map) and east_pipe not in visited):
        next_pipe = east_pipe
    elif pipe_exists(south_pipe, pipe_map) and (are_pipes_connected(current_pipe, south_pipe, pipe_map) and south_pipe not in visited):
        next_pipe = south_pipe

    if next_pipe == (-1, -1) and (
            get_pipe(west_pipe, pipe_map) == 'S' or get_pipe(north_pipe, pipe_map) == 'S' or get_pipe(east_pipe, pipe_map) == 'S' or get_pipe(south_pipe,
                                                                                                                                              pipe_map) == 'S'):
        next_pipe = get_start_location(pipe_map)
        print('Found S!!')
    return next_pipe


def get_pipe_gap_maps(path_map):
    """
    East gap idx:
    |xx.|
    |xx.|
    |xx.|

    South gap idx:
    |xxx|
    |xxx|
    |...|
    :param path_map:
    :return:
    """
    vertical_east_pipe_gap_map = np.full(path_map.shape, False)
    horizontal_south_pipe_gap_map = np.full(path_map.shape, False)

    width = path_map.shape[1]
    height = path_map.shape[0]

    for y, x in np.ndindex(path_map.shape):
        if x + 1 < width and not are_pipes_connected((x, y), (x + 1, y), path_map):
            vertical_east_pipe_gap_map[y, x] = True
        if y + 1 < height and not are_pipes_connected((x, y), (x, y + 1), path_map):
            horizontal_south_pipe_gap_map[y, x] = True

    # print("vertical gaps ===============================================")
    # print(vertical_east_pipe_gap_map)
    # print("horizontal gaps ===============================================")
    # print(horizontal_south_pipe_gap_map)
    return vertical_east_pipe_gap_map, horizontal_south_pipe_gap_map


def get_pipe(pipe_idx, pipe_map):
    return pipe_map[pipe_idx[1], pipe_idx[0]]


def pipe_exists(pipe, pipe_map):
    x, y = pipe
    return x >= 0 and x < pipe_map.shape[1] and y >= 0 and y < pipe_map.shape[0]


def get_start_location(pipe_map):
    for iy, ix in np.ndindex(pipe_map.shape):
        if pipe_map[iy, ix] == 'S':
            start_x, start_y = ix, iy
            return start_x, start_y
    return -1, -1


def get_junk_pipes(path_map):
    """Every junk pipe in path_map is '.'"""
    return [(ix, iy) for iy, ix in np.ndindex(path_map.shape) if path_map[iy, ix] == '.']


def run():
    lines = read_file(PATH)
    pipe_map = np.array([list(line) for line in lines])

    result, path_map, path_map_mask = solve_part1(pipe_map)
    print('===========================================================')
    result = solve_part2(path_map, pipe_map)

    return result


if __name__ == '__main__':
    result = run()
    print('Result:', result)
