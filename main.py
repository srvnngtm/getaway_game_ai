import collections
import random

import Agent
from Agent import RandomAgent, GreedyAgent, GreedyMinAgent, GreedySmartAgent
from Card import Card, all_cards

# cards = all_cards()

# for card in cards:
#     print(card.visual())
#
# for card in cards:
#     print(card.name())

# gameplay


n_players = 4
# init_agents
p1 = GreedyAgent('p1')
# p2 = GreedyAgent('p2')
p3 = GreedyMinAgent('p3')
# p4 = GreedyMinAgent('p4')
p5 = RandomAgent('p5')
# p6 = RandomAgent('p6')
p7 = GreedySmartAgent('p7')
# p8 = GreedySmartAgent('p8')
# p9 = RandomAgent('p9')
# p10 = RandomAgent('p10')
# p11 = RandomAgent('p11')
# p12 = RandomAgent('p12')


players = [p1, p3,  p5, p7]
winners = []

for _ in range(1000):

    # Either do a clockwise rotation, or do a shuffle of players, to make sure there is no undercut.
    # temp1 = players[1:]
    # temp1.append(players[0])
    # players = [k for k in temp1]
    random.shuffle(players)

    # init cards
    cards = all_cards()

    # shuffle cards
    random.shuffle(cards)

    # deal cards out

    hands = [cards[i::n_players] for i in range(0, n_players)]

    for hand in hands:
        print(len(hand))

    for i in range(n_players):
        players[i].accept_card_list(hands[i])

    for each in players:
        print(f"{each.name} has Ace of space ? {each.has_spade_ace()}")




    game_in_play = True
    round_in_play = True

    player_name_dict: dict[str, Agent] = {p.name: p for p in players}

    current_order = [i.name for i in players]

    starter = players[0]
    for each in players:
        if each.has_spade_ace():
            starter = each
            break

    curr_player_index = current_order.index(starter.name)
    temp = current_order[curr_player_index:]
    temp.extend(current_order[:curr_player_index])
    current_order = [i for i in temp]
    # print(current_order)

    while game_in_play:
        print(current_order)
        cards_played_in_round = []
        is_round_terminated = False
        played_in_round_dict = {}
        for player in current_order:
            curr = player_name_dict[player]
            played_card, is_round_terminated = curr.make_move(cards_played_in_round)
            cards_played_in_round.append(played_card)
            played_in_round_dict[played_card.name()] = player
            if is_round_terminated:
                break

        # print(*cards_played_in_round, sep='\n')

        if is_round_terminated:

            non_term_cards = cards_played_in_round[:-1]
            max_card = max(non_term_cards, key=lambda x: x.utility_function())
            max_player = played_in_round_dict[max_card.name()]

            player_name_dict[max_player].accept_card_list(cards_played_in_round)


        else:
            max_card = max(cards_played_in_round, key=lambda x: x.utility_function())
            max_player = played_in_round_dict[max_card.name()]

        # print(max_player)

        max_player_index = current_order.index(max_player)

        # print(max_player_index)
        temp = current_order[max_player_index:]
        temp.extend(current_order[:max_player_index])
        current_order = [i for i in temp]

        over = [player.is_play_over() for player in players]

        if any(over):
            game_in_play = False
            winners.append(players[over.index(True)].name)



        # print(current_order)

        # for each in players:
        #     string = f"{len(each.hand)} cards left for {each.name} :: "
        #     string += ", ".join([card.name() for card in each.hand])
        #     print(string)

        print(" \n ---------------- end of round ----------------\n")

    for each in players:
        each.clear_agent()
    print("+++++++++++ end of game ++++++++++++++")
winners.sort()
print(dict(collections.Counter(winners)))

