import time
import asyncio
import os
from threading import Thread
from flask import Flask
from telegram import Bot
import feedparser

# --- UNGA DETAILS ---
BOT_TOKEN = "8144965360:AAFUjgH6Ba1STnX_Qd9Bta1UAZQi0ytgU50"
CHANNEL_ID = "@mega_deals_offers_2025"
AMAZON_TAG = "zahidbasha-21"

RSS_FEEDS = [
    "https://www.indiafreestuff.in/rss/hot-deals",
    "https://freekaamaal.com/rss/hot-deals"
]

# --- FAKE WEBSITE CODE START (Render ku aaga) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running! I am alive!"

def run():
    # Render ethirpaarkura PORT la run pannuvom
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()
# --- FAKE WEBSITE CODE END ---

posted_deals = []

def add_affiliate_tag(link):
    if "amazon.in" in link:
        separator = "&" if "?" in link else "?"
        return f"{link}{separator}tag={AMAZON_TAG}"
    return link

async def send_telegram_message(title, link):
    try:
        bot = Bot(token=BOT_TOKEN)
        message = f"🔥 **{title}**\n\n👇 **Buy Now:**\n{link}"
        await bot.send_message(
            chat_id=CHANNEL_ID, 
            text=message, 
            parse_mode='Markdown',
            read_timeout=60, 
            write_timeout=60, 
            connect_timeout=60
        )
        print(f"✅ Sent: {title}")
    except Exception as e:
        print(f"❌ Error: {e}")

async def check_deals():
    print("🔍 Checking deals...")
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:3]:
                if entry.title not in posted_deals:
                    final_link = add_affiliate_tag(entry.link)
                    await send_telegram_message(entry.title, final_link)
                    posted_deals.append(entry.title)
                    time.sleep(2)
        except Exception as e:
            print(f"Skipping feed due to error: {e}")

async def main():
    print("🚀 Bot Started with Web Server!")
    await check_deals()
    while True:
        time.sleep(300) # 5 mins wait
        await check_deals()

if __name__ == "__main__":
    # Bot start aagum bothe, Fake Website-um start aagum
    keep_alive()
    asyncio.run(main())