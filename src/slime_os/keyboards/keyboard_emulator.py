from slime_os.keycode import Keycode

class Keyboard:
    def __init__(self, sos):
        self.sos = sos
        self.keys = {}

    def _key_to_keycode(self, key):
        if key == 13:
            return Keycode.ENTER
        if key == 1073741906:
            return Keycode.UP_ARROW
        if key == 1073741903:
            return Keycode.RIGHT_ARROW
        if key == 1073741905:
            return Keycode.DOWN_ARROW
        if key == 1073741904:
            return Keycode.LEFT_ARROW
        if key >= 97:
            return key-93

        return -1

    def set_key_down(self, key):
        self.keys[self._key_to_keycode(key)] = True

    def set_key_up(self, key):
        self.keys[self._key_to_keycode(key)] = False

    def get_key(self, key):
        return self.keys.get(key)

    def get_keys(self, keys):
        result = {}
        for key in keys:
            result[key] = self.get_key(key)
        return result

    def get_all(self):
        return self.keys
