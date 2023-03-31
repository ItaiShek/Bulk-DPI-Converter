from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QCheckBox, QHBoxLayout, QMenu, QAction, QActionGroup
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from PyQt5 import QtCore


class Row_3():
    """
    Row 3.
    The layout contains the "dpi" label and edit box, "Apply to" menu, and the "overwrite" checkbox and edit box.
    """
    def create_row_3(self, size_policy) -> QHBoxLayout:
        """
        Creates the 3'rd row layout.
        
        Args:
            size_policy (QSizePolicy): the size policy for the buttons.
        
        Returns:
            QHBoxLayout: the layout.
        """
        def toggle_apply(option: bool) -> None:
            self.apply = option

        row_3 = QHBoxLayout()
        # DPI
        # label
        dpi_label = QLabel(text='DPI:')
        self.dpi_edit= QLineEdit()
        self.dpi_edit.setText('300')
        self.dpi_edit.textChanged.connect(lambda: self.start_btn.setEnabled(self.dpi_edit.text() != ''))
        row_3.addWidget(dpi_label)
        # edit box
        self.dpi_edit.setValidator(QRegExpValidator(QRegExp('[0-9]{5}'))) # accept values in the range 0-99999
        self.dpi_edit.setSizePolicy(size_policy)
        row_3.addWidget(self.dpi_edit)
        # menu
        menu = QMenu()
        self.option_1 = QAction(text='Lower resolution images')
        self.option_1.setCheckable(True)
        self.option_1.setChecked(True)
        self.option_1.triggered.connect(lambda: toggle_apply(True))
        
        self.option_2 = QAction(text='All selected images')
        self.option_2.setCheckable(True)
        self.option_2.triggered.connect(lambda: toggle_apply(False))

        ag = QActionGroup(menu)
        ag.addAction(self.option_1)
        ag.addAction(self.option_2)        
        ag.setExclusive(True)

        menu.addAction(self.option_1)
        menu.addAction(self.option_2)
        self.dpi_menu = QPushButton('Apply to')
        self.dpi_menu.setMenu(menu)

        row_3.addWidget(self.dpi_menu, 1, QtCore.Qt.AlignLeft)

        row_3.addStretch()

        self.overwrite_check = QCheckBox('Overwrite files')
        self.overwrite_check.setChecked(True)
        self.overwrite_check.clicked.connect(lambda: self.overwrite_edit.setEnabled(not(self.overwrite_check.isChecked())))        

        self.overwrite_edit = QLineEdit()
        # disallow characters that windows doesn't allow for files and directories. Limit the file postfix to 50 characters.
        self.overwrite_edit.setValidator(QRegExpValidator(QRegExp(r'^(?!.*[<>:"/\\|?*]).{50}$')))
        self.overwrite_edit.setText('_new')
        self.overwrite_edit.setEnabled(False)
        row_3.addWidget(self.overwrite_check)
        row_3.addWidget(self.overwrite_edit)
        
        return row_3