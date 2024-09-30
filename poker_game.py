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

    def add_card(self, card):
        self.hand.append(card)

    def clear_hand(self):
        self.hand = []

class PokerGame:
    def __init__(self):
        self.deck = Deck()
        self.players = [Player("Player"), Player("Computer")]
        self.community_cards = []

    def deal_initial_hands(self):
        for _ in range(2):
            for player in self.players:
                player.add_card(self.deck.draw())

    def deal_flop(self):
        self.community_cards = [self.deck.draw() for _ in range(3)]

    def deal_turn(self):
        self.community_cards.append(self.deck.draw())

    def deal_river(self):
        self.community_cards.append(self.deck.draw())

    def reset_game(self):
        self.deck = Deck()
        for player in self.players:
            player.clear_hand()
        self.community_cards = []

    def get_player_hand(self):
        return self.players[0].hand

    def get_computer_hand(self):
        return self.players[1].hand

    def get_community_cards(self):
        return self.community_cards
