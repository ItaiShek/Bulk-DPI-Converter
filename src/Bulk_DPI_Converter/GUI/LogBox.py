from PyQt5.QtWidgets import QWidget, QGridLayout, QToolButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5 import QtGui, QtCore

from Bulk_DPI_Converter.GUI.CustomQTextEdit import CustomQTextEdit
from Bulk_DPI_Converter.GUI import icons


class LogBox(QWidget):
    """
    Custom QTextEdit with clear button.
    """   
    def __init__(self) -> None:
        """
        Initialize the custom widget.
        Creates a text box, and a "clear" button that's only visible when the cursor is inside the text box.
        """
        super().__init__()
        self.setMouseTracking(True)

        layout = QGridLayout(self)
        num=50
        [layout.setColumnStretch(i, 1) for i in range(num)]
        [layout.setRowStretch(i, 1) for i in range(num)]

        # Log textbox
        self.textbox = CustomQTextEdit()

        # Clear button
        self.clear_btn = QToolButton()
        self.clear_btn.setIcon(QIcon(f'{icons}/trash-can-icon.png'))
        icon_size = 30
        self.clear_btn.setIconSize(QSize(icon_size, icon_size))
        self.clear_btn.setStyleSheet('QToolButton {background-color: transparent; border: 0;}')
        self.clear_btn.hide()
        self.textbox.mouse_hover.connect(self.clear_btn.setVisible)
        self.clear_btn.clicked.connect(lambda: self.textbox.clear())
                
        layout.addWidget(self.textbox, 0, 0, num, num)
        layout.addWidget(self.clear_btn, 1, num-2)

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        """
        Hides the button when the mouse is over the QTextEdit widget.

        Args:
            a0 (QtGui.QMouseEvent): the event.
        """
        if not self.textbox.underMouse() and self.clear_btn.isVisible():
            self.clear_btn.hide()            
        return super().mouseMoveEvent(a0)
    
    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        """
        Hides the clear button when leaving the widget.

        Args:
            a0 (QtCore.QEvent): the event.
        """        
        self.clear_btn.hide()            
        return super().leaveEvent(a0)