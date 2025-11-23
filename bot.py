import time
import asyncio
from telegram import Bot
import feedparser

# --- UNGA DETAILS ---
BOT_TOKEN = "8144965360:AAFUjgH6Ba1STnX_Qd9Bta1UAZQi0ytgU50"

# MUKKIYAM: Unga Channel Link "mega_deals_offers_2025" thana? Check pannunga!
CHANNEL_ID = "@mega_deals_offers_2025" 

AMAZON_TAG = "zahidbasha-21"

RSS_FEEDS = [
    "https://www.indiafreestuff.in/rss/hot-deals",
    "https://freekaamaal.com/rss/hot-deals"
]

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
        print(f"✅ Message Sent to Channel: {title}")
    except Exception as e:
        print(f"❌ MESSAGE SEND ERROR: {e}")
        print("⚠️ Check: 1. Bot Admin ah? 2. Channel Link Correct ah?")

async def check_deals():
    print("🔍 Checking RSS Feeds for new deals...")
    found_any = False
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            print(f"   -> Site Checked. Found {len(feed.entries)} entries.")
            
            # Top 3 deals check pannuvom
            for entry in feed.entries[:3]:
                if entry.title not in posted_deals:
                    final_link = add_affiliate_tag(entry.link)
                    await send_telegram_message(entry.title, final_link)
                    posted_deals.append(entry.title)
                    found_any = True
                    time.sleep(2)
        except Exception as e:
            print(f"Error reading feed: {e}")
            
    if not found_any:
        print("😴 No NEW deals found right now. Waiting...")

async def main():
    print("🚀 Bot Started! Sending TEST MESSAGE to Channel...")
    
    # 1. First, send a test message to confirm connection
    await send_telegram_message("Bot Connected Successfully!", "https://t.me/mega_deals_offers_2025")
    
    # 2. Start checking deals
    await check_deals()
    
    while True:
        print("⏳ Waiting 5 minutes for next check...")
        time.sleep(300) 
        await check_deals()

if __name__ == "__main__":
    asyncio.run(main())