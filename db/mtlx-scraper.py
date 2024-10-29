# TODO
# split the mtlx file into sections for each node
# write efficient data parser to get {id, inputs:[type, default], outputs:[type, tils import executeTimeDecorator
import os
import logging
import re
from utils import executeTimeDecorator
from pathlib import Path
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


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


def get_parameter_value(param: str, data: str):
    pattern = rf'{param}="(.*?)"'
    matches = re.findall(pattern, data)
    return matches


@executeTimeDecorator
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
    a = get_parameter_value("input name", definitions[-7])
    inputs = [
        "".join(line.split())[1:]
        for line in definitions[-7].splitlines()
        if "".join(line.split()).startswith("<inputname")
    ]
    print(inputs)
    # for node in definitions:  # there are around 673 definitions, could be slow, might switch to c++ for better speed
    #     parsed_html = BeautifulSoup(node)
    #     print(parsed_html)


if __name__ == "__main__":
    split_list = split_mtlx_definitions()
    parse_mtlx_definitions(definitions=split_list)
