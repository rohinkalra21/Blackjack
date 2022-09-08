from card import Card
import betting
import basic_strategy as bs
import betting_strategy
import numpy as np
import pandas as pd

class Blackjack:
    dealer_cards = []
    dealer_total = 0
    user_hand = []
    user_total = 0
    split_hand_1 = []
    split_total_1 = 0
    split_hand_2 = []
    split_total_2 = 0
    split_hand_3 = []
    split_total_3 = 0
    split_hand_4 = []
    split_total_4 = 0

    dealer_undercard = Card
    times_split = 0
    blackjack = False
    surrender = False
    split = False
    user_busts = False
    splits_bust = True
    games_played = 0
    keep_playing = True
    see_what_is_happening = True
    x = np.arange(bs.simulations + 1)
    y = np.array([betting.chips])
    total_wins = 0
    total_losses = 0
    total_ties = 0

    num_of_decks = 8  # Set Number of Decks
    total_cards = num_of_decks * 52
    betting_strategy.num_of_decks = num_of_decks

    card_hist_df = pd.DataFrame(columns = ['wins', 'losses', 'ties', 'win %', 'loss %', 'tie %', 'total'], 
    index = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"])
    card_hist_df = card_hist_df.fillna(0)

    # Shuffles when stack is a quarter of total deck
    # Can double down on any total
    # Dealer stands on soft 17
    # Late surrender is used
    # Double after split is allowed
    # Can hit an Ace more than once after split

    def beginning_prompt():
        user_input = input(
            "Welcome to Blackjack!\r\nWould you like to know the rules?\r\n(Hit y for yes, and n for no)\n")
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
        Card.pop()
        Blackjack.dealer_cards.append(Card.card_deck[0])
        Card.card_deck.pop(0)  # Change undercard count later
        Blackjack.dealer_undercard = Blackjack.dealer_cards[1]
        bs.dealer_upcard = Blackjack.dealer_cards[0].value
        if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
            print(f"Dealer has {Blackjack.dealer_cards[0]} and Another Card")

    def give_user_cards():
        Blackjack.user_hand.append(Card.card_deck[0])
        Card.pop()
        Blackjack.user_hand.append(Card.card_deck[0])
        Card.pop()
        if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
            print(f"Your Hand: {Blackjack.user_hand}")

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
                if betting.can_double_down_or_split():
                    Blackjack.double_down(hand)
                    Blackjack.hit(hand, total, True)
                else:
                    if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                        print("Cannot Double Down; Hit Instead")
                    Blackjack.hit(hand, total)
            else:
                return Blackjack.hit_or_stand(hand, total)

    def hit(hand, total, double_down=False):
        hand.append(Card.card_deck[0])
        Card.pop()
        total = Blackjack.calculate_total(hand)
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
        if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
            print("You Doubled Down")
        betting.chips -= betting.bet
        if hand == Blackjack.user_hand:
            betting.bet *= 2
        elif hand == Blackjack.split_hand_1:
            betting.split_bet_1 *= 2
        elif hand == Blackjack.split_hand_2:
            betting.split_bet_2 *= 2
        elif hand == Blackjack.split_hand_3:
            betting.split_bet_3 *= 2
        elif hand == Blackjack.split_hand_4:
            betting.split_bet_4 *= 2

    def check_if_bust(hand, total, double_down=False):
        Blackjack.change_ace_value(hand, total)
        total = Blackjack.calculate_total(hand)
        if hand != Blackjack.dealer_cards:
            if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                print(f"Your Hand: {hand}")
            if total > 21:
                if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                    print("Bust")
                if hand == Blackjack.user_hand:
                    Blackjack.lose(Blackjack.user_hand)
                    Blackjack.user_busts = True
            else:
                if not double_down:
                    Blackjack.hit_or_stand(hand, total)
                elif double_down and hand == Blackjack.user_hand:
                    if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                        print(f"Dealer's hand: {Blackjack.dealer_cards}")
                else:
                    Blackjack.splits_bust = False
        elif hand == Blackjack.dealer_cards:
            if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                print(f"Dealer's Hand: {Blackjack.dealer_cards}")
            if Blackjack.dealer_total > 21:
                if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                    print("Dealer Busts")
                Blackjack.check_for_winner()
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
            betting.push(betting.bet)
            Blackjack.push(Blackjack.user_hand)
            if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                print(f"Dealer Hand: {Blackjack.dealer_cards}")
                print("Push")
        else:
            if Blackjack.user_total == 21:
                Blackjack.blackjack = True
                betting.blackjack_payout()
                Blackjack.win(Blackjack.user_hand)
                if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                    print("You have blackjack!")
            elif Blackjack.dealer_cards[0].number == "Ace" and betting.can_afford():
                Blackjack.insurance_prompt()
            if Blackjack.dealer_total == 21:
                betting.insurance_payout()
                Blackjack.blackjack = True
                Blackjack.lose(Blackjack.user_hand)
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
        min, max = betting.set_maximum_bet()
        if __name__ == '__main__':
            print("How much would you like to bet?")
            user_input = input(f"(Enter integer from {min} to {max}) \r\nChips: {betting.chips} \n")
        else:
            user_input = betting_strategy.get_betting_size()
        if betting.can_bet(user_input, min, max):
            user_input = int(user_input)
            betting.bet = user_input
            betting.chips -= betting.bet
            if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                print(f"You bet {user_input} chips")
        else:
            return Blackjack.betting_amount_prompt()

    def split_prompt(hand, total):
        if hand[0].number == hand[1].number and Blackjack.times_split < 3 and betting.can_double_down_or_split():
            if __name__ == '__main__':
                user_input = input(f"Would you like to split the hand for {betting.bet}? \r\nChips: {betting.chips}\n(y or n)\n")
            else:
                user_input = bs.get_split_decision(hand[0].number)
            if user_input == "y":
                Blackjack.split = True
                Blackjack.times_split += 1
                betting.chips -= betting.bet
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
            betting.set_maximum_insurance()
            betting.set_insurance()
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
            Blackjack.lose(Blackjack.user_hand)  # Comment in or out to determine if surrendering counts as losses
            betting.surrender()
            Blackjack.surrender = True
            if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                print("You surrendered")
        elif user_input == "n":
            return
        else:
            return Blackjack.surrender_prompt()

    def split_hand(hand, total):
        if hand == Blackjack.user_hand:
            Blackjack.split_hand_1.append(hand[0])
            Blackjack.split_hand_2.append(hand[1])
            betting.split_bet_1 = betting.bet
            betting.split_bet_2 = betting.bet
            del Blackjack.user_hand[:]
            Blackjack.user_total = 0
            Blackjack.hit(Blackjack.split_hand_1, Blackjack.split_total_1)
            Blackjack.hit(Blackjack.split_hand_2, Blackjack.split_total_2)
        if hand != Blackjack.user_hand:
            if len(Blackjack.split_hand_3) == 0:
                Blackjack.split_hand_3.append(hand[1])
                betting.split_bet_3 = betting.bet
                del hand[1]
                Blackjack.hit(hand, total)
                Blackjack.hit(Blackjack.split_hand_3, Blackjack.split_total_3)
            elif len(Blackjack.split_hand_4) == 0:
                Blackjack.split_hand_4.append(hand[1])
                betting.split_bet_4 = betting.bet
                del hand[1]
                Blackjack.hit(hand, total)
                Blackjack.hit(Blackjack.split_hand_4, Blackjack.split_total_4)

    def check_for_winner():
        dealer_busts = False
        if Blackjack.dealer_total > 21:
            dealer_busts = True
        if Blackjack.split == True:
            wins = 0
            ties = 0
            losses = 0
            bet = 0
            lst = [[Blackjack.split_hand_1, Blackjack.split_total_1, betting.split_bet_1],
                    [Blackjack.split_hand_2, Blackjack.split_total_2, betting.split_bet_2], 
                    [Blackjack.split_hand_3, Blackjack.split_total_3, betting.split_bet_3], 
                    [Blackjack.split_hand_4, Blackjack.split_total_4, betting.split_bet_4]]
            for hand, total, bet in lst:
                if total != 0:
                    if total <= 21 and (total > Blackjack.dealer_total or dealer_busts):
                        wins += 1
                        Blackjack.win(hand)
                        betting.win(bet)
                    elif total == Blackjack.dealer_total and total <= 21:
                        ties += 1  
                        Blackjack.push(hand)
                        betting.push(bet)
                    elif total > 21 or (total < Blackjack.dealer_total and Blackjack.dealer_total <= 21):
                        losses += 1
                        Blackjack.lose(hand)
            if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                print(f"{wins} splits won, {ties} splits tied, {losses} splits lost")
        elif Blackjack.dealer_total == Blackjack.user_total and dealer_busts == False:
            betting.push(betting.bet)
            Blackjack.push(Blackjack.user_hand)
            if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                print("Push")
        elif Blackjack.dealer_total > Blackjack.user_total and dealer_busts == False:
            Blackjack.lose(Blackjack.user_hand)
            if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                print("Dealer Wins")
        else:
            betting.win(betting.bet)
            Blackjack.win(Blackjack.user_hand)
            if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                print(f"Dealer had {Blackjack.dealer_cards}")
                print("Player Wins")

    def win(hand):
        for Card in hand:
            Blackjack.card_hist_df['wins'][Card.number] += 1
            Blackjack.card_hist_df['total'][Card.number] += 1
        Blackjack.total_wins += 1
        betting_strategy.win_streak += 1
        betting_strategy.loss_streak = 0
        betting_strategy.oscards_grind_win = True

    def lose(hand):
        for Card in hand:
            Blackjack.card_hist_df['losses'][Card.number] += 1
            Blackjack.card_hist_df['total'][Card.number] += 1
        Blackjack.total_losses += 1
        betting_strategy.loss_streak += 1
        betting_strategy.win_streak = 0

    def push(hand):
        for Card in hand:
            Blackjack.card_hist_df['ties'][Card.number] += 1
            Blackjack.card_hist_df['total'][Card.number] += 1
        Blackjack.total_ties += 1

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
        betting.clear_bets()
        Card.update_card_counts(Blackjack.dealer_undercard.number)
        if __name__ == '__main__':
            user_input = input("Would you like to keep playing?\r\n(y or n) \n")
        else:
            user_input = bs.get_continue_decision()
        if user_input == "y":
            return
        elif user_input == "n":
            Blackjack.keep_playing = False
            print(f"After {Blackjack.games_played} games, You cashed out with {betting.chips} chips")
        else:
            return Blackjack.restart()

    def new_run():
        betting.chips = betting.starting_chips
        Blackjack.x = np.arange(bs.simulations + 1)
        Blackjack.y = np.array([betting.chips])
        Blackjack.games_played = 0
        betting_strategy.lst = [betting.chips, betting_strategy.init_goal, 0]
        bs.games_played = 0
        Blackjack.keep_playing = True

    def blackjack_game():
        if betting.can_play() == False:
            if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                print("Cannot afford to continue\nGame over!")
            Blackjack.keep_playing = False
            print(f"After {Blackjack.games_played} games, You cashed out with {betting.chips} chips")
            return
        Blackjack.assign_black_jack_values()
        Blackjack.betting_amount_prompt()
        Blackjack.give_dealer_cards()
        Blackjack.give_user_cards()
        Blackjack.check_for_blackjack()
        if Blackjack.blackjack == False:
            Blackjack.surrender_prompt()
            if Blackjack.surrender == False:
                Blackjack.split_prompt(
                    Blackjack.user_hand, Blackjack.user_total)
                if Blackjack.splits_bust == False:
                    if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
                        print(f"Dealer's hand: {Blackjack.dealer_cards}")
                    Blackjack.dealer_decisions()
                if Blackjack.split == False:
                    Blackjack.hit_or_stand(
                        Blackjack.user_hand, Blackjack.user_total)
                    if Blackjack.user_busts == False:
                        Blackjack.dealer_decisions()
        if __name__ == '__main__' or Blackjack.see_what_is_happening == True:
            print("Chips:", betting.chips)
        Blackjack.y = np.append(Blackjack.y, betting.chips)
        if len(Card.card_deck) < (0.25 * Blackjack.total_cards):
            Card.card_deck.clear()
            for x in range(Blackjack.num_of_decks):
                Card.create_deck()
            Card.shuffle_deck()
        return Blackjack.restart()

if __name__ == '__main__':
    Blackjack.beginning_prompt()
    for x in range(Blackjack.num_of_decks):
        Card.create_deck()
    Card.shuffle_deck()
    while Blackjack.keep_playing == True:
        Blackjack.blackjack_game()
