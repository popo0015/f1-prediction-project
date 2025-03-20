import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from fetch_data import fetch_f1_results

def preprocess_data(df):
    """Prepares data by encoding categorical values and scaling numerical features."""
    if df.empty:
        print("No data available for training!")
        return None, None, None, None

    # Feature Selection
    features = df[["Grid Position", "Constructor"]].copy()
    target = df["Driver"]

    # Encode categorical features
    le_constructor = LabelEncoder()
    le_driver = LabelEncoder()

    features["Constructor"] = le_constructor.fit_transform(features["Constructor"])
    target = le_driver.fit_transform(target)

    # Scale numerical features
    scaler = StandardScaler()
    features["Grid Position"] = scaler.fit_transform(features[["Grid Position"]])

    return features, pd.Series(target), le_constructor, le_driver  # Convert target to Pandas Series

def train_model():
    """Trains a model using data from multiple seasons for better accuracy."""
    seasons = [2021, 2022, 2023]  # Train on multiple years
    all_data = pd.concat([fetch_f1_results(season) for season in seasons], ignore_index=True)

    features, target, le_constructor, le_driver = preprocess_data(all_data)

    if features is None or len(features) < 10:
        print("Not enough data to train the model!")
        return None, None, None

    # Convert target to Pandas Series before checking class distribution
    target_series = pd.Series(target)

    # Class distribution before filtering
    class_counts = target_series.value_counts()
    print(f"Class distribution before filtering:\n{class_counts}")

    # Remove classes (drivers) with only 1 appearance
    valid_classes = class_counts[class_counts > 1].index
    mask = target_series.isin(valid_classes)

    features = features[mask]
    target_series = target_series[mask]  # Use Pandas Series for target

    print(f"Class distribution after filtering:\n{target_series.value_counts()}")

    # If the remaining classes allow stratified splitting, use it
    if len(target_series.unique()) > 1:
        stratify_option = target_series
    else:
        stratify_option = None  # Avoid stratify error

    # Train-test split (80-20)
    X_train, X_test, y_train, y_test = train_test_split(features, target_series, test_size=0.2, random_state=42, stratify=stratify_option)

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Model Accuracy
    accuracy = model.score(X_test, y_test)
    print(f"Model trained with {accuracy*100:.2f}% accuracy.")

    return model, le_constructor, le_driver
    """Trains a model using data from multiple seasons for better accuracy."""
    seasons = [2021, 2022, 2023]  # Train on multiple years
    all_data = pd.concat([fetch_f1_results(season) for season in seasons], ignore_index=True)

    features, target, le_constructor, le_driver = preprocess_data(all_data)

    if features is None or len(features) < 10:
        print("Not enough data to train the model!")
        return None, None, None

    # Convert target to a Pandas Series before checking class distribution
    target_series = pd.Series(target)

    # Class distribution before filtering
    class_counts = target_series.value_counts()
    print(f"Class distribution before filtering:\n{class_counts}")

    # Remove classes (drivers) with only 1 appearance
    valid_classes = class_counts[class_counts > 1].index
    mask = target_series.isin(valid_classes)

    features = features[mask]
    target_series = target_series[mask]  # Use Pandas Series for target

    print(f"Class distribution after filtering:\n{target_series.value_counts()}")

    # If the remaining classes allow stratified splitting, use it
    if len(target_series.unique()) > 1:
        stratify_option = target_series
    else:
        stratify_option = None  # Avoid stratify error

    # Train-test split (80-20)
    X_train, X_test, y_train, y_test = train_test_split(features, target_series, test_size=0.2, random_state=42, stratify=stratify_option)

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Model Accuracy
    accuracy = model.score(X_test, y_test)
    print(f"Model trained with {accuracy*100:.2f}% accuracy.")

    return model, le_constructor, le_driver

def predict_winner(model, le_constructor, le_driver, constructor: str, grid_pos: int):
    """Predicts the winner of an upcoming F1 race."""
    if model is None:
        return "Model is not trained"

    try:
        encoded_constructor = le_constructor.transform([constructor])[0]
        input_features = pd.DataFrame([[grid_pos, encoded_constructor]], columns=["Grid Position", "Constructor"])

        predicted_driver_encoded = model.predict(input_features)
        predicted_driver = le_driver.inverse_transform(predicted_driver_encoded)

        return predicted_driver[0]
    except Exception as e:
        return f"Prediction error: {e}"

# Train the model using multiple seasons
model, le_constructor, le_driver = train_model()

# Example prediction
if model:
    predicted_driver = predict_winner(model, le_constructor, le_driver, "Red Bull", 1)
    print(f"Predicted Winner: {predicted_driver}")
