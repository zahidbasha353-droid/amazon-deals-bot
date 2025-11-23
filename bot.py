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

# --- FAKE WEBSITE (RENDER UPKEEP) ---
app = Flask('')

@app.route('/')
def home():
    return "I am Alive! Bot is Running..."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOT LOGIC ---
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
        await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')
        print(f"✅ Sent Deal: {title}", flush=True)
    except Exception as e:
        print(f"❌ Error sending msg: {e}", flush=True)

async def check_deals():
    print("🔍 Checking deals...", flush=True)
    # Fake Browser Header (Anti-Block)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    for feed_url in RSS_FEEDS:
        try:
            # Using request_headers to mimic a browser
            d = feedparser.parse(feed_url, request_headers=headers)
            
            if len(d.entries) == 0:
                print(f"⚠️ No entries found in {feed_url}", flush=True)
                continue

            for entry in d.entries[:2]: # Check top 2 deals
                if entry.title not in posted_deals:
                    final_link = add_affiliate_tag(entry.link)
                    await send_telegram_message(entry.title, final_link)
                    posted_deals.append(entry.title)
                    # Keep memory small
                    if len(posted_deals) > 50:
                        posted_deals.pop(0)
                    time.sleep(2)
        except Exception as e:
            print(f"❌ Feed Error: {e}", flush=True)

async def main():
    print("🚀 Bot Started! Sending Hello Message...", flush=True)
    # Start aana udane oru Hello solluvom
    try:
        bot = Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id=CHANNEL_ID, text="✅ **Bot Restarted & Connected!**\nScanning for deals now...")
    except Exception as e:
        print(f"Startup Msg Error: {e}")

    await check_deals()
    
    while True:
        # Wait 5 minutes
        await asyncio.sleep(300) 
        await check_deals()

if __name__ == "__main__":
    keep_alive()
    asyncio.run(main())
