# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from PIL import Image
import pyscreenshot as ImageGrab
import wx
import pytesseract
import re
import time
from playsound import playsound

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
        #Use Below for static window overlay
        wx.Frame.__init__(self, None, title='Fancy', style=style, size=(200, 75))

        #Use below for movable window overlay
        #wx.Frame.__init__(self, None, style=wx.TE_RICH, size=(200, 75))

        # For transparency use 0-255 with 255 being fully transparent
        self.SetTransparent(255)
        self.Show(True)
        # lets put some text
        self.mystext = wx.StaticText(self, label="", style=wx.TE_RICH)




        # create font object
        self.font = self.mystext.GetFont()

        # increase text size
        self.font.PointSize += 33

        # make text bold
        self.font = self.font.Bold()

        # associate font with text
        self.mystext.SetFont(self.font)

    def updateText(self, newText):
        mystext = wx.StaticText(self, label="Team Total: $" + newText)

    def updateTextColor(self):
        self.mystext.SetForegroundColour((255, 0, 0))
        self.mystext.SetBackgroundColour((0, 255, 0))


def alignToBottomRight(win):
    dw, dh = wx.DisplaySize()
    w, h = win.GetSize()
    # x = dw - w
    x = 0
    y = dh - h
    win.SetPosition((x, y))

def getTotalCash():
    y1 = 900
    x1 = 30
    y2 = 1380
    x2 = 400

    # grab screenshot from section of screen
    # img = ImageGrab.grab(bbox=(10, 10, 500, 500)) # X1,Y1,X2,Y2
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))  # X1,Y1,X2,Y2
    img.save('ocr-image.png')
    ocrtext = pytesseract.image_to_string(img)
    print("OCR Text: " + ocrtext)

    # Regex the OCR text string for names
    # name = re.findall(r'[a-zA-Z\s]+$', ocrtext)

    # below works and matches all text?
    # name = re.findall(r'(\b[A-Z][a-z]*\b)(.*)(\b[A-Z][a-z]*\b)', ocrtext)

    name = re.findall(r'\$(\d+)', ocrtext)

    print(type(name))
    # print(" ".join(name))
    print(name)

    # numbers_int = [int(x) for x in name]

    retypeInt = [int(x) for x in name]

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

    #y1 = dh - 900


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

    frame.Show()
    # f = FancyFrame()

    print("Running App.mainloop()")
    app.MainLoop()
    print ("Ran Mainloop")

if __name__ == '__main__':
    x = 0
    while x < 10:
        main()
        x = x+1
        print("X Value: " + str(x))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
