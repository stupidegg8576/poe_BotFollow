import win32api
import win32con
import time
from keycode import VK_CODE

DEBUG = False


def mouse_leftclick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.1)


def check_pause():
    global pause
    while True:
        if win32api.GetKeyState(VK_CODE["z"]) < 0:
            pause = True
            if DEBUG:
                print("pause")
        if win32api.GetKeyState(VK_CODE["x"]) < 0 and pause:
            if DEBUG:
                print("start")
            pause = False
        if pause == False:
            return
        time.sleep(0.1)


pause = True

while True:
    if pause:
        time.sleep(0.1)
    check_pause()
    mouse_leftclick()
    time.sleep(0.1)
