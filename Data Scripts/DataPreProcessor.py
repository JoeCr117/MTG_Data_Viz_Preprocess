# %%
import pandas as pd
from datetime import datetime
import os

fileName = 'SCG_5k_Kaldheim_2-21-2021.csv'

rawCSV = pd.read_csv(os.path.dirname(
    os.path.dirname(__file__)) + f'\\Data Raw\\{fileName}')
rawCSV.set_index('Rank', inplace=True)

deckSeries = rawCSV['List']
newDF = pd.DataFrame(
    columns=['Rank', 'Player', 'Deck', 'Wins', 'Losses', 'Card', 'Count', 'Main/Side'])

# %%
for index, deck in enumerate(deckSeries):
    recordAsDateTime = datetime.strptime(rawCSV.iat[index, 2], '%m/%d/%Y')
    wins = recordAsDateTime.month
    losses = recordAsDateTime.day
    deck = deck.split('\n')
    mainOrSide = None
    skip = False
    for line in deck:
        if line == 'Companion':
            skip = True
            continue
        elif skip == True:
            skip = False
            continue
        elif line == '':
            continue
        elif line == 'Deck':
            mainOrSide = 'Main'
            continue
        elif line == 'Sideboard':
            mainOrSide = 'Sideboard'
            continue
        newRow = {'Rank': index+1, 'Player': rawCSV.iat[index, 0], 'Deck': rawCSV.iat[index, 1], 'Wins': wins,
                  'Losses': losses, 'Card': line[2:], 'Count': int(line[:2].strip()), 'Main/Side': mainOrSide}
        newDF = newDF.append(newRow, ignore_index=True)

# %%
newDF.to_csv(os.path.dirname(
    os.path.dirname(__file__)) + f'\\Data Raw\\CORRECTED_{fileName}', index=False)
