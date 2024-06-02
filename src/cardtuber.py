import array
from math import log
from seeed_xiao_nrf52840 import IMU, Mic, Battery

class RotaryQueue:
    def __init__(self, N):
        self.N = N
        self.i = 0
        self.queue = [None for i in range(self.N)]
        
    def write(self, value):
        self.queue[self.i] = value
        self.i += 1
        self.i %= self.N
        
        

class MicVolume:
    def __init__(self, N=30, length=160):
        """
        N: number of max/min in the queue
        lenth: number of samples in each record piece
        """
        self.N_short_term = N
        self.N_long_term = N * 10
        self.length = length
        
        self.mic = Mic()
        self.b = array.array("H")
        for i in range(self.length):
            self.b.append(0)
            
        self.short_term = RotaryQueue(self.N_short_term)
        self.long_term = RotaryQueue(self.N_long_term)
    
    def record(self):
        self.mic.record(self.b, self.length)
        
        self.short_term.write([max(self.b), min(self.b)])
        self.long_term.write(self.getVolume())
    
    def getVolume(self):
        valid = [
            item
            for item in self.short_term.queue
            if item is not None
        ]
        overall_max = max([item[0] for item in valid])
        overall_min = min([item[1] for item in valid])
        return log(overall_max - overall_min)
        
    def getThreshold(self):
        valid = [
            item
            for item in self.long_term.queue
            if item is not None
        ]
        return min(valid) + 1.5
        
