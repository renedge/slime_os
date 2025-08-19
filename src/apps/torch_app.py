"""
app["name"]="Torch"
app["id"]="torch_app"
app["icon"]="0000000001000000000000000110100000000000111010000000000011111000000000001111100000000001011111000000000110111100000000011101110000000001100011000000000010000100000000110111100000000111000000000000111000000000000101000000000000101000000000000011000000000000"
"""

import slime_os as sos


class App:
    def setup(self, _):
        self.uart = sos.get_expansion_uart()

        self.led_on = True

    def run(self):
        last_led_on = False
        while True:

            if self.led_on != last_led_on:
                sos.gfx.set_pen(sos.config["theme"]["black"])
                sos.gfx.rectangle(0, 0, sos.gfx.width, sos.gfx.height)
                sos.gfx.set_pen(sos.config["theme"]["white"])
                message = ""
                if self.led_on:
                    self.uart.write(bytes("[sos].led_on", "ascii"))
                    message = "FLASHLIGHT ON"
                if not self.led_on:
                    self.uart.write(bytes("[sos].led_off", "ascii"))
                    message = "FLASHLIGHT OFF"

                sos.gfx.text(message, 20, 20, scale=3)
                sos.gfx.set_pen(sos.config["theme"]["grey"])
                sos.gfx.text("[Press Enter to Toggle]", 20, 50, scale=1)
                yield sos.INTENT_FLIP_BUFFER
                last_led_on = self.led_on

            keys = sos.keyboard.get_keys([sos.keycode.ENTER, sos.keycode.Q])

            if keys[sos.keycode.ENTER]:
                self.led_on = not self.led_on

            if keys[sos.keycode.Q]:
                yield sos.INTENT_KILL_APP
                break

            yield sos.INTENT_NO_OP

    def cleanup(self):
        pass


if __name__ == "__main__":
    sos.boot(App)
