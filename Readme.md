# Decentralized Oracle Node Setup Guide

## Overview

Welcome to the official **Oracle Node** guide for the **Orion Decentralized Oracle Network** on the **exSat Network**. This node fetches real-time **BTC/USD** prices, cryptographically signs the data, and sends it to the network via WebSocket, enabling secure data feeds for exSat-based DeFi applications.

This guide walks you through setting up and running your own **Oracle Node** locally to join the network.

## Features

- Fetches live **BTC/USD** price from CryptoCompare.
- Cryptographically signs the data for authenticity.
- Sends signed data to the Orion Network WebSocket endpoint.
- Auto-registers as an oracle if not already registered.

## Prerequisites

Before getting started, ensure you have the following installed:

- **Python 3.9+**
- **Node.js** (optional, for managing WebSocket server locally)
- **pip** (Python package manager)
- An **exSat-compatible wallet** (e.g., a Bitcoin wallet supporting exSat transactions)
- A **CryptoCompare API key** ([sign up here](https://www.cryptocompare.com/))

## Setup Instructions

### Step 1: Clone the Repository

Clone the Oracle Node repository and navigate to the project directory:

```bash
git clone https://github.com/your-username/oracle-node.git
cd oracle-node
```

*Update the repository URL with your actual GitHub link.*

### Step 2: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Step 3: Add Environment Variables

Rename the `.env.example` file to `.env` and add your private key:

```env
PRIVATE_KEY=your_private_key_here
```

Other configuration data is pre-set in the `.env` file.

⚠️ **Warning**: Never share your private key. Keep the `.env` file private and secure.

### Step 4: Prepare Required Files

Ensure the following file is in the project directory:

- **`nodemanager_abi.json`**: Contains the ABI of the **NodeManager** contract. This file is included in the repository.

## Run the Oracle Node

Once setup is complete, run the node:

```bash
python3 node.py
```

The node will automatically:

1. Check if your wallet is a registered oracle.
2. Register as an oracle if necessary (requires staking).
3. Start fetching, signing, and broadcasting **BTC/USD** price data to the WebSocket endpoint.

## Configuration Notes

- **Stake Amount**: Automatically retrieved from the **NodeManager** contract’s `MINIMUM_STAKE()` function.
- **Transaction Fees**: Defaults to a standard fee for exSat transactions. Adjust in the `node.py` code if needed.
- **Symbol Used**: Currently hardcoded to **BTCUSD**. Modify the `sign_price()` function in `node.py` to support other symbols.

## Troubleshooting

- **WebSocket Connection Issues**: Ensure the WebSocket endpoint URL in `node.py` is correct and accessible.
- **Insufficient Stake**: Verify your wallet has enough BTC to meet the minimum stake requirement.
- **API Key Errors**: Confirm your CryptoCompare API key is valid and correctly set in the `.env` file.
