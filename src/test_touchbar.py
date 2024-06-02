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

# touch_bar_phy = TouchBarPhysics(
#     pads=touch_pads,
#     pad_max=[537, 580, 639, 440, 697, 697, 358],
#     pad_min=[211, 212, 212, 212, 212, 212, 171],
# )

touch_bar_phy = TouchBarPhysicsSimple(
    pads=touch_pads,
)


# print('startplot:', 'x', 'z')
start_x = 0
for i in range(100000):
    time.sleep(0.5)
    raw = touch_bar_phy.get()
    # print(raw.x, raw.z)
    
    # for simple only, for non-simple, need another navigation wrapper
    if touch_bar_phy.z.diff > 0.5:
        # start touch
        start_x = touch_bar_phy.x.now
    if touch_bar_phy.z.diff < -0.5:
        # end touch
        print("distance", touch_bar_phy.x.now - start_x)
    if touch_bar_phy.z.now > 0.5 and touch_bar_phy.x.diff:
        print("move", touch_bar_phy.x.diff)
        
    