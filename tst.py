from pyrogram import Client , filters
from pyrogram.types import Message
from google import genai
import asyncio

api_id = 24382393  # جایگزین کن
api_hash = "476c460b2799544d58e5d64b433df9c4"  # جایگزین کن
bottoken = "8121071170:AAEmD9OqWdyGEkdvPcKZQWwUGYPfTAwWdzM"

proxy_host = "127.0.0.1"
proxy_port = 1089
proxy = {
    'http': 'socks5h://127.0.0.1:1089',
    'https': 'socks5h://127.0.0.1:1089'
}
app = Client(
    'tst',
    api_id= api_id,
    api_hash= api_hash,
    proxy=dict(
    hostname=proxy_host,
    port=proxy_port,
    scheme="socks5"
    )
)

api_key = 'AIzaSyDpRAjc8Lx0SYF6PKoouX0WUGfDUkGM7yI'
geminijun = genai.Client(api_key=api_key)


channels = [-1002679765201,-1002563073030]

@app.on_message(filters.channel)
async def get_channel_messages(client: Client, message: Message):
    print(f"new message from: {message.chat.title}:")



    await client.send_message(
        chat_id="@output_programing",
        text=f"new feed from channel {message.chat.title}:\n\n\n{message.text}"
    )



print("Bot is running...")
app.run()
















# @power.on_message(filters.channel & filters.text)
# async def get_channel_messages(client: Client, message: Message):
#     print(f"Received message from chat id: {message.chat.id}, title: {message.chat.title}")
#     print(f"Message text: {message.text}")

#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=f"{prompt}\n{message.text}"
#     )

#     print(f"new message from:\n{message.chat.title}:")

#     await power.send_message("@output_programing", f"new feed from channel {message.chat.title}:\n{message.text}\nedited by AI:\n{response.text}")
