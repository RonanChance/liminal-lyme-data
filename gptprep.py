import json

def clean_text(text):
    # Remove non-printable characters and control characters
    cleaned_text = ''.join(char for char in text if 32 <= ord(char) <= 126)
    return cleaned_text

with open('mydatav2.json', 'r', encoding="utf-8") as json_file:
    data = json.load(json_file)

for idx, dictionary in enumerate(data):
    if idx < 1000:
        filenum = 1
    elif idx < 2000:
        filenum = 2
    elif idx < 3000:
        filenum = 3
    elif idx < 4000:
        filenum = 4
    elif idx < 5000:
        filenum = 5
    elif idx < 6000:
        filenum = 6
    
    with open("./files/" + str(filenum) + ".csv", "a", encoding='utf-8') as chatgpt_file:
        try: 
            chatgpt_file.write(clean_text(dictionary['body']) + "\n")
            print(clean_text(dictionary['body']))
        except Exception:
            print("FOUND SOMETHING")
            exit()
            continue
        