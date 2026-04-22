"""
Configuration module for the Binance Futures CLI Trading Bot.
Loads environment variables and sets up API keys and base URLs.
"""
import os
from dotenv import load_dotenv

load_dotenv()

BINANCE_API_KEY: str = os.getenv("BINANCE_API_KEY", "")
BINANCE_API_SECRET: str = os.getenv("BINANCE_API_SECRET", "")
BINANCE_TESTNET: bool = os.getenv("BINANCE_TESTNET", "True").lower() in ("true", "1", "t", "yes")

BASE_URL: str = "https://testnet.binancefuture.com" if BINANCE_TESTNET else "https://fapi.binance.com"
