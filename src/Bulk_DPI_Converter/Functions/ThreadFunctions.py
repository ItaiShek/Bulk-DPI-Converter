from re import findall
from PyQt5.QtWidgets import QMessageBox
import glob, os


class ThreadFunctions():
    """
    Functions for threading and multiprocessing.
    """
    def terminate(self) -> None:
        """
        Terminates the processes and thread.
        """
        for proc in self.start_thread.processes:
            proc.term.set()
        self.start_thread.wait()
        self.start_thread.terminate()
        self.append_log('Process terminated by user')

    def toggle_widgets(self, val: bool) -> None:
        """
        Enables/Disables some of the widgets.

        Args:
            val (bool): True - Enable.
                        False - Disable.
        """
        self.select_btn.setEnabled(val)
        self.thread_edit.setEnabled(val)
        self.dirs_checkbox.setEnabled(val)
        self.dpi_edit.setEnabled(val)
        self.dpi_menu.setEnabled(val)
        self.overwrite_check.setEnabled(val)
    
    def get_files(self) -> list:
        """
        Prepare a list of images for the thread and filter them according to the user's filters.

        Returns:
            list: a list of strings that represents the absolute path of the images.
        """
        images = []
        recursive = self.dirs_checkbox.isChecked()
        
        # if it's just one directory and the recursive flag is not set just get the images in that directory
        if (len(self.files) == 1 and not recursive
            and os.path.exists(self.files[0])
            and os.path.isdir(self.files[0])):
            suffix = '**/*'
        else:
            suffix = '/**/*'

        # prepare the filters for glob
        filters = findall(r'\*(\.\w*)', self.filters)
        if 'All Picture Files' in self.filters:
            filters = ['.bmp', '.png', '.jpg', '.jpeg', '.jpe', '.jfif', '.tif', '.tiff']
        
        for file in self.files:
            if not os.path.exists(file):                
                continue

            if os.path.isdir(file):
                for filter in filters:
                    temp_list = glob.glob(f'{file}{suffix}{filter}', recursive=recursive)
                    images.extend(temp_list)
            else:
                ext = os.path.splitext(file)[-1]
                if ext in filters:
                    images.append(file)
        
        return images

    def validate(self) -> bool:
        """
        Checks that all of the input fields are ok.
        
        Returns:
            bool:   True - OK
                    False - Not OK
        """
        dlg = QMessageBox()
        dlg.setWindowTitle('Error')        
        dlg.setStandardButtons(QMessageBox.Ok)
        dlg.setIcon(QMessageBox.Critical)

        if not self.files:
            dlg.setText('Select files or directories')
            dlg.exec()
            return False

        if not self.thread_edit.text():
            dlg.setText('Enter number of threads')
            dlg.exec()
            return False
        
        if not self.dpi_edit.text():
            dlg.setText('Enter DPI value')
            dlg.exec()
            return False
        
        if not self.overwrite_check.isChecked() and not self.overwrite_edit.text():
            dlg.setIcon(QMessageBox.Warning)
            dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            dlg.setText('If you leave the suffix field empty it will overwrite the original file.\nDo you want to overwrite files?')
            if dlg.exec() == QMessageBox.No:
                return False
        
        return True