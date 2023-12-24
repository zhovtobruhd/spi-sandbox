"""
spidev module for:

* `Adafruit SHARP Memory Display Breakout - 1.3 inch 144x168 Monochrome <https://www.adafruit.com/product/3502>`_

"""
from time import sleep

import spidev


def sleep_ms(msecs):
    sleep(float(msecs) / 1000.0)


def reverse_bit(num: int) -> int:
    """Turn an LSB byte to an MSB byte, and vice versa"""
    result = 0
    for _ in range(8):
        result <<= 1
        result += num & 1
        num >>= 1
    return result


class SharpMemoryDisplay:
    """Driver class"""

    _SHARPMEM_BIT_WRITECMD = 0x01 # 0x80 in lsb
    _SHARPMEM_BIT_VCOM =     0x02 # 0x40 in lsb
    _SHARPMEM_BIT_CLEAR =    0x04 # 0x20 in lsb

    def __init__(self, bus, cs, width=144, height=168, mode=0, max_speed_hz=1000000):
        self.width = width
        self.height = height

        self.spi = spidev.SpiDev()
        self.spi.open(bus, cs)
        self.spi.max_speed_hz = max_speed_hz
        self.spi.mode = mode
        self.spi.lsbfirst = True

        # in SHARP displays CS is active HIGH
        self.spi.cshigh = False

        # prealloc for when we write the display
        self._buf = bytearray(1)

        self.buffer = bytearray([0xff] * (width // 8) * height)

        # Set the vcom bit to a defined state
        self._vcom = True

    def __del__(self):
        try:
            self.spi.close()
        except:
            pass

    def dummy(self, b):
        for i, v in enumerate(self.buffer):
            self.buffer[i] = b[i]
    
    def set_pixel(self, x, y, v) -> None:
        if v == 0:
            self.buffer[y * (self.width // 8) + x // 8] &= ~(1 << (x % 8))
        else:
            self.buffer[y * (self.width // 8) + x // 8] |= (1 << (x % 8))

    def show(self) -> None:
        """write out the frame buffer"""

        image_buffer = bytearray()
        # toggle the VCOM bit
        self._buf[0] = self._SHARPMEM_BIT_WRITECMD
        if self._vcom:
            self._buf[0] |= self._SHARPMEM_BIT_VCOM
        self._vcom = not self._vcom
        image_buffer.extend(self._buf)

        slice_from = 0
        line_len = self.width // 8
        for line in range(self.height):
            self._buf[0] = line + 1
            image_buffer.extend(self._buf)
            image_buffer.extend([reverse_bit(b) for b in self.buffer[slice_from : slice_from + line_len]])
            slice_from += line_len
            self._buf[0] = 0
            image_buffer.extend(self._buf)
        image_buffer.extend(self._buf)

        self.spi.cshigh = True
        # sleep_ms(1)
        self.spi.writebytes(image_buffer)
        # sleep_ms(1)
        self.spi.cshigh = False
        # sleep_ms(1)
