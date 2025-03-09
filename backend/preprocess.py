import pandas as pd
import os
from sklearn.model_selection import train_test_split

real_path = os.path.join(os.getcwd(), "datasets", "True.csv")
fake_path = os.path.join(os.getcwd(), "datasets", "Fake.csv")

real = pd.read_csv(real_path)
fake = pd.read_csv(fake_path)

real = real.drop(columns=['subject', 'date', "title"])
fake = fake.drop(columns=['subject', 'date', "title"])

real['label'] = 0
fake['label'] = 1

cleaned_dataset = pd.concat([real, fake])

cleaned_dataset = cleaned_dataset.sample(frac=1).reset_index(drop=True)

X, y = cleaned_dataset.drop(columns=['label']), cleaned_dataset['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

full_train = pd.concat([X_train, y_train], axis=1)
full_test = pd.concat([X_test, y_test], axis=1)

full_test.reset_index(drop=True, inplace=True)
full_train.reset_index(drop=True, inplace=True)

train_path = os.path.join(os.getcwd(), "datasets", "cleaned_data_train.csv")
test_path = os.path.join(os.getcwd(), "datasets", "cleaned_data_test.csv")

full_test.to_csv(test_path, index=False)
full_train.to_csv(train_path, index=False)