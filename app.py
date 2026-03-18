import streamlit as st
import pandas as pd

st.set_page_config(page_title="IPL Analytics", layout="wide")

st.title("🏏 IPL Analytics Dashboard")

uploaded_file = st.file_uploader("Upload IPL Dataset (.xlsx)")

# Cache to make app fast
@st.cache_data
def load_data(file):
    return pd.read_excel(file, sheet_name="Deliveries")

if uploaded_file is not None:

    deliveries = load_data(uploaded_file)

    st.success("Dataset Loaded Successfully ✅")

    # ---------------- PLAYER SELECT ----------------
    player = st.selectbox(
        "Select Batter",
        sorted(deliveries["Batter"].dropna().unique())
    )

    data = deliveries[deliveries["Batter"] == player]

    runs = data["Batter Runs"].sum()
    balls = len(data)
    fours = len(data[data["Batter Runs"] == 4])
    sixes = len(data[data["Batter Runs"] == 6])

    strike_rate = (runs / balls) * 100 if balls > 0 else 0

    # ---------------- PLAYER STATS ----------------
    st.subheader(f"📊 {player} Stats")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Runs", runs)
    col2.metric("Balls", balls)
    col3.metric("Strike Rate", round(strike_rate, 2))
    col4.metric("Fours / Sixes", f"{fours} / {sixes}")

    # ---------------- TOP RUN SCORERS ----------------
    st.subheader("🔥 Top 10 Run Scorers")

    top_runs = (
        deliveries.groupby("Batter")["Batter Runs"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.dataframe(top_runs)
    st.bar_chart(top_runs)

    # ---------------- ADDITIONAL ANALYTICS ----------------
    st.subheader("⚡ Extra Insights")

    total_runs = deliveries["Batter Runs"].sum()
    total_balls = len(deliveries)

    st.write("Total Runs in Dataset:", total_runs)
    st.write("Total Balls in Dataset:", total_balls)

else:
    st.info("Please upload your IPL dataset to begin")
st.subheader("⚔️ Batter vs Bowler Analysis")

col1, col2 = st.columns(2)

batter = col1.selectbox(
    "Select Batter (Battle)",
    sorted(deliveries["Batter"].dropna().unique()),
    key="batter_vs"
)

bowler = col2.selectbox(
    "Select Bowler",
    sorted(deliveries["Bowler"].dropna().unique())
)

battle_data = deliveries[
    (deliveries["Batter"] == batter) &
    (deliveries["Bowler"] == bowler)
]

runs = battle_data["Batter Runs"].sum()
balls = len(battle_data)
dismissals = battle_data["Is Wicket"].sum()

sr = (runs / balls) * 100 if balls > 0 else 0

st.write(f"Runs: {runs}")
st.write(f"Balls: {balls}")
st.write(f"Dismissals: {dismissals}")
st.write(f"Strike Rate: {round(sr,2)}")
st.bar_chart(battle_data["Batter Runs"].value_counts())
st.subheader("📈 Over-wise Runs Analysis")

selected_player = st.selectbox(
    "Select Batter (Over Analysis)",
    sorted(deliveries["Batter"].dropna().unique()),
    key="over_analysis"
)

player_data = deliveries[deliveries["Batter"] == selected_player]

over_runs = (
    player_data.groupby("Over Number")["Batter Runs"]
    .sum()
)

st.line_chart(over_runs)
st.subheader("⚡ Phase-wise Performance")

def get_phase(over):
    if over <= 6:
        return "Powerplay"
    elif over <= 15:
        return "Middle"
    else:
        return "Death"

player_data["Phase"] = player_data["Over Number"].apply(get_phase)

phase_stats = (
    player_data.groupby("Phase")["Batter Runs"]
    .sum()
)

st.bar_chart(phase_stats)
st.subheader("🎯 Win Probability Estimator")

col1, col2, col3 = st.columns(3)

current_runs = col1.number_input("Current Score", min_value=0, value=50)
overs = col2.number_input("Overs Completed", min_value=0.0, max_value=20.0, value=10.0)
target = col3.number_input("Target", min_value=1, value=180)

# Simple logic
balls_remaining = int((20 - overs) * 6)
runs_needed = target - current_runs

required_rr = (runs_needed / (balls_remaining/6)) if balls_remaining > 0 else 0

# Basic probability model
if required_rr <= 6:
    win_prob = 80
elif required_rr <= 8:
    win_prob = 65
elif required_rr <= 10:
    win_prob = 45
elif required_rr <= 12:
    win_prob = 25
else:
    win_prob = 10

st.metric("Win Probability (%)", f"{win_prob}%")
st.write("Required Run Rate:", round(required_rr,2))
