from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QLabel, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from Bulk_DPI_Converter.GUI import icons


class Row_2():
    """
    Row 2.
    The layout contains the "directories" checkbox, "directories" label, and "start" and "stop" buttons.
    """
    def create_row_2(self, size_policy) -> QHBoxLayout:
        """
        Creates the 2'nd row layout.
        
        Args:
            size_policy (QSizePolicy): the size policy for the buttons.
        
        Returns:
            QHBoxLayout: the layout.
        """
        row_2 = QHBoxLayout()

        # dirs checkbox
        self.dirs_checkbox = QCheckBox()
        self.dirs_checkbox.setChecked(True)
        dirs_label = QLabel(text='Include directories and subdirectories')
        row_2.addWidget(self.dirs_checkbox)
        row_2.addWidget(dirs_label, 1, QtCore.Qt.AlignLeft)
        
        # start/stop buttons
        # icons
        self.start_icon = QIcon(f'{icons}/play.png')
        self.pause_icon = QIcon(f'{icons}/pause.png')
        self.stop_icon = QIcon(f'{icons}/stop.png')

        row_2.addStretch()

        self.start_btn = QPushButton(text='Start')
        self.start_btn.clicked.connect(self.start)        
        self.start_btn.setIcon(self.start_icon)        
        self.start_btn.setStyleSheet('QPushButton {color: #12a40d}')
        row_2.addWidget(self.start_btn)

        self.stop_btn = QPushButton(text='Stop')
        self.stop_btn.setStyleSheet('QPushButton {color: #be0808}')
        self.stop_btn.setIcon(self.stop_icon)
        self.stop_btn.clicked.connect(self.stop)
        row_2.addWidget(self.stop_btn)

        self.stop_btn.setEnabled(False)
        return row_2