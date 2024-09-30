import tkinter as tk
from tkinter import messagebox, font
from poker_game import PokerGame, evaluate_hand, Card
from card_ui import create_card_display

class PokerUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Simple Poker Game")
        self.game = PokerGame()

        self.create_widgets()
        self.update_display()
        self.master.bind("<Configure>", self.on_window_resize)

    def create_widgets(self):
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        self.main_frame = tk.Frame(self.master)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        for i in range(17):  # Assuming 17 rows based on the original layout
            self.main_frame.grid_rowconfigure(i, weight=1)

        self.cheatsheet_frame = tk.Frame(self.master)
        self.cheatsheet_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.cheatsheet_frame.grid_columnconfigure(0, weight=1)
        for i in range(11):  # 11 rows for cheatsheet items
            self.cheatsheet_frame.grid_rowconfigure(i, weight=1)

        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font_size = self.default_font.cget("size")

        self.player_hand_label = tk.Label(self.main_frame, text="Your Hand:")
        self.player_hand_label.grid(row=0, column=0, sticky="w")

        self.player_hand_frame = tk.Frame(self.main_frame)
        self.player_hand_frame.grid(row=1, column=0, sticky="ew")

        self.computer_hand_label = tk.Label(self.main_frame, text="Computer's Hand:")
        self.computer_hand_label.grid(row=2, column=0, sticky="w")

        self.computer_hand_frame = tk.Frame(self.main_frame)
        self.computer_hand_frame.grid(row=3, column=0, sticky="ew")

        self.community_cards_label = tk.Label(self.main_frame, text="Community Cards:")
        self.community_cards_label.grid(row=4, column=0, sticky="w")

        self.community_cards_frame = tk.Frame(self.main_frame)
        self.community_cards_frame.grid(row=5, column=0, sticky="ew")

        self.pot_label = tk.Label(self.main_frame, text="Pot: $0")
        self.pot_label.grid(row=6, column=0, sticky="w")

        self.player_chips_label = tk.Label(self.main_frame, text="Your Chips: $1000")
        self.player_chips_label.grid(row=7, column=0, sticky="w")

        self.computer_chips_label = tk.Label(self.main_frame, text="Computer Chips: $1000")
        self.computer_chips_label.grid(row=8, column=0, sticky="w")

        self.blinds_label = tk.Label(self.main_frame, text=f"Blinds: ${self.game.small_blind}/{self.game.big_blind}")
        self.blinds_label.grid(row=9, column=0, sticky="w")

        self.dealer_label = tk.Label(self.main_frame, text="Dealer: Player")
        self.dealer_label.grid(row=10, column=0, sticky="w")

        self.action_frame = tk.Frame(self.main_frame)
        self.action_frame.grid(row=11, column=0, sticky="ew")

        self.fold_button = tk.Button(self.action_frame, text="Fold", command=lambda: self.player_action("fold"))
        self.fold_button.pack(side=tk.LEFT)

        self.check_button = tk.Button(self.action_frame, text="Check", command=lambda: self.player_action("check"))
        self.check_button.pack(side=tk.LEFT)

        self.bet_button = tk.Button(self.action_frame, text="Bet", command=self.open_bet_window)
        self.bet_button.pack(side=tk.LEFT)

        self.deal_button = tk.Button(self.main_frame, text="Deal", command=self.deal)
        self.deal_button.grid(row=12, column=0, sticky="ew")

        self.new_game_button = tk.Button(self.main_frame, text="Reset Chips", command=self.reset_chips)
        self.new_game_button.grid(row=13, column=0, sticky="ew")

        self.cheatsheet_var = tk.BooleanVar()
        self.cheatsheet_checkbox = tk.Checkbutton(self.main_frame, text="Show Cheatsheet", 
                                                  variable=self.cheatsheet_var, 
                                                  command=self.toggle_cheatsheet)
        self.cheatsheet_checkbox.grid(row=14, column=0, sticky="w")

        self.show_computer_cards_var = tk.BooleanVar()
        self.show_computer_cards_checkbox = tk.Checkbutton(self.main_frame, text="Show Computer's Cards", 
                                                           variable=self.show_computer_cards_var, 
                                                           command=self.update_display)
        self.show_computer_cards_checkbox.grid(row=15, column=0, sticky="w")

        self.message_label = tk.Label(self.main_frame, text="")
        self.message_label.grid(row=16, column=0, sticky="w")

        self.create_cheatsheet()

    def deal(self):
        self.game.reset_game()
        self.game.deal_initial_hands()
        self.update_display()
        self.deal_button.config(state=tk.DISABLED)
        self.enable_action_buttons()
        for widget in self.computer_hand_frame.winfo_children():
            widget.destroy()

    def player_action(self, action, amount=0):
        result = self.game.player_action(action, amount)
        self.message_label.config(text=f"Player {result}")
        self.update_display()
        if action == "fold":
            self.end_round("Computer wins!")
        else:
            self.game.next_player()
            self.bot_turn()

    def bot_turn(self):
        result = self.game.bot_action()
        self.message_label.config(text=f"Computer {result}")
        self.update_display()
        if result == "fold":
            self.end_round("Player wins!")
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
            self.end_round()
        self.update_display()

    def end_round(self, message=None):
        if message:
            self.message_label.config(text=message)
            if "Player wins" in message:
                self.game.player_action("win")
            elif "Computer wins" in message:
                self.game.current_player = 1  # Set to computer
                self.game.player_action("win")
        else:
            # For simplicity, we'll just compare the last card of each player
            player_hand = self.game.get_player_hand()
            computer_hand = self.game.get_computer_hand()
            if player_hand and computer_hand:
                player_card = player_hand[-1]
                computer_card = computer_hand[-1]
                if player_card.value > computer_card.value:
                    self.message_label.config(text="You win!")
                    self.game.player_action("win")
                elif player_card.value < computer_card.value:
                    self.message_label.config(text="Computer wins!")
                    self.game.current_player = 1  # Set to computer
                    self.game.player_action("win")
                else:
                    self.message_label.config(text="It's a tie!")
                    # In case of a tie, split the pot
                    self.game.players[0].chips += self.game.pot // 2
                    self.game.players[1].chips += self.game.pot // 2
                    self.game.pot = 0
            else:
                self.message_label.config(text="Round ended")
        self.disable_action_buttons()
        self.deal_button.config(state=tk.NORMAL)
        self.update_display()
        # Force show computer's cards at the end of the round
        self.show_computer_cards(True)

    def reset_chips(self):
        for player in self.game.players:
            player.chips = 1000
        self.update_display()
        self.message_label.config(text="Chips reset to $1000 for both players")

    def update_display(self):
        player_hand = self.game.get_player_hand()
        for widget in self.player_hand_frame.winfo_children():
            widget.destroy()
        if player_hand:
            create_card_display(self.player_hand_frame, player_hand).pack()

        computer_hand = self.game.get_computer_hand()
        for widget in self.computer_hand_frame.winfo_children():
            widget.destroy()
        if computer_hand:
            if self.show_computer_cards_var.get():
                create_card_display(self.computer_hand_frame, computer_hand).pack()
            else:
                # Display face-down cards for the computer's hand
                face_down_cards = [Card('', '') for _ in range(len(computer_hand))]
                create_card_display(self.computer_hand_frame, face_down_cards).pack()

        community_cards = self.game.get_community_cards()
        for widget in self.community_cards_frame.winfo_children():
            widget.destroy()
        create_card_display(self.community_cards_frame, community_cards).pack()

        # Update the checkbox state
        self.show_computer_cards_checkbox.config(state=tk.NORMAL if computer_hand else tk.DISABLED)

        self.pot_label.config(text=f"Pot: ${self.game.pot}")
        self.player_chips_label.config(text=f"Your Chips: ${self.game.players[0].chips}")
        self.computer_chips_label.config(text=f"Computer Chips: ${self.game.players[1].chips}")
        self.blinds_label.config(text=f"Blinds: ${self.game.small_blind}/{self.game.big_blind}")
        self.dealer_label.config(text=f"Dealer: {'Player' if self.game.dealer_index == 0 else 'Computer'}")

        if self.cheatsheet_var.get():
            self.update_cheatsheet()

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

    def create_cheatsheet(self):
        self.cheatsheet_labels = []
        cheatsheet_text = [
            "Poker Hand Rankings:",
            "1. Royal Flush: A, K, Q, J, 10 of the same suit",
            "2. Straight Flush: Five consecutive cards of the same suit",
            "3. Four of a Kind: Four cards of the same rank",
            "4. Full House: Three of a kind plus a pair",
            "5. Flush: Any five cards of the same suit",
            "6. Straight: Five consecutive cards of any suit",
            "7. Three of a Kind: Three cards of the same rank",
            "8. Two Pair: Two different pairs",
            "9. One Pair: Two cards of the same rank",
            "10. High Card: Highest card plays if no other hand"
        ]
        for i, line in enumerate(cheatsheet_text):
            label = tk.Label(self.cheatsheet_frame, text=line, justify=tk.LEFT, font=("Arial", 10), fg="black")
            label.grid(row=i, column=0, sticky="w")
            self.cheatsheet_labels.append(label)
        self.cheatsheet_frame.grid_remove()  # Initially hide the cheatsheet

    def toggle_cheatsheet(self):
        if self.cheatsheet_var.get():
            self.cheatsheet_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
            self.update_cheatsheet()
        else:
            self.cheatsheet_frame.grid_remove()

    def update_cheatsheet(self):
        player_hand = self.game.get_player_hand()
        community_cards = self.game.get_community_cards()
        all_cards = player_hand + community_cards
        hand_rank = evaluate_hand(all_cards)
        
        for i, label in enumerate(self.cheatsheet_labels):
            if i == 0:  # Title label
                label.config(bg="white")
            elif i == hand_rank + 1:  # +1 because the first label is the title
                label.config(bg="yellow")
            else:
                label.config(bg="white")

    def show_computer_cards(self, show=None):
        if show is not None:
            self.show_computer_cards_var.set(show)
        self.update_display()

    def on_window_resize(self, event):
        # Calculate new font size based on window width
        new_size = max(int(event.width / 100), 8)  # Minimum font size of 8
        scale_factor = new_size / self.default_font_size

        # Update font sizes
        for widget in self.master.winfo_children():
            self.update_widget_fonts(widget, scale_factor)

        # Update card sizes
        self.update_display()

    def update_widget_fonts(self, widget, scale_factor):
        try:
            current_font = font.nametofont(widget.cget("font"))
            new_size = max(int(current_font.cget("size") * scale_factor), 8)
            widget.configure(font=(current_font.cget("family"), new_size))
        except:
            pass  # Some widgets might not have a font property

        if widget.winfo_children():
            for child in widget.winfo_children():
                self.update_widget_fonts(child, scale_factor)

import traceback
import logging

if __name__ == "__main__":
    logging.basicConfig(filename='poker_error.log', level=logging.ERROR)
    try:
        root = tk.Tk()
        app = PokerUI(root)
        root.mainloop()
    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        logging.error(traceback.format_exc())
        print(f"An error occurred: {str(e)}")
        print("Please check the 'poker_error.log' file for more details.")
