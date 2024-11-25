from pxr import Usd, UsdShade, Sdf, Vt, Gf, UsdGeom
import logging
from typing import List, Optional, Dict, Any
from config import USDSHADEMTLX_DATABASE
from shade_class import UsdShadeMtlxClass
from utils import time_execution

UsdShadeMtlx = UsdShadeMtlxClass()
Utils = UsdShadeMtlxClass().Utils()

class UsdShadeShader:
    def __init__(self, stage: Usd.Stage, path: str, id: str) -> None:
        # constructor for shader class
        # create local stage if none is given, for unit testing
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
        
        if not param in self.inputs.keys(): logging.error("Unable to find parameter")

        type = self.inputs[param][0]
        self.shader.CreateInput(param, type).Set(value)

    def SetParamaters(self, input: Dict[str, Any]) -> None:
        pass

    def ConnectToMaterial(self, material, output: str) -> None:
        material.CreateSurfaceOutput().ConnectToSource(self.shader.ConnectableAPI(), output)

    def ConnectInput(self, input: str, source, output: str) -> None:
        # remember to add fallback for incorrect input
        if not input in list(self.inputs.keys()): logging.error("Invalid input parameter")
        if not output in list(source.outputs.keys()): logging.error("Invalid output parameter")

        type=self.inputs[input][0]
        self.shader.CreateInput(input, type).ConnectToSource(source.shader.ConnectableAPI(), output)


if __name__ == "__main__":
    # standard_surface.CreateInput("base_color", Sdf.ValueTypeNames.Color3f).ConnectToSource(image.ConnectableAPI(), "out")
    @time_execution
    def main():
        path = "/materials/mtl_main"
        texture = "/home/epalmer/Pictures/wallpapers/Knights.png"
        stage = UsdShadeMtlx.createLocalStage(filepath="shader_test.usda")

        ref_prim = UsdGeom.Scope.Define(stage, Sdf.Path("/ref")).GetPrim()
        references = ref_prim.GetReferences()
        references.AddReference(
            assetPath="/home/epalmer/Desktop/root/bin/seal_model_flattened.usda",
            primPath=Sdf.Path("/sopimport1")
        )

        material = UsdShadeMtlx.createMaterial(stage=stage, path=path)

        standard_surface = UsdShadeShader(stage=stage, path=f"{path}/surface", id="standard_surface_surfaceshader")
        standard_surface.SetParamater("base_color", (1, 0, 0))
        standard_surface.SetParamater("specular_roughness", (0.0))
        standard_surface.ConnectToMaterial(material=material, output="out")

        image = UsdShadeShader(stage=stage, path=f"{path}/image", id="image_color3")
        image.SetParamater("file", texture)
        standard_surface.ConnectInput(input="base_color", source=image, output="out")
        ref_prim.ApplyAPI(UsdShade.MaterialBindingAPI)
        UsdShade.MaterialBindingAPI(ref_prim).Bind(material)

        stage.Save()

    main()