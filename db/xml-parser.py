import xml.dom.minidom
from pathlib import Path

xml_file: str = str(Path(__file__).with_name("test.xml"))
xml_doc = xml.dom.minidom.parse(xml_file)
root = xml_doc.documentElement
package = xml_doc.getElementsByTagName("nodedef")


import xml.etree.ElementTree as ET

tree = ET.parse(xml_file)
root = tree.getroot()

children = {}
for child in root:
    # dont need to worry about child.tag as its just nodedef
    # print(child.tag, child.attrib)
    name: str = child.attrib["name"]
    if not name.startswith("ND"):
        continue
    inputs = []
    outputs = []
    children[name] = [inputs, outputs]
    for i in child:
        io_tag = i.tag
        io_attrib = i.attrib

        if io_tag == "input":
            inputs.append(io_attrib)
        elif io_tag == "output":
            outputs.append(io_attrib)

print(children)
