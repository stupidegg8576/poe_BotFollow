import cv2
import numpy
from matplotlib import pyplot as plt
import win32gui
import win32con
import win32api
import time
import pyautogui
import keycode

screenshot = cv2.imread("Compass\\Stash.png")
template = cv2.imread("Compass\\stash_block.png")
cv2.imshow("screenshot", screenshot)
while True:
    method = cv2.TM_CCORR_NORMED
    result = cv2.matchTemplate(screenshot, template, method)
    # val = match Similarity
    minval, maxval, minloc, maxloc = cv2.minMaxLoc(result)
    if maxval > 0.92:
        print("Found")
        screenshot = cv2.rectangle(
            screenshot,
            (maxloc[0] + 2, maxloc[1] + 2),
            (maxloc[0] + template.shape[0] - 2, maxloc[1] + template.shape[1] - 2),
            (0, 0, 255),
            1,
        )
    else:
        print("Not Found")
        cv2.imshow("screenshot", screenshot)
        time.sleep(100)
        break
    cv2.imshow("screenshot", screenshot)
    cv2.waitKey(1)
