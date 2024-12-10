from typing import Dict, Tuple
from pxr import Sdf, Gf
import logging

def time_execution(function):
    def wrapper(*args, **kwargs):
        # wrapper
        import time

        start = time.perf_counter()
        function(*args, **kwargs)
        end = time.perf_counter()
        print(f"{(end - start):.5f}")

    return wrapper

def function_execution_test(num_tests: int = 1, execute=True):
    def inner(function):
        def wrapper(*args, **kwargs):
            import time
            overall_time: float = 0
            for i in range(num_tests):
                i += 1
                start = time.perf_counter()
                function(*args, **kwargs)
                end = time.perf_counter()
                overall_time += (end - start)
                print(f"Test number: {i} | Time to execute: {(end - start):.5f}s")
            print('\n')
            print("Average Execution Time: ")
            print(f"{(overall_time / num_tests):.5f}s")

        return wrapper if execute else None
    return inner


def str_to_sdfpath(path: str) -> Sdf.Path:    
    if not isinstance(path, str) and not isinstance(path, Sdf.Path):
        raise TypeError("Input path must be of type string or Sdf.Path") 
    
    path = path if isinstance(path, Sdf.Path) else Sdf.Path(path)
    if not Sdf.Path.IsValidPathString(path.pathString):
        raise TypeError("Input path is not a valid Sdf.Path, must remove illegal characters before continuing.")

    return path


def string_conversion(string_value) ->str:
    return string_value


def float_conversion(string_value) -> float:
    return float(string_value) if string_value else 0.0


def int_conversion(string_value) -> int:
    return int(string_value) if string_value else 0


def bool_conversion(string_value) -> int:
    if string_value == "false" or string_value == "0":
        converted_bool = 0
    else:
        converted_bool = 1
    return converted_bool


def vector_conversion(string_value, size:int=0):
    # convert string to list
    if not string_value:
        vector = tuple([0.0 for i in range(size)])
    else:
        if ", " not in string_value:
            split_value = string_value.split(",")
        else:
            split_value = string_value.split(", ")
        vector = tuple(map(float, split_value))
    return vector   


def matrix_conversion(string_value, size:int=0):
    if not string_value:
        matrix = tuple([tuple([0.0 for i in range(size)]) for i in range(size)])
    else:
        split_values = string_value.split(", ")
        if len(split_values) <= 4:
            matrix = tuple([tuple(i) for i in split_values])
        else:
            values = list(map(float, split_values))
            matrix = tuple([tuple(values[i:i+4]) for i in range(0, len(values), 4)])
    return matrix


def converted_value_types() -> Dict[str, Sdf.ValueTypeNames]:
    """
    contains the converted value types from string to sdf
    """
    types = {
        "string": [Sdf.ValueTypeNames.String, string_conversion],
        "float": [Sdf.ValueTypeNames.Float, float_conversion],
        "integer": [Sdf.ValueTypeNames.Int, int_conversion],
        "color3": [Sdf.ValueTypeNames.Color3f, vector_conversion, 3],
        "color4": [Sdf.ValueTypeNames.Color4f, vector_conversion, 4],
        "vector2": [Sdf.ValueTypeNames.Float2, vector_conversion, 2],
        "vector3": [Sdf.ValueTypeNames.Vector3f, vector_conversion, 3],
        "vector4": [Sdf.ValueTypeNames.Float4, vector_conversion, 4],
        "matrix33": [Sdf.ValueTypeNames.Matrix3d, matrix_conversion, 3],
        "matrix44": [Sdf.ValueTypeNames.Matrix4d, matrix_conversion, 4],
        "boolean": [Sdf.ValueTypeNames.Bool, bool_conversion],
    }

    return types


def check_path(path: Sdf.Path) -> bool:
    #if path.isEmpty: logging.error("Given path is empty, please provide a valid path."); return 0
    if not Sdf.Path.IsValidPathString(path.pathString): raise Exception("Found forbidden characters in path.")
    if path.isEmpty: raise Exception("The given path is empty, please provide a valid path.")
    return 1

if __name__ == "__main__":
    path = None
    # print(check_path(path))
    str_to_sdfpath(path="wrong")
    # sample = '0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0'
