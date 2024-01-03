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

DEBUG = False
VOIDSTONE_THRESHOLD = 0.92
STASHBLOCK_THRESHOLD = 0.92
SEXTANT_THRESHOLD = 0.92
COMPASS_THRESHOLD = 0.92

jewel_list = []
jewel_list.append(cv2.imread("Jewel\\img\\Jewel1.png"))
jewel_list.append(cv2.imread("Jewel\\img\\Jewel2.png"))
jewel_list.append(cv2.imread("Jewel\\img\\Jewel3.png"))


alt_img = cv2.imread("Jewel\\img\\Alt.png")
aug_img = cv2.imread("Jewel\\img\\Aug.png")

screenshot = None

with open("Jewel\\wanted_mods.yaml") as f:
    wanted_mods = yaml.load(f, Loader=yaml.FullLoader)
