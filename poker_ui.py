import tkinter as tk
from tkinter import messagebox
from poker_game import PokerGame
from card_ui import create_card_display

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

        self.player_hand_frame = tk.Frame(self.master)
        self.player_hand_frame.pack()

        self.community_cards_label = tk.Label(self.master, text="Community Cards:")
        self.community_cards_label.pack()

        self.community_cards_frame = tk.Frame(self.master)
        self.community_cards_frame.pack()

        self.pot_label = tk.Label(self.master, text="Pot: $0")
        self.pot_label.pack()

        self.player_chips_label = tk.Label(self.master, text="Your Chips: $1000")
        self.player_chips_label.pack()

        self.computer_chips_label = tk.Label(self.master, text="Computer Chips: $1000")
        self.computer_chips_label.pack()

        self.action_frame = tk.Frame(self.master)
        self.action_frame.pack()

        self.fold_button = tk.Button(self.action_frame, text="Fold", command=lambda: self.player_action("fold"))
        self.fold_button.pack(side=tk.LEFT)

        self.check_button = tk.Button(self.action_frame, text="Check", command=lambda: self.player_action("check"))
        self.check_button.pack(side=tk.LEFT)

        self.bet_button = tk.Button(self.action_frame, text="Bet", command=self.open_bet_window)
        self.bet_button.pack(side=tk.LEFT)

        self.deal_button = tk.Button(self.master, text="Deal", command=self.deal)
        self.deal_button.pack()

        self.new_game_button = tk.Button(self.master, text="New Game", command=self.new_game)
        self.new_game_button.pack()

        self.cheatsheet_button = tk.Button(self.master, text="Cheatsheet", command=self.show_cheatsheet)
        self.cheatsheet_button.pack()

        self.message_label = tk.Label(self.master, text="")
        self.message_label.pack()

    def deal(self):
        self.game.deal_initial_hands()
        self.update_display()
        self.deal_button.config(state=tk.DISABLED)
        self.enable_action_buttons()

    def player_action(self, action, amount=0):
        result = self.game.player_action(action, amount)
        self.message_label.config(text=f"Player {result}")
        self.update_display()
        if action == "fold":
            self.show_results("Computer wins!")
            self.master.after(2000, self.new_game)
        else:
            self.game.next_player()
            self.bot_turn()

    def bot_turn(self):
        result = self.game.bot_action()
        self.message_label.config(text=f"Computer {result}")
        self.update_display()
        if result == "fold":
            self.show_results("Player wins!")
            self.master.after(2000, self.new_game)
        else:
            self.game.next_player()
            self.next_stage()

    def next_stage(self):
        if self.game.stage == "preflop":
            self.game.deal_flop()
        elif self.game.stage == "flop":
            self.game.deal_turn()
        elif self.game.stage == "turn":
            self.game.deal_river()
        elif self.game.stage == "river":
            self.game.stage = "showdown"
            self.show_results()
        self.update_display()

    def show_results(self, message=None):
        if message:
            self.message_label.config(text=message)
        else:
            # For simplicity, we'll just compare the last card of each player
            player_card = self.game.get_player_hand()[-1]
            computer_card = self.game.get_computer_hand()[-1]
            if player_card.value > computer_card.value:
                self.message_label.config(text="You win!")
            elif player_card.value < computer_card.value:
                self.message_label.config(text="Computer wins!")
            else:
                self.message_label.config(text="It's a tie!")
        self.disable_action_buttons()

    def new_game(self):
        self.game.reset_game()
        self.update_display()
        self.deal_button.config(state=tk.NORMAL)
        self.disable_action_buttons()
        self.message_label.config(text="")

    def update_display(self):
        player_hand = self.game.get_player_hand()
        for widget in self.player_hand_frame.winfo_children():
            widget.destroy()
        create_card_display(self.player_hand_frame, player_hand).pack()

        community_cards = self.game.get_community_cards()
        for widget in self.community_cards_frame.winfo_children():
            widget.destroy()
        create_card_display(self.community_cards_frame, community_cards).pack()

        self.pot_label.config(text=f"Pot: ${self.game.pot}")
        self.player_chips_label.config(text=f"Your Chips: ${self.game.players[0].chips}")
        self.computer_chips_label.config(text=f"Computer Chips: ${self.game.players[1].chips}")

    def open_bet_window(self):
        bet_window = tk.Toplevel(self.master)
        bet_window.title("Place Your Bet")

        bet_label = tk.Label(bet_window, text="Enter bet amount:")
        bet_label.pack()

        bet_entry = tk.Entry(bet_window)
        bet_entry.pack()

        confirm_button = tk.Button(bet_window, text="Confirm", command=lambda: self.confirm_bet(bet_entry.get(), bet_window))
        confirm_button.pack()

    def confirm_bet(self, amount, window):
        try:
            amount = int(amount)
            if amount > 0 and amount <= self.game.players[0].chips:
                self.player_action("bet", amount)
                window.destroy()
            else:
                tk.messagebox.showerror("Invalid Bet", "Please enter a valid bet amount.")
        except ValueError:
            tk.messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def enable_action_buttons(self):
        self.fold_button.config(state=tk.NORMAL)
        self.check_button.config(state=tk.NORMAL)
        self.bet_button.config(state=tk.NORMAL)

    def disable_action_buttons(self):
        self.fold_button.config(state=tk.DISABLED)
        self.check_button.config(state=tk.DISABLED)
        self.bet_button.config(state=tk.DISABLED)

    def show_cheatsheet(self):
        cheatsheet = """
        Poker Hand Rankings:
        1. Royal Flush: A, K, Q, J, 10 of the same suit
        2. Straight Flush: Five consecutive cards of the same suit
        3. Four of a Kind: Four cards of the same rank
        4. Full House: Three of a kind plus a pair
        5. Flush: Any five cards of the same suit
        6. Straight: Five consecutive cards of any suit
        7. Three of a Kind: Three cards of the same rank
        8. Two Pair: Two different pairs
        9. One Pair: Two cards of the same rank
        10. High Card: Highest card plays if no other hand
        """
        messagebox.showinfo("Poker Hand Rankings", cheatsheet)

if __name__ == "__main__":
    root = tk.Tk()
    app = PokerUI(root)
    root.mainloop()
