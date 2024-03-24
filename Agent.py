import random
from typing import Set, List

from Card import Card, all_cards

import numpy as np
from collections import defaultdict
import pickle


class Agent:
    def __init__(self, name):
        self.hand = []
        self.name = name

    def accept_card(self, card: Card):
        self.hand.append(card)

    def accept_card_list(self, cards: List[Card]):
        self.hand.extend(cards)

    def has_spade_ace(self):
        if len([card for card in self.hand if (card.suit == 'S' and card.value == 'A')]) > 0:
            return True
        return False

    def is_play_over(self):
        return len(self.hand) == 0

    def clear_agent(self):
        self.hand = []

    def announce_round(self, cards, taker):
        pass


class RandomAgent(Agent):

    def _random_picker(self, cards):

        l = len(cards)
        # print(l)
        r= random.randrange(l)
        return cards, cards.pop(r)

    def make_move(self, current_round_dict: dict[Card, str]) -> (Card, bool):
        # print(f"{self.name}  : {len(self.hand)}")
        current_round = list(current_round_dict.keys())

        if len(current_round) == 0:
            curr_list, popped_card = self._random_picker(self.hand)
            self.hand = curr_list
            return popped_card, False

        else:
            suit_in_play = current_round[0].suit

            suit_cards = [card for card in self.hand if card.suit == suit_in_play]
            non_suit_cards = [card for card in self.hand if card.suit != suit_in_play]

            if len(suit_cards) == 0:
                curr_list, popped_card = self._random_picker(self.hand)
                self.hand = curr_list
                return popped_card, True
            else:
                curr_list, popped_card = self._random_picker(suit_cards)
                self.hand = [card for card in non_suit_cards]
                self.hand.extend(curr_list)
                return popped_card, False


class GreedyAgent(Agent):
    def _random_picker(self, cards):
        max_card = max(cards, key=lambda x: x.utility_function())
        max_index = cards.index(max_card)

        return cards, cards.pop(max_index)

    def make_move(self, current_round_dict: dict[Card, str]) -> (Card, bool):
        current_round = list(current_round_dict.keys())

        if len(current_round) == 0:
            curr_list, popped_card = self._random_picker(self.hand)
            self.hand = curr_list
            return popped_card, False

        else:
            suit_in_play = current_round[0].suit

            suit_cards = [card for card in self.hand if card.suit == suit_in_play]
            non_suit_cards = [card for card in self.hand if card.suit != suit_in_play]

            if len(suit_cards) == 0:
                curr_list, popped_card = self._random_picker(self.hand)
                self.hand = curr_list
                return popped_card, True
            else:
                curr_list, popped_card = self._random_picker(suit_cards)
                self.hand = [card for card in non_suit_cards]
                self.hand.extend(curr_list)
                return popped_card, False


class GreedyMinAgent(Agent):
    def _random_picker(self, cards):
        min_card = min(cards, key=lambda x: x.utility_function())
        min_index = cards.index(min_card)

        return cards, cards.pop(min_index)

    def make_move(self, current_round_dict: dict[Card, str]) -> (Card, bool):
        current_round = list(current_round_dict.keys())

        if len(current_round) == 0:
            curr_list, popped_card = self._random_picker(self.hand)
            self.hand = curr_list
            return popped_card, False

        else:
            suit_in_play = current_round[0].suit

            suit_cards = [card for card in self.hand if card.suit == suit_in_play]
            non_suit_cards = [card for card in self.hand if card.suit != suit_in_play]

            if len(suit_cards) == 0:
                curr_list, popped_card = self._random_picker(self.hand)
                self.hand = curr_list
                return popped_card, True
            else:
                curr_list, popped_card = self._random_picker(suit_cards)
                self.hand = [card for card in non_suit_cards]
                self.hand.extend(curr_list)
                return popped_card, False


class GreedySmartAgent(Agent):
    """
    Returns a min card if normal turn,
     but returns a max card if its breaking a turn
    """

    def _random_picker(self, cards, brk):

        if brk:
            card = max(cards, key=lambda x: x.utility_function())
            ind = cards.index(card)
        else:
            card = min(cards, key=lambda x: x.utility_function())
            ind = cards.index(card)

        return cards, cards.pop(ind)

    def make_move(self, current_round_dict: dict[Card, str]) -> (Card, bool):
        current_round = list(current_round_dict.keys())

        if len(current_round) == 0:
            curr_list, popped_card = self._random_picker(self.hand, False)
            self.hand = curr_list
            return popped_card, False

        else:
            suit_in_play = current_round[0].suit

            suit_cards = [card for card in self.hand if card.suit == suit_in_play]
            non_suit_cards = [card for card in self.hand if card.suit != suit_in_play]

            if len(suit_cards) == 0:
                curr_list, popped_card = self._random_picker(self.hand, True)
                self.hand = curr_list
                return popped_card, True
            else:
                curr_list, popped_card = self._random_picker(suit_cards, False)
                self.hand = [card for card in non_suit_cards]
                self.hand.extend(curr_list)
                return popped_card, False


def zero():
    return 0


def dd():
    return defaultdict(zero)


