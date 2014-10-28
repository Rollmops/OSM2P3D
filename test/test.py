from osm2p3d.coords import Coords
from osm2p3d.nodes import Nodes
from osm2p3d.roads import Roads
from optparse import OptionParser
import json
import os


if __name__ == '__main__':
    
    parser = OptionParser()
    parser.add_option('--osm-file', dest='osm_file', help='The osm file you want to parse.')
    parser.add_option('--resource-dir', dest='resource_dir', default='../resources/')
    parser.add_option('--shp2vec', dest='shp2vec', help='Target to the shp2vec program')
    parser.add_option('--target', dest='target')
    
    (options, _) = parser.parse_args()
    
    vector_config = dict()
    
    with open(os.path.join(options.resource_dir, 'vector_config.json'), 'r') as config_file:
        vector_config = json.load(config_file)

    print('Collecting nodes and coords...')
    coords = Coords(options.osm_file)
    nodes = Nodes(options.osm_file)
    print('Done.')
    
    print('Creating roads...')  
    roads = Roads(options.osm_file, coords=coords, nodes=nodes, config=vector_config)
    print('Done.')

    print('Creating and saving shapefile to %s...' % options.target)    
    roads.create_bgl( target=options.target, resource_dir=options.resource_dir )
    print('Done.')
