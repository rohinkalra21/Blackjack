# These decisions were implemented to replicate the basic strategy of blackjack. 

dealer_upcard = None
total = 0
soft_total = False
games_played = 0
simulations = 1000

def get_split_decision(number):
    # SPLITTING
    if number == "Ace":
        return "y"
    elif number in ["King", "Queen", "Jack", "10"]:
        return "n"
    elif number == "9":
        if dealer_upcard in [7, 10, 11]:
            return "n"
        else:
            return "y"
    elif number == "8":
        return "y"
    elif number == "7":
        if dealer_upcard >= 8:
            return "n"
        else:
            return "y"
    elif number == "6":
        if dealer_upcard >= 7:
            return "n"
        else:
            return "y"
    elif number == "5":
        return "n"
    elif number == "4":
        if dealer_upcard in [5, 6]:
            return "y"
        else:
            return "n"
    elif number in ["3", "2"]:
        if dealer_upcard <= 7:
            return "y"
        else:
            return "n"

def get_hit_stand_double_down_decision():
    if soft_total == False:
        # HARD TOTALS
        if total >= 17:
            return "s"
        elif total >= 13 and total <= 16:
            if dealer_upcard <= 6:
                return "s"
            elif dealer_upcard > 6:
                return "h"
        elif total == 12:
            if dealer_upcard in [4, 5, 6]:
                return "s"
            else:
                return "h"
        elif total == 11:
            return "dd"
        elif total == 10:
            if dealer_upcard in [10, 11]:
                return "h"
            else:
                return "dd"
        elif total == 9:
            if dealer_upcard in [3, 4, 5, 6]:
                return "dd"
            else:
                return "h"
        elif total <= 8:
            return "h"
    elif soft_total == True:
        # SOFT TOTALS
        if total >= 20:
            return "s"
        elif total == 19:
            if dealer_upcard == 6:
                return "dd"
            else:
                return "s"
        elif total == 18:
            if dealer_upcard <= 6:
                return "dd"
            elif dealer_upcard in [7, 8]:
                return "s"
            else:
                return "h"
        elif total == 17:
            if dealer_upcard in [3, 4, 5, 6]:
                return "dd"
            else:
                return "h"
        elif total in [16, 15]:
            if dealer_upcard in [4, 5, 6]:
                return "dd"
            else:
                return "h"
        elif total in [14, 13]:
            if dealer_upcard in [5, 6]:
                return "dd"
            else:
                return "h"
        elif total == 12:
            return "h"

def get_surrender_decision():
    # SURRENDER
    if dealer_upcard in [9, 10, 11] and total == 16:
        return "y"
    elif dealer_upcard == 10 and total == 15:
        return "y"
    else:
        return "n"

def get_insurance_decision():
    # INSURANCE
    return "n"

def get_continue_decision():
    # CONTINUE
    if games_played < simulations:
        return "y"
    else:
        return "n"
