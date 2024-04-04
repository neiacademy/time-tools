"""
    Alternative to the Timer class on threading
    It allows for custom time format definition

    It also includes a normalizer function and a string parser for easier time definition
"""

import time
from threading import Timer

class Custom_timer():
    """
        Defines a class similar to timer in functionality  with the added feature of being able to define a custom time structure
        NOTE: this class will work with floating point numbers but except for tick_length they will be treated as integers
    """
    def __init__(self,tick_length = 1,time_format=(10,10),time_duration = [1,1],callback=None,*args):
        """
            tick_length: How long does the least significant time unit lasts, floating point numbers will be respected for this
            time_format: tuple containing the max time_duration of each significant place NOTE: list order is used for time calculations please adjust accordingly
            time_duration: list containing how much of each time unit is needed list order is also respected here
            callback; the function to be called upon timer termination (optional)
            args: arguments for the callback funtion (optional)
        """

        if len(time_duration) is not len(time_format):
            raise ValueError('Time format and duration must have the same number of components')
        if not callback:
            raise ValueError('callback must be defined')

        self.tick_length = tick_length
        self.max_time = time_format
        self.current = time_duration[:]
        self.callback = callback
        self.args = args
        self.timer = None

    def start(self):
        """
            Starts the timer normally
        """
        self.tick(0)

    def stop(self):
        """
            Terminates the current timer
        """
        self.timer.cancel()

    def tick(self,current_time_unit):
        """
            Calculates remaining time and executes callback if time's up
        """
        if current_time_unit == len(self.max_time):
            return True

        self.current[current_time_unit] -= 1
        flag = False
        if self.current[current_time_unit] < 0:
            self.current[current_time_unit] = self.max_time[current_time_unit] - 1
            flag |= self.tick(current_time_unit+1)

        if current_time_unit == 0 and not flag:
            self.timer = Timer(self.tick_length,self.tick,[0])
            self.timer.start()
        elif current_time_unit == 0 and flag:
            self.time_up()
        else:
            return flag

    def time_up(self):
        """
            Changes callback execution depending of wether there are arguments or not
        """
        if self.callback and self.args:
            self.callback(*self.args)
            return
        self.callback()


def custom_time_builder(time_format, time_duration = None):
    """
        Time_format: String of positive numbers separated by ':'
        time_duration: String of positive numbers separated by ':'
        Returns
            dict containing a 'time_format' tuple and a 'duration' list
    """
    time_format = [int(i) for i in time_format.split(":")]
    if time_duration:
        time_duration = [int(i) for i in time_duration.split(':')]
        if len(time_duration) is not len(time_format):
            raise RuntimeError('Time format and duration must have the same number of components')

    return time_format,time_duration


def normalize_time(time_format, time_duration):
    """
        Takes a 'time_format' tuple and a 'time_duration' list and calculates the proper duration of time_duration so it respects time_format specifications
    """
    if not time_format or not time_duration:
        raise RuntimeError('Mising or \'None\' arguments')

    if len(time_duration) != len(time_format):
        raise RuntimeError('Time format and duration must have the same number of components')

    for i in range(len(time_duration)):
        if time_duration[i] > time_format[i]:
            if i == len(time_duration)-1:
                continue
            time_duration[i+1] += time_duration[i] // time_format[i]
            time_duration[i] = time_duration[i] % time_format[i]

    return time_duration,time_format
