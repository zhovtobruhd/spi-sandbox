from sharpmemorydisplay import SharpMemoryDisplay
import time

display = SharpMemoryDisplay(bus=1, cs=0)
width  = 144
height = 168

for i in range(0, 144):
    b = [0xff] * (width * height // 8)
    for j in range(height):
        b[i // 8 + j * (width // 8)] &= ~(1 << (7 - i % 8)) & 0xff
    display.dummy(b)
    display.show()
    # time.sleep(0.1)


del display
