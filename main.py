from ensurepip import version
import requests
import json
import random
import sys
import time
from colorama import Fore, Back, Style
from utils import *

#https://discord.com/api/v9/channels/917792877302648844/messages?limit=50

DEBUG = False
VERSION = "1.0.0"

def success(message):
    print(Fore.BLACK + Back.GREEN + "SUCCESS:" + Style.RESET_ALL + " " + message + Fore.RESET)

def warn(message):
    print(Fore.YELLOW + "+:" + Style.RESET_ALL + " " + message + Fore.RESET)

def error(message):
    print(Back.RED + Fore.BLACK + "ERROR:" +
          Fore.RED + Back.RESET + " " + message + Fore.RESET)

def message(message):
    print(Fore.LIGHTCYAN_EX + "-> " + Fore.RESET + message)

send_count = 1
texts = []
tokens = []
channels = []

def main(sleep_time):
    get_texts()
    get_tokens()
    get_channels()
    while True:
        time.sleep(sleep_time)
        for token in tokens:
            for channel in channels:
                text = texts[2]
                send_message(
                    token,
                    channel,
                    text
                )

def send_message(token, channel_id, content):
    global send_count
    count = random.randint(5000, 99999999)
    headers = {
    'Content-type': 'application/json',
    'authorization': token,
    }
    print(token)
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    try:
        data = {"content":f"{content}","nonce":count,"tts":False}
        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        #message(f"[{send_count}] Message Sent: {Fore.LIGHTGREEN_EX + content}")
        print(response.text)
    except Exception as ex:
        print(ex)
    send_count+=1

def get_texts():
    with open('data/texts.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            texts.append(line.replace("\n", ""))

def get_tokens():
    with open('data/tokens.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            tokens.append(line.replace("\n", ""))

def get_channels():
    with open('data/channels.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            channels.append(line.replace("\n", ""))

if __name__ == "__main__":
    if not DEBUG: message(f"Welcome LES:Over Version:{VERSION}")
    else: message(f"Welcome Developer LES:Over Version:{VERSION}")

    try: sleep_time = int(input("Enter sleep time between two message: \n"))
    except:
        error("Entered value must contain numbers only.")
        sys.exit(0)
    warn("For stop, press CTRL + C")
    main(sleep_time)