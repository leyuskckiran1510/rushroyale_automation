import ctypes
import ctypes.wintypes
from typing import Generator
import win32con, win32gui, win32api


cwinu32 = ctypes.windll.user32

# for more information :- https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
VIRTUAL_KEYS = {
    "K_LBUTTON": 0x01,
    "K_RBUTTON": 0x02,
    "K_CANCEL": 0x03,
    "K_MBUTTON": 0x04,
    "K_XBUTTON1": 0x05,
    "K_XBUTTON2": 0x06,
    "K_BACK": 0x08,
    "K_TAB": 0x09,
    "K_CLEAR": 0x0C,
    "K_RETURN": 0x0D,
    "K_SHIFT": 0x10,
    "K_CONTROL": 0x11,
    "K_MENU": 0x12,
    "K_PAUSE": 0x13,
    "K_CAPITAL": 0x14,
    "K_KANA": 0x15,
    "K_HANGUL": 0x15,
    "K_IME_ON": 0x16,
    "K_JUNJA": 0x17,
    "K_FINAL": 0x18,
    "K_HANJA": 0x19,
    "K_KANJI": 0x19,
    "K_IME_OFF": 0x1A,
    "K_ESCAPE": 0x1B,
    "K_CONVERT": 0x1C,
    "K_NONCONVERT": 0x1D,
    "K_ACCEPT": 0x1E,
    "K_MODECHANGE": 0x1F,
    "K_SPACE": 0x20,
    "K_PRIOR": 0x21,
    "K_NEXT": 0x22,
    "K_END": 0x23,
    "K_HOME": 0x24,
    "K_LEFT": 0x25,
    "K_UP": 0x26,
    "K_RIGHT": 0x27,
    "K_DOWN": 0x28,
    "K_SELECT": 0x29,
    "K_PRINT": 0x2A,
    "K_EXECUTE": 0x2B,
    "K_SNAPSHOT": 0x2C,
    "K_INSERT": 0x2D,
    "K_DELETE": 0x2E,
    "K_HELP": 0x2F,
    "K_LWIN": 0x5B,
    "K_RWIN": 0x5C,
    "K_APPS": 0x5D,
    "K_SLEEP": 0x5F,
    "K_NUMPAD0": 0x60,
    "K_NUMPAD1": 0x61,
    "K_NUMPAD2": 0x62,
    "K_NUMPAD3": 0x63,
    "K_NUMPAD4": 0x64,
    "K_NUMPAD5": 0x65,
    "K_NUMPAD6": 0x66,
    "K_NUMPAD7": 0x67,
    "K_NUMPAD8": 0x68,
    "K_NUMPAD9": 0x69,
    "K_MULTIPLY": 0x6A,
    "K_ADD": 0x6B,
    "K_SEPARATOR": 0x6C,
    "K_SUBTRACT": 0x6D,
    "K_DECIMAL": 0x6E,
    "K_DIVIDE": 0x6F,
    "K_F1": 0x70,
    "K_F2": 0x71,
    "K_F3": 0x72,
    "K_F4": 0x73,
    "K_F5": 0x74,
    "K_F6": 0x75,
    "K_F7": 0x76,
    "K_F8": 0x77,
    "K_F9": 0x78,
    "K_F10": 0x79,
    "K_F11": 0x7A,
    "K_F12": 0x7B,
    "K_F13": 0x7C,
    "K_F14": 0x7D,
    "K_F15": 0x7E,
    "K_F16": 0x7F,
    "K_F17": 0x80,
    "K_F18": 0x81,
    "K_F19": 0x82,
    "K_F20": 0x83,
    "K_F21": 0x84,
    "K_F22": 0x85,
    "K_F23": 0x86,
    "K_F24": 0x87,
    "K_NUMLOCK": 0x90,
    "K_SCROLL": 0x91,
    "K_LSHIFT": 0xA0,
    "K_RSHIFT": 0xA1,
    "K_LCONTROL": 0xA2,
    "K_RCONTROL": 0xA3,
    "K_LMENU": 0xA4,
    "K_RMENU": 0xA5,
    "K_BROWSER_BACK": 0xA6,
    "K_BROWSER_FORWARD": 0xA7,
    "K_BROWSER_REFRESH": 0xA8,
    "K_BROWSER_STOP": 0xA9,
    "K_BROWSER_SEARCH": 0xAA,
    "K_BROWSER_FAVORITES": 0xAB,
    "K_BROWSER_HOME": 0xAC,
    "K_VOLUME_MUTE": 0xAD,
    "K_VOLUME_DOWN": 0xAE,
    "K_VOLUME_UP": 0xAF,
    "K_MEDIA_NEXT_TRACK": 0xB0,
    "K_MEDIA_PREV_TRACK": 0xB1,
    "K_MEDIA_STOP": 0xB2,
    "K_MEDIA_PLAY_PAUSE": 0xB3,
    "K_LAUNCH_MAIL": 0xB4,
    "K_LAUNCH_MEDIA_SELECT": 0xB5,
    "K_LAUNCH_APP1": 0xB6,
    "K_LAUNCH_APP2": 0xB7,
    "K_OEM_1": 0xBA,
    "K_OEM_PLUS": 0xBB,
    "K_OEM_COMMA": 0xBC,
    "K_OEM_MINUS": 0xBD,
    "K_OEM_PERIOD": 0xBE,
    "K_OEM_2": 0xBF,
    "K_OEM_3": 0xC0,
    "K_OEM_4": 0xDB,
    "K_OEM_5": 0xDC,
    "K_OEM_6": 0xDD,
    "K_OEM_7": 0xDE,
    "K_OEM_8": 0xDF,
    "K_OEM_102": 0xE2,
    "K_PROCESSKEY": 0xE5,
    "K_PACKET": 0xE7,
    "K_ATTN": 0xF6,
    "K_CRSEL": 0xF7,
    "K_EXSEL": 0xF8,
    "K_EREOF": 0xF9,
    "K_PLAY": 0xFA,
    "K_ZOOM": 0xFB,
    "K_NONAME": 0xFC,
    "K_PA1": 0xFD,
    "K_OEM_CLEAR": 0xFE,
}


