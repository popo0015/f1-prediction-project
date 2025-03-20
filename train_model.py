import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def get_data():
    df = fetch_f1_results()
    X = df[["round"]]
    y = df.index
    return X, y

X, y = get_data()
model = RandomForestClassifier()
model.fit(X, y)
print("Model trained dynamically!")
