from slime_os.keyboards.keyboard_i2c import Keyboard
from slime_os.displays.display_picovision import Display
from slime_os.hardware.micropython import Hardware

config = {
    "theme": {
        "black": (0, 0, 0),
        "red": (255, 0, 0),
        "blue": (0, 39, 65),
        "green": (0, 100, 0),
        "white": (255, 255, 255),
        "grey": (100, 100, 100),
        "yellow": (184, 184, 0),
    },
    "display": {"flipped": True},
    "modules": {
        "keyboard": Keyboard,
        "display": Display,
        "hardware": Hardware,
    },
}
