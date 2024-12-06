# --- Day 1: Historian Hysteria ---
from utils.utils import find_all, read_file, timeit, read_file_with_ints
from collections import Counter
import re

PATH = 'data/day3.txt'


def parse_int(s):
    try:
        return int(s)
    except ValueError:
        return None


def part1(code):
    pattern = re.compile(r"mul\((\d+),(\d+)\)", re.IGNORECASE)
    return sum(int(x) * int(y) for x, y in re.findall(pattern, code))


def part2(code):
    do = r"do\(\)"
    dont = r"don't\(\)"
    mul = r"mul\((\d+),(\d+)\)"
    total = 0
    enabled = True
    for x in re.finditer(f'{do}|{dont}|{mul}', code):
        if re.fullmatch(do, x.group()):
            enabled = True
        elif re.fullmatch(dont, x.group()):
            enabled = False
        elif enabled:
            total += int(x.group(1)) * int(x.group(2))

    return total


@timeit
def run():
    code = ''.join(read_file(PATH))
    result = part1(code)
    # result = part2(code)

    return result


if __name__ == '__main__':
    result = run()
    print('Result:', result)
