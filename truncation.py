import pandas as pd
import chess


def filter_rows_by_theme_and_popularity(df):
    df = df[df['Themes'].str.contains("mate", na=False)].copy()
    bins = list(range(400, 2000, 100))
    df.loc[:, 'RatingBin'] = pd.cut(df['Rating'], bins=bins)
    df = df.groupby('RatingBin').apply(lambda x: x.nlargest(100, 'Popularity')).reset_index(drop=True)
    return df


def divide_into_difficulty(df):
    easy = df[df['Rating'] < 900].copy()
    intermediate = df[(df['Rating'] >= 900) & (df['Rating'] < 1400)].copy()
    hard = df[df['Rating'] >= 1400].copy()
    return easy, intermediate, hard


def update_fen_with_move(row):
    board = chess.Board(row['FEN'])
    uci_move = row['Moves'][:4]
    move = chess.Move.from_uci(uci_move)
    board.push(move)
    return board.fen()


# Read the original CSV file
df = pd.read_csv('lichess_db_puzzle.csv')

# Filter rows and keep top 100 by popularity for each rating range
filtered_df = filter_rows_by_theme_and_popularity(df)

# Update FENs based on the Moves column
filtered_df['FEN'] = filtered_df.apply(update_fen_with_move, axis=1)

# Divide DataFrame into different difficulty levels
easy, intermediate, hard = divide_into_difficulty(filtered_df)

# Save the new DataFrames into CSV files
easy.to_csv('easy.csv', index=False)
intermediate.to_csv('intermediate.csv', index=False)
hard.to_csv('hard.csv', index=False)
