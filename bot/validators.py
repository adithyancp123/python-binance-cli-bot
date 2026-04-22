"""
Input validation module for trading orders.
Ensures all CLI inputs meet Binance API requirements before submission.
"""
from typing import Optional

def validate_symbol(symbol: str) -> str:
    """Validate and format the trading pair symbol."""
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string.")
    return symbol.upper()

def validate_side(side: str) -> str:
    """Validate the order side (BUY or SELL)."""
    side = side.upper()
    if side not in ("BUY", "SELL"):
        raise ValueError("Side must be either BUY or SELL.")
    return side

def validate_order_type(order_type: str) -> str:
    """Validate the order type."""
    order_type = order_type.upper()
    # Adding STOP_LIMIT to supported types
    if order_type not in ("MARKET", "LIMIT", "STOP_LIMIT"):
        raise ValueError("Order type must be MARKET, LIMIT, or STOP_LIMIT.")
    return order_type

def validate_quantity(quantity: float) -> float:
    """Validate the order quantity."""
    if quantity <= 0:
        raise ValueError("Quantity must be a positive float.")
    return float(quantity)

def validate_price(price: Optional[float], order_type: str) -> float:
    """Validate the limit price based on the order type."""
    if order_type in ("LIMIT", "STOP_LIMIT"):
        if price is None or price <= 0:
            raise ValueError(f"Price is required and must be positive for {order_type} orders.")
        return float(price)
    return float(price) if price is not None else 0.0

def validate_stop_price(stop_price: Optional[float], order_type: str) -> float:
    """Validate the stop price for STOP_LIMIT orders."""
    if order_type == "STOP_LIMIT":
        if stop_price is None or stop_price <= 0:
            raise ValueError("Stop price is required and must be positive for STOP_LIMIT orders.")
        return float(stop_price)
    return float(stop_price) if stop_price is not None else 0.0
