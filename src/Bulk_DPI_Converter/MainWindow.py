from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout

from Bulk_DPI_Converter import __title__, __version__, __license__, __copyright__

from Bulk_DPI_Converter.GUI.StartThread import StartThread
from Bulk_DPI_Converter.GUI.GUI import GUI
from Bulk_DPI_Converter.Functions.Functions import Functions


class MainWindow(QWidget, GUI, Functions):
    """
    The main window.
    """
    def __init__(self) -> None:
        """
        Initializes some of the class member variables, the other member variable are in the other GUI functions that are called in "initUI" method.
        """
        super().__init__()
        self.setWindowTitle(f'{__title__} - Version: {__version__}')
        self.initUI()

        self.files = ()
        self.apply = True   # True - apply to lower resolution images, False - apply to all images.

        self.start_thread = StartThread(self)
        self.start_thread.finished.connect(self.end)
        self.start_thread.append_log.connect(lambda x: self.append_log(x))
        self.start_thread.update_progress.connect(lambda x: self.progress_bar.setValue(x))

    def initUI(self) -> None:
        """
        Creates the GUI.
        """
        size_policy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        
        layout = QVBoxLayout(self)

        top_layout = QVBoxLayout()        
        
        row_1 = self.create_row_1(size_policy)
        top_layout.addLayout(row_1)

        row_2 = self.create_row_2(size_policy)
        top_layout.addLayout(row_2)
        
        row_3 = self.create_row_3(size_policy)
        top_layout.addLayout(row_3)

        layout.addLayout(top_layout)

        center_layout = self.create_center_layout(size_policy)
        layout.addLayout(center_layout)

        bottom_layout = self.bottom_layout(size_policy)
        layout.addLayout(bottom_layout)