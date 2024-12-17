# --- Day 9: Disk Fragmenter ---
import dataclasses
import time
from copy import deepcopy

from utils.utils import timeit, read_inline_sectioned_file_into_list_of_tuples, read_file
import itertools
import numpy as np
import sys
from dataclasses import dataclass


PATH = 'data/day9.txt'
TEST_PATH = 'data/test/day9.txt'

@dataclass
class DiskFile:
    file_id: int
    size: int
@dataclass
class EmptySpace:
    size: int

def part1(input):
    input_disk_map, disk_map_compressed = convert_input(input)
    result_disk_map = deepcopy(input_disk_map)
    index = -1
    right_id_index = get_index_of_last_id(result_disk_map)

    right_id_index = -1
    dot_indexes = [i for i, x in enumerate(result_disk_map) if x == '.']
    number_indexes = [i for i, x in enumerate(result_disk_map) if is_int(x)]
    for dot_index in dot_indexes:
        if dot_index >= number_indexes[right_id_index]:
            break
        result_disk_map[dot_index] = result_disk_map[number_indexes[right_id_index]]
        result_disk_map[number_indexes[right_id_index]] = '.'
        # print(''.join(result_disk_map), dot_index, number_indexes[right_id_index], right_id_index)

        right_id_index -= 1

    cut_disk_map = result_disk_map[:get_index_of_last_id(result_disk_map) + 1]
    result = [i * int(x) for i, x in enumerate(cut_disk_map)]

    print(''.join(result_disk_map))
    print(''.join(cut_disk_map))

    return sum(result)

def part2(input):
    disk_map, disk_map_compressed = convert_input(input)
    result_disk_map = deepcopy(disk_map_compressed)

    right_index = len(result_disk_map) - 1
    left_index = 0
    while right_index>0:
        disk_file = result_disk_map[right_index] #going from right
        empty_space_index = find_empty_space_index(result_disk_map[:right_index], disk_file_size=disk_file.size)

        print(empty_space_index, disk_file, result_disk_map)

        if empty_space_index == -1: # no empty space can fit the file
            right_index -= 1
            continue

        empty_space = result_disk_map[empty_space_index] #going from left
        if type(disk_file) == EmptySpace:
            right_index -= 1
            continue


        empty_space_size = empty_space.size
        disk_file_size = disk_file.size
        disk_file_id = disk_file.file_id

        if empty_space_size==disk_file_size:
            result_disk_map[empty_space_index] = DiskFile(file_id=disk_file_id, size=disk_file_size)
            result_disk_map[right_index] = EmptySpace(size=empty_space_size)
            right_index -= 1
        elif empty_space_size > disk_file_size:
            result_disk_map[empty_space_index] = EmptySpace(size=empty_space_size -disk_file_size)
            result_disk_map[right_index] = EmptySpace(size=disk_file_size)
            result_disk_map.insert(empty_space_index, DiskFile(file_id=disk_file_id, size=disk_file_size))
            # right_index -= 1
        else:
            print('Unhandled line')
            break
        time.sleep(1)

    decompressed_result = decompress_disk_map(result_disk_map)
    result = sum([i * int(x) for i, x in enumerate(decompressed_result) if x!= '.'])

    print(result_disk_map)
    print(decompressed_result)
    print(result)
    return result

def find_empty_space_index(compressed_disk_map, disk_file_size):
    for i, x in enumerate(compressed_disk_map):
        if type(x) == EmptySpace and x.size >= disk_file_size:
            return i
    return -1



def decompress_disk_map(compressed_disk_map):
    decompressed_disk_map = []
    for x in compressed_disk_map:
        if type(x) == DiskFile:
            decompressed_disk_map.extend(x.size * [str(x.file_id)])
        elif type(x) == EmptySpace:
            decompressed_disk_map.extend(x.size * ['.'])

    return ''.join(decompressed_disk_map)

def get_index_of_last_id(converted_input):
    index = len(converted_input) - 1
    while index >= 0:
        if is_int(converted_input[index]):
            return index
        index -= 1

    return -1


def is_int_after_dot(l1, l2):
    return l1 == '.' and is_int(l2)


def is_int(letter):
    try:
        int(letter)
        return True
    except ValueError:
        return False


def convert_input(input_line):
    disk_map = []
    disk_map_compressed = []
    block_id = 0
    for i, letter in enumerate(input_line):
        num = int(letter)

        if i % 2 == 0:
            disk_map.extend(num * [str(block_id)])
            disk_map_compressed.append(DiskFile(file_id=str(block_id), size=num))
            block_id += 1
        else:
            disk_map.extend(num * ['.'])
            if num != 0:
                disk_map_compressed.append(EmptySpace(size=num))
            # disk_map_compressed.extend((, num))

    print(disk_map)
    return disk_map, disk_map_compressed




@timeit
def run():
    input_line = read_file(PATH)[0]

    print(input_line)
    # result = part1(input_line)
    result = part2(input_line)

    return result


if __name__ == '__main__':
    result = run()
    print('Result:', result)
