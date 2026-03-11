import random


def analyze_coin_strength(listing_text):

    score = 0

    # Check if many exchanges listing
    if "BINANCE" in listing_text or "BYBIT" in listing_text:
        score += 2

    if "GATE" in listing_text:
        score += 1

    # Check hype words
    if "AI" in listing_text:
        score += 1

    if "DEPIN" in listing_text:
        score += 1

    if "GAMEFI" in listing_text:
        score += 1

    # Random small factor for demo testing
    score += random.randint(0, 1)

    if score >= 3:
        return "strong"

    return "normal"


def choose_risk(level):

    if level == "strong":

        return {
            "amount": 20,
            "leverage": 15,
            "tp": 100
        }

    else:

        return {
            "amount": 10,
            "leverage": 8,
            "tp": 50
        }
