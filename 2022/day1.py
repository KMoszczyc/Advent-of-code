from itertools import groupby


def get_grouped_elf_calories_sum_list():
    with open("2022/data/day1.txt", "r") as f:
        all_elf_calories = f.read().splitlines()
        i = (list(g) for _, g in groupby(all_elf_calories, key=''.__ne__))
        grouped_elf_calories = [a + b for a, b in zip(i, i)]
        return [sum(int(value) for value in elf_calories[:-1]) for elf_calories in grouped_elf_calories]

def get_max_calories():
    return max(get_grouped_elf_calories_sum_list())

def get_top_max_calories(num):
    """Num specifies number of top elves calories you want to sum."""

    sorted_summed_calories = sorted(get_grouped_elf_calories_sum_list())
    return sum(sorted_summed_calories[-num:])


if __name__ == '__main__':

    # result = get_max_calories()
    result = get_top_max_calories(3)

    print(result)
