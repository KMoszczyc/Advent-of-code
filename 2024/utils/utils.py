import time
from functools import wraps
import re
from collections import defaultdict
import multiprocessing
import numpy as np


def read_file(path):
    with open(path, "r") as f:
        return f.read().split('\n')

def read_file_by_split(path, split):
    with open(path, "r") as f:
        return f.read().split(split)

def read_file_with_ints(path):
    with open(path, "r") as f:
        lines = f.read().split('\n')

        parsed_lines = [[int(num) for num in line.split()] for line in lines]
        return parsed_lines


def read_str_grid_file(path):
    with open(path, "r") as f:
        lines = f.read().split('\n')
        return np.array([list(line) for line in lines])


def read_parted_file(path):
    """Read a file that has seperated lines into sections, such as:
    bla bla:
    3785633182 3505718598 362876274
    368447204 930285729 6647073

    temperature-to-humidity map:
    645925588 927807414 87140162
    0 398577479 157531253
    ...
    """
    print('hello1')
    with open(path, "r") as f:
        lines = f.read().split('\n')
        sectioned_lines = defaultdict(list)
        current_section = ''
        for line in lines:
            if ':' in line:
                line_split = line.strip().split(': ')
                current_section = line_split[0].replace(':', '')
                if len(line_split) > 1:
                    sectioned_lines[current_section] = [line_split[1].strip()]
                    continue
            elif line != '':
                sectioned_lines[current_section].append(line)

        return sectioned_lines


def read_inline_sectioned_file(path, type):
    """input:
    Time:        55     82     64     90
    Distance:   246   1441   1012   1111

    output:{ 'Time': [55, 82, 64, 90],
    ...}

    """
    with open(path, "r") as f:
        raw_lines = f.read().split('\n')
        sections = {}
        for line in raw_lines:
            print(line)
            section_key, data = line.split(':')
            sections[section_key] = [type(value) for value in data.split()]
        return sections


def find_all(s, pattern):
    """Yields all the positions of the pattern p in the string s."""
    # i = s.find(p)
    # while i != -1:
    #     yield i
    #     i = s.find(p, i + 1)
    return [idx for idx, s in enumerate(s) if pattern in s]


def find_all_numbers(line):
    return {m.start(0): int(m.group(0)) for m in re.finditer("\d+", line)}


def find_all_numbers_as_str(line):
    return {m.start(0): m.group(0) for m in re.finditer("\d+", line)}


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result

    return timeit_wrapper


@timeit
def parallel_processing(func, start, data_size, threads_num):
    processes = []
    thread_data_size = int(data_size / threads_num)
    for i in range(threads_num):
        data_start = start + thread_data_size * i
        data_end = data_start + thread_data_size

        process = multiprocessing.Process(target=func, args=(data_start, data_end))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()
