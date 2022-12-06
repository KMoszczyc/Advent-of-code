games = {
    'loses' : ['AC', 'BA', 'CB'],
    'draws' : ['AA', 'BB', 'CC'],
    'wins' : ['CA', 'AB', 'BC'],
}

def calculate_score():
    with open("2022/data/day2.txt", "r") as f:
        raw_games = f.read().splitlines()

        # part1
        # games_cleaned = [xyz_to_abc(game) for game in raw_games]

        # part2
        games_cleaned = [apply_strategy(game.replace(' ', '')) for game in raw_games]

        game_scores = [calculate_round(game) for game in games_cleaned]
        total_score = sum(game_scores)

        print(raw_games)
        print(games_cleaned)
        print(game_scores)

        return total_score

def apply_strategy(moves):
    """X - lose, Y - draw, Z - win, example input AX, BY .."""
    player1_move = moves[0]    #ABC
    player2_move = moves[1]    #XYZ
    strategy = {'X': 'loses', 'Y': 'draws', 'Z': 'wins'}

    return [x for x in games[strategy[player2_move]] if player1_move == x[0]][0]

def calculate_round(game):
    """Calculate round score from player2 perspective"""
    # A - rock, B - paper, C - scissors
    base_punctation = {'A': 1, 'B': 2, 'C': 3}


    score = base_punctation[game[1]]

    if game in games['wins']:
        score += 6
    elif game in games['draws']:
        score += 3
    elif game in games['loses']:
        score += 0

    return score


def xyz_to_abc(txt):
    return txt.replace('X', 'A').replace('Y', 'B').replace('Z', 'C').replace(' ', '')


if __name__ == '__main__':
    result = calculate_score()

    print('Total score:', result)
