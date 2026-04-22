"""
Command Line Interface entry point.
Built with Typer and Rich for a premium terminal UX.
"""
import os
import sys
import time
import socket
import random
import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from bot.config import check_and_setup_env, BINANCE_API_KEY, BINANCE_API_SECRET
from bot.logging_config import setup_logging
from bot.validators import (
    validate_symbol, validate_side, validate_order_type,
    validate_quantity, validate_price, validate_stop_price
)
from bot.client import get_client
from bot.orders import place_market_order, place_limit_order, place_stop_limit_order

app = typer.Typer(
    help="[PRO] Professional Binance Futures Testnet Trading Bot",
    add_completion=False,
    no_args_is_help=True
)
console = Console()
logger = setup_logging()

@app.callback()
def main():
    """Binance Futures Trading Bot"""
    pass

def print_banner():
    """Print a clean startup banner and handle first-run environment setup."""
    banner_text = "[bold cyan]Binance Futures CLI Bot[/bold cyan]\n[dim]Production-Grade Execution Engine[/dim]"
    console.print(Panel(banner_text, expand=False, border_style="cyan"))
    
    if check_and_setup_env():
        console.print("\n[bold yellow][*] Created .env template.[/bold yellow] Please paste your Binance Testnet keys in the file.\n")

def handle_missing_credentials():
    """Display premium error UX for missing credentials."""
    error_msg = (
        "[bold red]Configuration Required[/bold red]\n"
        "Missing Binance API credentials.\n\n"
        "[bold cyan]Next steps:[/bold cyan]\n"
        "1. Open [yellow].env[/yellow] file in the project root\n"
        "2. Add your [green]BINANCE_API_KEY[/green]\n"
        "3. Add your [green]BINANCE_API_SECRET[/green]\n"
        "4. Re-run your command\n\n"
        "[dim]If you don't have keys yet, run `python cli.py demo` to test locally.[/dim]"
    )
    console.print(Panel(error_msg, title="[ACTION REQUIRED]", border_style="red", expand=False))
    raise typer.Exit(code=1)

@app.command(help="Run system diagnostics.")
def doctor():
    """Check environment readiness."""
    print_banner()
    
    doc_table = Table(title="System Diagnostics", show_header=True, header_style="bold magenta", box=box.SIMPLE)
    doc_table.add_column("Check", style="cyan")
    doc_table.add_column("Status", style="bold white")
    doc_table.add_column("Details", style="dim")
    
    # Python Version
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    doc_table.add_row("Python Version", "[SUCCESS] OK", py_version)
    
    # Dependencies
    try:
        import binance
        import dotenv
        doc_table.add_row("Dependencies", "[SUCCESS] OK", "Binance, Typer, Rich installed")
    except ImportError:
        doc_table.add_row("Dependencies", "[ERROR] Missing", "Run pip install -r requirements.txt")
        
    # .env exists
    env_exists = os.path.exists(".env")
    doc_table.add_row(".env File", "[SUCCESS] OK" if env_exists else "[ERROR] Missing", "Configuration file")
    
    # Keys present
    keys_present = bool(BINANCE_API_KEY and BINANCE_API_SECRET and "your_testnet_api_key_here" not in BINANCE_API_KEY)
    doc_table.add_row("API Keys", "[SUCCESS] Configured" if keys_present else "[ERROR] Missing", "Required for trading")
    
    # Logs folder
    logs_exist = os.path.exists("logs")
    doc_table.add_row("Logs Directory", "[SUCCESS] OK" if logs_exist else "[WARNING] Missing", "Telemetry storage")
    
    # Internet Connectivity
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=3)
        doc_table.add_row("Internet", "[SUCCESS] OK", "Connected")
    except OSError:
        doc_table.add_row("Internet", "[ERROR] Failed", "No connection")
        
    console.print(doc_table)
    
    if keys_present and env_exists:
        console.print("\n[bold green][PRO] Ready for trading = YES[/bold green]")
    else:
        console.print("\n[bold red][WARNING] Ready for trading = NO[/bold red] (Please configure API keys)")

