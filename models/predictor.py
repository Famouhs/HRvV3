
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

MODEL_PATH = "model/hr_model.pkl"

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
    return joblib.load(MODEL_PATH)

def predict_home_runs(player_stats_df):
    """
    Takes a DataFrame with player stats and returns home run predictions.
    """
    model = load_model()
    features = player_stats_df.drop(columns=["Player", "Team", "HR_Odds"], errors="ignore")
    predictions = model.predict(features)
    player_stats_df["HR_Prediction"] = predictions
    return player_stats_df
