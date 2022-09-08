
starting_chips = 10000 # Set Starting Chips
minimum_bet = 5 # Set Minimum Bet
maximum_bet = 500 # Set Maximum Bet
bj_payout = 3 / 2 # Set Blackjack Payout 
insur_payout = 2 / 1 # Set Insurance Payout

chips = starting_chips 
bet = 0
insur_bet = 0
insur_max = 0
split_bet_1 = 0
split_bet_2 = 0
split_bet_3 = 0
split_bet_4 = 0

def can_bet(amount, min, max):
    try:
        amount = int(amount)
    except ValueError:
        print("Please enter an integer")
        return False
    if amount < min or amount > max:
        print(f"Please enter a bet between {min} and {max}")
        return False
    elif amount >= min and amount <= max:
        return True

def set_maximum_bet():
    min = minimum_bet
    if chips < maximum_bet:
        max = chips
    else:
        max = maximum_bet
    return min, max

def set_maximum_insurance():
    global insur_max
    if chips < 0.5 * bet:
        insur_max = chips
    else:
        insur_max = int(0.5 * bet) 

def set_insurance():
    global chips
    print("How much would you like to insure?")
    user_input = input(f"Enter a number between {minimum_bet} and {insur_max}\nChips: {chips}\n")
    if can_bet(user_input, minimum_bet, insur_max):
        insur_bet = int(user_input)
        chips -= insur_bet
    else:
        set_insurance()

def surrender():
    global chips
    chips += int(0.5 * bet)

def insurance_payout():
    global chips
    chips += int(insur_payout * insur_bet)

def blackjack_payout():
    global chips
    chips += bet 
    chips += int(bj_payout * bet)

def can_afford():
    if chips < minimum_bet:
        return False
    return True

def can_double_down_or_split():
    if chips < bet:
        return False
    else:
        return True

def can_play():
    if chips < minimum_bet:
        return False
    return True

def win(bet):
    global chips
    if bet == bet:
        chips += int(2 * bet)
    elif bet == split_bet_1:
        chips += int(2 * split_bet_1)
    elif bet == split_bet_2:
        chips += int(2 * split_bet_2)
    elif bet == split_bet_3:
        chips += int(2 * split_bet_3)
    elif bet == split_bet_4:
        chips += int(2 * split_bet_4)

def push(bet):
    global chips
    if bet == bet:
        chips += int(bet)
    elif bet == split_bet_1:
        chips += int(split_bet_1)
    elif bet == split_bet_2:
        chips += int(split_bet_2)
    elif bet == split_bet_3:
        chips += int(split_bet_3)
    elif bet == split_bet_4:
        chips += int(split_bet_4)
    
def clear_bets():
    global bet, insur_bet, split_bet_1, split_bet_2, split_bet_3, split_bet_4
    bet = 0
    insur_bet = 0
    split_bet_1 = 0
    split_bet_2 = 0
    split_bet_3 = 0
    split_bet_4 = 0