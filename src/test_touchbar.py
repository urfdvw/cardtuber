import time
import board
import touchio

from touchpad import TouchBarPhysics

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


print('startplot:', 'x', 'z')
for i in range(100000):
    time.sleep(0.01)
    raw = touch_bar_phy.get()
    print(raw.x, raw.z)