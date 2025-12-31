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

        # CORRECT image location
        image_url = item.get("displayAssets", [{}])[0].get("full_background")

        if not image_url:
            continue

        embeds.append({
            "title": item.get("name", "Fortnite Item"),
            "image": {"url": image_url},
            "color": 0xE6B7FF,
            "footer": {
                "text": "Don’t forget to use code: msdreams ☁️💖"
            }
        })

        if len(embeds) >= 10:
            break

    # SAFETY CHECK — NEVER POST EMPTY
    if not embeds:
        raise RuntimeError("No embeds created — API returned no usable images")

    payload = {
        "content": f"🛒 **Fortnite Item Shop — {today}**",
        "embeds": embeds
    }

    post = requests.post(WEBHOOK_URL, json=payload, timeout=10)
    post.raise_for_status()

if __name__ == "__main__":
    main()
