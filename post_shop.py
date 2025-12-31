import os
import requests
from datetime import datetime

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

SHOP_IMAGE_URL = "https://fortnite.gg/img/shop.png"

def main():
    if not WEBHOOK_URL:
        raise RuntimeError("DISCORD_WEBHOOK_URL is missing")

    today = datetime.utcnow().strftime("%B %d, %Y")

    payload = {
        "embeds": [
            {
                "title": f"Fortnite Item Shop — {today}",
                "description": (
                    "🛒 **The Item Shop has refreshed!**\n\n"
                    "Don’t forget to use code **msdreams** ☁️💖\n"
                    "Supporting the creator helps keep the Dream alive ☁️"
                ),
                "image": {
                    "url": SHOP_IMAGE_URL
                },
                "color": 0xE6B7FF
            }
        ]
    }

    r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
    r.raise_for_status()

if __name__ == "__main__":
    main()
