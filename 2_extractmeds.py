import sys
import nltk
from nltk.corpus import stopwords
import fileinput
import json
import string
print(sys.path)
sys.path.append("\\drugstandards")
# print(sys.path)
import drugstandards as ds

sys.stdout.reconfigure(encoding='utf-8')
# nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

# create standardizer object
s = ds.DrugStandardizer()
term_cores = ['x', 'y', 'z', 'cill', 'cline', 'cin', 'tria', 'ox', 'sulf', 'anta', 'mepro']

def format_file(filename, start):
    if start:
        with open(filename, "w") as json_file:
            json_file.write("[")
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
    # print(dictionary)
    body = dictionary["body"].lower()
    # result = client.collection("posts").create(dictionary)
    filtered_words = [word for word in body.replace(" im ","").replace(".","").replace("!","").split() if word.lower() not in stop_words]
    # my attempt to speed up the process... brace yourself 
    for word in filtered_words:
        for w in term_cores:
            if w in word:
                standardized_med = s.standardize([word], thresh=0.99)[0]
                if standardized_med:
                    print(word, standardized_med)
                    if standardized_med not in dictionary["tags"]:
                        dictionary["tags"].append(standardized_med)
                        if "All MEDICATIONS (ANY)" not in dictionary["tags"]:
                            dictionary["tags"].append("All MEDICATIONS (ANY)")
    
    if "All MEDICATIONS (ANY)" in dictionary["tags"]:
        with open(writing_filename, "a") as json_file:
            json_file.write(json.dumps(dictionary))
            json_file.write(",\n")
        json_file.close()
    
    i += 1
    if (i % 100 == 0):
        print(i)

format_file(writing_filename, start=False)