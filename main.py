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
import numpy as np
import random

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

totalCash = 0

time.sleep(3)

currentTotal = 0
previousTotal = 0


class TextExample(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(TextExample, self).__init__(*args, **kwargs)
        style = (wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR |
                 wx.NO_BORDER | wx.FRAME_SHAPED)
        # Use Below for static window overlay
        wx.Frame.__init__(self, None, title='Fancy', style=style, size=(200, 75))

        # Use below for movable window overlay
        # wx.Frame.__init__(self, None, style=wx.TE_RICH, size=(200, 75))

        # For transparency use 0-255 with 255 being fully transparent
        self.SetTransparent(255)
        self.Show(True)
        # lets put some text
        self.mystext = wx.StaticText(self, label="", style=wx.TE_RICH)
        self.SetForegroundColour('red')

        # create wx.font object to pass to static text
        font = wx.Font(99, family=wx.FONTFAMILY_MODERN, style=0, weight=90, underline=True, faceName="",
                       encoding=wx.FONTENCODING_DEFAULT)
        # font = wx.Font(88, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        # set font for the statictext
        self.mystext.SetFont(font)

        # create font object
        # self.font = self.mystext.GetFont()

        # increase text size
        # self.font.PointSize += 33

        # make text bold
        # self.font = self.font.Bold()

        # associate font with text
        # self.mystext.SetFont(self.font)

    def updateText(self, newText):
        mystext = wx.StaticText(self, label="                                      ")
        mystext = wx.StaticText(self, label="Team Total: $" + newText)
        # self.wx.SETFOREGROUNDCOLOUR((255,0,0))

    def updateTextColor(self):
        self.mystext.SetForegroundColour((255, 0, 0))
        self.mystext.SetBackgroundColour((0, 255, 0))


def alignToBottomRight(win):
    dw, dh = wx.DisplaySize()
    w, h = win.GetSize()
    # x = dw - w
    x = 0
    y = dh - h
    win.SetPosition((400, y))


def imageBounder():
    # load the image
    # load the image
    # image = cv2.imread("ct1.png")
    image = cv2.imread("ocrImage.png")

    # define list of RGB boundaries
    # boundaries = [([103, 86, 65], [145, 133, 128])]

    # create numpy arrays from the boundaries
    lower = np.array([133, 136, 115], dtype="uint8")
    upper = np.array([225, 225, 210], dtype="uint8")

    # Catches a lot   lower = np.array([113, 126, 115], dtype="uint8")
    # upper = np.array([235, 245, 230], dtype="uint8")

    # find colors in specified RGB boundary and apply mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)

    # show the final image
    # cv2.imshow("images", np.hstack([image, output, ]))

    fileName = "boundaryOutput.png"

    cv2.imwrite(fileName, output)


def getTotalCash():
    y1 = 900
    x1 = 30
    y2 = 1440
    x2 = 400

    # grab screenshot from section of screen
    # img = ImageGrab.grab(bbox=(10, 10, 500, 500)) # X1,Y1,X2,Y2
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))  # X1,Y1,X2,Y2

    # save image with random number appended
    randomNum = random.randint(11, 99)
    #ocrImageName = 'ocr-image'+ str(randomNum)+ '.png'
    #img.save(ocrImageName)
    img.save('ocrImage.png')

    #finds black and white bounds of text and outputs as boundaryOutput.png
    imageBounder()

    img = "boundaryOutput.png"

    ocrtext = pytesseract.image_to_string(img)
    print("OCR Text: " + ocrtext)

    # Regex the OCR text string for names
    # name = re.findall(r'[a-zA-Z\s]+$', ocrtext)

    # below works and matches all text?
    # name = re.findall(r'(\b[A-Z][a-z]*\b)(.*)(\b[A-Z][a-z]*\b)', ocrtext)

    amounts = re.findall(r'\$(\d+)', ocrtext)

    # print(type(name))
    # print(" ".join(name))
    # print(name)

    # numbers_int = [int(x) for x in name]
    # check to see if OCR detected numbers (hundreds)
    # for x in amounts:
    # print(x)
    retypeInt = [int(x) for x in amounts]

    total = sum(retypeInt)

    print(total)

    return total


def main():
    print('Testing Output')
    # determine screen resolution to find bottom left corner for screen shot coordinates (acquisition to send to OCR)
    global previousTotal
    global currentTotal
    app = wx.App()
    frame = TextExample(None, title="Read Text", size=(100, 200))

    dw, dh = wx.DisplaySize()
    w, h = frame.GetSize()
    # x = dw - w

    # y1 = dh - 900

    # y1 = 900
    # x2 = 300
    # y2 = 1300
    # x1 = 0

    total = getTotalCash()

    currentTotal = total

    if currentTotal != previousTotal:
        playsound('CashTotalTargetSound.mp3')
        previousTotal = currentTotal

    frame.updateText(str(total))

    alignToBottomRight(frame)
    app.SetTopWindow(frame)

    frame.updateTextColor()
    # frame.mystext.SetForegroundColour('blue')

    frame.Show()
    # f = FancyFrame()

    timer = wx.Timer(frame)
    timer.Start(3000)

    def onTimer(evt):
        total = getTotalCash()

        global currentTotal
        global previousTotal
        currentTotal = total
        print("CurrentTotal:" + str(currentTotal))
        print("PreviousTotal:" + str(previousTotal))

        if currentTotal != previousTotal:
            # if currentTotal > 10000:
            # playsound('CashTotalTargetSound.mp3')

            previousTotal = currentTotal
            frame.updateText(str(total))

    frame.Bind(wx.EVT_TIMER, onTimer)

    print("Running App.mainloop()")
    app.MainLoop()
    print("Ran Mainloop")


if __name__ == '__main__':
    x = 0
    while x < 10:
        main()
        x = x + 1
        print("X Value: " + str(x))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
