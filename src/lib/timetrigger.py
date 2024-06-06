"""
This script contains the classes for
triggers related to time
"""
from time import monotonic

# Timer class
class Timer:
    """
    One time use timer class
    """
    def __init__(self, hold=False):
        self.duration = 0
        self.start_time = monotonic()
        self.enable = False
        self.hold = hold
        self.dt = 0
    def over(self):
        """
        check if timer is over
        if self.hold is off
            timer is auto-reset after check
        otherwise
            timer can be checked multiple times without affectiong the result.
        """
        self.dt = monotonic() - self.start_time
        out = (self.dt > self.duration) and self.enable
        if out and not self.hold:
            self.enable = False
        return out
    def start(self, duration):
        """
        start a timer of a certian duration
        """
        self.duration = duration
        self.start_time = monotonic()
        self.enable = True
    def disable(self):
        self.enable = False

class Repeat:
    """
    Pause generator
    used as the trigger of repeated action
    """
    def __init__(self, freq):
        self.timer = Timer()
        self.freq_measure = 0 # measurement
        self.freq_set = freq
        self.timer.start(0)
    def check(self):
        """
        check if it is the time to take action
        """
        if self.timer.over():
            self.freq_measure = 1 / self.timer.dt
            self.timer.start(1 / self.freq_set)
            return True
        else:
            return False