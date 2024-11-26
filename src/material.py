from pxr import UsdShade, Sdf, Usd
from typing import Any
from utils import check_path

class UsdShadeMtlxMaterial:
    # add in functionality for purposes
    def __init__(self, stage: Usd.Stage, path: str) -> None:
        self.stage = stage
        self.path = path

        self.__setup()

    def __setup(self) -> None:
        self.material: UsdShade.Material = UsdShade.Material.Define(self.stage, self.path)

    def AssignToPath(self, path, purpose:str = "") -> None:
        # move to lower level api
        path = path if type(path) == Sdf.Path else Sdf.Path(path)
        check_path(path)

        prim = self.stage.GetPrimAtPath(path.pathString)

        if purpose == "":
            relationship = prim.CreateRelationship("material:binding")
            print(type(relationship))
        elif purpose == "preview" or purpose == "full":
            relationship = prim.CreateRelationship(f"material:binding:{purpose}")
        else:
            raise Exception("Given purpose is not valid, either leave empty or use `full` or `preview`")

        relationship.SetTargets([self.path])

    def AssignToPrim(self, prim, purpose:str = "") -> None:
        if purpose:
            if purpose != "preview" and purpose != "full":
                raise Exception("Given purpose is not valid, either leave empty or use `full` or `preview`")
        
        prim.ApplyAPI(UsdShade.MaterialBindingAPI)
        UsdShade.MaterialBindingAPI(prim).Bind(self.material, materialPurpose=purpose.lower())
