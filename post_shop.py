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

    r = requests.get(API_URL, headers=headers, timeout=20)
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
        images = item.get("images", {})

        image_url = (
            images.get("featured")
            or images.get("icon")
            or images.get("small
