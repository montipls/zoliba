if __name__ == 'game':
    import random

    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['1', '2', '3', '4']
    deck = []
    pull = []
    rank_map = {
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 1
    }

    # storing all cards in deck
    for suit in suits:
        for rank in ranks:
            deck.append(rank+suit)

    # shuffling deck
    random.shuffle(deck)

    # creating empty stacks
    stacks = [
        [],
        [],
        [],
        []
    ]
