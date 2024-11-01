import glob
import os
import logging
from pxr import Sdf
from pathlib import Path
from utils import executeTimeDecorator
from typing import List, Dict, Optional
import xml.etree.ElementTree as ET

files: List[str] = glob.glob(f"{os.getcwd()}/*.xml")

VALUE_TYPES = {}

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
    children = {}
    for child in root:
        name: str = child.attrib["name"]
        if not name.startswith("ND"):
            continue

        inputs, outputs = {}, {}
        for node in child:
            iname, itype = node.attrib["name"], node.attrib["type"]
            print(itype)
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


def convert_data_types_to_sdf(mtlx_dictionary):
    """
    Takes the mtlx dictionary and converts the data types
    to sdf supported format rather than string format

    Args:
    ----
        mtlx_dictionary - the xml converted materialx dictionary
    """
    return 0


if __name__ == "__main__":
    import time

    start = time.perf_counter()
    for i in files:
        parse_xml_file(input_file=i)
    end = time.perf_counter()
    print(f"{(end - start):.5f}")
