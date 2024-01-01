import win32clipboard
import win32con
import win32api
import time
from keycode import VK_CODE
import cv2
import pyautogui
import numpy
import regex

DEBUG = False
VOIDSTONE_THRESHOLD = 0.92
STASHBLOCK_THRESHOLD = 0.92
SEXTANT_THRESHOLD = 0.92
COMPASS_THRESHOLD = 0.92

stashblock_img = cv2.imread("Compass\\img\\Stashblock.png")
voidstone_img = cv2.imread("Compass\\img\\Voidstone_socketed.png")
compass_img = cv2.imread("Compass\\img\\Compass.png")
compass_mask = cv2.imread("Compass\\img\\Compass_Mask.png")
sextant_img = cv2.imread("Compass\\img\\Sextant.png")
sextant_mask = cv2.imread("Compass\\img\\Sextant_Mask.png")
screenshot = None
pause = True
# print("SEXTANT 4 USES PASSIVES!!!")
# time.sleep(10)


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


def Ctrl_C():
    win32api.keybd_event(VK_CODE["ctrl"], 0, 0, 0)
    win32api.keybd_event(VK_CODE["c"], 0, 0, 0)
    win32api.keybd_event(VK_CODE["ctrl"], 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(VK_CODE["c"], 0, win32con.KEYEVENTF_KEYUP, 0)


def mouse_rightclick():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
    time.sleep(0.1)


def mouse_leftclick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.1)


def find_empty_stashblock():
    """
    find empty stashblock in screenshot
    Returns:
        max val x, y
    """
    result = cv2.matchTemplate(screenshot, stashblock_img, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_location, max_location = cv2.minMaxLoc(result)
    if max_val >= STASHBLOCK_THRESHOLD:
        return (
            int(max_location[0] + stashblock_img.shape[1] / 2),
            int(max_location[1] + stashblock_img.shape[0] / 2),
        )


def find_voidstone():
    result = cv2.matchTemplate(screenshot, voidstone_img, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_location, max_location = cv2.minMaxLoc(result)
    if max_val >= VOIDSTONE_THRESHOLD:
        return (
            int(max_location[0] + voidstone_img.shape[1] / 2),
            int(max_location[1] + voidstone_img.shape[0] / 2),
        )


def find_compass():
    result = cv2.matchTemplate(
        screenshot, compass_img, cv2.TM_CCORR_NORMED, mask=compass_mask
    )
    min_val, max_val, min_location, max_location = cv2.minMaxLoc(result)
    if max_val >= COMPASS_THRESHOLD:
        return (
            int(max_location[0] + compass_img.shape[1] / 2),
            int(max_location[1] + compass_img.shape[0] / 2),
        )
    pass


def find_sextant():
    result = cv2.matchTemplate(
        screenshot, sextant_img, cv2.TM_CCORR_NORMED, mask=sextant_mask
    )
    min_val, max_val, min_location, max_location = cv2.minMaxLoc(result)
    if max_val >= SEXTANT_THRESHOLD:
        return (
            int(max_location[0] + sextant_img.shape[1] / 2),
            int(max_location[1] + sextant_img.shape[0] / 2),
        )


def copy_voidstone_mod():
    Ctrl_C()
    time.sleep(0.1)
    win32clipboard.OpenClipboard()
    voidstone_mod = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return voidstone_mod


def use_sextant():
    sextant_pos = find_sextant()
    if sextant_pos is None:
        return -1
    win32api.SetCursorPos(sextant_pos)
    time.sleep(0.1)
    mouse_rightclick()
    time.sleep(0.1)
    return 0


def use_compass():
    time.sleep(0.5)
    compass_pos = find_compass()
    if compass_pos is None:
        return -1
    win32api.SetCursorPos(compass_pos)
    time.sleep(0.1)
    mouse_rightclick()
    time.sleep(0.1)
    return 0


def click_voidstone():
    voidstone_pos = find_voidstone()
    if voidstone_pos is None:
        return -1
    win32api.SetCursorPos(voidstone_pos)
    time.sleep(0.1)
    mouse_leftclick()
    time.sleep(0.1)
    return 0


def put_into_stash():
    stash_pos = find_empty_stashblock()
    if stash_pos is None:
        return -1
    win32api.SetCursorPos(stash_pos)
    time.sleep(0.1)
    mouse_leftclick()
    time.sleep(0.1)
    return 0


keepmods = []


def load_keepmods():
    with open("Compass\\keepmods.txt", "r") as f:
        t = f.readlines()
        for i in t:
            i = regex.sub(r"[\n]", "", i)
            keepmods.append(i)


# print(click_voidstone())
# exit()
load_keepmods()
while True:
    check_pause()
    win32api.SetCursorPos((0, 0))
    time.sleep(0.1)
    screenshot = cv2.cvtColor(numpy.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    if DEBUG:
        print("use_sextant")
    while True:
        check_pause()
        if use_sextant() == -1:
            if DEBUG:
                print("Can't find sextant")
            win32api.SetCursorPos((0, 0))
            time.sleep(0.5)
            screenshot = cv2.cvtColor(
                numpy.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR
            )
            continue
        else:
            break

    if DEBUG:
        print("click_voidstone")
    while True:
        check_pause()
        if click_voidstone() == -1:
            if DEBUG:
                print("Can't find voidstone")
            win32api.SetCursorPos((0, 0))
            time.sleep(0.5)
            screenshot = cv2.cvtColor(
                numpy.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR
            )
            continue
        else:
            break
    time.sleep(0.2)
    voidstone_mod = copy_voidstone_mod()
    found = None
    for mods in keepmods:
        if mods in voidstone_mod:
            found = mods
            break
    if found is not None:
        check_pause()
        print(found)
        win32api.SetCursorPos((0, 0))
        time.sleep(1)
        screenshot = cv2.cvtColor(
            numpy.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR
        )
        while True:
            check_pause()
            if use_compass() == -1:
                if DEBUG:
                    print("Can't find compass")
                win32api.SetCursorPos((0, 0))
                time.sleep(0.5)
                screenshot = cv2.cvtColor(
                    numpy.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR
                )
                continue
            else:
                break
        while True:
            check_pause()
            if click_voidstone() == -1:
                if DEBUG:
                    print("Can't find voidstone")
                win32api.SetCursorPos((0, 0))
                time.sleep(0.5)
                screenshot = cv2.cvtColor(
                    numpy.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR
                )
                continue
            else:
                break
        while True:
            check_pause()
            if put_into_stash() == -1:
                if DEBUG:
                    print("Can't find stash")
                win32api.SetCursorPos((0, 0))
                time.sleep(0.5)
                screenshot = cv2.cvtColor(
                    numpy.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR
                )
                continue
            else:
                break
    else:
        print("Sextant not want")
        time.sleep(0.1)
