from PyQt4.QtGui import QMainWindow, qApp, QFileDialog, QMessageBox
from PyQt4 import uic, QtCore
import resource_loader
from widgets.download_widget import DownloadWidget
from widgets.osm_tree_model import OSMTreeViewModel


class MainWindow(QMainWindow):
    def __init__(self, osm_file=None):
        super(MainWindow, self).__init__()
        uic.loadUi('ui/mainwindow.ui', self)
        self.setWindowFlags(QtCore.Qt.Tool)

        self.osm_file = osm_file
        self.load_resources()

        self.action_Quit.triggered.connect(qApp.quit)
        self.buttonOSMBrowse.clicked.connect(self.load_osm_file)
        self.buttonDownloadOSM.clicked.connect(self.show_download_widget)

        if self.osm_file is not None:
            self.textOSMFile.setText(self.osm_file)

        osm_model = OSMTreeViewModel(self.resources)
        self.osmResourceTreeView.setModel(osm_model)
        self.osmResourceTreeView.setColumnWidth(0,self.width() / 2.5)


    def show_download_widget(self):
        DownloadWidget(self).show()

    def load_osm_file(self):
        file_name = QFileDialog.getOpenFileName(self, "Open OSM file", "", "OSM Files (*.osm.pbf *.osm.bz2)")
        if file_name:
            self.osm_file = file_name
            self.textOSMFile.setText(self.osm_file)

    def load_resources(self):
        self.resources = {}
        self.statusBar().showMessage("Loading resources...")
        self.resources = resource_loader.get()
        self.statusBar().showMessage("Ready.")

        # def download_osm(self):
        # osm_url = str(self.textOSMFile.text())
        #     try:
        #         file_name = osm_url.split('/')[-1]
        #         response = urllib2.urlopen(osm_url)
        #         self.textOSMFile.setEnabled(False)
        #         with open(file_name, 'wb') as f:
        #             meta = response.info()
        #             file_size = int(meta.getheaders("Content-Length")[0])
        #             self.statusBar().showMessage("Downloading: %s Bytes: %s" % (file_name, file_size))
        #
        #             file_size_dl = 0
        #             block_sz = 8192
        #             self.progressBarDownload.setVisible(True)
        #             self.progressBarDownload.setValue(0)
        #             self.progressBarDownload.setMinimum(0)
        #             self.progressBarDownload.setMaximum(file_size)
        #             while True:
        #                 buffer = response.read(block_sz)
        #                 if not buffer:
        #                     break
        #                 file_size_dl += len(buffer)
        #                 f.write(buffer)
        #                 self.progressBarDownload.setValue(file_size_dl)
        #
        #             if file_size_dl == file_size:
        #                 self.statusBar().showMessage("Finished downloading %s" % file_name)
        #     except urllib2.URLError, e:
        #         QMessageBox.critical(self, "Downloading %s" % file_name, str(e.reason))
        #     except Exception, e:
        #         QMessageBox.critical(self, "Downloading %s" % file_name, str(e.message))
        #     finally:
        #         self.textOSMFile.setEnabled(True)
