
#libraries
import feedparser
import requests
from pyrogram import Client , filters 
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserNotParticipant, PeerIdInvalid
from pyrogram.types import Message
import asyncio
from google import genai


#telegram stuff
api_id = 24382393
api_hash = "476c460b2799544d58e5d64b433df9c4"
my_phone = "+989361088530"
bottoken = "8121071170:AAEmD9OqWdyGEkdvPcKZQWwUGYPfTAwWdzM"
proxy_host = "127.0.0.1"
proxy_port = 1089
proxy = {
    'http': 'socks5h://127.0.0.1:1089',
    'https': 'socks5h://127.0.0.1:1089'
}
power = Client(
    'Pwr',
    api_id= api_id,
    api_hash= api_hash,
    phone_number=my_phone,
    proxy=dict(
    hostname=proxy_host,
    port=proxy_port,
    scheme="socks5"
    )
)


#gemini client
api_key = 'AIzaSyDpRAjc8Lx0SYF6PKoouX0WUGfDUkGM7yI'
geminiai = genai.Client(api_key=api_key)

#resouces
resource_sites = {
    "theverge": "https://www.theverge.com/rss/index.xml",
    "cnn": "http://rss.cnn.com/rss/cnn_latest.rss",
    "wired": "https://www.wired.com/feed/rss",
    "gamespot": "https://www.gamespot.com/feeds/mashup/",
    "nyt_world": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "engadget": "https://www.engadget.com/rss.xml",
    "arstechnica": "http://feeds.arstechnica.com/arstechnica/index"
}


#prompt for gemini
with open(r"D:\CODING-python\Projects\ai_content_relayer\prompt_text.txt", "r", encoding="utf-8") as theprompt:
    prompt = theprompt.read()


#cheking for new post in sites
def new_s_sitepost (site_name):  # this is for checking site status about new post and sends to check_sites() : true or false    
    print('checking for new started!')
    try:
        with open( f'{site_name}.txt' , "r" , encoding="utf-8") as reading_url_infile :   # save (last site link) in file to last_link_site_in_txt
            last_link_site_in_txt = reading_url_infile.read().strip()
    except:
        with open(f'{site_name}.txt','w',encoding="utf-8") as newfile:
            newfile.write(' ')
            last_link_site_in_txt = ""


    feeds = feedparser.parse(resource_sites[site_name])   #geting news   - in () gives this code: url site for fetchings/receiving
    
    if len(feeds.entries) < 2:
        print(f"⚠️ {site_name} has less than 2 entries!")
        return False

    latest_feed = feeds.entries[1]    #geting just last feed
    latest_feed_link = latest_feed.link    #variable for last feed #link


    if last_link_site_in_txt == latest_feed_link:   # IMPORTANT , chech that they are diffrent or not
        print(f"the news_link was same for {site_name}!")
        return False
    else:
        print(f"the news_link was diffrent for {site_name}!")
        with open( f'{site_name}.txt' , "w" , encoding="utf-8") as file_url:
            file_url.write(latest_feed_link)
        return True

#--------------------------------------------------------------------------------

#geting new posyt from sites and send to telegram channel
async def check_sites(): # Do all about site stuff
    print("check_sites() is working")
    for sites_to_check in resource_sites.keys():
        await asyncio.sleep(5)
        if new_s_sitepost(sites_to_check) is True :   # if there was not new feed , so pass
            new_feed = feedparser.parse(resource_sites[sites_to_check])
            releasable_feed = new_feed.entries[1]
            news_for_release = releasable_feed.description

            response = geminiai.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"{prompt}\n{news_for_release}"
            )

            await power.send_message("@output_programing", f"new feed from site {sites_to_check}:\n{news_for_release}\n\n\nedited by AI:\n{response.text}")
            
            # await power.send_message("@output_programing", f":خبر جدید\n\n{news_for_release}")
            # await power.send_message("@logstest_slq",f"the NEWS was posted from {sites_to_check}")

        else :
            pass



async def doing_loop():
    while True:
        await check_sites()
        await asyncio.sleep(3)



async def main():
    await power.start()
    print("Bot started")


    asyncio.create_task(doing_loop())

    stop_event = asyncio.Event()
    try:
        await stop_event.wait()  
    except (KeyboardInterrupt, SystemExit):
        print("Stopping...")

    await power.stop()
    while True:
        await asyncio.sleep(60)    

if __name__ == "__main__":
    asyncio.run(main())


