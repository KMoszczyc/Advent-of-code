# --- Day 2: Cube Conundrum ---
from utils.utils import find_all, read_file, timeit

RED_CUBES_THRESHOLD = 12
GREEN_CUBES_THRESHOLD = 13
BLUE_CUBES_THRESHOLD = 14

cube_count_thresholds = {'red':12, 'green':13,'blue':14}
PATH = 'data/day2.txt'

def preprocess_line(line):
    game_str, cubes_str = line.split(': ')
    game_id = int(game_str.split(' ')[1])

    cubes_split_str = cubes_str.replace(';', ',').split(', ')
    return game_id, cubes_split_str

def get_game_id_part_1(line):
    """If game is possible then get game ID, if not then return 0"""
    game_id, cubes_split_str = preprocess_line(line)
    # cube_counts = {'red':0, 'green':0,'blue':0}

    for elem in cubes_split_str:
        count_str, color = elem.split(' ')
        count = int(count_str)
        if count > cube_count_thresholds[color]:
            return 0

    return game_id

def get_game_power_part_2(line):
    """Get the fewest number of cubes of each color and multiply all of these numbers together (red * green * blue)"""
    game_id, cubes_split_str = preprocess_line(line)
    cube_counts = {'red':0, 'green':0,'blue':0}

    for elem in cubes_split_str:
        count_str, color = elem.split(' ')
        count = int(count_str)
        if count > cube_counts[color]:
            cube_counts[color] = count

    return cube_counts['red'] * cube_counts['green'] * cube_counts['blue']

def run():
    encoded_lines = read_file(PATH)

    # result = sum(get_game_id_part_1(line) for line in encoded_lines)
    result = sum(get_game_power_part_2(line) for line in encoded_lines)

    return result


if __name__ == '__main__':
    result = run()
    print('Result:', result)
