from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from PyQt5 import QtCore

class Row_1():
    """
    Row 1.
    The layout contains the "select files" button, and "thread" edit box.
    """
    def create_row_1(self, size_policy) -> QHBoxLayout:
        """
        Creates the 1'st row layout.
        
        Args:
            size_policy (QSizePolicy): the size policy for the buttons.
        
        Returns:
            QHBoxLayout: the layout.
        """
        row_1 = QHBoxLayout()
        # "select files" button
        self.select_btn = QPushButton(text='Select files')
        
        self.select_btn.clicked.connect(self.select_files)
        row_1.addWidget(self.select_btn)
        
        # threads
        thread_label = QLabel(text='Number of threads:')
        self.thread_edit = QLineEdit()
        self.thread_edit.setText('5')   # default number of threads: 5
        self.thread_edit.setValidator(QRegExpValidator(QRegExp('^(?!0)+[0-9]{3}'))) # accept values in the range 1-999
        self.thread_edit.textChanged.connect(lambda: self.start_btn.setEnabled(self.thread_edit.text() != ''))
        self.thread_edit.setSizePolicy(size_policy)
        
        row_1.addStretch()

        row_1.addWidget(thread_label, 0, QtCore.Qt.AlignRight)
        row_1.addWidget(self.thread_edit)

        return row_1