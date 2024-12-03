from spotlight_minter import connect_wallet_and_twitter, mint_spotlight, join_spotlight, mint_badge, mint_badge_on_blockchain
from selenium import webdriver
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Chrome driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

# Get environment variables
RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")  # replace with actual contract address
ABI = os.getenv("CONTRACT_ABI")  # load ABI (can be from file or env)

try:
    # Call the functions
    connect_wallet_and_twitter(driver)
    mint_spotlight(driver)
    join_spotlight(driver)
    mint_badge(driver)
    
    # Blockchain interaction
    #mint_badge_on_blockchain(PRIVATE_KEY, RPC_URL, CONTRACT_ADDRESS, ABI)
finally:
    driver.quit()
