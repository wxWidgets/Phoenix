##Andrea Gavana
#!/usr/bin/env python

# This sample shows how to assign different fonts to various
# wx.StaticTexts

import wx

class FontFrame(wx.Frame):

   def __init__(self, parent):

        wx.Frame.__init__(self, parent, title='Font sample')

        panel = wx.Panel(self, -1)

        text1 = '''Lasciatemi cantare
con la chitarra in mano
lasciatemi cantare
sono un italiano'''

        text2 = '''Buongiorno Italia gli spaghetti al dente
e un partigiano come Presidente
con l'autoradio sempre nella mano destra
e un canarino sopra la finestra'''

        text3 = '''Buongiorno Italia con i tuoi artisti
con troppa America sui manifesti
con le canzoni con amore con il cuore
con piu' donne sempre meno suore'''

        # Construct 2 font objects from the wx.Font constructor
        font1 = wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL)
        font2 = wx.Font(10, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        # A font can be retrieved from the OS default font
        # and modified
        font3 = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font3.SetStyle(wx.FONTSTYLE_ITALIC)
        font3.SetPointSize(12)

        lyrics1 = wx.StaticText(panel, -1, text1, style=wx.ALIGN_CENTRE)
        lyrics1.SetFont(font1)
        lyrics2 = wx.TextCtrl(panel, -1, text2, style=wx.TE_CENTER|wx.TE_MULTILINE)
        lyrics2.SetFont(font2)
        lyrics3 = wx.StaticText(panel, -1, text3, style=wx.ALIGN_CENTRE)
        lyrics3.SetFont(font3)

        # Size up everything in a nice vertical box sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(lyrics1, 0, wx.EXPAND|wx.ALL, 10)
        sizer.Add(lyrics2, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        sizer.Add(lyrics3, 0, wx.EXPAND|wx.ALL, 10)
        panel.SetSizer(sizer)
        sizer.SetSizeHints(panel)
        self.Center()


app = wx.App(0)
frame = FontFrame(None)
frame.Show()
# Enter the application main loop
app.MainLoop()
