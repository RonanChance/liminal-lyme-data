import drugstandards as ds
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

supplement_file = fileinput.input("supplements.txt", encoding="utf-8")
supplement_list = []
for line in supplement_file:
    supplement_list.append(line.strip().lower().split(", "))

sys.stdout.reconfigure(encoding='utf-8')
# nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

# create standardizer object
s = ds.DrugStandardizer()
term_cores = ['x', 'y', 'z', 'cill', 'cline', 'cin', 'tria', 'ox', 'sulf', 'anta', 'mepro', 'ectin']

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

    filtered_words_list = [word for word in body
                      .replace(" im "," ")
                      .replace("."," ")
                      .replace("!"," ")
                      .replace(",", " ")
                      .replace("?"," ")
                      .replace("("," ")
                      .replace(")", " ")
                      .replace("’", "")
                      .replace("&amp;#x200b;", " ")
                      .replace("\"", " ")
                      .replace("/", " ")
                      .replace("\'", " ")
                      .replace("=", " ")
                      .replace("*", "")
                      .split() if word.lower() not in stop_words]
    
    filtered_words = " ".join(filtered_words_list)
    
    # Identify medications
    for word in filtered_words_list:
        if any(w in word for w in term_cores):
                standardized_med = s.standardize([word], thresh=0.99)[0]
                if standardized_med:
                    print(word, standardized_med)

                    pattern = re.compile(r"(?<!>)" + re.escape(word), re.IGNORECASE)
                    dictionary["body"] = pattern.sub('<span style="background-color: #0000ff33">' + word + '</span>', dictionary["body"])          
          
                    if standardized_med not in dictionary["medications"]:
                        dictionary["medications"].append(standardized_med)
    
    # Identify supplements
    for item in supplement_list:
        # reverse to get which words to avoid first
        for idx, word in enumerate(item[::-1]):
            avoid_matching = []
            if "!" in word:
                avoid_matching.append(word[1:])
            else:   
                # make sure our term is in the filtered data, and NONE of the terms to avoid are there
                if (word.lower() + " " in filtered_words.lower()) and (not any(w in filtered_words for w in avoid_matching)):
                    # skip the blank space now, and risk it. #TODO: improve this
                    
                    # this should solve duplicate issue, check again later
                    pattern = re.compile(r"(?<!>)" + re.escape(word), re.IGNORECASE)
                    dictionary["body"] = pattern.sub('<span style="background-color: #00ff0033">' + word + '</span>', dictionary["body"])

                    if item[0].upper() not in dictionary["supplements"]:
                        dictionary["supplements"].append(item[0].upper())
                        total_results_list.append(item[0].upper())
    
    # if there's at least some medication or supplement, store it
    if (len(dictionary["medications"]) or len(dictionary["supplements"])):
        with open(writing_filename, "a") as json_file:
            json_file.write(json.dumps(dictionary))
            json_file.write(",\n")
        json_file.close()
    
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