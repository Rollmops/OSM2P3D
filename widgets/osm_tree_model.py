from PyQt4.QtCore import QVariant, QModelIndex, Qt, QAbstractItemModel

class OSMTreeItem:
    def __init__(self, parent, row, element, depth=0):
        self.parent = parent
        self.row = row
        self.element = element
        self.display = (element[0], None)
        if depth == 0:
            self.children = [OSMTreeItem(self, i, value, depth+1) for i, value in enumerate(element[1])]
            self.display = (element, "blubb")
        else:
            self.children = []




class OSMTreeViewModel(QAbstractItemModel):
    def __init__(self, osm_resource):
        super(OSMTreeViewModel, self).__init__()
        self.osm_resource = osm_resource
        self.nodes = [OSMTreeItem(None, i, (type, value)) for i, (type, value) in enumerate(osm_resource.items())]


    def index(self, row, column, parent):
        if not self.nodes:
            return QModelIndex()
        if not parent.isValid():
            return self.createIndex(row, column, self.nodes[row])
        node = parent.internalPointer()
        return self.createIndex(row, column, node.children[row])

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        node = index.internalPointer()
        if node.parent is None:
            return QModelIndex()
        else:
            return self.createIndex(node.parent.row, 0, node.parent)

    def columnCount(self, parent):
        return 2

    def rowCount(self, parent):
        if not parent.isValid():
            return len(self.nodes)
        node = parent.internalPointer()
        return len(node.children)

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        node = index.internalPointer()
        if role == Qt.DisplayRole:
            return node.display[index.column()]
        return QVariant()

    def flags(self, index):
        if not index.isValid():
            return None
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if (orientation, role) == (Qt.Horizontal, Qt.DisplayRole):
            return ["OSM Entity", "Description"][section]
        return QVariant()


    def setData(self, QModelIndex, QVariant, int_role=None):
        return True