import pandas as pd
import chess
import chess.engine
import random


def generate_top_moves(fen, stockfish_path, counter):
    board = chess.Board(fen)
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    top_moves = []

    # Get best moves according to Stockfish
    with engine.analysis(board, chess.engine.Limit(time=0.5)) as analysis:
        for info in analysis:
            if 'pv' in info and info['pv']:
                move = info['pv'][0]
                if board.uci(move) not in top_moves:
                    top_moves.append(board.uci(move))

            if len(top_moves) >= 4:
                break

    engine.quit()

    # Add random moves if less than 4 top moves are found
    while len(top_moves) < 4:
        legal_moves = [board.uci(move) for move in board.legal_moves]
        random_move = random.choice(legal_moves)
        if random_move not in top_moves:
            top_moves.append(random_move)

    # Shuffle the moves to randomize the choices
    random.shuffle(top_moves)

    # Display progress
    counter[0] += 1
    print(f"Evaluated {counter[0]} positions")

    return top_moves


def add_top_moves_to_csv(input_csv, output_csv, stockfish_path):
    # Read the CSV into a DataFrame
    df = pd.read_csv(input_csv)

    # Add the "BestMove" column by extracting 6th to 9th characters from the "Moves" column
    df['BestMove'] = df['Moves'].str[5:9]

    # Initialize counter for progress tracking
    counter = [0]

    # Generate top moves and add them to new columns
    df['A'], df['B'], df['C'], df['D'] = zip(*df['FEN'].apply(lambda x: generate_top_moves(x, stockfish_path, counter)))

    # Save the modified DataFrame back to a new CSV file
    df.to_csv(output_csv, index=False)


# Replace 'input.csv' with the name of your input CSV file
# Replace 'output.csv' with the name you want for the output CSV file
# Replace 'path/to/stockfish' with the path to your Stockfish executable
stockfish_path = '/opt/homebrew/cellar/stockfish/16/bin/stockfish'
add_top_moves_to_csv('hard.csv', 'mcq_hard.csv', stockfish_path)
