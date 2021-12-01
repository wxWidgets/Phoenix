#!/usr/bin/env python

import sys
import os
import wx
import random
import math
import images

import wx.lib.mixins.listctrl as listmix

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

#---------------------------------------------------------------------------

catalog = {}
index = []

folder = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABGdBTUEAANkE3LLaAgAABI5J"
    b"REFUeJztls+LHEUUxz+vqntmYgL+RCFoEPyFR6/r1Vs8ehRviwTBq4f8B+rBePCg+QM0gig5"
    b"qFFERFdFQSNiiCRqyK5r1nVNsjuZ6ep673nontmJ6Uk25iLig0dR1d31/bxvdVU3/EciALv/"
    b"yYPSNXjw4MHF/fv3v3pDSDOxsLDQqdMZbz5323vublVV+Xg89pSS55z9RmJpacn7/f69XXrF"
    b"FQOR+1NKsry8jLsTQiCEQIzxigwxEttrYaYV6Sz4Cq3OQTeX7996mrKMqBnuDg7mBg7guF/+"
    b"jAiEIDz4+Cv0ej2KopgHcW0ANWffY4e44/Y9WK6ZvibT+bYn9pl+nTO/fHmYvY88xWAwoCzL"
    b"HUF02uKAjzfZ2tgAd1wVN8VdcbWmNWfqhgi4M/r1BKOHK4qimC7JtSA6AQRwzbgmMMfdGogJ"
    b"gCluTWuquDuj9d8Y/r5CykrOeSoeY7x+AABM8VQ1jljjAGbQthMITMEh0PRTXaOqmBmq+g8B"
    b"TBmdOwNEXHMrbFMQNwM3UJ0CoAncUdUpwKz9VVV1SoXOUTfWv3qXvLmBWG4m1wo0IZoQrSBX"
    b"0zG0ImgCHFObVm+TXXSV6AQQN9Jvpzh//MOmiroRFB3PgFQNTK6QnBBLiBtqDcAsBECv1+t8"
    b"G7sdsExZCsPvjlGtnCBE2qpTI5arFmA7g7UOzAAAxBhZXV09lVIaXR9AcEpPXPz8DfTCOQJO"
    b"mAhaRcip6VtTfbCEW7P+ua3czDh8+PDygQMHXgT+2DmAZwpqBrt6hOEawy9ex4frBHFExwRN"
    b"iDVLEDQR8pgoxu7BXVwaDkkpUZYlR48eXVlcXHx2bW3tCLBTBxyxTEGmF2kgNleovj6Cnz9L"
    b"jEJoKw5WNaljAs5d9zwAP7zA5vmLpJQ4ffr0D8AHwJ+dhc5zQDxTkumX0kAMehSjdfT42/jy"
    b"N0RPRIxozTIESwSUfp15aN+jDD9/hosXLmJmNTCeJw7zTkJTSqnxguYFFKAowWv850/x9VOE"
    b"Ox+EPXcgIjgZ8Qyu+OpP3Kp7GW4NyTkHIAJ5xwC7b7k7Bq8pJOOlNHdImwTwAONzcGYNBrcS"
    b"9tyJD26B2AcCEgW9NGY0HKJmMs/luQBBfJDWz3BTkWHwdwDaL1UBBtR/wsYGYhEJfQh9XARJ"
    b"GbXmVGTOX9dcgNGFFRVqKHMjFtsaLgOgASgjKFBDyGMkjcEyQXehZqhd/RTsBGiQK7yoIUgD"
    b"MGvkBEBbCG0h64AEiDkilTdfSdMbAChzozxxoAtgkmE7RUDaE5FrrP8cAIdg0PNtByZLIGzb"
    b"P6k+zwAISBBCKeScOXt2ecjkx+m6HIjgPSAIUgoSZRtiFiC3WQARDENdqerMyy8d+vH9j44d"
    b"ae+8LgDbXP2WrbXjF+pYIP1eiP1BDGURRKKIBMEEUQFFrDK3UbY8rDRtVRqHl/LyuX7xyccn"
    b"D9V1/VHr084BPjtZLY7rd57fVdx8XyyMEJ1YjoIEIwR3EXd3TFoXXHEy1u4GCfTK/a9tPQEc"
    b"u5rwJObt0b1LS0tPdl1YWFj4YAfzfrMT8f/jXxF/AROfMsX0/mQPAAAAAElFTkSuQmCC")
