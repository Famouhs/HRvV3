import joblib
import pandas as pd

def load_model(path="models/hr_model.pkl"):
    """Load the trained XGBoost home run prediction model."""
    return joblib.load(path)

def get_today_predictions(model, features_df):
    """Generate predictions using the trained model and feature DataFrame."""
    X = features_df.drop(columns=["Player", "Team", "HR Odds"], errors="ignore")
    y_pred_proba = model.predict_proba(X)[:, 1]
    features_df["HR Probability"] = y_pred_proba
    features_df["AI Rating"] = pd.cut(
        y_pred_proba,
        bins=[0, 0.1, 0.2, 0.3, 0.4, 1.0],
        labels=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
    )
    return features_df.sort_values(by="HR Probability", ascending=False).reset_index(drop=True)