# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from PIL import Image, ImageFilter
import pyscreenshot as ImageGrab
import wx
import pytesseract
import re
import time
from playsound import playsound
import cv2
import imageio
from matplotlib import pyplot as plt
import numpy as np

# load the image
image = cv2.imread("ct1.png")

# define list of RGB boundaries
boundaries = [([103, 86, 65], [145, 133, 128])]

for (lower, upper) in boundaries:
    # create numpy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    # find colors in specified RGB boundary and apply mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)

    # show the final image
    cv2.imshow("images", np.hstack([image, output,]))
    cv2.waitKey(0)
