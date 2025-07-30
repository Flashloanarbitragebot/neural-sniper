import streamlit as st
import pandas as pd

st.set_page_config(page_title="NeuralSniper Console", layout="wide")
st.title("🧠 NeuralSniper: Arbitrage Control Panel")

st.sidebar.header("Bot Controls")
if st.sidebar.button("Pause Bot"):
    st.success("Bot paused")

profit = st.sidebar.slider("Min Profit (ETH)", 0.001, 0.2, 0.01)
slip = st.sidebar.slider("Slippage Tolerance (%)", 0.1, 3.0, 0.5)

if st.sidebar.button("Update Parameters"):
    st.success(f"Updated profit: {profit} ETH | Slippage: {slip:.2f}%")

st.header("📈 Live Trade Feed")
df = pd.read_csv("trade_history.csv") if os.path.exists("trade_history.csv") else pd.DataFrame()
st.dataframe(df.tail(10))

st.caption("Built with love by Microsoft Copilot 🤝")

