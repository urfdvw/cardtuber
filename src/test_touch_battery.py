import board
import displayio
import framebufferio
import sharpdisplay
        
# Release the existing display, if any
displayio.release_displays()

bus = board.SPI()
chip_select_pin = board.RX
# Select JUST ONE of the following lines:
# For the 400x240 display (can only be operated at 2MHz)
# framebuffer = sharpdisplay.SharpMemoryFramebuffer(bus, chip_select_pin, 144, 168)
# For the 144x168 display (can be operated at up to 8MHz)
framebuffer = sharpdisplay.SharpMemoryFramebuffer(bus, chip_select_pin, width=144, height=168, baudrate=8000000)

display = framebufferio.FramebufferDisplay(framebuffer, rotation = 0)

import time
import board
import touchio

from touchpad import TouchBarPhysics, TouchBarPhysicsSimple
from connected_variables import ConnectedVariables
cv = ConnectedVariables

touch_pads = [
    touchio.TouchIn(board.A0),
    touchio.TouchIn(board.A1),
    touchio.TouchIn(board.A2),
    touchio.TouchIn(board.A3),
    touchio.TouchIn(board.SDA),
    touchio.TouchIn(board.SCL),
    touchio.TouchIn(board.TX)
]

touch_bar_phy = TouchBarPhysics(
    pads=touch_pads,
)

# 283,315,253,260,378,366,216
# 203,207,208,208,207,207,168