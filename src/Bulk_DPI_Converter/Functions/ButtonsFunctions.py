from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QDir
import os
from os.path import expanduser

from Bulk_DPI_Converter.GUI.CustomQFileDialog import CustomQFileDialog
from Bulk_DPI_Converter import __title__, __version__, __license__, __copyright__


class ButtonsFunctions():
    """
    Functions for the GUI buttons.
    """
    def about(self) -> None:
        """
        Display message box with general details about the software
        """
        dlg = QMessageBox()
        dlg.setWindowTitle('About')
        
        dlg.setStandardButtons(QMessageBox.Close)
        dlg.setIcon(QMessageBox.Information)
        text =  f'<p>{__title__}</p>' \
                f'<p>Version: <a href="https://github.com/ItaiShek/{__title__}/releases/tag/v{__version__}">{__version__}</a></p>' \
                f'<p>License: <a href="https://github.com/ItaiShek/{__title__}/blob/main/LICENSE">{__license__}</a></p>' \
                f'<p>{__copyright__}</p>' \
                
        dlg.setText(text)
        dlg.exec()

    def select_files(self):
        filters = [ 
                    'BMP (*.bmp)',
                    'PNG (*.png)',
                    'JPEG (*.jpg *.jpeg *.jpe *.jfif)',
                    'TIFF (*.tiff *.tif)',
                    'All Picture Files ( )',
                    'All Files (*)'
                    ]
        
        file_dialog = CustomQFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        dir = expanduser('~/Desktop') if os.path.exists(expanduser('~/Desktop')) else QDir.homePath()
        self.files, self.filters = file_dialog.getOpenFilesAndDirs(caption='Open files', directory=dir, filter=';;'.join(filters), initialFilter=filters[1])
            
    def start(self) -> None:
        """
        Start/Pause button.
        When 'Start' is pressed an images list is created an passed to the thread.
        """
        if not self.validate():
            return
        
        # disable widgets
        self.toggle_widgets(False)

        if self.start_thread.isRunning():
            if self.start_thread.thread_pause.is_set():
                self.toggle_pause(False)
                self.start_thread.thread_pause.clear()
                self.append_log('Resumed')
            else:
                self.toggle_pause(True)
                self.start_thread.thread_pause.set()
                self.append_log('Paused')
        else:
            self.toggle_pause(False)
            self.stop_btn.setEnabled(True)
            self.overwrite_edit.setEnabled(False)
            self.start_thread.thread_pause.clear()

            self.log_widget.textbox.clear()
            self.append_log('Gathering files (this may take a while)')

            self.start_thread.images_lst, self.start_thread.n_threads = self.get_files(), int(self.thread_edit.text())
            
            self.append_log(f'Found {len(self.start_thread.images_lst)} files')
            self.append_log(f'Starting threads')

            self.progress_bar.setValue(0)
            self.start_thread.start()


    def stop(self) -> None:
        """
        Stop button.
        Stopping the thread and processes.
        """
        if not self.start_thread.isRunning():
            return
        
        original_pause_state = self.start_thread.thread_pause.is_set()
        self.start_thread.thread_pause.set()

        dlg = QMessageBox()
        dlg.setWindowTitle(self.windowTitle())
        dlg.setText('Are you sure you want to stop?')
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        
        if dlg.exec() == QMessageBox.Yes:
            self.terminate()
            self.toggle_widgets(True)
        else:
            self.start_thread.thread_pause.set() if original_pause_state else self.start_thread.thread_pause.clear()
