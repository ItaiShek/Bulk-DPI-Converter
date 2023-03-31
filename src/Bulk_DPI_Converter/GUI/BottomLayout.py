from PyQt5.QtWidgets import QVBoxLayout, QProgressBar, QPushButton
from PyQt5 import QtCore
from Bulk_DPI_Converter import __title__, __version__


class BottomLayout():
    """
    Bottom layout.
    The layout contains the progress bar and about button.
    """
    def bottom_layout(self, size_policy) -> QVBoxLayout:
        """
        Creates the bottom layout.
        
        Args:
            size_policy (QSizePolicy): the size policy for the buttons.
        
        Returns:
            QVBoxLayout: the layout.
        """
        bottom_layout = QVBoxLayout()
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.about_btn = QPushButton()
        self.about_btn.setText('About')
        self.about_btn.clicked.connect(self.about)
        
        bottom_layout.addWidget(self.progress_bar, 0, QtCore.Qt.AlignCenter)
        bottom_layout.addWidget(self.about_btn, 0, QtCore.Qt.AlignCenter)
        
        return bottom_layout