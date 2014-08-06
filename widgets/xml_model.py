from PyQt4.QtCore import QAbstractItemModel, Qt, SIGNAL, QModelIndex, QVariant
from PyQt4.QtGui import QCheckBox


class TreeNode(object):
    def __init__(self, parent, row, element):
        self.parent = parent
        self.row = row
        self.element = (element.get('name'), element.get('url'))
        self.children = [TreeNode(self, i, sub_element) for i, sub_element in enumerate(element)]

class TreeModel(QAbstractItemModel):
    def __init__(self, xml):
        super(TreeModel, self).__init__()
        self.xml = xml
        self.nodes = [TreeNode(None, i, continent) for i, continent in enumerate(xml.iter('continent'))]


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
        if role == Qt.DisplayRole and index.column() == 0:
            return node.element[0]
        return QVariant()

    def flags(self, index):
        if not index.isValid():
            return None
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if(orientation, role) == (Qt.Horizontal, Qt.DisplayRole):
            return QVariant("Regions")

    def setData(self, QModelIndex, QVariant, int_role=None):
        return True
