import time
import openai
import pandas as pd


def ask_gpt_for_move(fen, move):
    prompt = f"The chess board is set up as follows, in FEN format: {fen}. This move: {move}, expressed in UCI notation, is made. What is the FEN of the board after the move. Your answer should only include the FEN string."
    messages = [
        {"role": "system", "content": "You are a helpful assistant specialized in chess."},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    new_fen = response['choices'][0]['message']['content']
    return new_fen


def calculate_accuracy(df):
    correct_predictions = df[df['GPT_FEN'] == df['FEN2']].shape[0]
    total_predictions = df.shape[0]
    accuracy = (correct_predictions / total_predictions) * 100
    return accuracy


def main():
    openai.api_key = ""  # Replace with your actual API key
    df = pd.read_csv('fen_test.csv').iloc[:150]

    for index, row in df.iterrows():
        retries = 0
        while retries < 5:  # Retry up to 5 times
            try:
                df.loc[index, 'GPT_FEN'] = ask_gpt_for_move(row['FEN1'], row['Moves'])
                print(f"Successfully processed row {index}")
                break
            except openai.error.ServiceUnavailableError:
                print(f"Server unavailable, retrying row {index}")
                retries += 1
                time.sleep(2 ** retries)  # Exponential backoff

    accuracy = calculate_accuracy(df)
    print(f"Model's accuracy: {accuracy}%")

    # Add a row to save model's accuracy
    accuracy_row = pd.DataFrame([{'FEN1': 'Model Accuracy', 'FEN2': accuracy}], columns=df.columns)
    df = pd.concat([df, accuracy_row]).reset_index(drop=True)

    df.to_csv('fen_gpt.csv', index=False)


if __name__ == '__main__':
    main()
