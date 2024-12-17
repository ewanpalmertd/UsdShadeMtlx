from typing import Any
from pxr import Sdf
import sys
import os

sys.path.append(os.path.abspath(".."))

from database.database import DatabaseItem
from utils import str_to_sdfpath, time_execution


class SdfShaderInput:
    """
    class representation of a shader input for easier manipulation of inputs
    """
    
    def __init__(self, spec, name: str, type, value: Any = None, customData=None):
        self.name = name
        self.type = type
        self.value = value
        self.customData = customData
        self.input = Sdf.AttributeSpec(spec, name, type)
        self.input.default = value
        self.input.customData = self.customData


if __name__ == "__main__":
    pass
