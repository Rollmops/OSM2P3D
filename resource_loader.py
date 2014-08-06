import xml.etree.ElementTree as ET

resources_xml = ET.parse("resources.xml").getroot()


def get():
    ret = {}
    for type in resources_xml:
        ret[type.get('name')] = {}
        for node in type:
            ret[type.get('name')][node.get("name")] = (node.get("key"), node.get("value"), [i for i in node])
    return ret