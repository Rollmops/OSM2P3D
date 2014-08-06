import xml.etree.ElementTree as ET

resources_xml = ET.parse("src/resources/resources.xml").getroot()


def get():
    ret = {}
    for type in resources_xml:
        ret[type.get('name')] = {}
        for node in type:
            ret[type.get('name')][node.get("name")] = (node.get("key"), node.get("value"), [(i, True) for i in node])
    return ret