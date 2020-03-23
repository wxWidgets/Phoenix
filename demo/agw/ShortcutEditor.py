#!/usr/bin/env python

import wx

import os
import sys
import string
import random

from images import catalog
import images

from wx.lib.embeddedimage import PyEmbeddedImage

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import shortcuteditor as SE
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.shortcuteditor as SE


SE_DIR = os.path.split(SE.__file__)[0]
HTML_HELP = os.path.join(SE_DIR, 'data', 'default_help_text.html')

TOP_MENUS = ['File', 'Edit', 'View', 'Options', 'Window', 'Help']

COMBINATIONS = string.ascii_uppercase + string.digits
COMBINATIONS = [c for c in COMBINATIONS] + list(SE.KEYMAP.values())

ACCEL_IDS = wx.NewIdRef(6)

_ = wx.GetTranslation


#----------------------------------------------------------------------
_accelerators = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAGXRFWHRTb2Z0d2FyZQBBZG9i"
    b"ZSBJbWFnZVJlYWR5ccllPAAAAUNJREFUeNqkkrFqg1AUho+idLKCEgSnvoBkUiwBoU4tGXyJ"
    b"Lpmy+QI+gUuzFbK5OhSKQzZBfIlACCEiplAHkQj2XFNDaYOJ6YHPH7n85z/ncqm6ruE/xZDP"
    b"eDzu66ORELmnrwy+Q9K2U9+6RZ6Rt+MKvw6nyCNy09HkHXk91cBGPpAn5PPiS/wuFnlATKS8"
    b"dB9qPp+/oE6uvMwZU1XVxDRNyLIMBEGA3W53VkmJogiLxWJC7/d7WK/XMBwOYbVanVVFURqI"
    b"h3gp13VrXdchTdNesw8GA4iiCOiyLIHneSiKAgzD6NTRaASqqgIJ3G63QLyU4zi1pmmQJEln"
    b"IsdxkOf58V+SJIjjGBjShZgtywLP8xolu/0slmXB9/3mrNUgCA4T2LbdTLDZbP6knJqgVVmW"
    b"DxNg2iwMw97vYLlcNu/gS4ABALx5qLfCRWM1AAAAAElFTkSuQmCC")


#----------------------------------------------------------------------
_edit = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABmJLR0QAAAAAAAD5Q7t/AAAA"
    b"CXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1QsOEh8bQbXRcgAAAhxJREFUKM91ks1rE1EU"
    b"xc99H5l8m2lolKRuqtamKohFChahYF0IfoBSF4IbwY1/gv+DK/cuXLgTxaWIXSjSjWKEFgm4"
    b"aGvaJo1NJpm0eTPvzXPRmrZgz+7C+d3DPVz6WvmVTMTwT9tKK2W9le8Ta08VTXei0fL9R8nC"
    b"iYFBJJPO2VPFwRyEkbLMazwrnvvJTM5frP3+MDz24PHAwGAtDohLZpt113nHNoH5he6nL+mx"
    b"8wcNDIdFAG++imMVLaCFbzT+vtrdanWOBEyny9sveQjssLUa712aq7e9xaXqkQC8ea4r6Mds"
    b"nTZKV07O3iu4KSJ7JGCXn8tMAn685WX98dtDI0UOwxj9HzAbCzxeRS+NjrOVnnBn5hJWZdOZ"
    b"Rr0BIAiCw4Ax0doLFmdQWb+dbo3ccIslwRhx8trtMAybzT+9Xk/shikLbFSEs0zaBZzGjjN8"
    b"92Hgt8NAdbyOUkprDaDb9cXu9igCTB9RCfGMv15r5qfjEVebTUYUGUNEAIhICM4G9euQuJw1"
    b"+nplyQ3PzGirTWSFFAQCkRAilzuWz+f3EiTHcn37x8fPpUSKrj5JjZZ1fxuwXLBkKiV4KKWU"
    b"Uu4dvVtyf0evV9fl5J38hSkE/ZiQrpstFI4LyYul0v7zEWcEcKA8OXX64mWeG9L9MMxlpBOL"
    b"jI3FOOeCs/0yxepK7c3rt1wwYhJEkQlguYWxFjayjJHndW/dvDYA/gKtTuQVCWY6EAAAAABJ"
    b"RU5ErkJgggo=")

