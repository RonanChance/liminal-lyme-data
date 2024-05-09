import json
import fileinput
import os
import re
import networkx as nx

def clean_text(text):
    return ''.join(char for char in text if 32 <= ord(char) <= 126)

def prep_for_llm():
    jsonl_file = fileinput.input('mydatav2.jsonl', encoding="utf-8")
    counter = 0

    for idx, dictionary in enumerate(jsonl_file):
        dictionary = json.loads(dictionary)
        counter += 1

        open_tag_pattern = r'<span class[^>]*>'
        close_tag_pattern = r'</span>'
        
        with open("./files/llm_data.txt", "a", encoding='utf-8') as llm_file:
            try:
                text_without_open_tags = re.sub(open_tag_pattern, '', clean_text(dictionary['body']))
                result = re.sub(close_tag_pattern, '', text_without_open_tags)
                llm_file.write(result + "\n")
                print(clean_text(dictionary['body']))
            except Exception:
                print("FOUND ISSUE")
                exit()
                continue

def generate_graph_csv():
    G = nx.DiGraph()

    jsonl_file = fileinput.input('mydatav2.jsonl', encoding="utf-8")
    for idx, dictionary in enumerate(jsonl_file):
        dictionary = json.loads(dictionary)

        user = dictionary['author']
        # open_tag_pattern = r'<span class[^>]*>'
        # close_tag_pattern = r'</span>'
        # text_without_open_tags = re.sub(open_tag_pattern, '', clean_text(dictionary['body']))
        # result = re.sub(close_tag_pattern, '', text_without_open_tags)
        # for word in result.split():
        #     if DG.has_edge(user, word):
        #         DG.edges[user, word]['weight'] += 1
        #     else:
        #         DG.add_edge(user, word, weight=1)

        combinedList = dictionary['conditions'] + dictionary['medications'] + dictionary['supplements']
        for word in combinedList:
            if G.has_edge(user, word):
                G.edges[user, word]['weight'] += 1
            else:
                G.add_edge(user, word, weight=1)
        G.nodes[user]['user'] = True
        if 'healed' in dictionary['body']:
            G.nodes[user]['healed'] = True

    nx.write_gexf(G, 'files/network.gexf')
    
def check_for_text(text):
    directory_path = "./TheEye/extracted/"
    reading_filenames = [directory_path+f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    
    for filename in reading_filenames:
        file = fileinput.input(filename)
        for line in file:
            json_line = json.loads(line)
            try:
                try:
                    if text in json_line["body"]:
                        print(line["body"], "\n")
                except Exception:
                    if text in json_line["selftext"]:
                        print(line["selftext"], "\n")
            except Exception:
                continue


def get_subreddit_names():
    directory_path = "./TheEye/repo/"
    reading_filenames = sorted(list(set([f.split('_')[0] for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))])))
    print(reading_filenames)

def get_number_of_comments():
    total_lines = 0
    directory_path = "./TheEye/extracted/"
    reading_filenames = [directory_path+f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    
    for filename in reading_filenames:
        file = fileinput.input(filename)
        for _ in file:
            total_lines += 1

    print(total_lines)
        
def generate_wikipedia_links():
    illnesses = ['ANAPLASMOSIS', 'BABESIOSIS', 'BARTONELLOSIS', 'EHRLICHIOSIS', 'LYME DISEASE', 'ROCKY MOUNTAIN SPOTTED FEVER', 'TULAREMIA']
    # medications = ['ACETAMINOPHEN', 'ACETAZOLAMIDE', 'ACYCLOVIR', 'ALPRAZOLAM', 'AMITRIPTYLINE', 'AMOXICILLIN', 'ARIPIPRAZOLE', 'AZITHROMYCIN', 'AZLOCILLIN', 'BOTULINUM TOXIN TYPE A', 'CEFTRIAXONE', 'CEFUROXIME', 'CELECOXIB', 'CEPHALEXIN', 'CETIRIZINE', 'CHOLESTYRAMINE', 'CIPROFLOXACIN', 'CITALOPRAM', 'CLARITHROMYCIN', 'CLINDAMYCIN', 'CLONAZEPAM', 'COLCHICINE', 'CROMOGLICIC ACID', 'CYCLOBENZAPRINE', 'DAPTOMYCIN', 'DEXAMETHASONE', 'DIAZEPAM', 'DICYCLOMINE', 'DIPHENHYDRAMINE', 'DISULFIRAM', 'DOXYCYCLINE', 'DULOXETINE', 'ESCITALOPRAM', 'ESOMEPRAZOLE', 'FENTANYL', 'FLUCONAZOLE', 'FLUOXETINE', 'FLUVOXAMINE', 'HYDROCODONE', 'HYDROCORTISONE', 'HYDROXYCHLOROQUINE', 'HYDROXYZINE', 'L-TRYPTOPHAN', 'LEVOFLOXACIN', 'LEVOTHYROXINE', 'LIOTHYRONINE', 'LORAZEPAM', 'MECLIZINE', 'MELOXICAM', 'METHOTREXATE', 'METHYLPHENIDATE', 'METHYLPREDNISOLONE', 'METRONIDAZOLE', 'MINOCYCLINE', 'MIRTAZAPINE', 'NALTREXONE', 'NAPROXEN', 'NIACIN', 'NORTRIPTYLINE', 'NYSTATIN', 'OMEPRAZOLE', 'ONDANSETRON', 'OXYCODONE', 'PANTOPRAZOLE', 'PAROXETINE', 'PENICILLIN G', 'PREGABALIN', 'PROMETHAZINE', 'RANITIDINE', 'RIFAMPIN', 'RIFAXIMIN', 'SERTRALINE', 'TETRACYCLINE', 'TINIDAZOLE', 'TOPIRAMATE', 'TRAZODONE', 'VALACICLOVIR', 'VANCOMYCIN', 'VENLAFAXINE', 'ZINC']

    # medication_dict = {}

    # for item in medications:
    #     medication_dict[item] = "https://en.wikipedia.org/wiki/" + item.replace(" ", "_").lower()

    # print(medication_dict)
    # print(len(medications))


if __name__ == '__main__':
    get_subreddit_names()
    # generate_wikipedia_links()
    # get_number_of_comments()
    # prep_for_llm()
    # check_for_text()
    # generate_graph_csv()