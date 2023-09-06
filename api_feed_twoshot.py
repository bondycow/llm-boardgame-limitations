import time
import openai
import pandas as pd


def ask_gpt_for_move(fen, choices):
    example_fen1 = "6k1/6p1/R5K1/8/p2rp3/8/5P1P/8 w - - 12 41"
    example_move1 = "a6a8"
    example_fen2 = "4rk2/ppp1rp1p/8/5p2/3p4/P2P2R1/KPP5/6R1 w - - 0 26"
    example_move2 = "g3g8"

    prompt = f"Example 1: For the FEN {example_fen1}, the best next move in UCI format is {example_move1}.\nExample 2: For the FEN {example_fen2}, the best next move in UCI format is {example_move2}.\n\nThe chess board for the current question is set up as follows, in FEN format: {fen}. What would be the best next move in UCI (Universal Chess Interface) format? Your answer should only include the four-digit UCI notation, and nothing else. Do not add in anything other than the notation; no punctuation marks nor explanation for your choice."

    messages = [
        {"role": "system", "content": "You are a helpful assistant specialized in chess."},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )

    move_uci = response['choices'][0]['message']['content'].strip().split()[0]
    return move_uci


def calculate_accuracy(df):
    correct_predictions = df[df['GPT_BestMove'] == df['BestMove']].shape[0]
    total_predictions = df.shape[0]
    accuracy = (correct_predictions / total_predictions) * 100
    return accuracy


def main():
    openai.api_key = ""  # Replace with your actual API key
    df = pd.read_csv('mcq_hard.csv')

    for index, row in df.iterrows():
        choices = [row['A'], row['B'], row['C'], row['D']]
        retries = 0
        while retries < 5:  # Retry up to 5 times
            try:
                df.loc[index, 'GPT_BestMove'] = ask_gpt_for_move(row['FEN'], choices)
                print(f"Successfully processed row {index}")
                break
            except openai.error.ServiceUnavailableError:
                print(f"Server unavailable, retrying row {index}")
                retries += 1
                time.sleep(2 ** retries)  # Exponential backoff

    accuracy = calculate_accuracy(df)
    print(f"Model's accuracy: {accuracy}%")

    # Add a row to save model's accuracy
    accuracy_row = pd.DataFrame([{'FEN': 'Model Accuracy', 'GPT_BestMove': accuracy}], columns=df.columns)
    df = pd.concat([df, accuracy_row]).reset_index(drop=True)

    df.to_csv('gpt_twoshot_hard.csv', index=False)


if __name__ == '__main__':
    main()
