# --- Day 4: Ceres Search ---
from utils.utils import find_all, read_file, timeit, read_file_with_ints
from collections import Counter
import re
import numpy as np

PATH = 'data/day4.txt'


def parse_int(s):
    try:
        return int(s)
    except ValueError:
        return None


def part1(word, letter_map):
    word_reversed = word[::-1]
    count = find_word_occurrence(word, letter_map) + find_word_occurrence(word_reversed, letter_map)

    return count


def part2(letter_map):
    return sum(is_xmas(x, y, letter_map) for x in range(letter_map.shape[1]) for y in range(letter_map.shape[0]))


def find_word_occurrence(word, letter_map):
    letter_map_t = letter_map.T
    letter_map_flipped = np.flipud(letter_map)

    horizontal_counts = sum(substring_count(word, line) for line in letter_map)
    vertical_counts = sum(substring_count(word, line) for line in letter_map_t)

    # diagonal
    diagonal = [letter_map.diagonal(offset=offset) for offset in range(-letter_map.shape[0], letter_map.shape[1])]  # bottom left to top right
    diagonal_flipped = [letter_map_flipped.diagonal(offset=offset) for offset in range(-letter_map_flipped.shape[0], letter_map_flipped.shape[1])]  # top left to bottom right

    diagonal_counts = sum(substring_count(word, line) for line in diagonal)
    diagonal_flipped_counts = sum(substring_count(word, line) for line in diagonal_flipped)

    print(horizontal_counts, vertical_counts, diagonal_counts, diagonal_flipped_counts)
    return horizontal_counts + vertical_counts + diagonal_counts + diagonal_flipped_counts


def is_xmas(x, y, letter_map):
    if x + 2 >= letter_map.shape[1] or y + 2 >= letter_map.shape[0]:
        return False

    return (letter_map[y, x] == 'M' and letter_map[y + 2, x + 2] == 'S' and letter_map[y + 1, x + 1] == 'A' and letter_map[y + 2, x] == 'M' and letter_map[y, x + 2] == 'S') or \
        (letter_map[y, x] == 'M' and letter_map[y + 2, x + 2] == 'S' and letter_map[y + 1, x + 1] == 'A' and letter_map[y + 2, x] == 'S' and letter_map[y, x + 2] == 'M') or \
        (letter_map[y, x] == 'S' and letter_map[y + 2, x + 2] == 'M' and letter_map[y + 1, x + 1] == 'A' and letter_map[y + 2, x] == 'M' and letter_map[y, x + 2] == 'S') or \
        (letter_map[y, x] == 'S' and letter_map[y + 2, x + 2] == 'M' and letter_map[y + 1, x + 1] == 'A' and letter_map[y + 2, x] == 'S' and letter_map[y, x + 2] == 'M')


def substring_count(word, line):
    s = ''.join(line)
    return len(re.findall(word, s))


# @timeit
def run():
    letters = read_file(PATH)
    test_letters = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""".split('\n')
    print(test_letters)

    letter_map = np.array([list(line) for line in letters])
    # letter_map = np.array([list(line) for line in test_letters])
    print(letter_map)
    WORD = 'XMAS'
    # result = part1(WORD, letter_map)
    result = part2(letter_map)

    return result


if __name__ == '__main__':
    result = run()
    print('Result:', result)
