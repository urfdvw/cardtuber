"""
This script contains all classes for
Background processes
"""
from timetrigger import Repeat

class Background_app:
    """
    Base class for background procedures
    return 0 when not taking action
    """
    def __init__(self, freq=None, period=None):
        assert (freq is not None) != (period is not None)  # != use as xor
        if freq is not None:
            self.freq = freq
        if period is not None:
            self.freq = 1 / period
        self.repeat_timer = Repeat(self.freq)
    def procedure(self):
        return 0
    def __call__(self):
        if self.repeat_timer.check():
            return self.procedure()
        else:
            return 0

class FpsControl(Background_app):
    """
    Control the frame rate
    """
    def __init__(self, fps=None):
        super().__init__(freq=fps)
        self.fps_now = 10
    def procedure(self):
        self.fps_now = self.repeat_timer.freq_measure
        return 1

class FpsMonitor(Background_app):
    """
    print the current FPS to serial
    This is used for debug propose
    """
    def __init__(self, period, fps_app):
        self.fps_app = fps_app
        super().__init__(period=period)
    def procedure(self):
        print('FPS:', self.fps_app.fps_now)
        return 0
