from pxr import Sdf, Usd, UsdShade, Tf
from config import USDSHADEMTLX_DATABASE
from typing import List, Dict, Optional
import os
import logging

class UsdShadeMtlxClass:

    def __init__(self) -> None:
        self.database = USDSHADEMTLX_DATABASE

    class Utils:
        def __init__(self) -> None:
            # this feels wrong
            self.database = USDSHADEMTLX_DATABASE

        def getInputs(self, id:str):
            if not id in self.database.keys():
                logging.error("Invalid id, unable to get inputs")
            inputs = self.database[id][0]
            return inputs
        
        def getOutputs(self, id:str):
            if not id in self.database.keys():
                logging.error("Invalid id, unable to get outputs")
            outputs = self.database[id][1]
            return outputs
        
        def getShaders(self):
            return list(self.database.keys())
        
        def searchForShader(self, filter:str) -> List[str]:
            filtered_list = []
            for key in self.database.keys():
                if filter in key: filtered_list.append(key)

            if not filtered_list:
                logging.warning("Could not find any matches")
                return
            
            print(filtered_list)
            
        

    # create local stage (in memory)
    # open external stage
    # crete new local stage

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

    def createMaterial(self, stage:Usd.Stage, path:str) -> UsdShade.Material:
        # need to check if stage is valid and if path is valid
        # write this into another function and use usd API to check
        # rather than checking manually
        return UsdShade.Material.Define(stage, path)

    def createShader(self, stage:Usd.Stage, path:str, id:str) -> UsdShade.Shader:
        # this function is too simple, need to create all valid inputs and outputs
        # from database
        if id not in self.database.keys():
            # report to use function to search for valid ID
            logging.error("Received invalid Shader ID")
            return 0

        if id == "standard_surface_surfaceshader": id = f"{id}_100" # 100 shader is the correct shader
        valid_id:str = f"ID_{id}"
        shader:UsdShade.Shader = UsdShade.Shader.Define(stage, path)
        shader.CreateIdAttr(valid_id)

        # create inputs
        inputs = self.Utils().getInputs(id=id)
        for input in inputs.keys():
            input_name = input
            input_type, input_value = inputs[input][0], inputs[input][1]
            shader.CreateInput(input_name, input_type).Set(input_value)
            

        return shader

if __name__ == "__main__":
    UsdShadeMtlx = UsdShadeMtlxClass()
    Utils = UsdShadeMtlx.Utils()
    path = "/materials/MTL_test"

    stage = UsdShadeMtlx.createLocalStage(filepath="test.usda")
    material = UsdShadeMtlx.createMaterial(stage=stage, path=path)
    shader = UsdShadeMtlx.createShader(stage=stage, path=f"{path}/surface", id="surface")
    stage.Save()
    