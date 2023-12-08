import cv2
import numpy
from matplotlib import pyplot as plt
import win32gui
import win32con
import win32api
import time
import pyautogui
import keycode

MOVEMENT_CD = 3.2
# SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600


def press(key):
    """
    one press, one release.
    accepts as many arguments as you want. e.g. press('left_arrow', 'a','b').
    """

    win32api.keybd_event(keycode.VK_CODE[key], 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(keycode.VK_CODE[key], 0, win32con.KEYEVENTF_KEYUP, 0)


last_movement = 0


def movement_skill(x, y):
    if time.time() - last_movement < MOVEMENT_CD:
        return
    x, y = find_window_edge(x, y)
    win32api.SetCursorPos((int(x), int(y)))
    press("q")
    time.sleep(0.1)


def find_window_edge(x, y):
    char_x, char_y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
    x_to_target, y_to_target = x - char_x, y - char_y
    target_x, target_y = x, y

    n = 1
    while (
        target_x > SCREEN_WIDTH * 0.2
        and target_x < SCREEN_WIDTH * 0.8
        and target_y > SCREEN_HEIGHT * 0.2
        and target_y < SCREEN_HEIGHT * 0.8
    ):
        target_x = char_x + n * x_to_target
        target_y = char_y + n * y_to_target
        n += 1

    target_x = char_x + (n - 1) * x_to_target
    target_y = char_y + (n - 1) * y_to_target

    return target_x, target_y


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
pause = True

while True:
    if win32api.GetKeyState(keycode.VK_CODE["z"]) < 0:
        pause = True
        print("pause")
    if win32api.GetKeyState(keycode.VK_CODE["x"]) < 0 and pause:
        print("start")

    if pause:
        time.sleep(1)
        continue

    start_time = time.time()
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(numpy.array(screenshot), cv2.COLOR_RGB2BGR)
    method = cv2.TM_CCORR_NORMED

    res = cv2.matchTemplate(screenshot, template, method)
    # val = match Similarity
    min_val, max_val, min_location, max_location = cv2.minMaxLoc(res)

    if max_val < 0.95:
        time.sleep(0.1)
        continue

    print(f"Time cost: {time.time() - start_time}")
    print(f"Target: {max_location}")

    win32api.SetCursorPos((max_location[0] + 5, max_location[1] + 5))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.07)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    movement_skill(max_location[0] + 5, max_location[1] + 5)
