import random
import json

import board
import displayio
import framebufferio
import sharpdisplay
from terminalio import FONT
import touchio

from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label, wrap_text_to_lines

from background import FpsControl, FpsMonitor
from timetrigger import Timer
from touchpad import TouchBarPhysics
from connected_variables import ConnectedVariables

cv = ConnectedVariables()
cv.define('debug', '')
def log(text):
    cv.write('debug', str(text).replace(',', ',\r\n'))

SCREEN_X = 168
SCREEN_Y = 144

class BounceBall:
    """
    Bounce ball game
    """
    def __init__(self):
        # ball variables
        self.ball_size = 5
        self.ball_x = 0
        self.ball_y = 32
        self.ball_dx = 0.95
        self.ball_dy = - 1
        self.ball_ay = 0.2
        self.ball_width = SCREEN_X - self.ball_size - 1
        self.ball_height = SCREEN_Y - 2 - self.ball_size - 1

        # display
        self.group = displayio.Group()
        
        # # draw background
        # rect = Rect(0, 0, SCREEN_X, SCREEN_Y, fill=0x000000)
        # self.group.append(rect)

        # draw a square (ball)
        # self.ball_bitmap = displayio.Bitmap(self.ball_size, self.ball_size, 1)
        # color_palette = displayio.Palette(1)
        # color_palette[0] = 0xFFFFFF  # White
        # self.ball_disp = displayio.TileGrid(
        #     self.ball_bitmap,
        #     pixel_shader=color_palette,
        #     x=int(self.ball_x),
        #     y=int(self.ball_y)
        # )
        
        self.ball_disp = Rect(
            self.ball_x,
            self.ball_y,
            self.ball_size,
            self.ball_size,
            fill=0xFFFFFF
        )
        self.group.append(self.ball_disp)

        # pad variables
        self.pad_x = 0
        self.pad_size = 30

        # draw a square (pad)
        # self.pad_bitmap = displayio.Bitmap(self.pad_size, 1, 1)
        # color_palette = displayio.Palette(1)
        # color_palette[0] = 0xFFFFFF  # White
        # self.pad_disp = displayio.TileGrid(
        #     self.pad_bitmap,
        #     pixel_shader=color_palette,
        #     x=self.pad_x-self.pad_size//2,
        #     y=SCREEN_Y - 1)
        
        self.pad_disp = Rect(
            self.pad_x - self.pad_size // 2,
            SCREEN_Y - 1,
            self.pad_size,
            1,
            fill=0xFFFFFF
        )
        self.group.append(self.pad_disp)

        # Draw a label
        #     text = str(i) + ': ' + str(gc.mem_free()) # free ram
        text = "0" # free ram
        self.text_area = label.Label(
            FONT, text=text, color=0xFFFFFF, x=0, y=4
        )
        self.group.append(self.text_area)

        # game states
        self.info = ''
        self.count = 0
        self.game_over = False
        self.count_up = False
        self.game_over_timer = Timer()

    def init(self):
        self.pad_x = 0
        self.ball_x = 0
        self.ball_y = 32
        self.ball_dx = 0.95
        self.ball_dy = - 1
        self.count = 0
        self.count_up = True
        self.info = '0'

    def update(self, touch_phy_get):
        # if game over
        if self.game_over:
            # self.init()
            while True:
                pass

        # physics
        self.ball_dy += self.ball_ay
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        if touch_phy_get.z > 1:
            if True:  # absolute position
                self.pad_x = (6 - touch_phy_get.x) / 6 * SCREEN_X - 1 - self.pad_size // 2
            else: # relative position
                self.pad_x += ring_get['theta_d'] * 30
                if self.pad_x < -self.pad_size / 2:
                    self.pad_x = -self.pad_size / 2
                if self.pad_x > SCREEN_X - self.pad_size / 2:
                    self.pad_x = SCREEN_X - self.pad_size / 2
        # logic
        if self.ball_x < 0:
            self.ball_x = - self.ball_x
            self.ball_dx = - self.ball_dx
        if self.ball_y < 0:
            self.ball_y = - self.ball_y
            self.ball_dy = - self.ball_dy
        if self.ball_x > self.ball_width:
            self.ball_x = self.ball_width * 2 - self.ball_x
            self.ball_dx = - self.ball_dx
        if self.ball_y > self.ball_height:
            # if ball touching bottom
            if ((self.ball_x + self.ball_size - 1) > self.pad_x) and (self.ball_x < (self.pad_x + self.pad_size + 1)):
                # if touch
                self.ball_y = self.ball_height * 2 - self.ball_y
                self.ball_dy = - self.ball_dy
                self.ball_dx -= random.uniform(
                    0.5,
                    ((self.pad_x + self.pad_size / 2) - (self.ball_x + self.ball_size / 2)) / 5
                )
                self.count += 1
                self.count_up = True
                self.info = str(self.count)
            else:
                self.game_over = 2
                self.info = str(self.count) + '  game over'
                self.count_up = True
        return

    def display(self):
        # display
        self.ball_disp.x = int(self.ball_x)
        self.ball_disp.y = int(self.ball_y)
        self.pad_disp.x = int(self.pad_x)
        if self.count_up:
            # change info text only when count changes
            self.count_up = False
            self.text_area.text = self.info
            

displayio.release_displays()
bus = board.SPI()
chip_select_pin = board.RX
framebuffer = sharpdisplay.SharpMemoryFramebuffer(bus, chip_select_pin, width=SCREEN_Y, height=SCREEN_X, baudrate=8000000)
display = framebufferio.FramebufferDisplay(framebuffer, rotation = 270)

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
    pad_max=[537, 580, 639, 440, 697, 697, 358],
    pad_min=[211, 212, 212, 212, 212, 212, 171],
)

app = BounceBall()
frame_app = FpsControl(fps=30)
fpsMonitor_app = FpsMonitor(period=10, fps_app=frame_app)

display.root_group = app.group
display.refresh()

# while True:
#     pass
while True:
    
    # Background procedures
    fpsMonitor_app()
    # FPS control
    if not frame_app():
        continue
    
    app.update(touch_bar_phy.get())
    
    app.display()
    
    display.refresh()