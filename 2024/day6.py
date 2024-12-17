# --- Day 6: Guard Gallivant ---
from copy import deepcopy

from utils.utils import read_str_grid_file
import numpy as np
import sys
from dataclasses import dataclass

np.set_printoptions(threshold=sys.maxsize)
PATH = 'data/day6.txt'
TEST_PATH = 'data/test/day6.txt'

@dataclass
class Collision():
    current_pos: tuple
    obstacle_pos: tuple

def part1(guard_map, is_part2=False):
    start_pos = get_start_pos(guard_map)
    is_loop = False
    visited = np.full(shape=guard_map.shape, fill_value=False)
    collisions = []

    visited_for_printing = deepcopy(guard_map)

    visited[start_pos] = True

    current_pos = start_pos # (y, x)
    start_direction = (-1, 0) # (y, x)
    direction = start_direction
    next_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
    while is_in_bounds(next_pos, guard_map):

        if guard_map[next_pos] == '#':
            collisions.append(Collision(current_pos, next_pos))
            direction = turn_right(direction)
        else:
            current_pos = next_pos
            visited[current_pos] = True


        next_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
        if collision_exists(collisions, Collision(current_pos, next_pos)):
            is_loop = True
            return None, None, is_loop

    # visited_for_printing[start_pos] = '^'
    # write_output(visited_for_printing)
    return np.sum(visited), visited, is_loop


def compare_collisions(c1, c2):
    return c1.current_pos == c2.current_pos and c1.obstacle_pos == c2.obstacle_pos

def collision_exists(collisions, c):
    for collision in collisions:
        if compare_collisions(c, collision):
            return True

def update_printed_map(visited_for_printing, current_pos, direction, last_direction):
    if direction[0] != last_direction[0] or direction[1] != last_direction[1]:
        visited_for_printing[current_pos] = '+'
    elif direction[0] != 0:
        visited_for_printing[current_pos] = '|'
    elif direction[1] != 0:
        visited_for_printing[current_pos] = '-'
    return visited_for_printing

def write_output(visited_for_printing):
    with open("output.txt", "w") as f:
        for row in visited_for_printing:
            f.write("".join(map(str, row)) + "\n")

def part2(guard_map):
    _, visited, _ = part1(guard_map)
    start_pos = get_start_pos(guard_map)
    visited[start_pos] = False

    indexes = list(map(tuple, np.argwhere(visited)))
    loop_obstacle_index_count = 0
    for i, idx in enumerate(indexes):
        if i % 10==0:
            print(f"{i}/{len(indexes)} step - {loop_obstacle_index_count} loops found")
        new_guard_map = deepcopy(guard_map)
        new_guard_map[idx] = '#'
        _, _, is_loop = part1(new_guard_map)
        if is_loop:
            loop_obstacle_index_count += 1

    return loop_obstacle_index_count


def get_start_pos(map):
    start = np.where(map == '^')
    start = (start[0][0], start[1][0]) # (y, x)
    return start

def turn_right(direction):
    # Rotate the direction to the right (90 degrees clockwise)
    dy, dx = direction
    return dx, -dy

def is_in_bounds(pos, map):
    return pos[0] >= 0 and pos[0] < map.shape[0] and pos[1] >= 0 and pos[1] < map.shape[1]

# @timeit
def run():
    map = read_str_grid_file(PATH)
    # result, _, _ = part1(map)
    result = part2(map)

    return result


if __name__ == '__main__':
    result = run()
    print('Result:', result)
