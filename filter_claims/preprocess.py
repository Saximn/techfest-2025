import pandas as pd
import os
from sklearn.model_selection import train_test_split

def preprocess_data(data_path):
    df = pd.read_csv(data_path, sep='\t', lineterminator='\n', on_bad_lines='skip')
    df = df.drop("Unnamed: 0", axis=1)
    df = df[df["lang"] == "en"]
    df = df.drop(['lang', 'topic', 'style', 'source',], axis=1)
    return df

def split_data(df, train_size=0.95):
    X = df.drop("label", axis=1)
    Y = df["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, train_size=train_size, random_state=42, stratify=Y)
    full_X = pd.concat([X_train, X_test], axis=1)
    full_Y = pd.concat([y_train, y_test], axis=1)
    return full_X, full_Y


def save_data(df, data_path):
    df.to_csv(data_path, index=False)

def main():
    data_path = os.path.join(os.path.dirname(__file__), "datasets", "general-claim.csv")
    df = preprocess_data(data_path)
    train, test = split_data(df)
    save_path_train = os.path.join(os.path.dirname(__file__), "datasets", "cleaned_data_train.csv")
    save_path_test = os.path.join(os.path.dirname(__file__), "datasets", "cleaned_data_test.csv")
    save_data(train, save_path_train)
    save_data(test, save_path_test)

if __name__ == "__main__":
    main()