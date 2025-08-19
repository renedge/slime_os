from machine import Pin, I2C, UART, SPI
import sdcard


class Hardware:
    def __init__(self, sos):
        self.Pin = Pin
        self.I2C = I2C
        self.UART = UART
        self.SPI = SPI
        self.sdcard = sdcard
        self.open = open
        self._adc_enabled = False
        self._sos = sos

    def get_expansion_adc(self):
        if not self._adc_enabled:
            self._sos["display"].set_gpu_io_adc_enable(29, True)
            self._adc_enabled = True
        return self._sos["display"].get_gpu_io_adc_voltage(29)
