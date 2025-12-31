import os
import requests
from datetime import datetime

# Discord webhook from GitHub Secrets
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Fortnite.gg rendered Item Shop image (auto-updates daily)
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

    response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
    response.raise_for_status()

if __name__ == "__main__":
    main()
