import feedparser  
import asyncio 
from pyrogram import Client


# Telegram bot and informations
api_id = 12345678
api_hash = "your-api-hash"
bottoken = "your-bot-token"
proxy_host = "127.0.0.1"
proxy_port = 1089
proxy = {
    'http': 'socks5h://127.0.0.1:1089',
    'https': 'socks5h://127.0.0.1:1089'
}
bot = Client(
    'Pwr',
    api_id= api_id,
    api_hash= api_hash,
    bot_token=bottoken,
    proxy=dict(
    hostname=proxy_host,
    port=proxy_port,
    scheme="socks5"
    )
)

target_channel = '@your-tanget-channel-id'


# here i used a simple site/rss's for example
resource_sites = { 
    "theguardian": "https://www.theguardian.com/politics/rss",
    "cnet": "https://www.cnet.com/rss/news/",
    "mushable": "https://mashable.com/tech/feed",
    "gizmodo": "https://gizmodo.com/rss",
    "theverge": "https://www.theverge.com/rss/index.xml"
}

def check_for_new_post_in_site (site_name):
    try:     
        with open( f'{site_name}.txt' , "r" , encoding="utf-8") as reading_url_infile :   
            last_link_feed_in_txt = reading_url_infile.read().strip()
    except FileNotFoundError:
        with open(f'{site_name}.txt' , "w" , encoding="utf-8") as file:
            file.write("")
            print(f"file for {site_name} was not created, programm will be try again!")
            return False
        
    feeds = feedparser.parse(resource_sites[site_name])   
    
    if len(feeds.entries) < 2:
        print(f"{site_name} has less than 2 entries!")
        return False
    
    latest_feed = feeds.entries[1]  
    latest_news_link = latest_feed.link  


    if last_link_feed_in_txt == latest_news_link:  
        print(f"the news_link was same for {site_name}!")
        return False
    else:
        print(f"the news_link was diffrent for {site_name}!")
        with open( f'{site_name}.txt' , "w" , encoding="utf-8") as file_url:
            file_url.write(latest_news_link)
        return True, latest_feed.description, site_name



# THE MAIN DEF:

async def check_sites(): 
    await bot.start()
    print("bot is running ...")

    while True:
        for site in resource_sites.keys():
            result = check_for_new_post_in_site(site)
            if result:
                new_post, description, site_name = result
                await bot.send_message(target_channel, f"خبر جدید از {site_name}:\n\n{description}")
                print(f"Sent news from {site_name}")
        
        print("bot is going to sleep for 5 seconds!")
        await asyncio.sleep(5)
    

if __name__ == "__main__":
    asyncio.run(check_sites())
