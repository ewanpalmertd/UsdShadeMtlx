import glob
import os
import logging
from pathlib import Path
from utils import executeTimeDecorator
from typing import List, Dict, Optional
import xml.etree.ElementTree as ET

files: List[str] = glob.glob(f"{os.getcwd()}/*.xml")

# TODO
# download other mtlx libraries and convert to xml
# test parse function on other xml files
# sort dictionary output so inputs are in list 1 and outputs in list 2
# ^^ atm the lists are all messed up
# combine dictionaries between all xml files
# write function to convert data types to Sdf.ValueTypes and replace into dictionary


def parse_xml_file(input_file: str):
    """
    Given a .xml file. this function will parse it and get the relevant data
    in this case, it is parsing all the needed information from the materialx stdlib
    which has been converted from .mtlx to .xml
    """
    tree: ET.ElementTree = ET.parse(input_file)
    root: ET.Element = tree.getroot()
    children = {}
    for child in root:
        name: str = child.attrib["name"]
        if not name.startswith("ND"):
            continue

        inputs, outputs = {}, {}
        for node in child:
            iname, itype = node.attrib["name"], node.attrib["type"]
            try:
                ivalue = node.attrib["value"]
            except KeyError:
                ivalue = None
            if node.tag == "input":
                inputs[iname] = [itype, ivalue]
            else:
                outputs[iname] = [itype, ivalue]

        children[name] = [inputs, outputs]

    return children


if __name__ == "__main__":
    import time

    start = time.perf_counter()
    for i in files:
        print("-------------------------------------")
        print(parse_xml_file(input_file=i))
        print("-------------------------------------")
    end = time.perf_counter()
    print(f"{(end - start):.5f}")
