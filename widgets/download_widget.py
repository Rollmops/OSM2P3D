from PyQt4.QtGui import QDialog, QAbstractItemView, QItemSelectionModel
from PyQt4 import uic, QtCore
from xml_model import TreeModel
import threading, urllib2, time
import xml.etree.ElementTree as ET

class DownloadThread(threading.Thread):
    def __init__(self):
        super(DownloadThread, self).__init__()
        self._stop = threading.Event()
        self.url = ""

    def set_url(self, url):
        self.url = url

    def run(self):
        time.sleep(40)
        try:
            file_name = self.url.split('/')[-1]
            response = urllib2.urlopen(self.url)
        except:
            pass

    def stop(self):
        self._stop.set()



class DownloadWidget(QDialog):
    def __init__(self, parent=None):
        super(DownloadWidget, self).__init__(parent)
        self.url_list = []
        self.download_thread = DownloadThread()

        uic.loadUi('ui/download.ui', self)
        self.buttonDownload.setEnabled(False)

        self.xml = ET.parse('config.xml').getroot().find('download')

        model = TreeModel(self.xml)
        self.treeView.setModel(model)
        self.treeView.setSelectionMode(QAbstractItemView.MultiSelection)

        self.buttonCancel.pressed.connect(self.close)
        self.buttonDownload.pressed.connect(self.start_download)
        self.progressBarDownload.setVisible(False)

        self.connect(self.treeView.selectionModel(), QtCore.SIGNAL("selectionChanged(QItemSelection, QItemSelection)"),
                     self.selection_changed)

    def selection_changed(self, _, __):
        self.url_list = []
        num_selected = len(self.treeView.selectedIndexes())
        self.buttonDownload.setEnabled(num_selected)
        self.buttonDownload.setText('Download (%d)' % num_selected)

        for idx in self.treeView.selectedIndexes():
            url = self.xml.find('baseUrl').text + '/' + idx.internalPointer().element[1] + self.xml.find('suffix').text
            self.url_list.append((url, idx.internalPointer().element[0]))


    def start_download(self):
        if self.buttonDownload.text() == "Cancel":
            self.download_thread.stop()
            self.progressBarDownload.setVisible(False)
            self.buttonDownload.setText('Download (%d)' % len(self.treeView.selectedIndexes()))
        else:
            self.progressBarDownload.setVisible(True)
            for url in self.url_list:
                self.download_thread.set_url(url)
                self.download_thread.start()
                self.buttonDownload.setText("Cancel")
