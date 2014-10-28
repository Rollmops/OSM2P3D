from imposm.parser import OSMParser
import shapefile
import os
import shutil
import tempfile
import subprocess
import glob

class Roads(list):
    ID = '{055DFCA0-253F-4CE6-9982-A6749102079E}'
    def __init__(self, osm_file, coords, nodes, config):

        self.tmp_dir = tempfile.mkdtemp()
        
        self.config = config
        self.osm_file = osm_file
        self.coords = dict(coords.items() + nodes.items())
        
        osm_parser = OSMParser(concurrency=1, ways_callback=self._ways_callback)
        osm_parser.parse(osm_file)

    def _ways_callback(self, ways):
             
        for _, tags, refs in ways:
            for key, values in self.config['roadTags'].iteritems():
                for type, guid in values.iteritems():
                    if tags.get(key) == type:
                        self.append(([list(self.coords[ref]) for ref in refs if ref in self.coords], self.config['vectorShapeProperties'][guid]))

    def create_bgl(self, target, resource_dir, type=3):
        
        w = shapefile.Writer(shapeType=type)
        w.field('Uuid', 'C', '38')
        w.field('Guid', 'C', '38')
        
        for elem in self:
            w.poly(parts=[elem[0]])
            w.record(Roads.ID, elem[1])
        
        w.save(os.path.join(self.tmp_dir, 'ABC1234'))
        shutil.copy(os.path.join(resource_dir, 'roads_shape_xml.xml'), os.path.join(self.tmp_dir, 'ABC1234.xml'))
        
        subprocess.call('%s %s 1234' % (self.config['common']['shp2vec'], self.tmp_dir))
        
        for bgl in glob.glob(os.path.join(self.tmp_dir, '*.bgl')):
            shutil.move(bgl, target)
        
    def __del__(self):
        shutil.rmtree(self.tmp_dir)