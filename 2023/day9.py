# --- Day 9: Mirage Maintenance ---
from utils.utils import read_file_with_ints

PATH = 'data/day9.txt'

def solve(numbers_history, part_mode):
    """part_mode = [part_1, part_2]"""
    extrapolated_values = []
    for numbers in numbers_history:
        number_diffs_list = [numbers]
        while True:
            number_diffs_list.append(create_diff_list(number_diffs_list[-1]))

            if are_diffs_zero(number_diffs_list[-1]):
                break

        print('numbers:', numbers)
        if part_mode == 'part_1':
            extrapolated_values.append(extrapolate_diff_value_part_1(number_diffs_list))
        elif part_mode == 'part_2':
            extrapolated_values.append(extrapolate_diff_value_part_2(number_diffs_list))

    return sum(extrapolated_values)


def extrapolate_diff_value_part_1(number_diffs_list):
    number_diffs_list_reversed = number_diffs_list[::-1]
    for i, number_diffs in enumerate(number_diffs_list_reversed):
        if i == 0:
            number_diffs_list_reversed[i].append(0)
        else:
            new_value = number_diffs_list_reversed[i][-1] + number_diffs_list_reversed[i-1][-1]
            number_diffs_list_reversed[i].append(new_value)

    print(number_diffs_list_reversed[-1][-1], number_diffs_list_reversed)
    return number_diffs_list_reversed[-1][-1]

def extrapolate_diff_value_part_2(number_diffs_list):
    number_diffs_list_reversed = number_diffs_list[::-1]
    for i, number_diffs in enumerate(number_diffs_list_reversed):
        if i == 0:
            number_diffs_list_reversed[i].insert(0,0)
        else:
            new_value = number_diffs_list_reversed[i][0] - number_diffs_list_reversed[i-1][0]
            number_diffs_list_reversed[i].insert(0, new_value)

    print(number_diffs_list_reversed[-1][0], number_diffs_list_reversed)
    return number_diffs_list_reversed[-1][0]


def create_diff_list(numbers):
    number_diffs = []
    for i in range(len(numbers) - 1):
        number_diffs.append(numbers[i + 1] - numbers[i])
    return number_diffs


def are_diffs_zero(numbers):
    return len([num for num in numbers if num == 0]) == len(numbers)


def run():
    numbers_history = read_file_with_ints(PATH)
    # result = solve(numbers_history, 'part_1')
    result = solve(numbers_history, 'part_2')

    return result


if __name__ == '__main__':
    result = run()
    print('Result:', result)
