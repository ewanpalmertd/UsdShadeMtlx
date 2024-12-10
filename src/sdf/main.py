from pxr import Sdf
from typing import List
from shader import SdfShaderSpec
from material import SdfMaterialSpec
import sys
import os

sys.path.append(os.path.abspath(".."))
from utils  import time_execution, str_to_sdfpath
from database.database import DatabaseItem


# ------------------------------------------------------------------------------------------------------------


class SdfMtlx:
    def __init__(self):
        pass

    class CreateShaderSpec(SdfShaderSpec):
        def __init__(self, layer: Sdf.Layer, path, node, node_name=None):

            if not isinstance(layer, Sdf.Layer):
                raise AttributeError("Layer must be a Sdf.Layer object")
            self.layer = layer
            self.database = DatabaseItem(node)
            self.node = self.database.node
            self.id = self.database.node_id
            self.node_name = node_name if node_name else self.id[3:]
            self.path = str_to_sdfpath(path).AppendChild(self.node_name)

            self.__setup()

        def __setup(self) -> None:
            
            self.shader_spec = Sdf.CreatePrimInLayer(self.layer, self.path)
            self.shader_spec.specifier = Sdf.SpecifierDef
            self.shader_spec.typeName = "Shader"
            self.shader_spec.customData = self.database.Metadata() 

            shader_spec_id_attr = Sdf.AttributeSpec(self.shader_spec, "info:id", Sdf.ValueTypeNames.Token)
            shader_spec_id_attr.default = self.id
            shader_spec_id_attr.SetInfo("variability", Sdf.VariabilityUniform)

            for output in self.database.Outputs():
                Sdf.AttributeSpec(self.shader_spec, f"outputs:{output}", self.database.OutputType(output))

    class CreateMaterialSpec(SdfMaterialSpec):
        def __init__(self, layer: Sdf.Layer, path):
            
            if not isinstance(layer, Sdf.Layer):
                raise TypeError("Layer must be Sdf.Layer object")
            self.path = str_to_sdfpath(path)
            self.layer = layer
            self.__setup()

        def __setup(self):
        
            self.material = Sdf.CreatePrimInLayer(self.layer, self.path)
            self.material.specifier = Sdf.SpecifierDef
            self.material.typeName = "Material"
            
    @staticmethod
    def GetIDs() -> List[str]:
        return DatabaseItem.GetNodes()


# ------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    
    def test():
        layer = Sdf.Layer.CreateNew("sdf_material_test.usda")
        
        prim_spec = Sdf.CreatePrimInLayer(layer, Sdf.Path("/test"))
        prim_spec.specifier = Sdf.SpecifierDef
        prim_spec.typeName = "Cube"
        
        material_spec = SdfMtlx.CreateMaterialSpec(layer, Sdf.Path("/material"))
        material_spec.AssignToPrimSpec(prim_spec)

        shader_spec = SdfMtlx.CreateShaderSpec(layer, Sdf.Path("/material"), "ND_standard_surface_surfaceshader_100", "surface")
        shader_spec.SetAttributeSpec("base_color", (1, 0, 0))

        material_spec.ConnectSurfaceToShaderSpec(shader_spec)
        layer.Save()
    
    test()
    
