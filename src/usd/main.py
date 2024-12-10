from pxr import Sdf, Usd, UsdShade, Tf, UsdGeom, Gf
from config import USDSHADEMTLX_DATABASE
from typing import List, Any, Tuple
from shader import UsdShadeMtlxShader
from material import UsdShadeMtlxMaterial
from utils import time_execution, check_path
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

"""


class UsdShadeMtlx:
    # if we import the class only, need to make sure that all the modules are imported here
    # also make sure to check for missing modules (especially pxr modules) 

    class Shader(UsdShadeMtlxShader):
        def __init__(self, stage: Usd.Stage, path: str, id: str) -> None:
            self.database = USDSHADEMTLX_DATABASE
            self.stage = stage
            self.path = path if type(path) is Sdf.Path else Sdf.Path(path)
            self.id = id
            check_path(self.path)
            self.__setup()

        def __setup(self) -> None:
            if self.id not in self.database.keys():
                logging.error("Received invalid Shader ID")
                return 0

            if self.id == "standard_surface_surfaceshader": 
                self.id = f"{self.id}_100"  # 100 shader is the correct shader
                valid_id: str = "ND_standard_surface_surfaceshader"
            else:
                valid_id: str = f"ND_{self.id}"

            self.shader: UsdShade.Shader = UsdShade.Shader.Define(self.stage, self.path)
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

    class Material(UsdShadeMtlxMaterial):
        def __init__(self, stage: Usd.Stage, path: str) -> None:
            self.stage = stage
            self.path = path

            self.__setup()

        def __setup(self) -> None:
            self.material: UsdShade.Material = UsdShade.Material.Define(self.stage, self.path)

    def __init__(self) -> None:
        self.database = USDSHADEMTLX_DATABASE

    def __is_valid_purpose(self, purpose: str) -> int:
        if purpose == "": return 1
        if purpose == "preview" or purpose == "full": return 1
        return 0

    def __convert_to_prim(self, prim):
        if type(prim) is Sdf.Path:
            prim = stage.GetPrimAtPath(prim.pathString)
            return prim
        elif type(prim) is str:
            prim = stage.GetPrimAtPath(prim)
            return prim
        else:
            return prim

    def searchForShader(self, filter:str) -> List[str]:
        # this needs better implementation
        filtered_list = []
        for key in self.database.keys():
            if filter in key:
                filtered_list.append(key)

        if not filtered_list:
            logging.warning("Could not find any matches")
            return

    def CreateLocalStage(self, filepath: str) -> Usd.Stage:
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
        except Tf.ErrorException:
            logging.error("Passed invalid file path")
            return 0

    def __SetDisplayColor(self, prim: Any, color: Tuple[float] = (), random: bool = False) -> None:

        # NOTE: this function is very slow for what its doing, will private it and come back later
        from random import uniform
        prim = self.__convert_to_prim(prim)
        if not prim.GetChildren():
            if not prim.IsA("Mesh"):
                logging.warning("You are assigning to a primitve that isn't a Mesh, the displayColor will not work")
            prim.GetAttribute("primvars:displayColor").Set([Gf.Vec3f(color)])
        else:
            for child in prim.GetAllChildren():
                if child.IsA("Mesh") and not random:
                    prim.CreateAttribute("primvars:displayColor", Sdf.ValueTypeNames.Color3fArray).Set([Gf.Vec3f(color)])
                if child.IsA("Mesh") and random:
                    prim.CreateAttribute("primvars:displayColor", Sdf.ValueTypeNames.Color3fArray).Set(
                        [Gf.Vec3f(uniform(0, 1), uniform(0, 1), uniform(0, 1))])
        return

    def SetPurpose(self, stage: Any, prim: Any, purpose: str = "") -> None:

        # NOTE: need to do a check for if a given prim exists in the current stage
        # NOTE: this function is way to overcomplicated atm, will simplify later down the line

        if not self.__is_valid_purpose(purpose): 
            raise Exception("Given purpose is not valid, either leave empty or use `full` or `preview`")
        prim = self.__convert_to_prim(prim)
        if purpose != "":
            purpose = f":{purpose}"

        bindings: List[str] = ["material:binding", "material:binding:full", "material:binding:preview"]

        try:
            bindings_list = [bind for bind in bindings if prim.GetRelationship(bind)]
        except AttributeError:
            raise AttributeError("Input prim is invalid. Accepted types: [str, Sdf.Path, Usd.Prim]")

        if len(bindings_list) != 1:
            raise Exception("No material bindings found")

        current_binding = prim.GetRelationship(bindings_list[0])
        rm_list = current_binding.GetTargets()
        targets = []
        for rm in rm_list:
            current_binding.RemoveTarget(rm)
            targets.append(rm)

        rel = prim.CreateRelationship(f"material:binding{purpose}")
        rel.SetTargets(targets)


if __name__ == "__main__":
    UsdShadeMtlx = UsdShadeMtlx()  # need to rename class
    stage = UsdShadeMtlx.CreateLocalStage(filepath="shader_test.usda")
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
        material = UsdShadeMtlx.Material(stage, Sdf.Path("/root/materials/mtl_main"))
        surface = UsdShadeMtlx.Shader(stage, "/root/materials/mtl_main/surface", "standard_surface_surfaceshader")
        surface.SetParameters({
            "base_color": (0, 0, 0.8),
            "specular_roughness": 0.53,
        })

        image = UsdShadeMtlx.Shader(stage, "/root/materials/mtl_main/picture", "image_color3")
        image.SetParameter("file", "/home/epalmer/Pictures/wallpapers/Knights.png")
        surface.ConnectInput("base_color", image, "out")
        surface.ConnectToMaterial(material, "out")
        material.AssignToPrim(ref_prim, purpose="full")
        # UsdShadeMtlx.SetPurpose(stage, "/root/seal", "")

    main()
    stage.Save()
