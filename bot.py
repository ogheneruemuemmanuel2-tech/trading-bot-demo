import time
from keep_alive import keep_alive

keep_alive()

print("Trading bot started...")

while True:
    print("Bot is running and checking the market...")
    time.sleep(60)
