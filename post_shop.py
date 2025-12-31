import os
import requests
from datetime import datetime

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
ITEM_SHOP_URL = "https://www.fortnite.com/item-shop?lang=en-US"

def main():
    if not WEBHOOK_URL:
        raise RuntimeError("DISCORD_WEBHOOK_URL is missing")

    today = datetime.utcnow().strftime("%B %d, %Y")

    payload = {
        "embeds": [
            {
                # 👇 TITLE IS CLICKABLE
                "title": f"Fortnite Item Shop — {today}",
                "url": ITEM_SHOP_URL,

                "description": (
                    "🛒 **The Item Shop has refreshed!**\n\n"
                    f"👉 **[CLICK HERE TO OPEN THE ITEM SHOP]({ITEM_SHOP_URL})**\n\n"
                    "Don’t forget to use code **msdreams** ☁️💖"
                ),
                "color": 0xE6B7FF
            }
        ]
    }

    r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
    r.raise_for_status()

if __name__ == "__main__":
    main()
