from slime_os.keyboards.keyboard_emulator import Keyboard
from slime_os.displays.display_emulator import Display
from slime_os.hardware.emulator import Hardware

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
    "display": {"flipped": False},
    "modules": {
        "keyboard": Keyboard,
        "display": Display,
        "hardware": Hardware,
    },
}
