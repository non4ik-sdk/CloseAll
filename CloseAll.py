import ctypes
from ctypes import wintypes
import sys
import time

user32 = ctypes.WinDLL("user32", use_last_error=True)

EnumWindows = user32.EnumWindows
EnumWindows.argtypes = (ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM), wintypes.LPARAM)
EnumWindows.restype = wintypes.BOOL

EnumChildWindows = user32.EnumChildWindows
EnumChildWindows.argtypes = (wintypes.HWND, ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM), wintypes.LPARAM)
EnumChildWindows.restype = wintypes.BOOL

IsWindowVisible = user32.IsWindowVisible
IsWindowVisible.argtypes = (wintypes.HWND,)
IsWindowVisible.restype = wintypes.BOOL

IsWindow = user32.IsWindow
IsWindow.argtypes = (wintypes.HWND,)
IsWindow.restype = wintypes.BOOL

GetWindowTextLengthW = user32.GetWindowTextLengthW
GetWindowTextLengthW.argtypes = (wintypes.HWND,)
GetWindowTextLengthW.restype = ctypes.c_int

GetClassNameW = user32.GetClassNameW
GetClassNameW.argtypes = (wintypes.HWND, wintypes.LPWSTR, ctypes.c_int)
GetClassNameW.restype = ctypes.c_int

PostMessageW = user32.PostMessageW
PostMessageW.argtypes = (wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)
PostMessageW.restype = wintypes.BOOL

GetDlgCtrlID = user32.GetDlgCtrlID
GetDlgCtrlID.argtypes = (wintypes.HWND,)
GetDlgCtrlID.restype = ctypes.c_int

WM_CLOSE = 0x0010
BM_CLICK = 0x00F5

IDOK = 1
IDYES = 6
PREFERRED_IDS = {IDYES, IDOK}

BLACKLIST_CLASSES = {
    "Shell_TrayWnd",
    "Progman",
    "WorkerW",
    "TaskManagerWindow",
    "Windows.UI.Core.CoreWindow"
}

def auto_accept_dialog(hwnd):

    def enum_child(child, _):
        ctrl_id = GetDlgCtrlID(child)

        if ctrl_id in PREFERRED_IDS:
            PostMessageW(child, BM_CLICK, 0, 0)
            time.sleep(0.03)
            return False

        return True

    EnumChildWindows(hwnd, CHILD_ENUM_PROC(enum_child), 0)


def close_user_windows():

    def enum_window(hwnd, _):

        if not IsWindow(hwnd):
            return True

        if not IsWindowVisible(hwnd):
            return True

        text_len = GetWindowTextLengthW(hwnd)
        if text_len == 0:
            return True

        class_buf = ctypes.create_unicode_buffer(64)
        GetClassNameW(hwnd, class_buf, 64)

        class_name = class_buf.value

        if class_name in BLACKLIST_CLASSES:
            return True

        if class_name == "#32770":
            auto_accept_dialog(hwnd)
        else:
            PostMessageW(hwnd, WM_CLOSE, 0, 0)
            time.sleep(0.03)

        return True

    EnumWindows(WINDOW_ENUM_PROC(enum_window), 0)


WINDOW_ENUM_PROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
CHILD_ENUM_PROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)


if __name__ == "__main__":
    close_user_windows()
    sys.exit(0)
