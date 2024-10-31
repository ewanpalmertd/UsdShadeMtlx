import logging
from pathlib import Path
from utils import executeTimeDecorator
from typing import List, Dict, Optional
import xml.etree.ElementTree as ET

xml_file: str = str(Path(__file__).with_name("test.xml"))

# TODO
# > check all input and output types to start figuring ways out how to filter them
# > filter all input/output data and convert it to usdAPI readable data


@executeTimeDecorator
def parse_xml_file(
    input_file: str,
):  # might need to sort return data later, we shall see
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
        inputs = []
        outputs = []
        children[name] = [inputs, outputs]
        for i in child:
            io_tag = i.tag
            io_attrib = i.attrib
            if io_tag == "input":
                inputs.append(io_attrib)
            elif io_tag == "output":
                outputs.append(io_attrib)

    return children


if __name__ == "__main__":
    parse_xml_file(input_file=xml_file)
