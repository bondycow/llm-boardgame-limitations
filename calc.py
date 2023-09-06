import pandas as pd


def calculate_accuracy(input_csv):
    # Read the CSV into a DataFrame
    df = pd.read_csv(input_csv)

    # Count the number of rows where 'BestMove' is equal to 'GPT_BestMove'
    correct_predictions = df[df['BestMove'] == df['GPT_BestMove']].shape[0]

    # Get the total number of rows
    total_predictions = df.shape[0]

    # Calculate the accuracy
    if total_predictions != 0:  # To prevent division by zero
        accuracy = (correct_predictions / total_predictions) * 100
    else:
        accuracy = 0.0

    return accuracy


input_csv = 'gpt_easy.csv'  # Replace with the name of your CSV file
accuracy = calculate_accuracy(input_csv)
print(f"Accuracy: {accuracy}%")
