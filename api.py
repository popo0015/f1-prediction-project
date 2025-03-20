from fastapi import FastAPI
from fetch_data import fetch_f1_results
from train_model import train_model, predict_winner

app = FastAPI()

# Train the model on startup
model, le_constructor, le_driver = train_model()

@app.get("/")
def home():
    return {"message": "F1 Prediction API is running!"}

@app.get("/f1-data")
def get_f1_data():
    """API to fetch F1 race data dynamically."""
    df = fetch_f1_results(2023)
    return df.to_dict(orient="records")

@app.get("/predict")
def predict_race_winner(constructor: str, grid_position: int):
    """API to predict the winner based on constructor & grid position."""
    if not model:
        return {"error": "Model not trained yet!"}
    
    predicted_driver = predict_winner(model, le_constructor, le_driver, constructor, grid_position)
    return {"Predicted Winner": predicted_driver}
