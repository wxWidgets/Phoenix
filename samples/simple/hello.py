import sys, os
import wxPhoenix as wx

#print 'PID:', os.getpid(); raw_input('Ready to start, press enter...')
 
app = wx.App()
frm = wx.Frame(None, title="Hello World!")
frm.Show()
app.MainLoop()

    
