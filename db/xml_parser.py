import glob
import os
from pxr import Sdf
from pathlib import Path
from typing import List, Dict, Optional
import xml.etree.ElementTree as ET

files: List[str] = glob.glob(f"{os.getcwd()}/*.xml")

# TODO
# download other mtlx libraries and convert to xml
# combine dictionaries between all xml files -not prio
# get all unique data types and convert to Sdf types
# write function to convert data types to Sdf.ValueTypes and replace into dictionary
# we need a function that fixes the name for standard surface, simple fix but important


def parse_xml_file(input_file: str):
    """
    Given a .xml file. this function will parse it and get the relevant data
    in this case, it is parsing all the needed information from the materialx stdlib
    which has been converted from .mtlx to .xml
    """
    tree: ET.ElementTree = ET.parse(input_file)
    root: ET.Element = tree.getroot()
    types = []
    children = {}
    for child in root:
        name: str = child.attrib["name"]
        if not name.startswith("ND"):
            continue
        
        name = name.replace("ND_", "")
        inputs, outputs = {}, {}
        for node in child:
            iname, itype = node.attrib["name"], node.attrib["type"]
            try:
                ivalue = node.attrib["value"]
            except KeyError:
                ivalue = None
            if node.tag == "input":
                # if itype in VALUE_TYPES:
                #    itype = VALUE_TYPES[itype]
                if itype not in types:
                    types.append(itype)
                inputs[iname] = [itype, ivalue]
            else:
                outputs[iname] = [itype, ivalue]

        children[name] = [inputs, outputs]

    return children

def get_unique_data_types(mtlx_dictionary) -> List[str]:
    """
    Uses the dictionary as an input and returns a list of all the unique
    data types so its easier to convert them from string to sdf type
    
    params
    :mtlx_dictionary - dict: -> the unconverted dictionary to get the value types from
    """
    unique_list = []
    for node in mtlx_dictionary.keys():
        inputs = mtlx_dictionary[node][0]
        for input in inputs:
            input_type = inputs[input][0]
            if input_type not in unique_list: unique_list.append(input_type)
            continue
            
    return unique_list

def combine_dicionaries(files : List[str]):
    """
    combines all of the xml dictionaries into a single dictionary
    """
    dictionary = {}
    for file in files:
        unconverted_dictionary = parse_xml_file(input_file=file)
        for key in unconverted_dictionary.keys():
            dictionary[key] = unconverted_dictionary[key]

    return dictionary

MTLX_DICTIONARY = combine_dicionaries(files=files)

if __name__ == "__main__":
    import time
    start = time.perf_counter()
    print(MTLX_DICTIONARY.keys())
    end = time.perf_counter()
    print(f"{(end - start):.5f}")
