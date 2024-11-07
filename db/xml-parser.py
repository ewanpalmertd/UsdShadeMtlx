import glob
import os
import logging
from pxr import Sdf
from pathlib import Path
from utils import executeTimeDecorator
from typing import List, Dict, Optional
import xml.etree.ElementTree as ET

files: List[str] = glob.glob(f"{os.getcwd()}/*.xml")

# look at filename value type
VALUE_TYPES = {
    "string": Sdf.ValueTypeNames.String,
    "float": Sdf.ValueTypeNames.Float,
    "integer": Sdf.ValueTypeNames.Int, #double check signed/unsiged and 32/64 bit int
    "color3": Sdf.ValueTypeNames.Color3f,
    "color4": Sdf.ValueTypeNames.Color4f,
    "vector2": Sdf.ValueTypeNames.Float2,
    "vector3": Sdf.ValueTypeNames.Float3, # double check vector types if Float3 or Vector3f
    "vector4": Sdf.ValueTypeNames.Float4,
    "vector2array": Sdf.ValueTypeNames.Float2Array,
    "matrix33": Sdf.ValueTypeNames.Matrix3d,
    "matrix44": Sdf.ValueTypeNames.Matrix4d,
    "boolean" : Sdf.ValueTypeNames.Bool,
}

# ^^^^^^^^^^^^^^^^^^
"""
Need to check types:
surfaceshader
displacementshader
volumeshader
filename
lightshader
filename
EDF
BSDF
VDF
"""


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


def convert_data_types_to_sdf(mtlx_dictionary):
    """
    Takes the mtlx dictionary and converts the data types
    to sdf supported format rather than string format

    Args:
    ----
        mtlx_dictionary - the xml converted materialx dictionary
    """
    converted_dictionary = {} # change variable name
    for node in mtlx_dictionary.keys():
        inputs  = mtlx_dictionary[node][0]
        outputs = mtlx_dictionary[node][1]

        # loop through each individual input
        # might avoid doing loop as we could maybe do it another way
        for input in inputs.keys():
            input_name = inputs[input][0]
            if input_name in VALUE_TYPES:
                converted_input = VALUE_TYPES[input_name]
            else:
                converted_input = input_name
            inputs[input][0] = converted_input
  
        for output in outputs.keys():
            output_name = outputs[output][0]
            if output_name in VALUE_TYPES:
                converted_output = VALUE_TYPES[output_name]
            else:
                converted_output = Sdf.ValueTypeNames.Token
            outputs[output][0] = converted_output
            
        converted_dictionary[node] = mtlx_dictionary[node]

    return converted_dictionary

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

if __name__ == "__main__":
    import time
    test : str = files[-1]
    start = time.perf_counter()
    #shaders = parse_xml_file(input_file=test)
    #converted_shaders = convert_data_types_to_sdf(mtlx_dictionary=shaders)
    #get_unique_data_types(shaders)
    Sdf.ValueTypeNames.Float2Array
    for i in files:
        shaders = parse_xml_file(input_file=i)
        data_types = get_unique_data_types(mtlx_dictionary=shaders)
        for type in data_types:
            if type not in VALUE_TYPES.keys(): print(type)
    end = time.perf_counter()
    print(f"{(end - start):.5f}")
