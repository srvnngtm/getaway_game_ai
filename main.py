import random

from Agent import RandomAgent
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
p1 = RandomAgent('p1')
p2 = RandomAgent('p2')
p3 = RandomAgent('p3')
p4 = RandomAgent('p4')


players = [p1, p2, p3, p4]


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


