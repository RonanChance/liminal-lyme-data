import sys
import nltk
from nltk.corpus import stopwords
import fileinput
import json
import collections
import re
import time
start_time = time.time()

total_results_list = []
total_medications_list = []
total_supplements_list = []

supplement_file = fileinput.input("txts/supplements.txt", encoding="utf-8")
supplement_list = []
for line in supplement_file:
    supplement_list.append(line.strip().lower().split(", "))

medication_file = fileinput.input("txts/medications.txt", encoding="utf-8")
medication_list = []
for line in medication_file:
    medication_list.append(line.strip().lower().split(", "))

sys.stdout.reconfigure(encoding='utf-8')
# nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

def format_file(filename, start):
    if start:
        with open(filename, "w") as json_file:
            json_file.write("[\n")
        json_file.close()
    else:
        with open(filename, "a") as json_file:
            json_file.write("]")
        json_file.close()

reading_filename = "mydatav1.json"
writing_filename = "mydatav2.json"
format_file(writing_filename, start=True)

with open(reading_filename, 'r', encoding="utf-8") as json_file:
    data = json.load(json_file)

i = 0
for dictionary in data:
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    body = url_pattern.sub('', dictionary["body"])

    filtered_words_list = [word.lower() for word in body
                      .replace(' im ',' ')
                      .replace('.',' ')
                      .replace('!',' ')
                      .replace(',', ' ')
                      .replace('?',' ')
                      .replace('(',' ')
                      .replace(')', ' ')
                      .replace('’', '\'')
                      .replace('&amp;#x200b;', ' ')
                      .replace('\"', ' ')
                      .replace('/', ' ')
                    #   .replace('\'', ' ')
                      .replace('=', ' ')
                      .replace('*', ' ')
                      .replace('<', ' ')
                      .replace('>', ' ')
                      .replace('background-color:', ' ')
                      .replace('--condition_highlight', ' ')
                      .split() if word.lower() not in stop_words]
    
    filtered_words = " ".join(filtered_words_list)
    
    # Identify medications
    for item in medication_list:
        # reverse to get which words to avoid first
        for idx, word in enumerate(item[::-1]):
            avoid_matching = []
            if "!" in word:
                avoid_matching.append(word[1:])
            else:   
                # make sure our term is in the filtered data, and NONE of the terms to avoid are there
                if (" " + word + " " in filtered_words.lower()) and (not any(w in filtered_words for w in avoid_matching)):
                    # print(word.upper())
                    # skip the blank space now, and risk it. #TODO: improve this
                    # this should solve duplicate issue, check again later
                    pattern = re.compile(r"(?<!>)" + re.escape(word), re.IGNORECASE)
                    dictionary["body"] = pattern.sub('<span style="background-color: var(--medication_highlight)">' + word + '</span>', dictionary["body"])

                    if item[0].upper() not in dictionary["medications"]:
                        dictionary["medications"].append(item[0].upper())
                        total_results_list.append(item[0].upper())
                        total_medications_list.append(item[0].upper())

    # Identify supplements
    for item in supplement_list:
        # reverse to get which words to avoid first
        for idx, word in enumerate(item[::-1]):
            avoid_matching = []
            if "!" in word:
                avoid_matching.append(word[1:])
            else:
                # make sure our term is in the filtered data, and NONE of the terms to avoid are there
                if (" " + word + " " in filtered_words.lower()) and (not any(w in filtered_words for w in avoid_matching)):
                    # print(word.upper())
                    # skip the blank space now, and risk it. #TODO: improve this
                    # this should solve duplicate issue, check again later
                    pattern = re.compile(r"(?<!>)" + re.escape(word), re.IGNORECASE)
                    dictionary["body"] = pattern.sub('<span style="background-color: var(--supplement_highlight)">' + word + '</span>', dictionary["body"])

                    if item[0].upper() not in dictionary["supplements"]:
                        dictionary["supplements"].append(item[0].upper())
                        total_results_list.append(item[0].upper())
    
    # if there's at least some medication or supplement, store it
    if (len(dictionary["medications"]) or len(dictionary["supplements"])):
        with open(writing_filename, "a") as json_file:
            json_file.write(json.dumps(dictionary))
            json_file.write(",\n")
        json_file.close()

    # if (i == 1436):
    #     print(filtered_words_list)
    #     print("-"*20)
    #     print(filtered_words)
    #     print("-"*20)
    #     print(dictionary["body"])
    #     exit()

    # get an update on how far into the process we are
    i += 1
    if (i % 100 == 0):
        print(i)

format_file(writing_filename, start=False)

for item in collections.Counter(total_results_list).most_common():
    print(item[1], item[0])


elapsed_time = time.time() - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)
print(f"Elapsed time: {minutes} minutes {seconds} seconds")
# print(list(set(total_medications_list)))
# for item in collections.Counter(total_medications_list).most_common():
#     print(item[1], item[0])
# for item in collections.Counter(total_medications_list).most_common():
#     print(item[0])