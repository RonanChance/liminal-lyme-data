import json
from collections import Counter

with open('mydatav2.json', 'r', encoding="utf-8") as json_file:
    data = json.load(json_file)

con_tags = []
all_tags = []
all_tags_labeled = []
med_tags = []
sup_tags = []

i = 0
for dictionary in data:
    for item in dictionary["conditions"]:
        con_tags.append(item)
    for item in dictionary["medications"]:
        all_tags.append(item)
        med_tags.append(item)
    for item in dictionary["supplements"]:
        all_tags.append(item)
        sup_tags.append(item)


# All conditions
# results = Counter(con_tags)
# all_con_count = {item.upper(): count for item, count in results.items()}
# print("export const illnesses =", [item for item, count in sorted(all_con_count.items(), key=lambda x: x[1], reverse=True)])

# All Medications
# results = Counter(med_tags)
# all_med_count = {item.upper(): count for item, count in results.items()}
# print("export const medications =", [item for item, count in sorted(all_med_count.items(), key=lambda x: x[1], reverse=True)])

# All Supplements
# results = Counter(sup_tags)
# all_sup_count = {item.upper(): count for item, count in results.items()}
# print("export const supplements =", [item for item, count in sorted(all_sup_count.items(), key=lambda x: x[1], reverse=True)])



##################################

# All tags (Med + Sup)
# results = Counter(all_tags)
# all_results_count = {item.upper(): count for item, count in results.items()}
# print("export const all_tags =", [item for item, count in sorted(all_results_count.items(), key=lambda x: x[1], reverse=True)])

# All tags w/ Count and label (Med + Sup)
results = Counter(all_tags)
all_results_count = {item.upper(): count for item, count in results.items()}
all_results_labeled = {}
for item in all_results_count:
    if item in med_tags:
        all_results_labeled[item] = {"count": all_results_count[item], "type": "MED"}
    if item in sup_tags:
        all_results_labeled[item] = {"count": all_results_count[item], "type": "SUP"}

sorted_labeled_results = dict(sorted(all_results_labeled.items(), key=lambda x: x[1]["count"], reverse=True))
print("export const tag_counts =", sorted_labeled_results)

# Med Counts
# results = Counter(med_tags)
# print("export const med_counts =", dict(sorted(results.items(), key=lambda x: x[1], reverse=True)))

# Sup Counts
# results = Counter(sup_tags)
# print("export const sup_counts =", dict(sorted(results.items(), key=lambda x: x[1], reverse=True)))


