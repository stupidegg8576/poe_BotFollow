import cv2
import numpy
from matplotlib import pyplot as plt
import win32gui
import win32con
import win32api
import time
import pyautogui
import keycode

template = cv2.imread("Compass\\voidstone.png")

while True:
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(numpy.array(screenshot), cv2.COLOR_RGB2BGR)
    method = cv2.TM_CCORR_NORMED

    res = cv2.matchTemplate(screenshot, template, method)
    # val = match Similarity
    min_val, max_val, min_location, max_location = cv2.minMaxLoc(res)

    if max_val < 0.95:
        time.sleep(0.1)
        continue

    print(f"Target: {max_location}, {max_val}")
    time.sleep(1)
