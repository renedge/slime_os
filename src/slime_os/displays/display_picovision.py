from display_picovision import PicoVision, PEN_P5


class Display:
    def __init__(self, sos):
        self.display = PicoVision(PEN_P5, 400, 240)
        self.width = 400
        self.height = 240

    def tick(self):
        pass

    def get_bounds(self, *args, **kwargs):
        return self.display.get_bounds(*args, **kwargs)

    def update(self, *args, **kwargs):
        return self.display.update(*args, **kwargs)

    def line(self, *args, **kwargs):
        return self.display.line(*args, **kwargs)

    def pixel(self, *args, **kwargs):
        return self.display.pixel(*args, **kwargs)

    def rectangle(self, *args, **kwargs):
        return self.display.rectangle(*args, **kwargs)

    def create_pen(self, *args, **kwargs):
        return self.display.create_pen(*args, **kwargs)

    def set_pen(self, *args, **kwargs):
        return self.display.set_pen(*args, **kwargs)
