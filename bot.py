import time
from multi_exchange_scanner import scanner_loop
from mexc_api import get_price
from strategy import detect_top
from risk_manager import choose_risk, analyze_coin_strength
from token_analyzer import analyze_dump_risk
from telegram_bot import send_message
from listing_timer import extract_listing_time, start_countdown

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
Entry Price: {price}
Leverage: {trade['leverage']}x
Amount: ${trade['amount']}

Take Profit: {trade['tp']}
Stop Loss: {trade['sl']}
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

    print("🚀 BOT STARTED")
    send_message("🤖 LISTING BOT STARTED")

    exchange, symbol = scanner_loop()

    send_message(
        f"""
🚀 NEW LISTING DETECTED

Exchange: {exchange}
Coin: {symbol}
"""
    )

    level = analyze_coin_strength(symbol)
    dump_risk = analyze_dump_risk(symbol)

    risk = choose_risk(level)

    send_message(
        f"""
Coin Strength: {level}
Dump Risk: {dump_risk}

Trade Amount: ${risk['amount']}
Leverage: {risk['leverage']}x
"""
    )

    listing_time = extract_listing_time(symbol)

    if listing_time:
        start_countdown(listing_time)

    print("👀 Watching for pump top...")

    while True:

        if detect_top(symbol):

            price = get_price(symbol)

            send_message("🔥 TOP DETECTED — OPENING SHORT")

            open_demo_short(symbol, price, risk)

            track_trade(symbol)

            break

        time.sleep(0.5)


run_bot()
