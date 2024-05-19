import json
import chardet

json_file_path = "whitelist.json"
whitelist_data = {}  

file_path = f"whitelist.txt"  

with open(file_path, 'rb') as file:
    encoding = chardet.detect(file.read())['encoding']

rule_names = []

with open(file_path, 'r', encoding=encoding) as file:
    for line in file:
        rule_name = line.split(' ')[0]
        rule_names.append(rule_name)

whitelist_data["whitelist"] = rule_names

with open(json_file_path, 'w') as json_file:
    json.dump(whitelist_data, json_file, indent=4)
