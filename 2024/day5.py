# --- Day 4: Ceres Search ---
from utils.utils import find_all, read_file, timeit, read_file_with_ints, read_file_by_split
from collections import Counter
import re
import numpy as np

PATH = 'data/day5.txt'
TEST_PATH = 'data/test/day5.txt'


def part1(rules, updates):
    middle_numbers = []
    for update in updates:
        correct = is_update_correct(update, rules)

        if correct:
            index = len(update) // 2
            middle_numbers.append(update[index])

    return sum(middle_numbers)


def does_rule_exist(page1, page2, rules):
    return any(page1 == rule[0] and page2 == rule[1] for rule in rules)


def part2(rules, updates):
    middle_numbers = []
    for update in updates:
        correct = is_update_correct(update, rules)

        if not correct:
            fixed_update = fix_update(update, rules)
            print(update, fixed_update)
            index = len(fixed_update) // 2
            middle_numbers.append(fixed_update[index])

    return sum(middle_numbers)


def is_update_correct(update, rules):
    correct = True
    for i in range(len(update) - 1):
        if does_rule_exist(update[i], update[i + 1], rules):
            continue

        correct = False
        break
    return correct


def fix_update(update, rules):
    fixed_update = update.copy()
    index = 0
    while index < len(fixed_update) - 1:
        if does_rule_exist(fixed_update[index], fixed_update[index + 1], rules):
            index += 1
            continue
        page1 = fixed_update[index]
        page2 = fixed_update[index + 1]

        fixed_update[index], fixed_update[index + 1] = page2, page1
        index=0
    return fixed_update


def read(path):
    raw_lines = read_file_by_split(path, '\n\n')

    rules = [line.split('|') for line in raw_lines[0].split('\n')]
    updates = [line.split(',') for line in raw_lines[1].split('\n')]

    rules = [[int(num) for num in rule] for rule in rules]
    updates = [[int(num) for num in update] for update in updates]

    print(rules)
    print(updates)
    return rules, updates


# @timeit
def run():
    rules, updates = read(PATH)

    # result = part1(rules, updates)
    result = part2(rules, updates)

    return result


if __name__ == '__main__':
    result = run()
    print('Result:', result)
