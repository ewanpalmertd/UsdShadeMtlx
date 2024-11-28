from pxr import Sdf
from config import USDSHADEMTLX_DATABASE
from typing import List
from utils import time_execution, function_execution_test, str_to_sdfpath
from sdfshader import SdfShaderSpec
from sdfmaterial import SdfMaterialSpec
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

    class CreateShaderSpec(SdfShaderSpec):
        pass

    class CreateMaterialSpec(SdfMaterialSpec):
        def __init__(self, layer:Sdf.Layer, path) -> None:
            if not isinstance(layer, Sdf.Layer): raise TypeError("Layer must be Sdf.Layer object") # write better error message
            if not isinstance(path, Sdf.Path):
                self.path = str_to_sdfpath(path)
            else:
                self.path = path 
            self.layer = layer
            self.__setup()

        def __setup(self) -> None:
            self.material = Sdf.CreatePrimInLayer(self.layer, self.path)
            self.material.specifier = Sdf.SpecifierDef
            self.material.typeName  = "Material"

    

    @staticmethod
    def GetIDs() -> List[str]:
        return list(USDSHADEMTLX_DATABASE.keys())

if __name__ == "__main__":
    # layer = Sdf.Layer.CreateNew("tmp_sdfmtlx.usda")
    layer = Sdf.Layer.CreateNew("sdf_material_test.usda")
    prim_spec = Sdf.CreatePrimInLayer(layer, Sdf.Path("/test"))
    prim_spec.specifier = Sdf.SpecifierDef
    prim_spec.typeName = "Cube"
    
    material_spec = SdfMtlx.CreateMaterialSpec(layer, Sdf.Path("/material"))
    material_spec.AssignToPrimSpec(prim_spec)

    layer.Save()