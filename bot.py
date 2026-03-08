import time
import requests
from keep_alive import keep_alive

keep_alive()

print("Trading bot started...")

def get_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    data = requests.get(url).json()
    return float(data["price"])

while True:
    price = get_price()
    print("BTC Price:", price)
    time.sleep(60)
