import requests
import time
import re


def extract_symbol(text):

    match = re.search(r'([A-Z]{2,10})USDT', text)

    if match:
        return match.group(1) + "_USDT"

    return None


# ---------- MEXC ----------
def scan_mexc():

    try:

        url = "https://www.mexc.com/support/sections/360000254832-New-Listings"

        r = requests.get(url)

        text = r.text.upper()

        symbol = extract_symbol(text)

        if symbol:

            return "MEXC", symbol

    except:
        pass

    return None, None


# ---------- BYBIT ----------
def scan_bybit():

    try:

        url = "https://announcements.bybit.com"

        r = requests.get(url)

        text = r.text.upper()

        symbol = extract_symbol(text)

        if symbol:

            return "BYBIT", symbol

    except:
        pass

    return None, None


# ---------- GATE ----------
def scan_gate():

    try:

        url = "https://www.gate.io/announcements"

        r = requests.get(url)

        text = r.text.upper()

        symbol = extract_symbol(text)

        if symbol:

            return "GATE", symbol

    except:
        pass

    return None, None


def scanner_loop():

    print("🔎 Scanning exchanges...")

    while True:

        exchange, symbol = scan_mexc()

        if symbol:
            return exchange, symbol

        exchange, symbol = scan_bybit()

        if symbol:
            return exchange, symbol

        exchange, symbol = scan_gate()

        if symbol:
            return exchange, symbol

        time.sleep(20)
