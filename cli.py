"""
Command Line Interface entry point.
Built with Typer and Rich for a premium terminal UX.
"""
import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

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
    """Print a clean startup banner."""
    banner_text = "[bold cyan]Binance Futures CLI Bot[/bold cyan]\n[dim]Production-Grade Execution Engine[/dim]"
    console.print(Panel(banner_text, expand=False, border_style="cyan"))

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
        # Validation Pipeline
        symbol_val = validate_symbol(symbol)
        side_val = validate_side(side)
        type_val = validate_order_type(type)
        quantity_val = validate_quantity(quantity)
        price_val = validate_price(price, type_val)
        stop_price_val = validate_stop_price(stop_price, type_val)

        # Display Request Summary
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

        # Execution
        client = get_client()

        with console.status("[bold green]Executing order...", spinner="dots"):
            if type_val == "MARKET":
                response = place_market_order(client, symbol_val, side_val, quantity_val)
            elif type_val == "LIMIT":
                response = place_limit_order(client, symbol_val, side_val, quantity_val, price_val)
            elif type_val == "STOP_LIMIT":
                response = place_stop_limit_order(client, symbol_val, side_val, quantity_val, price_val, stop_price_val)

        # Display Response
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
        logger.warning(f"Validation Error: {ve}")
        console.print(f"\n[bold red][ERROR] Validation Error:[/bold red] {ve}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"\n[bold red][ERROR] Execution Error:[/bold red] {e}")
        console.print("[dim]Check logs/trading.log for full traceback.[/dim]")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
