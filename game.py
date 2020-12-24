from card_data import CardType, Card, createShuffledDeck


class Guess():
    def __init__(self, person, weapon, location):
        self.person = person
        self.weapon = weapon
        self.location = location
    

class Game():
  def __init__(self, channel_id, signup_message_id):
    self.channel_id = channel_id
    self.signup_message_id = signup_message_id

    self.deck = createShuffledDeck()
    self.answer = createAnswer()

    # Fill in on game start
    self.players = set()

  def createAnswer(self):
    selected_cards = {}
    needed_types = set(CardType.person, CardType.weapon, CardType.location)
    for card in self.deck:
        if card.type in needed_types:
            needed_types.remove(card.type)

            self.deck.remove(card)
            selected_cards[card.type] = card
    return Guess(selected_cards[CardType.person], 
                 selected_cards[CardType.weapon], 
                 selected_cards[CardType.location])


  def enrollPlayer(self, user):
    self.players.add(user)

  def startGame(self):
    # Divide cards amongst players
    card_allotment = {}

    # Message players their cards



  
      