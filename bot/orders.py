"""
Order execution module.
Handles placing different types of orders on Binance Futures.
"""
import logging
from typing import Dict, Any
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

logger = logging.getLogger("bot")

def _handle_order_exception(e: Exception, context: str) -> None:
    """Helper to log order exceptions consistently."""
    if isinstance(e, BinanceAPIException):
        logger.error(f"[{context}] Binance API Error {e.status_code}: {e.message}")
    elif isinstance(e, BinanceRequestException):
        logger.error(f"[{context}] Binance Request Error: {e.message}")
    else:
        logger.exception(f"[{context}] Unexpected execution error: {str(e)}")
    raise e

def place_market_order(client: Client, symbol: str, side: str, quantity: float) -> Dict[str, Any]:
    """Execute a MARKET order."""
    context = f"MARKET {side} | {symbol}"
    logger.info(f"Request: {context} | Qty: {quantity}")
    try:
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )
        logger.info(f"Success: {context} | Order ID: {response.get('orderId')} | Status: {response.get('status')}")
        return response
    except Exception as e:
        _handle_order_exception(e, context)
        return {}  # Should raise before this

def place_limit_order(client: Client, symbol: str, side: str, quantity: float, price: float) -> Dict[str, Any]:
    """Execute a LIMIT order."""
    context = f"LIMIT {side} | {symbol}"
    logger.info(f"Request: {context} | Qty: {quantity} | Price: {price}")
    try:
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=price,
            timeInForce="GTC"
        )
        logger.info(f"Success: {context} | Order ID: {response.get('orderId')} | Status: {response.get('status')}")
        return response
    except Exception as e:
        _handle_order_exception(e, context)
        return {}

def place_stop_limit_order(client: Client, symbol: str, side: str, quantity: float, price: float, stop_price: float) -> Dict[str, Any]:
    """Execute a STOP_LIMIT order."""
    context = f"STOP_LIMIT {side} | {symbol}"
    logger.info(f"Request: {context} | Qty: {quantity} | Price: {price} | Stop: {stop_price}")
    try:
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="STOP",
            quantity=quantity,
            price=price,
            stopPrice=stop_price,
            timeInForce="GTC"
        )
        logger.info(f"Success: {context} | Order ID: {response.get('orderId')} | Status: {response.get('status')}")
        return response
    except Exception as e:
        _handle_order_exception(e, context)
        return {}
