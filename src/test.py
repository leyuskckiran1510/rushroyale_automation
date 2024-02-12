import ctypes
from os.path import dirname, abspath

try:
    parent_dir = dirname(dirname(abspath(__file__)))
    mouse_click = ctypes.CDLL(rf"{parent_dir}\mouse_click.dll")
except FileNotFoundError as e:
    raise Exception(
        f"{e.with_traceback(None)}\n\n{'-'*10}\nPlease Run \n\t./run.sh prepdll\n{'-'*10}\n "
    )
print(mouse_click._FuncPtr.__dict__)
mouse_click.moue_click.argtypes = [ctypes.c_ulong, ctypes.c_int, ctypes.c_int]
mouse_click.moue_click.restype = None

ev = 0x0002 | 0x4  # Example: MOUSEEVENTF_LEFTDOWN
x = 146  # Example: x-coordinate
y = 342  # Example: y-coordinate
for i in range(1, 20, 10):
    mouse_click.moue_click(ev, x + i, y + i)
