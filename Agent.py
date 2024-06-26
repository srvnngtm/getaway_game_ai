import random
from typing import Set, List

from Card import Card, all_cards

import numpy as np
from collections import defaultdict
import pickle
from multiprocessing import Pool
from functools import partial

TRAIN_MODE = False


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
        if len(self.hand)==0:
            return 0
        return sum([card.utility_function() for card in self.hand])


class RandomAgent(Agent):

    def _random_picker(self, cards):
        # if(len(cards) == 0):
        #     print("here")

        l = len(cards)
        # print(l)
        r = random.randrange(l)
        return cards, cards.pop(r)

    def make_move(self, current_round_dict: dict[Card, str],
                  player_order: List[str] = None,
                  **kwargs) -> (Card, bool):
        # print(f"{self.name}  : {len(self.hand)}")
        current_round = list(current_round_dict.keys())

        if len(current_round) == 0:
            curr_list, popped_card = self._random_picker(self.hand)
            self.hand = curr_list

            self.hand_count -= 1
            return popped_card, False

        else:
            suit_in_play = current_round[0].suit

            suit_cards = []
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

    def make_move(self, current_round_dict: dict[Card, str],
                  player_order: List[str] = None,
                  **kwargs) -> (Card, bool):
        current_round = list(current_round_dict.keys())

        if len(current_round) == 0:
            curr_list, popped_card = self._random_picker(self.hand)
            self.hand = curr_list

            self.hand_count -= 1
            return popped_card, False

        else:
            suit_in_play = current_round[0].suit

            suit_cards = []
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

    def make_move(self, current_round_dict: dict[Card, str],
                  player_order: List[str] = None,
                  **kwargs) -> (Card, bool):
        current_round = list(current_round_dict.keys())

        if len(current_round) == 0:
            curr_list, popped_card = self._random_picker(self.hand)
            self.hand = curr_list

            self.hand_count -= 1
            return popped_card, False

        else:
            suit_in_play = current_round[0].suit

            suit_cards = []
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

    def make_move(self, current_round_dict: dict[Card, str],
                  player_order: List[str] = None,
                  **kwargs) -> (Card, bool):
        current_round = list(current_round_dict.keys())

        if len(current_round) == 0:
            curr_list, popped_card = self._random_picker(self.hand, False)
            self.hand = curr_list
            self.hand_count -= 1
            return popped_card, False

        else:
            suit_in_play = current_round[0].suit

            suit_cards = []
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


class QLearningAgent(Agent):
    Q = {}
    num_updates = {}
    episode_rewards = []

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

    def simulator_open(self, my_card, current_round_dict: dict[Card, str], **kwargs) -> float:
        value = -1

        current_round_dict[my_card] = self.name

        environment = {}
        all_players = {'p1', 'p2', 'p3', 'p4'}

        for k, v in kwargs.items():
            if k != self.name:
                environment[k] = v.copy(k)

        if len(current_round_dict.values()) != 0:
            # check if current card terminates the round
            if my_card.suit != list(current_round_dict.keys())[0].suit:
                if self.hand == 1:
                    value += 100







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
            if max_player != self.name:
                environment[max_player].accept_card_list(cards_played_in_round)


        over = [player.is_play_over() for player in environment.values()]


        if any(over):
                value -= 100
        elif self.hand_count == 1:
            value += 100

        return value

    def _picker(self, cards, current_round_dict, brk, **kwargs):
        sarsa = False
        # max case :
        # if brk:
        #     card = max(cards, key=lambda x: x.utility_function())
        #     ind = cards.index(card)
        #     return cards, cards.pop(ind)

        state = tuple(self.hand)

        epsilon = 0.2

        q_current_state = {}
        state_actions = self.Q.get(state, dict({}))
        for action in cards:
            q_current_state[action] = state_actions.get(action, 0)

        # choose action based on epsilon greedy



        if(sarsa):
            # chosen_action = max(cards, key=lambda x: x.utility_function())
            chosen_action = max(q_current_state, key=q_current_state.get)
        else:
            chosen_action = max(q_current_state, key=q_current_state.get)



        # calculate reward
        # reward = self.simulator_open(chosen_action, current_round_dict, **kwargs)



        # #-----
        # rewards_for_cards = {}
        # for action in cards:
        #     reward = 0
        #     for i in range(5):
        #         reward += self.simulator_open(action, current_round_dict, **kwargs)
        #         # reward += self.smart_sim_open(action, current_round_dict, **kwargs)
        #     rewards_for_cards[action] = (reward / 5)
        #
        #
        # #-----
        #
        # chosen_action = max(rewards_for_cards, key=rewards_for_cards.get)





        if TRAIN_MODE and random.random() < epsilon:
            chosen_action = random.choice(cards)

        # calculate reward 5 times and take average
        reward =  0
        for i in range(5):
            reward += self.simulator_open(chosen_action, current_round_dict, **kwargs)
        reward = reward / 5
        # if(reward>0):
        #     print(f"reward : {reward}")

        self.episode_rewards.append(reward)

        next_state = tuple([c for c in state if c != chosen_action])
        next_state_actions = self.Q.get(next_state, dict({}))

        updates = self.num_updates.get(state, dict({})).get(chosen_action, 0)
        eta = 1 / (1 + updates)

        # standard q learning:


        # SARSA, with base policy as greedy.
        if sarsa:
            chosen_next_state_action = max(next_state, key=lambda x: x.utility_function()) if len(
                next_state_actions) > 0 else 0
            V_opt_next_state = next_state_actions.get(chosen_next_state_action, 0)
        else:
            next_state_actions = next_state_actions.items()
            V_opt_next_state = max(next_state_actions, key=lambda x: x[1])[1] if len(next_state_actions) > 0 else 0

        curr_value = state_actions.get(chosen_action, 0)

        # q_value = ((1 - eta) * curr_value) + (eta * (reward + V_opt_next_state))

        q_value = curr_value + (eta * (reward + V_opt_next_state - curr_value))

        state_actions[chosen_action] = q_value
        self.Q[state] = state_actions

        updates_dict = self.num_updates.get(state, dict({}))
        updates_dict[chosen_action] = updates + 1
        self.num_updates[state] = updates_dict

        cards.remove(chosen_action)

        return cards, chosen_action

    def make_move(self, current_round_dict: dict[Card, str],
                  player_order: List[str] = None,
                  **kwargs) -> (Card, bool):
        current_round = list(current_round_dict.keys())

        if len(current_round) == 0:
            curr_list, popped_card = self._picker(self.hand, current_round_dict, False, **kwargs)
            self.hand = curr_list
            self.hand_count -= 1
            return popped_card, False

        else:
            suit_in_play = current_round[0].suit

            suit_cards = []
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

    def clear_agent(self):
        self.hand = []
        self.hand_count = 0
        self.played_cards = []
        self.episode_rewards = []
