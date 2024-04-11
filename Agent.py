import random
from typing import Set, List

from Card import Card, all_cards

import numpy as np
from collections import defaultdict
import pickle
from multiprocessing import Pool
from functools import partial


class Agent:

    def __init__(self, name):
        self.hand = []
        self.name = name
        self.hand_count = 0

    def accept_card(self, card: Card):
        self.hand.append(card)
        self.hand_count += 1

    def accept_card_list(self, cards: List[Card]):
        self.hand.extend(cards)
        self.hand_count += len(cards)

    def has_spade_ace(self):
        if len([card for card in self.hand if (card.suit == 'S' and card.value == 'A')]) > 0:
            return True
        return False

    def is_play_over(self):
        return self.hand_count == 0

    def clear_agent(self):
        self.hand = []
        self.hand_count = 0

    def announce_round(self, cards, taker):
        pass

    def calculate_score(self):
        return sum([card.utility_function() for card in self.hand])


class RandomAgent(Agent):

    def _random_picker(self, cards):
        # if(len(cards) == 0):
        #     print("here")

        l = len(cards)
        # print(l)
        r = random.randrange(l)
        return cards, cards.pop(r)

    def make_move(self, current_round_dict: dict[Card, str], **kwargs) -> (Card, bool):
        # print(f"{self.name}  : {len(self.hand)}")
        current_round = list(current_round_dict.keys())

        if len(current_round) == 0:
            curr_list, popped_card = self._random_picker(self.hand)
            self.hand = curr_list

            self.hand_count -= 1
            return popped_card, False

        else:
            suit_in_play = current_round[0].suit

            suit_cards= []
            non_suit_cards = []
            for card in self.hand:
                if card.suit == suit_in_play:
                    suit_cards.append(card)
                else:
                    non_suit_cards.append(card)


            if len(suit_cards) == 0:
                curr_list, popped_card = self._random_picker(self.hand)
                self.hand = curr_list

                self.hand_count -= 1
                return popped_card, True
            else:
                curr_list, popped_card = self._random_picker(suit_cards)
                self.hand = [card for card in non_suit_cards]
                self.hand.extend(curr_list)

                self.hand_count -= 1
                return popped_card, False

    def copy(self, name):
        copy_agent = RandomAgent(name)
        copy_agent.hand = [i for i in self.hand]
        copy_agent.hand_count = self.hand_count
        return copy_agent


class GreedyAgent(Agent):
    def copy(self, name):
        copy_agent = GreedyAgent(name)
        copy_agent.hand = [i for i in self.hand]
        copy_agent.hand_count = self.hand_count
        return copy_agent

    def _random_picker(self, cards):
        max_card = max(cards, key=lambda x: x.utility_function())
        max_index = cards.index(max_card)

        return cards, cards.pop(max_index)

    def make_move(self, current_round_dict: dict[Card, str], **kwargs) -> (Card, bool):
        current_round = list(current_round_dict.keys())

        if len(current_round) == 0:
            curr_list, popped_card = self._random_picker(self.hand)
            self.hand = curr_list

            self.hand_count -= 1
            return popped_card, False

        else:
            suit_in_play = current_round[0].suit

            suit_cards= []
            non_suit_cards = []
            for card in self.hand:
                if card.suit == suit_in_play:
                    suit_cards.append(card)
                else:
                    non_suit_cards.append(card)

            if len(suit_cards) == 0:
                curr_list, popped_card = self._random_picker(self.hand)
                self.hand = curr_list

                self.hand_count -= 1
                return popped_card, True
            else:
                curr_list, popped_card = self._random_picker(suit_cards)
                self.hand = [card for card in non_suit_cards]
                self.hand.extend(curr_list)

                self.hand_count -= 1
                return popped_card, False


class GreedyMinAgent(Agent):

    def copy(self, name):
        copy_agent = GreedyMinAgent(name)
        copy_agent.hand = [i for i in self.hand]
        copy_agent.hand_count = self.hand_count
        return copy_agent

    def _random_picker(self, cards):
        # if(len(cards) == 0):
        #     print("here")

        min_card = min(cards, key=lambda x: x.utility_function())
        min_index = cards.index(min_card)

        return cards, cards.pop(min_index)

    def make_move(self, current_round_dict: dict[Card, str], **kwargs) -> (Card, bool):
        current_round = list(current_round_dict.keys())

        if len(current_round) == 0:
            curr_list, popped_card = self._random_picker(self.hand)
            self.hand = curr_list

            self.hand_count -= 1
            return popped_card, False

        else:
            suit_in_play = current_round[0].suit

            suit_cards= []
            non_suit_cards = []
            for card in self.hand:
                if card.suit == suit_in_play:
                    suit_cards.append(card)
                else:
                    non_suit_cards.append(card)

            if len(suit_cards) == 0:
                curr_list, popped_card = self._random_picker(self.hand)
                self.hand = curr_list

                self.hand_count -= 1
                return popped_card, True
            else:
                curr_list, popped_card = self._random_picker(suit_cards)
                self.hand = [card for card in non_suit_cards]
                self.hand.extend(curr_list)

                self.hand_count -= 1
                return popped_card, False