@app.command(help="Run in demo mode without API keys.")
def demo(
    symbol: str = typer.Option("BTCUSDT", "--symbol", "-s", help="Trading pair"),
    side: str = typer.Option("BUY", "--side", "-d", help="Direction: BUY or SELL"),
    type: str = typer.Option("MARKET", "--type", "-t", help="Order type: MARKET, LIMIT, or STOP_LIMIT"),
    quantity: float = typer.Option(0.001, "--quantity", "-q", help="Order quantity"),
    price: Optional[float] = typer.Option(None, "--price", "-p", help="Order price"),
    stop_price: Optional[float] = typer.Option(None, "--stop-price", "-sp", help="Stop trigger price")
):
    """Simulate order execution realistically without API keys."""
    print_banner()
    console.print("[bold yellow][DEMO] Running in DEMO MODE (No API calls will be made)[/bold yellow]\n")
    
    try:
        symbol_val = validate_symbol(symbol)
        side_val = validate_side(side)
        type_val = validate_order_type(type)
        quantity_val = validate_quantity(quantity)
        price_val = validate_price(price, type_val)
        stop_price_val = validate_stop_price(stop_price, type_val)
        
        req_table = Table(title="Simulated Order Request", show_header=False, box=box.SIMPLE)
        req_table.add_column("Property", style="cyan")
        req_table.add_column("Value", style="bold white")
        
        req_table.add_row("Symbol", symbol_val)
        req_table.add_row("Side", side_val)
        req_table.add_row("Type", type_val)
        req_table.add_row("Quantity", str(quantity_val))
        if type_val in ("LIMIT", "STOP_LIMIT"):
            req_table.add_row("Price", str(price_val))
        if type_val == "STOP_LIMIT":
            req_table.add_row("Stop Price", str(stop_price_val))
            
        console.print(req_table)
        
        with console.status("[bold green]Simulating Binance network latency...", spinner="dots"):
            time.sleep(1.5)
            
        console.print("\n[bold green][SUCCESS] Simulated Order Successfully Placed![/bold green]")
        
        res_table = Table(title="Simulated Response Details", show_header=False, box=box.MINIMAL_DOUBLE_HEAD)
        res_table.add_column("Key", style="yellow")
        res_table.add_column("Value", style="bold white")
        
        mock_order_id = random.randint(1000000000, 9999999999)
        res_table.add_row("Order ID", str(mock_order_id))
        res_table.add_row("Status", "NEW")
        res_table.add_row("Executed Qty", "0.0")
        if type_val == "MARKET":
            res_table.add_row("Avg Price", "MockExecutionPrice")
            
        console.print(res_table)
        
    except ValueError as ve:
        console.print(f"\n[bold red][ERROR] Validation Error:[/bold red] {ve}")
        raise typer.Exit(code=1)

@app.command(help="Place a new order on the Binance Futures Testnet.")
def order(
    symbol: str = typer.Option(..., "--symbol", "-s", help="Trading pair (e.g., BTCUSDT)"),
    side: str = typer.Option(..., "--side", "-d", help="Direction: BUY or SELL"),
    type: str = typer.Option(..., "--type", "-t", help="Order type: MARKET, LIMIT, or STOP_LIMIT"),
    quantity: float = typer.Option(..., "--quantity", "-q", help="Order quantity in base asset"),
    price: Optional[float] = typer.Option(None, "--price", "-p", help="Order price (Required for LIMIT/STOP_LIMIT)"),
    stop_price: Optional[float] = typer.Option(None, "--stop-price", "-sp", help="Stop trigger price (Required for STOP_LIMIT)")
):
    """
    Execute a trade on Binance Futures.

    Examples:
      Market Buy:  python cli.py order -s BTCUSDT -d BUY -t MARKET -q 0.001
      Limit Sell:  python cli.py order -s BTCUSDT -d SELL -t LIMIT -q 0.001 -p 120000
      Stop Limit:  python cli.py order -s ETHUSDT -d BUY -t STOP_LIMIT -q 0.05 -p 3500 -sp 3550
    """
    print_banner()
    
    try:
        symbol_val = validate_symbol(symbol)
        side_val = validate_side(side)
        type_val = validate_order_type(type)
        quantity_val = validate_quantity(quantity)
        price_val = validate_price(price, type_val)
        stop_price_val = validate_stop_price(stop_price, type_val)

        req_table = Table(title="Order Request Summary", show_header=False, box=box.SIMPLE)
        req_table.add_column("Property", style="cyan")
        req_table.add_column("Value", style="bold white")
        
        req_table.add_row("Symbol", symbol_val)
        req_table.add_row("Side", side_val)
        req_table.add_row("Type", type_val)
        req_table.add_row("Quantity", str(quantity_val))
        if type_val in ("LIMIT", "STOP_LIMIT"):
            req_table.add_row("Price", str(price_val))
        if type_val == "STOP_LIMIT":
            req_table.add_row("Stop Price", str(stop_price_val))
            
        console.print(req_table)
        console.print("[dim]Connecting to Binance Testnet...[/dim]")

        # Check credentials and connect
        client = get_client()

        with console.status("[bold green]Executing order...", spinner="dots"):
            if type_val == "MARKET":
                response = place_market_order(client, symbol_val, side_val, quantity_val)
            elif type_val == "LIMIT":
                response = place_limit_order(client, symbol_val, side_val, quantity_val, price_val)
            elif type_val == "STOP_LIMIT":
                response = place_stop_limit_order(client, symbol_val, side_val, quantity_val, price_val, stop_price_val)

        console.print("\n[bold green][SUCCESS] Order Successfully Placed![/bold green]")
        
        res_table = Table(title="Order Response Details", show_header=False, box=box.MINIMAL_DOUBLE_HEAD)
        res_table.add_column("Key", style="yellow")
        res_table.add_column("Value", style="bold white")
        
        res_table.add_row("Order ID", str(response.get('orderId')))
        res_table.add_row("Status", str(response.get('status')))
        res_table.add_row("Executed Qty", str(response.get('executedQty', '0')))
        
        if response.get('avgPrice') and float(response.get('avgPrice', 0)) > 0:
            res_table.add_row("Avg Price", str(response.get('avgPrice')))
            
        console.print(res_table)
        console.print("[dim]View full details in logs/trading.log[/dim]")
        
    except ValueError as ve:
        if str(ve) == "MissingCredentials":
            handle_missing_credentials()
        else:
            logger.warning(f"Validation Error: {ve}")
            console.print(f"\n[bold red][ERROR] Validation Error:[/bold red] {ve}")
            raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"\n[bold red][ERROR] Execution Error:[/bold red] {e}")
        console.print("[dim]Check logs/trading.log for full traceback.[/dim]")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
