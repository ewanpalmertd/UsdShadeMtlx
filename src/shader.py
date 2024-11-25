from pxr import Usd, UsdShade, Sdf, Vt, Gf, UsdGeom
import logging
from typing import List, Optional
from config import USDSHADEMTLX_DATABASE
from shade_class import UsdShadeMtlxClass

UsdShadeMtlx = UsdShadeMtlxClass()
Utils = UsdShadeMtlxClass().Utils()

class UsdShadeShader:
    def __init__(self, stage: Usd.Stage, path: str, id: str) -> None:
        # constructor for shader class
        self.database = USDSHADEMTLX_DATABASE
        self.stage    = stage
        self.path     = path
        self.id       = id

        # creating shader (might put into different function)
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
        self.inputs = Utils.getInputs(id=self.id)
        for input in self.inputs.keys():
            input_name = input
            input_type, input_value = self.inputs[input][0], self.inputs[input][1]
            self.shader.CreateInput(input_name, input_type).Set(input_value)

        self.outputs = Utils.getOutputs(id=self.id)
        for output in self.outputs.keys():
            self.shader.CreateOutput(output, self.outputs[output][0])

    def GetInputs(self) -> None:
        return self.inputs
    
    def GetOutputs(self) -> None:
        return self.outputs
    
    def GetParamaters(self) -> List[str]:
        return list(self.inputs.keys())

    def SetParamater(self, param: str, value) -> None:
        
        # - convert type to Vt/Gf when needed 
        if not param in self.inputs.keys(): logging.error("Unable to find parameter")

        type = self.inputs[param][0]
        self.shader.CreateInput(param, type).Set(value)

    def ConnectToMaterial(self, material, output: str) -> None:
        material.CreateSurfaceOutput().ConnectToSource(self.shader.ConnectableAPI(), output)


if __name__ == "__main__":
    path = "/materials/MTL_test"
    stage = UsdShadeMtlx.createLocalStage(filepath="shader_test.usda")
    sphere = UsdGeom.Sphere.Define(stage, "/sphere")
    material = UsdShadeMtlx.createMaterial(stage=stage, path=path)

    Shader = UsdShadeShader(stage=stage, path=f"{path}/surface", id="standard_surface_surfaceshader")
    Shader.SetParamater("base_color", (1, 0, 0))
    Shader.SetParamater("specular_roughness", (0.0))
    Shader.ConnectToMaterial(material=material, output="out")

    # assigning shader
    sphere.GetPrim().ApplyAPI(UsdShade.MaterialBindingAPI)
    UsdShade.MaterialBindingAPI(sphere).Bind(material)

    stage.Save()
