import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Achievement Simulator")

# 🎛️ Population dropdown (max 100,000)
population_options = (
    list(range(100, 1000, 100)) +          # 100 to 900 (steps of 100)
    list(range(1000, 10000, 1000)) +       # 1,000 to 9,000 (steps of 1,000)
    list(range(10000, 100001, 10000))      # 10,000 to 100,000 (steps of 10,000)
)

population = st.selectbox(
    "Population size",
    options=population_options,
    index=population_options.index(10000),
    key="population"
)

talent = st.slider("Your Talent (1–100)", min_value=1, max_value=100, value=50, key="talent")
effort = st.slider("Your Effort (1–100)", min_value=1, max_value=100, value=50, key="effort")
attempts = st.selectbox("Number of Attempts", options=[1, 5, 10, 20, 30], index=2, key="attempts")
competition_cutoff = st.slider("Competition – Top X%", min_value=1, max_value=100, value=10, step=1, key="competition")

# Fixed simulation settings
num_runs = 10000
st.write(f"📊 Population: **{population:,}** | 🎯 Target: **Top {competition_cutoff}%** | 🔁 Repeats: **{num_runs}**")
st.write(f"🧠 Talent: **{talent}**, 💪 Effort: **{effort}**, 🔁 Attempts: **{attempts}**")

# ⚙️ Optional weightings
with st.expander("Optional: Adjust Weightings (Must sum to 1.0)"):
    st.write("These control how much each factor contributes to achievement.")
    talent_weight = st.number_input("Talent Weight", min_value=0.0, max_value=1.0, value=0.29, step=0.01, key="talent_weight")
    effort_weight = st.number_input("Effort Weight", min_value=0.0, max_value=1.0, value=0.29, step=0.01, key="effort_weight")
    luck_weight = st.number_input("Luck Weight", min_value=0.0, max_value=1.0, value=0.42,
