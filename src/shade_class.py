from pxr import Sdf, Usd, UsdShade, Tf, UsdGeom
from config import USDSHADEMTLX_DATABASE
from typing import List
from shader import UsdShadeShader
from utils import time_execution
import logging


"""
TODO:

TASKS:
- add docstrings to all functions in this file and shader file
- rename file to somethong more appropriate and fix across files
- run 2-3 unit tests
- turn into pip package
- create and share documentation
- present tool

FUNCTIONS:
- revert parameter to default
- unassign shader? not prio
- function for setting material purpose
- add function for assigning random display colors
"""

class UsdShadeMtlxClass:
    # if we import the class only, need to make sure that all the modules are imported here
    # also make sure to check for missing modules (especially pxr modules) 

    class Shader(UsdShadeShader):
        def __init__(self, stage: Usd.Stage, path: str, id: str) -> None:
            self.database = USDSHADEMTLX_DATABASE
            self.stage    = stage 
            self.path     = path if type(path) == Sdf.Path else Sdf.Path(path)
            self.id       = id
            self.__setup()

        def __setup(self) -> None:
            if self.id not in self.database.keys():
                logging.error("Received invalid Shader ID")
                return 0
            
            if self.id == "standard_surface_surfaceshader": 
                self.id = f"{self.id}_100" # 100 shader is the correct shader
                valid_id: str = "ND_standard_surface_surfaceshader"
            else:
                valid_id:str = f"ND_{self.id}"

            
            self.shader:UsdShade.Shader = UsdShade.Shader.Define(self.stage, self.path)
            self.shader.CreateIdAttr(valid_id)

            # create inputs
            self.inputs = self.GetInputs()
            for input in self.inputs.keys():
                input_name = input
                input_type, input_value = self.inputs[input][0], self.inputs[input][1]
                self.shader.CreateInput(input_name, input_type).Set(input_value)

            self.outputs = self.GetOutputs()
            for output in self.outputs.keys():
                self.shader.CreateOutput(output, self.outputs[output][0])
    
    def __init__(self) -> None:
        self.database = USDSHADEMTLX_DATABASE

    def getShaders(self):
            return list(self.database.keys())
    
    def searchForShader(self, filter:str) -> List[str]:
            # this needs better implementation
            filtered_list = []
            for key in self.database.keys():
                if filter in key: filtered_list.append(key)

            if not filtered_list:
                logging.warning("Could not find any matches")
                return
          
    def createLocalStage(self, filepath:str) -> Usd.Stage:
        """
        Creates a local USD stage from a given filepath

        Args:
        ----
            filepath (str): The path to where the stage should be saved

        Return:
        ----
            Usd.Stage: The USD stage to be used during the class
        """
        try:
            return Usd.Stage.CreateNew(filepath)
        except Tf.ErrorException as e:
            logging.error("Passed invalid file path")
            return 0

    def CreateMaterial(self, stage:Usd.Stage, path:str) -> UsdShade.Material:
        # need to check if stage is valid and if path is valid
        # write this into another function and use usd API to check
        # rather than checking manually
        return UsdShade.Material.Define(stage, path)

    def AssignMaterial(self, prim, material) -> None:
        # need to be able to assign this from given path not just prim, leave as is for now
        assignable_prim = prim
        assignable_prim.ApplyAPI(UsdShade.MaterialBindingAPI)
        UsdShade.MaterialBindingAPI(prim).Bind(material)

if __name__ == "__main__":
    UsdShadeMtlx = UsdShadeMtlxClass() # need to rename class
    stage = UsdShadeMtlx.createLocalStage(filepath="shader_test.usda")
    
    root = UsdGeom.Scope.Define(stage, Sdf.Path("/root"))
    materials = UsdGeom.Scope.Define(stage, Sdf.Path("/root/materials"))
    ref_prim = UsdGeom.Xform.Define(stage, Sdf.Path("/root/seal")).GetPrim()
    
    references = ref_prim.GetReferences()
    references.AddReference(
        assetPath="/home/epalmer/Desktop/root/bin/seal_model_flattened.usda",
        primPath=Sdf.Path("/sopimport1")
    )

    @time_execution
    def main():
        material = UsdShadeMtlx.CreateMaterial(stage, Sdf.Path("/root/materials/mtl_main"))
        surface = UsdShadeMtlx.Shader(stage, "/root/materials/mtl_main/surface", "standard_surface_surfaceshader")
        surface.SetParameters({
            "base_color": (0, 0, 0.8),
            "specular_roughness": 0.53,
        })

        image = UsdShadeMtlx.Shader(stage, "/root/materials/mtl_main/picture", "image_color3")
        image.SetParameter("file", "/home/epalmer/Pictures/wallpapers/Knights.png")
        
        surface.ConnectInput("base_color", image, "out")
        surface.ConnectToMaterial(material, "out")
        UsdShadeMtlx.AssignMaterial(ref_prim, material)



    main()
    stage.Save()