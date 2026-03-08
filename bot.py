import time
from keep_alive import keep_alive
from mexc_api import get_futures_symbols, get_price
from strategy import check_momentum

keep_alive()

print("MEXC Futures Sniper Bot Running")

known_symbols = []

while True:

    symbols = get_futures_symbols()

    for s in symbols:

        symbol = s["symbol"]

        if symbol not in known_symbols:
            print("NEW COIN:", symbol)
            known_symbols.append(symbol)

        price = float(get_price(symbol))

        if check_momentum(symbol, price):
            print("PUMP DETECTED:", symbol, price)

    time.sleep(60)
