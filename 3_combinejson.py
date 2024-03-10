import json


with open("mydatavmed.json", 'r', encoding="utf-8") as json_file:
    data_med = json.load(json_file)

with open("mydatavsupp.json", 'r', encoding="utf-8") as json_file:
    data_supp = json.load(json_file)

def format_file(filename, start):
    if start:
        with open(filename, "w") as json_file:
            json_file.write("[\n")
        json_file.close()
    else:
        with open(filename, "a") as json_file:
            json_file.write("]")
        json_file.close()

format_file("mydatav3.json", start=True)


for med_dict in data_med:
    identified = False
    for supp_dict in data_supp:
        if med_dict['keyid'] == supp_dict['keyid']:
            identified = True
            # Merge the supplements
            med_dict['supplements'] = supp_dict['supplements']
            # Write merged data to file
            with open("mydatav3.json", "a") as json_file:
                json_file.write(json.dumps(med_dict))
                json_file.write(",\n")
                json_file.close()
            break
    if not identified:
        # If med_dict doesn't have corresponding supp_dict, write med_dict to file
        with open("mydatav3.json", "a") as json_file:
            json_file.write(json.dumps(med_dict))
            json_file.write(",\n")
            json_file.close()

# Write remaining supp_dicts that are not in med_dicts to the file
for supp_dict in data_supp:
    if not any(med_dict['keyid'] == supp_dict['keyid'] for med_dict in data_med):
        with open("mydatav3.json", "a") as json_file:
                json_file.write(json.dumps(supp_dict))
                json_file.write(",\n")
                json_file.close()

# for supp_dict in data_supp:
#     identified = False
#     for med_dict in data_med:
#         if med_dict['keyid'] == supp_dict['keyid']:
#             identified = True
#             # add the supplements here
#             med_dict['supplements'] = supp_dict['supplements']
            
#             with open("mydatav3.json", "a") as json_file:
#                 json_file.write(json.dumps(med_dict))
#                 json_file.write(",\n")
#                 json_file.close()
    
#     if not identified:
#         with open("mydatav3.json", "a") as json_file:
#                 json_file.write(json.dumps(supp_dict))
#                 json_file.write(",\n")
#                 json_file.close()
        
format_file("mydatav3.json", start=False)