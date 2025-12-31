import os
import requests
from datetime import datetime

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

API_URL = "https://fortnite-api.com/v2/shop/br/combined?language=en"

def main():
    if not WEBHOOK_URL:
        raise ValueError("Missing DISCORD_WEBHOOK_URL")

    response = requests.get(API_URL, timeout=20)
    response.raise_for_status()
    data = response.json()

    shop_date = datetime.utcnow().strftime("%B %d, %Y")

    embeds = []

    sections = {
        "Featured": data["data"]["featured"]["entries"],
        "Daily": data["data"]["daily"]["entries"]
    }

    for section_name, entries in sections.items():
        for entry in entries:
            if not entry.get("items"):
                continue

            item = entry["items"][0]
            image = (
                item["images"].get("featured")
                or item["images"].get("icon")
            )

            if not image:
                continue

            embed = {
                "title": item["name"],
                "description": f"**{section_name} Item**",
                "image": {"url": image},
                "footer": {
                    "text": "Don’t forget to use code: msdreams ☁️💖"
                },
                "color": 0xE6B7FF
            }

            embeds.append(embed)

            if len(embeds) >= 9:
                break
        if len(embeds) >= 9:
            break

    payload = {
        "content": f"🛒 **Fortnite Item Shop — {shop_date}**",
        "embeds": embeds
    }

    post = requests.post(WEBHOOK_URL, json=payload)
    post.raise_for_status()

if __name__ == "__main__":
    main()
