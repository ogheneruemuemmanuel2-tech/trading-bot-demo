import time

from announcement_scanner import scanner_loop
from mexc_api import get_price
from strategy import detect_pump
from risk_manager import choose_risk
from listing_timer import extract_listing_time, start_countdown


# Demo trade storage
trade = {
    "active": False,
    "entry_price": 0,
    "amount": 0,
    "leverage": 0,
    "tp": 0,
    "sl": 0
}


def open_demo_short(symbol, price, risk):

    trade["active"] = True
    trade["entry_price"] = price
    trade["amount"] = risk["amount"]
    trade["leverage"] = risk["leverage"]

    trade["tp"] = price * (1 - (risk["tp"] / 100))
    trade["sl"] = price * 1.15

    print("\n🚨 DEMO SHORT OPENED")
    print("Symbol:", symbol)
    print("Entry Price:", price)
    print("Leverage:", trade["leverage"])
    print("Amount: $", trade["amount"])
    print("Take Profit:", trade["tp"])
    print("Stop Loss:", trade["sl"])


def track_trade(symbol):

    while trade["active"]:

        current_price = get_price(symbol)
        entry = trade["entry_price"]

        profit_percent = ((entry - current_price) / entry) * 100 * trade["leverage"]

        print("\n📊 TRADE TRACKER")
        print("Entry Price:", entry)
        print("Current Price:", current_price)
        print("Profit %:", round(profit_percent, 2))
        print("TP:", trade["tp"])
        print("SL:", trade["sl"])

        if current_price <= trade["tp"]:
            print("\n✅ TAKE PROFIT HIT")
            trade["active"] = False
            break

        if current_price >= trade["sl"]:
            print("\n❌ STOP LOSS HIT")
            trade["active"] = False
            break

        time.sleep(2)


def run_bot():

    print("🚀 LISTING SNIPER BOT STARTED")

    # Step 1: Scan MEXC announcements
    listing = scanner_loop()

    print("\n📢 New listing detected:")
    print(listing)

    # Step 2: Extract listing time
    listing_time = extract_listing_time(listing)

    if listing_time:
        start_countdown(listing_time)

    # Example symbol (later we will auto detect it)
    symbol = "NEWCOIN_USDT"

    risk = choose_risk("normal")

    print("\nWaiting for pump...")

    while True:

        price = get_price(symbol)

        print("Price:", price)

        # Example pump detection
        if price > 1.2:

            print("\n🔥 PUMP DETECTED")

            open_demo_short(symbol, price, risk)

            track_trade(symbol)

            break

        time.sleep(2)


run_bot()
