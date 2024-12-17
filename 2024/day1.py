# --- Day 1: Historian Hysteria ---
from utils.utils import timeit, read_file_with_ints
from collections import Counter

PATH = 'data/day1.txt'

def part1(lines):
    left = sorted([line[0] for line in lines])
    right = sorted([line[1] for line in lines])
    diffs = [abs(right[i] - left[i]) for i in range(len(left))]
    return sum(diffs)

def part2(lines):
    left = [line[0] for line in lines]
    right = [line[1] for line in lines]

    counts = Counter(right)
    scores = [num*counts[num] for num in left if num in right]

    return sum(scores)

@timeit
def run():
    lines = read_file_with_ints(PATH)

    # result = part1(lines)
    result = part2(lines)

    return result


if __name__ == '__main__':
    result = run()
    print('Sum of all of the calibration values:', result)