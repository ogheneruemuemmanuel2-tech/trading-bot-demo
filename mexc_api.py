import requests

BASE_URL = "https://contract.mexc.com"

def get_futures_symbols():
    url = BASE_URL + "/api/v1/contract/detail"
    data = requests.get(url).json()
    return data["data"]

def get_price(symbol):
    url = BASE_URL + f"/api/v1/contract/ticker?symbol={symbol}"
    data = requests.get(url).json()
    return data["data"]["lastPrice"]
