#!/usr/bin/env python

import wx
import os, sys
import random
import images

from wx.lib.embeddedimage import PyEmbeddedImage

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import ultimatelistctrl as ULC
except ImportError: # if it's not there locally, try the wxPython lib.
    from wx.lib.agw import ultimatelistctrl as ULC


catalog = {}
index = []

smicon01 = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAB3RJTUUH1AgHFicMIwSmbQAA"
    b"AAlwSFlzAAALEwAACxMBAJqcGAAAAARnQU1BAACxjwv8YQUAAACZSURBVHjapZMBDsAQDEVX"
    b"cTA3w816MyPSaqXG4ie1Neb5rQFEfG7k2xBCKNZkhcMO4OillKLiC2wCLDXQDuJlAgC8sOe5"
    b"jqlCUEEQA5emHEj74xlV9NIG0M0OZKxLiwwxHUgnEjzyzE7MHgwlVQ7tLkG/HFjluZOPZrCE"
    b"+34s9h9HjbIaShD/HEjuOGsLoI4v529vo7taXfUCVHt4TiSsPYMAAAAASUVORK5CYII=")
index.append('smicon01')
catalog['smicon01'] = smicon01

#----------------------------------------------------------------------
smicon02 = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAB3RJTUUH1AgHFiYzjHm6EQAA"
    b"AAlwSFlzAAAewgAAHsIBbtB1PgAAAARnQU1BAACxjwv8YQUAAABjSURBVHja7ZPRCsAgCEV3"
    b"Y///y2ZjgrSrxXztQtSDHg9REJGrktsOAFKSDkIKeItos8KfAQzSWLHfPZxZfgBmMds4sKQA"
    b"ZjBgtn4bRFkaRHeybbAyOgbTU46mZEH1N7ZSt6YD1C9PHbDZOYgAAAAASUVORK5CYII=")
index.append('smicon02')
catalog['smicon02'] = smicon02

#----------------------------------------------------------------------
smicon03 = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAB3RJTUUH1AgHFiYeyabmZAAA"
    b"AAlwSFlzAAALEwAACxMBAJqcGAAAAARnQU1BAACxjwv8YQUAAABcSURBVHja7ZNLCgAgCEQb"
    b"6f5XtjaBmZ/IbQOhSI3PQDBzq6ivBEDoNBvBqtN2yTlRA9IFqCgITJPDgFUUI5okVwR6nCcC"
    b"TymB9yfXBBnRJxC7EHWJhOo2Uun11ADQZCkbCzp5EwAAAABJRU5ErkJggg==")
index.append('smicon03')
catalog['smicon03'] = smicon03

#----------------------------------------------------------------------
smicon04 = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAB3RJTUUH1AgHFiYK03wyGQAA"
    b"AAlwSFlzAAAewgAAHsIBbtB1PgAAAARnQU1BAACxjwv8YQUAAACISURBVHja5VNtDoAgCIXm"
    b"vepm4M3wZCQ2Kvua2c/exhAdj/ecoqrCF4R9EWM8sRERPjKYAgtmLksRqfKyr3AXwScTMaQk"
    b"MI5TlYmmfA6XPou6bfo7WI8ZGGpOzFNTU67uwBUc/T9lV3Cw0Nbsl3si+KkCtOrqCbcgkwD6"
    b"Z0LELpKVoBfDp+6MGUT4tQ7B0XvcAAAAAElFTkSuQmCC")
index.append('smicon04')
catalog['smicon04'] = smicon04

#----------------------------------------------------------------------
smicon05 = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAB3RJTUUH1AgHFiUuxFKFCwAA"
    b"AAlwSFlzAAALEwAACxMBAJqcGAAAAARnQU1BAACxjwv8YQUAAACQSURBVHja5VPhCsYgCPRG"
    b"77W9mfVm9mR+OhZMaiPWz0+II+nOSxSqSiuR7pdSSqfGzHhVcAd+cs7uRUUk4Jm/3oxOapU5"
    b"Z6oitB9HQDYsJjQq7u7SzQrtD8gDshUlALqFLEC11ikMPbj+2f3/DZ3j9CAwS27N7QT+1AGc"
    b"NhrhmTARQlsmH4ovIljdxm2JbfED/cdja9DB0AMAAAAASUVORK5CYII=")
index.append('smicon05')
catalog['smicon05'] = smicon05

#----------------------------------------------------------------------
smicon06 = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAB3RJTUUH1AgHFiUHhuAdZwAA"
    b"AAlwSFlzAAAuIgAALiIBquLdkgAAAARnQU1BAACxjwv8YQUAAABxSURBVHjatVMBDoAgCJTG"
    b"/79M4KoRIiEuNnXj5DhPbW0zgAcVap5AmYhyHAAw5DACdcyaHLseYKGGQoLID4vJsX0FH35c"
    b"bG8FbmcvZ8jxljIQ8eoJ6bgChEBvW31Uf14jy6SsBxFJTUHyb/QetnTVgxOMpSQrnCCj/wAA"
    b"AABJRU5ErkJggg==")
index.append('smicon06')
catalog['smicon06'] = smicon06


class TestFrame(wx.Frame):
    def __init__(self, parent, log):
        wx.Frame.__init__(self, parent, -1,
                          "UltimateListCtrl in wx.LC_LIST mode",
                          size=(600, 400))

        # load some images into an image list
        il = wx.ImageList(16, 16, True)
        imgs = sorted(catalog)

        for img in imgs:
            bmp = catalog[img].GetBitmap()
            il_max = il.Add(bmp)

        # create the list control
        self.list = ULC.UltimateListCtrl(self, -1, agwStyle=wx.LC_LIST|ULC.ULC_HOT_TRACKING)
        self.list.EnableSelectionVista()

        # assign the image list to it
        self.list.AssignImageList(il, wx.IMAGE_LIST_SMALL)

        # create some items for the list
        for x in range(25):
            img = x % (il_max+1)
            it_kind = 0
            if random.randint(0, 2) == 2:
                it_kind = random.randint(1, 2)

            self.list.InsertImageStringItem(x, "This is item %02d" % x, img, it_kind=it_kind)

        self.SetIcon(images.Mondrian.GetIcon())
        self.Show()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    app = wx.App(0)
    frame = TestFrame(None, sys.stdout)
    frame.Show(True)
    app.MainLoop()
