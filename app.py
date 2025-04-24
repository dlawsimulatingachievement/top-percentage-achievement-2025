import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import truncnorm, beta

st.title("Achievement Simulator")

# Truncated normal generator (rounded to int like Colab)
def truncated_normal(mean, std_dev, size, min_val=0, max_val=100):
    lower = (min_val - mean) / std_dev
    upper = (max_val - mean) / std_dev
    values = truncnorm.rvs(lower, upper, loc=mean, scale=std_dev, size=size)
    return np.round(values).astype(int)

# Beta left-skewed generator for effort
def left_skewed_effort(size):
    values = beta.rvs(a=5, b=2, size=size) * 100
    return np.clip(values, 0, 100).astype(int)

# Population dropdown (max 100,000)
population_options = (
    list(range(100, 1000, 100)) +
    list(range(1000, 10000, 1000)) +
    list(range(10000, 100001, 10000))
)
population = st.selectbox("Population size", options=population_options, index=population_options.index(10000), key="population")

talent = st.slider("Your Talent (1–100)", 1, 100, 50, key="talent")
effort = st.slider("Your Effort (1–100)", 1, 100, 50, key="effort")
attempts = st.selectbox("Number of Attempts", [1, 5, 10, 20, 30], index=2, key="attempts")
competition_cutoff = st.slider("Competition – Top X%", 1, 100, 10, step=1, key="competition")

# Effort distribution choice
use_left_skew = st.checkbox("Use left-skewed effort distribution (most people work very hard)", value=False)

show_distributions = st.checkbox("Show input distribution plots", value=False)

num_runs = 10000
st.write(f"📊 Population: **{population:,}** | 🎯 Target: **Top {competition_cutoff}%** | 🔁 Repeats: **{num_runs}**")
st.write(f"🧒 Talent: **{talent}**, 💪 Effort: **{effort}**, 🔁 Attempts: **{attempts}**")

with st.expander("Optional: Adjust Weightings (Must sum to 1.0)"):
    st.write("These control how much each factor contributes to achievement.")
    talent_weight = st.number_input("Talent Weight", 0.0, 1.0, 0.29, step=0.01, key="talent_weight")
    effort_weight = st.number_input("Effort Weight", 0.0, 1.0, 0.29, step=0.01, key="effort_weight")
    luck_weight = st.number_input("Luck Weight", 0.0, 1.0, 0.42, step=0.01, key="luck_weight")

    total = talent_weight + effort_weight + luck_weight
    if total != 1.0:
        st.warning(f"⚠️ Your weights currently sum to {total:.2f}. They must sum to 1.0 for the simulation to work correctly.")

if st.button("Run Simulation"):
    if talent_weight + effort_weight + luck_weight == 1.0:
        st.markdown("---")
        st.subheader("🎉 Running Simulation...")

        success_count = 0

        for run in range(num_runs):
            talent_pop = truncated_normal(50, 20, population)
            effort_pop = left_skewed_effort(population) if use_left_skew else truncated_normal(50, 20, population)
            luck_pop = np.array([truncated_normal(50, 20, population) for _ in range(attempts)]).T

            if show_distributions and run == 0:
                st.subheader("🔍 Input Distributions")
                bins = np.arange(0, 102) - 0.5

                fig1, ax1 = plt.subplots()
                ax1.hist(talent_pop, bins=bins, color='skyblue', edgecolor='black')
                ax1.set_title("Talent Distribution")
                st.pyplot(fig1)

                fig2, ax2 = plt.subplots()
                ax2.hist(effort_pop, bins=bins, color='lightgreen', edgecolor='black')
                ax2.set_title("Effort Distribution")
                st.pyplot(fig2)

                fig3, ax3 = plt.subplots()
                ax3.hist(luck_pop[:, 0], bins=bins, color='orange', edgecolor='black')
                ax3.set_title("Luck Distribution (1st Attempt)")
                st.pyplot(fig3)

            achievement_pop = np.zeros(population)
            for i in range(attempts):
                achievement_pop += (
                    (talent_pop * talent_weight)
                    + (effort_pop * effort_weight)
                    + (luck_pop[:, i] * luck_weight)
                )

            user_luck = np.random.randint(0, 101, size=attempts)
            user_achievement = 0
            for i in range(attempts):
                user_achievement += (
                    (talent * talent_weight)
                    + (effort * effort_weight)
                    + (user_luck[i] * luck_weight)
                )

            threshold = np.percentile(achievement_pop, 100 - competition_cutoff)
            if user_achievement >= threshold:
                success_count += 1

        chance = (success_count / num_runs) * 100
        st.subheader("📈 Results")
        st.write(f"You have a **{chance:.1f}% chance** of being in the **top {competition_cutoff}%**.")
    else:
