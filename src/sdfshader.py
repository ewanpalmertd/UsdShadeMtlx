from database.database import DatabaseItem
from utils import str_to_sdfpath, time_execution
from pxr import Sdf, Usd
from typing import Any, List


"""
FUNCTIONS:

- GetInput() -> Get the value of an input if it exists
- IsInput(string input) -> checks the database if the input is valid
- IsOutput(string output) -> same as IsInput but for output
- GetMetadata
- GetAttributeMetadata
- Path() -> returns the location of the 
- Function to get the ascii data for the shader
- Apply schema?
- Shader search function using decent search algo
- check if there are no shaders with the same name
- add docstrings

"""

# ------------------------------------------------------------------------------------------------------------


class SdfShaderSpec:
    """
    class representation of a SdfPrimSpec as a shader
    
    """

    def __init__(self, layer: Sdf.Layer, path, node, node_name=None):

        if not isinstance(layer, Sdf.Layer): 
            raise AttributeError("Layer must be a Sdf.Layer object")
        self.layer     = layer
        self.database  = DatabaseItem(node)
        self.node      = self.database.node
        self.id        = self.database.node_id
        self.node_name = node_name if node_name else self.id[3:]
        self.path = str_to_sdfpath(path).AppendChild(self.node_name)

        self.__setup()

    def __setup(self) -> None:
        
        self.shader_spec = Sdf.CreatePrimInLayer(self.layer, self.path)
        self.shader_spec.specifier  = Sdf.SpecifierDef
        self.shader_spec.typeName   = "Shader"
        self.shader_spec.customData = self.database.Metadata() 

        shader_spec_id_attr = Sdf.AttributeSpec(self.shader_spec, "info:id", Sdf.ValueTypeNames.Token)
        shader_spec_id_attr.default = self.id
        shader_spec_id_attr.SetInfo("variability", Sdf.VariabilityUniform)

        for output in self.database.Outputs():
            Sdf.AttributeSpec(self.shader_spec, f"outputs:{output}", self.database.OutputType(output))

    def SetAttributeSpec(self, attribute : str, value : Any) -> None:
        
        attribute_spec = Sdf.AttributeSpec(self.shader_spec, f"inputs:{attribute}", self.database.InputType(attribute))
        attribute_spec.default    = value
        attribute_spec.customData = self.database.InputMetadata(attribute)

    def GetInputs(self, authored_only : bool = True) -> List[Any]:
        """
        Returns a list of all avaialable inputs on the given node

        params:
        -- authored_only : bool - if enabled, only returns the inputs that have already been authored ( not default ) 
        
        returns:
        -- a list of inputs with the type string ( might adjust this later on to be a different type )
        """

        return


# ------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":

    @time_execution
    def main():
        layer = Sdf.Layer.CreateNew("tmp.usda")
        prim_spec = Sdf.CreatePrimInLayer(layer, Sdf.Path("/test"))
        prim_spec.specifier = Sdf.SpecifierDef
        prim_spec.typeName = "Cube"
        test_shader = SdfShaderSpec(layer, Sdf.Path("/material"), "ND_standard_surface_surfaceshader_100")
        test_shader.SetAttributeSpec("base_color", (1, 0, 0))
        layer.Save()
    
    main()
