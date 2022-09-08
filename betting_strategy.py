import betting
from card import Card

init_bet = 100
betting_unit = 25
win_streak = 0
loss_streak = 0
streak_percent_change = 0.10
init_goal = betting.chips + init_bet
oscards_grind_series_value = 5
oscards_grind_win = False
lst = [betting.chips, init_goal, 0]
num_of_decks = 0

# Set betting strategy to True
fixed_betting = True
streak_betting = False
martingale_system_betting = False
oscars_grind_betting = False
hi_lo_card_count_betting = False
omega_II_card_count_betting = False
wong_halves_card_count_betting = False
victor_advanced_point_card_count_betting = False
original_card_count_strategy = False

def get_betting_size():
    global lst
    if fixed_betting == True:
        return fixed_bet(betting.chips)
    elif streak_betting == True:
        return streak_bet(betting.chips)
    elif martingale_system_betting == True:
        betting.maximum_bet = betting.chips
        lst[0] = betting.chips
        lst[0], lst[1], lst[2] = martingale_system_bet(lst[0], lst[1], lst[2])
        return lst[2]
    elif oscars_grind_betting == True:
        betting.maximum_bet = betting.chips
        lst[0] = betting.chips
        lst[0], lst[1], lst[2] = oscars_grind_bet(lst[0], lst[1], lst[2])
        return lst[2]
    elif hi_lo_card_count_betting == True:
        return card_count_bet(betting.chips, Card.hi_lo_count)
    elif omega_II_card_count_betting == True:
        return card_count_bet(betting.chips, Card.omega_II_count)
    elif wong_halves_card_count_betting == True:
        return card_count_bet(betting.chips, Card.wong_halves_count)
    elif victor_advanced_point_card_count_betting == True:
        return card_count_bet(betting.chips, Card.victor_advanced_point_count)
    elif original_card_count_strategy == True:
        return card_count_bet(betting.chips, Card.original_card_count)

def fixed_bet(chips):
    bet = init_bet
    if bet > chips:
        bet = chips
    return bet

def streak_bet(chips):
    if win_streak > 0:
        bet = init_bet + ((streak_percent_change * init_bet) * win_streak)
    elif loss_streak > 0:
        bet = init_bet - ((streak_percent_change * init_bet) * loss_streak)
    else:
        bet = init_bet
    if bet > chips:
        bet = chips
    if bet < betting.minimum_bet:
        return betting.minimum_bet
    elif bet > betting.maximum_bet:
        return betting.maximum_bet
    else:
        return bet

def martingale_system_bet(chips, goal, bet):
    bet = goal - chips
    if bet > 0:
        if bet >= chips:
            return chips, goal, chips
        else:
            return chips, goal, bet
    elif bet <= 0:
        goal += -bet + init_bet
        return martingale_system_bet(chips, goal, bet)

def oscars_grind_bet(chips, goal, bet):
    if chips >= goal:
        bet = oscards_grind_series_value
        goal = chips + oscards_grind_series_value
    elif oscards_grind_win:
        bet += oscards_grind_series_value
    oscards_grind_win = False
    return chips, goal, bet

def card_count_bet(chips, card_count):
    true_count = card_count / num_of_decks
    bet = init_bet + (betting_unit * true_count)
    if bet > chips:
        bet = chips
    if bet > betting.maximum_bet:
        bet = betting.maximum_bet
    elif bet < betting.minimum_bet:
        bet = betting.minimum_bet
    return bet