from imposm.parser import OSMParser

class Coords(dict):
    
    def __init__(self, osm_file):
        self.osm_file = osm_file
        osm_parser = OSMParser(concurrency=1, coords_callback=self._coords_callback)
        osm_parser.parse(osm_file)
        
        
    def _coords_callback(self, coords):
        for coord in coords:
            self[coord[0]] = tuple(coord[1:])
        
    