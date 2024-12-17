# --- Day 11: Plutonian Pebbles ---
import itertools
from collections import defaultdict
from utils.utils import timeit, read_file_with_ints

PATH = 'data/day11.txt'
TEST_PATH = 'data/test/day11.txt'


def p1(stones):
    blink_count = 25
    stones = stones.copy()
    for _ in range(blink_count):
        nested_stones = [apply_p1_rules(stone) for stone in stones]
        stones = list(itertools.chain(*nested_stones))

    return len(stones)


def p2(stones):
    blink_count = 75
    stones = {stone: 1 for stone in stones}

    for _ in range(blink_count):
        nested_stones_dicts = [apply_p2_rules(stone, count) for stone, count in stones.items()]
        stones = flatten_dict(nested_stones_dicts)
    return sum(count for stone, count in stones.items())


def apply_p1_rules(stone):
    stone_str = str(stone)
    if stone == 0:
        return [1]
    elif len(stone_str) % 2 == 0:
        part_index = (len(stone_str) + 1) // 2
        return [int(stone_str[:part_index]), int(stone_str[part_index:])]
    else:
        return [stone * 2024]


def apply_p2_rules(stone, count):
    stone_str = str(stone)
    stone_updates = {}
    if stone == 0:
        stone_updates[1] = count
    elif len(stone_str) % 2 == 0:
        part_index = (len(stone_str) + 1) // 2
        left = int(stone_str[:part_index])
        right = int(stone_str[part_index:])
        if left == right:
            stone_updates[left] = count * 2
        else:
            stone_updates[left] = count
            stone_updates[right] = count
    else:
        stone_updates[stone * 2024] = count

    return stone_updates


def flatten_dict(nested_dicts):
    flat_dict = defaultdict(int)
    for stones_nested in nested_dicts:
        for c, j in stones_nested.items():
            flat_dict[c] += j

    return flat_dict


@timeit
def run():
    stones = read_file_with_ints(PATH)[0]
    # stones = [125, 17]
    print(stones)
    p1_result = p1(stones)
    p2_result = p2(stones)

    return p1_result, p2_result


if __name__ == '__main__':
    p1, p2 = run()
    print('P1 result:', p1)
    print('P2 result:', p2)
