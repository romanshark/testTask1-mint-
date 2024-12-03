# Spotlight Minter Library

This library automates the process of minting a badge and interacting with the Spotlight Protocol app using Selenium and Web3.

## Installation

Install the necessary dependencies using pip:

```bash
pip install selenium web3 python-dotenv

Usage
Import the library in your script.
Set up your environment variables in a .env file.
Call the necessary functions for minting badges.
Example usage:

python
Copy code
from spotlight_minter import connect_wallet_and_twitter, mint_spotlight, mint_badge_on_blockchain

# Set up WebDriver (headless Chrome)
driver = setup_chrome_driver()

# Connect wallet and Twitter
connect_wallet_and_twitter(driver)

# Mint a spotlight
mint_spotlight(driver)
