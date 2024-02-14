import fileinput
import json
import datetime
import os

key_cond = ["lyme", "babesi", "bartone", "rmsf", "rocky mountain spot", "rickettsi", "borreli", "burgdorferi", "anaplas", "ehrlich", "tulare"]
mapping = {
    "anaplas": "ANAPLASMOSIS",
    "babesi": "BABESIOSIS",
    "bartone": "BARTONELLOSIS",
    "ehrlich": "EHRLICHIOSIS",
    "tulare": "TULAREMIA",
    "rmsf": "ROCKY MOUNTAIN SPOTTED FEVER",
    "rocky mountain spot": "ROCKY MOUNTAIN SPOTTED FEVER", 
    "rickettsi" : "ROCKY MOUNTAIN SPOTTED FEVER",
    "lyme": "LYME DISEASE",
    "borreli" : "LYME DISEASE",
    "burgdorferi" : "LYME DISEASE"
}

def format_file(filename, start):
    if start:
        with open(filename, "w") as json_file:
            json_file.write("[\n")
        json_file.close()
    else:
        with open(filename, "a") as json_file:
            json_file.write("]")
        json_file.close()

def format_and_store(filename, json_dict, comment_flag):
    # 0 = submissions, 1 = comments
    if comment_flag:
        body = json_dict['body']
    else:
        body = json_dict['selftext']

    # TODO: 80 seems reasonable for now since we want only substantial content... let's look into a more mathematical way to determine this threshold
    if len(body) <= 80:
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

    for cond in key_cond:
        if cond in body_lower:
            # get rid of lymecycline miscategorization
            if cond == "lyme":
                if "lyme" in body_lower.replace("lymecycline", " "):
                    entry_dict["conditions"].append(mapping[cond])
                else:
                    continue
            else:
                entry_dict["conditions"].append(mapping[cond])
            # add the any attribute now that we know there's at least one condition
            # TODO: remove this comment if improved solution works
            # if "ALL CONDITIONS (ANY)" not in entry_dict["conditions"]:
                # entry_dict["tags"].append("ALL CONDITIONS (ANY)")

    if not len(entry_dict["conditions"]):
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
        
        comment_flag = 0
        if "comment" in reading_filename:
            comment_flag = 1

        format_and_store(writing_filename, json_line, comment_flag)
        i += 1
        if (i % 100000 == 0):
            print(i)

    file.close()

format_file(writing_filename, start=False)

