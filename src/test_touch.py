import time
import board
import touchio

touch_pads = [
    touchio.TouchIn(board.A0),
    touchio.TouchIn(board.A1),
    touchio.TouchIn(board.A2),
    touchio.TouchIn(board.A3),
    touchio.TouchIn(board.SDA),
    touchio.TouchIn(board.SCL),
    touchio.TouchIn(board.TX)
]
#%% show touched pad
while False:
    for i in range(len(touch_pads)):
        if touch_pads[i].value:
            print(i)
        time.sleep(0.05)
#%% show raw valus
while True:
    print('startplot:', 'value')
    for i in range(len(touch_pads)):
        print(touch_pads[i].raw_value)
    time.sleep(1)    