import requests
import secrets
import json
import calendar
import time as t

SECURITY_HASH = "C7E876AD26C4BBF271A22CF89E94D3D2A01B4C31CE91E08E894CFCA83C1F4D5DE35512F7202A8AA16EBF0FB8D6B360B55AC23C3A67D9B0516C8AA18047BC990D"

create_url = "https://www.tnycl.net/lesover/create.php"
one_month_timestamp = 2678400

username = input("Username: ")
time = int(input("Time(Month): "))
discord = input("Discord: ")

timestamp = calendar.timegm(t.gmtime())
deadline = (time*one_month_timestamp)+timestamp
token = secrets.token_urlsafe(12)

sent = {"username": username, "token": token, "deadline": deadline, "discord": discord, "security_hash": SECURITY_HASH}
response = requests.post(url=create_url, params=sent)
incoming = json.loads(response.text)

print(incoming['message'] + token)