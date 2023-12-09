# --- Day 3: Gear Ratios ---
import numpy as np
import re
from utils.utils import find_all, read_file, timeit, find_all_numbers, find_all_numbers_as_str
import itertools
from collections import Counter, defaultdict

PATH = 'data/day4.txt'


def get_points_per_card_part1(line):
    winning_numbers_str, card_numbers_str = line.split(': ')[1].split(' | ')
    winning_numbers = winning_numbers_str.split()
    card_numbers = card_numbers_str.split()

    matching_cards = [card_number for card_number in card_numbers if card_number in winning_numbers]
    count = len(matching_cards)
    value = pow(2, count - 1) if count>0 else 0

    print(winning_numbers, card_numbers, matching_cards, count, value)
    return value

def process_scratchcard_part2(line, card_count):
    winning_numbers_str, card_numbers_str = line.split(': ')[1].split(' | ')
    card_id = get_card_id(line)
    winning_numbers = winning_numbers_str.split()
    card_numbers = card_numbers_str.split()

    matching_cards = [card_number for card_number in card_numbers if card_number in winning_numbers]
    count = len(matching_cards)

    for i in range(card_id+1, card_id+count+1):
        card_count[i] += card_count[card_id]
    print(card_id, matching_cards, count, card_count)

    return card_count

def get_card_id(line):
    return int(line.split(':')[0].split()[1])

def run():
    lines = read_file(PATH)
    card_count = dict([(get_card_id(line), 1) for line in lines])
    print(card_count)

    # result = sum(get_points_per_card_part1(line) for line in lines)
    for line in lines:
        process_scratchcard_part2(line, card_count)

    result = sum(card_num for card_id, card_num in card_count.items())
    print(card_count)
    return result


if __name__ == '__main__':
    result = run()

    print('Result:', result)
