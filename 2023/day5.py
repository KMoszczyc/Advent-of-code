# --- Day 5: If You Give A Seed A Fertilizer ---
from utils.utils import read_file, read_parted_file, timeit
from collections import defaultdict
import multiprocessing

PATH = 'data/day5.txt'
# PATH = 'data/day5_test.txt'

mapping_order = ['seed-to-soil map', 'soil-to-fertilizer map', 'fertilizer-to-water map', 'water-to-light map', 'light-to-temperature map',
                 'temperature-to-humidity map', 'humidity-to-location map']
reversed_mapping_order = mapping_order[::-1]


# print(reversed_mapping_order)


@timeit
def parallel_processing(func, data_start, data_size, seed_ranges, range_map, threads_num):
    processes = []
    thread_data_size = int(data_size / threads_num)
    queue = multiprocessing.Queue()
    ret = {'foo': -1}
    queue.put(ret)

    for i in range(threads_num):
        start = data_start + thread_data_size * i
        end = start + thread_data_size

        process = multiprocessing.Process(target=func, args=(start, end, seed_ranges, range_map, queue))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    return queue.get()


def process_seed_part1(seed, range_map):
    current_mapped_value = seed
    result_dict = {}
    for map_key in mapping_order:
        for range in range_map[map_key]:
            dst_start = range[0]
            src_start = range[1]
            range_length = range[2]

            if current_mapped_value >= src_start and current_mapped_value < src_start + range_length:
                # print(map_key, dst_start, src_start, range_length, map_number(current_mapped_value, dst_start, src_start))
                current_mapped_value = map_number(current_mapped_value, dst_start, src_start)

                break
        result_dict[map_key] = current_mapped_value

    return current_mapped_value


def reverse_search_part2(location, range_map):
    current_mapped_value = location
    result_dict = {}
    for map_key in reversed_mapping_order:
        for range in range_map[map_key]:
            dst_start = range[1]
            src_start = range[0]
            range_length = range[2]

            if current_mapped_value >= src_start and current_mapped_value < src_start + range_length:
                # print(map_key, dst_start, src_start, range_length, map_number(current_mapped_value, dst_start, src_start))
                current_mapped_value = map_number(current_mapped_value, dst_start, src_start)

                break
        result_dict[map_key] = current_mapped_value
    # print(result_dict)
    return current_mapped_value


def slow_solve_part2(seed_ranges, range_map):
    location_num = 0
    potential_seed = reverse_search_part2(location_num, range_map)
    while not is_potential_seed_in_range(potential_seed, seed_ranges):
        location_num += 1
        potential_seed = reverse_search_part2(location_num, range_map)

        # if location_num % 100000 == 0:
        #     print(f'{location_num}: still nope :<')
    return location_num


@timeit
def fast_solve_part_2(seed_ranges, range_map):
    data_size = 15000000  # 15 mln
    threads = 15

    for i in range(10):
        data_start = data_size * i
        queue = parallel_processing(solve_subrange_part2, data_start, data_size, seed_ranges, range_map, threads_num=threads)
        print(queue)
        if len(queue) > 1:
            del queue['foo']
            return min(queue.values())

    return -1


def solve_subrange_part2(start, end, seed_ranges, range_map, queue):
    for location_num in range(start, end, 1):
        potential_seed = reverse_search_part2(location_num, range_map)
        if is_potential_seed_in_range(potential_seed, seed_ranges):
            potential_seed = reverse_search_part2(location_num, range_map)

            ret = queue.get()
            ret[potential_seed] = location_num
            queue.put(ret)
            return

        # if location_num % 100000 == 0:
        #     print(f'{location_num}: still nope :<')


def is_potential_seed_in_range(potential_seed, seed_ranges):
    for i in range(0, len(seed_ranges), 2):
        if potential_seed >= seed_ranges[i] and potential_seed < seed_ranges[i] + seed_ranges[i + 1]:
            return True
    return False


def get_seeds_part_2(seeds_part_1):
    """NOPE"""
    seeds_part_2 = []
    for i in range(0, len(seeds_part_1), 2):
        seeds_part_2 += list(range(seeds_part_1[i], seeds_part_1[i] + seeds_part_1[i + 1], 1))
    return seeds_part_2


def map_number(number, dst_start, src_start):
    range_diff = dst_start - src_start
    return number + range_diff


def run():
    sectioned_lines = read_parted_file(PATH)
    seeds_part_1 = str_line_to_int_list(sectioned_lines['seeds'][0])
    del sectioned_lines['seeds']
    range_map = format_sectioned_lines(sectioned_lines)

    # locations = [process_seed_part1(seed, range_map) for seed in seeds_part_1]
    # min_location = min(locations)

    min_location = fast_solve_part_2(seeds_part_1, range_map)

    print(min_location)
    return min_location


def format_sectioned_lines(sectioned_lines):
    range_map = defaultdict(list)

    for section_key, lines in sectioned_lines.items():
        for line in sectioned_lines[section_key]:
            range_map[section_key].append(str_line_to_int_list(line))

    return range_map


def str_line_to_int_list(line):
    return [int(elem) for elem in line.split()]


if __name__ == '__main__':
    result = run()

    print('Result:', result)

    # 160.3752 seconds