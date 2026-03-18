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
