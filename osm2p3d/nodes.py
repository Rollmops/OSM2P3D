from imposm.parser import OSMParser

class Nodes(dict):
    
    def __init__(self, osm_file, filter=None):
        self.osm_file = osm_file
        self.filter = filter
        osm_parser = OSMParser(concurrency=1, nodes_callback=self._nodes_callback)
        osm_parser.parse(osm_file)
        
        
    def _nodes_callback(self, nodes):
        for node in nodes:
            if self.filter is not None:
                for key, value in self.filter.iteritems():
                    if node[1].get(key, None) == value:
                        self[node[0]] = tuple(node[2])
            else:
                self[node[0]] = tuple(node[2])
        
    