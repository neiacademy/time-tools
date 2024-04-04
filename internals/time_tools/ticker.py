"""
    Main class of the timer_tools provides the core for infinite timers
    and Subject ticker to implement the Observer pattern with
"""

from threading import Timer
import functools


class Ticker:
    """
        Defines a timer that will loop inifinetly executing whatever function is passed unto it,
        arguments can be passed on the constructor as *args and **kwargs
    """

    def __init__(self,t,callback,*args,**kwargs):
        """
            t: time in seconds for the timer
            callback: function that will be called when timer is up
            args: arguments to be pased as *args
            kwargs: arguments to be passed **kwargs
        """
        self.t=t
        if args or kwargs:
            self.ticking_function = functools.partial(callback,*args,**kwargs)
        else:
            self.ticking_function = callback
        self.thread = Timer(self.t,self.handle_function)

    def handle_function(self):
        """
            Executes the stored function and continues the loop
        """
        self.ticking_function()
        self.thread = Timer(self.t,self.handle_function)
        self.start()

    def start(self):
        """
            Starts the Ticker
        """
        self.thread.start()

    def cancel(self):
        """
            cancels the Ticker
        """
        self.thread.cancel()


class Multi_Ticker(Ticker):
    """
        Extention of the Ticker class
        main diference being that you can add observers
        to execute multiple functions each tick
    """

    def __init__(self,t):
        super().__init__(t,self.tick)
        self.observers = []

    def tick(self):
        """
            the default (and only) executable tick function
            goes through the observers and calls it's function
        """
        for function in self.observers:
            function()

    def addObserver(self,function,*args, **kwargs):
        """
            appends new function to the list of observers
            if the observer requires somme kind of arguments
            it creates a parcial that will be able to use said arguments

            as of now there's no way to modify a predifined function
            it's recommended that called functions are as self contained as posible
        """
        if args or kwargs:
            self.observers.append(functools.partial(function,*args,**kwargs))
        else:
            self.observers.append(function)
