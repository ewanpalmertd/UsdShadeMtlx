from xml_parser import MTLX_DICTIONARY
import json

with open("database.json", "w") as file:
    file.write(json.dumps(MTLX_DICTIONARY, sort_keys=True, indent=4))