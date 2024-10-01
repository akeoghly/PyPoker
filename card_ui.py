import tkinter as tk

class CardUI(tk.Frame):
    SUITS = {
        'Hearts': '♥',
        'Diamonds': '♦',
        'Clubs': '♣',
        'Spades': '♠'
    }
    
    def __init__(self, master, card, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.config(relief=tk.RAISED, borderwidth=2, bg="white", width=50, height=70)
        
        self.value_label = tk.Label(self, text=card.value, font=("Arial", 14, "bold"), bg="white", fg="black")
        self.value_label.pack(expand=True, fill=tk.BOTH)
        
        suit_symbol = self.SUITS.get(card.suit, card.suit)
        suit_color = "red" if card.suit in ["Hearts", "Diamonds"] else "black"
        self.suit_label = tk.Label(self, text=suit_symbol, font=("Arial", 24), fg=suit_color, bg="white")
        self.suit_label.pack(expand=True, fill=tk.BOTH)

def create_card_display(master, cards):
    frame = tk.Frame(master)
    for card in cards:
        card_ui = CardUI(frame, card)
        card_ui.pack(side=tk.LEFT, padx=2)
    return frame
