import pandas as pd
import os

def preprocess_data(data_path):
    df = pd.read_csv(data_path, sep='\t', lineterminator='\n', on_bad_lines='skip')
    df = df.drop("Unnamed: 0", axis=1)
    df = df[df["lang"] == "en"]
    df = df.drop("lang", axis=1)
    return df

def save_data(df, data_path):
    df.to_csv(data_path, index=False)

def main():
    data_path = os.path.join(os.path.dirname(__file__), "datasets", "general-claim.csv")
    df = preprocess_data(data_path)
    save_path = os.path.join(os.path.dirname(__file__), "datasets", "cleaned_data.csv")
    save_data(df, save_path)

if __name__ == "__main__":
    main()