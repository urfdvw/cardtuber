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