from pxr import Sdr
import json

# NOTE: this can only be executed via hython 
# TODO: currently this cannot be written to json to do Gf/Vt data types, need to find a way to convert back to original values to be reconverted later down the line 

class Database:
    def __init__(self):
        self.registry = Sdr.Registry()
        self.nodes    = {}
        
        self._get_materialx_nodes()
        self._write_to_json()

    def _write_to_json(self):
        with open("database.json", "w") as file:
            file.write(json.dumps(self.nodes, sort_keys=True, indent=4))

    def _get_materialx_nodes(self):

        # NOTE: this is a very slow and inefficient way of doing this but it only gets executed once and isnt a part of the main functions
        for node in self.registry.GetNodeNames():
            if not node.startswith("ND_"): continue
            
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
                input_property_type     = input_property.GetType()
                input_property_value    = input_property.GetDefaultValue()
                input_property_metadata = input_property.GetMetadata()

                _input["type"]          = input_property_type
                _input["default_value"] = input_property_value
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
                output_property_type     = output_property.GetType()
                output_property_value    = output_property.GetDefaultValue()
                output_property_metadata = output_property.GetMetadata()

                _output["type"]          = output_property_type
                _output["default_value"] = output_property_value
                _output["metadata"]      = output_property_metadata

                outputs[output_property_name] = _output

            _node["inputs"]   = inputs
            _node["outputs"]  = outputs
            _node["metadata"] = metadata

            self.nodes[node] = _node


if __name__ == "__main__":
    Database()