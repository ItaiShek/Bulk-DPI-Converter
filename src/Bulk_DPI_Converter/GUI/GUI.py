from Bulk_DPI_Converter import __title__, __version__, __license__, __copyright__
from Bulk_DPI_Converter.GUI.BottomLayout import BottomLayout
from Bulk_DPI_Converter.GUI.Row_1 import Row_1
from Bulk_DPI_Converter.GUI.Row_2 import Row_2
from Bulk_DPI_Converter.GUI.Row_3 import Row_3
from Bulk_DPI_Converter.GUI.LogLayout import LogLayout

class GUI(BottomLayout, Row_1, Row_2, Row_3, LogLayout):
    pass