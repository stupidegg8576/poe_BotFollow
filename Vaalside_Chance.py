import win32clipboard
import win32con
import win32api
import time
from keycode import VK_CODE
import cv2
import pyautogui
import numpy

rare_vaalside = cv2.imread("Currency\\rare_vaalside.png")
magic_vaalside = cv2.imread("Currency\\magic_vaalside.png")
normal_vaalside = cv2.imread("Currency\\normal_vaalside.png")
scour = cv2.imread("Currency\\scour.png")
chance = cv2.imread("Currency\\chance.png")
pause = True


def check_pause():
    global pause
    while True:
        if win32api.GetKeyState(VK_CODE["F1"]) < 0:
            pause = True
        if win32api.GetKeyState(VK_CODE["F2"]) < 0 and pause:
            pause = False
        if pause == False:
            return
        time.sleep(0.06)


def read_clipboard():
    while True:
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            return data
        except:
            time.sleep(0.06)


def Ctrl_Alt_C():
    win32api.keybd_event(VK_CODE["ctrl"], 0, 0, 0)
    win32api.keybd_event(VK_CODE["alt"], 0, 0, 0)
    win32api.keybd_event(VK_CODE["c"], 0, 0, 0)
    win32api.keybd_event(VK_CODE["ctrl"], 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(VK_CODE["alt"], 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(VK_CODE["c"], 0, win32con.KEYEVENTF_KEYUP, 0)


def mouse_rightclick():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    time.sleep(0.06)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
    time.sleep(0.05)


def mouse_leftclick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.06)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.05)


check_pause()
vaalside_pos = None
screenshot = cv2.cvtColor(numpy.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
vaalside_res = cv2.matchTemplate(screenshot, normal_vaalside, cv2.TM_CCORR_NORMED)
min_val, max_val, min_location, max_location = cv2.minMaxLoc(vaalside_res)
if max_val > 0.90:
    vaalside_pos = max_location
count = 0
while True:
    count += 1
    if count % 10 == 0:
        print(count)
    check_pause()

    chance_res = cv2.matchTemplate(screenshot, chance, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_location, max_location = cv2.minMaxLoc(chance_res)
    if max_val > 0.94:
        win32api.SetCursorPos(
            (
                max_location[0] + int(chance.shape[1] / 2),
                max_location[1] + int(chance.shape[0] / 2),
            )
        )
        time.sleep(0.06)
        mouse_rightclick()
        time.sleep(0.06)
        win32api.SetCursorPos(
            (
                vaalside_pos[0],
                vaalside_pos[1] + int(normal_vaalside.shape[0] / 2),
            )
        )
        time.sleep(0.06)
        mouse_leftclick()
        time.sleep(0.06)
        win32api.SetCursorPos((0, 0))
    else:
        time.sleep(0.06)

    win32api.SetCursorPos((0, 0))
    check_pause()

    screenshot = cv2.cvtColor(numpy.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    scour_res = cv2.matchTemplate(screenshot, scour, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_location, max_location = cv2.minMaxLoc(scour_res)
    if max_val > 0.92:
        win32api.SetCursorPos(
            (
                max_location[0] + int(scour.shape[1] / 2),
                max_location[1] + int(scour.shape[0] / 2),
            )
        )
        time.sleep(0.06)
        mouse_rightclick()
        time.sleep(0.06)
        win32api.SetCursorPos(
            (
                vaalside_pos[0],
                vaalside_pos[1] + int(normal_vaalside.shape[0] / 2),
            )
        )
        time.sleep(0.06)
        mouse_leftclick()
        time.sleep(0.06)
    else:
        print("None!")
        time.sleep(0.3)
        continue
