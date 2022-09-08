from betting import Betting
import basic_strategy as bs
import numpy as np

class Card:   
    card_deck = []

    def __init__(self, suit: str, number: str, value = 0):
        self.suit = suit
        self.number = number
        self.value = value

        Card.card_deck.append(self)

    def __repr__(self):
        return f"{self.number} of {self.suit}" 

c3 = Card("Hearts", "8", 8)
c4 = Card("Clubs", "8", 8)
c2 = Card("Spades", "Ace", 11)
c1 = Card("Hearts", "Ace", 11)
c7 = Card("Diamonds", "Ace", 11)
c6 = Card("Spades", "8", 8)
c8 = Card("Clubs", "6", 6)
c9 = Card("Hearts", "4", 4)
c10 = Card("Hearts", "5", 5)
c5 = Card("Diamonds", "8", 8)
c11 = Card("Hearts", "10", 10)
c12 = Card("Diamonds", "Jack", 10)
c13 = Card("Clubs", "King", 10)
c14 = Card("Hearts", "Queen", 10)

class Blackjack:
    dealer_cards = []; dealer_total = 0
    user_hand = []; user_total = 0
    split_hand_1 = []; split_total_1 = 0
    split_hand_2 = []; split_total_2 = 0
    split_hand_3 = []; split_total_3 = 0
    split_hand_4 = []; split_total_4 = 0

    times_split = 0
    blackjack = False
    surrender = False
    split = False
    user_busts = False
    splits_bust = True
    games_played = 0
    see_what_is_happening = True
    x = np.arange(bs.simulations + 1)
    y = np.array([Betting.chips])
    total_wins = 0
    total_losses = 0
    total_ties = 0

    num_of_decks = 8 # Set Number of Decks
    total_cards = num_of_decks * 52
    # Shuffles when stack is a quarter of total deck
    # Can double down on any total
    # Dealer stands on soft 17
    # Late surrender is used
    # Double after split is allowed
    # Can hit an Ace more than once after split

    def beginning_prompt():
        user_input = input("Welcome to Blackjack!\r\nWould you like to know the rules?\r\n(Hit y for yes, and n for no)\n")
        if user_input == "y":
            Blackjack.rules()
        elif user_input == "n":
            print("Lets Begin!")
        else:
            return Blackjack.beginning_prompt()

    def rules():
        print("The goal of blackjack is to be as close to 21 without going over\n")
        print("Face cards are 10 and the Ace is either a 1 or 11.\n")
        print("Blackjack occurs when the two dealt cards equal 21\n")
        print("If you go over, you bust, and lose the hand.\n")
        print("Splitting up to 3 times is allowed.\n")
        print("Insurance and surrendering is allowed when dealer has an ace.\n")

    def give_dealer_cards():
        Blackjack.dealer_cards.append(Card.card_deck[0])
        Blackjack.dealer_cards.append(Card.card_deck[1])
        bs.dealer_upcard = Blackjack.dealer_cards[0].value
        if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
            print(f"Dealer has {Blackjack.dealer_cards[0]} and Another Card")

    def give_user_cards():
        Blackjack.user_hand.append(Card.card_deck[2])
        Blackjack.user_hand.append(Card.card_deck[3])
        if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
            print(f"Your Hand: {Blackjack.user_hand}")

    def remove_dealt_cards():
        del Card.card_deck[0:4]

    def assign_black_jack_values():
        for x in range(len(Card.card_deck)):
            if Card.card_deck[x].number == "Ace":
                Card.card_deck[x].value = 11
            elif Card.card_deck[x].number == "King" or Card.card_deck[x].number == "Queen" or Card.card_deck[x].number == "Jack":
                Card.card_deck[x].value = 10
            else:
                Card.card_deck[x].value = int(Card.card_deck[x].number)

    def calculate_total(hand): 
        total = 0
        for x in range(len(hand)):
            total += hand[x].value
        Blackjack.change_total_value(hand, total)
        if __name__ != '__main__':
            if hand != Blackjack.dealer_cards:
                bs.soft_total = False
                for card in hand:
                    if card.value == 11:
                        bs.soft_total = True
                        break
                bs.total = total
        return total

    def change_total_value(hand, total):
        if hand == Blackjack.user_hand:
            Blackjack.user_total = total
        elif hand == Blackjack.dealer_cards:
            Blackjack.dealer_total = total
        elif hand == Blackjack.split_hand_1:
            Blackjack.split_total_1 = total
        elif hand == Blackjack.split_hand_2:
            Blackjack.split_total_2 = total
        elif hand == Blackjack.split_hand_3:
            Blackjack.split_total_3 = total
        elif hand == Blackjack.split_hand_4:
            Blackjack.split_total_4 = total
        
    def hit_or_stand(hand, total):
        dec = False
        if len(hand) == 2 and hand != Blackjack.dealer_cards and Blackjack.split == True:
            dec = Blackjack.split_prompt(hand, total)
        if dec == False:
            if __name__ == '__main__':
                user_input = input("Would you like to hit, stand, or dd?\r\n(h, s, or dd)\n")
            else: 
                user_input = bs.get_hit_stand_double_down_decision()
            if user_input == "h":
                Blackjack.hit(hand, total)
            elif user_input == "s":
                Blackjack.stand(hand, total)
            elif user_input == "dd":
                if Betting.can_double_down_or_split():
                    Blackjack.double_down(hand)
                    Blackjack.hit(hand, total, True)
                else:
                    Blackjack.hit_or_stand(hand, total)
            else: 
                return Blackjack.hit_or_stand(hand, total)

    def hit(hand, total, double_down = False):
            hand.append(Card.card_deck[0]) 
            Card.card_deck.pop(0)
            total = Blackjack.calculate_total(hand)
            if hand[0].value in ["Ace of Clubs", "Ace of Spades", "Ace of Diamonds", "Ace of Hearts"]\
                and hand[1].value in ["Ace of Clubs", "Ace of Spades", "Ace of Diamonds", "Ace of Hearts"]\
                and len(hand) == 2:
                print("YO")
                return 
            Blackjack.check_if_bust(hand, total, double_down)

    def stand(hand, total):
        Blackjack.calculate_total(hand)
        if hand == Blackjack.user_hand:
            if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                print(f"Dealer's hand: {Blackjack.dealer_cards}")
        elif hand in [Blackjack.split_hand_1, Blackjack.split_hand_2, 
            Blackjack.split_hand_3, Blackjack.split_hand_4]:
            Blackjack.splits_bust = False
        elif hand == Blackjack.dealer_cards:
            Blackjack.check_for_winner()

    def double_down(hand):
        Betting.chips -= Betting.bet    
        if hand == Blackjack.user_hand:
            Betting.bet *= 2
        elif hand == Blackjack.split_hand_1:
            Betting.split_bet_1
        elif hand == Blackjack.split_hand_2:
            Betting.split_bet_2
        elif hand == Blackjack.split_hand_3:
            Betting.split_bet_3
        elif hand == Blackjack.split_hand_3:
            Betting.split_bet_3

    def check_if_bust(hand, total, double_down = False):
        Blackjack.change_ace_value(hand, total)
        total = Blackjack.calculate_total(hand)
        if hand != Blackjack.dealer_cards:
            if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                print(f"Your Hand: {hand}") 
            if total > 21: 
                Blackjack.total_losses += 1
                if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                    print("Bust")
                if hand == Blackjack.user_hand:
                    Blackjack.user_busts = True     
            else: 
                if not double_down:
                    Blackjack.hit_or_stand(hand, total)
        elif hand == Blackjack.dealer_cards:
            if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                print(f"Dealer's Hand: {Blackjack.dealer_cards}")
            if Blackjack.dealer_total > 21:
                Blackjack.total_wins += 1
                if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                    print("Dealer Busts")
                if Blackjack.split == True:
                    Blackjack.check_for_winner()
                else:
                    Betting.win()
            else:
                Blackjack.dealer_decisions()

    def change_ace_value(hand, total):
        has_ace = False       
        for x in range(len(hand)):
            if hand[x].number == "Ace":
                has_ace = True
                break
        if total > 21 and has_ace == True:
            for x in range(len(hand)):
                if hand[x].number == "Ace" and hand[x].value == 11:
                    hand[x].value = 1
                    total = Blackjack.calculate_total(hand)
                    Blackjack.change_ace_value(hand, total)
                    break

    def check_for_blackjack():
        Blackjack.calculate_total(Blackjack.user_hand)
        Blackjack.calculate_total(Blackjack.dealer_cards)
        if Blackjack.user_total == 21 and Blackjack.dealer_total == 21:
            Blackjack.blackjack = True
            Betting.push()
            Blackjack.total_ties += 1
            if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                print(f"Dealer Hand: {Blackjack.dealer_cards}")
                print("Push")
        else:
            if Blackjack.user_total == 21:
                Blackjack.blackjack = True
                Betting.blackjack_payout()
                Blackjack.total_wins += 1
                if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                    print("You have blackjack!")
            elif Blackjack.dealer_cards[0].number == "Ace" and Betting.can_afford():
                Blackjack.insurance_prompt()
            if Blackjack.dealer_total == 21:
                Betting.insurance_payout()
                Blackjack.blackjack = True
                Blackjack.total_losses += 1
                if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                    print(f"Dealer had {Blackjack.dealer_cards}")
                    print("Dealer had blackjack")
            
    def dealer_decisions():
        if Blackjack.dealer_total < 17:
            if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                print("Dealer Hits")
            Blackjack.hit(Blackjack.dealer_cards, Blackjack.dealer_total)
        else:
            Blackjack.stand(Blackjack.dealer_cards, Blackjack.dealer_total)

    def betting_amount_prompt():
        Betting.set_maximum_bet()
        if __name__ == '__main__':
            print("How much would you like to bet?") 
            user_input = input(f"(Enter integer from {Betting.minimum_bet} to {Betting.maximum_bet}) \r\nChips: {Betting.chips} \n")
        else:
            user_input = bs.get_betting_size()
        if Betting.can_bet(user_input, Betting.minimum_bet, Betting.maximum_bet):
            user_input = int(user_input)
            Betting.bet = user_input
            Betting.chips -= Betting.bet
        else:
            return Blackjack.betting_amount_prompt()

    def split_prompt(hand, total):
        if hand[0].number == hand[1].number and Blackjack.times_split < 3 and Betting.can_double_down_or_split():
            if __name__ == '__main__':
                user_input = input(f"Would you like to split the hand for {Betting.bet}? \r\nChips: {Betting.chips}\n(y or n)\n")
            else:
                user_input = bs.get_split_decision(hand[0].number)
            if user_input == "y":
                Blackjack.split = True
                Blackjack.times_split += 1
                Betting.chips -= Betting.bet
                Blackjack.split_hand(hand, total)
                return True
            elif user_input == "n":
                return False
            else:
                Blackjack.split_prompt(hand, total)
        return False

    def insurance_prompt():
        if __name__ == '__main__':
            user_input = input("Dealer has an Ace, would you like to take insurance?\r\n(y or n)\n")
        else:
            user_input = bs.get_insurance_decision()
        if user_input == "y":
            Betting.set_maximum_insurance()
            Betting.set_insurance()
        elif user_input == "n":
            return 
        else:
            return Blackjack.insurance_prompt()

    def surrender_prompt():
        if __name__ == '__main__':
            user_input = input("Would you like to surrender?\n(y or n)\n")
        else:
            user_input = bs.get_surrender_decision()
        if user_input == "y":
            Blackjack.total_losses += 1
            Betting.surrender()
            Blackjack.surrender = True
        elif user_input == "n":
            return
        else:
            return Blackjack.surrender_prompt()

    def split_hand(hand, total):
        if hand == Blackjack.user_hand:
            Blackjack.split_hand_1.append(hand[0])
            Blackjack.split_hand_2.append(hand[1])   
            del Blackjack.user_hand[:]
            Blackjack.user_total = 0
            Blackjack.hit(Blackjack.split_hand_1, Blackjack.split_total_1)
            Blackjack.hit(Blackjack.split_hand_2, Blackjack.split_total_2)
        if hand != Blackjack.user_hand:
            if len(Blackjack.split_hand_3) == 0:
                Blackjack.split_hand_3.append(hand[1])
                del hand[1]
                Blackjack.hit(hand, total)
                Blackjack.hit(Blackjack.split_hand_3, Blackjack.split_total_3)
            elif len(Blackjack.split_hand_4) == 0:
                Blackjack.split_hand_4.append(hand[1])
                del hand[1]
                Blackjack.hit(hand, total)
                Blackjack.hit(Blackjack.split_hand_4, Blackjack.split_total_4)

    def check_for_winner():
        if Blackjack.split == True:
            wins = 0
            ties = 0
            losses = 0
            for x in [Blackjack.split_total_1, Blackjack.split_total_2,
                Blackjack.split_total_3, Blackjack.split_total_4]:
                if x > Blackjack.dealer_total and x <= 21:
                    wins += 1
                    Blackjack.total_wins += 1
                    Betting.win()
                elif x == Blackjack.dealer_total:
                    ties += 1
                    Blackjack.total_ties += 1
                    Betting.push()
                elif x > 21 or (x < Blackjack.dealer_total and x != 0):
                    losses += 1
                    Blackjack.total_losses += 1
            if __name__ == '__main__' or Blackjack.see_what_is_happening == True:        
                print(f"{wins} splits won, {ties} splits tied, {losses} splits lost")
        elif Blackjack.dealer_total == Blackjack.user_total:
            Betting.push()
            Blackjack.total_ties += 1
            if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                print("Push")
        elif Blackjack.dealer_total > Blackjack.user_total:
            Blackjack.total_losses += 1
            if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                print("Dealer Wins")
        else: 
            Betting.win()
            Blackjack.total_wins += 1
            if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                print(f"Dealer had {Blackjack.dealer_cards}")
                print("Player Wins")
    
    def restart():
        Blackjack.games_played += 1; bs.games_played += 1
        Blackjack.dealer_cards.clear(); Blackjack.dealer_total = 0
        Blackjack.user_hand.clear(); Blackjack.user_total = 0
        Blackjack.split_hand_1.clear(); Blackjack.split_total_1 = 0
        Blackjack.split_hand_2.clear(); Blackjack.split_total_2 = 0
        Blackjack.split_hand_3.clear(); Blackjack.split_total_3 = 0
        Blackjack.split_hand_4.clear(); Blackjack.split_total_4 = 0
        Blackjack.times_split = 0
        Blackjack.blackjack = False
        Blackjack.split = False
        Blackjack.user_busts = False
        Blackjack.splits_bust = True
        Blackjack.surrender = False
        Betting.clear_bets()
        if __name__ == '__main__':
            user_input = input("Would you like to keep playing?\r\n(y or n) \n")
        else:
            user_input = bs.get_continue_decision()
        if user_input == "y":
            return Blackjack.blackjack_game()
        elif user_input == "n":
            print(f"After {Blackjack.games_played} games, You cashed out with {Betting.chips} chips")
        else:
            return Blackjack.restart()

    def new_run():
        Betting.chips = Betting.starting_chips
        Blackjack.x = np.arange(bs.simulations + 1)
        Blackjack.y = np.array([Betting.chips])
        Blackjack.games_played = 0
        bs.games_played = 0

    def blackjack_game():
        if Betting.can_play() == False:
            print("Not enough to continue")
            return
        Blackjack.assign_black_jack_values()
        Blackjack.betting_amount_prompt()
        Blackjack.give_dealer_cards()
        Blackjack.give_user_cards()
        Blackjack.remove_dealt_cards()
        Blackjack.check_for_blackjack()
        if Blackjack.blackjack == False:
            Blackjack.surrender_prompt()
            if Blackjack.surrender == False:
                Blackjack.split_prompt(Blackjack.user_hand, Blackjack.user_total)
                if Blackjack.splits_bust == False:
                    if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                        print(f"Dealer's hand: {Blackjack.dealer_cards}")
                    Blackjack.dealer_decisions()
                if Blackjack.split == False:
                    Blackjack.hit_or_stand(Blackjack.user_hand, Blackjack.user_total)
                    if Blackjack.user_busts == False:
                        Blackjack.dealer_decisions()
        if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
            print(Betting.chips)
        Blackjack.y = np.append(Blackjack.y, Betting.chips)
        # if len(Card.card_deck) < (0.25 * Blackjack.total_cards):
        #     Card.card_deck.clear()
        #     for x in range(Blackjack.num_of_decks):
        #         Card.create_deck()
        #     Card.shuffle_deck()     
        return Blackjack.restart()

if __name__ == '__main__' :
    Blackjack.beginning_prompt()
    # for x in range(Blackjack.num_of_decks): 
    #     Card.create_deck()
    # Card.shuffle_deck()
    Blackjack.blackjack_game()
