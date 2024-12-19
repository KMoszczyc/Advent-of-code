# --- Day 12: Garden Groups ---
import itertools
from collections import defaultdict
from operator import itemgetter
import numpy as np

from utils.utils import timeit, read_file_with_ints, read_str_grid_file

PATH = 'data/day12.txt'
TEST_PATH = 'data/test/day12.txt'


def solve(grid):
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
            neighbouring_region_ids = list(set([pos_to_region_id[neighbour] for neighbour in visited_neighbours if neighbour in pos_to_region_id]))
            if len(neighbouring_region_ids) == 0:  # create new region
                region_id = grid[pos] + str(region_id_count)
                regions[region_id] = [pos]
                pos_to_region_id[pos] = region_id
                region_id_count += 1
            elif len(neighbouring_region_ids) == 1:  # add to existing neighbouring region
                pos_to_region_id[pos] = neighbouring_region_ids[0]
                regions[neighbouring_region_ids[0]].append(pos)
            elif len(neighbouring_region_ids) > 1:  # merge regions:
                merge_region_id = neighbouring_region_ids[0]
                pos_to_region_id[pos] = merge_region_id
                regions[merge_region_id].append(pos)

                for region_id in neighbouring_region_ids:
                    if region_id == merge_region_id:
                        continue
                    region_members = regions[region_id]
                    assign_plants_to_new_region(region_members, merge_region_id, pos_to_region_id)
                    regions[merge_region_id].extend(region_members)
                    del regions[region_id]

    p1 = [calculate_price_p1(region_id, region_members) for region_id, region_members in regions.items()]
    p2 = [calculate_price_p2(region_id, region_members, pos_to_region_id) for region_id, region_members in regions.items()]

    print(p1)
    print(p2)

    return sum(p1), sum(p2)


def is_neighbour(pos1, pos2):
    y1, x1 = pos1
    y2, x2 = pos2
    return (y1 == y2 and np.abs(x1 - x2) == 1) or (x1 == x2 and np.abs(y1 - y2) == 1)


def calculate_price_p1(region_id, region_members):
    all_combinations = list(itertools.combinations(region_members, 2))
    neighbour_counts = defaultdict(int)
    if not all_combinations:  # only 1 member so area = 1, fence = 4
        return 4 * 1

    for pos1, pos2 in all_combinations:
        if is_neighbour(pos1, pos2):
            neighbour_counts[pos1] += 1
            neighbour_counts[pos2] += 1

    area = len(region_members)
    fence = sum(4 - count for pos, count in neighbour_counts.items())
    return area * fence


def calculate_price_p2(region_id, region_members, pos_to_region_id):
    if len(region_members)==1:
        # print(region_id, region_members, neighbour_counts, 1, 4)
        return 4 * 1

    # group by xs and ys and sort em so its easier to find sides
    pos_grouped_by_y = defaultdict(list)
    for y, x in region_members:
        pos_grouped_by_y[y].append((y, x))
    for y in pos_grouped_by_y.keys():
        pos_grouped_by_y[y] = sorted(pos_grouped_by_y[y], key=itemgetter(1))

    pos_grouped_by_x = defaultdict(list)
    for y, x in region_members:
        pos_grouped_by_x[x].append((y, x))
    for x in pos_grouped_by_x.keys():
        pos_grouped_by_x[x] = sorted(pos_grouped_by_x[x], key=itemgetter(0))

    topside_count = 0
    bottomside_count = 0
    is_top_counting = False
    is_bottom_counting = False
    for y, positions in pos_grouped_by_y.items():
        for y, x in positions:
            top = get_top(pos_to_region_id, x, y)
            bottom = get_bottom(pos_to_region_id, x, y)
            left = get_left(pos_to_region_id, x, y)

            # count topside
            if top is not None:  # if there is plant at top, there is no topside then
                is_top_counting = False
            elif not is_top_counting:  # new topside, lets go
                is_top_counting = True
                topside_count += 1
            elif left is None:  # there is a topside on the left, but its not a neighbour so a new topside
                topside_count += 1

            # count bottomside
            if bottom is not None:  # if there is plant at top, there is no topside then
                is_bottom_counting = False
            elif not is_bottom_counting:  # new topside, lets go
                is_bottom_counting = True
                bottomside_count += 1
            elif left is None:  # there is a bottom on the left, but its not a neighbour so a new topside
                bottomside_count += 1

    leftside_count = 0
    rightside_count = 0
    is_left_counting = False
    is_right_counting = False

    for x, positions in pos_grouped_by_x.items():
        for y, x in positions:
            right = get_right(pos_to_region_id, x, y)
            left = get_left(pos_to_region_id, x, y)
            top = get_top(pos_to_region_id, x, y)

            # count leftside
            if left is not None:  # if there is plant at left, there is no leftside then
                is_left_counting = False
            elif not is_left_counting:  # new leftside, lets go
                is_left_counting = True
                leftside_count += 1
            elif top is None:  # there is a leftside on top, but its not a neighbour so a new leftside
                leftside_count += 1

            # count rightside
            if right is not None:  # if there is plant at right, there is no rightside then
                is_right_counting = False
            elif not is_right_counting:  # new rightside, lets go
                is_right_counting = True
                rightside_count += 1
            elif top is None:  # there is a rightside on top, but its not a neighbour so a new rightside
                rightside_count += 1

            # print((y, x), 'rightside_count:', rightside_count)

    area = len(region_members)
    sides = topside_count + bottomside_count + leftside_count + rightside_count
    # print(region_id, region_members, topside_count, bottomside_count, leftside_count, rightside_count, 'area:', area, 'sides:', sides)
    print(region_id, topside_count, bottomside_count, leftside_count, rightside_count, 'area:', area, 'sides:', sides)

    return area * sides




def get_left(pos_to_region_id, x, y):
    region_id = pos_to_region_id[(y, x)]
    if x == 0:
        return None
    left_pos = (y, x - 1)
    neighbour_region_id = pos_to_region_id[left_pos]
    return left_pos if neighbour_region_id == region_id else None


def get_right(pos_to_region_id, x, y):
    region_id = pos_to_region_id[(y, x)]
    if x == WIDTH - 1:
        return None
    right_pos = (y, x + 1)
    neighbour_region_id = pos_to_region_id[right_pos]
    return right_pos if neighbour_region_id == region_id else None


def get_top(pos_to_region_id, x, y):
    region_id = pos_to_region_id[(y, x)]
    if y == 0:
        return None
    top_pos = (y - 1, x)
    neighbour_region_id = pos_to_region_id[top_pos]
    return top_pos if neighbour_region_id == region_id else None


def get_bottom(pos_to_region_id, x, y):
    region_id = pos_to_region_id[(y, x)]
    if y == HEIGHT - 1:
        return None
    bottom_pos = (y + 1, x)
    neighbour_region_id = pos_to_region_id[bottom_pos]
    return bottom_pos if neighbour_region_id == region_id else None


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


@timeit
def run():
    global WIDTH
    global HEIGHT
    grid = read_str_grid_file(PATH)
    WIDTH = grid.shape[1]
    HEIGHT = grid.shape[0]

    # stones = [125, 17]
    print(grid)
    p1, p2 = solve(grid)

    return p1, p2


if __name__ == '__main__':
    p1, p2 = run()
    print('P1 result:', p1)
    print('P2 result:', p2)
