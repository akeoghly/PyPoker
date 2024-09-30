import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(suit, value) for suit in suits for value in values]
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        return None

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.chips = 1000
        self.current_bet = 0

    def add_card(self, card):
        self.hand.append(card)

    def clear_hand(self):
        self.hand = []

    def place_bet(self, amount):
        if amount <= self.chips:
            self.chips -= amount
            self.current_bet += amount
            return amount
        return 0

    def fold(self):
        self.hand = []

def evaluate_hand(cards):
    # This is a simplified hand evaluation function
    # It returns the rank of the hand (0-9, where 0 is the highest hand)
    values = [card.value for card in cards]
    suits = [card.suit for card in cards]
    
    # Check for flush
    if len(set(suits)) == 1:
        return 4  # Flush
    
    # Check for pairs, three of a kind, etc.
    value_counts = {value: values.count(value) for value in set(values)}
    if 4 in value_counts.values():
        return 3  # Four of a kind
    elif 3 in value_counts.values() and 2 in value_counts.values():
        return 4  # Full house
    elif 3 in value_counts.values():
        return 6  # Three of a kind
    elif list(value_counts.values()).count(2) == 2:
        return 7  # Two pair
    elif 2 in value_counts.values():
        return 8  # One pair
    else:
        return 9  # High card

class PokerGame:
    def __init__(self):
        self.deck = Deck()
        self.players = [Player("Player"), Player("Computer")]
        self.community_cards = []
        self.pot = 0
        self.current_player = 0
        self.stage = "preflop"
        self.small_blind = 5
        self.big_blind = 10
        self.dealer_index = 0

    def deal_initial_hands(self):
        self.post_blinds()
        for _ in range(2):
            for player in self.players:
                player.add_card(self.deck.draw())

    def post_blinds(self):
        small_blind_index = (self.dealer_index + 1) % len(self.players)
        big_blind_index = (self.dealer_index + 2) % len(self.players)
        
        self.players[small_blind_index].place_bet(self.small_blind)
        self.players[big_blind_index].place_bet(self.big_blind)
        self.pot += self.small_blind + self.big_blind

    def next_dealer(self):
        self.dealer_index = (self.dealer_index + 1) % len(self.players)

    def deal_flop(self):
        self.community_cards = [self.deck.draw() for _ in range(3)]
        self.stage = "flop"

    def deal_turn(self):
        self.community_cards.append(self.deck.draw())
        self.stage = "turn"

    def deal_river(self):
        self.community_cards.append(self.deck.draw())
        self.stage = "river"

    def reset_game(self):
        self.deck = Deck()
        for player in self.players:
            player.clear_hand()
            player.current_bet = 0
        self.community_cards = []
        self.pot = 0
        self.current_player = 0
        self.stage = "preflop"

    def get_player_hand(self):
        return self.players[0].hand

    def get_computer_hand(self):
        return self.players[1].hand

    def get_community_cards(self):
        return self.community_cards

    def player_action(self, action, amount=0):
        player = self.players[self.current_player]
        opponent = self.players[(self.current_player + 1) % 2]
        if action == "fold":
            player.fold()
            opponent.chips += self.pot
            self.pot = 0
            return "fold"
        elif action == "check":
            return "check"
        elif action == "bet":
            bet_amount = player.place_bet(amount)
            self.pot += bet_amount
            return f"bet {bet_amount}"

    def bot_action(self):
        actions = ["fold", "check", "bet"]
        action = random.choice(actions)
        if action == "bet":
            amount = random.randint(10, 100)
            return self.player_action(action, amount)
        return self.player_action(action)

    def next_player(self):
        self.current_player = (self.current_player + 1) % len(self.players)

    def next_stage(self):
        if self.stage == "preflop":
            self.deal_flop()
        elif self.stage == "flop":
            self.deal_turn()
        elif self.stage == "turn":
            self.deal_river()
        elif self.stage == "river":
            self.stage = "showdown"
