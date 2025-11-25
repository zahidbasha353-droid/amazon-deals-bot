import time
import asyncio
import os
import requests
from threading import Thread
from flask import Flask
from telegram import Bot
import feedparser

# --- UNGA DETAILS ---
BOT_TOKEN = "8144965360:AAFUjgH6Ba1STnX_Qd9Bta1UAZQi0ytgU50"
CHANNEL_ID = "@mega_deals_offers_2025"
AMAZON_TAG = "zahidbasha-21"

# --- WORKING SOURCES (IndiaFreeStuff & FreeKaaMaal) ---
RSS_FEEDS = [
    "https://www.indiafreestuff.in/rss/hot-deals",
    "https://freekaamaal.com/rss/hot-deals"
]

# --- FAKE WEBSITE (RENDER UPKEEP) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running! (Advanced Mode)"

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
        # Message Format
        message = f"⚡ **{title}**\n\n🔗 **Check Deal:**\n{link}"
        await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')
        print(f"✅ Sent Deal: {title}", flush=True)
    except Exception as e:
        print(f"❌ Error sending msg: {e}", flush=True)

async def check_deals():
    print("🔍 Checking Deals (Advanced Mode)...", flush=True)
    
    # Strong Browser Header (Chrome) - Ithu iruntha Block panna maatanga
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    
    for feed_url in RSS_FEEDS:
        try:
            # 1. Strong Request (Fetch like a Browser)
            response = requests.get(feed_url, headers=headers, timeout=15)
            
            if response.status_code != 200:
                print(f"❌ Site Error {feed_url}: Status {response.status_code}", flush=True)
                continue

            # 2. Read Data
            d = feedparser.parse(response.content)
            
            if len(d.entries) == 0:
                print(f"⚠️ Feed empty: {feed_url}", flush=True)
                continue

            # 3. Process Deals
            for entry in d.entries[:3]:
                if entry.title not in posted_deals:
                    final_link = add_affiliate_tag(entry.link)
                    await send_telegram_message(entry.title, final_link)
                    
                    posted_deals.append(entry.title)
                    if len(posted_deals) > 100:
                        posted_deals.pop(0)
                    time.sleep(2)
        except Exception as e:
            print(f"❌ Error: {e}", flush=True)

async def main():
    print("🚀 Bot Started! Tracking IndiaFreeStuff...", flush=True)
    
    # Welcome Message
    try:
        bot = Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id=CHANNEL_ID, text="✅ **Source Fixed!**\nTracking Top Deals from IndiaFreeStuff...")
    except:
        pass

    await check_deals()
    
    while True:
        # Wait 5 minutes
        await asyncio.sleep(300) 
        await check_deals()

if __name__ == "__main__":
    keep_alive()
    asyncio.run(main())
