# --- Day 1: Historian Hysteria ---
from utils.utils import find_all, read_file, timeit, read_file_with_ints
from collections import Counter

PATH = 'data/day2.txt'


def is_report_safe_part1(numbers: list):
    """Returns 1 if the report is safe, 0 if not."""
    ascending_global = None
    result = 1
    for i in range(len(numbers) - 1):
        num1, num2 = numbers[i], numbers[i + 1]
        ascending_local = is_ascending(num1, num2)

        if ascending_global is None:
            ascending_global = ascending_local

        if ascending_global != ascending_local or not is_number_pair_within_boundries(num1, num2):
            result = 0
            break

    return result


def is_report_safe_part2(numbers: list):
    if is_report_safe_part1(numbers) == 1:
        return 1

    for i in range(len(numbers)):
        numbers_cut = numbers[:]
        numbers_cut.pop(i)
        result = is_report_safe_part1(numbers_cut)

        if result == 1:
            return 1

    return 0


def is_number_pair_within_boundries(num1, num2):
    diff = abs(num2 - num1)
    return diff >= 1 and diff <= 3


def is_ascending(num1, num2):
    diff = num2 - num1
    return diff > 0


def part1(lines: list[list]):
    return sum(is_report_safe_part1(line) for line in lines)


def part2(lines: list[list]):
    return sum(is_report_safe_part2(line) for line in lines)


@timeit
def run():
    lines = read_file_with_ints(PATH)

    # result = part1(lines)
    result = part2(lines)

    return result


if __name__ == '__main__':
    result = run()
    print('Result:', result)
