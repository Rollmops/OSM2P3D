from optparse import OptionParser
import sys

from PyQt4.QtGui import QApplication

from src.widgets.main_window import MainWindow


if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("--osm-file", dest="osm_file", help="Denotes the OSM file to load", default=None)

    (options, _) = parser.parse_args()

    QApplication.setOrganizationName('RollmopsDevelopment')
    QApplication.setOrganizationDomain('rollmopsdevelopment.com')
    QApplication.setApplicationName('OSM2P3D')

    app = QApplication(sys.argv)

    window = MainWindow(osm_file=options.osm_file)
    window.show()

    sys.exit(app.exec_())


