"""
    This class abstracts the well known startTime - time.time()
    it's a little redundant but it limits calls and allows to temporally pause
    time tracking
"""

import time

class Stopwatch():
    """
        defines the class that abstracts time tracking
    """

    def __init__(self):
        """
            initialize variables and control flags
        """
        self.start_time = -1.0
        self.elapsed_time = 0.0
        self.is_stopped = True
        self.is_paused = False

    def start(self):
        """
            sets flags and variables
        """
        if self.is_stopped and not self.is_paused:
            self.is_stopped = False
            self.elapsed_time = 0.0
        elif self.is_paused and not self.is_stopped:
            self.is_paused = False
        else:
            raise RuntimeError('Flags are unproperly set notify code author for him to revise logic')
        self.start_time = time.time()


    def stop(self):
        """
            stops stopwatch elapsed time gets stored but is lost upon restarting
        """

        if self.is_stopped:
            raise RuntimeError('Stopwatch is already stopped')
        self.elapsed_time += time.time() - self.start_time
        self.is_stopped = True
        self.is_paused = False


    def pause(self):
        """
            pauses the stopwatch without loosing elapsed time nor restarting it
        """
        if self.is_stopped:
            raise RuntimeError('Stopwatch is currently stopped, can\'t be paused')
        self.elapsed_time += time.time() - self.start_time
        self.is_paused = True

    def reset(self):
        """
            resets data without stopping the stopwatch itself
        """
        self.start_time = time.time()
        self.elapsed_time = 0

    def get_time(self):
        """
            returns the time elapsed since the stopwatch got started
            it's redundancy causes a small margin of error, please be weary
        """
        if not self.is_paused and not self.is_stopped:
            self.elapsed_time += time.time() - self.start_time
            self.start_time = time.time()

        return self.elapsed_time
