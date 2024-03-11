import json
from pocketbase import PocketBase

client = PocketBase('http://127.0.0.1:8090')

with open('mydatav2.json', 'r', encoding="utf-8") as json_file:
    data = json.load(json_file)

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