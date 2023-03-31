from PyQt5.QtWidgets import QTextEdit
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal


class CustomQTextEdit(QTextEdit):
    """
    Custom QTextEdit that handles enterEvent signal (for the "clear" button).
    """
    mouse_hover = pyqtSignal(bool)

    def __init__(self) -> None:
        """
        Initialize (just call super).
        """
        super().__init__()
        
    def enterEvent(self, a0: QtCore.QEvent) -> None:
        """
        Handles the event when the cursor enters the widget.
        
        Args:
            a0 (QtCore.QEvent): the event.

        Returns:
            bool:   True - when entering text box area.
                    False - any other event.
        """
        self.mouse_hover.emit(True)
        return super().enterEvent(a0)