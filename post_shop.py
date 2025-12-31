import os
import requests
from datetime import datetime

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# CURRENT Fortnite Item Shop endpoint (stable)
API_URL = "https://fortnite-api.com/v2/shop/br?language=en"

def main():
    if not WEBHOOK_URL:
        raise RuntimeError("DISCORD_WEBHOOK_URL secret is missing")

    # Fetch shop
    r = requests.get(API_URL, timeout=20)
    r.raise_for_status()
    data = r.json()

    entries = data.get("data", {}).get("entries", [])
    if not entries:
        raise RuntimeError("No shop entries returned from Fortnite API")

    embeds = []
    today = datetime.utcnow().strftime("%B %d, %Y")

    for entry in entries:
        items = entry.get("items", [])
        if not items:
            continue

        item = items[0]

        images = item.get("images", {})
        image_url = (
            images.get("featured")
            or images.get("icon")
            or images.get("smallIcon")
        )

        if not image_url:
            continue

        embed = {
            "title": item.get("name", "Fortnite Item"),
            "description": "🛒 **Today’s Fortnite Item Shop**",
            "image": {"url": image_url},
            "color": 0xE6B7FF,
            "footer": {
                "text": "Don’t forget to use code: msdreams ☁️💖"
            }
        }

        embeds.append(embed)

        # Discord hard limit: max 10 embeds per message
        if len(embeds) == 10:
            break

    payload = {
        "content": f"✨ **Fortnite Item Shop — {today}** ✨",
        "embeds": embeds
    }

    post = requests.post(WEBHOOK_URL, json=payload, timeout=20)
    post.raise_for_status()

if __name__ == "__main__":
    main()
