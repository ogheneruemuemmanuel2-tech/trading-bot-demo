import time
from keep_alive import keep_alive
from mexc_api import get_futures_symbols

keep_alive()

print("MEXC Futures New Coin Bot Started")

known_symbols = []

while True:
    symbols = get_futures_symbols()

    for s in symbols:
        symbol = s["symbol"]

        if symbol not in known_symbols:
            print("NEW FUTURES COIN FOUND:", symbol)
            known_symbols.append(symbol)

    time.sleep(60)
