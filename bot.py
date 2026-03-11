import time

from announcement_scanner import scanner_loop
from mexc_api import get_price
from strategy import detect_top
from risk_manager import choose_risk, analyze_coin_strength
from listing_timer import extract_listing_time, start_countdown
from telegram_bot import send_message


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

    message = f"""
🚨 DEMO SHORT OPENED

Coin: {symbol}
Entry: {price}
Leverage: {trade['leverage']}x
Amount: ${trade['amount']}
TP: {trade['tp']}
SL: {trade['sl']}
"""

    print(message)
    send_message(message)


def track_trade(symbol):

    while trade["active"]:

        current_price = get_price(symbol)

        entry = trade["entry_price"]

        profit_percent = ((entry - current_price) / entry) * 100 * trade["leverage"]

        print("Profit:", round(profit_percent, 2), "%")

        if current_price <= trade["tp"]:

            send_message("✅ TAKE PROFIT HIT")
            trade["active"] = False
            break

        if current_price >= trade["sl"]:

            send_message("❌ STOP LOSS HIT")
            trade["active"] = False
            break

        time.sleep(1)


def run_bot():

    send_message("🤖 LISTING BOT STARTED")

    listing, symbol = scanner_loop()

    send_message(f"🚀 NEW LISTING DETECTED\n{symbol}")

    level = analyze_coin_strength(listing)

    risk = choose_risk(level)

    send_message(f"""
Coin strength: {level}
Trade amount: ${risk['amount']}
Leverage: {risk['leverage']}x
""")

    listing_time = extract_listing_time(listing)

    if listing_time:
        start_countdown(listing_time)

    while True:

        if detect_top(symbol):

            price = get_price(symbol)

            send_message("🔥 TOP DETECTED")

            open_demo_short(symbol, price, risk)

            track_trade(symbol)

            break

        time.sleep(0.5)


run_bot()
