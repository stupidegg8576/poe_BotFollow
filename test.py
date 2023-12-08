# you will need the win32 libraries for this snippet of code to work, Links below
import win32gui
import win32con
import win32api
from time import sleep
import pyautogui

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
print(SCREEN_WIDTH, SCREEN_HEIGHT)
