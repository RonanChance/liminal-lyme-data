import fileinput
import json
import datetime
import os
import pprint
import operator

directory_path = "./TheEye/extracted/"
reading_filenames = [directory_path+f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
writing_filename = "mydata.json"

key_meds = ["abx", 
            "antibiotic", 
            "doxy", 
            "amoxi", 
            "ceftriax", 
            "azithro", 
            "cefuroxime", 
            "ceftin", 
            "cefdinir", 
            "omnicef", 
            "rocephin", 
            "penicillin", 
            "rifampin", 
            "erythro", 
            "minocycline", 
            "clarithro", 
            "biaxin", 
            "cipro", 
            "septra", 
            "sulfamethoxazole", 
            "trimethoprim",
            "flagyl",
            "metronidazole",
            "atovaquone",
            "mepron",
            "augmentin",
            "tobramycin",
            "cefotaxime",
            "claforan",
            "tigecycline",
            "tygacil",
            "moxifloxacin",
            "avelox"
        ]
# key_cond = ["lyme", "babesia", "bart", "rmsf", "rocky mountain spot", "rickettsia", "borrelia", "burgdorferi"]

term_count_meds = {term: 0 for term in key_meds}
# term_count_cond = {term: 0 for term in key_cond}

def count_tags(post):
    try:
        body = post['body']
    except Exception:
        body = post['selftext']
        pass
    
    for term in key_meds:
        if term in body:
            term_count_meds[term] += 1
    # for term in key_cond:
    #     if term in body:
    #         term_count_cond[term] += 1

i = 0
for reading_filename in reading_filenames:
    file = fileinput.input(reading_filename, encoding="utf-8")
    for line in file:
        # json_line = json.loads(line)
        
        # count_tags(json_line)
        i += 1
        if (i % 1000 == 0):
            print(i)
    file.close()

print("\n")
# pprint.pprint(sorted(term_count_meds.items(), key=operator.itemgetter(1), reverse=True))

print(i)