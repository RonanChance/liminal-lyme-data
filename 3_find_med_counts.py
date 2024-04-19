import json
from collections import Counter
import fileinput

file = fileinput.input("mydatav2.jsonl", encoding="utf-8")
data = [json.loads(line) for line in file]

constants_file = open("constants.txt", "w")

con_tags = []
all_tags = []
all_tags_labeled = []
med_tags = []
sup_tags = []
username_list = []

i = 0
for dictionary in data:
    if (dictionary["author"] != '[deleted]'):
        username_list.append(dictionary["author"])
    for item in dictionary["conditions"]:
        con_tags.append(item)
    for item in dictionary["medications"]:
        all_tags.append(item)
        med_tags.append(item)
    for item in dictionary["supplements"]:
        all_tags.append(item)
        sup_tags.append(item)

# All conditions
results = Counter(con_tags)
all_con_count = {item: count for item, count in results.items()}
# print("export const illnesses =", [item for item, count in sorted(all_con_count.items(), key=lambda x: x[1], reverse=True)])
constants_file.write("export const illnesses = " + str([item for item, count in sorted(all_con_count.items(), key=lambda x: x[1], reverse=True)]))
print(", ".join([item for item, count in sorted(all_con_count.items(), key=lambda x: x[1], reverse=True)]))

# All Medications
results = Counter(med_tags)
all_med_count = {item: count for item, count in results.items()}
# print("export const medications =", [item for item, count in sorted(all_med_count.items(), key=lambda x: x[1], reverse=True)])
constants_file.write("\n" + "export const medications = " + str([item for item, count in sorted(all_med_count.items(), key=lambda x: x[1], reverse=True)]))
print("\n" + ", ".join([item for item, count in sorted(all_med_count.items(), key=lambda x: x[1], reverse=True)]))
# MAKING medications.txt, 
# alphabetized = sorted([item for item, count in all_med_count.items()])
# for item in alphabetized:
#     print(item)
# print(len(all_med_count))

# All Supplements
results = Counter(sup_tags)
all_sup_count = {item: count for item, count in results.items()}
# print("export const supplements =", [item for item, count in sorted(all_sup_count.items(), key=lambda x: x[1], reverse=True)])
constants_file.write("\n" + "export const supplements = " + str([item for item, count in sorted(all_sup_count.items(), key=lambda x: x[1], reverse=True)]))
print("\n" + ", ".join([item for item, count in sorted(all_sup_count.items(), key=lambda x: x[1], reverse=True)]))
# print(len(all_sup_count))


##################################

# All tags (Med + Sup)
results = Counter(all_tags)
all_results_count = {item: count for item, count in results.items()}
# print("export const all_tags =", [item for item, count in sorted(all_results_count.items(), key=lambda x: x[1], reverse=True)])
constants_file.write("\n" + "export const all_tags = " + str([item for item, count in sorted(all_results_count.items(), key=lambda x: x[1], reverse=True)]))


# All tags w/ Count and label (Med + Sup)
# results = Counter(all_tags)
all_results_count = {item: count for item, count in results.items()}
all_results_labeled = {}
for item in all_results_count:
    if item in med_tags:
        all_results_labeled[item] = {"count": all_results_count[item], "label": "MED"}
    if item in sup_tags:
        all_results_labeled[item] = {"count": all_results_count[item], "label": "SUP"}

sorted_labeled_results = dict(sorted(all_results_labeled.items(), key=lambda x: x[1]["count"], reverse=True))
# print("export const tag_counts =", sorted_labeled_results)
constants_file.write("\n" + "export const tag_counts = " + str(sorted_labeled_results))


# Med Counts
results = Counter(med_tags)
# print("export const med_counts =", dict(sorted(results.items(), key=lambda x: x[1], reverse=True)))
constants_file.write("\n" + "export const med_counts = " + str(dict(sorted(results.items(), key=lambda x: x[1], reverse=True))))

# Sup Counts
results = Counter(sup_tags)
# print("export const sup_counts =", dict(sorted(results.items(), key=lambda x: x[1], reverse=True)))
constants_file.write("\n" + "export const sup_counts = " + str(dict(sorted(results.items(), key=lambda x: x[1], reverse=True))))


results = Counter(username_list)
print("\n" + "export const chronology_usernames = " + str(dict([(item, count) for item, count in sorted(results.items(), key=lambda x: x[1], reverse=True) if count > 1])))
constants_file.write("\n" + "export const chronology_usernames = " + str(dict([(item, count) for item, count in sorted(results.items(), key=lambda x: x[1], reverse=True) if count > 1])))
