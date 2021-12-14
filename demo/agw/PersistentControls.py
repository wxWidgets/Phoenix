#!/usr/bin/env python

import wx
import wx.adv
import os
import sys
import images
import random

import wx.dataview as dv

from wx.lib.expando import ExpandoTextCtrl
import wx.lib.agw.aui as AUI
import wx.lib.agw.floatspin as FS

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    import agw.persist as PM
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.persist as PM

_sampleText1 = "wx.Frame with AUI perspective, wx.MenuBar, wx.ColourDialog, " \
               "wx.FindReplaceDialog, wx.FontDialog, wx.TextEntryDialog, " \
               "wx.ColourPickerCtrl, wx.DirPickerCtrl, wx.FilePickerCtrl, " \
               "AuiToolBar, wx.RadioBox, wx.ToggleButton, wx.ComboBox, " \
               "wx.Slider, wx.SpinCtrl, FloatSpin\n\n" \
               "PersistenceManager Style: PM.PM_DEFAULT_STYLE\n"

_sampleText2 = "wx.Frame, wx.SplitterWindow, wx.TreeCtrl, wx.Notebook, " \
               "wx.CheckListBox, wx.CheckBox, wx.SearchCtrl, wx.TextCtrl, " \
               "wx.DatePickerCtrl, wx.Choice, AuiNotebook, wx.ListCtrl, " \
               "TreeListCtrl, wx.HtmlListBox\n\nPersistenceManager Style: " \
               "PM.PM_SAVE_RESTORE_TREE_LIST_SELECTIONS\n"

_sampleList = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']
_sampleList2 = _sampleList + ['nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen']

_title = "PersistentControls for wxPython :-D "
_configFile1 = os.path.join(dirName, "Example1")
_configFile2 = os.path.join(dirName, "Example2")


ID_AuiToolBar = wx.ID_HIGHEST + 100


class PersistentPanel(wx.Panel):

    def __init__(self, parent, log):

        wx.Panel.__init__(self, parent)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.FlexGridSizer(3, 2, 10, 10)

        btn1 = wx.Button(self, -1, "Example 1")
        text1 = ExpandoTextCtrl(self, -1, _sampleText1, size=(300,-1), style=wx.TE_READONLY)

        btn2 = wx.Button(self, -1, "Example 2")
        text2 = ExpandoTextCtrl(self, -1, _sampleText2, size=(300,-1), style=wx.TE_READONLY)

        sizer.Add(btn1, 0, wx.ALIGN_CENTER)
        sizer.Add(text1, 1, wx.EXPAND)

        sizer.Add(btn2, 0, wx.ALIGN_CENTER)
        sizer.Add(text2, 1, wx.EXPAND)

        sizer.AddGrowableCol(1)
        mainSizer.Add(sizer, 1, wx.EXPAND|wx.ALL, 20)
        self.SetSizer(mainSizer)
        mainSizer.Layout()

        btn1.Bind(wx.EVT_BUTTON, self.OnExample1)
        btn2.Bind(wx.EVT_BUTTON, self.OnExample2)


    def OnExample1(self, event):

        frame = PersistentFrame1(self, _title + "- Example 1", (700, 500))


    def OnExample2(self, event):

        frame = PersistentFrame2(self, _title + "- Example 2", (700, 500))


