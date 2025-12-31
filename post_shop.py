import os
import requests
from datetime import datetime

# Secrets from GitHub Actions
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
FORTNITE_API_KEY = os.getenv("FORTNITE_API_KEY")

API_URL = "https://fortnite-api.com/v2/shop/br"

def main():
    if not WEBHOOK_URL:
        raise RuntimeError("DISCORD_WEBHOOK_URL is missing")
    if not FORTNITE_API_KEY:
        raise RuntimeError("FORTNITE_API_KEY is missing")

    headers = {
        "Authorization": FORTNITE_API_KEY
    }

    # Fetch item shop
    response = requests.get(API_URL, headers=headers, timeout=20)
    response.raise_for_status()
    data = response.json()

    entries = data.get("data", {}).get("entries", [])
    if not entries:
        raise RuntimeError("No shop entries returned")

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

        embeds.append({
            "title": item.get("name", "Fortnite Item"),
            "description": "🛒 **Today’s Fortnite Item Shop**",
            "image": {"url": image_url},
            "color": 0xE6B7FF,
            "footer": {
                "text": "Don’t forget to use code: msdreams ☁️💖"
            }
        })

        # Discord limit
        if len(embeds) >= 10:
            break

    payload = {
        "content": f"✨ **Fortnite Item Shop — {today}** ✨",
        "embeds": embeds
    }

    post = requests.post(WEBHOOK_URL, json=payload, timeout=20)
    post.raise_for_status()

if __name__ == "__main__":
    main()
