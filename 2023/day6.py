# --- Day 6: Wait For It ---
from utils.utils import read_inline_sectioned_file
import functools
import operator

PATH = 'data/day6.txt'
PATH_part2 = 'data/day6_part2.txt'


def get_mult_number_of_ways_to_win_part1(data):
    winning_ways = []
    for time, distance in zip(data['Time'], data['Distance']):
        winning_numbers = [(x, calculate_distance(x, time)) for x in range(time) if calculate_distance(x, time) > distance]
        winning_ways.append(len(winning_numbers))

    return functools.reduce(operator.mul, winning_ways)


def run():
    data = read_inline_sectioned_file(PATH, int)
    data_part2 = read_inline_sectioned_file(PATH_part2, int)

    # result = get_mult_number_of_ways_to_win_part1(data)
    result = get_mult_number_of_ways_to_win_part1(data_part2)

    return result


def calculate_distance(time_passed, total_time):
    v = time_passed
    time_left = total_time - time_passed
    return v * time_left


if __name__ == '__main__':
    result = run()
    print('Result:', result)
