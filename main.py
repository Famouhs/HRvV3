import os
import sys
import streamlit as st
import pandas as pd
from datetime import datetime

# Ensure local modules are importable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraper.player_stats import get_player_stats
from scraper.odds_scraper import get_odds_data
from model.predictor import predict_home_runs
from visuals.charts import plot_top_predictions

# --- App Title ---
st.set_page_config(page_title="MLB Home Run Predictor", layout="wide")
st.title("⚾ MLB Home Run AI Predictor")

# --- Refresh Button ---
if st.button("🔄 Refresh Data"):
    st.experimental_rerun()

# --- Load and Process Data ---
try:
    st.info("Loading player statistics...")
    player_stats = get_player_stats()

    st.info("Fetching odds data...")
    odds_data = get_odds_data()

    st.success("Data loaded successfully!")

    # --- Merge and Predict ---
    st.info("Generating home run predictions...")
    predictions = predict_home_runs(player_stats, odds_data)

    if predictions.empty:
        st.warning("No projections available at this time.")
    else:
        # --- Display Results ---
        st.subheader("🔍 Top HR Predictions Today")
        st.dataframe(predictions, use_container_width=True)

        # --- Visual Chart ---
        st.subheader("📊 Home Run Prediction Chart")
        fig = plot_top_predictions(predictions)
        st.plotly_chart(fig, use_container_width=True)

        # --- Download Button ---
        csv_data = predictions.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Projections as CSV",
            data=csv_data,
            file_name=f"hr_projections_{datetime.now().strftime('%Y-%m-%d')}.csv",
            mime="text/csv"
        )
except Exception as e:
    st.error(f"An error occurred: {e}")
