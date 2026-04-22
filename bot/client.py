"""
Binance API client initialization.
Handles authentication and connection setup.
"""
import logging
from binance.client import Client
from bot.config import BINANCE_API_KEY, BINANCE_API_SECRET, BINANCE_TESTNET

logger = logging.getLogger("bot")

def get_client() -> Client:
    """
    Initialize and return the Binance Futures Client.
    
    Raises:
        ValueError: If API keys are missing.
        Exception: If initialization fails.
    """
    if not BINANCE_API_KEY or not BINANCE_API_SECRET or "your_testnet_api_key_here" in BINANCE_API_KEY:
        logger.error("Authentication failed: API keys not found or default template values detected.")
        raise ValueError("MissingCredentials")
        
    try:
        client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=BINANCE_TESTNET)
        logger.info(f"Initialized Binance Futures Client (Testnet: {BINANCE_TESTNET})")
        return client
    except Exception as e:
        logger.exception("Failed to initialize Binance Client.")
        raise
