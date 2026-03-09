def auto_leverage(price_change):

    if price_change < 2:
        return 15

    elif price_change < 5:
        return 10

    else:
        return 5
