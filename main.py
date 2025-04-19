import streamlit as st
import pandas as pd
import altair as alt
from mlb_hr_model import load_model, get_today_predictions
from scraper.player_stats import get_player_stats
from scraper.odds_scraper import get_hr_odds

st.set_page_config(page_title="MLB HR AI Predictor", layout="wide")

# Load model
model = load_model("models/hr_model.pkl")

# Manual refresh button
if st.button("🔄 Refresh Player Data & Odds"):
    st.experimental_rerun()

# Get real player stats and odds
stats_df = get_player_stats()
odds_df = get_hr_odds()
merged_df = pd.merge(stats_df, odds_df, on="Player", how="inner")

# Fill mock feature values (in real use, replace with engineered features)
merged_df["barrel_pct"] = 0.12
merged_df["avg_exit_velocity"] = 91.4
merged_df["hr_rate"] = merged_df["HR"] / merged_df["G"]
merged_df["pitcher_hr_per_9"] = 1.1
merged_df["matchup_score"] = 1.0
merged_df["weather_boost"] = 1.0
merged_df["park_hr_factor"] = 1.0

# Predict
results = get_today_predictions(model, merged_df)

# Streamlit UI
st.title("⚾ MLB Home Run Prediction AI")
st.markdown("### 📊 Predicted Home Run Probabilities")
st.dataframe(results[["Player", "Team", "HR Odds", "HR Probability", "AI Rating"]])

# Bar chart
chart = alt.Chart(results).mark_bar().encode(
    x=alt.X('HR Probability', scale=alt.Scale(domain=[0, 1])),
    y=alt.Y('Player', sort='-x'),
    color=alt.Color('AI Rating', scale=alt.Scale(scheme='goldgreen'))
).properties(width=700, height=400, title="AI-Predicted HR Probability")

st.altair_chart(chart, use_container_width=True)

# CSV download
csv = results.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Projections as CSV", data=csv, file_name="hr_predictions.csv", mime="text/csv")