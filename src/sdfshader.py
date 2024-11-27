from pxr import Sdf, Usd
from typing import List, Any
from utils import (
    time_execution, 
    function_execution_test,
    str_to_sdfpath)
from config import USDSHADEMTLX_DATABASE

"""
TODO:
- test with inputting an invalid layer and seeing how the class responds
"""

class SdfMtlxShader:


    @time_execution
    def __init__(self, layer: Sdf.Layer, path: Any, id: str, node_name=None):
        self.layer = layer
        
        self.node_name = node_name if node_name else id
        if not isinstance(path, Sdf.Path):
            self.path = str_to_sdfpath(path).AppendChild(self.node_name)
        else:
            self.path = path.AppendChild(self.node_name) 
        
        # TODO: need to account for 100 surface shader but not prio atm
        if not id in USDSHADEMTLX_DATABASE.keys(): raise Exception("Invalid shader ID, use SdfMtlx.Shader.GetIDs() to get a list of available shader IDs.")

        # NOTE: this code below means that usdpreviewsurface is not compatible
        # should fix this asap
        if id == "standard_surface_surfaceshader":
            self.id = "standard_surface_surfaceshader_100"
            self.search_id = "ND_standard_surface_surfaceshader"
        else:
            self.id = id
            self.search_id = f"ND_{id}"

        self.__setup()

    def __setup(self) -> None:
        self.shader_spec = Sdf.CreatePrimInLayer(layer, self.path)
        self.shader_spec.specifier = Sdf.SpecifierDef
        self.shader_spec.typeName = "Shader"
        shader_spec_id_attr = Sdf.AttributeSpec(self.shader_spec, "info:id", Sdf.ValueTypeNames.Token)
        shader_spec_id_attr.default = self.search_id
        shader_spec_id_attr.SetInfo("variability", Sdf.VariabilityUniform)
        for output in self.GetOutputAttributes():
            shader_spec_output_attr = Sdf.AttributeSpec(self.shader_spec, output, Sdf.ValueTypeNames.Token)

    def GetInputAttributes(self) -> List[str]:
        return [f"inputs:{key}" for key in USDSHADEMTLX_DATABASE[self.id][0]]
    
    def GetOutputAttributes(self) -> List[str]:
        return [f"outputs:{key}" for key in USDSHADEMTLX_DATABASE[self.id][1]]
    
    def SetAttributeSpec(self, attribute: str, value: Any) -> None:
        # NOTE: need to decide whether user uses `inputs:` prefix when providing
        # attribute, should accompany for both

        if not f"inputs:{attribute}" in self.GetInputAttributes(): raise AttributeError("Given attribute is not valid, use GetInputAttributes() to see all avaialable attributes.")

        attribute_info = USDSHADEMTLX_DATABASE[self.id][0][attribute]
        attribute_spec = Sdf.AttributeSpec(self.shader_spec, f"inputs:{attribute}", attribute_info[0], declaresCustom=False)
        # NOTE: see if there is an alternative to .default
        attribute_spec.default = value

    def ConnectToMaterialSpec(self):
        return

    def ConnectToShaderInputAttribute(self):
        return        

if __name__ == "__main__":
    layer = Sdf.Layer.CreateNew("sdf_shader_test.usda")
    
    root = Sdf.CreatePrimInLayer(layer, Sdf.Path("/root"))
    mtl  = Sdf.CreatePrimInLayer(layer, Sdf.Path("/root/material"))
    root.specifier = Sdf.SpecifierDef
    mtl.specifier  = Sdf.SpecifierDef

    test_shader = SdfMtlxShader(layer, Sdf.Path("/root/material"), "standard_surface_surfaceshader")
    test_shader.SetAttributeSpec("base_color", (1.0, 0.0, 0.0))
    
    layer.Save()
    pass