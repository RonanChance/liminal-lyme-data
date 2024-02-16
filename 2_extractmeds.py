import drugstandards as ds
import sys
import nltk
from nltk.corpus import stopwords
import fileinput
import json
import collections
import re


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

writing_filename = "mydatav2.json"
format_file(writing_filename, start=True)

with open('mydatav1.json', 'r', encoding="utf-8") as json_file:
    data = json.load(json_file)

i = 0
for dictionary in data:
    body = dictionary["body"].lower()
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    body = url_pattern.sub('', body)

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
    
    # print(filtered_words)
    # if i == 9:
    #     exit()
    # print(filtered_words)
    
    # my attempt to speed up the process... brace yourself 
    # for word in filtered_words_list:
    #     for w in term_cores:
    #         if w in word:
    #             standardized_med = s.standardize([word], thresh=0.99)[0]
    #             if standardized_med:
    #                 print(word, standardized_med)
    #                 if standardized_med not in dictionary["medications"]:
    #                     dictionary["medications"].append(standardized_med)
    
    # TODO: handle some edge cases, for ex. rmsf in url link
    for item in supplement_list:
        for idx, word in enumerate(item):
            word = word.lower() + " "
            if word in filtered_words:
                print(word)
                
                index = filtered_words.index(word)
                print(filtered_words[index:index + len(word) + 30])
                
                if item[0].upper() not in dictionary["supplements"]:
                    dictionary["supplements"].append(item[0].upper())
                    total_results_list.append(item[0].upper())
    
    
    if (len(dictionary["medications"]) or len(dictionary["supplements"])):
        
        print(dictionary["medications"], dictionary["supplements"])

        with open(writing_filename, "a") as json_file:
            json_file.write(json.dumps(dictionary))
            json_file.write(",\n")
        json_file.close()
    
    i += 1
    if (i % 100 == 0):
        print(i)

format_file(writing_filename, start=False)

print(collections.Counter(total_results_list).most_common())