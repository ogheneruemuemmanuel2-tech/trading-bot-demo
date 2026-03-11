import requests
from bs4 import BeautifulSoup
import time
import re

URL = "https://www.mexc.com/support/sections/360000254832-New-Listings"


def extract_symbol(text):

    # looks for things like ABCUSDT
    match = re.search(r'([A-Z]{2,10})USDT', text)

    if match:
        coin = match.group(1)
        symbol = coin + "_USDT"
        return symbol

    return None


def check_new_listing():

    try:

        r = requests.get(URL)
        soup = BeautifulSoup(r.text, "html.parser")

        titles = soup.find_all("a")

        for t in titles:

            text = t.text.upper()

            if "FUTURES" in text or "PERPETUAL" in text:

                symbol = extract_symbol(text)

                return text, symbol

    except Exception as e:

        print("Scanner error:", e)

    return None, None


def scanner_loop():

    print("🔎 Scanning MEXC announcements...")

    while True:

        listing, symbol = check_new_listing()

        if listing and symbol:

            print("\n🚨 NEW FUTURES LISTING FOUND")
            print(listing)
            print("Detected symbol:", symbol)

            return listing, symbol

        time.sleep(30)
