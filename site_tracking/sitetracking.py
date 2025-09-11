import json
import feedparser
from pyrogram import Client
import asyncio
import os
from google import genai
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTING_FILE = os.path.join(BASE_DIR, "data-setting.json")

with open(SETTING_FILE, "r", encoding="utf-8") as setting:
    data = json.load(setting)

rss_links: dict = data.get('sites').get('resources')
id_list = list(rss_links.keys())

tokenbot = data.get("bot_token")
target_chnl = data.get("goal_id")
apiid = data['api_id']
apihash = data['api_hash']

if data['ai']['val']:
    usingAi = True
    ai_api = data['ai']['api_token']
    prompt_file = os.path.join(BASE_DIR, "prompt.txt")
    with open(prompt_file, 'r') as f:
        prompt = f.read()
    gemini = genai.Client(api_key=ai_api)
else:
    usingAi = False

proxy = dict(hostname="127.0.0.1", port=1089, scheme="socks5") if data.get("local_proxy_enabled") else None

bot = Client(
    "rss-tracker",
    api_id=apiid,
    api_hash=apihash,
    bot_token=tokenbot,
    proxy=proxy
)

RSS_JSON_FILE = os.path.join(BASE_DIR, "rss-id.json")


def checkingfornew(site_id: int) -> str | None:
    
    if not os.path.exists(RSS_JSON_FILE):
        with open(RSS_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(rss_links, f)
    
    with open(RSS_JSON_FILE, "r", encoding="utf-8") as f:
        full_sources = json.load(f)

    last_link = full_sources.get(str(site_id), "")

    feed = feedparser.parse(rss_links[str(site_id)])
    if not feed.entries:
        print(f"!-! {site_id} has no entries")
        return None

    latest = feed.entries[0]
    latest_link = getattr(latest, "link", None)
    if not latest_link or last_link == latest_link:
        return None

    full_sources[str(site_id)] = latest_link
    with open(RSS_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(full_sources, f, ensure_ascii=False, indent=2)

    # برمی‌گرداند متن خبر برای ارسال به AI
    body = getattr(latest, "description", None) or getattr(latest, "summary", None) or getattr(latest, "title", "")
    return body


# تابع اصلی چک کردن سایت‌ها
async def check_sites(poll_interval: int = 30):
    while True:
        for rss_id in id_list:
            try:
                new_text = checkingfornew(rss_id)
                if new_text:
                    
                    if usingAi:
                        try:
                            airesponse = gemini.models.generate_content(
                                model="gemini-2.5-flash",
                                contents=f"{prompt}\n{new_text}"
                            )
                            message_to_send = airesponse.text
                            print(f"Ai done his work (on {rss_id}), sending message...")
                        except Exception as e:
                            print(f"Error in AI response for {rss_id}:\n{e}")
                            message_to_send = new_text  # fallback
                    else:
                        message_to_send = new_text

                    try:
                        await bot.send_message(target_chnl, message_to_send)
                        print(f"Sent feed from {rss_id} to {target_chnl}\n\n")
                    except Exception as e:
                        print(f"Failed to send message for {rss_id}:", e)
            except Exception as e:
                print(f"Error while checking {rss_id}: {e}")
        await asyncio.sleep(poll_interval)


async def run(poll_interval: int = 30):
    async with bot:
        task = asyncio.create_task(check_sites(poll_interval))
        print("site-tracker started")
        await asyncio.Event().wait()