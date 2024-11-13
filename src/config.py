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
                converted_input = VALUE_TYPES[input_name][0]
                # if "matrix" in input_name:
                #     print(input_name, inputs[input][1])
                if len(VALUE_TYPES[input_name]) > 2:
                    try:
                        converted_default = VALUE_TYPES[input_name][1](
                            string_value=inputs[input][1], size=VALUE_TYPES[input_name][2])
                    except Exception as e:
                        print(input_name, inputs[input][1], e)
                else:
                    converted_default = VALUE_TYPES[input_name][1](string_value=inputs[input][1])
            else:
                converted_input = Sdf.ValueTypeNames.String
                converted_default = ""
            inputs[input][0] = converted_input
            inputs[input][1] = converted_default
  
        for output in outputs.keys():
            output_name = outputs[output][0]
            if output_name in VALUE_TYPES:
                converted_output = VALUE_TYPES[output_name][0]
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
