# https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-a-bitmap
import board
import displayio
import framebufferio
import sharpdisplay
import adafruit_imageload
from adafruit_display_shapes.rect import Rect
import gc
from math import sin
from time import monotonic as t
from time import sleep

jump_scale = 5


displayio.release_displays()

bus = board.SPI()
chip_select_pin = board.RX
framebuffer = sharpdisplay.SharpMemoryFramebuffer(bus, chip_select_pin, width=144, height=168, baudrate=8000000)

display = framebufferio.FramebufferDisplay(framebuffer, rotation = 0)
bitmap, palette = adafruit_imageload.load(
    "/avatar/mceo.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)

# Create a TileGrid to hold the bitmap
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

# Create a rectangle
rect = Rect(0, 168 - jump_scale, 144, jump_scale, fill=0xffffff)

# Create a Group to hold the TileGrid
group = displayio.Group()

# Add the TileGrid to the Group
group.append(rect)
group.append(tile_grid)

# Add the Group to the Display
display.root_group = group

print(gc.mem_free())

#%% main
# Loop forever so you can enjoy your image
print('startplot:', 'y')
while True:
    y = - abs(int(sin(t()*3)*jump_scale))
    print(y)
    tile_grid.y = y
    sleep(0.05)
    