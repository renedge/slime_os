import os


class Hardware:
    def __init__(self, sos):
        self.Pin = {}
        self.I2C = {}
        self.UART = {}
        self.SPI = {}
        self.os = OS()
        self.gc = GC()
        self.sdcard = SDCard()
        self.open = _open

    def get_expansion_adc(self):
        return 0


def toEmulatorPath(filename):
    if filename.startswith("/sd/"):
        filename = os.path.abspath(os.path.join(".tmp", filename[4:]))
    return filename


def _open(filename, mode):
    filename = toEmulatorPath(filename)
    return open(filename, mode)


class OS:
    def __init__(self):
        self.listdir = os.listdir

    def mount(self, sd, path):
        return None

    def stat(self, filename):
        filename = toEmulatorPath(filename)
        return os.stat(filename)


class SDCard:
    def get_sdcard(self):
        return None


class GC:
    def collect(self):
        pass

    def mem_free(self):
        return 100 * 1000

    def mem_alloc(self):
        return 50 * 1000
