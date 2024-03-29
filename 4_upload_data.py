import json
import fileinput
from pocketbase import PocketBase
import os
from dotenv import load_dotenv
load_dotenv()

client = PocketBase('http://127.0.0.1:8090')
admin_data = client.admins.auth_with_password(os.getenv('SECRET_EMAIL'), os.getenv('SECRET_PASSWORD'))

file = fileinput.input("mydatav2.json", encoding="utf-8")
data = [json.loads(line) for line in file]

i = 0
for dictionary in data:
    try:
        result = client.collection("posts").create(dictionary)
    except Exception:
        print(dictionary)
        exit()

    i += 1
    if (i % 100 == 0):
        print(i)