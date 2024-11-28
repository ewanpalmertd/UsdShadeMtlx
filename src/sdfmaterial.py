from pxr import Sdf, Usd
from typing import List, Any
from utils import (
    time_execution, 
    function_execution_test,
    str_to_sdfpath)
from config import USDSHADEMTLX_DATABASE

class SdfMaterialSpec:
    def __init__(self, layer:Sdf.Layer, path) -> None:
        if not isinstance(layer, Sdf.Layer): raise TypeError("Layer must be Sdf.Layer object") # write better error message
        if not isinstance(path, Sdf.Path):
            self.path = str_to_sdfpath(path)
        else:
            self.path = path 
        self.layer = layer

    def __setup(self) -> None:
        self.material = Sdf.CreatePrimInLayer(self.layer, self.path)
        self.material.specifier = Sdf.SpecifierDef
        self.material.typeName  = "Material"

    def AssignToPrimSpec(self, prim_spec:Sdf.PrimSpec, purpose=None) -> None:
        # sort out preview
        material_binding_rel_spec = Sdf.RelationshipSpec(prim_spec, "material:binding", custom=False)
        material_binding_rel_spec.targetPathList.Append(self.path)
        schemas = Sdf.TokenListOp.Create(
            appendedItems=["MaterialBindingAPI"]
        )
        prim_spec.SetInfo("apiSchemas", schemas)
        return
    
    def ConnectToShaderSpec(self, shader_spec, source_name) -> None:
        return
    
