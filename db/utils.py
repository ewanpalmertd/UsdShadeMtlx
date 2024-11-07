from typing import Dict
from pxr import Sdf

def time_execution(function):
    def wrapper(*args, **kwargs):
        # wrapper
        import time

        start = time.perf_counter()
        function(*args, **kwargs)
        end = time.perf_counter()
        print(f"{(end - start):.5f}")

    return wrapper

def converted_value_types() -> Dict[str, Sdf.ValueTypeNames]:
    """
    contains the converted value types from string to sdf
    """
    types = {
    "string": Sdf.ValueTypeNames.String,
    "float": Sdf.ValueTypeNames.Float,
    "integer": Sdf.ValueTypeNames.Int,
    "color3": Sdf.ValueTypeNames.Color3f,
    "color4": Sdf.ValueTypeNames.Color4f,
    "vector2": Sdf.ValueTypeNames.Float2,
    "vector3": Sdf.ValueTypeNames.Vector3f,
    "vector4": Sdf.ValueTypeNames.Float4,
    "vector2array": Sdf.ValueTypeNames.Float2Array,
    "matrix33": Sdf.ValueTypeNames.Matrix3d,
    "matrix44": Sdf.ValueTypeNames.Matrix4d,
    "boolean" : Sdf.ValueTypeNames.Bool,
    }

    return types