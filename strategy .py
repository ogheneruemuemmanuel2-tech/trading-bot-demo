price_history = {}

def check_momentum(symbol, price):
    
    if symbol not in price_history:
        price_history[symbol] = price
        return False

    old_price = price_history[symbol]

    change = (price - old_price) / old_price * 100

    price_history[symbol] = price

    if change > 2:
        return True

    return False
