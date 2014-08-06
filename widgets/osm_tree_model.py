from PyQt4.QtCore import QVariant, QModelIndex, Qt, QAbstractItemModel

class OSMTreeItem:
    def __init__(self, parent, row, element, depth=0):
        self.parent = parent
        self.row = row
        self.element = element
        self.check_state = Qt.Checked
        if depth == 0:
            self.children = [OSMTreeItem(self, i, value, depth+1) for i, value in enumerate(element[1])]
            self.display = element[0]
        else:
            self.children = []
            self.display = element

    def setCheckState(self, checked):
        self.check_state = checked
        [c.setCheckState(checked) for c in self.children]


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
        return 1

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
            return node.display
        elif role == Qt.CheckStateRole:
            return node.check_state
        return QVariant()

    def flags(self, index):
        if not index.isValid():
            return None
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsTristate

    def headerData(self, section, orientation, role):
        if (orientation, role) == (Qt.Horizontal, Qt.DisplayRole):
            return QVariant("OSM Entity")
        return QVariant()


    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if role == Qt.CheckStateRole or role:
            index.internalPointer().setCheckState(value)
            self.dataChanged.emit(index, self.createIndex(1,0))
        return True