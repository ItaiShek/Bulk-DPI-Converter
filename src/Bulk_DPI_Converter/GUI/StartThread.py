from typing import Iterator, Optional
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from multiprocessing import Event, Value, connection

from Bulk_DPI_Converter.Functions.CustomProcess import CustomProcess


class StartThread(QThread):
    """
    A thread creates and handles processes for updating the DPI of images.
    This thread is run when the user clicks the "Start" button.
    """
    append_log = pyqtSignal(str)
    update_progress = pyqtSignal(int)

    def __init__(self, parent: Optional[QObject]) -> None:
        """
        Initializes the thread, prepares some of the class's members.

        Args:
            parent (QObject): the thread's parent.
        """
        super().__init__(parent)
        self.parent = parent

        self.thread_pause = Event()     # event for pausing the processes
        self.processes = []             # list of processes
        self.images_lst = []            # list of strings (paths to images)
        self.n_threads = 0              # number of processes to create
        self.prog = Value('i')          # progress

    def run(self) -> None:
        """
        Creates and runs multiprocessing processes, prepares the values for the processes,
        and updates the progress bar with values from the processes.
        """

        # initialize and prepare some values for the processes
        n_images = len(self.images_lst)
        gen = self.split_list(self.images_lst, self.n_threads)
        self.processes = []
        self.prog.value = 0
        
        apply = self.parent.apply
        dpi = int(self.parent.dpi_edit.text())
        overwrite = self.parent.overwrite_check.isChecked()
        n = min(self.n_threads, n_images)
        if overwrite:
            suffix = ''
        else:
            suffix = self.parent.overwrite_edit.text()

        # create and start the processes
        for _ in range(n):
            p = CustomProcess(pause=self.thread_pause, apply=apply, images=next(gen), dpi=dpi, overwrite=overwrite, suffix=suffix, prog=self.prog)
            self.processes.append(p)
            p.start()
        
        self.append_log.emit(f'Created and started {len(self.processes)} processes')
        
        n = n_images if n_images else 1 # avoid division by zero when the list is empty
        while any(p.is_alive() for p in self.processes):    # wait for processes to die
            with self.prog.get_lock():
                self.update_progress.emit(int(self.prog.value*100/n))                # update the progress bar every 5 seconds
            connection.wait((p.sentinel for p in self.processes), timeout=5)    # wait for 5 seconds for processes to finish
        
        # update one last time after the processes finish
        with self.prog.get_lock():
            self.update_progress.emit(int(self.prog.value*100/n))

        self.append_log.emit('Done\n\tSkipped: {}\n\tErrored: {}\n\tCompleted: {}'.format(sum(proc.q.get() for proc in self.processes),
                                                                                          sum(proc.q.get() for proc in self.processes),
                                                                                          sum(proc.q.get() for proc in self.processes)))
    
    @staticmethod
    def split_list(lst: list, n: int) -> Iterator[list]:
        """
        Splits a list into n parts of of approximately equal length.

        Args:
            lst (list): a list to split.
            n (int): how many chunks to split.
        
        Returns:
            Iterator (list): a generator of lists
        """
        n = min(n, len(lst))        # avoid empty lists        
        q, r = divmod(len(lst), n)  # q-quotient, r-remainder
        for i in range(n):
            yield lst[i*q+min(i, r):(i+1)*q+min(i+1, r)]