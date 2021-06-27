import serial

_CMD_PREFIX_KB = [0x57, 0xAB, 0x00, 0x02, 0x08]
_CMD_PREFIX_MOUSE = [0x57, 0xAB, 0x00, 0x05, 0x05, 0x01]


class HidDevice:
    def __init__(self, port=None,
                 baudrate=9600,
                 timeout=None):
        self._serial = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        if not self._serial.isOpen():
            self._serial.open()

    def send_report(self, data):
        if len(data) == 8:
            self._send_keyboard_report(data)
        else:
            self._send_mouse_report(data)

    def _send_keyboard_report(self, data):
        hid_data = bytearray()
        hid_data.extend(_CMD_PREFIX_KB)
        hid_data.extend(data)
        hid_data.append(sum(hid_data) % 256)
        print('键盘命令:', len(hid_data), hid_data)
        self._serial.write(data=hid_data)

    def _send_mouse_report(self, data):
        hid_data = bytearray()
        hid_data.extend(_CMD_PREFIX_MOUSE)
        hid_data.extend(data)
        hid_data.append(sum(hid_data) % 256)
        print('鼠标命令：', len(hid_data), hid_data)
        self._serial.write(data=hid_data)
