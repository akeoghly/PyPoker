import tkinter as tk
from poker_game import PokerGame

class PokerUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Simple Poker Game")
        self.game = PokerGame()

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        self.player_hand_label = tk.Label(self.master, text="Your Hand:")
        self.player_hand_label.pack()

        self.player_hand_display = tk.Label(self.master, text="")
        self.player_hand_display.pack()

        self.community_cards_label = tk.Label(self.master, text="Community Cards:")
        self.community_cards_label.pack()

        self.community_cards_display = tk.Label(self.master, text="")
        self.community_cards_display.pack()

        self.deal_button = tk.Button(self.master, text="Deal", command=self.deal)
        self.deal_button.pack()

        self.next_button = tk.Button(self.master, text="Next", command=self.next_stage, state=tk.DISABLED)
        self.next_button.pack()

        self.new_game_button = tk.Button(self.master, text="New Game", command=self.new_game)
        self.new_game_button.pack()

    def deal(self):
        self.game.deal_initial_hands()
        self.update_display()
        self.deal_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)

    def next_stage(self):
        if len(self.game.community_cards) == 0:
            self.game.deal_flop()
        elif len(self.game.community_cards) == 3:
            self.game.deal_turn()
        elif len(self.game.community_cards) == 4:
            self.game.deal_river()
            self.next_button.config(state=tk.DISABLED)
        self.update_display()

    def new_game(self):
        self.game.reset_game()
        self.update_display()
        self.deal_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.DISABLED)

    def update_display(self):
        player_hand = self.game.get_player_hand()
        self.player_hand_display.config(text=", ".join(str(card) for card in player_hand))

        community_cards = self.game.get_community_cards()
        self.community_cards_display.config(text=", ".join(str(card) for card in community_cards))

if __name__ == "__main__":
    root = tk.Tk()
    app = PokerUI(root)
    root.mainloop()
