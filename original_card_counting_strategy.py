import pandas as pd


card_hist_df = pd.DataFrame(columns = ['wins', 'losses', 'ties'], 
index = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"])
card_hist_df = card_hist_df.fillna(0)
card_hist_df["wins"]["Ace"] = 5
print(card_hist_df)
