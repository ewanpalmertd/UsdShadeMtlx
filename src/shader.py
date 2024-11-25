from pxr import Usd, UsdShade
import logging
from typing import List, Dict, Any
from config import USDSHADEMTLX_DATABASE
from utils import time_execution

class UsdShadeMtlxShader:
    def __init__(self, stage: Usd.Stage, path: str, id: str) -> None:
        # constructor for shader class
        # create local stage if none is given, for unit testing
        self.database = USDSHADEMTLX_DATABASE
        self.stage    = stage
        self.path     = path
        self.id       = id

        self.__setup()

    def __setup(self) -> None:
        if self.id not in self.database.keys():
            logging.error("Received invalid Shader ID")
            return 0
        
        # add more verbose reasoning
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

    def GetInputs(self) -> None:
        self.inputs = self.database[self.id][0]
        return self.inputs
    
    def GetOutputs(self) -> None:
        self.outputs = self.database[self.id][1]
        return self.outputs
    
    def GetParameters(self) -> List[str]:
        return list(self.inputs.keys())

    def SetParameter(self, param: str, value) -> None:
        
        if not param in self.inputs.keys(): logging.error("Unable to find parameter")

        type = self.inputs[param][0]
        self.shader.CreateInput(param, type).Set(value)

    def SetParameters(self, input: Dict[str, Any]) -> None:
        for key, value in input.items():
            self.SetParameter(param=key, value=value)

    def ConnectToMaterial(self, material, output: str) -> None:
        # same thing here where we automate the output if there is only one output
        material.material.CreateSurfaceOutput().ConnectToSource(self.shader.ConnectableAPI(), output)

    def ConnectInput(self, input: str, source, output: str) -> None:
        # remember to add fallback for incorrect input
        # forget last argument if there is only one output on the node 
        if not input in list(self.inputs.keys()): logging.error("Invalid input parameter")
        if not output in list(source.outputs.keys()): logging.error("Invalid output parameter")

        type=self.inputs[input][0]
        self.shader.CreateInput(input, type).ConnectToSource(source.shader.ConnectableAPI(), output)

    def GetShaders(self):
        return list(self.database.keys())

if __name__ == "__main__":
    pass
    