import sys
from PyQt5.QtWidgets import QApplication
from Bulk_DPI_Converter.MainWindow import MainWindow
import os.path
from multiprocessing import freeze_support

# set the path for pyinstaller
path = os.path.realpath(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(path)))


if __name__ == "__main__":
    freeze_support()
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())