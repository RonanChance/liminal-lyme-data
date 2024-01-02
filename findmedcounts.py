import drugstandards as ds
import sys
import nltk
from nltk.corpus import stopwords
import fileinput
import json
import string
from collections import Counter


with open('mydatav2.json', 'r', encoding="utf-8") as json_file:
    data = json.load(json_file)

all_tags = []

i = 0
for dictionary in data:
    for item in dictionary["tags"]:
        all_tags.append(item)

results = Counter(all_tags)

# Filter items with at least 30 occurrences and store them in a list
# filtered_results = [item.upper() for item, count in results.items() if count >= 20]
filtered_results_with_count = result_dict = {item.upper(): count for item, count in results.items() if count >= 9}

print("\n viable tags \n")
print(", ".join(sorted(list(filtered_results_with_count.keys()))))

print("\n number of viable tags \n")
print(len(filtered_results_with_count))

# print dictionary so that we can include counts in website
print("\n mapping \n")
print(dict(sorted(filtered_results_with_count.items(), key=lambda x: x[1], reverse=True)))

print("\n only medications \n")
mapping = {
    "anaplas": "ANAPLASMOSIS",
    "babesia": "BABESIOSIS",
    "babesio" : "BABESIOSIS",
    "bartone": "BARTONELLOSIS",
    "ehrlich": "EHRLICHIOSIS",
    "tulare": "TULAREMIA",
    "rmsf": "ROCKY MOUNTAIN SPOTTED FEVER",
    "rocky mountain spot": "ROCKY MOUNTAIN SPOTTED FEVER", 
    "rickettsi" : "ROCKY MOUNTAIN SPOTTED FEVER",
    "lyme": "LYME DISEASE",
    "borrelia" : "LYME DISEASE",
    "borrelio" : "LYME DISEASE",
    "burgdorferi" : "LYME DISEASE"
}
print(sorted([item for item in filtered_results_with_count if item not in mapping.values() and item != "ALL CONDITIONS (ANY)"]))

print("\n only conditions \n")
print(sorted(list(set(list(mapping.values()) + ["ALL CONDITIONS (ANY)"]))))

print("\n viable tags for upload \n")
print(list(filtered_results_with_count.keys()))

# print("\n Results \n")
# print(sorted(filtered_results))
# print("\n Unformated \n")
# print(', '.join(sorted(filtered_results)))
# print("\n Length \n")
# print(len(filtered_results))