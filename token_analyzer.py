import requests


def get_token_data(symbol):

    coin = symbol.replace("_USDT", "")

    try:

        url = f"https://api.coingecko.com/api/v3/coins/{coin.lower()}"

        r = requests.get(url)

        data = r.json()

        supply = data["market_data"]["total_supply"]

        circulating = data["market_data"]["circulating_supply"]

        marketcap = data["market_data"]["market_cap"]["usd"]

        return {
            "supply": supply,
            "circulating": circulating,
            "marketcap": marketcap
        }

    except:

        return None


def analyze_dump_risk(symbol):

    data = get_token_data(symbol)

    if not data:

        return "unknown"

    supply = data["supply"]
    circulating = data["circulating"]

    if not supply or not circulating:

        return "unknown"

    ratio = circulating / supply

    print("Circulating ratio:", ratio)

    if ratio < 0.2:

        return "high_dump"

    if ratio < 0.5:

        return "medium_dump"

    return "low_dump"
