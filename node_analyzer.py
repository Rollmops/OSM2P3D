from resources import known_nodes

class NodeAnalyzer():
    def __init__(self):
        self.nodes = {}
        for key, _ in known_nodes.NODES.items():
            self.nodes[key] = []

    def call(self, nodes):
        for node in nodes:
            for key, value in known_nodes.NODES.items():
                if node[1].get(value[0]) == value[1]:
                    self.nodes[key].append(node)