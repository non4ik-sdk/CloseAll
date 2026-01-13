import ctypes
from ctypes import wintypes
import sys
import time

user32 = ctypes.WinDLL("user32", use_last_error=True)

EnumWindows = user32.EnumWindows
EnumChildWindows = user32.EnumChildWindows
EnumProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

IsWindowVisible = user32.IsWindowVisible
GetWindowTextLengthW = user32.GetWindowTextLengthW
GetClassNameW = user32.GetClassNameW
PostMessageW = user32.PostMessageW
GetDlgCtrlID = user32.GetDlgCtrlID

WM_CLOSE = 0x0010
BM_CLICK = 0x00F5

IDOK = 1
IDYES = 6
PREFERRED_IDS = (IDYES, IDOK)

BLACKLIST_CLASSES = {
    "Shell_TrayWnd",
    "Progman",
    "WorkerW",
    "TaskManagerWindow",
    "Windows.UI.Core.CoreWindow"
}

def auto_accept_dialog(hwnd):
    def enum_child(child, lparam):
        try:
            ctrl_id = GetDlgCtrlID(child)
            if ctrl_id in PREFERRED_IDS:
                PostMessageW(child, BM_CLICK, 0, 0)
                time.sleep(0.05)  # небольшая пауза
                return False
        except Exception:
            pass
        return True

    EnumChildWindows(hwnd, EnumProc(enum_child), 0)

def close_user_windows():
    def enum_window(hwnd, lparam):
        try:
            if not IsWindowVisible(hwnd):
                return True

            if GetWindowTextLengthW(hwnd) == 0:
                return True

            class_name = ctypes.create_unicode_buffer(64)
            GetClassNameW(hwnd, class_name, 64)

            if class_name.value in BLACKLIST_CLASSES:
                return True

            if class_name.value == "#32770":
                auto_accept_dialog(hwnd)
            else:
                PostMessageW(hwnd, WM_CLOSE, 0, 0)
                time.sleep(0.05)  # пауза после отправки сообщения

        except Exception:
            pass
        return True

    EnumWindows(EnumProc(enum_window), 0)

if __name__ == "__main__":
    try:
        close_user_windows()
    finally:
        sys.exit(0)
