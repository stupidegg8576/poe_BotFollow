import win32clipboard
import win32con
import win32api
import time
from keycode import VK_CODE
import cv2
import pyautogui
import numpy

while True:
    print(win32api.GetCursorPos())
    time.sleep(0.5)