#----------------------------------------------------------------------
_file = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAB3RJTUUH0AwNAR44FPFuJQAA"
    b"AAlwSFlzAAAK8AAACvABQqw0mAAAADBQTFRFAP8Af39/UFBQz8/P4ODg////8PDw///wn5+f"
    b"MDAwgICAAAAAAAAAAAAAAAAAAAAAZbZ2KAAAAAF0Uk5TAEDm2GYAAABRSURBVHjaY2BcBQQL"
    b"GBgYGEOBoAnECC8vL29XgDI0Z0IY6RZCYEZZmXMTRCTFxQjMSHeBMNLdoIySFCgDKABmhKVB"
    b"GS4uUIYxCIAYSmDAAAcA0SwdEWLFwocAAAAASUVORK5CYII=")

#----------------------------------------------------------------------
_help = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAC+ElEQVR4nGWTP2xbVRjFf9+9"
    b"9/01TgwJCQkMbkMKqCkEKGoXBpiQEqkpZUL8y8BeRqYwMMBQRMWMGtQgJCSKYWCohARIVCCo"
    b"MJUgLbSipVERTuzYcexn+713L4OlirafdLZzznC+c4TbbnZxrSTIEkoeQ9S8iICob0WkevHM"
    b"C5Xb+XKLeOH08WIxXnloZqoUhSFRFDHIcmr1XerNDts7navWuTfWPz1SucNgduH0qfm58mt7"
    b"y/ezfq1LrZmR2SHFaAg9QTtLo1WnnybLv3+yuHrTYHZh7a1DT8ysFEfH+eVyh73TEa8vTvL0"
    b"o0WsdXzz6w6nzm5x5cYALdDtNMgG3aO/ffxcRWYX18pTE6W/Dj7+CN9daDM17lN5+2GsteS5"
    b"w1qLc44b9ZSXTlxHRHDOkrRqTWvzPXp837GVw0/OHl7fyOiljt2eJQ4U9VbGiTM1HLBn0iP2"
    b"hR8v92n1QGmNaB3m6eCS8QNvSZmI7XYXRECED76skTshs6C18OyBGOccm7uOTjrMLNQRottH"
    b"zOhIoVxrpsM0BPqpo9vJEa15YMLnzWNjWGs590efRg/8yABQUJB0dclYB71BjnWwvZORI3i+"
    b"RnuKd16ZIA6EK/9mnPy6QxB7KDV8XDFw1BsGM0hzBMfmdooTwfgKZRQLB+9iZtJgrePD7xNS"
    b"ZQgChdIKgJGCRZRGdZJBpd1OsM4hSlB6iKl7DM45nHNc2nQEoSGIPMLYY2TEIwxAtKkaRH3R"
    b"au8uFcNRulZQaojKzwn7pn22EjC+xgs0fuhhfE15DP5cbyFKf6Qufvb8atJPqpHOMQKIIEo4"
    b"+lTMoRmfhTmfuWmD9jReqJm+10ORs/FPv3L+/QNVBeBwy4O01QzE3uz2hesp3QFs7MDfTYdR"
    b"cN+oUPIyzv3QqIrSy7dsYf+LX82jzOe5GS3rsEgcGeKCR6FouLvkMVYybDV6XNtIqoNMnvnp"
    b"3Qebd6xx7uWzJZQ6Ltp71XhBOS7EhJEhzS27SV4VbU6ef2//6v81/wH6bjI8fK9HXAAAAABJ"
    b"RU5ErkJggg==")

