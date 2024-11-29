from pxr import Sdr, Sdf, Gf, Vt
import json

# NOTE: this can only be executed via hython 
# TODO: currently this cannot be written to json to do Gf/Vt data types, need to find a way to convert back to original values to be reconverted later down the line 
# TODO: check what type of value are currently causing issues with json
# TODO: create list of all uniqwue types and reverse engineer from there

# NOTE: convert all data to string and convert all types to string and resolve for example ("pxr.Gf.Vec3f", "(0, 0, 0)"): "pxr.Gf.Vec3f": pxr.Gf.Vec3f only need to do this with json incompatible types

class Database:
    def __init__(self):
        self.registry = Sdr.Registry()
        self.nodes    = {}
        self.types = [type for type in dir(Sdf.ValueTypeNames) if not type.startswith("__")]
        self._get_materialx_nodes()
        self._write_to_json()

    def _write_to_json(self):
        with open("database.json", "w") as file:
            file.write(json.dumps(self.nodes, sort_keys=True, indent=4))

    def __is_matrix(self, input):
        matrix_types = [Gf.Matrix2d, Gf.Matrix2f, Gf.Matrix3d, Gf.Matrix3f, Gf.Matrix4d, Gf.Matrix4f]
        if type(input) in matrix_types:
            return True
        return False
    
    def __is_vec(self, input):
        vec_types = [Gf.Vec2d, Gf.Vec2f, Gf.Vec2h, Gf.Vec2i, Gf.Vec3d, Gf.Vec3f, Gf.Vec3h, Gf.Vec3i, Gf.Vec4d, Gf.Vec4f, Gf.Vec4h, Gf.Vec4i]
        if type(input) in vec_types:
            return True
        return False
    
    def __convert_values(self, input):
        # converting Gf types to JSON serialized values, need to find a way to reconvert
        # NOTE: need to add a way to distinguish between doubles and floats, not a high prio
        if self.__is_matrix(input):
            converted_value = tuple([tuple(i) for i in input])
        elif self.__is_vec(input):
            converted_value = tuple(input)
        else:
            converted_value = input
        return converted_value
    
    def __convert_types(self, type):

        string_type = str(type[0])
        if string_type[-2:] == "[]": string_type = string_type.replace("[]", "array")
        return [type for type in self.types if type.lower() == string_type][0]

    def _get_materialx_nodes(self):

        # NOTE: this is a very slow and inefficient way of doing this but it only gets executed once and isnt a part of the main functions
        self._types=[]
        for node in self.registry.GetNodeNames():
            if not node.startswith("ND_"): continue
            # if not node == "ND_standard_surface_surfaceshader_100": continue
            
            shader_node  = self.registry.GetShaderNodeByIdentifier(node)
            input_names  = shader_node.GetInputNames()
            output_names = shader_node.GetOutputNames()
            metadata     = shader_node.GetMetadata()

            _node  = {}
            inputs = {}
            for input in input_names:
                """
                input_name : {
                             type : Sdf.ValueTypeName,
                             default_value : Any,
                             metadata : {name : value}
                             }
                """
                _input = {}
                input_property          = shader_node.GetInput(input)
                input_property_name     = input_property.GetName()
                input_property_type     = input_property.GetTypeAsSdfType()
                input_property_value    = input_property.GetDefaultValue()
                input_property_metadata = input_property.GetMetadata()

                converted_type  = self.__convert_types(input_property_type)
                converted_value = self.__convert_values(input_property_value)

                _input["type"]          = converted_type
                _input["default_value"] = converted_value
                _input["metadata"]      = input_property_metadata

                inputs[input_property_name] = _input

            outputs = {}
            for output in output_names:
                """
                output_name : {
                             type : Sdf.ValueTypeName,
                             default_value : Any,
                             metadata : {name : value}
                             }
                """
                _output = {}
                output_property          = shader_node.GetOutput(output)
                output_property_name     = output_property.GetName()
                output_property_type     = output_property.GetTypeAsSdfType()
                output_property_value    = output_property.GetDefaultValueAsSdfType()
                output_property_metadata = output_property.GetMetadata()

                converted_type  = self.__convert_types(output_property_type)

                if type(output_property_value) == Vt.StringArray:
                    converted_value = [[]]
                elif type(output_property_value) == Vt.Vec3fArray or type(output_property_value) == Vt.Vec4fArray:
                    converted_value = []
                else:
                    converted_value = self.__convert_values(output_property_value)

                _output["type"]          = converted_type
                _output["default_value"] = converted_value
                _output["metadata"]      = output_property_metadata

                outputs[output_property_name] = _output

            _node["inputs"]   = inputs
            _node["outputs"]  = outputs
            _node["metadata"] = metadata

            self.nodes[node] = _node


if __name__ == "__main__":
    Database()