class GreedySmartAgent(Agent):
    """
    Returns a min card if normal turn,
     but returns a max card if its breaking a turn
    """

    def copy(self, name):
        copy_agent = GreedySmartAgent(name)
        copy_agent.hand = [i for i in self.hand]
        copy_agent.hand_count = self.hand_count
        return copy_agent

    def _random_picker(self, cards, brk):

        if brk:
            card = max(cards, key=lambda x: x.utility_function())
            ind = cards.index(card)
        else:
            card = min(cards, key=lambda x: x.utility_function())
            ind = cards.index(card)
        return cards, cards.pop(ind)

    def make_move(self, current_round_dict: dict[Card, str], **kwargs) -> (Card, bool):
        current_round = list(current_round_dict.keys())

        if len(current_round) == 0:
            curr_list, popped_card = self._random_picker(self.hand, False)
            self.hand = curr_list
            self.hand_count -= 1
            return popped_card, False

        else:
            suit_in_play = current_round[0].suit

            suit_cards= []
            non_suit_cards = []
            for card in self.hand:
                if card.suit == suit_in_play:
                    suit_cards.append(card)
                else:
                    non_suit_cards.append(card)

            if len(suit_cards) == 0:
                curr_list, popped_card = self._random_picker(self.hand, True)
                self.hand = curr_list
                self.hand_count -= 1
                return popped_card, True
            else:
                curr_list, popped_card = self._random_picker(suit_cards, False)
                self.hand = [card for card in non_suit_cards]
                self.hand.extend(curr_list)
                self.hand_count -= 1
                return popped_card, False


# def zero():
#     return 0
#
#
# def dd():
#     return defaultdict(zero)


