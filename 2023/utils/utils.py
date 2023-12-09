import time
from functools import wraps
import re

def read_file(path):
    with open(path, "r") as f:
        return f.read().split('\n')


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
