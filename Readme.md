🧠 Decentralized Oracle Node
Welcome to the official Oracle Node of our Decentralized Oracle Network. This node fetches real-time BTC/USD prices, signs the data cryptographically, and sends it to the network via WebSocket.

🛠 This guide will walk you through setting up and running your own Oracle Node locally to join the network.

📦 Features
Fetches live BTC/USD price from CryptoCompare

Cryptographically signs the data

Sends it to the Oracle Network WebSocket endpoint

Auto-registers as an oracle if not already registered

🧰 Prerequisites
Before getting started, make sure you have the following installed:

Python 3.9+

Node.js (optional, for managing WebSocket server locally)

pip (Python package manager)

An Ethereum wallet (Metamask or similar)

CryptoCompare API key

🔧 Setup Instructions
1. Clone the Repository

git clone https://github.com/your-username/oracle-node.git
cd oracle-node


2. Install Dependencies

pip install -r requirements.txt


3. Add Environment Variables
Rename the .env.example to .env and just add your private key 

PRIVATE_KEY=your_private_key_here


(other data is already setup for you.)
⚠️ Never share your private key. This file must remain private and secure.

📁 Required Files

nodemanager_abi.json
This should contain the ABI of your NodeManager contract. Place it in the same directory as the script. This is already provided in the repository.

🚀 Run the Oracle Node
Once everything is set up:

python3 node.py
The node will automatically:

Check if your wallet is a registered oracle.

Register if necessary (staking required).

Start fetching, signing, and broadcasting price data to the WebSocket endpoint.

⚙️ Configuration Notes
Stake Amount: Pulled automatically from the smart contract (MINIMUM_STAKE()).

Gas Price: Defaults to 20 gwei. Adjust in code if needed.

Symbol Used: BTCUSD is currently hardcoded. Change it in sign_price() if needed.

