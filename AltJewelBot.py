import win32clipboard
import win32con
import win32api
import time
from keycode import VK_CODE
import cv2
import pyautogui
import numpy
import regex
import yaml
from Jewel.wanted_mods import jewel_mods

DEBUG = False
STASHBLOCK_THRESHOLD = 0.92
ALT_THRESHOLD = 0.92
SCOUR_THRESHOLD = 0.92
AUG_THRESHOLD = 0.92
pause = True
alt_pos = None
aug_pos = None
failed_try = 0


alt_img = cv2.imread("Currency\\Alteration.png")
aug_img = cv2.imread("Currency\\Augmetation.png")

# backback stash is a 12*5 box
stash_left = 1303
stash_top = 571
stash_right = 1906
stash_bottom = 826

blocksize = int((stash_right - stash_left) / 12)
stash_blocks = []

for i in range(12):
    for j in range(5):
        stash_blocks.append(
            (
                int(stash_left + (i + 0.5) * blocksize),
                int(stash_top + (j + 0.5) * blocksize),
            )
        )


def check_pause():
    global pause
    while True:
        if win32api.GetKeyState(VK_CODE["F1"]) < 0:
            pause = True
            if DEBUG:
                print("pause")
        if win32api.GetKeyState(VK_CODE["F2"]) < 0 and pause:
            if DEBUG:
                print("start")
            pause = False
        if pause == False:
            return
        time.sleep(0.1)


def read_clipboard():
    while True:
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            return data
        except:
            time.sleep(0.1)
            return ""


def clear_clipboard():
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()


def Ctrl_Alt_C():
    win32api.keybd_event(VK_CODE["ctrl"], 0, 0, 0)
    win32api.keybd_event(VK_CODE["alt"], 0, 0, 0)
    win32api.keybd_event(VK_CODE["c"], 0, 0, 0)
    win32api.keybd_event(VK_CODE["ctrl"], 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(VK_CODE["alt"], 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(VK_CODE["c"], 0, win32con.KEYEVENTF_KEYUP, 0)


def mouse_rightclick():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    time.sleep(0.03)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
    time.sleep(0.05)


def mouse_leftclick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.03)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.05)


def Aug_Jewel(jewel_pos):
    global aug_pos
    global failed_try

    if aug_pos is None:
        time.sleep(0.1)
        screenshot = cv2.cvtColor(
            numpy.array(pyautogui.screenshot()),
            cv2.COLOR_RGB2BGR,
        )

        aug_res = cv2.matchTemplate(screenshot, aug_img, cv2.TM_CCORR_NORMED)
        min_val, max_val, min_location, max_location = cv2.minMaxLoc(aug_res)
        if max_val >= AUG_THRESHOLD:
            aug_pos = (
                int(max_location[0] + aug_img.shape[1] / 2),
                int(max_location[1] + aug_img.shape[0] / 2),
            )
        else:
            failed_try += 1
            print("can't find aug")
            return

    if failed_try >= 50:
        print("failed to find aug jewel")
        exit()

    win32api.SetCursorPos(aug_pos)
    clear_clipboard()
    time.sleep(0.05)
    Ctrl_Alt_C()
    time.sleep(0.05)
    target_currency = read_clipboard()
    if regex.search("Augmentation", target_currency) is None:
        print("can't find aug")
        aug_pos = None
        return
    mouse_rightclick()
    time.sleep(0.05)
    win32api.SetCursorPos(jewel_pos)
    time.sleep(0.05)
    mouse_leftclick()
    time.sleep(0.05)


def Alt_Jewel(jewel_pos):
    global alt_pos
    global failed_try

    if alt_pos is None:
        time.sleep(0.1)
        screenshot = cv2.cvtColor(
            numpy.array(pyautogui.screenshot()),
            cv2.COLOR_RGB2BGR,
        )

        alt_res = cv2.matchTemplate(screenshot, alt_img, cv2.TM_CCORR_NORMED)
        min_val, max_val, min_location, max_location = cv2.minMaxLoc(alt_res)

        if max_val >= ALT_THRESHOLD:
            alt_pos = (
                int(max_location[0] + alt_img.shape[1] / 2),
                int(max_location[1] + alt_img.shape[0] / 2),
            )
        else:
            failed_try += 1
            print("can't find alt")
            return

    if failed_try >= 50:
        print("failed to find alt jewel")
        exit()

    win32api.SetCursorPos(alt_pos)
    clear_clipboard()
    time.sleep(0.05)
    Ctrl_Alt_C()
    time.sleep(0.05)

    target_currency = read_clipboard()
    if regex.search("Alteration", target_currency) is None:
        print("can't find alt")
        alt_pos = None
        return
    mouse_rightclick()
    time.sleep(0.05)
    win32api.SetCursorPos(jewel_pos)
    time.sleep(0.05)
    mouse_leftclick()
    time.sleep(0.05)

    return


# main loop of alt all jewel
def main():
    global pause
    total_alt_count = 0
    total_aug_count = 0
    for jewel_pos in stash_blocks:
        alt_count = 0
        aug_count = 0
        while True:
            check_pause()
            win32api.SetCursorPos(jewel_pos)
            clear_clipboard()
            time.sleep(0.1)
            Ctrl_Alt_C()
            time.sleep(0.1)
            target_jewel = read_clipboard()
            count = 0
            jewel = []
            for mod in jewel_mods:
                result = regex.search(mod[0], target_jewel)
                if result is not None:
                    if int(result.group(1)) >= mod[1]:
                        jewel.append(f"{mod[0]}, {int(result.group(1))}")
                        # print(mod[0], int(result.group(1))
                        count += 1

            if count >= 2:
                print(f"Alt used:{alt_count}, {jewel}")
                break

            Alt_Jewel(jewel_pos)
            alt_count += 1
            total_alt_count += 1

            check_pause()
            win32api.SetCursorPos(jewel_pos)
            clear_clipboard()
            time.sleep(0.1)
            Ctrl_Alt_C()
            time.sleep(0.1)
            target_jewel = read_clipboard()
            count = 0
            jewel = []
            for mod in jewel_mods:
                result = regex.search(mod[0], target_jewel)
                if result is not None:
                    if int(result.group(1)) >= mod[1]:
                        jewel.append(f"{mod[0]}, {int(result.group(1))}")
                        # print(mod[0], int(result.group(1))
                        count += 1
            if count == 0:
                continue
            Aug_Jewel(jewel_pos)
            aug_count += 1
            total_aug_count += 1


main()