index.append('folder')
catalog['folder'] = folder

#----------------------------------------------------------------------
movie = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1B"
    b"AACxjwv8YQUAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAA"
    b"ABh0RVh0U29mdHdhcmUAUGFpbnQuTkVUIHYzLjM2qefiJQAACIZJREFUWEetV2lMXNcVxkkt"
    b"V/HSJk6dxO6iFrWhqiJVrVSpUvujf6K2SX90caVaUZpfURupUqv+qJQ2ctrihTiJMeDBxoSt"
    b"gAGz7zsMszIzDDDDMAuzD8zA8GZlGTAwX8+5eCxFnaGW2jecucy775773fOd7R3Le3TZF+0F"
    b"zz73eevpM2fy9g/28vJwLC+P/v7jAk3RR1yZAchLp9N5u7u7+/GtZIV/7/jlV7/5VSnL6ty3"
    b"tFptgdfrRcDnh81mh81updEKq/VQFhcXhVgsFiELCwtCzGYz5ufnodfrYaHfPr83sLBoe7fR"
    b"KT2bbbdjM3yyLNeUQlXgcrnhdrtI6QIcjiUSB+x2+2Ox2WwEyvYYVAaYyWSCTjeNyQk5lhz2"
    b"tN/vjxoXzP/ssPkuXHZuPN7wKT2Ok5zICkClUhV4PB5MyRXo6+uFy+WC0+kUsrS09FiygWLL"
    b"GGYMGBkZoXEGkUgUHq9nzWhe/KDT5v1iZsPPGPAUydNZAeg02gKf14NEPI5gMMgKwIDcbrbK"
    b"oWUYVDZgbCWmYWxsDEqlAhsbG1hfD6fdbk/YaLJcrXKtZ6XjU0DUarWwAJ+YuSUzEp8++HwB"
    b"+H1eeFk8vkegCJyLrEOUMSC2kHXRiinFFJQqJXZ2U9hIbkCSorTGm5gxm651Wr0XjnRKjUYj"
    b"nJBGjI6OYnl5GcuBAAI0BgJ++APLBIoBMRg/vF4f3GQlL4F2kXWYGrVGDe20Dnv7e0ildghE"
    b"kkBE0m6nK2A0Lfy1xBU9nRNEBsD29jZisZigYYUkuEIjCQMik0KlM6OhS4GypgkU35+ArHkc"
    b"HUMa6GYOI6GtvRW3b8tw5eoV3LxZjPb2dpCTpt0uV9Bstf1hxO47mxUEA2AK2Mvn5uawuroq"
    b"JBQKIRQMYc5kRVG9BpfKLXi9Poafdu3gJ70P8bOuFH5Rt4q3y42QNY5iaHgIzc0tuFdRiTt3"
    b"7uBeZSUaGuoxODREIJyBeaPxYk4ATAGfYmpqCuFwGOH1dRrXiWM33ipW4WsfruL58iTO3d/B"
    b"+bYdvERyviOFF2pT+N4nEr5T5ERhRS9URKNGrYRiSoHx8TG0tbXhX/X1TFWaou2PWQFknHBv"
    b"bw9bW1sUShFIkTDxv4I/l0/h6cIoTsliyG8I4Y36acg6RlDfN4LCxgFcvG+Bb2MPdw1b+NJ7"
    b"NtxrV1MUeeH2eMmpXSDzC0pZ5FOTfzoSACcVg8GAaDRKEsGE2oSX/+HEMyVRnLsTxNUuLRxO"
    b"L4WZJKwzorLiYvUSCmd2UTa3jePX1/DjawpyUD9CqyGxqWnBjJHhYWFVpUqRHUDGCTnNGo1G"
    b"AWBtTcLlBh1OFYXwudII3qqdQYAcMkZzUkTCgMaJS3VefL06jNcrNHj5YwtOlsZw6m9WjKuN"
    b"kAjkOtHIeUKhUAidaq02NwB2wocPHwoK+OFAIIhLsll89sYaLtwKonp0gTaPIR6LQ25045e1"
    b"PuTXELAGI/QmC35XqcXJsgSOX5NQ0yVHhCzIkognsJ3i6IpDpdYcTQGbn/xBAPARgJ/fNuHk"
    b"TQn5twLo0doRT8RpLob3W+fwrQdxXKzTY4Eo4Qz692Y9nilex4mPEyh/ICegCcToPqfq/oF+"
    b"RClFk+7cADgKOO1yKMZp4TKF36WKeZwsJv4/9KNimADQaRKUYPTziyjvU8Dh9iGR2CRKovjt"
    b"XQNREMaJjyJoGlDTcwkk6dkAJbQ5StWcX4jqowFQTQcno0QiwVkM7zXN4LlSCWdvEh13zVgN"
    b"SyLNcpZjIDwmN5LQzHvwykd28pV1PH/VAc2sWdznusCUplIpAeBIC7APsPknJyfFwk1SoDAs"
    b"4tsyH168m8D3KyWU9NjhXg6TaQ9BRKNx6KwreLvOgfzbIZyThfGbMgU5XwSbm5tCmIKOjo5D"
    b"J8xFQSYKOGx8Pp9AvbnJBSWCwmYlzlTE8Y3aJH7dFEVhdwCNEx50KL24N+rFO80B/KB2DefL"
    b"QvhyuYQ3PrHDbHGJzVkPhx8Xuf9KAVuAFzFvTMP21g7JNpZXVvFmlRrn70v4SmMK321I4tWm"
    b"OF57kMAPG2MoqIviQl0SL1Zv4mx5nH6n8EGzTlDEelgnU/pEFCiVSkxMTBwCYCHutiiElpeD"
    b"uNWjwo/anMhvD+KF1i18oTWFlx4k8UqbD7+qN+K1u2qca9nC6ZY0fl+lF5sy90xBa2vrk1HA"
    b"PHHy4IUp2pjL6jZJ6lGVNFiWUDWux/vd0/hLpw5XeqbRrpqDg9Lu7KID77Zp8U7LNBqHdORH"
    b"m0IPRxQXtSeiQJIkyoBr2NnZEcJRkfmflfH/PDK3QghY5j7PCd8hYetl1vHGXM6fiAKOArlc"
    b"Ljb+fwnnlUwU5MwDmSjgE3AIZlDzKdgq3BswIJEhKUq4WrJzZe7ziXmOPZ7XZ6KJrclz7NhM"
    b"xZGJiKOAsxZv0N/fj+vXr4vwaWpqQlVVlZirra0VXU5NTQ1mZ2dF08E+wwWMrVddXS3eG4qL"
    b"i9HY2Aiq/+IAbIUjKchYgF5QqLNVCgBFRUXo7e1FJXU1DIDvdXZ2Cm67u7vR09ODemo0dDqd"
    b"aMk5jWcAlJSUoKuri9q5FdG08vNsodwWoLacm4iDgwPs7x9gYGBAbHzjxg20tLQIxX19fUIR"
    b"V0wGNjQ0JDaXyWQCAFuCn+OwKy0tFc0tn35/fx8HpFNQkKscU5kkAB7qbum1zObAwOCA2KCh"
    b"oUH0+6yYW3WmgDdnCphf9gW2FHfT7D98nwGwBRg49wHc1Bqo1WML5CzHoiklAHPzc8TnrKj7"
    b"oh48yufsVHwS3pDfBXjk3yw8x89yO8dOyU532EW7D98vqIUfHx+n3uAICrT8XkDJBEgjnaZv"
    b"+vpfhZQd6qIPf3Mjo8nVkBj0MwV6nR6T8kkMDw6Sww0Izo8Sdspc85k51jNI+kbHRqGbniYq"
    b"Zj7VD/wb8xLWxx63hcwAAAAASUVORK5CYII=")
