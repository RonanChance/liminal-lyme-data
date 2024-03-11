import json
from collections import Counter

with open('mydatav3.json', 'r', encoding="utf-8") as json_file:
    data = json.load(json_file)

con_tags = []
all_tags = []
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


results = Counter(all_tags)
all_results_count = {item.upper(): count for item, count in results.items()}
# All medications & supplements counts
# print(dict(sorted(all_results_count.items(), key=lambda x: x[1], reverse=True)))

# All tags list
# print(dict(sorted(all_results_count.items(), key=lambda x: x[1], reverse=True)))

# Medications and counts
# results = Counter(med_tags)
# print(dict(sorted(results.items(), key=lambda x: x[1], reverse=True)))

# Supplements and counts
# results = Counter(sup_tags)
# print(dict(sorted(results.items(), key=lambda x: x[1], reverse=True)))

con_results = Counter(con_tags)
con_results_count = {item.upper(): count for item, count in con_results.items()}
med_results = Counter(med_tags)
med_results_count = {item.upper(): count for item, count in med_results.items()}
sup_results = Counter(sup_tags)
sup_results_count = {item.upper(): count for item, count in sup_results.items()}

# ONLY Conditions
# print(", ".join([i for i,c in sorted(con_results_count.items(), key=lambda x: x[1], reverse=True)]))

# ONLY Medications
print(", ".join([i for i,c in sorted(med_results_count.items(), key=lambda x: x[1], reverse=True)]))

# ONLY Supplements
print(", ".join([i for i,c in sorted(sup_results_count.items(), key=lambda x: x[1], reverse=True)]))




# print("\n viable tags \n")
# print(", ".join(sorted(list(all_results_count.keys()))))

# print("\n number of viable tags \n")
# print(len(all_results_count))

# # print dictionary so that we can include counts in website
# print("\n mapping \n")
# print(dict(sorted(all_results_count.items(), key=lambda x: x[1], reverse=True)))

# print("\n only medications \n")
# print(sorted([item for item in all_results_count if item not in mapping.values()]))

# print("\n only conditions \n")
# print(sorted(list(set(list(mapping.values()) + ["ALL CONDITIONS (ANY)"]))))

# print("\n viable tags for upload \n")
# print(list(all_results_count.keys()))