class Dragers:
    @staticmethod
    def linear(
        start: tuple[int, int], end: tuple[int, int]
    ) -> Generator[tuple[int, int]]:
        cur_x, cur_y = start
        end_x, end_y = end
        while cur_x <= end_x and cur_y <= end_y:
            cur_x += 1
            cur_y += 1
            yield cur_x, cur_y

        while cur_x <= end_x:
            cur_x += 1
            yield cur_x, cur_y
        while cur_y <= end_y:
            cur_y += 1
            yield cur_x, cur_y


class Event:
    _initiated = None
    setuped = False

    def __new__(cls, *args, **kwargs) -> "Event":
        if not Event._initiated:
            Event._initiated = super().__new__(cls)
        return Event._initiated

    def __init__(self, win_handle, /, force=False, **kwargs) -> None:
        if not self.setuped or force:
            self.win_handle = win_handle
            self.data = kwargs
            self.setuped = True
            self.old_pos = win32api.GetCursorPos()
        else:
            print("Already initialized")

    def __del__(self):
        win32api.SetCursorPos(self.old_pos)

    def _size(self):
        return (
            cwinu32.GetSystemMetrics(0),
            cwinu32.GetSystemMetrics(1),
        )

    def __limit_to_client_window(self, x, y):
        cx, cy, width, height = win32gui.GetWindowRect(self.win_handle)
        new_x = max(min(width, x), 0)
        new_y = max(min(height, y), 0)
        return int(cx + new_x), int(cy + new_y)

    def __focus_window(self):
        win32gui.ShowWindow(self.win_handle, win32con.SW_NORMAL)
        win32gui.SetWindowPos(self.win_handle, 0, 0, 0, 0, 0, win32con.SW_NORMAL)
        win32gui.SetForegroundWindow(self.win_handle)

    def __send_mouse_event(self, ev, x, y, scrollvalue=0):
        """
        for more information:-https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-mouse_event
        """
        self.__focus_window()
        width, height = self._size()
        x, y = self.__limit_to_client_window(x, y)
        convertedX = 65536 * x // width + 1
        convertedY = 65536 * y // height + 1
        cwinu32.mouse_event(
            ev | win32con.MOUSEEVENTF_ABSOLUTE,
            ctypes.c_long(convertedX),
            ctypes.c_long(convertedY),
            scrollvalue,
            0,
        )

    def __compute_virtual(self, key: str):
        vk = VIRTUAL_KEYS.get(key, -1)
        if len(key) == 1 and vk == -1:
            """for more information:- https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-vkkeyscana"""
            return cwinu32.VkKeyScanA(ctypes.wintypes.WCHAR(key))
        elif vk != -1:
            return vk
        else:
            raise ValueError(f"Unknown Key {key} supplied")

    def __send_key_event(self, ev, key):
        """
        for more informations:-https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-keybd_event
        """
        self.__focus_window()
        virtualKey = self.__compute_virtual(key)
        print(virtualKey, chr(virtualKey))
        cwinu32.keybd_event(virtualKey, 0, ev, 0)

    def press(self, key):
        ev = 0x00
        self.__send_key_event(ev, key)

    def type(self, word):
        for char in word:
            self.press(char)
            self.unpress(char)

    def unpress(self, key):
        ev = win32con.KEYEVENTF_KEYUP
        self.__send_key_event(ev, key)

    def click(self, x, y):
        self.move(x, y)
        ev = win32con.MOUSEEVENTF_LEFTDOWN
        self.__send_mouse_event(ev, x, y)
        ev = win32con.MOUSEEVENTF_LEFTUP
        self.__send_mouse_event(ev, x, y)

    def drag(self, start, end, func):
        for new_x, new_y in func(start, end):
            self.click(new_x, new_y)

    def move(self, x, y):
        ev = win32con.MOUSEEVENTF_MOVE
        self.__send_mouse_event(ev, x, y)


def __main__():
    win_name = "Rush Royale"
    win_name = "a - Paint"
    win_handle = win32gui.FindWindow(None, win_name)
    e = Event(win_handle)
    e.drag((100, 100), (120, 120), linear)
    # for i in range(1, 100, 10):
    #     e.click(100 + i, 101 + i)
    # e.press("K_CONTROL")
    # e.press("s")
    # e.unpress("K_CONTROL")

    # win_name = "a - Notepad"
    # win_handle = win32gui.FindWindow(None, win_name)
    # e = Event(win_handle, force=True)
    # e.type("Hello World")
    # e.press("K_CONTROL")
    # e.press("s")
    # e.unpress("K_CONTROL")


if __name__ == "__main__":
    __main__()
