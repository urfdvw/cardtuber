import array
from time import monotonic
from math import log

import board

from seeed_xiao_nrf52840 import IMU, Mic, Battery

class MicVolume:
    def __init__(self, N=30, length=160):
        """
        N: number of max/min in the queue
        lenth: number of samples in each record piece
        """
        self.N = N
        self.length = length
        
        self.mic = Mic()
        self.b = array.array("H")
        for i in range(self.length):
            self.b.append(0)
            
        self.i = 0 # rotation index
        self.ranges = [[0, 65535] for i in range(self.N)] # [max, min]
    
    def record(self):
        self.mic.record(self.b, self.length)
        self.ranges[self.i] = [max(self.b), min(self.b)]
        
        self.i += 1
        if self.i >= self.N:
            self.i = 0
    
    def getVolume(self):
        valid_ranges = [
            r
            for r in self.ranges
            if r[0] > r[1]
        ]
        overall_max = max([r[0] for r in self.ranges])
        overall_min = min([r[1] for r in self.ranges])
        return log(overall_max - overall_min)

mv = MicVolume()
for i in range(1000):
    mv.record()
    print(mv.getVolume())