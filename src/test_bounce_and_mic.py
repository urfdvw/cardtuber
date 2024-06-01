import board
import displayio
import framebufferio
import sharpdisplay
import adafruit_imageload
from adafruit_display_shapes.rect import Rect
import gc
from time import monotonic as t
from time import sleep
from random import random

from cardtuber import MicVolume
from touchpad import State
from connected_variables import ConnectedVariables

cv = ConnectedVariables()

jump_scale = 4

displayio.release_displays()

bus = board.SPI()
chip_select_pin = board.RX
framebuffer = sharpdisplay.SharpMemoryFramebuffer(bus, chip_select_pin, width=144, height=168, baudrate=8000000)

display = framebufferio.FramebufferDisplay(framebuffer, rotation = 0)

mceo_bmp, palette = adafruit_imageload.load(
    "/avatar/mceo.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
mcec_bmp, palette = adafruit_imageload.load(
    "/avatar/mcec.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
moeo_bmp, palette = adafruit_imageload.load(
    "/avatar/moeo.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
moec_bmp, palette = adafruit_imageload.load(
    "/avatar/moec.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)

# Create a TileGrid to hold the bitmap
tile_grid = displayio.TileGrid(mceo_bmp, pixel_shader=palette)

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

mv = MicVolume(N=4, length=80)
speak = State()
blink = State()
blink_max = 5 # at least blink once every x sec
blink_min = 2 # not to blink x sec once blinked
blink_timer = 0
blink_last_t = t()
cv.define('vol', 0.0)
cv.define('thr', 6.0)
while True:
    mv.record()
    vol = mv.getVolume()
    cv.write('vol', round(vol, 1)) # for monitoring
    if vol > cv.read('thr'):
        speak.now = 1
    else:
        speak.now = 0
        
    if blink.now == 0 and t() - blink_last_t >= blink_timer:
        blink.now = 1
        blink_last_t = t()
        
    if blink.now == 1 and t() - blink_last_t >= 0.2:
        blink.now = 0
        blink_last_t = t()
        blink_timer = blink_min + random() * (blink_max - blink_min)
    
    if speak.diff == 1:
        tile_grid.bitmap = moeo_bmp
        tile_grid.y = -jump_scale // 2
    elif speak.diff == -1:
        tile_grid.bitmap = mceo_bmp
        tile_grid.y = -jump_scale // 2
    elif speak.diff == 0 and speak.now == 1:
        tile_grid.y = -jump_scale
    elif speak.diff == 0 and speak.now == 0:
        tile_grid.y = 0

    if blink.diff == 1:
        if speak.now == 1:
            tile_grid.bitmap = moec_bmp
        if speak.now == 0:
            tile_grid.bitmap = mcec_bmp
    elif blink.diff == -1:
        if speak.now == 1:
            tile_grid.bitmap = moeo_bmp
        if speak.now == 0:
            tile_grid.bitmap = mceo_bmp