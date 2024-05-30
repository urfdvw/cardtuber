import board
import displayio
import framebufferio
import sharpdisplay
import adafruit_imageload
from adafruit_display_shapes.rect import Rect
import gc
from time import monotonic as t
from time import sleep

from cardtuber import MicVolume
from touchpad import State

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
while True:
    mv.record()
    vol = mv.getVolume()
    if vol > 6:
        speak.now = 1
    else:
        speak.now = 0
    
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