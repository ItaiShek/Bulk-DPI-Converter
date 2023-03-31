from PyQt5.QtWidgets import QFileDialog, QDialog
from PyQt5 import QtWidgets
from typing import List, Tuple
from PyQt5.QtCore import QSortFilterProxyModel, QModelIndex, QRegExp 


class FilterProxyModel(QSortFilterProxyModel):
    """
    Filter proxy model for the custom file dialog.    
    """
    def __init__(self) -> None:
        """
        Initializes the class.
        """
        super().__init__()
    
    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        """
        Checks if the source and parent should be included in the model.

        Args:
            source_row (int): the row's number.
            source_parent (QModelIndex): index to the item's model.
        
        Returns:
            bool:   True - if the item should be included in the model.
                    False - the item should not be included in the model.
        """
        model = self.sourceModel()
        index = model.index(source_row, 0, source_parent)
        if model.isDir(index):
            return True
        
        filename = model.fileName(index).lower()
        
        return self.rx.exactMatch(filename)

class CustomQFileDialog(QFileDialog):
    """
    Custom file dialog that can accept multiple files and directory.
    """
    def __init__(self) -> None:
        """
        Calls super and creates a proxy model class variable.
        """
        super().__init__()
        self.proxy_model = FilterProxyModel()

    def getOpenFilesAndDirs(self, parent=None, caption:str='', directory:str='', filter:str='', initialFilter:str='', options:QFileDialog.Options=None) -> Tuple[List[str], str]:
        """
        Let's the user choose multiple files and/or directories.

        Args:
            parent (QWidget): the parent.
            caption (str): the title of the widget.
            directory (str): the default directory to open.
            filter (str): filters, every 2 adjacent filter are separated with ";;".
            initialFilter (str): the default filter.
            options (QFileDialog.Options): options to set to the dialog, see QFileDialog.Options for more info on available options.
            
        Returns:
            Tuple (List[str], str): list of strings of the files absolute paths, and the chosen filter.
        """
        def update_line_edit() -> None:
            """
            Updates the files edit box
            """
            if list_view_model.hasSelection():
                p = '"' if len(list_view_model.selectedRows()) > 1 else ''
                select_list = [f'{p + row.data() + p}' for row in list_view_model.selectedRows()]
                line_edit.setText(' '.join(select_list))            
        
        def filter_changed() -> None:
            """
            Sets the regular expression for the proxy when the filter has changed.
            """
            if 'All Picture Files' in self.selectedNameFilter():
                self.proxy_model.rx = QRegExp(r'^.*\.(?:bmp|png|jp.+g|jpe|jfif|ti.+f)')
            else:
                self.proxy_model.rx = QRegExp(r'.*')

        self.setWindowTitle(caption)
        self.setFileMode(QFileDialog.ExistingFiles)
        if parent:
            self.setParent(parent)
        
        if options:
            self.setOptions(options)
        self.setOption(QFileDialog.DontUseNativeDialog, True)
        self.setProxyModel(self.proxy_model)
        
        if directory:
            self.setDirectory(directory)
        
        if filter:            
            self.setNameFilter(filter)
            if initialFilter:
                self.selectNameFilter(initialFilter)
        
        self.accept = lambda: QDialog.accept(self)        
        
        stacked_widget = self.findChild(QtWidgets.QStackedWidget)
        list_view = stacked_widget.findChild(QtWidgets.QListView)
        list_view_model = list_view.selectionModel()
        list_view_model.selectionChanged.connect(update_line_edit)

        line_edit = self.findChild(QtWidgets.QLineEdit)
        # clear text when changing directory
        self.directoryEntered.connect(lambda: line_edit.clear())
        
        self.filterSelected.connect(filter_changed)
        filter_changed()
        selected_files = []
        selected_name_filter = ''
        if self.exec():
            selected_files.extend(self.selectedFiles())
            selected_name_filter = self.selectedNameFilter()
                    
        return (selected_files, selected_name_filter)