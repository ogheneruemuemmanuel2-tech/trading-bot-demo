import time
from mexc_api import get_price

price_history = []

def detect_pump(symbol):

    global price_history

    price = get_price(symbol)

    price_history.append(price)

    # keep only last 10 prices
    if len(price_history) > 10:
        price_history.pop(0)

    if len(price_history) < 10:
        return False

    first_price = price_history[0]
    last_price = price_history[-1]

    pump_percent = ((last_price - first_price) / first_price) * 100

    print("Pump check:", round(pump_percent,2), "%")

    # if price pumped 25% in few seconds
    if pump_percent > 25:
        return True

    return False
