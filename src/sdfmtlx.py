from pxr import Sdf
from config import USDSHADEMTLX_DATABASE
from typing import List
from utils import time_execution, function_execution_test
import logging

"""
TODO:
- replicate materialxusdshade class but supporting
lower level api
- exclusive to Sdf, is an extension of the Sdf module rather than UsdShade
"""


class SdfMtlx:
    def __init__(self):
        pass

    @staticmethod
    def GetIDs() -> List[str]:
        return list(USDSHADEMTLX_DATABASE.keys())

if __name__ == "__main__":
    # layer = Sdf.Layer.CreateNew("tmp_sdfmtlx.usda")
    layer = Sdf.Layer.CreateAnonymous()
    