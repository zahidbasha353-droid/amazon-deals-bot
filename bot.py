import time
import asyncio
import os
import random
import requests
from bs4 import BeautifulSoup
from threading import Thread
from flask import Flask
from telegram import Bot

# --- UNGA DETAILS ---
BOT_TOKEN = "8144965360:AAFUjgH6Ba1STnX_Qd9Bta1UAZQi0ytgU50"
CHANNEL_ID = "@mega_deals_offers_2025"
AMAZON_TAG = "zahidbasha-21"

# --- TARGET AMAZON PAGE (Itha maathi vera category vekalam) ---
# Ippo "Today's Deals" sorted by Newest nu potruken
AMAZON_URL = "https://www.amazon.in/s?k=deal+of+the+day&s=date-desc-rank"

# --- ROTATING HEADERS (Masks) ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
]

# --- FAKE WEBSITE (Render ku) ---
app = Flask('')

@app.route('/')
def home():
    return "Amazon Smart Scraper is Running..."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOT LOGIC ---
posted_deals = []

def get_header():
    # Random ah oru Mask poduvom
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.google.com/'
    }

def add_affiliate_tag(link):
    if "amazon.in" in link:
        separator = "&" if "?" in link else "?"
        return f"{link}{separator}tag={AMAZON_TAG}"
    return link

async def send_telegram_message(title, price, link):
    try:
        bot = Bot(token=BOT_TOKEN)
        # Message Format with Price
        message = f"🚨 **AMAZON DIRECT DEAL!**\n\n📦 **{title}**\n💰 **Price:** {price}\n\n👇 **Buy Now:**\n{link}"
        
        await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')
        print(f"✅ Sent Deal: {title}", flush=True)
    except Exception as e:
        print(f"❌ Error sending msg: {e}", flush=True)

async def check_amazon():
    print("🕵️‍♂️ Secretly checking Amazon...", flush=True)
    try:
        response = requests.get(AMAZON_URL, headers=get_header())
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "lxml")
            
            # Searching for products in the page
            results = soup.find_all("div", {"data-component-type": "s-search-result"})
            
            if not results:
                print("⚠️ Amazon Page Loaded, but no products found (Structure Changed?)", flush=True)
            
            # Top 3 latest results
            for item in results[:3]:
                try:
                    # Title Edukkum
                    title_element = item.find("h2")
                    title = title_element.text.strip()
                    
                    # Link Edukkum
                    link_element = title_element.find("a")
                    raw_link = "https://www.amazon.in" + link_element['href']
                    
                    # Price Edukkum (Iruntha mattum)
                    price_element = item.find("span", {"class": "a-price-whole"})
                    if price_element:
                        price = "₹" + price_element.text
                    else:
                        price = "Check Link"

                    # Already post pannalaya nu check pannum
                    if title not in posted_deals:
                        final_link = add_affiliate_tag(raw_link)
                        await send_telegram_message(title, price, final_link)
                        
                        posted_deals.append(title)
                        if len(posted_deals) > 100:
                            posted_deals.pop(0)
                            
                        # Human Delay (Oru deal ku aprom 3 sec wait pannum)
                        time.sleep(3)
                        
                except Exception as inner_e:
                    print(f"Skipping one item: {inner_e}")
                    continue
        else:
            print(f"❌ Amazon Blocked us? Status: {response.status_code}", flush=True)

    except Exception as e:
        print(f"❌ Scraping Error: {e}", flush=True)

async def main():
    print("🚀 Amazon Smart Scraper Started!", flush=True)
    
    # Welcome Message
    try:
        bot = Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id=CHANNEL_ID, text="🕵️‍♂️ **Spy Mode On!**\nDirectly watching Amazon for deals...")
    except:
        pass

    await check_amazon()
    
    while True:
        # Wait 10 minutes (Amazon direct scraping ku konjam gap vidanum)
        await asyncio.sleep(600) 
        await check_amazon()

if __name__ == "__main__":
    keep_alive()
    asyncio.run(main())
