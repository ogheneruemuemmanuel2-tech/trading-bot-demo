import requests

BOT_TOKEN = "8722594173:AAH33q_51XGUOku6NsJn41EO1dme9gdiL-I"
CHAT_ID = "7375137177"


def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": text
    }

    try:
        requests.post(url, data=data)
    except:
        print("Telegram message failed")
