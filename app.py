import streamlit as st
import numpy as np

st.title("Achievement Simulator")

# 🎛️ Population dropdown (cleaner!)
population_options = (
    list(range(100, 1000, 100)) +          # 100 to 900 (steps of 100)
    list(range(1000, 10000, 1000)) +       # 1,000 to 9,000 (steps of 1,000)
    list(range(10000, 100001, 10000))      # 10,000 to 100,000 (steps of 10,000)
)

population = st.selectbox(
    "Population size",
    options=population_options,
    index=population_options.index(10000),  # Default to 10,000
    key="population"
)

# 🌟 User settings
talent = st.slider("Your Talent (1–100)", min_value=1, max_value=100, value=50, key="talent")
effort = st.slider("Your Effort (1–100)", min_value=1, max_value=100, value=50, key="effort")
attempts = st.selectbox("Number of Attempts", options=[1, 5, 10, 20, 30], index=2, key="attempts")
competition_cutoff = st.slider("Competition – Top X%", min_value=1, max_value=100, value=10, step=1, key="competition")

# 🧠 Info
num_runs = 10000
st.write(f"📊 Population: **{population:,}** | 🎯 Target: **Top {competition_cutoff}%**")
st.write(f"🧠 Talent: **{talent}**, 💪 Effort: **{effort}**, 🔁 Attempts: **{attempts}**")

# ⚙️ Optional weights
with st.expander("Optional: Adjust Weightings (Must sum to 1.0)"):
    st.write("These control how much each factor contributes to achievement.")
    talent_weight = st.number_input("Talent Weight", min_value=0.0, max_value=1.0, value=0.29, step=0.01, key="talent_weight")
    effort_weight = st.number_input("Effort Weight", min_value=0.0, max_value=1.0, value=0.29, step=0.01, key="effort_weight")
    luck_weight = st.number_input("Luck Weight", min_value=0.0, max_value=1.0, value=0.42, step=0.01, key="luck_weight")

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
            # Generate population
            talent_pop = np.random.normal(loc=50, scale=20, size=population)
            effort_pop = np.random.normal(loc=50, scale=20, size=population)
            luck_pop = np.random.normal(loc=50, scale=20, size=(population, attempts))

            # Clip and round
            talent_pop = np.clip(np.round(talent_pop), 0, 100)
            effort_pop = np.clip(np.round(effort_pop), 0, 100)
            luck_pop = np.clip(np.round(luck_pop), 0, 100)

            # Population achievement
            achievement_pop = np.zeros(population)
            for i in range(attempts):
                achievement_pop += (
                    (talent_pop * talent_weight)
                    + (effort_pop * effort_weight)
                    + (luck_pop[:, i] * luck_weight)
                )

            # User achievement
            user_luck = np.random.randint(0, 101, size=attempts)
            user_achievement = 0
            for i in range(attempts):
                user_achievement += (
                    (talent * talent_weight)
                    + (effort * effort_weight)
                    + (user_luck[i] * luck_weight)
                )

            # Check if user in top X%
            threshold = np.percentile(achievement_pop, 100 - competition_cutoff)
            if user_achievement >= threshold:
                success_count += 1

        # Show results
        chance = (success_count / num_runs) * 100
        st.subheader("📈 Results")
        st.write(f"You have a **{chance:.1f}% chance** of being in the **top {competition_cutoff}%**.")
    else:
        st.error("⚠️ Simulation cannot run: Weightings must sum to 1.0.")
