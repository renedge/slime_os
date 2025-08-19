from picovision import PicoVision, PEN_P5


class Display:
    def __init__(self, sos):
        self.pv = PicoVision(PEN_P5, 400, 240)
        self.width = 400
        self.height = 240

    def tick(self):
        pass

    def get_bounds(self, *args, **kwargs):
        return self.pv.get_bounds(*args, **kwargs)

    def update(self, *args, **kwargs):
        return self.pv.update(*args, **kwargs)

    def line(self, *args, **kwargs):
        return self.pv.line(*args, **kwargs)

    def pixel(self, *args, **kwargs):
        return self.pv.pixel(*args, **kwargs)

    def rectangle(self, *args, **kwargs):
        return self.pv.rectangle(*args, **kwargs)

    def create_pen(self, *args, **kwargs):
        return self.pv.create_pen(*args, **kwargs)

    def set_pen(self, *args, **kwargs):
        return self.pv.set_pen(*args, **kwargs)

