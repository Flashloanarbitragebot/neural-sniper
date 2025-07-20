# 🧠 NeuralSniper: AI-Powered Flash Arbitrage Bot

NeuralSniper is an intelligent, adaptive DeFi trading bot that executes real-time flash loan arbitrage across multiple DEXs. It uses Aave for flash liquidity, Uniswap/Sushiswap for trades, and optional AI models to auto-tune strategy.

## 📦 Features
- Flash Loan via Aave
- Dual DEX Arbitrage (Uniswap V2, Sushiswap V1)
- Slippage + gas protection
- Real-time on-chain logging
- AI-ready off-chain bot (Python)
- Streamlit dashboard for control
- ML scaffold for strategy improvement

## 🚀 Quick Start
1. Deploy smart contract with Hardhat (`npx hardhat run scripts/deploy.js`)
2. Configure `.env` with keys
3. Run Python bot: `python3 scripts/neural_sniper.py`
4. Launch dashboard: `streamlit run dashboard/dashboard.py`
