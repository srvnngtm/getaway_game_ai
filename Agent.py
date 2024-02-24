import random
from typing import Set, List

from Card import Card


class RandomAgent:

    def __init__(self, name):
        self.hand = []
        self.name = name

    def accept_card(self, card: Card):
        self.hand.append(card)

    def accept_card_list(self, cards: List[Card]):
        self.hand.extend(cards)

    def _random_picker(self, cards):
        return cards, cards.pop(random.randrange(len(cards)))

    def make_move(self, current_round: List[Card]):
        if len(current_round) == 0:
            curr_list, popped_card = self._random_picker(self.hand)
            self.hand = curr_list
            return popped_card

        else:
            suit_in_play = current_round[0].suit

            suit_cards = [card for card in self.hand if card.suit == suit_in_play]
            non_suit_cards = [card for card in self.hand if card.suit != suit_in_play]

            if len(suit_cards) == 0:
                curr_list, popped_card = self._random_picker(self.hand)
                self.hand = curr_list
                return popped_card
            else:
                curr_list, popped_card = self._random_picker(suit_cards)
                self.hand = [card for card in non_suit_cards]
                self.hand.extend(curr_list)
                return popped_card

    def has_spade_ace(self):
        if len([card for card in self.hand if (card.suit == 'S' and card.value=='A') ]) >0:
            return True
        return False