index.append('movie')
catalog['movie'] = movie


PIPE_HEIGHT = 18
PIPE_WIDTH = 2000

class MacRenderer(object):

    DONE_BITMAP = None
    REMAINING_BITMAP = None

    def __init__(self, parent):

        self.progressValue = random.randint(1, 99)


    def DrawSubItem(self, dc, rect, line, highlighted, enabled):
        """Draw a custom progress bar using double buffering to prevent flicker"""

        canvas = wx.Bitmap(rect.width, rect.height)
        mdc = wx.MemoryDC()
        mdc.SelectObject(canvas)

        if highlighted:
            mdc.SetBackground(wx.Brush(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)))
            mdc.SetTextForeground(wx.WHITE)
        else:
            mdc.SetBackground(wx.Brush(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)))
        mdc.Clear()

        mdc.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))

        if line == 0:
            text1 = "Apple Ads"
            text2 = "2.67 MB of 11.9 MB selected (22.53%) - 5 min 13 sec remaining"
            text3 = "Downloading from 1 of 1 peer - DL: 30.0 KB/s, UL: 0.0 KB/s"
            progress = 22.53
        else:
            text1 = "Apple TV Intro (HD).mov"
            text2 = "13.4 MB, uploaded 8.65 MB (Ratio: 0.64) - 1 hr 23 min remaining"
            text3 = "Seeding to 1 of 1 peer - UL: 12.0 KB/s"
            progress = 18.0

        ypos = 5
        xtext, ytext = mdc.GetTextExtent(text1)
        mdc.DrawText(text1, 0, ypos)
        ypos += ytext + 5

        mdc.SetFont(wx.Font(7, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))

        xtext, ytext = mdc.GetTextExtent(text2)
        mdc.DrawText(text2, 0, ypos)
        ypos += ytext + 5

        self.DrawProgressBar(mdc, 0, ypos, rect.width, 20, progress)

        mdc.SetFont(wx.Font(7, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))
        ypos += 25

        mdc.DrawText(text3, 0, ypos)
        dc.Blit(rect.x+3, rect.y, rect.width-6, rect.height, mdc, 0, 0)


    def GetLineHeight(self):

        dc = wx.MemoryDC()
        dc.SelectObject(wx.Bitmap(1, 1))
        dc.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
        dummy, ytext1 = dc.GetTextExtent("Agw")
        dc.SetFont(wx.Font(7, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))
        dummy, ytext2 = dc.GetTextExtent("Agw")

        dc.SelectObject(wx.NullBitmap)
        return ytext1 + 2*ytext2 + 40


    def GetSubItemWidth(self):

        return 250


    def DrawHorizontalPipe(self, dc, x, y, w, colour):
        """Draws a horizontal 3D-looking pipe."""

        for r in range(PIPE_HEIGHT):
            red = int(colour.Red() * math.sin((math.pi/PIPE_HEIGHT)*r))
            green = int(colour.Green() * math.sin((math.pi/PIPE_HEIGHT)*r))
            blue = int(colour.Blue() * math.sin((math.pi/PIPE_HEIGHT)*r))
            dc.SetPen(wx.Pen(wx.Colour(red, green, blue)))
            dc.DrawLine(x, y+r, x+w, y+r)


    def DrawProgressBar(self, dc, x, y, w, h, percent):
        """
        Draws a progress bar in the (x,y,w,h) box that represents a progress of
        'percent'. The progress bar is only horizontal and it's height is constant
        (PIPE_HEIGHT). The 'h' parameter is used to vertically center the progress
        bar in the allotted space.

        The drawing is speed-optimized. Two bitmaps are created the first time this
        function runs - one for the done (green) part of the progress bar and one for
        the remaining (white) part. During normal operation the function just cuts
        the necessary part of the two bitmaps and draws them.
        """

        # Create two pipes
        if self.DONE_BITMAP is None:
            self.DONE_BITMAP = wx.Bitmap(PIPE_WIDTH, PIPE_HEIGHT)
            mdc = wx.MemoryDC()
            mdc.SelectObject(self.DONE_BITMAP)
            self.DrawHorizontalPipe(mdc, 0, 0, PIPE_WIDTH, wx.GREEN)
            mdc.SelectObject(wx.NullBitmap)

            self.REMAINING_BITMAP = wx.Bitmap(PIPE_WIDTH, PIPE_HEIGHT)
            mdc = wx.MemoryDC()
            mdc.SelectObject(self.REMAINING_BITMAP)
            self.DrawHorizontalPipe(mdc, 0, 0, PIPE_WIDTH, wx.RED)
            self.DrawHorizontalPipe(mdc, 1, 0, PIPE_WIDTH-1, wx.WHITE)
            mdc.SelectObject(wx.NullBitmap)

        # Center the progress bar vertically in the box supplied
        y = y + (h - PIPE_HEIGHT)//2

        if percent == 0:
            middle = 0
        else:
            middle = int((w * percent)/100)

        if w < 1:
            return

        if middle == 0: # not started
            bitmap = self.REMAINING_BITMAP.GetSubBitmap((1, 0, w, PIPE_HEIGHT))
            dc.DrawBitmap(bitmap, x, y, False)
        elif middle == w: # completed
            bitmap = self.DONE_BITMAP.GetSubBitmap((0, 0, w, PIPE_HEIGHT))
            dc.DrawBitmap(bitmap, x, y, False)
        else: # in progress
            doneBitmap = self.DONE_BITMAP.GetSubBitmap((0, 0, middle, PIPE_HEIGHT))
            dc.DrawBitmap(doneBitmap, x, y, False)
            remainingBitmap = self.REMAINING_BITMAP.GetSubBitmap((0, 0, w - middle, PIPE_HEIGHT))
            dc.DrawBitmap(remainingBitmap, x + middle, y, False)


