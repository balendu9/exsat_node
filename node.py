import os
import time
import requests
from dotenv import load_dotenv
from web3 import Web3
import json
import yaml
from apscheduler.schedulers.blocking import BlockingScheduler
import asyncio
import websockets
import sys
import aiohttp
import logging
from eth_account import Account
from eth_account.messages import encode_defunct

load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("NODE_MANAGER_CONTRACT")

w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)
wallet = account.address

with open("nodemanager_abi.json", "r") as abi_file:
    CONTRACT_ABI = json.load(abi_file)

contract = w3.eth.contract(address = CONTRACT_ADDRESS, abi = CONTRACT_ABI)

def setup_logger():
    logging.basicConfig(
        level= logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    return logging.getLogger("Oracle Node")

logger = setup_logger()

def is_registered_oracle():
    try:
        return contract.functions.registeredOracles(wallet).call()
    except Exception as e:
        print(f"[ERROR] Checking registration: {e}")
        return False
   
def get_minimum_stake():
    try:
        return contract.functions.MINIMUM_STAKE().call()
    except Exception as e:
        print(f"[ERROR] Getting minimum stake: {e}")
        return w3.to_wei(0.01, 'ether')  # Fallback

def register_as_oracle():
    try:
        stake = get_minimum_stake()
        nonce = w3.eth.get_transaction_count(wallet)
        txn = contract.functions.registerOracle().build_transaction({
            'from': wallet,
            'value': stake,
            'nonce': nonce,
            'gas': 300000,
            'gasPrice': w3.to_wei('20', 'gwei')
        })

        signed_txn = w3.eth.account.sign_transaction(txn, private_key = PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"[✅] Registered as oracle. TX: {tx_hash.hex()}")
        w3.eth.wait_for_transaction_receipt(tx_hash)
        return True
    except Exception as e:
        print(f"[ERROR] Registration failed: {e}")
        return False




async def fetch_price(session):
    url = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD&api_key=YOUR_API_KEY"
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                print(f"[DEBUG] Response data: {data}")
                if "USD" in data:
                    price = float(data["USD"])
                    return int(price)
                else:
                    print(f"[ERROR] 'USD' not found in response.")
                    return None
    except Exception as e:
        print(f"[ERROR] Failed to fetch price from DIA: {e}")
        return None


def current_timestamp():
    return int(time.time())


def sign_price(symbol, price):
    if not PRIVATE_KEY:
        raise Exception("Private key not found")
    
    timestamp = current_timestamp()
    message = f"{symbol}:{price}:{timestamp}"

    message_encoded = encode_defunct(text=message)
    message_hash = w3.keccak(message_encoded.body)
    signed = w3.eth.account.sign_message(message_encoded, private_key = PRIVATE_KEY)

    signer_address = Account.from_key(PRIVATE_KEY).address

    return {
        "symbol": symbol,
        "price": price,
        "timestamp": timestamp,
        "signature": signed.signature.hex(),
        "address": signer_address,
        "message_hash": message_hash.hex()
    }

async def send_data(node_id: str):
    print(f"[🔐] Wallet: {wallet}")
    if not is_registered_oracle():
        print("[🛠] Oracle not registered. Registering...")

        if not register_as_oracle():
            print("[❌] Could not register. Exiting.")
            return
    else:
        print("[✅] Oracle already registered.")

    print("[🔄] Starting oracle node...")

    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        print(f"[Connected] Node {node_id}")

        async with aiohttp.ClientSession() as session:
            while True:
                price = await fetch_price(session)
                signed_data = sign_price("BTCUSD", price)
                
                if price is not None:
                    await websocket.send(json.dumps(signed_data))
                    print(f"[SENT] {signed_data}")
                    logger.info(f"Signed data with address {signed_data['address']}")

                else:
                    print("[WARN] Skipping send due to fetch error")
                
                await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(send_data(wallet))
