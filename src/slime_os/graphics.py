import json

from config import config

class Gfx:
    def __init__(self, sos):
        self.display = sos["display"]
        self.dw, self.dh = self.display.get_bounds()

        self.is_flipped = config["display"]["flipped"]
        with sos["hardware"].open("slime_os/monospace.font.json", "r") as f:
            self.font = json.load(f)

    def set_pen(self, *args, **kwargs):
        self.display.set_pen(*args, **kwargs)

    def create_pen(self, r,g,b):
        return self.display.create_pen(r,g,b)

    def _adjust_x(self, x, w=0):
        if self.is_flipped:
            return self.dw - w - x
        else:
            return x

    def _adjust_y(self, y, h=0):
        if self.is_flipped:
            return self.dh - h - y
        else:
            return y

    def rectangle(self, *args):
        x, y, w, h = args
        x = self._adjust_x(x, w)
        y = self._adjust_y(y, h)
        self.display.rectangle(x, y, w, h)

    def pixel(self, *args):
        x, y = args
        x = self._adjust_x(x)
        y = self._adjust_y(y)
        self.display.pixel(x, y)

    def line(self, *args, **kwargs):
        x1, y1, x2, y2 = args[0:4]
        x1 = self._adjust_x(x1)
        y1 = self._adjust_y(y1)
        x2 = self._adjust_x(x2)
        y2 = self._adjust_y(y2)
        t = args[4] if len(args) == 5 else 1
        self.display.line(x1, y1, x2, y2, t, **kwargs)

    def text(self, *args, **kwargs):
        text = args[0]
        ox = args[1]
        oy = args[2]

        x_step = self.font["glyph_width"] + 1
        y_step = self.font["glyph_height"] + 1

        for line_y, line in enumerate(text.split("\n")):
            for letter_x, letter in enumerate(line):
                lines = self.font["ops"][letter]["lines"]
                pixels = self.font["ops"][letter]["pixels"]

                for line in lines:
                    [x1, y, x2] = line
                    x1 += ox + (letter_x*x_step)
                    y += oy + (line_y*y_step)
                    x2 += ox + (letter_x*x_step)
                    fx1 = self._adjust_x(x1)
                    fx2 = self._adjust_x(x2)
                    fy = self._adjust_y(y)
                    self.display.line(fx1, fy, fx2, fy, 1)

                for pixel in pixels:
                    [x, y] = pixel
                    x += ox + (letter_x*x_step)
                    y += oy + (line_y*y_step)
                    fx = self._adjust_x(x)
                    fy = self._adjust_y(y)
                    self.display.pixel(fx, fy)

    def measure_text(self, text, scale=1):
        return ((len(text) * (self.font["glyph_width"] + 1)) - 1) * scale

    def update(self):
        return self.display.update()
