from random import shuffle
from enum import Enum

class CardType(Enum):
  person = 1
  weapon = 2
  location = 3


cards = [
    {
        'name' : 'Chili Czar',
        'type' : CardType.person
    },
    {
        'name' : 'Chainsaw',
        'type' : CardType.person
    },
    {
        'name' : 'Damage Control',
        'type' : CardType.person
    },
    {
        'name': 'Bookie',
        'type': CardType.person
    },
    {
        'name': 'Head Waiter',
        'type': CardType.person
    },
    {
        'name': 'Frosh',
        'type': CardType.person
    },
    {
        'name': 'Potato Cannon',
        'type': CardType.weapon
    },
    {
        'name': 'Lead Brick',
        'type': CardType.weapon
    },
    {
        'name': 'The Ride',
        'type': CardType.weapon
    },
    {
        'name': 'Epoxy Quesadilla',
        'type': CardType.weapon
    },
    {
        'name': 'Snek',
        'type': CardType.weapon
    },
    {
        'name': 'The Presidential Democracy Axe',
        'type': CardType.weapon
    },
    {
        'name': 'Tapestry',
        'type': CardType.location
    },
    {
        'name': 'Gondor',
        'type': CardType.location
    },
    {
        'name': 'Hell',
        'type': CardType.location
    },
    {
        'name': 'Library',
        'type': CardType.location
    },
    {
        'name': 'Tool Room',
        'type': CardType.location
    },
    {
        'name': 'Pub Kitchen',
        'type': CardType.location
    },
]



class Card():
  def __init__(self, name, type):
    self.name = name
    self.type = type

def createShuffledDeck():
    deck = []

    for card in cards:
        deck.append(Card(card['name'], card['type']))

    shuffle(deck)
    return deck
