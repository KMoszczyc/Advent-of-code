# --- Day 8: Haunted Wasteland ---
from utils.utils import read_file
from enum import IntEnum
from collections import Counter
from collections import deque, defaultdict
import time
import math

PATH = 'data/day8.txt'
# PATH = 'data/day8_test.txt'


def bfs_part2(network, instructions):
    """Brute force, not working :((((("""
    root_nodes = [node for node in list(network.keys()) if node[-1] == 'A']
    step_count = 0
    i = 0
    instructions_num = len(instructions)

    # visited = {k: False for k in list(network.keys())}
    bfs_queue = deque(['VBA'])
    # visited[root] = True
    print(root_nodes, bfs_queue)

    while not are_we_at_destination(list(bfs_queue)):
        if i == instructions_num:
            i = 0

        instruction = instructions[i]
        curent_queue = bfs_queue.copy()
        for node in curent_queue:
            children = network[node]
            bfs_queue.popleft()
            if instruction == 'L':
                bfs_queue.append(children[0])
            elif instruction == 'R':
                bfs_queue.append(children[1])

        # print(node, children, instruction, bfs_queue)

        step_count += 1
        i += 1

        if step_count % 1000000 == 0:
            print('Step:', step_count)
        time.sleep(1)

def find_number_of_steps_part2(network, instructions, current_node):
    """LCM approach"""
    step_count = 0
    i = 0
    instructions_num = len(instructions)

    while not is_z_node(current_node):
        if i == instructions_num:
            i = 0

        instruction = instructions[i]
        children = network[current_node]

        if instruction == 'L':
            current_node = children[0]
        elif instruction == 'R':
            current_node = children[1]

        step_count += 1
        i += 1

        if step_count % 1000000 == 0:
            print('Step:', step_count)

    return step_count

def solve_part_2(network, instructions):
    """LCM approach"""
    root_nodes = [node for node in list(network.keys()) if node[-1] == 'A']
    steps = [find_number_of_steps_part2(network, instructions, node) for node in root_nodes]
    lcm = math.lcm(*steps)
    print(root_nodes, steps)

    return lcm

def is_z_node(node):
    return node[-1] == 'Z'

def are_we_at_destination(nodes):
    z_nodes = [node for node in nodes if node[-1] == 'Z']
    return len(nodes) == len(z_nodes)


def find_number_of_steps_to_reach_destination_part_1(network, instructions):
    root = 'AAA'
    destination = 'ZZZ'

    step_count = 0
    i = 0
    instructions_num = len(instructions)
    current_node = root
    print(len(instructions))
    while current_node != destination:
        if i == instructions_num:
            i = 0

        instruction = instructions[i]
        children = network[current_node]
        if instruction == 'L':
            current_node = children[0]
        elif instruction == 'R':
            current_node = children[1]

        step_count += 1
        i += 1

        if step_count % 10000000 == 0:
            print('Step:', step_count)

    return step_count


def parse_input_data(lines):
    instructions = lines[0]

    network = {}
    for line in lines[2:]:
        node, lr_str = line.split(' = ')
        left, right = lr_str.replace('(', '').replace(')', '').replace(',', '').split()
        network[node] = [left, right]

    return network, instructions


def run():
    lines = read_file(PATH)
    network, instructions = parse_input_data(lines)
    # result = find_number_of_steps_to_reach_destination_part_1(network, instructions)
    result = solve_part_2(network, instructions)

    return result


if __name__ == '__main__':
    result = run()
    print('Result:', result)
