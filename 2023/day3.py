# --- Day 3: Gear Ratios ---
import numpy as np
import re
from utils.utils import find_all, read_file, timeit, find_all_numbers, find_all_numbers_as_str
import itertools
from collections import Counter, defaultdict

PATH = 'data/day3.txt'
symbols = '@#$%&*-=/+'


def get_number_adjacent_to_symbol_part1(schematic_map, number, y, x, symbols):
    """Number centric solution, get indexes of all numbers and look for symbols around them"""
    # print(y, x, schematic_map[y, x:x + len(number)], number)

    symbol_left_border_index = max(0, x - 1)
    symbol_right_border_index = min(schematic_map.shape[1] - 1, x + len(number) + 1)

    potential_symbols = []

    # upper line potential symbols
    if y > 0:
        potential_symbols += list(schematic_map[y - 1, symbol_left_border_index:symbol_right_border_index])
    # bottom line potential symbols
    if y < schematic_map.shape[0] - 1:
        potential_symbols += list(schematic_map[y + 1, symbol_left_border_index:symbol_right_border_index])

    # Left and right potential symbols
    if x > 0:
        potential_symbols += schematic_map[y, x - 1]
    if x + len(number) + 1 < schematic_map.shape[1]:
        potential_symbols += schematic_map[y, x + len(number)]


    for letter in potential_symbols:
        if is_letter_a_symbol(letter, symbols):
            return int(number)

    return 0

def get_stars_around_a_number(schematic_map, index_map, number, y, x):
    """Symbol centric approach, look for numbers around a star symbol, if there are exactly 2 numbers then return n1*n2 - gear ratio"""
    symbol_left_border_index = max(0, x - 1)
    symbol_right_border_index = min(schematic_map.shape[1] - 1, x + len(number) + 1)

    potential_symbols = []
    potential_symbol_indexes = []

    # upper line potential symbols
    if y > 0:
        potential_symbols += list(schematic_map[y - 1, symbol_left_border_index:symbol_right_border_index])
        potential_symbol_indexes += list(index_map[y - 1, symbol_left_border_index:symbol_right_border_index])
    # bottom line potential symbols
    if y < schematic_map.shape[0] - 1:
        potential_symbols += list(schematic_map[y + 1, symbol_left_border_index:symbol_right_border_index])
        potential_symbol_indexes += list(index_map[y + 1, symbol_left_border_index:symbol_right_border_index])


    # Left and right potential symbols
    if x > 0:
        potential_symbols += schematic_map[y, x - 1]
        potential_symbol_indexes.append(index_map[y, x - 1])

    if x + len(number) + 1 < schematic_map.shape[1]:
        potential_symbols += schematic_map[y, x + len(number)]
        potential_symbol_indexes.append(index_map[y, x + len(number)])

    symbol_indexes = []
    for i, letter in enumerate(potential_symbols):
        if letter == '*':
            symbol_indexes.append(potential_symbol_indexes[i])

    print(y,x, potential_symbol_indexes, symbol_indexes)
    return symbol_indexes, number

def get_multiplied_gear_ratio_part2(schematic_map, index_map, numbers_map_list):
    stars_list = []
    star_counter = defaultdict(list)
    for i, numbers_map in enumerate(numbers_map_list):
        for index, number in numbers_map.items():
            stars_list.append(get_stars_around_a_number(schematic_map, index_map, number, i, index))
    print(stars_list)

    for stars, number in stars_list:
        print(stars, number)
        for y, x in stars:
            id = f'{str(y)},{str(x)}'
            star_counter[id].append(int(number))

    print(star_counter)
    gear_ratio_sum = 0
    for key, numbers in star_counter.items():
        if len(numbers) == 2:
            gear_ratio_sum += numbers[0]*numbers[1]
    return gear_ratio_sum

def array_2d_to_index_array_2d(array_2d):
    index_array = np.zeros(array_2d.shape, dtype=tuple)
    for y, x in np.ndindex(array_2d.shape):
        index_array[y,x] = (y, x)

    return  index_array

def is_letter_a_symbol(letter, symbols):
    return letter in symbols


def count_symbols(lines):
    letters_list = list(itertools.chain(*[list(line) for line in lines]))
    counter = Counter(letters_list)
    print(counter)


def run():
    lines = read_file(PATH)
    schematic_map = np.array([list(line) for line in lines])
    print(schematic_map, schematic_map.shape)

    index_map = array_2d_to_index_array_2d(schematic_map)

    numbers_map_list = [find_all_numbers_as_str(line) for line in lines]
    stars_indexes_list = [find_all(line, '*') for line in lines]

    print(index_map)
    print(stars_indexes_list)

    result = 0
    # for i, numbers_map in enumerate(numbers_map_list):
    #     numbers_with_adjacent_symbols = [get_number_adjacent_to_symbol_part1(schematic_map, number, i, index, symbols) for index, number in numbers_map.items()]
    #     result += sum(numbers_with_adjacent_symbols)

    result = get_multiplied_gear_ratio_part2(schematic_map, index_map, numbers_map_list)

    # for i, numbers_map in enumerate(numbers_map_list):
    #     numbers_with_adjacent_symbols = [get_multiplied_gear_ratio_part2(schematic_map, index_map, number, i, index) for index, number in numbers_map.items()]
    #     # result += sum(numbers_with_adjacent_symbols)
    # #

    return result


if __name__ == '__main__':
    result = run()

    print('Result:', result)
