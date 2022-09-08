from card import Card
import basic_strategy as bs
import matplotlib.pyplot as plt
from blackjack import Blackjack
import numpy as np
import pandas as pd

Blackjack.see_what_is_happening = False # Set true to see the actual games
runs = 100
bs.simulations = 1000
col = []
for i in range(runs): 
    col.append("Run " + str(i))
df = pd.DataFrame(columns = col)

def main():
    for x in range(Blackjack.num_of_decks): 
        Card.create_deck()
    Card.shuffle_deck()
    for x in range(runs):
        while Blackjack.keep_playing == True:
            Blackjack.blackjack_game()
        if len(Blackjack.y) != bs.simulations + 1:
            for i in range(len(Blackjack.y), bs.simulations + 1):
                Blackjack.y = np.append(Blackjack.y, 0) # If all chips are loss, fill blanks with zeros
        df["Run " + str(x)] = Blackjack.y.tolist()
        Blackjack.new_run()
    for num in Blackjack.card_hist_df.index:
        Blackjack.card_hist_df['win %'][num] = str(Blackjack.card_hist_df['wins'][num] / Blackjack.card_hist_df['total'][num] * 100)
        Blackjack.card_hist_df['loss %'][num] = str(Blackjack.card_hist_df['losses'][num] / Blackjack.card_hist_df['total'][num] * 100)
        Blackjack.card_hist_df['tie %'][num] = str(Blackjack.card_hist_df['ties'][num] / Blackjack.card_hist_df['total'][num] * 100)
    mean = df.mean(axis = 1); std = df.std(axis = 1); median = df.median(axis = 1)
    df["Average Chip Values"], df["Standard Deviation Chip Values"], df["Median Chip Values"] = mean, std, median
    Blackjack.card_hist_df.to_csv("data.csv")
    print("Total Wins:", Blackjack.total_wins)
    print("Total Losses:", Blackjack.total_losses)
    print("Total Ties:", Blackjack.total_ties)
    total = Blackjack.total_wins + Blackjack.total_losses + Blackjack.total_ties
    win_percentage = Blackjack.total_wins / total
    loss_percentage = Blackjack.total_losses / total
    tie_percentage = Blackjack.total_ties / total
    print("Win Percentage:", win_percentage)
    print("Loss Percentage:", loss_percentage)
    print("Tie Percentage:", tie_percentage)
    plt.title("Chip total through a number of games")
    plt.xlabel("Games")
    plt.ylabel("Chip total")
    plt.plot(Blackjack.x, mean, label = "Mean")
    #plt.plot(Blackjack.x, df["Standard Deviation Chip Values"], label = "S.D.")
    plt.plot(Blackjack.x, median, label = "Median")
    plt.legend(loc ='lower right')
    plt.show()

main()