#----------------------------------------------------------------------
_options = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAA"
    b"CXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1QkaDBM5i2PCSAAAAfBJREFUOMulkktoE2EU"
    b"hb+Z+EyKTRQKgkqwzMaFtt1FrC40FGJm60JwIVSkqLUtElICFQNDQqBrQXRlQIriwomN0GJX"
    b"gtI2iUkXFYJVadOXhiBERDozbmaGMR3rwrP7ueece++5P/wnBOcjnVGigArI8Vgi9xdNNJ1R"
    b"bI7YUlT7r/YDqKaZq/j6tQHNbLQd6YxiNBp1I51RDPdaw6pFAcR0RolaZKur19vmZhwFePDw"
    b"PvFYQgZyACKgDt4cMp4+mzAA9fatETbX15A6Jer1r/das4ndGRUsMYBgFW8MDBqatiXoum7o"
    b"ukZhfk4ovC8CyDsFK7R0sBHpu0i5UmG59gUgGY8l7v7zjE68yr80SpUS3Sd7KJYLmBNMArqr"
    b"QTCSOgzUrPeVkE7XCYmjR47RbDZ5N/cWtzU8TvH4cJi+UCcdAS/ZmU2Ot39LLn1eOtd9qoeA"
    b"P8BKbfnyhfD5+emp11XAABCDkVQXUHs0JjNbXmS2vEjHQR8A5t5yLv8CSZI4e7rX+mR2HiJQ"
    b"HB8OM/WmxJamI+7zs1Fv2iOaI8vZJ4850O7nTKgXYMxpAMDuXR72+A7x88cvsvkFgHCrSS6v"
    b"Uv1Y/SNsEWBl4zv7fQHa9np4PvMBIPxpcnTaSTRNkmvrqwtA0r5CMJK6BEw4uNvEO+E3N+LV"
    b"9uq8VLwAAAAASUVORK5CYII=")

#----------------------------------------------------------------------
_view = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAB3RJTUUH2QMSDgcQHD2pKgAA"
    b"AAlwSFlzAAALEgAACxIB0t1+/AAAAARnQU1BAACxjwv8YQUAAACWUExURb7Dxvz8/ObXxs+0"
    b"mK6UZb6JXMGZf9rBpezn39PT07unkOq0iuvBotSdZ/7+/trZ2eng1uvr5O7u7v///ubMsNDe"
    b"7ae+23Og32aX3Y+z58va6vHx8fT09Nzm8Zm66nql4+Dg3/j4+LXN8IOs5vf39/v7+6fE7g8U"
    b"G8iUWdXGwMqldOvUtr/Jzunp6ayfnaSps5qhs9/NuBN0LcUAAAABdFJOUwBA5thmAAAAqUlE"
    b"QVR42o2PSxaCMBAEx4kQZIKGGAQEE8NXRUHufzkRL2Dt6vWmGuAfXIzzrLWW7ucKh2HgjAsh"
    b"gq+/cGDhOE3v0SfCdQ+fXWdMXlecKACp723Vmb6vbd0iPUDLpu1M3vc2tW0jb3BVpavy2to0"
    b"M65UDFAW5cUsmtmkLJAg1hio5JRm+bmIdcQADlygjNUCUuQfl5BdSLRECYo8tl9TN8i2nuf5"
    b"PPjr6Qc/LA45I8MgVQAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
