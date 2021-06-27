import fake_keyboard
import fake_mouse
import hid_device
from keycode import KeyCode

if __name__ == '__main__':
    device = hid_device.HidDevice(port='COM1', baudrate=9600, timeout=50)
    keyboard = fake_keyboard.FakeKeyboard(device=device)
    mouse = fake_mouse.FakeMouse(device=device)
    keyboard.press(KeyCode.A)
    keyboard.release(KeyCode.A)
    mouse.move(x=-3)
