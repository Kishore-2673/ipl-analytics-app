import streamlit as st
import pandas as pd

st.title("IPL Analytics Dashboard")

uploaded_file = st.file_uploader("Upload IPL Dataset")

if uploaded_file:
    deliveries = pd.read_excel(uploaded_file, sheet_name="Deliveries")

    player = st.selectbox("Select Batter", deliveries["Batter"].unique())

    data = deliveries[deliveries["Batter"] == player]

    runs = data["Batter Runs"].sum()
    balls = len(data)

    st.write("Runs:", runs)
    st.write("Balls:", balls)
    st.write("Strike Rate:", round((runs/balls)*100,2))
