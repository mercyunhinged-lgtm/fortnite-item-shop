import os
import time
import requests
from playwright.sync_api import sync_playwright

SHOP_URL = "https://www.fortnite.com/item-shop?lang=en-US"
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

OUT_PATH = "item_shop.png"

def take_screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=2,
            locale="en-US",
        )
        page = context.new_page()

        # Load the page
        page.goto(SHOP_URL, wait_until="domcontentloaded", timeout=60000)

        # Give it time to load assets (item cards are often lazy-loaded)
        page.wait_for_timeout(8000)

        # Try to dismiss common consent dialogs if present (best-effort; won't fail if not found)
        for selector in [
            "button:has-text('Accept')",
            "button:has-text('I Accept')",
            "button:has-text('Agree')",
            "button:has-text('OK')",
        ]:
            try:
                page.locator(selector).first.click(timeout=1500)
                page.wait_for_timeout(1500)
                break
            except Exception:
                pass

        # Scroll a bit to trigger lazy-load
        for _ in range(6):
            page.mouse.wheel(0, 1200)
            page.wait_for_timeout(1000)

        # Back to top for a nicer full-page screenshot
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(1000)

        # Full page screenshot (big file, but reliable)
        page.screenshot(path=OUT_PATH, full_page=True)

        context.close()
        browser.close()

def post_to_discord():
    if not WEBHOOK_URL:
        raise RuntimeError("DISCORD_WEBHOOK_URL is missing")

    # Discord webhooks accept multipart form upload
    with open(OUT_PATH, "rb") as f:
        files = {"file": ("item_shop.png", f, "image/png")}
        payload = {
            "content": "🛒 **Fortnite Item Shop (Auto Screenshot)**\nDon’t forget to use code: **msdreams** ☁️💖"
        }
        r = requests.post(WEBHOOK_URL, data=payload, files=files, timeout=30)
        r.raise_for_status()

def main():
    take_screenshot()
    post_to_discord()

if __name__ == "__main__":
    main()
