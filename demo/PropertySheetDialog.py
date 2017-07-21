#!/usr/bin/env python

import wx
import wx.adv

import images

#----------------------------------------------------------------------


class MyPropSheetDlg(wx.adv.PropertySheetDialog):
    def __init__(self, parent, bookType):
        wx.adv.PropertySheetDialog.__init__(self)

        # Setup
        sheetStyle = bookType | wx.adv.PROPSHEET_SHRINKTOFIT
        self.SetSheetStyle(sheetStyle)
        self.SetSheetInnerBorder(0)
        self.SetSheetOuterBorder(0)

        # Base class' Create() makes the book control, sizers, etc.
        self.Create(parent, title="Sample App Preferences")

        # Create the stock buttons
        self.CreateButtons(wx.OK|wx.CANCEL)

        # Add some pages
        notebook = self.GetBookCtrl()
        page0 = self.CreateInfoPage(notebook)
        page1 = self.CreateGeneralSettingsPage(notebook)
        page2 = self.CreateAestheticSettingsPage(notebook)

        if bookType & (wx.adv.PROPSHEET_BUTTONTOOLBOOK |
                       wx.adv.PROPSHEET_TOOLBOOK ):

            self.imageList = wx.ImageList(32,32)
            lb01 = self.imageList.Add(images.LB01.GetBitmap())
            lb02 = self.imageList.Add(images.LB02.GetBitmap())
            lb03 = self.imageList.Add(images.LB03.GetBitmap())
            notebook.SetImageList(self.imageList)
        else:
            lb01 = lb02 = lb03 = -1

        notebook.AddPage(page0, "Info", imageId=lb01)
        notebook.AddPage(page1, "General", imageId=lb02)
        notebook.AddPage(page2, "Aesthetics", imageId=lb03)

        # Do the layout
        self.LayoutDialog()


    # This and the following method just create some panels to display in the
    # bookctrl in the dialog.  The actual content of these panels don't
    # matter much so pay very little attention to them, the point is that any
    # kind of panels with controls can be used here and the PropertySheetDialog
    # takes care of the rest.
    def CreateGeneralSettingsPage(self, parent):
        panel = wx.Panel(parent)

        topSizer = wx.BoxSizer( wx.VERTICAL )
        item0 = wx.BoxSizer( wx.VERTICAL )

        itemSizer3 = wx.BoxSizer( wx.HORIZONTAL )
        checkBox3 = wx.CheckBox(panel, -1, "&Load last project on startup")
        itemSizer3.Add(checkBox3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        item0.Add(itemSizer3, 0, wx.EXPAND|wx.ALL, 0)

        autoSaveLabel = "&Auto-save every"
        minsLabel = "mins"

        itemSizer12 = wx.BoxSizer( wx.HORIZONTAL )
        checkBox12 = wx.CheckBox(panel, -1, autoSaveLabel)

        spinCtrl12 = wx.SpinCtrl(panel, -1, "", (-1,-1), (40, -1), wx.SP_ARROW_KEYS, 1, 60, 1)
        itemSizer12.Add(checkBox12, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        itemSizer12.Add(spinCtrl12, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        itemSizer12.Add(wx.StaticText(panel, -1, minsLabel), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        item0.Add(itemSizer12, 0, wx.EXPAND|wx.ALL, 0)

        itemSizer8 = wx.BoxSizer( wx.HORIZONTAL )
        checkBox6 = wx.CheckBox(panel, -1, "Show &tooltips")
        itemSizer8.Add(checkBox6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        item0.Add(itemSizer8, 0, wx.EXPAND|wx.ALL, 0)

        topSizer.Add( item0, 1, wx.EXPAND|wx.ALIGN_CENTRE|wx.ALL, 5 )

        panel.SetSizer(topSizer)
        return panel


    def CreateAestheticSettingsPage(self, parent):
        panel = wx.Panel(parent)

        topSizer = wx.BoxSizer( wx.VERTICAL )
        item0 = wx.BoxSizer( wx.VERTICAL )

        globalOrProjectChoices = [ "&New projects",
                                   "&This project",
                                   ]

        projectOrGlobal = wx.RadioBox(panel, -1, "&Apply settings to:",
                                      choices=globalOrProjectChoices,
                                      majorDimension=2)
        item0.Add(projectOrGlobal, 0, wx.EXPAND|wx.ALL, 5)
        projectOrGlobal.SetSelection(0)

        backgroundStyleChoices = [ "Colour",
                                   "Image",
                                   ]

        staticBox3 = wx.StaticBox(panel, -1, "Background style:")
        styleSizer = wx.StaticBoxSizer( staticBox3, wx.VERTICAL )
        item0.Add(styleSizer, 0, wx.EXPAND|wx.ALL, 5)

        itemSizer2 = wx.BoxSizer( wx.HORIZONTAL )
        choice2 = wx.Choice(panel, -1, choices=backgroundStyleChoices)

        itemSizer2.Add(wx.StaticText(panel, -1, "&Window:"), 0,
                       wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        itemSizer2.Add(5, 5, 1, wx.ALL, 0)
        itemSizer2.Add(choice2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        styleSizer.Add(itemSizer2, 0, wx.EXPAND|wx.ALL, 5)

        staticBox1 = wx.StaticBox(panel, -1, "Tile font size:")
        itemSizer5 = wx.StaticBoxSizer( staticBox1, wx.HORIZONTAL )

        spinCtrl = wx.SpinCtrl(panel, -1, "", size=(80, -1))
        itemSizer5.Add(spinCtrl, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)

        item0.Add(itemSizer5, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        topSizer.Add(item0, 1, wx.EXPAND|wx.ALIGN_CENTRE|wx.ALL, 5 )
        topSizer.AddSpacer(5)

        panel.SetSizer(topSizer)
        return panel


    def CreateInfoPage(self, parent):
        panel = wx.Panel(parent)
        statTxt = wx.StaticText(panel, -1, infoText)
        sizer = wx.BoxSizer()
        sizer.Add(statTxt, 1, wx.EXPAND|wx.ALL, 15)
        panel.SetSizer(sizer)
        return panel



#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        btn1 = wx.Button(self, -1, "Show PropertySheetDialog with Notebook")
        btn2 = wx.Button(self, -1, "Show PropertySheetDialog with Toolbook")
        btn3 = wx.Button(self, -1, "Show PropertySheetDialog with ButtonToolbook")
        btn4 = wx.Button(self, -1, "Show PropertySheetDialog with Listbook")

        self.Bind(wx.EVT_BUTTON, self.OnButton1, btn1)
        self.Bind(wx.EVT_BUTTON, self.OnButton2, btn2)
        self.Bind(wx.EVT_BUTTON, self.OnButton3, btn3)
        self.Bind(wx.EVT_BUTTON, self.OnButton4, btn4)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn1, 0, wx.ALL, 10)
        sizer.Add(btn2, 0, wx.ALL, 10)
        sizer.Add(btn3, 0, wx.ALL, 10)
        sizer.Add(btn4, 0, wx.ALL, 10)

        box = wx.BoxSizer()
        box.Add(sizer, 0, wx.ALL, 15)
        self.SetSizer(box)


    def ShowPropSheet(self, style):
        with MyPropSheetDlg(self, style) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.log.write('Dialog ended with OK button\n')
            else:
                self.log.write('Dialog cancelled\n')


    def OnButton1(self, evt):
        self.ShowPropSheet(wx.adv.PROPSHEET_NOTEBOOK)


    def OnButton2(self, evt):
        self.ShowPropSheet(wx.adv.PROPSHEET_TOOLBOOK)


    def OnButton3(self, evt):
        self.ShowPropSheet(wx.adv.PROPSHEET_BUTTONTOOLBOOK)


    def OnButton4(self, evt):
        self.ShowPropSheet(wx.adv.PROPSHEET_LISTBOOK)


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------

infoText = """\
A wx.adv.PropertySheetDialog provides a standard framework to show settings or
preferences for your applications.  You just need to provide panels for each
'page' to be shown in the dialog and the PropertySheetDialog takes care of
showing those panels in one of several kinds of book controls, adding buttons,
etc.
"""


overview = """<html><body>
<h2><center>PropertySheetDialog</center></h2>
{}
</body></html>
""".format(infoText)



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

