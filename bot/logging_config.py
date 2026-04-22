"""
Logging configuration module.
Sets up rotating file logs and console output for the trading bot.
"""
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging() -> logging.Logger:
    """
    Configure and return the main logger for the application.
    Logs are saved to logs/trading.log with a professional format.
    """
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, "trading.log")
    
    # Professional log format: [TIMESTAMP] [LEVEL] [LOGGER] - MESSAGE
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10*1024*1024, backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # Optional console handler for debug purposes, but CLI handles UX separately.
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.WARNING)
    
    logger = logging.getLogger("bot")
    logger.setLevel(logging.INFO)
    
    # Prevent adding handlers multiple times
    if not logger.handlers:
        logger.addHandler(file_handler)
    
    return logger
