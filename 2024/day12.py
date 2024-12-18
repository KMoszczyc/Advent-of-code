# --- Day 12: Garden Groups ---
import itertools
from collections import defaultdict

import numpy as np

from utils.utils import timeit, read_file_with_ints, read_str_grid_file

PATH = 'data/day12.txt'
TEST_PATH = 'data/test/day12.txt'


def p1(grid):
    visited = np.full(grid.shape, fill_value=False)
    regions = {}
    pos_to_region_id = {}
    region_id_count = 0
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            pos = (y, x)
            visited[pos] = True
            same_plant_neighbours = get_plant_neighbours(grid, x, y)
            visited_neighbours = [neighbour for neighbour in same_plant_neighbours if visited[neighbour]]
            neighbouring_region_ids = [pos_to_region_id[neighbour] for neighbour in visited_neighbours if neighbour in pos_to_region_id]
            print(pos, grid[pos], same_plant_neighbours , visited_neighbours, regions, neighbouring_region_ids)
            if len(neighbouring_region_ids) == 0: # create new region
                region_id = grid[pos] + str(region_id_count)
                regions[region_id] = [pos]
                pos_to_region_id[pos] = region_id
                region_id_count+=1
            elif len(neighbouring_region_ids) == 1: # add to existing neighbouring region
                pos_to_region_id[pos] = neighbouring_region_ids[0]
                regions[neighbouring_region_ids[0]].append(pos)
            elif len(neighbouring_region_ids) > 1: # merge regions:
                merge_region_id = neighbouring_region_ids[0]
                for region_id in neighbouring_region_ids:
                    if region_id == merge_region_id:
                        continue
                    region_members = regions[region_id]
                    assign_plants_to_new_region(region_members, merge_region_id, pos_to_region_id)
                    regions[merge_region_id].extend(region_members)

    print('regions:', regions)
    print('pos_to_region_id', pos_to_region_id)

    pass



def assign_plants_to_new_region(positions, new_region_id, pos_to_region_id):
    for pos in positions:
        pos_to_region_id[pos] = new_region_id
    return pos_to_region_id

def get_plant_neighbours(grid, x, y):
    """That are of the same plant type"""
    plant = grid[y][x]
    neighbours = []
    if y - 1 >= 0 and grid[y - 1][x] == plant:
        neighbours.append((y - 1, x))
    if y + 1 < grid.shape[0] and grid[y + 1][x] == plant:
        neighbours.append((y + 1, x))
    if x - 1 >= 0 and grid[y][x - 1] == plant:
        neighbours.append((y, x - 1))
    if x + 1 < grid.shape[1] and grid[y][x + 1] == plant:
        neighbours.append((y, x + 1))

    return neighbours

def p2(grid):
    pass
def flatten_dict(nested_dicts):
    flat_dict = defaultdict(int)
    for stones_nested in nested_dicts:
        for c, j in stones_nested.items():
            flat_dict[c] += j

    return flat_dict


@timeit
def run():
    grid = read_str_grid_file(TEST_PATH)
    # stones = [125, 17]
    print(grid)
    p1_result = p1(grid)
    p2_result = p2(grid)

    return p1_result, p2_result


if __name__ == '__main__':
    p1, p2 = run()
    print('P1 result:', p1)
    print('P2 result:', p2)
