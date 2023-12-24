import time
import sys
from datetime import datetime

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from sharpmemorydisplay import SharpMemoryDisplay

# Colors
BLACK = 0
WHITE = 255

# Parameters to Change
BORDER = 5
FONTSIZE = 24

display = SharpMemoryDisplay(1, 0)

w = display.width
h = display.height

display.dummy([0xff] * (w * h // 8))
display.show()

image = Image.new("1", (w, h))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, w, h), outline=BLACK, fill=BLACK)
draw.rectangle(
    (BORDER, BORDER, w - BORDER - 1, h - BORDER - 1),
    outline=WHITE,
    fill=WHITE,
)

start_time = datetime.now()

# Draw Some Text
try:
    while True:
        current_time = datetime.now()
        text_time = current_time.strftime("%H:%M:%S")
        elapsed = current_time - start_time
        text_elapsed = str(elapsed).split('.')[0]

        draw.rectangle(
            (BORDER, BORDER, w - BORDER - 1, h - BORDER - 1),
            outline=WHITE,
            fill=WHITE,
        )

        texts = []
        if len(sys.argv) > 1:
            texts.extend(sys.argv[1:])
        texts.append(text_time)
        texts.append(text_elapsed)

        while FONTSIZE > 1 and FONTSIZE * len(texts) > 0.8 * display.height:
            FONTSIZE -= 1
        else:
            # Load a TTF font.
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)

        for i, text in enumerate(texts):
            (font_width, font_height) = font.getsize(text)
            (c_w, c_h) = (display.width // 2, display.height * (i + 1) // (len(texts) + 1))
            draw.text(
                (c_w - font_width // 2, c_h - font_height // 2),
                text,
                font=font,
                fill=BLACK,
            )

#draw.line([0, 0, w - 1, h - 1], fill=BLACK, width=0)
#draw.line([0, h - 1, w - 1, 0], fill=BLACK, width=0)

        display.dummy(np.packbits(np.asarray(image.rotate(180, expand=1)), axis=1).flatten().tolist())
        display.show()
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
except Exception as e:
    print(e)
    with open('log.txt', 'w', encoding='utf-8') as f:
        f.write(str(e))
finally:
    del display

