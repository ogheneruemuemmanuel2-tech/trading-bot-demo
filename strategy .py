def check_momentum(symbol, price):

    if not hasattr(check_momentum, "history"):
        check_momentum.history = {}

    if symbol not in check_momentum.history:
        check_momentum.history[symbol] = price
        return False

    old_price = check_momentum.history[symbol]

    change = (price - old_price) / old_price * 100

    check_momentum.history[symbol] = price

    if change > 2:
        return True

    return False
