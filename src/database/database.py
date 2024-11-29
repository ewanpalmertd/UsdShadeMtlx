from pxr import Sdf
from typing import List
import json


def time_execution(function):
    def wrapper(*args, **kwargs):
        # wrapper
        import time

        start = time.perf_counter()
        function(*args, **kwargs)
        end = time.perf_counter()
        print(f"{(end - start):.5f}")

    return wrapper

# NOTE: might switch class functionality to single node rather than managing the entire database as it doesnt seem to necessary
# TODO: add search function in here

class DatabaseItem:

    @time_execution
    def __init__(self, node=None):
        with open("database.json") as file:
            self.data = json.load(file)

        if not node in self.data.keys(): raise Exception("invalid node")
        self.node = node
        self.__convert_data(node)


    def __convert_data(self, node: str):
        # TODO: convert type names from str to Sdf.ValueTypeName
        inputs = self.data[node]["inputs"]
        for input_attribute in inputs.keys():
            inputs[input_attribute]["type"] = getattr(Sdf.ValueTypeNames, inputs[input_attribute]["type"])

        outputs = self.data[node]["outputs"]
        for output_attribute in outputs.keys():
            outputs[output_attribute]["type"] = getattr(Sdf.ValueTypeNames, outputs[output_attribute]["type"])

    def __check_input(self, input):
        if not input in self.data[self.node]["inputs"].keys(): raise Exception("Inavlid input") 

    def __check_output(self, input):
        if not input in self.data[self.node]["inputs"].keys(): raise Exception("Inavlid output") 
    
    def Inputs(self) -> None:
        return list( self.data[self.node]["inputs"].keys() )
    
    def Outputs(self) -> None:
        return list( self.data[self.node]["outputs"].keys() )

    def Metadata(self) -> None:
        return self.data[self.node]["metadata"]


    # NOTE: might switch IO to its own class which would be more efficient, but might be too overkill
    def InputType(self, input) -> None:
        self.__check_input(input)
        return self.data[self.node]["inputs"][input]["type"]
    
    def InputValue(self, input) -> None:
        self.__check_input(input)
        return self.data[self.node]["inputs"][input]["default_value"]
    
    def InputMetadata(self, input) -> None:
        self.__check_input(input)
        return self.data[self.node]["inputs"][input]["metadata"]
    
    def OutputType(self, output) -> None:
        self.__check_output(output)
        return self.data[self.node]["outputs"][output]["type"]
    
    def OutputValue(self, output) -> None:
        self.__check_output(output)
        return self.data[self.node]["outputs"][output]["default_value"]
    
    def OutputMetadata(self, output) -> None:
        self.__check_output(output)
        return self.data[self.node]["outputs"][output]["metadata"]
    
    @staticmethod
    def GetNodes() -> List[str]:
        with open("database.json") as file:
            data = json.load(file)
        return list(data.keys())


if __name__ == "__main__":
    a = DatabaseItem("ND_standard_surface_surfaceshader_100")
    print(DatabaseItem.GetNodes())