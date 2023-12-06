import cv2
import numpy as np
from matplotlib import pyplot as plt


img = cv2.imread("poe_img\\screen.png")
target = cv2.imread("poe_img\\target.png")
mask = cv2.imread("poe_img\\mask.png")
cv2.imshow("img", img)
cv2.imshow("target", target)
methods = [
    "cv2.TM_CCOEFF",
    "cv2.TM_CCOEFF_NORMED",
    "cv2.TM_CCORR",
    "cv2.TM_CCORR_NORMED",
    "cv2.TM_SQDIFF",
    "cv2.TM_SQDIFF_NORMED",
]
w = target.shape[1]
h = target.shape[0]

for meth in methods:
    method = eval(meth)
    res = cv2.matchTemplate(img, target, method, mask=mask)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc

    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(img, top_left, bottom_right, 255, 2)
    plt.subplot(121), plt.imshow(res, cmap="gray")
    plt.title("Matching Result"), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(img, cmap="gray")
    plt.title("Detected Point"), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)
    plt.show()
