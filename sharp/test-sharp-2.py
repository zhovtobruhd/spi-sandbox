import time
import sys
from datetime import datetime

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from sharpmemorydisplay import SharpMemoryDisplay

def test_rectangle(d):
    image = Image.new("1", (w, h))
    draw = ImageDraw.Draw(image)

    for i in range(min(w, h) // (BORDER * 2)):
        draw.rectangle(
            (0 + BORDER * i, 0 + BORDER * i, w - BORDER * i - 1, h - BORDER * i - 1), 
            outline=WHITE if (i % 2 == 0) else BLACK, 
            fill=WHITE if (i % 2 == 0) else BLACK
        )
        d.dummy(np.packbits(np.asarray(image.rotate(180, expand=1)), axis=1).flatten().tolist())
        d.show()

# Colors
BLACK = 0
WHITE = 255

# Parameters to Change
BORDER = 4
FONTSIZE = 24

display = SharpMemoryDisplay(1, 0)

w = display.width
h = display.height

display.dummy([0xff] * (w * h // 8))
display.show()

try:
    test_rectangle(display)
except KeyboardInterrupt:
    pass
except Exception as e:
    print(e)
    with open('log.txt', 'w', encoding='utf-8') as f:
        f.write(str(e))
finally:
    del display

