import time
from keycode import KeyCode

_MAX_KEYPRESSES = 6


class FakeKeyboard:
    def __init__(self, device):
        self.report_modifier = None
        self.report = bytearray(8)
        self.report_keys = memoryview(self.report)[2:]
        self.report_modifier = memoryview(self.report)[0:1]
        self._keyboard_device = device
        try:
            self.release_all()
        except OSError:
            time.sleep(1)
            self.release_all()

    def press(self, *keycodes):
        for keycode in keycodes:
            self._add_keycode_to_report(keycode)
        self._keyboard_device.send_report(self.report)

    def release(self, *keycodes):
        for keycode in keycodes:
            self._remove_keycode_from_report(keycode)
        self._keyboard_device.send_report(self.report)

    def release_all(self):
        for i in range(8):
            self.report[i] = 0
        self._keyboard_device.send_report(self.report)

    def send(self, *keycodes):
        self.press(*keycodes)
        self.release_all()

    def _add_keycode_to_report(self, keycode):
        modifier = KeyCode.modifier_bit(keycode)
        if modifier:
            # Set bit for this modifier.
            self.report_modifier[0] |= modifier
        else:
            # Don't press twice.
            # (I'd like to use 'not in self.report_keys' here, but that's not implemented.)
            for i in range(_MAX_KEYPRESSES):
                if self.report_keys[i] == keycode:
                    # Already pressed.
                    return
            # Put keycode in first empty slot.
            for i in range(_MAX_KEYPRESSES):
                if self.report_keys[i] == 0:
                    self.report_keys[i] = keycode
                    return
            # All slots are filled.
            raise ValueError("Trying to press more than six keys at once.")

    def _remove_keycode_from_report(self, keycode):
        """Remove a single keycode from the report."""
        modifier = KeyCode.modifier_bit(keycode)
        if modifier:
            # Turn off the bit for this modifier.
            self.report_modifier[0] &= ~modifier
        else:
            # Check all the slots, just in case there's a duplicate. (There should not be.)
            for i in range(_MAX_KEYPRESSES):
                if self.report_keys[i] == keycode:
                    self.report_keys[i] = 0
