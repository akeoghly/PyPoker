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
        self.config(width=50, height=70, relief=tk.RAISED, borderwidth=2)
        
        self.value_label = tk.Label(self, text=card.value, font=("Arial", 14, "bold"))
        self.value_label.pack(pady=(5, 0))
        
        suit_symbol = self.SUITS.get(card.suit, card.suit)
        suit_color = "red" if card.suit in ["Hearts", "Diamonds"] else "black"
        self.suit_label = tk.Label(self, text=suit_symbol, font=("Arial", 24), fg=suit_color)
        self.suit_label.pack(expand=True)

def create_card_display(master, cards):
    frame = tk.Frame(master)
    for card in cards:
        card_ui = CardUI(frame, card)
        card_ui.pack(side=tk.LEFT, padx=2)
    return frame
