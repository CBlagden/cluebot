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
    self.answer = self.createAnswer()

    # Fill in on game start
    self.players = set()
    self.started = False

  def createAnswer(self):
    selected_cards = {}
    needed_types = set([CardType.person, CardType.weapon, CardType.location])
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

  async def startGame(self):
    self.started = True

    # Map players to cards
    card_allotment = {}
    player_list = list(self.players)

    for player in player_list:
        card_allotment[player] = []

    idx = 0
    while len(self.deck) > 0:
        curr_player = player_list[idx % len(player_list)]
        card_allotment[curr_player].append(self.deck.pop())
        idx += 1

    # Message players their cards
    for player in player_list:
        cards = card_allotment[player]

        message_to_send = "Your cards are: " + ", ".join(card.name for card in cards)
        await player.send(message_to_send)

  def makeGuess(self, user, person, weapon, location):
      # compare the guess with the answer

      # Return if the guess was correct or not
      self.players.remove(user)
      return self.answer.person.name.lower() == person.lower() \
            and self.answer.weapon.name.lower() == weapon.lower() \
            and self.answer.location.name.lower() == location.lower()

  def isPlayerInGame(self, player):
    return player in self.players
