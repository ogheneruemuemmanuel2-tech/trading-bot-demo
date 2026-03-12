import time
from mexc_api import get_price

price_history = []


def detect_top(symbol):

    global price_history

    price = get_price(symbol)

    price_history.append(price)

    # keep only last 20 prices
    if len(price_history) > 20:
        price_history.pop(0)

    if len(price_history) < 6:
        return False

    p1 = price_history[-6]
    p2 = price_history[-5]
    p3 = price_history[-4]
    p4 = price_history[-3]
    p5 = price_history[-2]
    p6 = price_history[-1]

    # detect strong pump then slowdown
    pump = (p4 - p1) / p1 * 100

    # detect top rejection
    if pump > 20 and p6 < p5:

        print("⚠️ Possible TOP detected")

        return True

    return False
