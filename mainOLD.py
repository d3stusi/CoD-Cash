# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from PIL import Image
import pyscreenshot as ImageGrab
import wx
import pytesseract
import re
import time


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


totalCash = 0

time.sleep(3)


class TextExample(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(TextExample, self).__init__(*args, **kwargs)
        style = (wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR |
                 wx.NO_BORDER | wx.FRAME_SHAPED)
        wx.Frame.__init__(self, None, title='Fancy', style=style, size=(200, 75))

        # For transparency use 0-255 with 255 being fully transparent
        self.SetTransparent(100)
        self.Show(True)
        # lets put some text
        mystext = wx.StaticText(self, label="Team Total: $" + str(totalCash))
        # create font object
        font = mystext.GetFont()

        # increase text size
        font.PointSize += 4

        # make text bold
        font = font.Bold()

        # associate font with text
        mystext.SetFont(font)

    def updateText(self, newText):
        mystext = wx.StaticText(self, label="Team Total: $" + newText)


def alignToBottomRight(win):
    dw, dh = wx.DisplaySize()
    w, h = win.GetSize()
    # x = dw - w
    x = 0
    y = dh - h
    win.SetPosition((x, y))


def main():
    print('Testing Output')
    # determine screen resolution to find bottom left corner for screen shot coordinates (acquisition to send to OCR)

    app = wx.App()
    frame = TextExample(None, title="Read Text", size=(100, 200))

    dw, dh = wx.DisplaySize()
    w, h = frame.GetSize()
    # x = dw - w

    #y1 = dh - 900

    # x1 = 0
    # y1 = 900
    # x2 = 300
    # y2 = 1300



    # grab screenshot from section of screen
    # img = ImageGrab.grab(bbox=(10, 10, 500, 500)) # X1,Y1,X2,Y2
    img = ImageGrab.grab()  # X1,Y1,X2,Y2
    img.save('ocr-image.png')
    ocrtext = pytesseract.image_to_string(img)
    
    print("OCR Text: " + ocrtext)

    # Regex the OCR text string for names
    # name = re.findall(r'[a-zA-Z\s]+$', ocrtext)
    # https://stackoverflow.com/questions/43422093/regex-finding-capital-words-in-string
    name = re.findall(r'(\b[A-Z][a-z]*\b)(.*)(\b[A-Z][a-z]*\b)', ocrtext)
    print(type(name))
    # print(" ".join(name))
    print(name)
    alignToBottomRight(frame)
    app.SetTopWindow(frame)

    frame.updateText(ocrtext)
    frame.Show()
    # f = FancyFrame()
    app.MainLoop()


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
