from pxr import UsdShade, Sdf, Usd

class UsdShadeMtlxMaterial:
    # add in functionality for purposes
    def __init__(self, stage: Usd.Stage, path: str) -> None:
        self.stage = stage
        self.path = path

        self.__setup()

    def __setup(self) -> None:
        self.material: UsdShade.Material = UsdShade.Material.Define(self.stage, self.path)

    def AssignToPath(self, path) -> None:
        # move to lower level api
        # create error handling for incorrect stage/path usage
        prim = self.stage.GetPrimAtPath(path)
        relationship = prim.CreateRelationship("material:binding")
        relationship.SetTargets([self.path])

    def AssignToPrim(self, prim) -> None:
        prim.ApplyAPI(UsdShade.MaterialBindingAPI)
        UsdShade.MaterialBindingAPI(prim).Bind(self.material)