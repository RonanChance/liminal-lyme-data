import json
import pprint
import operator
import os
import fileinput

# Define the directory where your files are located
directory_path = "./TheEye/extracted/"
reading_filenames = sorted(list(set([f.split("_")[0] for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))])), key=lambda x: x.lower())

print(reading_filenames)


# file = fileinput.input("mydatav2.json", encoding="utf-8")

myset = set()

shortest_sentence = 99999

with open('mydatav2.json', 'r', encoding="utf-8") as json_file:
    data = json.load(json_file)
    for item in data:
        for tag in item["tags"]:
            myset.add(tag)
        
        shortest_sentence = min(shortest_sentence, len(item["body"]))
        # check length of sentences
print(myset)
print("shortest sentence:", shortest_sentence)