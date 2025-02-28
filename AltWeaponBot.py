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
from Jewel.wanted_mods_weapon import weapon_mods

DEBUG = False
STASHBLOCK_THRESHOLD = 0.92
ALT_THRESHOLD = 0.92
SCOUR_THRESHOLD = 0.92
AUG_THRESHOLD = 0.92
pause = True
alt_pos = None
aug_pos = None
failed_try = 0
total_alt_count = 0
total_aug_count = 0


alt_img = cv2.imread("Currency\\Alteration_2k.png")
aug_img = cv2.imread("Currency\\Augmetation_2k.png")

# backback stash is a 12*5 box
stash_left = 1303
stash_top = 571
stash_right = 1906
stash_bottom = 826

blocksize = int((stash_right - stash_left) / 12)
stash_blocks = []

for i in range(12):
    for j in range(2):
        stash_blocks.append(
            (
                int(stash_left + (i + 0.5) * blocksize),
                int(stash_top + (j * 2 + 0.5) * blocksize),
            )
        )


def check_pause():
    global pause
    global total_alt_count
    global total_aug_count
    while True:
        if win32api.GetKeyState(VK_CODE["F1"]) < 0:
            pause = True
            if DEBUG:
                print("pause")
        if win32api.GetKeyState(VK_CODE["F2"]) < 0 and pause:
            if DEBUG:
                print("start")
            pause = False
        if win32api.GetKeyState(VK_CODE["F3"]) < 0:
            print("exit")
            print("alt used:", total_alt_count)
            print("aug used:", total_aug_count)
            exit()
        if pause == False:
            return
        time.sleep(0.2)


def read_clipboard():
    while True:
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            return data
        except:
            time.sleep(0.2)
            return ""


def clear_clipboard():
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.CloseClipboard()
    except:
        pass


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
    time.sleep(0.2)


def mouse_leftclick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.03)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.2)


def Aug_Jewel(jewel_pos):
    global aug_pos
    global failed_try

    if aug_pos is None:
        win32api.SetCursorPos((0, 0))
        time.sleep(0.5)
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
    time.sleep(0.2)
    Ctrl_Alt_C()
    time.sleep(0.2)
    target_currency = read_clipboard()
    if regex.search("Augmentation", target_currency) is None:
        print("can't find aug")
        failed_try += 1
        aug_pos = None
        return
    mouse_rightclick()
    time.sleep(0.2)
    win32api.SetCursorPos(jewel_pos)
    time.sleep(0.2)
    mouse_leftclick()
    time.sleep(0.2)


def Alt_Jewel(jewel_pos):
    global alt_pos
    global failed_try

    if alt_pos is None:
        win32api.SetCursorPos((0, 0))
        time.sleep(0.5)
        screenshot = cv2.cvtColor(
            numpy.array(pyautogui.screenshot()),
            cv2.COLOR_RGB2BGR,
        )
        cv2.imwrite("screenshot.png", screenshot)
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
    time.sleep(0.2)
    Ctrl_Alt_C()
    time.sleep(0.2)

    target_currency = read_clipboard()
    if regex.search("Alteration", target_currency) is None:
        print("can't find alt")
        failed_try += 1
        alt_pos = None
        return
    mouse_rightclick()
    time.sleep(0.2)
    win32api.SetCursorPos(jewel_pos)
    time.sleep(0.2)
    mouse_leftclick()
    time.sleep(0.2)

    return


# main loop of alt all jewel
def main():
    global pause
    global total_alt_count
    global total_aug_count

    alt_count = 0
    aug_count = 0
    stash_pos = (400, 600)
    while True:
        check_pause()
        print(f"alt used:{total_alt_count}, aug used:{total_aug_count}", end="\r")
        win32api.SetCursorPos(stash_pos)
        clear_clipboard()
        time.sleep(0.1)
        Ctrl_Alt_C()
        time.sleep(0.1)
        target_jewel = read_clipboard()
        count = 0
        jewel = []

        for mod, weihgt in weapon_mods:
            result = regex.search(mod, target_jewel)
            if result is not None:
                print(mod[0], result)
                count += weihgt
        if count:
            time.sleep(0.1)
            print(f"Alt used:{alt_count}, {jewel}")
            pause = True
            check_pause()

        Alt_Jewel(stash_pos)
        alt_count += 1
        total_alt_count += 1

        check_pause()
        win32api.SetCursorPos(stash_pos)
        clear_clipboard()
        time.sleep(0.1)
        Ctrl_Alt_C()
        time.sleep(0.1)
        target_jewel = read_clipboard()
        count = 0
        jewel = []
        has_prefix = False
        for mod, weihgt in weapon_mods:
            result = regex.search(mod, target_jewel)
            if result is not None:
                # print(mod[0], int(result.group(1))
                count += weihgt
                print(mod, count, weihgt)
            if "Prefix Modifier" in target_jewel:
                has_prefix = True
        if count >= 1:
            time.sleep(0.1)
            print(f"Alt used:{alt_count}, {jewel}")
            pause = True
            check_pause()
        if has_prefix:
            continue
        time.sleep(0.1)
        Aug_Jewel(stash_pos)
        aug_count += 1
        total_aug_count += 1


main()
