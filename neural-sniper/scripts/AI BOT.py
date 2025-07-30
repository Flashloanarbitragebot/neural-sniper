import os, time, json
from dotenv import load_dotenv
from web3 import Web3
import pandas as pd

load_dotenv()

INFURA = os.getenv("https://mainnet.infura.io/v3/b25b95d1b4ae408cb2cbc684d8c67bb8")
PRIVATE_KEY = os.getenv("b25b95d1b4ae408cb2cbc684d8c67bb8")
WALLET = os.getenv("BOT_ADDRESS")
CONTRACT_ADDRESS = Web3.toChecksumAddress("0xYourContract")

web3 = Web3(Web3.HTTPProvider(INFURA))
assert web3.isConnected()

with open("FlashArbBot_ABI.json") as f:
    abi = json.load(f)

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

def fetch_prices():
    # Placeholder API call
    uniswap = 0.998
    sushiswap = 1.006
    spread = abs(sushiswap - uniswap)
    return spread, uniswap, sushiswap

def should_trade(spread, gas_cost_eth):
    return spread > 0.006 and gas_cost_eth < 0.005

def execute():
    nonce = web3.eth.get_transaction_count(WALLET)
    txn = contract.functions.executeArbOpportunity(
        Web3.toChecksumAddress("0xYourDAIAddress"),
        Web3.toWei(1000, 'ether')
    ).buildTransaction({
        "from": WALLET,
        "gas": 300000,
        "gasPrice": web3.eth.gas_price,
        "nonce": nonce
    })

    signed = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    print(f"Trade Executed: {web3.toHex(tx_hash)}")

while True:
    try:
        spread, u, s = fetch_prices()
        gas_eth = web3.eth.gas_price * 250000 / 1e18
        if should_trade(spread, gas_eth):
            execute()
        else:
            print(f"No trade | Spread: {spread:.4f} | Gas ETH: {gas_eth:.5f}")
        time.sleep(30)
    except Exception as e:
        print("Error:", e)
        time.sleep(60)