_window = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAKnRFWHRDcmVhdGlvbiBUaW1l"
    b"AERpIDQgTXJ6IDIwMDMgMDA6MjQ6MDQgKzAxMDDdSQ6OAAAAB3RJTUUH0woGFAwIjuRPzgAA"
    b"AAlwSFlzAAAK8AAACvABQqw0mAAAAARnQU1BAACxjwv8YQUAAAEVSURBVHjaY2SY/tuDgYll"
    b"OwMp4OqOKIZJntuArM+MDDP//59pTLzeJQ8ZGA6/ATLSGT2A5AkWkGD6WSDx5g1xJvDwMDBw"
    b"cIBYlkB8C2zANdvrKGr+/mVg+P0bQv/5g8AgsT9/XjN4PdYEKRMEYjawAZqamigGgBT/+gXR"
    b"AKORMcNjsDJGEMFEUuBhAdQ34N8/VEwIsMD8jGwAiA8KQBgbn6FgA0ABhWwAsub//xF8nAaA"
    b"QxbNCzBXwFwAYoMMA2G8LoB5CaQQZggMwwzD6wJ0b6C7AoSh4D/EgGu7IqUZ3JaTFHcdFkuA"
    b"5HuQ40GpiR+ILRggaRuUPBkJaP8P1XwciE8wQtMCLxALAzErkW4AefotEH8GAEJMrcAWjkHy"
    b"AAAAAElFTkSuQmCC")

#----------------------------------------------------------------------

def GetValidMenuImages():

    valid_images = []
    counter = 0

    for key in catalog:
        bmp = catalog[key].GetBitmap()
        if bmp.GetWidth() == 16 and bmp.GetHeight() == 16:
            valid_images.append(bmp)

    return valid_images

#----------------------------------------------------------------------

