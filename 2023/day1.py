# --- Day 1: Trebuchet?! ---
from utils.utils import find_all, read_file, timeit

PATH = 'data/day1.txt'
word_digits_map = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}


def get_calibration_value_part_1(encoded_line):
    digits = [s for s in encoded_line if s.isdigit()]
    first_digit = digits[0]
    last_digit = digits[-1]
    decoded_value = int(first_digit + last_digit)

    # print(encoded_line, digits, first_digit, last_digit, decoded_value)
    return decoded_value


def get_calibration_value_part_2(encoded_line):
    digits = {i: s for i, s in enumerate(encoded_line) if s.isdigit()}
    for word_digit, digit in word_digits_map.items():
        indexes = find_all(encoded_line, word_digit)
        for index in indexes:
            if index != -1:
                digits[index] = digit

    digits_keys = list(digits.keys())

    first_digit = digits[min(digits_keys)]
    last_digit = digits[max(digits_keys)]
    decoded_value = int(first_digit + last_digit)

    # print(encoded_line, digits, first_digit, last_digit, decoded_value)
    return decoded_value


@timeit
def run():
    encoded_lines = read_file(PATH)

    # calibration_values = [get_calibration_value_part_1(line) for line in encoded_lines]
    calibration_values = [get_calibration_value_part_2(line) for line in encoded_lines]

    return sum(calibration_values)


if __name__ == '__main__':
    result = run()
    print('Sum of all of the calibration values:', result)
