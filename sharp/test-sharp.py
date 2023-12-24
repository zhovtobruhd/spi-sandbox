from sharpmemorydisplay import SharpMemoryDisplay
import time

display = SharpMemoryDisplay(bus=1, cs=0)
width  = 144
height = 168

for i in range(width // 8):
    b = [0] * (width * height // 8)
    for j in range(height):
        b[i + j * (width // 8)] = 0xff
    display.dummy(b)
    display.show()
    time.sleep(0.1)
del display