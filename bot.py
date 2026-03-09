import time
from keep_alive import keep_alive
from mexc_api import get_futures_symbols, get_price
from strategy import check_momentum
from risk_manager import auto_leverage

keep_alive()

print("MEXC Futures Demo Bot Running")

known_symbols = []
price_history = {}
open_trades = {}

TAKE_PROFIT = 5
STOP_LOSS = -3

while True:

    try:

        symbols = get_futures_symbols()

        for s in symbols:

            symbol = s["symbol"]

            if symbol not in known_symbols:
                print("NEW COIN FOUND:", symbol)
                known_symbols.append(symbol)

            price = float(get_price(symbol))

            # TRACK OPEN TRADES
            if symbol in open_trades:

                entry = open_trades[symbol]["entry"]

                profit = (price - entry) / entry * 100

                print("TRADE UPDATE")
                print("Symbol:", symbol)
                print("Entry:", entry)
                print("Current:", price)
                print("Profit:", round(profit,2), "%")

                if profit >= TAKE_PROFIT:
                    print("TAKE PROFIT HIT")
                    del open_trades[symbol]

                elif profit <= STOP_LOSS:
                    print("STOP LOSS HIT")
                    del open_trades[symbol]

                continue

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
                print("Entry Price:", price)
                print("Change:", round(change,2), "%")
                print("Leverage:", leverage)
                print("DEMO TRADE OPENED")
                print("---------------")

                open_trades[symbol] = {
                    "entry": price,
                    "leverage": leverage
                }

        time.sleep(10)

    except Exception as e:

        print("ERROR:", e)
        time.sleep(10)
