import os
import json
from pathlib import Path
from pxr import Sdf
from typing import List, Dict
from core_utils import time_execution, converted_value_types

VALUE_TYPES = converted_value_types()
json_path = f"{Path(__file__).parents[1]}/db/database.json"

assert os.path.isfile(json_path)

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
                converted_input = Sdf.ValueTypeNames.String
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

def load_json(input_file : str):
    with open(input_file) as file:
        data = json.load(file)
        converted_data = convert_data_types_to_sdf(mtlx_dictionary=data)
        return converted_data

USDSHADEMTLX_DATABASE = load_json(input_file=json_path)
# TODO: remove the ND_prefix from the list to start as it makes
# it much harder to search and to write

# NOTE : GOING TO INHERIT IN MAIN CLASS RATHER THAN HAVE A WHOLE 
# SEPERATE CLASS 

# class UsdShadeMtlxUtils:

#     def __init__(self) -> None:
#         self.database = load_json(input_file=json_path)

#     def get_nodes(self) -> List[str]:
#         """
#         Prints all of the different nodes that you can choose in the db
#         """
#         keys = list(self.database.keys())
#         return keys
    
#     def search_for_node(self, search : str):
#         """
#         Given a string to search with, it will filter all nodes and 
#         return nodes matching the filter
#         """
#         if not search: print("Please enter a valid keyword")

#         all_nodes = self.get_nodes()
#         filtered_nodes = [ node for node in all_nodes if search in node ]
#         return filtered_nodes
        

if __name__ == "__main__":
    import time
    start = time.perf_counter()
    a = UsdShadeMtlxUtils()
    end = time.perf_counter()
    print(f"{(end - start):.5f}")
