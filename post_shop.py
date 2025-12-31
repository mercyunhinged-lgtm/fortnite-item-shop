import os
import requests
from datetime import datetime

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
FORTNITE_API_KEY = os.getenv("FORTNITE_API_KEY")

API_URL = "https://fortnite-api.com/v2/shop"

def main():
    if not WEBHOOK_URL:
        raise RuntimeError("DISCORD_WEBHOOK_URL is missing")
    if not FORTNITE_API_KEY:
        raise RuntimeError("FORTNITE_API_KEY is missing")

    headers = {
        "Authorization": FORTNITE_API_KEY
    }

    r = requests.get(API_URL, headers=headers, timeout=10)
    r.raise_for_status()
    data = r.json()

    shop = data.get("data", {})
    entries = shop.get("entries", [])
    if not entries:
        raise RuntimeError("No shop entries returned")

    # 🔹 Try to get a SHOP-LEVEL image (most reliable)
    banner_image = None
    for entry in entries:
        assets = entry.get("displayAssets", [])
        if assets:
            banner_image = assets[0].get("full_background")
            if banner_image:
                break

    today = datetime.utcnow().strftime("%B %d, %Y")

    embed = {
        "title": f"Fortnite Item Shop — {today}",
        "description": "🛒 The Item Shop has refreshed!\n\nDon’t forget to use code **msdreams** ☁️💖",
        "color": 0xE6B7FF,
        "footer": {
            "text": "Supporting the creator helps keep the Dream alive 💭"
        }
    }

    if banner_image:
        embed["image"] = {"url": banner_image}

    payload = {
        "embeds": [embed]
    }

    post = requests.post(WEBHOOK_URL, json=payload, timeout=10)
    post.raise_for_status()

if __name__ == "__main__":
    main()
