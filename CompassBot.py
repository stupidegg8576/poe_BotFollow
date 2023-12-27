import win32clipboard
import win32con
import win32api
import time
from keycode import VK_CODE
import cv2
import pyautogui
import numpy

DEBUG = True
VOIDSTONE_THRESHOLD = 0.93
STASHBLOCK_THRESHOLD = 0.93
SEXTANT_THRESHOLD = 0.93
COMPASS_THRESHOLD = 0.93

stashblock_img = cv2.imread("img\\Stashblock.png")
voidstone_img = cv2.imread("img\\Voidstone_socketed.png")
compass_img = cv2.imread("img\\Compass.png")
compass_mask = cv2.imread("img\\CompassMask.png")
sextant_img = cv2.imread("img\\Sextant.png")
sextant_mask = cv2.imread("img\\SextantMask.png")


def Ctrl_C():
    win32api.keybd_event(VK_CODE["ctrl"], 0, 0, 0)
    win32api.keybd_event(VK_CODE["c"], 0, 0, 0)
    win32api.keybd_event(VK_CODE["ctrl"], 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(VK_CODE["c"], 0, win32con.KEYEVENTF_KEYUP, 0)


def find_empty_stashblock():
    """
    find empty stashblock in screenshot
    Returns:
        max val x, y
    """
    screenshot = pyautogui.screenshot()
    result = cv2.matchTemplate(screenshot, stashblock_img, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_location, max_location = cv2.minMaxLoc(result)
    if max_val >= STASHBLOCK_THRESHOLD:
        if DEBUG:
            print(max_val, max_location)
            tmp = cv2.rectangle(
                screenshot,
                max_location,
                (
                    max_location[0] + stashblock_img.shape[1],
                    max_location[1] + stashblock_img.shape[0],
                ),
                (0, 0, 255),
                2,
            )
            cv2.imshow("screenshot", tmp)
        return (
            max_location[0] + stashblock_img.shape[1] / 2,
            max_location[1] + stashblock_img.shape[0] / 2,
        )


def find_voidstone():
    screenshot = pyautogui.screenshot()
    result = cv2.matchTemplate(screenshot, voidstone_img, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_location, max_location = cv2.minMaxLoc(result)
    if max_val >= VOIDSTONE_THRESHOLD:
        if DEBUG:
            print(max_val, max_location)
            tmp = cv2.rectangle(
                screenshot,
                max_location,
                (
                    max_location[0] + voidstone_img.shape[1],
                    max_location[1] + voidstone_img.shape[0],
                ),
                (0, 0, 255),
                2,
            )
            cv2.imshow("screenshot", tmp)
        return (
            max_location[0] + voidstone_img.shape[1] / 2,
            max_location[1] + voidstone_img.shape[0] / 2,
        )


def find_compass():
    screenshot = pyautogui.screenshot()
    result = cv2.matchTemplate(
        screenshot, compass_img, cv2.TM_CCORR_NORMED, mask=compass_mask
    )
    min_val, max_val, min_location, max_location = cv2.minMaxLoc(result)
    if max_val >= COMPASS_THRESHOLD:
        if DEBUG:
            print(max_val, max_location)
            tmp = cv2.rectangle(
                screenshot,
                max_location,
                (
                    max_location[0] + compass_img.shape[1],
                    max_location[1] + compass_img.shape[0],
                ),
                (0, 0, 255),
                2,
            )
            cv2.imshow("screenshot", tmp)
        return (
            max_location[0] + compass_img.shape[1] / 2,
            max_location[1] + compass_img.shape[0] / 2,
        )
    pass


def find_sextant():
    screenshot = pyautogui.screenshot()
    result = cv2.matchTemplate(
        screenshot, sextant_img, cv2.TM_CCORR_NORMED, mask=sextant_mask
    )
    min_val, max_val, min_location, max_location = cv2.minMaxLoc(result)
    if max_val >= SEXTANT_THRESHOLD:
        if DEBUG:
            print(max_val, max_location)
            tmp = cv2.rectangle(
                screenshot,
                max_location,
                (
                    max_location[0] + sextant_img.shape[1],
                    max_location[1] + sextant_img.shape[0],
                ),
                (0, 0, 255),
                2,
            )
            cv2.imshow("screenshot", tmp)
        return (
            max_location[0] + sextant_img.shape[1] / 2,
            max_location[1] + sextant_img.shape[0] / 2,
        )
    pass


while True:
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    print(data)
    time.sleep(2)
