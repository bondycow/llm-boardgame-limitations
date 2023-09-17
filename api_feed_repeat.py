import time
import openai
import pandas as pd


def ask_gpt_for_move(fen, correct_move, max_attempts=3):
    base_prompt = f"The chess board is set up as follows, in FEN format: {fen}. What would be the best next move in UCI (Universal Chess Interface) format? Your answer should only include the four-digit UCI notation, and nothing else. Do not add in anything other than the notation, no punctuation marks nor explanation for your choice."

    for attempt in range(max_attempts):
        messages = [
            {"role": "system", "content": "You are a helpful assistant specialized in chess."},
            {"role": "user", "content": base_prompt}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )

        move_uci = response['choices'][0]['message']['content'].strip().split()[0]

        if move_uci == correct_move:
            break
        else:
            print(f"Incorrect move, attempt {attempt + 1}")

    return move_uci


def calculate_accuracy(df):
    correct_predictions = df[df['GPT_BestMove'] == df['BestMove']].shape[0]
    total_predictions = df.shape[0]
    accuracy = (correct_predictions / total_predictions) * 100
    return accuracy


def main():
    openai.api_key = ""  # Replace with your actual API key
    df = pd.read_csv('mcq_easy.csv')

    for index, row in df.iterrows():
        retries = 0
        correct_move = row['BestMove']  # Extract the correct move for this row from the DataFrame
        while retries < 5:  # Retry up to 5 times for service errors
            try:
                df.loc[index, 'GPT_BestMove'] = ask_gpt_for_move(row['FEN'], correct_move)
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

    df.to_csv('gpt_repeat_mt3.csv', index=False)


if __name__ == '__main__':
    main()