class QLearningAgent(Agent):
    Q = {}
    num_updates = {}

    def __init__(self, name):
        super().__init__(name)
        self.all_cards_set = set(all_cards())

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


    def copy(self, name):
        copy_agent = QLearningAgent(name)
        copy_agent.hand = [i for i in self.hand]
        copy_agent.hand_count = self.hand_count
        return copy_agent

    played_cards = []

    def announce_round(self, cards, taker):
        # need to work with taker, so we know some of the cards each player has
        self.played_cards.extend(cards)

    def simulator(self, my_card, current_round_dict: dict[Card, str]) -> float:
        value = 0.0

        current_round_dict[my_card] = 'p4'

        environment = {}
        all_players = {'p1', 'p2', 'p3', 'p4'}
        # all_players = {'p1', 'p3', 'p4'}
        environment['p1'] = GreedyMinAgent('p1')
        environment['p2'] = RandomAgent('p2')
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

    def simulator_open(self, my_card, current_round_dict: dict[Card, str], **kwargs) -> float:
        value = -10.0

        current_round_dict[my_card] = self.name

        environment = {}
        all_players = {'p1', 'p2', 'p3', 'p4'}

        for k, v in kwargs.items():
            if k != self.name:
                environment[k] = v.copy(k)


        # cards_remaining = (self.all_cards_set - set(self.played_cards)) - set(self.hand)

        # if len(cards_remaining) < len(all_players):
        #     return value

        is_round_terminated = False
        cards_played_in_round = list(current_round_dict.keys())
        simulated_cards_in_round = []

        remaining_players = list(all_players - set(current_round_dict.values()))
        # random.shuffle(remaining_players)
        for player_name in remaining_players:

            player = environment.get(player_name)
            if player.is_play_over():
                continue
            played_card, is_round_terminated = player.make_move(current_round_dict)
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
            # if max_player == self.name:
            #     value -= 100
            # else:
            #     # reward for causing another player to lose
            #     value += 20

        # else:
        #     max_card = max(cards_played_in_round, key=lambda x: x.utility_function())
        #     max_player = current_round_dict[max_card]
        #
        #     # penalize for being the biggest card in the round
        #     if max_player == 'p4':
        #         value -= 10

            # add reward for playing making players play small cards
        if len(simulated_cards_in_round) > 0:
            additional = sum([x.utility_function() for x in simulated_cards_in_round]) / len(
                simulated_cards_in_round)
            value += additional

        over = [player.is_play_over() for player in environment.values()]

        if any(over):
            if not self.is_play_over():
                value -= 2000
            else :
                value += 2000


        # if len(self.hand) == 0 or len(self.hand) == 1:
        #     value += 2000

        return value



    # def open_sim_wrapper(self, action, current_round_dict, **kwargs):
    #     reward = 0
    #     for i in range(10):
    #         reward += self.simulator_open(action, current_round_dict, **kwargs)
    #     return  reward/4


    def smart_sim_open(self, my_card, current_round_dict: dict[Card, str], **kwargs) -> float:
        value = 0.0

        current_round_dict[my_card] = 'p4'

        environment = {}
        all_players = {'p1', 'p2', 'p3', 'p4'}

        for k, v in kwargs.items():
            if k != 'p4':
                environment[k] = v

        # cards = set(all_cards())
        # cards_remaining = list((cards - set(self.played_cards)) - set(self.hand))
        #
        # if len(cards_remaining) < len(all_players):
        #     return value

        is_round_terminated = False
        cards_played_in_round = list(current_round_dict.keys())
        simulated_cards_in_round = []

        remaining_players = list(all_players - set(current_round_dict.values()))
        # random.shuffle(remaining_players)
        for player_name in remaining_players:

            player = environment.get(player_name)
            if player.is_play_over():
                continue
            played_card, is_round_terminated = player.make_move(current_round_dict)

            # no copy, so put the card back
            player.accept_card(played_card)

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

            # add reward for playing making players play small cards
        # if len(simulated_cards_in_round) > 0:
        #     additional = sum([x.utility_function() for x in simulated_cards_in_round]) / len(
        #         simulated_cards_in_round)
        #     value += additional

        if len(self.hand) == 0 or len(self.hand) == 1:
            value += 2000

        return value

    def _picker(self, cards, current_round_dict, brk, **kwargs):

        # max case :
        if brk:
            card = max(cards, key=lambda x: x.utility_function())
            ind = cards.index(card)
            return cards, cards.pop(ind)

        state = tuple(self.hand)

        rewards_for_cards = {}

        for action in cards:
            reward = 0
            for i in range(5):
                reward += self.simulator_open(action, current_round_dict, **kwargs)
                # reward += self.smart_sim_open(action, current_round_dict, **kwargs)
            rewards_for_cards[action] = (reward/4)

        for card in cards:
            action = card
            # Q[state][action] = value
            state_actions = self.Q.get(state, dict({}))

            # reward = self.simulator(card, current_round_dict)
            # reward = self.simulator_open(action, current_round_dict, **kwargs)

            reward = rewards_for_cards[action]
            updates = self.num_updates.get(state, dict({})).get(action, 0)

            curr_value = state_actions.get(action, 0)
            eta = 1 / (1 + updates)

            next_action = tuple([c for c in state if c != action])

            next_state_actions = self.Q.get(next_action, dict({})).items()
            V_opt_next_state = max(next_state_actions, key=lambda x: x[1])[1] if len(next_state_actions) > 0 else 0

            q_value = ((1 - eta) * curr_value) + (eta * (reward + V_opt_next_state))

            next_state_actions = self.Q.get(next_action, dict({}))
            next_state_actions[action] = q_value
            self.Q[state] = next_state_actions

            updates_dict = self.num_updates.get(state, dict({}))
            updates_dict[action] = updates + 1
            self.num_updates[state] = updates_dict

        max_val = float('-inf')
        card_to_pick = None

        state_action_values = self.Q.get(state, dict({}))
        for card in cards:
            if state_action_values.get(card, 0) > max_val:
                card_to_pick = card
                max_val = state_action_values.get(card, 0)

        # card_to_pick_list =
        # card_to_pick = max(card_to_pick_list, key=card_to_pick_list.get)

        probability = random.random()
        if probability < 0.2:
            card_to_pick = random.choice(cards)

        cards.remove(card_to_pick)


        return cards, card_to_pick

    def make_move(self, current_round_dict: dict[Card, str], **kwargs) -> (Card, bool):
        current_round = list(current_round_dict.keys())

        if len(current_round) == 0:
            curr_list, popped_card = self._picker(self.hand, current_round_dict, False, **kwargs)
            self.hand = curr_list
            self.hand_count -= 1
            return popped_card, False

        else:
            suit_in_play = current_round[0].suit

            suit_cards= []
            non_suit_cards = []
            for card in self.hand:
                if card.suit == suit_in_play:
                    suit_cards.append(card)
                else:
                    non_suit_cards.append(card)

            if len(suit_cards) == 0:
                curr_list, popped_card = self._picker(self.hand, current_round_dict, True, **kwargs)
                self.hand = curr_list
                self.hand_count -= 1
                return popped_card, True
            else:
                curr_list, popped_card = self._picker(suit_cards, current_round_dict, False, **kwargs)
                self.hand = [card for card in non_suit_cards]
                self.hand.extend(curr_list)
                self.hand_count -= 1
                return popped_card, False
