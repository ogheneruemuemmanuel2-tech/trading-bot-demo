import time
from keep_alive import keep_alive
from mexc_api import get_futures_symbols, get_price
from strategy import check_momentum
from risk_manager import auto_leverage

keep_alive()

print("MEXC Futures Demo Bot Running")

known_symbols = []
price_history = {}

while True:

    try:

        symbols = get_futures_symbols()

        for s in symbols:

            symbol = s["symbol"]

            if symbol not in known_symbols:
                print("NEW COIN FOUND:", symbol)
                known_symbols.append(symbol)

            price = float(get_price(symbol))

            if symbol not in price_history:
                price_history[symbol] = price
                continue

            old_price = price_history[symbol]

            change = (price - old_price) / old_price * 100

            price_history[symbol] = price

            if check_momentum(symbol, price):

                leverage = auto_leverage(change)

                print("---------------")
                print("PUMP DETECTED")
                print("Symbol:", symbol)
                print("Price:", price)
                print("Change:", round(change,2), "%")
                print("Leverage:", leverage)
                print("DEMO TRADE OPENED")
                print("---------------")

        time.sleep(60)

    except Exception as e:

        print("ERROR:", e)
        time.sleep(60)
