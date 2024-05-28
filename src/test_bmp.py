# https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-a-bitmap
import board
import displayio
import framebufferio
import sharpdisplay
import adafruit_imageload
import gc
from math import sin
from time import monotonic as t
from time import sleep

displayio.release_displays()

bus = board.SPI()
chip_select_pin = board.RX
framebuffer = sharpdisplay.SharpMemoryFramebuffer(bus, chip_select_pin, width=144, height=168, baudrate=8000000)

display = framebufferio.FramebufferDisplay(framebuffer, rotation = 0)
bitmap, palette = adafruit_imageload.load(
    "/maker.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)

# Create a TileGrid to hold the bitmap
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

# Create a Group to hold the TileGrid
group = displayio.Group()

# Add the TileGrid to the Group
group.append(tile_grid)

# Add the Group to the Display
display.root_group = group

print(gc.mem_free())

# Loop forever so you can enjoy your image
scale = 10
print('startplot:', 'y')
while True:
    y = int(sin(t())*scale)
    print(y)
    group.y = y
    sleep(0.05)
    