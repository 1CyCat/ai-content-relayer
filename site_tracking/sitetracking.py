# site_tracking.py
import json
import feedparser
from pyrogram import Client
import asyncio
import os
from google import genai

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTING_FILE = os.path.join(BASE_DIR, "data-setting.json")

with open(SETTING_FILE, "r", encoding="utf-8") as setting:
    data = json.load(setting)

rss_links: dict = data.get("sites", {})
tokenbot = data.get("bot_token")
target_chnl = data.get("goal_id")
apiid = data['api_id']
apihash = data['api_hash']
if data['ai']['val'] :
    ai_api = data['ai']['api_token']

proxy = dict(hostname="127.0.0.1", port=1089, scheme="socks5") if data.get("local_proxy_enabled") else None

bot = Client(
    "rss-tracker",
    api_id=apiid,
    api_hash=apihash,
    bot_token=tokenbot,
    proxy=proxy
)

prompt_file = os.path.join(BASE_DIR,"prompt.txt")
with open(prompt_file,'r') as f :
    prompt = f.read()
gemini = genai.Client(api_key=ai_api)

def checkingfornew(site_name: str) -> bool:
    fname = os.path.join(os.path.dirname(__file__), f"{site_name}.txt")
    try:
        with open(fname, "r", encoding="utf-8") as f:
            last = f.read().strip()
    except FileNotFoundError:
        with open(fname, "w", encoding="utf-8") as f:
            f.write("")
        last = ""

    feeds = feedparser.parse(rss_links[site_name])
    if not feeds.entries:
        print(f"!-! {site_name} has no entries")
        return False

    latest = feeds.entries[0]  # usually newest is at index 0
    latest_link = getattr(latest, "link", None)
    if not latest_link:
        return False

    if last == latest_link:
        return False

    with open(fname, "w", encoding="utf-8") as f:
        f.write(latest_link)
    print(f"new feed from {site_name} was detected!")
    return True


async def check_sites(poll_interval: int = 30):
    while True:
        for site in list(rss_links.keys()):
            try:
                if checkingfornew(site):
                    feed = feedparser.parse(rss_links[site])
                    if not feed.entries:
                        continue
                    entry = feed.entries[0]
                    body = getattr(entry, "description", None) or getattr(entry, "summary", None) or getattr(entry, "title", "")
                    text = f"new feed from site {site}:\n\n{body}\n\n{getattr(entry, 'link', '')}"

                    try:
                        response = gemini.models.generate_content(
                            model="gemini-2.5-flash", contents=f"{prompt}\n{text}"
                        )
                        print(f"Ai done his work (on {site}), send message to telgram ...")
                    except Exception as e:
                        print(f'ther is an error in Ai responsing:\n{e}')
                    
                    try:
                        await bot.send_message(target_chnl, f"{site}:\n\n{response.text}")
                        print(f"Sent feed from {site} to {target_chnl}\n\n")
                    except Exception as e:
                        print("Failed to send message:", e)
            except Exception as e:
                print(f"Error while checking {site}: {e}")
        await asyncio.sleep(poll_interval)


async def run(poll_interval: int = 30):
    async with bot:
        task = asyncio.create_task(check_sites(poll_interval))
        print("site-tracker started")
        await asyncio.Event().wait() 
