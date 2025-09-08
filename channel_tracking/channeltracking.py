import json
import os
from pyrogram import Client, filters
import asyncio
from google import genai

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTING_FILE = os.path.join(BASE_DIR, "data-setting.json")

with open(SETTING_FILE, 'r') as setting:
    data = json.load(setting)

if data['local_proxy_enabled']:
    proxy_host = "127.0.0.1"
    proxy_port = 1089


target_chnl = data['goal_id']
apiid = data['api_id']
apihash = data['api_hash']
number = str(data['number'])
if not number.startswith("+"):
    number = "+" + number
source_channels: list = data['source_channels']
if data['ai']['val'] :
    ai_api = data['ai']['api_token']

acc = Client(
    'tg-channel-tracker',
    api_id=apiid,
    api_hash=apihash,
    phone_number=number,
    proxy=dict(hostname=proxy_host, port=proxy_port, scheme="socks5") if data['local_proxy_enabled'] else None
)
prompt_file = os.path.join(BASE_DIR,"prompt.txt")
with open(prompt_file,'r') as f :
    prompt = f.read()
gemini = genai.Client(api_key=ai_api)

def run_channel_tracker():
    app = Client(
        'tg-channel-tracker',
        api_id=apiid,
        api_hash=apihash,
        phone_number=number,
        proxy=dict(hostname=proxy_host, port=proxy_port, scheme="socks5") if proxy_host else None
    )

    @app.on_message(filters.channel)
    def get_channel_messages(client: Client, message):
        if source_channels and message.chat.id not in source_channels:
            return

        print(f"New post from [{message.chat.title}]")

        try:
            response = gemini.models.generate_content(
                model="gemini-2.5-flash", contents=f"{prompt}\n{message.text}"
            )
            print(f"Ai done his work (on {message.chat.title}), end message to telgram ...")
        except Exception as e:
            print(f'ther is an error in Ai responsing:\n{e}')

        client.send_message(
            chat_id=target_chnl,
            text=f"{response.text}"
        )

    print("Channel tracker is running...")
    app.run()