# --- Day 13: Claw Contraption ---
import itertools
import re
from collections import defaultdict

import numpy as np
from sympy import symbols, Eq, solve

from utils.utils import timeit, read_file_with_ints

PATH = 'data/day13.txt'
TEST_PATH = 'data/test/day13.txt'


def p1(machines):
    tokens = 0
    for machine in machines:
        a, b, correct = solve_equation_v2(**machine)
        if correct:
            tokens += 3 * a + b

    return tokens


def p2(machines):
    tokens = 0
    for machine in machines:
        machine['c1'] += 10000000000000
        machine['c2'] += 10000000000000

        a, b, correct = solve_equation_v2(**machine)
        if correct:
            tokens += 3 * a + b

    return tokens


def solve_equation_v2(x1, y1, c1, x2, y2, c2):
    A, B = symbols('a b')
    eq1 = Eq(x1 * A + x2 * B, c1)  # Total X achieved
    eq2 = Eq(y1 * A + y2 * B, c2)  # Total Y achieved
    solution = solve([eq1, eq2], (A, B))
    a, b = float(solution[symbols('a')]), float(solution[symbols('b')])

    try:
        if not round(a, 8).is_integer() or not round(b, 8).is_integer():
            # print(f"{a}, {b}: Numbers are not integers.")
            return -1, -1, False

        return int(a), int(b), True
    except np.linalg.LinAlgError:
        # print("The system of equations cannot be solved (matrix is singular).")
        return -1, -1, False


def read_sectioned_file(path):
    machines = []
    with open(path) as f:
        sections_split = [section.split('\n') for section in f.read().split('\n\n')]
        for section in sections_split:
            x1, y1 = get_numbers_after_sign(section[0], '+')
            x2, y2 = get_numbers_after_sign(section[1], '+')
            c1, c2 = get_numbers_after_sign(section[2], '=')
            machines.append({'x1': int(x1), 'y1': int(y1), 'x2': int(x2), 'y2': int(y2), 'c1': int(c1), 'c2': int(c2)})

    return machines


def get_numbers_after_sign(line, sign):
    line_split = line.split(sign)[1:]
    n1 = int(line_split[0].split(',')[0].strip())
    n2 = int(line_split[1].strip())

    return n1, n2


@timeit
def run():
    machines = read_sectioned_file(PATH)
    print(machines)
    p1_result = p1(machines)
    p2_result = p2(machines)

    return p1_result, p2_result


if __name__ == '__main__':
    p1, p2 = run()
    print('P1 result:', p1)
    print('P2 result:', p2)
