from pxr    import Sdf, Usd
from typing import List, Any
from utils  import (
    time_execution, 
    function_execution_test,
    str_to_sdfpath
)

"""
FUNCTIONS:

- Connect Displacement
- Make a check to see if shader is applicable or object is assignable
- Add in function for custom purpose
- Connect Volume
- GetSurfaceOutput
- GetDisplacementOutput
- GetVolumeOutput

- SurfaceSource() -> Returns a sdfshader object
- BaseMaterial???

- Look at Houdini for extra options of functions
- check to make sure there are no other materials with the same name

"""
# ------------------------------------------------------------------------------------------------------------


class SdfMaterialSpec:
    
    def __init__(self, layer : Sdf.Layer, path):
        
        if not isinstance(layer, Sdf.Layer): raise TypeError("Layer must be Sdf.Layer object")
        self.path  = str_to_sdfpath(path)
        self.layer = layer

    def __setup(self):
    
        self.material = Sdf.CreatePrimInLayer(self.layer, self.path)
        self.material.specifier = Sdf.SpecifierDef
        self.material.typeName  = "Material"

    def AssignToPrimSpec(self, prim_spec : Sdf.PrimSpec, purpose=None):
    
        # TODO: add in custom purpose functionality
        material_binding_rel_spec = Sdf.RelationshipSpec(prim_spec, "material:binding", custom=False)
        material_binding_rel_spec.targetPathList.Append(self.path)

        # NOTE: not sure this works if user adds another schema on top
        schemas = Sdf.TokenListOp.Create(appendedItems=["MaterialBindingAPI"])
        prim_spec.SetInfo("apiSchemas", schemas)
    
    def ConnectSurfaceToShaderSpec(self, shader_spec, source_name=None):
        
        # NOTE: if source has only one input then just default to input
        # NOTE: need to account for displacement and other attributes as well, or just automate it
        if len( shader_spec.database.Outputs() ) == 1: 
            source_name = "outputs:" + shader_spec.database.Outputs()[0]

        source_path = shader_spec.path.AppendProperty(source_name)
        material_output_attr_spec = Sdf.AttributeSpec(self.material, "outputs:surface", Sdf.ValueTypeNames.Token)
        material_output_attr_spec.connectionPathList.Append(source_path)
    

# ------------------------------------------------------------------------------------------------------------