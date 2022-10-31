import json

with open("assets/genres.json") as f:
    name_dict = json.load(f)
name_list = name_dict["pokemon"]