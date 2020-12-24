from random import shuffle
from enum import Enum

class CardType(Enum):
  person = 1
  weapon = 2
  location = 3


cards = [
    {
        'name' : 'Irene',
        'type' : CardType.person
    },
    {
        'name' : 'Michael',
        'type' : CardType.person
    },
    {
        'name' : 'Chase',
        'type' : CardType.person
    },
    {
        'name' : 'gun',
        'type' : CardType.weapon
    },
    {
        'name' : 'knife',
        'type' : CardType.weapon
    },
    {
        'name' : 'club',
        'type' : CardType.weapon
    },
    {
        'name' : 'Hell',
        'type' : CardType.location
    },
    {
        'name' : 'Lounge',
        'type' : CardType.location
    },
    {
        'name' : 'Heaven',
        'type' : CardType.location
    }
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
