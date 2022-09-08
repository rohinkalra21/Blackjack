import random

class Card:
    card_deck = []
    card_count_df = []
    hi_lo_count = 0
    omega_II_count = 0
    wong_halves_count = 0
    victor_advanced_point_count = 0
    original_card_count = 0

    def __init__(self, suit: str, number: str, value = 0):
        self.suit = suit
        self.number = number
        self.value = value
        
        Card.card_deck.append(self)

    def __repr__(self):
        return f"{self.number} of {self.suit}" 

    def create_deck():    
        suit = str
        number = 0
        for x in range(52):
            number = x % 13 + 1
            if number == 1:
                number = "Ace"
            elif number == 11:
                number = "Jack"
            elif number == 12:
                number = "Queen"
            elif number == 13:
                number = "King"
            else:
                number = str(number)
            if x < 13:
                suit = "Hearts"
            elif x < 26:
                suit = "Diamonds"      
            elif x < 39:
                suit = "Spades"
            elif x < 52:
                suit = "Clubs"
            Card(suit, number)

    def shuffle_deck():
        random.shuffle(Card.card_deck)
        Card.hi_lo_count = 0
        Card.omega_II_count = 0
        Card.wong_halves_count = 0
        Card.victor_advanced_point_count = 0
        Card.original_card_count = 0

    def pop():
        removed_card = Card.card_deck.pop(0)
        Card.update_card_counts(removed_card.number)

    def update_card_counts(num):
        Card.update_hi_lo_count(num)
        Card.update_omega_II_count(num)
        Card.update_wong_halves_count(num)
        Card.update_victor_advanced_point_count(num)
        Card.update_original_card_count(num)

    def update_hi_lo_count(num):
        # 7's, 8's, 9's are worth 0
        if num in ["2", "3", "4", "5", "6"]:
            Card.hi_lo_count += 1
        elif num in ["10", "Jack", "Queen", "King", "Ace"]:
            Card.hi_lo_count -= 1
    
    def update_omega_II_count(num):
        # Aces and 8's are worth 0
        if num in ["2", "3", "7"]:
            Card.omega_II_count += 1
        elif num in ["4", "5", "6"]:
            Card.omega_II_count += 2
        elif num == "9":
            Card.omega_II_count -= 1
        elif num in ["10", "Jack", "Queen", "King"]:
            Card.omega_II_count -= 2
    
    def update_wong_halves_count(num):
        # 8's are worth 0
        if num in ["3", "4", "6"]:
            Card.wong_halves_count += 1
        elif num in ["2", "7"]:
            Card.wong_halves_count += 0.5
        elif num in ["5"]:
            Card.wong_halves_count += 1.5
        elif num == 9:
            Card.wong_halves_count -= 0.5
        elif num == ["10", "Jack", "Queen", "King", "Ace"]:
            Card.wong_halves_count -= 1
    
    def update_victor_advanced_point_count(num):
        # Aces and 8's are worth 0
        if num in ["2", "3", "4", "6", "7"]:
            Card.victor_advanced_point_count += 2
        elif num == 5:
            Card.victor_advanced_point_count += 3
        elif num == 9:
            Card.victor_advanced_point_count -= 1
        elif num in ["10", "Jack", "Queen", "King"]:
            Card.victor_advanced_point_count -= 3
    
    def update_original_card_count(num):
        pass
        
