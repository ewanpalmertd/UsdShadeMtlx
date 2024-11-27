"""
This test is to determine the most efficient USD API for creating and assigning materials & shaders

Tests to run:
1. Core USD API, using the higher level API to create attributes/relationships (slower but more efficient)
2. Sdf API, the lower level API (much faster but less efficient)
3. UsdShade Schema, (the most efficient but speed unknown relative to other APIs)

The test will be to create a simple bsdf shader and assign it to a cube, if this is too fast then I will switch
to assigning to a reference instead
"""

from test_utils import function_execution_test, time_execution
from pxr import Usd, Sdf, UsdShade

# @function_execution_test(num_tests=4)
@time_execution
def test_usd_core():
    stage = Usd.Stage.CreateNew("test_usd_core.usda")
    
    # creating prims
    cube = stage.DefinePrim(Sdf.Path("/cube"), "Cube")
    mtl_path = Sdf.Path("/materials/mtl_test")
    material = stage.DefinePrim(mtl_path, "Material")

    shader = stage.DefinePrim(mtl_path.AppendChild("usdpreviewsurface"), "Shader")
    shader.ApplyAPI("NodeDefAPI")
    shader_attr = shader.CreateAttribute("info:id", Sdf.ValueTypeNames.Token)
    shader_attr.Set("UsdPreviewSurface")
    shader_color_attr = shader.CreateAttribute("inputs:diffuseColor", Sdf.ValueTypeNames.Color3f)
    shader_color_attr.Set((1.0, 0.0, 0.0))
    shader_output = shader.CreateAttribute("outputs:surface", Sdf.ValueTypeNames.Token)
    
    material_output = material.CreateAttribute("outputs:surface", Sdf.ValueTypeNames.Token)
    material_output.AddConnection(Sdf.Path('/materials/mtl_test/usdpreviewsurface.outputs:surface'), Usd.ListPositionFrontOfAppendList)

    rel = cube.CreateRelationship("material:binding", custom=False)
    rel.SetTargets([mtl_path])


    stage.Save()
    return

# @function_execution_test(num_tests=4)
@time_execution
def test_sdf():
    layer = Sdf.Layer.CreateNew("test_sdf.usda")
    
    cube_spec = Sdf.CreatePrimInLayer(layer, Sdf.Path("/cube"))
    cube_spec.specifier = Sdf.SpecifierDef
    cube_spec.typeName = "Cube"

    mtl_path = Sdf.Path("/materials/mtl_test")
    material_spec = Sdf.CreatePrimInLayer(layer, mtl_path)
    material_spec.specifier = Sdf.SpecifierDef
    material_spec.typeName = "Material"
    material_spec.nameParent.specifier = Sdf.SpecifierDef

    shader_spec = Sdf.CreatePrimInLayer(layer, mtl_path.AppendChild("usdpreviewsurface"))
    shader_spec.specifier = Sdf.SpecifierDef
    shader_spec.typeName = "Shader"

    # create shader attributes
    shader_attr = Sdf.AttributeSpec(shader_spec, "info:id", Sdf.ValueTypeNames.Token)
    shader_attr.default = "UsdPreviewSurface"
    shader_attr.SetInfo("variability", Sdf.VariabilityUniform)
    shader_color_attr = Sdf.AttributeSpec(shader_spec, "inputs:diffuseColor", Sdf.ValueTypeNames.Color3f)
    shader_color_attr.default = (1.0, 0.0, 0.0)
    shader_output_spec = Sdf.AttributeSpec(shader_spec, "outputs:surface", Sdf.ValueTypeNames.Token)

    # create material attributes
    material_output_attr = Sdf.AttributeSpec(material_spec, "outputs:surface", Sdf.ValueTypeNames.Token)
    material_output_attr.connectionPathList.Append(shader_output_spec.path)

    # assign material
    rel_spec = Sdf.RelationshipSpec(cube_spec, "material:binding", custom=False)
    rel_spec.targetPathList.Append(material_spec.path)


    layer.Save()
    return

# @function_execution_test(num_tests=4)
@time_execution
def test_usdshade():
    stage = Usd.Stage.CreateNew("test_usdshade.usda")
    cube = stage.DefinePrim(Sdf.Path("/cube"), "Cube")
    mtl_path = Sdf.Path("/materials/mtl_test")
    material = UsdShade.Material.Define(stage, mtl_path)

    shader = UsdShade.Shader.Define(stage, mtl_path.AppendChild("usdpreviewsurface"))
    shader.CreateIdAttr("UsdPreviewSurface")
    shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set((1.0, 0.0, 0.0))
    shader.CreateOutput("surface", Sdf.ValueTypeNames.Token)

    material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")
    UsdShade.MaterialBindingAPI(cube).Bind(material)

    stage.Save()
    return

if __name__ == "__main__":
    print(" USD CORE TEST:")
    test_usd_core()
    print('\n')
    print(" USD SDF TEST:")
    test_sdf()
    print('\n')
    print(" USD SHADE TEST:")
    test_usdshade()

    # NOTE: Final Outcome: {}