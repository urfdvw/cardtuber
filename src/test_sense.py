# https://github.com/furbrain/CircuitPython_seeed_xiao_nRF52840?tab=readme-ov-file
#%%
import array
import time

import audiocore
import audiopwmio
import board
from math import log
from time import monotonic

from seeed_xiao_nrf52840 import IMU, Mic, Battery
# #%%
# with Battery() as bat:
#     print(f"Charge_status: {bat.charge_status}")
#     print(f"Voltage: {bat.voltage}")
#     print(f"Charge_current high?: {bat.charge_current}")
#     print("Setting charge current to high")
#     bat.charge_current = bat.CHARGE_100MA
#     print(f"Charge_current high?: {bat.charge_current}")
# #%%
# with IMU() as imu:
#     for i in range(5):
#         print("Acceleration:", imu.acceleration)
#         time.sleep(1)
#%%

with Mic() as mic:
    b = array.array("H")
    for i in range(3200):
        b.append(0)
    print("startplot:", 'x')
    while True:
        mic.record(b, len(b))
        print(log(max(b)- min(b)))