class MCTSAgent(Agent):
    Q = defaultdict(dd)
    num_updates = defaultdict(dd)

    def __init__(self, name):
        super().__init__(name)

        try:
            with open('q_values', 'rb') as file:
                # Deserialize and retrieve the variable from the file
                self.Q = pickle.load(file)

        except:
            print("couldn't reload q value")

        try:
            with open('num_updates', 'rb') as file:
                # Deserialize and retrieve the variable from the file
                self.num_updates = pickle.load(file)

        except:
            print("couldn't reload num updates")


    played_cards = []

    def announce_round(self, cards, taker):
        # need to work with taker, so we know some of the cards each player has
        self.played_cards.extend(cards)

    def simulator(self, my_card, current_round_dict: dict[Card, str]) -> float:
        value = 0.0

        current_round_dict[my_card] = 'p4'

        environment = {}
        # all_players = {'p1', 'p2', 'p3', 'p4'}
        all_players = {'p1', 'p3', 'p4'}
        environment['p1'] = GreedyMinAgent('p1')
        # environment['p2'] = RandomAgent('p2')
        environment['p3'] = GreedyAgent('p3')

        cards = set(all_cards())
        cards_remaining = list((cards - set(self.played_cards)) - set(self.hand))

        if len(cards_remaining) < len(all_players):
            return value


        random.shuffle(cards_remaining)
        hands = [cards_remaining[i::len(environment)] for i in range(0, len(environment))]

        for i, player in enumerate(environment.values()):
            player.accept_card_list(list(hands[i]))

        is_round_terminated = False
        cards_played_in_round = list(current_round_dict.keys())
        simulated_cards_in_round = []

        remaining_players = list(all_players - set(current_round_dict.values()))
        random.shuffle(remaining_players)
        for player_name in remaining_players:

            played_card, is_round_terminated = environment.get(player_name).make_move(current_round_dict)
            current_round_dict[played_card] = player_name
            cards_played_in_round.append(played_card)
            simulated_cards_in_round.append(played_card)

            if is_round_terminated:
                break

        if is_round_terminated:
            non_term_cards = cards_played_in_round[:-1]
            max_card = max(non_term_cards, key=lambda x: x.utility_function())
            max_player = current_round_dict[max_card]

            # reduce value to penalize losing the round.
            if max_player == 'p4':
                value -= 50
            else:
                # reward for causing another player to lose
                value += 200

        else:
            max_card = max(cards_played_in_round, key=lambda x: x.utility_function())
            max_player = current_round_dict[max_card]

            # penalize for being the biggest card in the round
            if max_player == 'p4':
                value -= 10

            # add reward for playing making players play small cards
            if len(simulated_cards_in_round) > 0:
                additional = sum([x.utility_function() for x in simulated_cards_in_round]) / len(
                    simulated_cards_in_round)
                value += additional

        if len(self.hand) == 0 or len(self.hand) == 1:
            value += 2000

        return value

    def _picker(self, cards, current_round_dict, brk):

        # max case :
        if brk:
            card = max(cards, key=lambda x: x.utility_function())
            ind = cards.index(card)
            return cards, cards.pop(ind)

        state = tuple(self.hand)

        for card in cards:
            # if(len(state) > 3):
                # print(state)
            action = card
            # Q[state][action] = value
            state_actions = self.Q[state]

            reward = self.simulator(card, current_round_dict)

            updates = self.num_updates[state][action]
            curr_value = state_actions[action]
            eta = 1 / (1 + updates)

            next_action = tuple([c for c in state if c != card])

            next_state_actions = self.Q[next_action].items()
            V_opt_next_state = max(next_state_actions, key=lambda x: x[1])[1] if len(next_state_actions) > 0 else 0
            # print(V_opt_next_state)
            q_value = (1 - eta)*curr_value + eta*(reward + V_opt_next_state)

            self.Q[state][action] = q_value
            self.num_updates[state][action] += 1



        max_val = float('-inf')
        card_to_pick = None
        for card in cards:
            if self.Q[state][card] > max_val:
                card_to_pick = card
                max_val = self.Q[state][card]


        # card_to_pick_list =
        # card_to_pick = max(card_to_pick_list, key=card_to_pick_list.get)
        cards.remove(card_to_pick)

        return cards, card_to_pick

    def make_move(self, current_round_dict: dict[Card, str]) -> (Card, bool):
        current_round = list(current_round_dict.keys())

        if len(current_round) == 0:
            curr_list, popped_card = self._picker(self.hand, current_round_dict, False)
            self.hand = curr_list
            return popped_card, False

        else:
            suit_in_play = current_round[0].suit

            suit_cards = [card for card in self.hand if card.suit == suit_in_play]
            non_suit_cards = [card for card in self.hand if card.suit != suit_in_play]

            if len(suit_cards) == 0:
                curr_list, popped_card = self._picker(self.hand, current_round_dict, True)
                self.hand = curr_list
                return popped_card, True
            else:
                curr_list, popped_card = self._picker(suit_cards, current_round_dict, False)
                self.hand = [card for card in non_suit_cards]
                self.hand.extend(curr_list)
                return popped_card, False


