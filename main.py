from asyncio.windows_events import NULL
import requests
import json
import random
import sys
import os
import time
import subprocess
from colorama import Fore, Back, Style
from utils import *
import calendar
import time

#https://discord.com/api/v9/channels/917792877302648844/messages?limit=50

DEBUG = True
VERSION = "1.0.0"
SECURITY_HASH = "C7E876AD26C4BBF271A22CF89E94D3D2A01B4C31CE91E08E894CFCA83C1F4D5DE35512F7202A8AA16EBF0FB8D6B360B55AC23C3A67D9B0516C8AA18047BC990D"
TOKEN_VALIDATED = False

settings_path = "settings.json"
validate_url = "https://www.tnycl.net/lesover/validate.php"

def success(message):
    print(Fore.BLACK + Back.GREEN + "SUCCESS:" + Style.RESET_ALL + " " + message + Fore.RESET)

def warn(message):
    print(Fore.YELLOW + "+:" + Style.RESET_ALL + " " + message + Fore.RESET)

def error(message, exit):
    print(Back.RED + Fore.BLACK + "ERROR:" +
          Fore.RED + Back.RESET + " " + message + Fore.RESET)
    if exit:
        input("")
        sys.exit(0)

def message(message):
    print(Fore.LIGHTCYAN_EX + "-> " + Fore.RESET + message)

send_count = 1
reply_rate = 10
texts = []
tokens = []
channels = []

def main():
    print(Fore.LIGHTBLACK_EX + "  0. Exit")
    print(Fore.CYAN + "  1. Message")
    print(Fore.CYAN + "  2. Invite")
    try:
        operation = int(input(Fore.RESET + "\n  Select an option: "))
        if(operation == 0):
            message("Good bye")
        elif(operation == 1):
            message("\n ")
    except:
        error("Wrong option.\n\n", False)
        main()

def loop_message(sleep_time):
    global send_count
    get_texts()
    get_tokens()
    get_channels()
    while True:
        time.sleep(sleep_time)
        for token in tokens:
            for channel_id in channels:
                text = texts[random.randrange(0, len(texts))]
                if send_count % reply_rate != 0:
                    send_message(
                        token,
                        channel_id,
                        text,
                        False,
                        None
                    )
                else:
                    history = json.loads(reply(token, channel_id))
                    selected_message = history[random.randrange(0, 10)]
                    send_message(
                        token,
                        channel_id,
                        text,
                        True,
                        selected_message["id"]
                    )
            send_count+=1

def reply(token, channel_id):
    headers = {
    'Content-type': 'application/json',
    'authorization': token,
    }
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=50"
    try:
        response = requests.get(url=url, headers=headers)
        return response.text
    except Exception as ex:
        print(ex)
    return None

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

def save_token(token):
    with open(settings_path, "w+") as file:
        file.write('{"token": "'+token+'"}')

def get_token():
    if not os.path.exists(settings_path): return None
    with open(settings_path, 'r') as file:
        return json.load(file)['token']

def validate_token(token):
    sent = {"token": token, "security_hash": SECURITY_HASH, "hwid": get_hwid(), "timestamp": calendar.timegm(time.gmtime())}
    response = requests.post(url=validate_url, params=sent)
    incoming = json.loads(response.text)

    global TOKEN_VALIDATED
    TOKEN_VALIDATED = incoming['status']

    if incoming['error'] == 2 and TOKEN_VALIDATED:
        error(incoming['message'], True)

    if incoming['error'] == 3 and TOKEN_VALIDATED:
        error(incoming['message'], True)

    if TOKEN_VALIDATED:
        save_token(token)
        message(incoming['message'])
    else: 
        error(incoming['message'], True)

def get_hwid():
    return str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()

def send_message(token, channel_id, content, is_reply, message_id):
    count = random.randint(5000, 99999999)
    headers = {
    'Content-type': 'application/json',
    'authorization': token,
    }
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    try:
        if not is_reply:
            data = {"content":f"{content}","nonce":count,"tts":False}
        else:
            data = {"content":f"{content}","nonce":count,"tts":False,"message_reference":{"channel_id":channel_id,"message_id":message_id}}
        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        if not is_reply:
            message(f"[{send_count}] Message Sent: {Fore.LIGHTGREEN_EX + content}")
        else:
            message(f"[{send_count}] Reply Sent: {Fore.LIGHTGREEN_EX + content}")
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    if not DEBUG: message(f"Welcome LES:Over Version:{VERSION}\n")
    else: 
        message(f"(Dev) LES:Over Version: {VERSION}")
        message(f"Secure Hash: {SECURITY_HASH}\n")

    if get_token() == None:
        token = input("\nEnter your token: ")
        validate_token(token)
    else:
        validate_token(get_token())

    if TOKEN_VALIDATED:
        try: sleep_time = int(input("\nEnter sleep time between two message: \n"))
        except:
            error("Entered value must contain numbers only.")
        warn("For stop, press X")
        loop_message(sleep_time)