class ShortcutEditorDemo(wx.Frame):

    def __init__(self, parent, log):

        wx.Frame.__init__(self, parent, -1, 'ShortcutEditor wxPython Demo :-D', size=(900, 800))

        self.log = log

        self.valid_images = GetValidMenuImages()
        self.used_shortcuts = []

        self.SetIcon(images.Mondrian.GetIcon())

        self.MakeMenuBar()
        self.MakeAcceleratorTable()

        dlg = SE.ShortcutEditor(self)
        dlg.FromMenuBar(self)
        dlg.FromAcceleratorTable(self.accelTable)

        self.AddTopMenuBitmaps(dlg)

        dlg.Bind(SE.EVT_SHORTCUT_CHANGING, self.OnShortcutChanging)
        dlg.Bind(SE.EVT_SHORTCUT_CHANGED, self.OnShortcutChanged)

        self.CenterOnScreen()
        self.Show()
        self.Raise()

        wx.CallAfter(self.ShowDialog, dlg)


    def MakeMenuBar(self):

        bar = wx.MenuBar()
        top_menus = []

        for title in TOP_MENUS:
            menu = wx.Menu()

            self.AppendMenus(menu, title)

            bar.Append(menu, title)
            top_menus.append(menu)

        self.SetMenuBar(bar)


    def MakeAcceleratorTable(self):

        table = []
        saved_table = []

        for i in range(6):
            name = 'Accelerator %d'%(i+1)
            choice = random.choice(list(SE.ACCELERATORS))

            if choice == wx.ACCEL_ALT:
                letter = random.choice(COMBINATIONS)

                if len(letter) > 1:
                    inv_keyMap = dict(zip(SE.KEYMAP.values(), SE.KEYMAP.keys()))
                    wxk = inv_keyMap[letter]
                else:
                    wxk = ord(letter)

            else:
                wxk = random.choice(list(SE.KEYMAP))

            accel = (choice, wxk, ACCEL_IDS[i])
            saved_accel = (name, choice, wxk, ACCEL_IDS[i])

            self.Bind(wx.EVT_MENU, self.OnAcceleratorShortcuts, id=ACCEL_IDS[i])

            table.append(accel)
            saved_table.append(saved_accel)

        self.accelTable = saved_table
        self.SetAcceleratorTable(wx.AcceleratorTable(table))


    def AppendMenus(self, top_menu, title, recursive=''):

        num_menus = random.randint(2, 7)

        for index in range(num_menus):
            shortcut = self.CreateShortcut()

            sub_menu = wx.MenuItem(top_menu, -1, '%s%sItem %d%s'%(recursive, title, index+1, shortcut),
                                   'Help for %s%sItem %d'%(recursive, title, index+1))

            if random.randint(0, 1) == 1:
                # Get a random image for the menu
                bmp = random.choice(self.valid_images)
                sub_menu.SetBitmap(bmp)

            self.Bind(wx.EVT_MENU, self.OnMenuShortcuts, id=sub_menu.GetId())

            if random.randint(0, 10) == 5 and not recursive:
                # Append a sub-sub-menu
                dummy_menu = wx.Menu()

                recursive = 'Sub-'
                self.AppendMenus(dummy_menu, title, recursive)
                dummy_item = top_menu.AppendSubMenu(dummy_menu, 'Sub ' + title)

                if random.randint(0, 1) == 1:
                    # Get a random image for the menu
                    bmp = random.choice(self.valid_images)
                    dummy_item.SetBitmap(bmp)

                recursive = ''

            top_menu.Append(sub_menu)

            if random.randint(0, 1) == 1 and index < num_menus - 1:
                # Append a separator
                top_menu.AppendSeparator()


    def CreateShortcut(self):

        rand = random.randint(0, 3)

        if rand == 0:
            # No shortcut
            return ''

        letter = random.choice(COMBINATIONS)
        shortcut = '\t%s+' + letter

        if rand == 1:
            # Ctrl + character
            modifier = 'Ctrl'

        elif rand == 2:
            # Shift + character
            modifier = 'Shift'

        else:
            # Ctrl + Shift + character
            modifier = 'Ctrl+Shift'

        shortcut = shortcut % modifier

        if shortcut in self.used_shortcuts:
            return self.CreateShortcut()

        self.used_shortcuts.append(shortcut)
        return shortcut


    def AddTopMenuBitmaps(self, dlg):

        manager = dlg.GetShortcutManager()

        for child in manager.children:
            name = child.label.lower()
            bitmap = eval('_%s'%name).GetBitmap()
            child.SetBitmap(bitmap)


    def ShowDialog(self, dlg):

        answer = dlg.ShowModal()

        if answer == wx.ID_CANCEL:
            dlg.Destroy()
            return

        dlg.ToMenuBar(self)
        dlg.ToAcceleratorTable(self)

        dlg.Destroy()


    def OnMenuShortcuts(self, event):

        itemId = event.GetId()
        menu = event.GetEventObject().GetMenuBar()
        menuItem = menu.FindItemById(itemId)

        label = menuItem.GetItemLabel()
        label, accel = label.split('\t')

        self.log.write('You have selected the shortcut for %s (%s)'%(label, accel))


    def OnAcceleratorShortcuts(self, event):

        itemId = event.GetId()

        for label, choice, accel, ids in self.accelTable:
            if ids == itemId:
                self.log.write('You have selected the accelerator for %s (%s)'%(label, accel))
                break


    def OnShortcutChanging(self, event):

        shortcut = event.GetShortcut()
        oldAccel = event.GetOldAccelerator()
        newAccel = event.GetAccelerator()

        self.log.write('Shortcut for "%s" changing from "%s" to "%s"'%(shortcut.label, oldAccel, newAccel))
        event.Skip()


    def OnShortcutChanged(self, event):

        shortcut = event.GetShortcut()
        newAccel = event.GetAccelerator()

        self.log.write('Shortcut for "%s" changed to "%s"'%(shortcut.label, newAccel))


#---------------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b1 = wx.Button(self, -1, " Run ShortcutEditor ", (50, 50))
        self.Bind(wx.EVT_BUTTON, self.OnButton1, b1)


    def OnButton1(self, event):
        self.win = ShortcutEditorDemo(self, self.log)

#----------------------------------------------------------------------

def runTest(frame, nb, log):

    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------

with open(HTML_HELP, 'rt') as fid:
    overview = fid.read()


if __name__ == '__main__':
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

