from time import monotonic
import board

from cardtuber import MicVolume


mv = MicVolume(N=10, length=320)
for i in range(1000):
    mv.record()
    print(mv.getVolume())