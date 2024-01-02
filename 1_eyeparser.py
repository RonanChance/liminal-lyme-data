import fileinput
import json
import datetime
import os

key_cond = ["lyme", "babesia", "babesio", "bartone", "rmsf", "rocky mountain spot", "rickettsi", "borrelia", "borrelio", "burgdorferi", "anaplas", "ehrlich", "tulare"]
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

term_count_cond = {term: 0 for term in key_cond}

def format_file(filename, start):
    if start:
        with open(filename, "w") as json_file:
            json_file.write("[")
        json_file.close()
    else:
        with open(filename, "a") as json_file:
            json_file.write("]")
        json_file.close()

def count_tags(post):
    for term in key_cond:
        if term in post["body"]:
            term_count_cond[term] += 1

def format_and_store(filename, json_dict):
    try:
        body = json_dict['body']
    except Exception:
        body = json_dict['selftext']
        pass
    body_lower = body.lower()

    try:
        permalink = "https://www.reddit.com" + json_dict['permalink']
    except Exception:
        permalink = "https://www.reddit.com/r/" + json_dict['subreddit'] + "/" + json_dict['link_id']

    try:
        score = json_dict.get('score')
    except Exception:
        score = json_dict.get('ups', 'N/A')

    # 50 seems reasonable, but look into a more mathematical way to determine this
    if len(body_lower) <= 50:
        return

    # get rid of posts not talking about personal experience
    relevance_strings = ["i had", "i have", "i contracted"]
    if all(string not in body_lower for string in relevance_strings):
        return
    if "quack" in body_lower:
        return
    
    entry_dict = {
            "keyid": json_dict['id'],
            "author": json_dict['author'],
            "score": score,
            "date": str(datetime.datetime.fromtimestamp(int(json_dict['created_utc']))),
            "permalink": permalink,
            "subreddit": json_dict['subreddit'],
            "tags": [],
            "body": body
        }

    for cond in key_cond:
        if cond in body_lower:
            # get rid of lymecycline conflict
            if cond == "lyme":
                if "lyme" in body_lower.replace("lymecycline", " "):
                    entry_dict["tags"].append(mapping[cond])
                else:
                    continue
            else:
                entry_dict["tags"].append(mapping[cond])
            # add the any attribute now that we know there's at least one cond
            if "ALL CONDITIONS (ANY)" not in entry_dict["tags"]:
                entry_dict["tags"].append("ALL CONDITIONS (ANY)")

    if not len(entry_dict["tags"]):
        return
    
    with open(filename, "a") as json_file:
        json_file.write(json.dumps(entry_dict))
        json_file.write(",\n")
    json_file.close()



directory_path = "./TheEye/extracted/"
reading_filenames = [directory_path+f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
writing_filename = "mydatav1.json"

format_file(writing_filename, start=True)

i = 0
for reading_filename in reading_filenames:
    file = fileinput.input(reading_filename, encoding="utf-8")
    
    for line in file:
        json_line = json.loads(line)
        format_and_store(writing_filename, json_line)
        i += 1
        if (i % 1000 == 0):
            print(i)

    file.close()

format_file(writing_filename, start=False)

