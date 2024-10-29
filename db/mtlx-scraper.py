# TODO
# split the mtlx file into sections for each node
# write efficient data parser to get {id, inputs:[type, default], outputs:[type, default]}

import re
import os
import logging
from pathlib import Path
from typing import List, Dict, Optional

STDLIB: str = str(Path(__file__).with_name("stdlib_defs.mtlx"))


def split_mtlx_definitions(input_file: str = STDLIB) -> List[str]:
    """
    Takes the stdlib_defs.mtlx file from the public repo and splits all
    definitions into a list to be parsed later

    Args:
    ----
        input_file (str): Takes the input .mtlx file to split from

    Returns:
    ----
        List[str]: a list of each materialx node definition
    """

    if not os.path.isfile(input_file):
        logging.exception("File does not exist")

    # would like to try to find an alternative method at some point
    output_list: List[str] = []
    with open(input_file) as file:
        contents = file.read().split("</nodedef>")
        for line in contents:
            output_list.append(f"<nodedef {line.split('<nodedef ')[-1]}")

    return output_list


def parse_mtlx_definitions(definitions: List[str]) -> None:
    """
    Takes the raw materialx definitions and converts
    them to more readable data

    Args:
    ----
        definitions (List[str]): The list of nodes from the previous function

    Returns:
    ----
        !!still need to figure out the best way to return
    """
    pass


if __name__ == "__main__":
    split_list = split_mtlx_definitions()
    print(split_list[0])
