# Python native
import gc
from random import random
from time import monotonic as t
from time import sleep

# Board native
import board
import displayio
import framebufferio
import sharpdisplay
import touchio

# Adafruit
from adafruit_display_shapes.rect import Rect
import adafruit_imageload

# Mine
from cardtuber import MicVolume
from connected_variables import ConnectedVariables
from touchpad import State, TouchBarPhysicsSimple

#%% parameters
jump_scale = 4
blink_max = 5 # at least blink once every x sec
blink_min = 2 # not to blink x sec once blinked

#%% define

cv = ConnectedVariables()

touch_pads = [
    touchio.TouchIn(board.A0),
    touchio.TouchIn(board.A1),
    touchio.TouchIn(board.A2),
    touchio.TouchIn(board.A3),
    touchio.TouchIn(board.SDA),
    touchio.TouchIn(board.SCL),
    touchio.TouchIn(board.TX)
]

touch_bar_phy = TouchBarPhysicsSimple(
    pads=touch_pads,
)

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
qr_bmp, palette = adafruit_imageload.load(
    "/QR.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)

rect = Rect(0, 0, 144, 168, fill=0xffffff)

tile_grid = displayio.TileGrid(mceo_bmp, pixel_shader=palette)
tile_grid_qr = displayio.TileGrid(qr_bmp, pixel_shader=palette, y=168)

group = displayio.Group()
group.append(rect)
group.append(tile_grid)
group.append(tile_grid_qr)

display.root_group = group

print(gc.mem_free())

#%% main
# Loop forever so you can enjoy your image

mv = MicVolume(N=4, length=80)
speak = State()
blink = State()
blink_timer = 0
blink_last_t = t()
cv.define('vol', 0.0)
cv.define('thr', 6.0)
while True:
    mv.record()
    vol = mv.getVolume()
    thr = mv.getThreshold()
    cv.write('vol', round(vol, 1)) # for monitoring
    cv.write('thr', round(thr, 1)) # for monitoring
    if vol > thr:
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
            
    touch_bar_phy.get()
    if touch_bar_phy.z.now > 0.5:
        tile_grid_qr.y += int(touch_bar_phy.x.diff * 60)
    else:
        if tile_grid_qr.y > 84:
            tile_grid_qr.y += (168 - tile_grid_qr.y) // 2
        else:
            tile_grid_qr.y += - tile_grid_qr.y // 2
        if abs(tile_grid_qr.y - 168) < 2:
            tile_grid_qr.y = 168
        if abs(tile_grid_qr.y) < 2:
            tile_grid_qr.y = 0