import time
import sys
import math
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


def test_triangle(d):
    image = Image.new("1", (w, h))
    draw = ImageDraw.Draw(image)

    x1, y1 = w // 2, 0
    x2, y2 = 0, h - 1 
    x3, y3 = w - 1, 0

    draw.polygon(
        [(x1, y1), (x2, y2), (x3, y3)], 
        outline=BLACK, 
        fill=BLACK
    )

    # Lengths of sides of the triangle
    a = ((x2 - x3)**2 + (y2 - y3)**2)**0.5
    b = ((x1 - x3)**2 + (y1 - y3)**2)**0.5
    c = ((x1 - x2)**2 + (y1 - y2)**2)**0.5

    j = BORDER

    h = (b**2 - (a/2)**2) ** 0.5
    k = 2 * j * b / a
    i = (h - k - j) * a / (2 * h)

    #for i in range(min(w, h) // (BORDER * 2)):
    i0 = 1
    draw.polygon(
        [(x1, y1 + k), (x1 - i, y2 - j), (x1 + i, y3 - j)], 
        outline=WHITE if (i0 % 2 == 0) else BLACK, 
        fill=WHITE if (i0 % 2 == 0) else BLACK
    )
    d.dummy(np.packbits(np.asarray(image.rotate(180, expand=1)), axis=1).flatten().tolist())
    d.show()
    

def test_line(d):
    image = Image.new("1", (w, h))

    draw = ImageDraw.Draw(image)

    # Upper left corner

    draw.rectangle(
            (0, 0, w - 1, h - 1), 
            outline=WHITE,
            fill=WHITE
        )

    for i in range(h // (BORDER * 2)):
        draw.line(
            (0, 0, w - 1, BORDER * 2 * i), 
            width=1, 
            fill=BLACK
        )
        d.dummy(np.packbits(np.asarray(image.rotate(180, expand=1)), axis=1).flatten().tolist())
        d.show()

    for i in range(w // (BORDER * 2)):
        draw.line(
            (0, 0, w - BORDER * 2 * i - 1, h - 1), 
            width=1, 
            fill=BLACK
        )
        d.dummy(np.packbits(np.asarray(image.rotate(180, expand=1)), axis=1).flatten().tolist())
        d.show()

    # Upper right corner

    draw.rectangle(
            (0, 0, w - 1, h - 1), 
            outline=WHITE,
            fill=WHITE
        )

    for i in range(h // (BORDER * 2)):
        draw.line(
            (w - 1, 0, 0, BORDER * 2 * i), 
            width=1, 
            fill=BLACK
        )
        d.dummy(np.packbits(np.asarray(image.rotate(180, expand=1)), axis=1).flatten().tolist())
        d.show()

    for i in range(w // (BORDER * 2)):
        draw.line(
            (w - 1, 0, BORDER * 2 * i, h - 1), 
            width=1, 
            fill=BLACK
        )
        d.dummy(np.packbits(np.asarray(image.rotate(180, expand=1)), axis=1).flatten().tolist())
        d.show()

    # Lower right corner

    draw.rectangle(
            (0, 0, w - 1, h - 1), 
            outline=WHITE,
            fill=WHITE
        )

    for i in range(h // (BORDER * 2)):
        draw.line(
            (w - 1, h - 1, 0, h - BORDER * 2 * i - 1), 
            width=1, 
            fill=BLACK
        )
        d.dummy(np.packbits(np.asarray(image.rotate(180, expand=1)), axis=1).flatten().tolist())
        d.show()

    for i in range(w // (BORDER * 2)):
        draw.line(
            (w - 1, h - 1, BORDER * 2 * i, 0), 
            width=1, 
            fill=BLACK
        )
        d.dummy(np.packbits(np.asarray(image.rotate(180, expand=1)), axis=1).flatten().tolist())
        d.show()
    
    # Lower left corner

    draw.rectangle(
            (0, 0, w - 1, h - 1), 
            outline=WHITE,
            fill=WHITE
        )

    for i in range(h // (BORDER * 2)):
        draw.line(
            (0, h - 1, w - 1, h - BORDER * 2 * i - 1), 
            width=1, 
            fill=BLACK
        )
        d.dummy(np.packbits(np.asarray(image.rotate(180, expand=1)), axis=1).flatten().tolist())
        d.show()

    for i in range(w // (BORDER * 2)):
        draw.line(
            (0, h - 1, w - BORDER * 2 * i - 1, 0), 
            width=1, 
            fill=BLACK
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
    test_line(display)
    test_triangle(display)
except KeyboardInterrupt:
    pass
except Exception as e:
    print(e)
    with open('log.txt', 'w', encoding='utf-8') as f:
        f.write(str(e))
finally:
    del display

