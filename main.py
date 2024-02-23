from Card import Card, all_cards


cards = all_cards()

for card in cards:
    print(card.visual())

for card in cards:
    print(card.name())

