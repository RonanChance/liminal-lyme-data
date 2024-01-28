import json

with open('mydatav2.json', 'r', encoding="utf-8") as json_file:
    data = json.load(json_file)

i = 0
for dictionary in data:
    # guarantee the tags are uppercase
    dictionary["tags"] = [term.upper() for term in dictionary["tags"]]

    body = dictionary["body"].lower()
    for word in body.split():
        i += 1

print(i)