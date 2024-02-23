from typing import Set, List

from Card import Card


class Agent:
    def __init__(self, hand: List[Card]):
        self.hand = hand

    def make_move(self, current_round):
        if len(current_round) == 0:
            return
