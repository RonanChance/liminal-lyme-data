import json
import fileinput

def parse_line(line):
    """Parse a line of the file into a dictionary."""
    parts = line.strip().split(': ')
    if len(parts) == 2:  # URL line
        name = parts[0]
        link = parts[1]
        return {"name": name, "type": "url", "link": link}
    else:  # Folder line
        name = parts
        return {"name": name, "type": "folder", "children": []}

def build_tree(lines):
    """Build a nested dictionary from the list of lines."""
    root = {"name": "Treatments", "type": "folder", "children": []}
    stack = [(root, -1)]  # (parent, parent_indent_level)

    for line in lines:
        if not line.strip():
            continue
        
        indent_level = len(line) - len(line.lstrip())
        item = parse_line(line)
        
        while stack and stack[-1][1] >= indent_level:
            stack.pop()
        
        if indent_level == 0:
            stack[0][0]["children"].append(item)
        else:
            stack[-1][0]["children"].append(item)
        
        if item["type"] == "folder":
            stack.append((item, indent_level))
    
    return root

def main():
    lines = fileinput.input(files='txts/treatments.txt')
    tree = build_tree(lines)
    # print(json.dumps(tree, indent=4))
    with open('treeData.json', 'w') as f:
        json.dump(tree, f)

if __name__ == '__main__':
    main()
