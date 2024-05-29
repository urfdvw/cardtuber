# https://github.com/furbrain/CircuitPython_seeed_xiao_nRF52840?tab=readme-ov-file
#%%
# async failed

import array
import time
from time import monotonic

import audiocore
import audiopwmio
import board
from math import log

from seeed_xiao_nrf52840 import IMU, Mic, Battery


import asyncio
import board
import digitalio


async def blink(pin, interval, count):
    for _ in range(count):
        print(pin, True)
        await asyncio.sleep(interval)  # Don't forget the "await"!
        print(pin, False)
        await asyncio.sleep(interval)  # Don't forget the "await"!

async def getVol():
    with Mic() as mic:
        b = array.array("H")
        for i in range(160):
            b.append(0)
        print("startplot:", 'x')
        while True:
            mic.record(b, len(b))
            print(log(max(b)- min(b)))

async def main():
    led1_task = asyncio.create_task(blink('pin 1', 0.25, 10))
    led2_task = asyncio.create_task(blink('pin 2', 0.1, 20))

    mic_task = asyncio.create_task(getVol())

    await asyncio.gather(led1_task, led2_task, mic_task)  # Don't forget "await"!
    print("done")


asyncio.run(main())
