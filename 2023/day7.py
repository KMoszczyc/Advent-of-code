# --- Day 7: Camel Cards ---
from utils.utils import read_file
from enum import IntEnum
from collections import Counter

PATH = 'data/day7.txt'


card_map_part_1 = {
    'A': 'a', 'K': 'b', 'Q': 'c', 'J': 'd', 'T': 'e', '9': 'f', '8': 'g', '7': 'h', '6': 'i', '5': 'j', '4': 'k', '3': 'l', '2': 'm'
}

card_map_part_2 = {
    'A': 'a', 'K': 'b', 'Q': 'c', 'T': 'e', '9': 'f', '8': 'g', '7': 'h', '6': 'i', '5': 'j', '4': 'k', '3': 'l', '2': 'm', 'J': 'n',
}


class Hand(IntEnum):
    FIVE = 1
    FOUR = 2
    FULL = 3
    THREE = 4
    TWO_PAIR = 5
    ONE_PAIR = 6
    HIGH_CARD = 7


def get_hand_type_part_1(hand):
    hand_key, bid = hand
    card_counts = Counter(hand_key)
    sorted_cards = card_counts.most_common()
    hand_type = map_cards(sorted_cards)

    mapped_hand = ''.join([card_map_part_1[letter] for letter in hand_key])
    return (hand_key, hand_type, mapped_hand, bid)


def get_hand_type_part_2(hand):
    hand_key, bid = hand
    mapped_hand = ''.join([card_map_part_2[letter] for letter in hand_key])
    card_counts = Counter(hand_key)
    sorted_cards = card_counts.most_common()

    if 'J' in hand_key:
        most_common_card = sorted_cards[0][0]
        sorted_mapped_most_common_card_keys = []
        if card_counts['J'] != 5:
            sorted_mapped_most_common_card_keys = [(key, value) for key, value in sorted_cards if key != 'J']

            most_common_card = sorted_mapped_most_common_card_keys[0][0]
            card_counts[most_common_card] = min(5, card_counts[most_common_card] + card_counts['J'])
            card_counts['J'] = 0

        print('J', hand_key, sorted_cards, sorted_mapped_most_common_card_keys, card_counts, most_common_card)

    hand_type = map_cards(card_counts.most_common())
    print(hand_type)

    return (hand_key, hand_type, mapped_hand, bid)


def map_cards(sorted_cards):
    if sorted_cards[0][1] == 5:
        hand_type = Hand.FIVE
    elif sorted_cards[0][1] == 4:
        hand_type = Hand.FOUR
    elif sorted_cards[0][1] == 3 and sorted_cards[1][1] == 2:
        hand_type = Hand.FULL
    elif sorted_cards[0][1] == 3 and sorted_cards[1][1] == 1:
        hand_type = Hand.THREE
    elif sorted_cards[0][1] == 2 and sorted_cards[1][1] == 2:
        hand_type = Hand.TWO_PAIR
    elif sorted_cards[0][1] == 2 and sorted_cards[1][1] == 1:
        hand_type = Hand.ONE_PAIR
    else:
        hand_type = Hand.HIGH_CARD

    return hand_type


def get_total_winnings(hands):
    sorted_hands = sorted(hands, key=lambda element: (element[1], element[2]), reverse=True)
    total_winnings = sum((i + 1) * elems[3] for i, elems in enumerate(sorted_hands))

    print(sorted_hands)

    return total_winnings


def run():
    lines = read_file(PATH)
    raw_hands = {line.split()[0]: int(line.split()[1]) for line in lines}
    # hands_part_1 = [get_hand_type_part_1(hand) for hand in raw_hands.items()]
    hands_part_2 = [get_hand_type_part_2(hand) for hand in raw_hands.items()]

    # result = get_total_winnings(hands_part_1)
    result = get_total_winnings(hands_part_2)

    return result


if __name__ == '__main__':
    result = run()
    print('Result:', result)