class PersistentFrame1(wx.Frame):

    def __init__(self, parent, title, size):

        wx.Frame.__init__(self, parent, -1, title, size=size, name="Example1")

        self._auiMgr = AUI.AuiManager()
        self._auiMgr.SetManagedWindow(self)

        self._persistMgr = PM.PersistenceManager.Get()
        self._persistMgr.SetPersistenceFile(_configFile1)

        self.CreateMenuBar()
        self.CreateAuiToolBar()

        self.BuildPanes()

        self.SetIcon(images.Mondrian.Icon)
        self.CenterOnParent()
        self.Show()

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        wx.CallAfter(self.RegisterControls)


    def CreateMenuBar(self):

        # Prepare the menu bar
        menuBar = wx.MenuBar()
        menuBar.SetName("MenuBar1")

        # 1st menu from left
        menu1 = wx.Menu()
        menu1.Append(101, "wx.Colo&urDialog")
        menu1.Append(102, "wx.F&ontDialog")
        menu1.AppendSeparator()
        menu1.Append(103, "wx.&TextEntryDialog")
        menu1.AppendSeparator()
        menu1.Append(105, "&Close", "Close this frame")
        # Add menu to the menu bar
        menuBar.Append(menu1, "&Dialogs")

        menu2 = wx.Menu()
        # Radio items
        menu2.Append(201, "Radio 1-1", "", wx.ITEM_RADIO)
        menu2.Append(202, "Radio 1-2", "", wx.ITEM_RADIO)
        menu2.Append(203, "Radio 1-3", "", wx.ITEM_RADIO)
        menu2.AppendSeparator()
        menu2.Append(204, "Radio 2-1", "", wx.ITEM_RADIO)
        menu2.Append(205, "Radio 2-2", "", wx.ITEM_RADIO)
        menuBar.Append(menu2, "&Radio Items")

        menu3 = wx.Menu()
        # Check menu items
        menu3.Append(301, "Check 1", "", wx.ITEM_CHECK)
        menu3.Append(302, "Check 2", "", wx.ITEM_CHECK)
        menu3.Append(303, "Check 3", "", wx.ITEM_CHECK)
        menuBar.Append(menu3, "Chec&k Items")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU_RANGE, self.OnDialogs, id=101, id2=103)
        self.Bind(wx.EVT_MENU, self.CloseWindow, id=105)


    def CreateAuiToolBar(self):

        tb3 = AUI.AuiToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize, AUI.AUI_TB_DEFAULT_STYLE)
        tb3.SetName("AuiToolBar")
        tb3.SetToolBitmapSize(wx.Size(16, 16))

        tb3_bmp1 = wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16, 16))
        tb3.AddSimpleTool(ID_AuiToolBar, "Check 1", tb3_bmp1, "Check 1", AUI.ITEM_CHECK)
        tb3.AddSimpleTool(ID_AuiToolBar+1, "Check 2", tb3_bmp1, "Check 2", AUI.ITEM_CHECK)
        tb3.AddSimpleTool(ID_AuiToolBar+2, "Check 3", tb3_bmp1, "Check 3", AUI.ITEM_CHECK)
        tb3.AddSimpleTool(ID_AuiToolBar+3, "Check 4", tb3_bmp1, "Check 4", AUI.ITEM_CHECK)
        tb3.AddSeparator()
        tb3.AddSimpleTool(ID_AuiToolBar+4, "Radio 1", tb3_bmp1, "Radio 1", AUI.ITEM_RADIO)
        tb3.AddSimpleTool(ID_AuiToolBar+5, "Radio 2", tb3_bmp1, "Radio 2", AUI.ITEM_RADIO)
        tb3.AddSimpleTool(ID_AuiToolBar+6, "Radio 3", tb3_bmp1, "Radio 3", AUI.ITEM_RADIO)
        tb3.AddSeparator()
        tb3.AddSimpleTool(ID_AuiToolBar+7, "Radio 1 (Group 2)", tb3_bmp1, "Radio 1 (Group 2)", AUI.ITEM_RADIO)
        tb3.AddSimpleTool(ID_AuiToolBar+8, "Radio 2 (Group 2)", tb3_bmp1, "Radio 2 (Group 2)", AUI.ITEM_RADIO)
        tb3.AddSimpleTool(ID_AuiToolBar+9, "Radio 3 (Group 2)", tb3_bmp1, "Radio 3 (Group 2)", AUI.ITEM_RADIO)

        tb3.Realize()

        self._auiMgr.AddPane(tb3, AUI.AuiPaneInfo().Name("tb3").Caption("AuiToolbar").ToolbarPane().Top())


    def BuildPanes(self):

        pickerPanel = wx.Panel(self)

        box1 = wx.BoxSizer(wx.VERTICAL)
        fgs = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)

        fgs.Add(wx.StaticText(pickerPanel, -1, "wx.ColourPickerCtrl:"), 0, wx.ALIGN_CENTER_VERTICAL)
        cp1 = wx.ColourPickerCtrl(pickerPanel, name="ColourPicker1")
        fgs.Add(cp1, 0, wx.ALIGN_CENTER)
        fgs.Add(wx.StaticText(pickerPanel, -1, "        with label:"), 0, wx.ALIGN_CENTER_VERTICAL)
        cp3 = wx.ColourPickerCtrl(pickerPanel, style=wx.CLRP_SHOW_LABEL, name="ColourPicker2")
        fgs.Add(cp3, 0, wx.ALIGN_CENTER)

        fgs.Add(wx.StaticText(pickerPanel, -1, "wx.DirPickerCtrl:"), 0, wx.ALIGN_CENTER_VERTICAL)
        dp1 = wx.DirPickerCtrl(pickerPanel, name="DirPicker1")
        fgs.Add(dp1, 0, wx.ALIGN_CENTER)

        fgs.Add(wx.StaticText(pickerPanel, -1, "wx.FilePickerCtrl:"), 0, wx.ALIGN_CENTER_VERTICAL)
        fp1 = wx.FilePickerCtrl(pickerPanel, name="FilePicker1")
        fgs.Add(fp1, 0, wx.ALIGN_CENTER)

        fgs.Add(wx.StaticText(pickerPanel, -1, "wx.FontPickerCtrl:"), 0, wx.ALIGN_CENTER_VERTICAL)
        fnt1 = wx.FontPickerCtrl(pickerPanel, style=wx.FNTP_FONTDESC_AS_LABEL, name="FontPicker1")
        fgs.Add(fnt1, 0, wx.ALIGN_CENTER)

        box1.Add(fgs, 1, wx.EXPAND|wx.ALL, 5)
        pickerPanel.SetSizer(box1)
        box1.Layout()

        otherPanel = wx.Panel(self)
        box2 = wx.BoxSizer(wx.VERTICAL)

        radiobox = wx.RadioBox(otherPanel, -1, "RadioBox", choices=_sampleList, majorDimension=2,
                               style=wx.RA_SPECIFY_COLS, name="RadioBox1")
        toggle = wx.ToggleButton(otherPanel, -1, "ToggleButton", name="Toggle1")
        combo = wx.ComboBox(otherPanel, -1, choices=_sampleList, style=wx.CB_DROPDOWN|wx.CB_READONLY,
                            name="ComboBox1")

        boldFont = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "")

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        box2.Add((0, 0), 1)
        box2.Add(radiobox, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        box2.Add((20, 0))

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add((20, 20), 1)
        sizer_1.Add(toggle, 0, wx.ALL, 5)
        sizer_1.Add((0, 10))
        label_1 = wx.StaticText(otherPanel, -1, "ComboBox")
        label_1.SetFont(boldFont)
        sizer_1.Add(label_1, 0, wx.ALL, 5)
        sizer_1.Add(combo, 0, wx.LEFT|wx.RIGHT, 5)
        sizer_1.Add((20, 20), 1)
        box2.Add(sizer_1, 1, wx.EXPAND, 0)
        box2.Add((0, 0), 1, 1)

        otherPanel.SetSizer(box2)

        otherPanel2 = wx.Panel(self)
        box3 = wx.BoxSizer(wx.VERTICAL)

        gs1 = wx.FlexGridSizer(2, 3, 5, 10)

        slider = wx.Slider(otherPanel2, -1, 3, 0, 10, style=wx.SL_HORIZONTAL|wx.SL_LABELS,
                           name="Slider1")
        spinctrl = wx.SpinCtrl(otherPanel2, -1, "20", min=0, max=100, name="SpinCtrl1")
        floatspin = FS.FloatSpin(otherPanel2, -1, value=150, min_val=20, max_val=200, name="FloatSpin1")
        floatspin.SetDigits(2)

        label_2 = wx.StaticText(otherPanel2, -1, "Slider")
        label_2.SetFont(boldFont)
        gs1.Add(label_2, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        label_3 = wx.StaticText(otherPanel2, -1, "SpinCtrl")
        label_3.SetFont(boldFont)
        gs1.Add(label_3, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        label_4 = wx.StaticText(otherPanel2, -1, "FloatSpin")
        label_4.SetFont(boldFont)
        gs1.Add(label_4, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        gs1.Add(slider, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        gs1.Add(spinctrl, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        gs1.Add(floatspin, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        gs1.AddGrowableCol(0)
        gs1.AddGrowableCol(1)
        gs1.AddGrowableCol(2)
        box3.Add(gs1, 1, wx.EXPAND|wx.ALL, 5)
        otherPanel2.SetSizer(box3)

        self._auiMgr.AddPane(pickerPanel, AUI.AuiPaneInfo().Name("DummyPanel1").Caption("Pickers").
                             Left().MinSize(wx.Size(300, -1)).FloatingSize(wx.Size(300, 300)))
        self._auiMgr.AddPane(otherPanel, AUI.AuiPaneInfo().Name("DummyPanel2").CenterPane())
        self._auiMgr.AddPane(otherPanel2, AUI.AuiPaneInfo().Name("DummyPanel3").Bottom().
                             BestSize(wx.Size(-1, 200)).Caption("Slider & Spins").
                             FloatingSize(wx.Size(300, 300)))
        self._auiMgr.Update()


    def RegisterControls(self):

        self.Freeze()
        self.Register()
        self.Thaw()


    def Register(self, children=None):

        if children is None:
            self._persistMgr.RegisterAndRestore(self)
            self._persistMgr.RegisterAndRestore(self.GetMenuBar())
            children = self.GetChildren()

        for child in children:

            name = child.GetName()

            if name not in PM.BAD_DEFAULT_NAMES and "widget" not in name and \
               "wxSpinButton" not in name and "auiFloating" not in name and \
               "AuiTabCtrl" not in name and "AuiNotebook" not in name:
                self._persistMgr.RegisterAndRestore(child)

            if child.GetChildren():
                self.Register(child.GetChildren())


    def CloseWindow(self, event):

        self.Close()


    def OnClose(self, event):

        self._persistMgr.SaveAndUnregister()
        event.Skip()


    def OnDialogs(self, event):

        evId = event.GetId()

        if evId == 101:
            # wx.ColourDialog
            data = wx.ColourData()
            dlg = wx.ColourDialog(self, data)
            dlg.SetName("ColourDialog1")

        elif evId == 102:
            # wx.FontDialog
            data = wx.FontData()
            dlg = wx.FontDialog(self, data)
            dlg.SetName("FontDialog1")

        elif evId == 103:
            # wx.TextEntryDialog
            dlg = wx.TextEntryDialog(self, 'What is your favorite programming language?',
                                     'Eh??', 'Python')
            dlg.SetValue("Python is the best!")
            dlg.SetName("TextEntryDialog1")

        self._persistMgr.RegisterAndRestore(dlg)

        if dlg.ShowModal() == wx.ID_OK:
            self._persistMgr.Save(dlg)

        self._persistMgr.Unregister(dlg)
        dlg.Destroy()


# The wx.HtmlListBox derives from wx.VListBox, but draws each item
# itself as a wx.HtmlCell.
class MyHtmlListBox(wx.html.HtmlListBox):

    def OnGetItem(self, n):
        if n % 2 == 0:
            return "This is item# <b>%d</b>" % n
        else:
            return "This is item# <b>%d</b> <br>Any <font color='RED'>HTML</font> is okay." % n


class PersistentFrame2(wx.Frame):

    def __init__(self, parent, title, size):

        wx.Frame.__init__(self, parent, -1, title, size=size, name="Example2")

        self._persistMgr = PM.PersistenceManager.Get()
        self._persistMgr.SetManagerStyle(PM.PM_DEFAULT_STYLE|PM.PM_SAVE_RESTORE_TREE_LIST_SELECTIONS)
        self._persistMgr.SetPersistenceFile(_configFile2)

        self.split1 = wx.SplitterWindow(self, -1, style=wx.SP_3D|wx.SP_BORDER, name="Splitter1")
        self.treectrl = self.CreateTreeListCtrl(False)

        self.split2 = wx.SplitterWindow(self.split1, -1, style=wx.SP_3D|wx.SP_BORDER, name="Splitter2")
        self.notebook = wx.Notebook(self.split2, name="Notebook1")
        dummyPanel = wx.Panel(self.split2)

        text = "Hello world!\nI am a simple wx.TextCtrl" \
               "I will remember my value if you change it!"

        self.checklistbox = wx.CheckListBox(dummyPanel, -1, choices=_sampleList2, name="CheckListBox1")
        self.textctrl = wx.TextCtrl(dummyPanel, -1, text, style=wx.TE_MULTILINE, name="TextCtrl1")
        self.searchctrl = wx.SearchCtrl(dummyPanel, -1, "", name="SearchCtrl1")
        self.checkbox = wx.CheckBox(dummyPanel, -1, "CheckBox", name="CheckBox1")
        self.datepickerctrl = wx.adv.DatePickerCtrl(dummyPanel, style=wx.adv.DP_DROPDOWN, name="DatePicker1")
        self.choice = wx.Choice(dummyPanel, -1, choices=_sampleList, name="Choice1")

        self.split2.SplitHorizontally(self.notebook, dummyPanel)
        self.split1.SplitVertically(self.treectrl, self.split2)

        self.DoLayout(dummyPanel)
        self.SetIcon(images.Mondrian.Icon)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        wx.CallAfter(self.RegisterControls)

        self.CenterOnParent()
        self.Show()


    def DoLayout(self, dummyPanel):

        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)

        self.notebook.AddPage(self.CreateNotebook(), "AuiNotebook")
        self.notebook.AddPage(self.CreateListCtrl(), "wx.ListCtrl")
        self.notebook.AddPage(self.CreateTreeListCtrl(True), "TreeListCtrl")
        self.notebook.AddPage(self.CreateHtmlListBox(), "wx.HtmlListBox")

        sizer_5.Add(self.checklistbox, 1, wx.EXPAND|wx.ALL, 5)
        sizer_6.Add(self.textctrl, 1, wx.EXPAND|wx.BOTTOM, 10)
        sizer_6.Add(self.searchctrl, 0, wx.BOTTOM, 10)
        sizer_6.Add(self.checkbox, 0, wx.BOTTOM, 10)
        sizer_6.Add(self.datepickerctrl, 0, wx.BOTTOM, 10)
        sizer_6.Add(self.choice, 0, 0, 0)
        sizer_5.Add(sizer_6, 1, wx.ALL|wx.EXPAND, 5)

        dummyPanel.SetSizer(sizer_5)
        self.Layout()


    def CreateNotebook(self):

        # create the notebook off-window to avoid flicker
        ctrl = AUI.AuiNotebook(self.notebook, -1)
        ctrl.SetName("AuiNotebook1")
        page_bmp = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16))
        ctrl.AddPage(wx.Panel(ctrl), "Page 1", False, page_bmp)
        ctrl.AddPage(wx.TextCtrl(ctrl, -1, "Some text", wx.DefaultPosition, wx.DefaultSize,
                                 wx.TE_MULTILINE|wx.NO_BORDER), "Page 1", False, page_bmp)

        ctrl.AddPage(wx.TextCtrl(ctrl, -1, "Some more text", wx.DefaultPosition, wx.DefaultSize,
                                 wx.TE_MULTILINE|wx.NO_BORDER), "Page 2")

        ctrl.AddPage(wx.TextCtrl(ctrl, -1, "Some more text", wx.DefaultPosition, wx.DefaultSize,
                                 wx.TE_MULTILINE|wx.NO_BORDER), "Page 3")

        ctrl.AddPage(wx.TextCtrl(ctrl, -1, "Some more text", wx.DefaultPosition, wx.DefaultSize,
                                 wx.TE_MULTILINE|wx.NO_BORDER), "Page 4")

        return ctrl


    def CreateListCtrl(self):

        il = wx.ImageList(16, 16)
        il.Add(images.Smiles.GetBitmap())

        listCtrl = wx.ListCtrl(self.notebook, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER, name="ListCtrl1")
        for col in range(6):
            listCtrl.InsertColumn(col, "Column %d"%col)

        listCtrl.AssignImageList(il, wx.IMAGE_LIST_SMALL)
        text = "Row: %d, Col: %d"
        for row in range(30):
            if random.randint(0, 1):
                idx = listCtrl.InsertItem(sys.maxsize, text%(row+1, 1), 0)
            else:
                idx = listCtrl.InsertItem(sys.maxsize, text%(row+1, 1))

            for col in range(1, 6):
                listCtrl.SetItem(idx, col, text%(row+1, col+1), random.randint(0, 1)-1)

        return listCtrl


    def CreateTreeListCtrl(self, isTreeList):

        if isTreeList:
            treeList = dv.TreeListCtrl(self.notebook, style=wx.TR_DEFAULT_STYLE|wx.TR_FULL_ROW_HIGHLIGHT|
                                              wx.SUNKEN_BORDER|wx.TR_MULTIPLE, name="TreeList1")
        else:
            treeList = wx.TreeCtrl(self.split1, style=wx.TR_DEFAULT_STYLE|wx.SUNKEN_BORDER|wx.TR_MULTIPLE,
                                   name="TreeCtrl1")

        il = wx.ImageList(16, 16)
        fldridx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16, 16)))
        smileidx = il.Add(images.Smiles.GetBitmap())

        treeList.AssignImageList(il)

        if isTreeList:
            # create some columns
            treeList.AppendColumn("Main column")
            treeList.AppendColumn("Column 1")
            treeList.AppendColumn("Column 2")
            ##treeList.SetMainColumn(0) # the one with the tree in it...
            treeList.SetColumnWidth(0, 175)

        if isTreeList:
            root = treeList.InsertItem(treeList.GetRootItem(), dv.TLI_FIRST, "The Root Item")
        else:
            root = treeList.AddRoot("The Root Item")

        if isTreeList:
            treeList.SetItemText(root, 1, "col 1 root")
            treeList.SetItemText(root, 2, "col 2 root")

        treeList.SetItemImage(root, fldridx)

        for x in range(15):
            txt = "Item %d" % x
            child = treeList.AppendItem(root, txt)
            treeList.SetItemImage(child, smileidx)
            if isTreeList:
                treeList.SetItemText(child, 1, txt + "(c1)")
                treeList.SetItemText(child, 2, txt + "(c2)")

            for y in range(5):
                txt = "item %d-%s" % (x, chr(ord("a")+y))
                last = treeList.AppendItem(child, txt)
                treeList.SetItemImage(last, fldridx)
                if isTreeList:
                    treeList.SetItemText(last, 1, txt + "(c1)")
                    treeList.SetItemText(last, 2, txt + "(c2)")

                for z in range(5):
                    txt = "item %d-%s-%d" % (x, chr(ord("a")+y), z)
                    item = treeList.AppendItem(last,  txt)
                    treeList.SetItemImage(item, smileidx)
                    if isTreeList:
                        treeList.SetItemText(item, 1, txt + "(c1)")
                        treeList.SetItemText(item, 2, txt + "(c2)")

        treeList.Expand(root)
        return treeList


    def CreateHtmlListBox(self):

        hlb = MyHtmlListBox(self.notebook, -1, style=wx.BORDER_SUNKEN|wx.LB_MULTIPLE, name="HtmlListBox1")
        hlb.SetItemCount(300)
        hlb.SetSelection(0)

        return hlb


    def OnClose(self, event):

        self._persistMgr.SaveAndUnregister()
        event.Skip()


    def RegisterControls(self):

        self.Freeze()
        self.Register()
        self.Thaw()


    def Register(self, children=None):

        if children is None:
            self._persistMgr.RegisterAndRestore(self)
            children = self.GetChildren()

        for child in children:

            name = child.GetName()

            if name not in PM.BAD_DEFAULT_NAMES and "wxtreelist" not in name and \
               "AuiTabCtrl" not in name:
                self._persistMgr.RegisterAndRestore(child)

            if child.GetChildren():
                self.Register(child.GetChildren())


#----------------------------------------------------------------------

def runTest(frame, nb, log):

    win = PersistentPanel(nb, log)
    return win

#----------------------------------------------------------------------

overview = PM.__doc__

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
