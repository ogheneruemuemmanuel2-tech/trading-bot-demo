def auto_leverage(change):

    if change < 2:
        return 15

    elif change < 5:
        return 10

    else:
        return 5
