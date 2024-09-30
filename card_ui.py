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
        self.config(relief=tk.RAISED, borderwidth=2, bg="white")
        
        self.value_label = tk.Label(self, text=card.value, font=("Arial", 14, "bold"), bg="white", fg="black")
        self.value_label.pack(expand=True, fill=tk.BOTH)
        
        suit_symbol = self.SUITS.get(card.suit, card.suit)
        suit_color = "red" if card.suit in ["Hearts", "Diamonds"] else "black"
        self.suit_label = tk.Label(self, text=suit_symbol, font=("Arial", 24), fg=suit_color, bg="white")
        self.suit_label.pack(expand=True, fill=tk.BOTH)

        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        # Update font sizes based on new dimensions
        value_font_size = max(int(event.width / 4), 8)
        suit_font_size = max(int(event.width / 2), 12)
        
        self.value_label.config(font=("Arial", value_font_size, "bold"))
        self.suit_label.config(font=("Arial", suit_font_size))

def create_card_display(master, cards):
    frame = tk.Frame(master)
    for i, card in enumerate(cards):
        frame.columnconfigure(i, weight=1)
        card_ui = CardUI(frame, card)
        card_ui.grid(row=0, column=i, padx=2, sticky="nsew")
    return frame