class TestUltimateListCtrl(ULC.UltimateListCtrl, listmix.ListCtrlAutoWidthMixin):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, agwStyle=0):

        ULC.UltimateListCtrl.__init__(self, parent, id, pos, size, style, agwStyle)
        listmix.ListCtrlAutoWidthMixin.__init__(self)


class UltimateListCtrlPanel(wx.Panel):

    def __init__(self, parent, log):

        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.log = log
        self.il = wx.ImageList(32, 32)

        self.il.Add(folder.GetBitmap())
        self.il.Add(movie.GetBitmap())

        self.list = TestUltimateListCtrl(self, -1,
                                         agwStyle=wx.LC_REPORT
                                         | wx.BORDER_SUNKEN
                                         #| wx.BORDER_NONE
                                         #| wx.LC_SORT_ASCENDING
                                         #| wx.LC_NO_HEADER
                                         #| wx.LC_VRULES
                                         | wx.LC_HRULES
                                         #| wx.LC_SINGLE_SEL
                                         | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)

        self.list.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        sizer.Add(self.list, 1, wx.EXPAND)

        self.PopulateList()
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

        self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self.OnColBeginDrag, self.list)


    def PopulateList(self):

        self.list.Freeze()

        info = ULC.UltimateListItem()
        info.Mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_FORMAT
        info.Align = 0
        info.Text = ""

        self.list.InsertColumnInfo(0, info)

        info = ULC.UltimateListItem()
        info.Align = wx.LIST_FORMAT_LEFT
        info.Mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_FORMAT
        info.Image = []
        info.Text = "Some useful info here"

        self.list.InsertColumnInfo(1, info)

        for i in range(2):
            index = self.list.InsertImageStringItem(sys.maxsize, "", [i])
            self.list.SetStringItem(index, 1, "")
            klass = MacRenderer(self)
            self.list.SetItemCustomRenderer(index, 1, klass)

        self.list.SetColumnWidth(0, 34)
        self.list.SetColumnWidth(1, 300)
        self.list.Thaw()
        self.list.Update()


    def OnColBeginDrag(self, event):

        if event.GetColumn() == 0:
            event.Veto()
            return

        event.Skip()


#---------------------------------------------------------------------------

class TestFrame(wx.Frame):

    def __init__(self, parent, log):

        wx.Frame.__init__(self, parent, -1, "UltimateListCtrl in torrent style :-D", size=(800, 600))

        self.log = log
        # Create the CustomTreeCtrl, using a derived class defined below
        self.ulc = UltimateListCtrlPanel(self, self.log)

        self.SetIcon(images.Mondrian.GetIcon())
        self.CenterOnScreen()
        self.Show()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    app = wx.App(0)
    frame = TestFrame(None, sys.stdout)
    frame.Show(True)
    app.MainLoop()


