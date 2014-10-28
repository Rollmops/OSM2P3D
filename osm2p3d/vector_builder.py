import json

class VectorBuilder(object):
    
    def __init__(self):
        with open('resources/vector_config.json') as json_file:
            self.config = json.load(json_file)
            
        print self.config 