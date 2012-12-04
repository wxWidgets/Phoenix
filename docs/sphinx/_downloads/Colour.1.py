##Andrea Gavana
#!/usr/bin/env python

# This sample shows how to assign different fonts to various
# wx.StaticTexts

import wx

app = wx.App(0)
frame = wx.Frame(None, -1, 'Colour settings')

text_ctrl_1 = wx.TextCtrl(frame, -1, 'Some text')
text_ctrl_1.SetBackgroundColour(wx.Colour(0, 0, 255))
# OR
text_ctrl_2 = wx.TextCtrl(frame, -1, 'Other text')
text_ctrl_2.SetBackgroundColour('BLUE')
# OR
text_ctrl_3 = wx.TextCtrl(frame, -1, 'Another text')
text_ctrl_3.SetBackgroundColour('#0000FF')

# Size up everything in a nice vertical box sizer
sizer = wx.BoxSizer(wx.VERTICAL)
sizer.Add(text_ctrl_1, 0, wx.EXPAND|wx.ALL, 10)
sizer.Add(text_ctrl_2, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
sizer.Add(text_ctrl_3, 0, wx.EXPAND|wx.ALL, 10)
frame.SetSizer(sizer)
sizer.SetSizeHints(frame)

frame.Show()

# Enter the application main loop
app.MainLoop()
