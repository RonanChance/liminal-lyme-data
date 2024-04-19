import fileinput
import json
import datetime
import os
import re
import time
start_time = time.time()

mapping = {

    "post treatment lyme disease": "Lyme Disease",
    "post lyme disease syndrome": "Lyme Disease",
    "lyme neuroborreliosis": "Lyme Disease",
    "chronic lyme disease": "Lyme Disease",
    "neuroborreliosis": "Lyme Disease",
    "lyme's disease": "Lyme Disease",
    "lyme diseases": "Lyme Disease",
    "chronic lymes": "Lyme Disease",
    "lymes disease": "Lyme Disease",
    "chronic lymie": "Lyme Disease",
    "chronic lyme": "Lyme Disease",
    "lyme disease": "Lyme Disease",
    "burgdorferi": "Lyme Disease",
    "burgderfori": "Lyme Disease", # common misspelling
    "borreliosis": "Lyme Disease",
    "burgdoferi": "Lyme Disease", # common misspelling
    "borrelia": "Lyme Disease",
    "borelia": "Lyme Disease", # common misspelling
    "borreli": "Lyme Disease",
    "lymie": "Lyme Disease",
    "ptlds": "Lyme Disease",
    " lyme": "Lyme Disease",

    "rocky mountain spotted fever": "RMSF & Rickettsia",
    "rocky mt. spotted fever": "RMSF & Rickettsia",
    "rocky mt spotted fever": "RMSF & Rickettsia",
    "rocky mountain spot": "RMSF & Rickettsia",
    "rickettsiosis": "RMSF & Rickettsia",
    "rickettsial": "RMSF & Rickettsia",
    "rickettsia": "RMSF & Rickettsia",
    "rickettsi": "RMSF & Rickettsia",
    "rickestta": "RMSF & Rickettsia",
    "rmsf": "RMSF & Rickettsia",

    "phagocytophilum": "Anaplasmosis",
    "anaplasmosis": "Anaplasmosis",
    "anaplasma": "Anaplasmosis",
    "anaplas": "Anaplasmosis",

    "tick borne relapsing fever": "Relapsing Fever",
    "tick-borne relapsing fever": "Relapsing Fever",
    "tickborne relapsing fever": "Relapsing Fever",
    "borrelia miyamotoi": "Relapsing Fever",
    "borrelia miyamoti": "Relapsing Fever",
    "borrelia hermsii": "Relapsing Fever",
    "relapsing fever": "Relapsing Fever",
    "tbrf": "Relapsing Fever",

    "babesia microti": "Babesiosis",
    "babesia duncani": "Babesiosis",
    "babesiosis": "Babesiosis",
    "babesiosa": "Babesiosis",
    "babesia": "Babesiosis",
    "babesi": "Babesiosis",

    "bartonellosis": "Bartonellosis",
    "bartonelosis": "Bartonellosis",
    "bartonella": "Bartonellosis",
    "bartonela": "Bartonellosis",
    "bartone": "Bartonellosis",
    " bart ": "Bartonellosis",

    "mycoplasmia": "Mycoplasma", # this isn't the typical spelling, but might catch mistakes
    "mycoplasma": "Mycoplasma",

    "ehrlichiosis": "Ehrlichiosis",
    "ehrlichia": "Ehrlichiosis",
    "ehrlich": "Ehrlichiosis",

    "tularemia": "Tularemia",
    "tulare": "Tularemia",

    "toxoplasma gondii": "Toxoplasmosis",
    "toxoplasmosis": "Toxoplasmosis",
    "toxoplasm": "Toxoplasmosis",
    "gondii": "Toxoplasmosis",

    "tick-borne encephalitis": "Tickborne Encephalitis (TBE)",
    "tick borne encephalitis": "Tickborne Encephalitis (TBE)",
    "tickborne encephalitis": "Tickborne Encephalitis (TBE)",

}

def format_and_store(filename, json_dict, comment_flag):
    # 0 = submissions, 1 = comments
    if comment_flag:
        body = json_dict['body']
    else:
        body = json_dict['selftext']

    # TODO: 100 seems reasonable for now since we want only substantial content... let's look into a more mathematical way to determine this threshold
    if len(body) <= 100:
        return

    body_lower = body.lower()
    
    # get rid of posts not talking about personal experience
    relevance_strings = ["i had", "i have", "i contracted"]
    if not any(string in body_lower for string in relevance_strings):
        return
    
    # get rid of posts that are slander
    if "quack" in body_lower:
        return

    if comment_flag:
        permalink = "https://www.reddit.com/r/" + json_dict['subreddit'] + "/" + json_dict['link_id']
    else:
        permalink = "https://www.reddit.com" + json_dict['permalink']

    try:
        score = json_dict['score']
    except Exception:
        score = json_dict.get('ups', 'N/A')
    
    entry_dict = {
            "keyid": json_dict['id'],
            "author": json_dict['author'],
            "score": score,
            "date": str(datetime.datetime.fromtimestamp(int(json_dict['created_utc']))),
            "permalink": permalink,
            "subreddit": json_dict['subreddit'],
            "conditions": [],
            "medications": [],
            "supplements": [],
            "body": body
        }

    for cond in sorted([item.lower() for item in mapping.keys()], key=len, reverse=True):
        if cond in body_lower:
            # get rid of lymecycline miscategorization
            if cond == " lyme":
                if " lyme" in body_lower.replace("lymecycline", " "):
                    pattern = re.compile(r"(?<!>)" + re.escape("lyme"), re.IGNORECASE)
                    entry_dict["body"] = pattern.sub('<span class="'+ "emyl-" + " condition" + '" style="background-color: var(--condition_highlight); border-radius: 3px;">lyme</span>', entry_dict["body"])
                else:
                    continue
            else:
                pattern = re.compile(r"(?<!>)" + re.escape(cond), re.IGNORECASE)
                entry_dict["body"] = pattern.sub('<span class="' + cond[::-1].replace(" ", "-") + " condition" + '" style="background-color: var(--condition_highlight); border-radius: 3px;">' + cond + '</span>', entry_dict["body"])

            # add to medication list, then highlight the relevant text
            if mapping[cond] not in entry_dict["conditions"]:
                entry_dict["conditions"].append(mapping[cond])

    if not len(entry_dict["conditions"]):
        return
    
    with open(filename, "a") as json_file:
        json_file.write(json.dumps(entry_dict))
        json_file.write("\n")
    json_file.close()

directory_path = "./TheEye/extracted/"
reading_filenames = [directory_path+f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
writing_filename = "mydatav1.jsonl"

try:
    os.remove('mydatav1.jsonl')
except Exception:
    pass

i = 0
for reading_filename in reading_filenames:
    file = fileinput.input(reading_filename, encoding="utf-8")
    
    for line in file:
        json_line = json.loads(line)
        
        comment_flag = 0
        if "comment" in reading_filename:
            comment_flag = 1

        format_and_store(writing_filename, json_line, comment_flag)
        i += 1
        if (i % 100000 == 0):
            print(i)

    file.close()

elapsed_time = time.time() - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)
print(f"Elapsed time: {minutes} minutes {seconds} seconds")