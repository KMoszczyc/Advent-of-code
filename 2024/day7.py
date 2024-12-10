# --- Day 7: Bridge Repair ---
import functools
from copy import deepcopy

from utils.utils import find_all, read_file, timeit, read_file_with_ints, read_file_by_split, read_str_grid_file, read_inline_sectioned_file_into_list_of_tuples
from collections import Counter
import itertools
import re
import numpy as np
import sys
from dataclasses import dataclass

np.set_printoptions(threshold=sys.maxsize)
PATH = 'data/day7.txt'
TEST_PATH = 'data/test/day7.txt'


def part1(calibrations, operators=['+', '*']):
    lengths = [len(numbers) for result, numbers in calibrations]
    min_operators_num, max_operators_num = min(lengths) - 1, max(lengths)
    combinations = generate_combinations(min_operators_num, max_operators_num, operators)

    result_sum = 0
    for result, numbers in calibrations:
        is_possible, operators = is_equation_possible(result, numbers, combinations[len(numbers) - 1])
        if is_possible:
            result_sum += result
    return result_sum


def is_equation_possible(source_result, numbers, operator_combinations):
    for operator_combination in operator_combinations:
        result = calculate_result(numbers, operator_combination)
        if source_result == result:
            return True, operator_combination

    return False, []


def calculate_result(numbers, operators):
    result = numbers[0]
    for i in range(1, len(numbers)):
        result = apply_operator(result, numbers[i], operators[i - 1])
    return result


def apply_operator(num1, num2, operator):
    match operator:
        case '+':
            return num1 + num2
        case '*':
            return num1 * num2
        case '||':
            return int(f"{num1}{num2}")
        case _:
            raise Exception(f'Unknown operator: {operator}')


def generate_combinations(min_operators_num, max_operators_num, available_operators):
    return {
        i: list(itertools.product(available_operators, repeat=i))
        for i in range(min_operators_num, max_operators_num)
    }


def part2(calibrations):
    return part1(calibrations, operators=['+', '*', '||'])


@timeit
def run():
    calibrations = read_inline_sectioned_file_into_list_of_tuples(PATH, int, int)
    # result = part1(calibrations)
    result = part2(calibrations)

    return result


if __name__ == '__main__':
    result = run()
    print('Result:', result)
