from position_calls import get_active_positions, get_open_positions, query_existing_order
from calculations import get_trade_details
from ws_connect import ws_public

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

# Check order items
def check_order(ticker, order_id, remaining_capital, direction='Long'):

    # Get current orderbook
    orderbook = ws_public.fetch(f'orderBookL2_25.{ticker}')

    # Get latest price
    mid_price, _, _ = get_trade_details(orderbook)

    # Get trade details
    order_price, order_quantity, order_status = query_existing_order(ticker, order_id, direction)

    # Get open positions
    position_price, position_quantity = get_open_positions(ticker, direction)

    # Get active positions
    # active_order_price, active_order_quantity = get_active_positions(ticker)

    # Determine action - trade complete - stop placing orders
    if (position_quantity*position_price) >= remaining_capital and position_quantity > 0:
        print(style.MAGENTA)
        print(f'Position Quantity {ticker}: {position_quantity}')
        print(f'Remaining Capital {ticker}: {remaining_capital}')
        print(style.WHITE)
        
        return 'Trade Complete'

    # Determine action - position filled - buy more
    if order_status == 'Filled':
        return 'Position Filled'

    # Determine action - order active - do nothing
    active_items = ['Created', 'New']
    if order_status in active_items:
        return 'Order Active'

    # Determine action - partial filled order - do nothing
    if order_status == 'PartiallyFilled':
        return 'Partial Fill'

    # Determine action - order failed - try place order again
    cancel_items = ['Cancelled', 'Rejected', 'PendingCancel']
    if order_status in cancel_items:
        return 'Try Again'
