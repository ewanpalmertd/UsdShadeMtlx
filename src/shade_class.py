from pxr import Sdf, Usd, UsdShade, Tf
from config import USDSHADEMTLX_DATABASE
import os
import logging

class UsdShadeMtlx:

    def __init__(self):
        self.database = USDSHADEMTLX_DATABASE


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
        if id not in self.database.keys():
            # report to use function to search for valid ID
            logging.error("Received invalid Shader ID")
            return 0

        valid_id:str = f"ID_{id}"
        surface:UsdShade.Shader = UsdShade.Shader.Define(stage, path)
        surface.CreateIdAttr(valid_id)
        return surface

if __name__ == "__main__":
    _class = UsdShadeMtlx()
    stage = UsdShadeMtlx().createLocalStage(filepath="test.usda")

    path = "/materials/MTL_test"
    material = UsdShadeMtlx().createMaterial(stage=stage, path=path)
    shader = _class.createShader(stage=stage, path=f"{path}/surface", id="surface")
    stage.Save()