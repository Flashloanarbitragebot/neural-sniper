import time
import json
import os
import pandas as pd
from dotenv import load_dotenv
from web3 import Web3

# Load environment variables
load_dotenv()
INFURA_URL = os.getenv("https://mainnet.infura.io/v3/b25b95d1b4ae408cb2cbc684d8c67bb8")
PRIVATE_KEY = os.getenv("b25b95d1b4ae408cb2cbc684d8c67bb8")
BOT_ADDRESS = Web3.toChecksumAddress(os.getenv("0x64a45F49d115c885C5995Ca2aC14df2dA3815E91"))
CONTRACT_ADDRESS = Web3.toChecksumAddress("0xYourDeployedContract")

# Connect to Web3
web3 = Web3(Web3.HTTPProvider(INFURA_URL))
assert web3.isConnected(), "Web3 connection failed"

# Load ABI
with open("FlashArbBot_ABI.json") as f:
    abi = json.load(f)

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

# Placeholder: Fetch DEX price spreads from external APIs
def fetch_price_spread():
    # Simulated prices for DAI on Uniswap and Sushiswap
    uni_price = 0.998
    sushi_price = 1.007
    spread = abs(sushi_price - uni_price)
    return spread, uni_price, sushi_price

# Profitability decision logic (can be replaced with ML)
def should_trade(spread, gas_cost_eth):
    threshold_spread = 0.006
    max_gas_cost = 0.005
    return spread > threshold_spread and gas_cost_eth < max_gas_cost

# Execute arbitrage via smart contract
def execute_arbitrage():
    try:
        nonce = web3.eth.get_transaction_count(BOT_ADDRESS)
        txn = contract.functions.executeArbOpportunity(
            Web3.toChecksumAddress("0xDAITokenAddress"),  # replace with real DAI address
            Web3.toWei(1000, "ether")                     # trade size
        ).buildTransaction({
            'from': BOT_ADDRESS,
            'gas': 300000,
            'gasPrice': web3.eth.gas_price,
            'nonce': nonce
        })

        signed_txn = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"✅ Trade executed: {web3.toHex(tx_hash)}")
    except Exception as e:
        print(f"❌ Execution failed: {e}")

# Main loop
while True:
    try:
        spread, uni_price, sushi_price = fetch_price_spread()
        gas_gwei = web3.eth.gas_price / 1e9
        estimated_gas_cost_eth = gas_gwei * 250000 / 1e9

        print(f"📊 Spread: {spread:.5f} | Gas (ETH): {estimated_gas_cost_eth:.5f}")

        if should_trade(spread, estimated_gas_cost_eth):
            execute_arbitrage()
        else:
            print("⏸️ Conditions not ideal, skipping trade.")

        time.sleep(30)  # Wait before next check
    except Exception as error:
        print(f"⚠️ Error: {error}")
        time.sleep(60)
