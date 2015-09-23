from collections import defaultdict


class MockGPIO(object):

    def __init__(self):
        self.BCM = None
        self.IN = None
        self.OUT = None
        self.LOW = 0
        self.HIGH = 1
        self.PUD_UP = None
        self.PUD_DOWN = None
        self.PUD_OFF = None
        self.RISING = 'RISING'
        self.FALLING = 'FALLING'
        self.BOTH = 'BOTH'
        self._data = defaultdict(int)

    def setmode(self, mode):
        pass

    def setwarnings(self, warn):
        pass

    def input(self, pin_number):
        return self._data[pin_number]

    def output(self, pin_number, value):
        self._data[pin_number] = value

    def setup(self, pin_number, mode, initial, pull_up_down):
        self._data[pin_number] = initial

    def add_event_detect(self, *args, **kwargs):
        pass
