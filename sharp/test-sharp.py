from sharpmemorydisplay import SharpMemoryDisplay
import time

display = SharpMemoryDisplay(bus=1, cs=0)
width  = 144
height = 168

# for i in range(width // 8):
#     b = [0] * (width * height // 8)
#     for j in range(height):
#         b[i + j * (width // 8)] = 0xff
#     display.dummy(b)
#     display.show()
#     time.sleep(0.1)

b = [0] * (width * height // 8)

for i in range(5, 7):
    for j in range(height):
        b[j * (width // 8) + i // 8] |= (1 << (i % 8))
        #display.set_pixel(i, j, 1)
#display.show()

display.dummy(b)

del display
