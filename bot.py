import time
from token_analyzer import analyze_dump_risk
from multi_exchange_scanner import scanner_loop
from mexc_api import get_price
from strategy import detect_top
from risk_manager import choose_risk, analyze_coin_strength
from telegram_bot import send_message
print("BOT STARTED SUCCESSFULLY")

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

    msg = f"""
🚨 DEMO SHORT OPENED

Coin: {symbol}
Entry: {price}
Leverage: {trade['leverage']}x
Amount: ${trade['amount']}
"""

    print(msg)

    send_message(msg)


def run_bot():

    send_message("🤖 LISTING BOT STARTED")

    exchange, symbol = scanner_loop()

    send_message(f"""
🚀 NEW LISTING DETECTED

Exchange: {exchange}
Coin: {symbol}
""")

    level = analyze_coin_strength(symbol)

dump_risk = analyze_dump_risk(symbol)

print("Dump risk:", dump_risk)

risk = choose_risk(level)

    send_message(f"""
Coin strength: {level}
Trade: ${risk['amount']}
Leverage: {risk['leverage']}x
""")

    print("Watching price...")

    while True:

        if detect_top(symbol):

            price = get_price(symbol)

            send_message("🔥 TOP DETECTED")

            open_demo_short(symbol, price, risk)

            break

        time.sleep(0.5)


run_bot()
