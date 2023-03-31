import imghdr
from time import sleep
import os
from PIL import Image
from multiprocessing import Event, Process, Queue, Value


class CustomProcess(Process):
    """
    Custom process for multiprocessing.
    """
    def __init__(self, pause: Event, apply: bool, images: list, dpi: int, overwrite: bool, suffix: str, prog: Value) -> None:
        """
        Initialize the processes with values from the parent, a queue, and an event.
        """
        super().__init__()
        self.term = Event() # terminate
        self.q = Queue()    # queue with "skipped", "errored", and "successful" values for the parent.

        self.pause = pause
        self.apply = apply  # True - apply to lower resolution images, False - apply to all
        self.images = images
        self.dpi = dpi
        self.overwrite = overwrite
        self.suffix = suffix
        self.prog = prog

    def run(self) -> None:
        """
        Updates the DPI of a list of images according to the user's choice.
        """
        skipped = 0
        errored = 0
        success = 0

        for image in self.images:
            if self.term.is_set():
                self.end(skipped, errored, success)
                return
            while self.pause.is_set():
                sleep(0.1)
                if self.term.is_set():
                    self.end(skipped, errored, success)
                    return
            # check if file exists
            if not os.path.exists(image):
                skipped += 1
                self.inc()
                continue
            # check if file is an image
            if not imghdr.what(image):
                skipped += 1
                self.inc()
                continue
            try:
                im = Image.open(image)
                dpi = im.info.get("dpi")
                if (not dpi or
                    dpi[0] < self.dpi or
                    not self.apply):                    
                    new_image = '{0}{2}{1}'.format(*os.path.splitext(image), self.suffix)
                    im.save(new_image, dpi=(self.dpi, self.dpi))
                else:
                    skipped += 1                    
            except:
                errored += 1
            else:
                success += 1
            self.inc()
        self.end(skipped, errored, success)
        
    def end(self, skipped: int, errored: int, success: int) -> None:
        """
        Saves the details of the handled images in queue for the parent.

        Args:
            skipped (int): the amount of files that were skipped.
            errored (int): the amount of files that were errored.
            success (int): the amount of files that were successful.
        """
        self.q.put(skipped)
        self.q.put(errored)
        self.q.put(success)
    
    def inc(self) -> None:
        """
        Increments the progress variable.
        """
        with self.prog.get_lock():
            self.prog.value += 1
