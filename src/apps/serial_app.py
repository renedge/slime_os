"""
app["name"]="Serial"
app["id"]="serial_app"
app["icon"]="1011111111111111101000000000000110101010001111011010000001111001101010001111000110100001111001011010001111001001101001111001000110101111001000011010000000000001101111111111111100000000000000000000011110000000000001111000000000000000000000000011111111111100"
"""

import slime_os as sos


class App:
    def setup(self, display):
        pass

    def run(self):
        offset = 0
        gfx = sos.graphics
        while True:
            gfx.set_pen(sos.config["theme"]["blue"])
            gfx.rectangle(0, 0, sos.display.width, sos.display.height)
            gfx.set_pen(sos.config["theme"]["white"])
            lines = []
            for i in range(0 + offset, 23 + offset):
                lines.append(str(i) + ": " + "X" * 57)

            gfx.text("\n".join(lines), 10, 10)
            offset += 1
            keys = sos.keyboard.get_keys([sos.keycode.Q])
            if keys[sos.keycode.Q]:
                yield sos.INTENT_KILL_APP
                break
            yield sos.INTENT_FLIP_BUFFER

    def cleanup(self):
        pass


if __name__ == "__main__":
    sos.boot(App)
