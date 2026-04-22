"""
Configuration module for the Binance Futures CLI Trading Bot.
Loads environment variables and sets up API keys and base URLs.
"""
import os
import shutil
from dotenv import load_dotenv

def check_and_setup_env() -> bool:
    """Check if .env exists, create if not. Return True if it was created."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    env_path = os.path.join(base_dir, ".env")
    example_path = os.path.join(base_dir, ".env.example")
    
    if not os.path.exists(env_path):
        if os.path.exists(example_path):
            shutil.copy(example_path, env_path)
            return True
    return False

# Initial check and load
load_dotenv()

BINANCE_API_KEY: str = os.getenv("BINANCE_API_KEY", "")
BINANCE_API_SECRET: str = os.getenv("BINANCE_API_SECRET", "")
BINANCE_TESTNET: bool = os.getenv("BINANCE_TESTNET", "True").lower() in ("true", "1", "t", "yes")

BASE_URL: str = "https://testnet.binancefuture.com" if BINANCE_TESTNET else "https://fapi.binance.com"
