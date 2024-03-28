from typing import List


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def utility_function(self):
        if isinstance(self.value, int):
            return self.value
        elif self.value == 'J':
            return 11
        elif self.value == 'Q':
            return 12
        elif self.value == 'K':
            return 13
        elif self.value == 'A':
            return 14
        else:
            return 0

    def visual(self):
        visual_suits = {'S': '♠', 'H': '♥', 'C': '♣', 'D': '♦'}
        return f'{self.value} of {visual_suits[self.suit]}'

    def name(self):
        suit_names = {'S': 'Spade', 'H': 'Heart', 'C': 'Club', 'D': 'Diamond'}
        return f'{self.value} of {suit_names[self.suit]}'

    def __str__(self):
        return self.name()

    def __eq__(self, other):
        return (self.suit == other.suit) and (self.value == other.value)

    def __hash__(self):
        return hash(str(self))


def all_cards() -> List[Card]:
    # suits = [ 'S', 'H']  # each for clubs, spades, hearts, and diamonds suits
    suits = ['C', 'S', 'H', 'D']  # each for clubs, spades, hearts, and diamonds suits
    # value = [2, 3, 4, 5, 6, 'A']
    value = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']

    cards = []
    for s in suits:
        for v in value:
            cards.append(Card(suit=s, value=v))

    return cards
