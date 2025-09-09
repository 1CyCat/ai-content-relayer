import json
import threading
import asyncio
from channel_tracking.channeltracking import run_channel_tracker
from site_tracking.sitetracking import run as run_site
import time


imp_data = {
    'api_id' : None ,
    'api_hash' : None ,
    'number' : None ,
    'bot_token' : None ,
    'local_proxy_enabled' : False ,
    'ai' : {
        'val' : False ,
        'api_token' : None
    } ,
    'sites' : {},
    'source_channels' : [],
    'goal_id' : None
}


# asking each data needed:
imp_data['api_id'] = input("Enter account api id: ")
imp_data['api_hash'] = input("Enter account api hash: ")
imp_data['number'] = int(input("Enter account number: "))
imp_data['bot_token'] = input("Enter bot token: ")
proxy_using = input('Enable using system proxy ?  y/n : ')
if proxy_using == 'y':
    imp_data['local_proxy_enabled'] = True
ai = input('Using ai gemini api ?  y/n : ')
if ai == 'y':
    imp_data['ai']['val'] = True
    imp_data['ai']['api_token'] = input('enter gemini api: ')
elif ai == 'n':
    imp_data['ai']['val'] = False
num = int(input('enter num of your rss sites(after this u have to enter a label and rss link): '))
for i in range(num):
    label = input(f"enter label [{i+1}] :  ") 
    site = input(f"enter rss link [{i+1}] :  ")
    imp_data['sites'][label] = site 
num0 = int(input('enter num of source_channels for input (u have to just enter the num-id of channel): '))
for i in range(num0):
    chnl = int(input(f"enter num-id channel[{i+1}] :  "))
    imp_data['source_channels'].append(chnl)
imp_data['goal_id'] = input("Enter your tg-channel id (like @telegramchannel): ")




with open('data-setting.json' , 'w') as json_file :
    json.dump(imp_data,json_file)




def start_site_tracker():
    try:
        asyncio.run(run_site())
    except Exception as e:
        print(f"site-tracker stopped with error: {e}")


if __name__ == "__main__":

    site_thread = threading.Thread(target=start_site_tracker, daemon=True)
    site_thread.start()

    run_channel_tracker()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program stopped by user.")
