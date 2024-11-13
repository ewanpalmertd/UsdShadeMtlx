import os
import json
from pathlib import Path
from pxr import Sdf
from typing import List, Dict
from utils import time_execution, converted_value_types

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

if __name__ == "__main__":
    import time
    start = time.perf_counter()
    end = time.perf_counter()
    print(f"{(end - start):.5f}")
