from PyQt5.QtWidgets import QVBoxLayout
from Bulk_DPI_Converter.GUI.LogBox import LogBox
from Bulk_DPI_Converter import __title__, __version__


class LogLayout():
    """
    Log layout.
    The layout contains the custom log box.
    """
    def create_center_layout(self, size_policy) -> QVBoxLayout:
        """
        Creates the log box layout.
        
        Args:
            size_policy (QSizePolicy): the size policy for the buttons.
        
        Returns:
            QVBoxLayout: the layout.
        """
        center_layout = QVBoxLayout()
        self.log_widget = LogBox()
        self.log_widget.textbox.setReadOnly(True)   
        self.log_widget.setMouseTracking(True)
        center_layout.addWidget(self.log_widget)
        return center_layout