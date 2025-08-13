# ai-content-relayer
**V 0.1.0**  
A program that can relay the content with AI.  
This version is **not** the AI-powered V1 yet — it currently works as an RSS-to-Telegram channel forwarder.  
The AI-enhanced V1 will be uploaded when its development is completed.

---

## 📌 Description
This script monitors multiple RSS feeds from selected websites and automatically sends new content updates to a target Telegram channel or group.  
It uses the **Pyrogram** library for interacting with Telegram Bot API and **feedparser** for reading RSS feeds.

---

## ✨ Features
- Monitor multiple RSS feed sources.
- Detects only *new* posts to avoid duplicates.
- Sends post description and source name to a Telegram channel/group.
- Configurable proxy support (SOCKS5).
- Easily extendable to add more RSS sources.
- Designed to be upgraded with AI capabilities in the next major version.

---

## ⚙️ Requirements
- Python **3.8+**
- Telegram **api_id** and **api_hash** (from [my.telegram.org](https://my.telegram.org))
- Telegram **bot_token** (create via [@BotFather](https://t.me/BotFather))
- Target Telegram channel/group username or ID.
- (Optional) SOCKS5 proxy credentials.
- RSS feed URLs from your desired sources.

---

## 📦 Installation

1. **Clone this repository**
```bash
git clone https://github.com/your-username/ai-content-relayer.git
cd ai-content-relayer
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Create a config by replacing values in the script

python
Copy
Edit
api_id = 12345678
api_hash = "your-api-hash"
bottoken = "your-bot-token"
target_channel = "@your-target-channel-id"
(Optional) Configure proxy

python
Copy
Edit
proxy_host = "127.0.0.1"
proxy_port = 1089
🚀 Usage
Run the script:

bash
Copy
Edit
python main.py
The bot will:

Start monitoring all configured RSS sources.

Send a message to the Telegram channel whenever a new post is detected.

Repeat every 5 seconds.

📝 Example Output
sql
Copy
Edit
خبر جدید از theguardian:

Boris Johnson faces questions over latest policy decision...
📡 Adding More RSS Sources
Inside the script, add new entries to:

python
Copy
Edit
resource_sites = {
    "sitename": "https://site.com/rss"
}
🛠 Dependencies
Pyrogram – Telegram API client

feedparser – RSS feed parser

Install manually if needed:

bash
Copy
Edit
pip install pyrogram feedparser tgcrypto
