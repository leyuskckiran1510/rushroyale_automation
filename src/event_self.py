import win32api, win32gui, win32con
import win32ui


from win32con import SM_CXSCREEN, SM_CYSCREEN


def calculate_absolute_coordinates(cx, cy, x, y):
    width, height = win32api.GetSystemMetrics(SM_CXSCREEN), win32api.GetSystemMetrics(
        SM_CYSCREEN
    )
    x = x * 65536
    y = y * 65536
    return cx + int(x / width), cy + int(y / height)


def tap(x, y, win_handle):
    x, y = int(x), int(y)
    ox, oy = win32api.GetCursorPos()
    curr_window = win32gui.GetForegroundWindow()

    win32gui.ShowWindow(win_handle, win32con.SW_NORMAL)
    win32gui.SetWindowPos(win_handle, 0, 0, 0, 0, 0, win32con.SW_NORMAL)
    win32gui.SetForegroundWindow(win_handle)

    cx, cy, width, height = win32gui.GetWindowRect(win_handle)
    cx, cy = win32gui.ClientToScreen(win_handle, (x, y))
    x, y = calculate_absolute_coordinates(cx, cy, x, y)
    print(cx, cy, width, height, x, y, ox, oy)
    # win32api.mouse_event(
    #     x, y, 0, win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, 0
    # )
    win32api.mouse_event(
        win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, x, y, 0, 0
    )
    print(win32api.GetCursorPos())
    # win32api.mouse_event(
    #     x, y, win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_ABSOLUTE, 0, 0
    # )
    # time.sleep(0.1)
    # win32api.mouse_event(
    #     x, y, win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_ABSOLUTE, 0, 0
    # )
    # win32api.mouse_event(
    #     x, y, win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_ABSOLUTE, 0, 0
    # )
    # win32api.mouse_event(
    #     win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_ABSOLUTE, x, y, 0, 0
    # )
    # win32api.mouse_event(
    #     win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_ABSOLUTE, x, y, 0, 0
    # )
    time.sleep(1 / 100)
    win32api.SetCursorPos((ox, oy))
    win32gui.SetActiveWindow(curr_window)


class Event:
    _initiated = None
    setuped = False

    def __new__(cls, *args, **kwargs) -> "Event":
        if not Event._initiated:
            Event._initiated = super().__new__(cls)
        return Event._initiated

    def __init__(self, *args, force=False, **kwargs) -> None:
        if not self.setuped or force:
            self.name = args
            self.data = kwargs
            self.setuped = True
        else:
            print("Already initialized")


import time

win_name = "Rush Royale"
win_name = "a - Paint"
handle = win32gui.FindWindow(None, win_name)
for i in range(1, 100, 100):
    tap(300 + i, 300 + i, handle)
    # send_left_click(handle, 300 + i, 300 + i)
    time.sleep(0.1)


def main():
    hwnd = win32gui.FindWindow(None, win_name)
    win = win32ui.CreateWindowFromHandle(hwnd)
    win32gui.SetForegroundWindow(hwnd)
    win.SendMessage(win32con.WM_CHAR, ord("A"), 0)
    win.SendMessage(win32con.WM_CHAR, ord("B"), 0)
    win.SendMessage(win32con.WM_KEYDOWN, 0x1E, 0)
