import cv2
import numpy
from matplotlib import pyplot as plt
import win32gui
import win32con
import win32api
import time
import pyautogui
import keycode


def press(key):
    """
    one press, one release.
    accepts as many arguments as you want. e.g. press('left_arrow', 'a','b').
    """

    win32api.keybd_event(keycode.VK_CODE[key], 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(keycode.VK_CODE[key], 0, win32con.KEYEVENTF_KEYUP, 0)


template = cv2.imread("template.png")

w, h = template.shape[0], template.shape[1]

methods = [
    "cv2.TM_CCOEFF",
    "cv2.TM_CCOEFF_NORMED",
    "cv2.TM_CCORR",
    "cv2.TM_CCORR_NORMED",
    "cv2.TM_SQDIFF",
    "cv2.TM_SQDIFF_NORMED",
]

time.sleep(1)
while True:
    start_time = time.time()
    # screenshot = cv2.imread("screen.png")
    screenshot = pyautogui.screenshot()
    # screenshot = numpy.array(screenshot)
    screenshot = cv2.cvtColor(numpy.array(screenshot), cv2.COLOR_RGB2BGR)
    method = cv2.TM_CCORR_NORMED

    res = cv2.matchTemplate(screenshot, template, method)
    # val = match Similarity
    min_val, max_val, min_location, max_location = cv2.minMaxLoc(res)
    print(max_val)
    if max_val < 0.95:
        time.sleep(0.1)
        continue

    top_left = max_location

    bottom_right = (top_left[0] + w, top_left[1] + h)
    print(f"Time cost: {time.time() - start_time}")
    print(f"Target: {top_left}, {bottom_right}")

    win32api.SetCursorPos((top_left[0] + 5, top_left[1] + 5))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.07)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.07)
    press("q")
