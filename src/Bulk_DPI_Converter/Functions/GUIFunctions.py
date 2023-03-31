from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QCloseEvent, QColor
from PyQt5.QtCore import QDateTime


class GUIFunctions():
    """
    Contains functions for the GUI and interactions with some of the buttons.
    """
    def append_log(self, message: str) -> None:
        """"
        Appends message to the log box with the current time.

        Args:
            message (str): the message to append to the log box.
        """
        red_color = QColor(190, 8, 8)
        black_color = QColor(0, 0, 0)
        time = QDateTime().currentDateTime()
        self.log_widget.textbox.setTextColor(red_color)
        self.log_widget.textbox.insertPlainText(f'{time.toString("hh:mm:ss")} - ')
        self.log_widget.textbox.setTextColor(black_color)
        self.log_widget.textbox.insertPlainText(f'{message}\n')
    
    def end(self) -> None:
        """
        Sets to GUI back to it's default state.
        Called when the thread ends.
        """    
        self.toggle_pause(True)
        self.overwrite_edit.setEnabled(not self.overwrite_check.isChecked())
        self.start_btn.setText('Start')        
        self.toggle_widgets(True)
        self.stop_btn.setEnabled(False)

    def toggle_pause(self, val: bool) -> None:
        """
        Toggles the Start/Pause button.

        Args:
            val (bool): True - resume.
                        False - pause.
        """
        if val:
            icon = self.start_icon
            text = 'Resume'
            color = '#12a40d'
        else:
            icon = self.pause_icon
            text = 'Pause'
            color = '#1428bd'

        self.start_btn.setIcon(icon)
        self.start_btn.setText(f'{text}')
        self.start_btn.setStyleSheet(f'QPushButton {{color: {color}}}')


    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Terminates the software gracefully.
        Called when the user try to exit the software.
        """
        original_pause_state = self.start_thread.thread_pause.is_set()
        self.start_thread.thread_pause.set()

        if not self.start_thread.isRunning():
            event.accept()
            return
        
        dlg = QMessageBox()
        dlg.setWindowTitle(self.windowTitle())
        dlg.setText('There are unfinished processes.\nAre you sure you want to quit?')
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        if dlg.exec() == QMessageBox.Yes:
            self.terminate()
            event.accept()
            return
        
        self.start_thread.thread_pause.set() if original_pause_state else self.start_thread.thread_pause.clear()
        event.ignore()