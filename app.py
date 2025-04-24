import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import truncnorm

st.title("Achievement Simulator")

# 🎯 Truncated normal generator (true truncation, not clipping)
def generate_truncnorm(mean, std, size):
    a, b = (0 - mean) / std, (100 - mean) / std
    return truncnorm.rvs(a, b, loc=mean, scale=std, size=size)

# 🎛️ Population dropdown (max 100,000)
population_options = (
    list(range(100, 1000, 100)) +
    list(range(1000, 10000, 1000)) +
    list(range(10000, 100001, 10000))
)
population = st.selectbox(
    "Population size",
    options=population_options,
    index=population_options.index(10000),
    key="population"
)

talent = st.slider("Your Talent (1–100)", 1, 100, 50, key="talent")
effort = st.slider("Your Effort (1–100)", 1, 100, 50, key="effort")
attempts = st.selectbox("Number of Attempts", [1, 5, 10, 20, 30], index=2, key="attempts")
competition_cutoff = st.slider("Competition – Top X%", 1, 100, 10, step=1, key="competition")

# Fixed simulation settings
num_runs = 10000
st.write(f"📊 Population: **{population:,}** | 🎯 Target: **Top {competition_cutoff}%** | 🔁 Repeats: **{num_runs}**")
st.write(f"🧠 Talent: **{talent}**, 💪 Effort: **{effort}**, 🔁 Attempts: **{attempts}**")

# ⚙️ Optional weightings
with st.expander("Optional: Adjust Weightings (Must sum to 1.0)"):
    st.write("These control how much each factor contributes to achievement.")
    talent_weight = st.number_input("Talent Weight", 0.0, 1.0, 0.29, step=0.01, key="talent_weight")
    effort_weight = st.number_input("Effort Weight", 0.0, 1.0, 0.29, step=0.01, key="effort_weight")
    luck_weight = st.number_input("Luck Weight", 0.0, 1.0, 0.42, step=0.01, key="luck_weight")

    total = talent_weight + effort_weight + luck_weight
    if total != 1.0:
        st.warning(f"⚠️ Your weights currently sum to {total:.2f}. They must sum to 1.0 for the simulation to work correctly.")

# 🟢 Run simulation
if st.button("Run Simulation"):
    if talent_weight + effort_weight + luck_weight == 1.0:
        st.markdown("---")
        st.subheader("🎉 Running Simulation...")

        success_count = 0

        for run in range(num_runs):
            talent_pop = np.round(generate_truncnorm(50, 20, population))
            effort_pop = np.round(generate_truncnorm(50, 20, population))
            luck_pop = np.round(generate_truncnorm(50, 20, (population, attempts)))

            if run == 0:
                st.subheader("🔍 Input Distributions")

                fig1, ax1 = plt.subplots()
                ax1.hist(talent_pop, bins=range(0, 101), color='skyblue', edgecolor='black')
                ax1.set_title("Talent Distribution")
                st.pyplot(fig1)

                fig2, ax2 = plt.subplots()
                ax2.hist(effort_pop, bins=range(0, 101), color='lightgreen', edgecolor='black')
                ax2.set_title("Effort Distribution")
                st.pyplot(fig2)

                fig3, ax3 = plt.subplots()
                ax3.hist(luck_pop[:, 0], bins=range(0, 101), color='orange', edgecolor='black')
                ax3.set_title("Luck Distribution (1st Attempt)")
                st.pyplot(fig3)

            achievement_pop = np.zeros(population)
            for i in range(attempts):
                achievement_pop += (
                    (talent_pop * talent_weight)
                    + (effort_pop * effort_weight)
                    + (luck_pop[:, i_
