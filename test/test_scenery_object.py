import xml.etree.ElementTree as ET

from osm2p3d.scenery_object import LibraryObject

s = LibraryObject(name='huhu', lat=1.3, lon=1.5)

ET.dump(s)

