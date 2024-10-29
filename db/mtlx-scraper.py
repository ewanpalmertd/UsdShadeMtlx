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
    # splitting the stdlib.mtlx file into each of their node
    # definitions then returning as a list

    if not os.path.isfile(input_file):
        logging.exception("File does not exist")

    # would like to try to find an alternative method at some point
    output_list: List[str] = []
    with open(input_file) as file:
        contents = file.read().split("</nodedef>")
        for line in contents:
            output_list.append(f"<nodedef {line.split('<nodedef ')[-1]}")

    return output_list


if __name__ == "__main__":
    split_list = split_mtlx_definitions()
    print(split_list[0])
