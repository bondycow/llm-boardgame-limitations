import pandas as pd
import chess


# Function to update FEN based on a move in UCI notation
def update_fen(fen, move):
    board = chess.Board(fen)
    try:
        board.push_uci(move)
    except:
        return "Invalid Move"
    return board.fen()


# Read the first CSV file and take only the first 500 rows
df1 = pd.read_csv('lichess_db_puzzle.csv').iloc[:500]

# Extract FEN column and the characters of Moves until a space
df1_new = df1[['FEN']].copy()
df1_new['Moves'] = df1['Moves'].apply(lambda x: x.split()[0] if ' ' in x else x)

# Create a new FEN column based on applying the Moves to the original FEN
df1_new['FEN2'] = df1.apply(
    lambda row: update_fen(row['FEN'], row['Moves'].split()[0] if ' ' in row['Moves'] else row['Moves']), axis=1)

# Rename the columns
df1_new.columns = ['FEN1', 'Moves', 'FEN2']

# Write the new DataFrame to a new CSV file
df1_new.to_csv('fen_test.csv', index=False)
