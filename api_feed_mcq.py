import time
import openai
import pandas as pd


def ask_gpt_for_move(fen, choices):
    prompt = f"The chess board is set up as follows, in FEN format: {fen}. What would be the best next move in UCI format? Your answer should only include the four-digit UCI notation, and nothing else. Here are your choices:\n"
    for idx, choice in enumerate(choices, 1):
        prompt += f"{idx}. {choice}\n"

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

    df.to_csv('gpt_mcq_hard.csv', index=False)


if __name__ == '__main__':
    main()
