import wx

def alignToBottomRight(win):
    dw, dh = wx.DisplaySize()
    w, h = win.GetSize()
    x = dw - w
    y = dh - h
    win.SetPosition((x, y))

app = wx.PySimpleApp()
frame = wx.MiniFrame(None, title="My PopUp", size=(200,300), style=wx.DEFAULT_MINIFRAME_STYLE|wx.CLOSE_BOX)
alignToBottomRight(frame)
app.SetTopWindow(frame)
frame.Show()
app.MainLoop()