## global imports
import threading

class Timer:

    def __init__(self): pass

    def callback_delay(self, delay: float, callback: callable, *args, **kwargs) -> any:
        return threading.Timer(delay, callback, *args, **kwargs)

class Toolkit:

    def __init__(self):
        self.timer = Timer()

    def tuple_to_list(self, value: tuple) -> list:
        return [*value]

class Quiggle:

    def __init__(self):
        self.errors = {}
        self.toolkit = Toolkit()
        self.settings = {}