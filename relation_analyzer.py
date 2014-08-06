

def relations_callback(relations):
    for relation in relations:
        if relation[1].get('type') == 'multipolygon':
            print relation