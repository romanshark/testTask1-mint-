# spotlight_minter/spotlight_minter.py

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from web3 import Web3
from dotenv import load_dotenv
from selenium.webdriver.common.action_chains import ActionChains

# Load environment variables
load_dotenv()

# Configuration variables
RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")

# Web3 Setup
web3 = Web3(Web3.HTTPProvider(RPC_URL))
if not web3.is_connected():
    raise Exception("Failed to connect to blockchain node.")

# ChromeDriver Setup
chrome_options = Options()
chrome_options.add_argument("--headless")  # Running in headless mode
service = Service("./chromedriver.exe")  # ChromeDriver executable path

driver = webdriver.Chrome(service=service, options=chrome_options)

def connect_wallet_and_twitter(driver):
    """Connect the wallet and Twitter to the Spotlight app."""
    driver.get("https://app.spotlightprotocol.com/authenticate")
    time.sleep(2)

    # Connect wallet
    connect_wallet_btn = driver.find_element(
        By.XPATH, "//p[text()='Connect Wallet']/following-sibling::button"
    )
    connect_wallet_btn.click()
    time.sleep(2)

    # Connect Twitter
    connect_twitter_btn = driver.find_element(
        By.XPATH, "//p[text()='Connect X (Twitter)']/following-sibling::button"
    )

    if not connect_twitter_btn.get_attribute("disabled"):
        driver.execute_script("arguments[0].scrollIntoView(true);", connect_twitter_btn)
        connect_twitter_btn.click()
        time.sleep(2)

        twitter_username_field = driver.find_element(By.NAME, "text")
        twitter_username_field.send_keys(TWITTER_USERNAME)
        twitter_username_field.send_keys(Keys.RETURN)
        time.sleep(2)

        twitter_password_field = driver.find_element(By.NAME, "password")
        twitter_password_field.send_keys(TWITTER_PASSWORD)
        twitter_password_field.send_keys(Keys.RETURN)
        time.sleep(5)

        print("Connected to Twitter")
    else:
        print("Connect Twitter button is disabled. Skipping...")

def mint_spotlight(driver):
    """Initiate the process to mint a Spotlight badge."""
    driver.get("https://app.spotlightprotocol.com/badge")
    time.sleep(2)

    try:
        mint_spotlight_link = driver.find_element(
            By.XPATH, "//p[text()='Mint a Spotlight']/following-sibling::a[contains(@class, 'chakra-button')]"
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", mint_spotlight_link)
        mint_spotlight_link.click()
        time.sleep(2)
        print("Mint a Spotlight action initiated.")
    except Exception as e:
        print(f"Error while trying to mint a Spotlight: {e}")

def join_spotlight(driver):
    """Join a Spotlight by clicking a random available circle."""
    driver.get("https://app.spotlightprotocol.com/explore")
    time.sleep(2)

    spotlight_circles = driver.find_elements(By.XPATH, "//button[contains(text(), 'Mint Now')]")
    if spotlight_circles:
        spotlight_circles[0].click()
        time.sleep(2)

    print("Joined a Spotlight.")

def mint_badge(driver):
    """Claim a badge in Spotlight."""
    driver.get("https://app.spotlightprotocol.com/badge")
    time.sleep(2)

    claim_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Claim this Badge')]")
    claim_btn.click()
    time.sleep(5)

    print("Badge claimed.")

def mint_badge_on_blockchain(private_key, rpc_url, contract_address, abi):
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        raise Exception("Failed to connect to blockchain node.")

    contract = web3.eth.contract(address=contract_address, abi=abi)

    gas_price = web3.eth.gas_price
    transaction = contract.functions.mintBadge().buildTransaction({
        'chainId': 1234, 
        'gas': contract.functions.mintBadge().estimateGas({'from': web3.eth.default_account}),
        'gasPrice': gas_price,
        'nonce': web3.eth.getTransactionCount(web3.eth.default_account),
    })

    signed_transaction = web3.eth.account.signTransaction(transaction, private_key)

    tx_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    print(f"Transaction Hash: {tx_hash.hex()}")