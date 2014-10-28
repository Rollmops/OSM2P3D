import xml.etree.ElementTree as ET


class BaseObject(ET.Element):
    
    def __init__(self, name, needed, default, **kwargs):
        
        
        
        super(BaseObject, self).__init__(name)
        
        
        pass

class SceneryObject(ET.Element):
    
    NEEDED_ATTRIBUTES = ['lat', 'lon']
    DEFAULT_ATTRIBUTES = {'alt': '0', 'altitudeIsAgl': 'TRUE', 'pitch': '0'}
    
    
    def __init__(self, **kwargs):
        
        super(SceneryObject, self).__init__('SceneryObject', attrib=dict([(a, str(x)) for a, x in kwargs.iteritems() if a in SceneryObject.NEEDED_ATTRIBUTES]))
        
        
class LibraryObject(SceneryObject):
    NEEDED_ATTRIBUTES = ['name']
    DEFAULT_ATTRIBUTES = {'scale': '1.0'}
    def __init__(self, **kwargs):
        super(LibraryObject, self).__init__(**kwargs)
        
        libraryElem = ET.Element('LibraryObject', attrib=dict([(a, str(x)) for a, x in kwargs.iteritems() if a in LibraryObject.NEEDED_ATTRIBUTES])) 
        
        for key, value in LibraryObject.DEFAULT_ATTRIBUTES.iteritems():
            libraryElem.set(key, value)
        
        self.append(libraryElem)
        
        
        
