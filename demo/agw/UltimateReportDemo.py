#!/usr/bin/env python

import sys
import os
import wx
import random
import datetime
import math
import operator

import wx.lib.mixins.listctrl as listmix
import wx.lib.colourdb as cdb
import wx.lib.colourselect as csel
import wx.lib.colourutils as cutils

from wx.lib.embeddedimage import PyEmbeddedImage

import images

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

musicdata = {
1 : ("Bad English", "The Price Of Love", "Rock", ""),
2 : ("DNA featuring Suzanne Vega", "Tom's Diner", "Rock", ""),
3 : ("George Michael", "Praying For Time", "Rock - HYPERTEXT", ""),
4 : ("Gloria Estefan", "Here We Are", "Rock", ""),
5 : ("Linda Ronstadt", "Don't Know Much", "Rock", ""),
6 : ("Michael Bolton", "How Am I Supposed To Live Without You", "Blues - HYPERTEXT", ""),
7 : ("Paul Young", "Oh Girl", "Rock", ""),
8 : ("Paula Abdul", "Opposites Attract", "Rock", ""),
9 : ("Richard Marx", "Should've Known Better", "Rock", ""),
10: ("Rod Stewart", "Forever Young (DISABLED)", "Rock", ""),
11: ("I am a really long item and I am going into overflow", "", "", ""),
12: ("Sheena Easton", "The Lover In Me", "Rock", ""),
13: ("Sinead O'Connor", "Nothing Compares 2 U", "Rock", ""),
14: ("Stevie B.", "Because I Love You", "Rock", ""),
15: ("Taylor Dayne", "Love Will Lead You Back", "Rock", ""),
16: ("The Bangles", "Eternal Flame", "Rock", ""),
17: ("Wilson Phillips", "Release Me", "Rock", ""),
18: ("Billy Joel", "Blonde Over Blue", "Rock", ""),
19: ("Billy Joel", "Famous Last Words", "Rock", ""),
20: ("Billy Joel", "Lullabye (Goodnight, My Angel)", "Rock", ""),
21: ("Billy Joel", "The River Of Dreams", "Rock", ""),
22: ("Billy Joel", "Two Thousand Years", "Rock", ""),
23: ("Janet Jackson", "Alright", "Rock", ""),
24: ("Janet Jackson", "Black Cat", "Rock", ""),
25: ("Janet Jackson", "Come Back To Me", "Rock", ""),
26: ("Janet Jackson", "Escapade", "Rock", ""),
27: ("Janet Jackson", "Love Will Never Do (Without You)", "Rock", ""),
28: ("Janet Jackson", "Miss You Much", "Rock", ""),
29: ("Janet Jackson", "Rhythm Nation", "Rock", ""),
30: ("Janet Jackson", "State Of The World", "Rock", ""),
31: ("Janet Jackson", "The Knowledge", "Rock", ""),
32: ("Spyro Gyra", "End of Romanticism", "Jazz", ""),
33: ("Spyro Gyra", "Heliopolis", "Jazz", ""),
34: ("Spyro Gyra", "Jubilee", "Jazz", ""),
35: ("Spyro Gyra", "Little Linda", "Jazz", ""),
36: ("Spyro Gyra", "Morning Dance", "Jazz", ""),
37: ("Spyro Gyra", "Song for Lorraine", "Jazz", ""),
38: ("Yes", "Owner Of A Lonely Heart", "Rock", ""),
39: ("Yes", "Rhythm Of Love", "Rock", ""),
40: ("Cusco", "Dream Catcher", "New Age", ""),
41: ("Cusco", "Geronimos Laughter", "New Age", ""),
42: ("Cusco", "Ghost Dance", "New Age", ""),
43: ("Blue Man Group", "Drumbone", "New Age", ""),
44: ("Blue Man Group", "Endless Column", "New Age", ""),
45: ("Blue Man Group", "Klein Mandelbrot", "New Age", ""),
46: ("Kenny G", "Silhouette", "Jazz", ""),
47: ("Sade", "Smooth Operator", "Jazz", ""),
48: ("David Arkenstone", "Papillon (On The Wings Of The Butterfly)", "New Age", ""),
49: ("David Arkenstone", "Stepping Stars", "New Age", ""),
50: ("David Arkenstone", "Carnation Lily Lily Rose", "New Age", ""),
51: ("David Lanz", "Behind The Waterfall", "New Age", ""),
52: ("David Lanz", "Cristofori's Dream", "New Age", ""),
53: ("David Lanz", "Heartsounds", "New Age", ""),
54: ("David Lanz", "Leaves on the Seine", "New Age", ""),
}

#---------------------------------------------------------------------------

_ulcStyles = ["ULC_VRULES", "ULC_HRULES", "ULC_ICON", "ULC_SMALL_ICON", "ULC_LIST",
              "ULC_REPORT", "ULC_TILE", "ULC_ALIGN_TOP", "ULC_ALIGN_LEFT", "ULC_AUTOARRANGE",
              "ULC_VIRTUAL", "ULC_EDIT_LABELS", "ULC_NO_HEADER", "ULC_NO_SORT_HEADER",
              "ULC_SINGLE_SEL", "ULC_SORT_ASCENDING", "ULC_SORT_DESCENDING",
              "ULC_NO_HIGHLIGHT", "ULC_STICKY_HIGHLIGHT", "ULC_STICKY_NOSELEVENT",
              "ULC_SEND_LEFTCLICK", "ULC_HAS_VARIABLE_ROW_HEIGHT", "ULC_AUTO_CHECK_CHILD",
              "ULC_AUTO_TOGGLE_CHILD", "ULC_AUTO_CHECK_PARENT", "ULC_SHOW_TOOLTIPS",
              "ULC_HOT_TRACKING", "ULC_BORDER_SELECT", "ULC_TRACK_SELECT", "ULC_HEADER_IN_ALL_VIEWS",
              "ULC_NO_FULL_ROW_SELECT", "ULC_FOOTER"]

#---------------------------------------------------------------------------

coloursBitmap = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABGdBTUEAAK/INwWK6QAAABl0"
    b"RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAnTSURBVHjaYvz//z/DQAKAAGIB"
    b"EXl5DWAO0DGMnJxCScKiKg4cHPzyLMycwoyMTEDx3+///P329P+/z3dPndx25tbd61dd3MLf"
    b"/P707O3GjfMZzGwiGG7dOM5w9uwxkh0AEEBgB+zfvwXM+fPnN4OCgjZHWERkDBurGMO3z0Cx"
    b"30CH/WNgYGVkYGACqnZxcmWwd/j8/O7rN6/vfHj7TFBP+BYX//9TjP//7GBhZHj7h8QABQgg"
    b"RlAUMDIywgU4OTmYSku23BYXdVb69AHiABD+9xdkMiMDMEAY2NkZGLi4GBi+ANl3vjAwnHvy"
    b"g+HblzvPFBkOrL1+uK332YvnD4mNWYAAAjvA3MIR6M0/oChgkJJStLKz7tv366co+6dPDAzf"
    b"vv9n+P7jH8PvP3/BaliZ/wId8J+BnYOVgZeHnUGAn4nhGzBkTjxnYDj4mIFBifHY1YfbA+Pe"
    b"vnt1jhgHAAQQ2AFRMVkMjP9+MPz995tdRiZ0C5+An8uHt98Z2H4+YuBjuMcgznKXQYb9PoMg"
    b"6wcGLqafDOzM/xhYmZgZ/jFxM/xl4Gb4xyLA8IdDluHKZxWGw++ZGNg4T97evn1u4evbb3e8"
    b"/friLz4HAAQQOA38BQbvn//cDDx8mjWCfLYukt/XM/iIrGGQ5jnHIMTxioGV9Tsw9IEJ4T8z"
    b"UDErELNAaSD/NxS/YGLQ/svE4GMjzLCQI05V3sZ5rcb5F9uuzLnadOfB1Qu4HAAQQGAH/AYa"
    b"zMslUxAky1VjzRbDICJ4ioGBGxi5rL8YGIC+BSY/cPwz/Ad65t8fsAP+/wYmjN9A7b9ZGf5/"
    b"ZmT4z8nPwGwpz8CtxsTgwvCA4e6zBvabjhWBEupCLkorg9uObNjZ/+3Pl5/oDgAIIJDJDCpc"
    b"LFX1snd7/ZmnMogw3wLaB0xh/7iBFgJT23+QG/8z/Gf8C0wjwHTyF4h/Ax326yfD/6/fGf69"
    b"BaZUXm4GZmcjBgZ1DSBbjUFK4AMDKzDNuDBOZBAQNeR9k3673TbWo5+TkZsf3QEAAQR2wNsX"
    b"d0T+f3n8D+gNYJIHqvnNAcTsEAzy7T+gsl8gDAwFkB+AifL/V6BDPvxiYBSXY2BydWJgUFNl"
    b"YBASAzpABBiVzAxSPGcYnv3kYPDj6mUQYrRgeB1zM9My3LWLlYmNB9kBAAEEdsC87VtrHFbd"
    b"Klj3gO81w18+oEXcEAx0wH+QI36CMDDOfwAd84OZ4f83YOH06T8Dk5w8A5OzKQODgiwDA58g"
    b"MNqAelmBjge6UlfgDMPLn/+ALBYGP+4eBuY/8gzfk16kaRoaZgAVMMMcABBATFD625Mn96ZG"
    b"rTwR2XeJ/fK/30JAy0COADr2BzA6fgAN/c7B8P87GzDzAx3xgZmBSUaGgdFOmoFBCugwXiDm"
    b"AKpjAqaRv2+BDn/OIMlxCRhlXxg+AZMKDxsvgwd7H8N7lu8MoimCJSK8kg4wBwAEEBNycPz8"
    b"/HZv+ebj0W3n2c7AHQHC37iAvgaGwhdgiLxjZWCSlGBgtAJGlTAwd3B8BfoHiP8D08LvJ0B8"
    b"FxiNLxkE2Z4z8LB8ZQCVX7+B6ViCS5XB6HcNw1uNR+IyVgpxQOvA6QEggJjQE8Wf7x8vN+44"
    b"ET/pGtd5hj+CEAd8B6aNb8AQeM/OwCgmyMBoCfSxAMhioAP+vwHacB8YWteAGJiAfwNLo38/"
    b"GXhZvjHwsH5h+ActEUEOUeUIYWD+q80g7MzlwcbEoQ0SBwggJmx588/X99dqth5P2/GY/zXj"
    b"Hx4GRmA0/P/EycDIx83AZAEMZp73QFVAB/z9AVT8EWjpQ6Dld4D8p6AUCjaWE+g4DuZvDGD7"
    b"oSU9C9A2yd8pDD80f4vJKSkCi18GDoAAYsJVQHz99PZM+YGHJQ++CgHLYS4GRjYOBiZzoKU8"
    b"wDj+9w1UcwFpYNj+BWbJf8Ba6/9nkNMRRSww27Iw/EbiQ7DgfyeGX+xKDHzyXIZAYSGAAGLC"
    b"V0xeun1j5bTrv9czsPAyMBkBfcr7CuhBoIW/gSb9YYGUhP+g4Qv2JtSrMG8D0d9/IHdC4oEJ"
    b"yGdjBibiPxYMjMJ/xYFCAgABhNcBDH9//lx89l7bCV7Gz9+FgcH+A2TxX0iZ8BOIfwAN/vkX"
    b"IvYXpYYBWszK8PsvG9gBv4EO+AtkgOodNrAR1gx/uThA5QEXQACxEKqtXjy/dS5k5s9kmRV8"
    b"/mYqglpuRowqdlovefmkgFUlsFRk+AXMftzAHMIJ8jEzpNQGBsv3v9wMX35ygbnfgdkTFAbf"
    b"/4BijoWB5b8aw08WCWBKZmADCCAWYqrMp48ergEmrwMnLzMJHrlm2mQpLxsqLP3yVab7OwlJ"
    b"ZWDIMPICLWaCRjSQBlbZH37zM7z6xscgwPyH4dO/3+CY+gYMpW+gEPvPysD4SxQcVgABxEJk"
    b"w+W/iIjEawV5FW4zYV6nA7cfHL22686q5fvlpYoChKJivd/K8ygA/cgkAHXIP4aXX8UZXn3m"
    b"ZmBk/cHwD+gIUBh8/8vI8BGYLn8BKz/Gz6yg7PIXIIDADnB2C8PfaABiHj4BBlnWr3Vvntxl"
    b"u/3s4X6g3m13Htx7nDWJd9PWM7L5PdlfIzQsgQkV2DZg4PjLcPWNFsPLj8wMrGwfGT4B23S/"
    b"gEHwE5gWvv1jZPgGDCXObz9/gSpigAACO0BUVAq/94Exyfrviz3nj3vxR+89W/v757dDQOGH"
    b"IB8As+CJrUeuX73+SOnknArOBkf/T/z/fvIwrLjlxPDy0x+G7/9/A+sTYAj8+wtsczACSwkW"
    b"hn/AAkrq2ztQCPwGCCBog+Qv/swATCzyDA/q7r35+vTRs6cgyy8woKT7/5/vPbo7MaZJ/uV6"
    b"Ho7ZotbK3MfuSDJwP9nxh+Hl+Q/sX55++P/nx1d2Ll7mPwKqwj8kTSX/fnoNbHAw/AIIIEga"
    b"ADV7cYB/wIpLkOFVMPff1077rj6bBWwQnALV4NgC6tmLh8vze5V4NI+yFLLtDn/76enZM89+"
    b"/rkEykxA/BFkHDA6uRUVlM2evX/3CSQGEEDgNmFoeCaOsP8P1MHEa8Z28eLhm+8+bj19YwJQ"
    b"dB0Qf8adYFjYgK0XA0hjAhxNrxggrQjkdjKwWgU2JoHVG0AAgUOAlRl7efT52w8mBab7bb9+"
    b"vhLfd+31KqDQSbyWgx39B5S4ThHIVb+gmAEggPCWhCzMDEF/2Hmytz/kuvH968fTQKF71O6a"
    b"AQQQVgeAypN///7x/vrxrusjs8j/q/efngcKX4e5mpoAIIDAUcDGxobmACaGr18/xktLSyke"
    b"OXL4wqePb4H5HtjUpQEACCCwA+7cuYbmAEaGnz+/Xfz+/cv6u3dvXwQKHQGVpLRwAEAAMRDo"
    b"nssAsTLMobQAAAEGABjdycfQA1R2AAAAAElFTkSuQmCC")

#----------------------------------------------------------------------
decryptedBitmap = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAABGdBTUEAAK/INwWK6QAAABl0"
    b"RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAUnSURBVHjaYvz//z8DCISGpjLA"
    b"AEjs9+8/DL9+fefh4uKoVlCQi5KQkBBnYmJifPHi2Ztbt66v+/DhfTMrK/Or////AHUwwvXu"
    b"3bsXTAMEEAsDDvD79y95WVnpXV5eHmqSknJA/j8GVlYWBh4eLqlXr57mrFq1NPDKlQs+bGws"
    b"F7DpBwggFuyG/mEBGrrJ399f7f9/NoYdO3b/f/Tozot///7+VVJSl/Lw8GDKzMyXnj69f8Pl"
    b"yxcM2NnZP6CbARBATDDG338MDP/+/WP48+cPAwcHW7OFhaXez59MQEM3/zp58kDO06cPpB4/"
    b"vi+7d+/m8IUL537984eJwc8vTJ6fX7Dj798/DIyMjGAMAwABBDeYjfk/w38WLgYmZlYWdjY2"
    b"75s3b//fu3fb7ydPH7X8Z+Gc9p+ZneEfCycDEyvbmuvXzubt37/7v6KiGoOGhk4o0DF8//4B"
    b"4+Tvf7jBAAEEN9jo9yEGiX+PGThYmf99+cMWfPX2A/X7z16rMjP8a5X5/5RBiuEFgzzjcwY+"
    b"pp8Mv/4xLLpy5fyDHz9+MqioaAoyMzPb/wDGoQjzF7jBAAEED2Puv+8YdH/sZnjDJv/vOyPP"
    b"bYZ/fxmAocPA+f8rg/i/J0A2MwMz0z+Gd0y8DIf+qP159+XrjU+fPikKCokw/mXiUJP6/5rB"
    b"juMJ3GCAAIIb/O8/I8P3XywMvL8eMPCBjISG139gUvrCwAJmgZIVJ+NHBss/ZxjOf+X/+Pnb"
    b"X4Zvf1gZRP5/+GvDcoPh/z9OuMEAAQQ3mJ2TvVtaUTSQiQmUjBn/w0MKbgETPL0y/f/9W4Hl"
    b"gxzrw6UMYj++MYQZM1bz/FfOevH0436gdDpIDUAAMcIyyP4265/2Ee5sIC////sTaNJvIP4F"
    b"9Aowxpn+M7Cw/QHz//z6xfD/538G5r/AZPnjK1COkYGZDehSdm6GU3vu/LHM38sKMg8ggOAu"
    b"5mAH5iseQQYmFiGgjrfA9PcJkgYZgIb/fMLw7No1hn+/fzDIKPMBxXgZGL6yMbADLWQAWsAA"
    b"DBIGRgEGDk5meHoDCCC4wf+BkcXw4zUDAzPQtb/fAzUAY5jpB9DQZwxb5h9gKJrzheEn0BOt"
    b"MSwMMVEyDAx/eKAWgzQD9TL9Yfj/hwue3gACCJHz/gMV/fkIpIFe/guk/wENZv7B8Pv5I4ZF"
    b"W78wPHoH5AKVLdr5h8HP6h0DnxTIAVBzQHpAIfefA24cQAAhGfwfajDQ638+QVz8/zsDK9cf"
    b"BjclJoY7V4G5EqjMXR4YEGzfgb77BTYMkqR+g3IYkBaDGwcQQEwIg0EKvgIxyLWfIfgn0AIB"
    b"RgZ3O04GVXYGBnmgag9TYNYVAFrxB+hiBhgGBTTI2n9w4wACCGEwKFkxgmL+KwQzfAOGGxB/"
    b"+8Jw6/hPhn9A/cxAfbfPgPSzMTDwAb3NxQ7B3ECPc7KiFEIAAYSIPJDBTCCDf0AMBWEWoJdv"
    b"f2QQeP+HIUQD4gzRX/8Z/r1gZGDSARr8AxZXQH0cQMuYEO4ECCAWFBczgILhE9RbQEN/AZ0p"
    b"wsJgVCXEYMwGzSjAoGVkBRrAAsTcMM3MoPQKch3cOIAAQoo8oEImoKH/XgHVsYJdB9Ygzs3A"
    b"iEiekLwHCkqkkgwchKzsyBUJA0AAwQ1mBBnEDTQQWLADy0cGkgDItywsKA4ACCAWpNTGyMAt"
    b"AlQESjbMJBoMTBXMfMCE9QceyAABBDf43vXnp5nnMpswAQv0///+/yfNwSCH/GK6e+X5dWOo"
    b"GECAAQCxvOh5cbsDqwAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------

PIPE_HEIGHT = 18
PIPE_WIDTH = 300

class UltimateRenderer_1(object):

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
        else:
            mdc.SetBackground(wx.Brush(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)))
        mdc.Clear()

        self.DrawProgressBar(mdc, 0, 0, rect.width, rect.height, self.progressValue)

        mdc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        text = "%d Mb"%self.progressValue
        textWidth, dummy = mdc.GetTextExtent(text)
        mdc.DrawText(text, rect.width/2 - textWidth/2, rect.height/2 - dummy/2)
        dc.SetClippingRegion(rect.x, rect.y, rect.width, rect.height)
        dc.Blit(rect.x+3, rect.y, rect.width-6, rect.height, mdc, 0, 0)
        dc.DestroyClippingRegion()


    def GetLineHeight(self):

        return PIPE_HEIGHT + 6


    def GetSubItemWidth(self):

        return 130


    def UpdateValue(self):

        self.progressValue += 5
        if self.progressValue >= 100:
            self.progressValue = 1


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
        y = y + (h - PIPE_HEIGHT)/2

        if percent == 0:
            middle = 0
        else:
            middle = (w * percent)/100

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


class UltimateRenderer_2(object):

    def __init__(self, parent):

        e = wx.FontEnumerator()
        e.EnumerateFacenames()
        fontList = e.GetFacenames()
        fontList.sort()

        rdn = random.randint(0, len(fontList)-1)
        randomFont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        randomFont.SetFaceName(fontList[rdn])

        self.randomFont = randomFont
        self.text = "This is my renderer"

        dc = wx.ClientDC(parent)
        dc.SetFont(self.randomFont)
        self.width, self.height, descent, el = dc.GetFullTextExtent(self.text)

        self.height += descent


    def DrawSubItem(self, dc, rect, line, highlighted, enabled):

        dc.SetBackgroundMode(wx.SOLID)
        dc.SetBrush(wx.Brush(wx.BLACK, wx.BRUSHSTYLE_SOLID))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(rect)

        dc.SetBackgroundMode(wx.TRANSPARENT)
        dc.SetFont(self.randomFont)

        colours = [wx.RED, wx.WHITE, wx.GREEN, wx.Colour("SKY BLUE")]
        w, h = dc.GetTextExtent("Hg")
        x = rect.x + 1
        y = rect.y + rect.height/2 - h/2

        for ch in self.text:
            dc.SetTextForeground(random.choice(colours))
            dc.DrawText(ch, x, y)
            w, h = dc.GetTextExtent(ch)
            x = x + w
            if x > rect.right - 5:
                break


    def GetLineHeight(self):

        return self.height + 5


    def GetSubItemWidth(self):

        return self.width + 5


class UltimateRenderer_3(object):

    def __init__(self):

        cdb.updateColourDB()
        colourList = cdb.getColourList()
        lenCDB = len(colourList)
        colourIndex = random.randint(0, lenCDB-1)
        self.colour = colourList[colourIndex]


    def DrawSubItem(self, dc, rect, line, highlighted, enabled):

        centerX, centerY = rect.width/2, rect.height/2
        dc.GradientFillConcentric(rect, self.colour, wx.WHITE, (centerX, centerY))


    def GetLineHeight(self):

        return 30


    def GetSubItemWidth(self):

        return 40


class UltimateHeaderRenderer(object):

    def __init__(self, parent):
        self._hover = False
        self._pressed = False

    def DrawHeaderButton(self, dc, rect, flags):

        self._hover = False
        self._pressed = False

        color = wx.Colour(150,150,150)
        if flags & wx.CONTROL_DISABLED:
            color = wx.Colour(wx.WHITE)
        elif flags & wx.CONTROL_SELECTED:
            color = wx.Colour(wx.BLUE)

        if flags & wx.CONTROL_PRESSED:
            self._pressed = True
            color = cutils.AdjustColour(color,-50)
        elif flags & wx.CONTROL_CURRENT:
            self._hover = True
            color = cutils.AdjustColour(color,50)

        dc.SetBrush(wx.Brush(color, wx.BRUSHSTYLE_SOLID))
        dc.SetBackgroundMode(wx.SOLID)
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(rect)

        dc.SetBackgroundMode(wx.TRANSPARENT)


    def GetForegroundColour(self):

        if self._hover:
            return wx.Colour(30,30,30)
        else:
            return wx.Colour(230,230,230)



class TestUltimateListCtrl(ULC.UltimateListCtrl):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, agwStyle=0):

        ULC.UltimateListCtrl.__init__(self, parent, id, pos, size, style, agwStyle)
##        listmix.TextEditMixin.__init__(self)


class UltimateListCtrlPanel(wx.Panel, listmix.ColumnSorterMixin):

    def __init__(self, parent, log):

        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS|wx.SUNKEN_BORDER)

        sizer = wx.BoxSizer(wx.VERTICAL)

        cdb.updateColourDB()
        self.colourList = cdb.getColourList()
        self.count = 0
        self.log = log

        self.il = ULC.PyImageList(16, 16)

        self.idx1 = self.il.Add(images.Smiles.GetBitmap())
        self.sm_up = self.il.Add(images.SmallUpArrow.GetBitmap())
        self.sm_dn = self.il.Add(images.SmallDnArrow.GetBitmap())
        self.il.Add(images.core.GetBitmap())
        self.il.Add(images.custom.GetBitmap())
        self.il.Add(images.exit.GetBitmap())
        self.il.Add(images.expansion.GetBitmap())
        self.il.Add(decryptedBitmap.GetBitmap())
        self.il.Add(coloursBitmap.GetBitmap())

        self.list = TestUltimateListCtrl(self, -1,
                                         agwStyle=wx.LC_REPORT
                                         #| wx.BORDER_SUNKEN
                                         | wx.BORDER_NONE
                                         | wx.LC_EDIT_LABELS
                                         #| wx.LC_SORT_ASCENDING
                                         #| wx.LC_NO_HEADER
                                         | wx.LC_VRULES
                                         | wx.LC_HRULES
                                         #| wx.LC_SINGLE_SEL
                                         | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)

        self.list.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        sizer.Add(self.list, 1, wx.EXPAND)

        self.timer = wx.Timer(self, wx.ID_ANY)

        self.PopulateList()
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

        self.itemDataMap = musicdata
##        listmix.ColumnSorterMixin.__init__(self, 4)

        self.Bind(ULC.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.list)
        self.Bind(ULC.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.list)
        self.Bind(ULC.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.list)
        self.Bind(ULC.EVT_LIST_DELETE_ITEM, self.OnItemDelete, self.list)
        self.Bind(ULC.EVT_LIST_COL_CLICK, self.OnColClick, self.list)
        self.Bind(ULC.EVT_LIST_COL_RIGHT_CLICK, self.OnColRightClick, self.list)
        self.Bind(ULC.EVT_LIST_COL_BEGIN_DRAG, self.OnColBeginDrag, self.list)
        self.Bind(ULC.EVT_LIST_COL_DRAGGING, self.OnColDragging, self.list)
        self.Bind(ULC.EVT_LIST_COL_END_DRAG, self.OnColEndDrag, self.list)
        self.Bind(ULC.EVT_LIST_BEGIN_LABEL_EDIT, self.OnBeginEdit, self.list)
        self.Bind(ULC.EVT_LIST_BEGIN_DRAG, self.OnBeginDrag)
        self.Bind(ULC.EVT_LIST_END_DRAG, self.OnEndDrag)

        self.list.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.list.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

        # for wxMSW
        self.list.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)

        # for wxGTK
        self.list.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)

        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(wx.EVT_TIMER, self.OnTimer)


    def PopulateList(self):

        self.list.Freeze()

        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        boldfont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        boldfont.SetWeight(wx.FONTWEIGHT_BOLD)
        boldfont.SetPointSize(12)
        boldfont.SetUnderlined(True)

        info = ULC.UltimateListItem()
        info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT | ULC.ULC_MASK_CHECK
        info._image = [1, 2]
        info._format = 0
        info._kind = 1
        info._text = "Artist\nName"

        self.list.InsertColumnInfo(0, info)

        info = ULC.UltimateListItem()
        info._format = wx.LIST_FORMAT_RIGHT
        info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT | ULC.ULC_MASK_FONT
        info._image = []
        info._text = "Title"
        info._font = boldfont

        self.list.InsertColumnInfo(1, info)

        info = ULC.UltimateListItem()
        info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
        info._format = 0
        info._text = "Genre"
        info._font = font
        info._image = [3]
        self.list.InsertColumnInfo(2, info)

        info = ULC.UltimateListItem()
        info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_FORMAT | ULC.ULC_MASK_FONTCOLOUR
        info._format = 0
        info._text = "Custom Renderer"
        info._colour = wx.RED

        # Add our custom renderer for the header of column 3, we can also use
        # SetHeaderCustomRenderer to set the renderer for all the columns.
        klass = UltimateHeaderRenderer(self)
        info.SetCustomRenderer(klass)

        self.list.InsertColumnInfo(3, info)

        # The custom renderer can also be set for all columns on the header and/or footer
        # self.list.SetHeaderCustomRenderer(klass)

        # We must first have a footer in order to set its custom renderer:
        # style = self.list.GetAGWWindowStyleFlag() | ULC.ULC_FOOTER
        # if self.list.GetAGWWindowStyleFlag() != style:
            # self.list.SetAGWWindowStyleFlag(style)
        # self.list.SetFooterCustomRenderer(klass)

        items = musicdata.items()
        renderers = {}

        for key, data in items:
            if key == 3:
                index = self.list.InsertImageStringItem(sys.maxsize, data[0], [3, 4, 7], it_kind=1)
            elif key == 4:
                dt = "\n".join(data[0].split())
                index = self.list.InsertImageStringItem(sys.maxsize, dt, [self.idx1, 8, 7])
            else:
                index = self.list.InsertImageStringItem(sys.maxsize, data[0], self.idx1)

            if key == 6:
                self.list.SetStringItem(index, 1, data[1], it_kind=1)
            elif key == 7:
                self.list.SetStringItem(index, 1, data[1], [6, 5, 4])
            elif key == 8:
                dt = "\n".join(data[1].split())
                self.list.SetStringItem(index, 1, dt)
            else:
                self.list.SetStringItem(index, 1, data[1])

            it_kind = 0
            if random.randint(0, 2) == 2:
                # set some radiobutton-like item on the 3rd column
                it_kind = 2

            self.list.SetStringItem(index, 2, data[2], it_kind=it_kind)
            self.list.SetStringItem(index, 3, data[3])

            randomRenderer = random.randint(0, 2)
            if randomRenderer == 2:
                # set some custom renderers...
                klass = UltimateRenderer_1(self)
                renderers[index] = klass
                self.list.SetItemCustomRenderer(index, 3, klass)
            elif randomRenderer == 1:
                klass = UltimateRenderer_2(self)
                self.list.SetItemCustomRenderer(index, 3, klass)
            else:
                klass = UltimateRenderer_3()
                self.list.SetItemCustomRenderer(index, 3, klass)

            self.list.SetItemData(index, key)

        self.renderers = renderers

        # show how to select an item
        self.list.Select(5, True)

        # show how to change the colour of a couple items
        item = self.list.GetItem(1)
        item.SetTextColour(wx.BLUE)
        pyData = datetime.date(2009, 1, 1)
        item.SetPyData(pyData)

        self.list.SetItem(item)
        item = self.list.GetItem(4)
        item.SetTextColour(wx.RED)
        pyData = datetime.date(2011, 3, 2)
        item.SetPyData(pyData)
        self.list.SetItem(item)

        # Disable one item
        item = self.list.GetItem(9)
        item.Enable(False)
        self.list.SetItem(item)

        # Set 2 hypertext items
        for ids in [2, 5]:
            item = self.list.GetItem(ids, 2)
            item.SetHyperText(True)
            self.list.SetItem(item)

        # Set 2 items with widgets
        item = self.list.GetItem(8, 1)
        self.gauge = wx.Gauge(self.list, -1, 50, style=wx.GA_HORIZONTAL|wx.GA_SMOOTH)
        self.gauge.SetValue(20)
        item.SetWindow(self.gauge)
        self.list.SetItem(item)

        item = self.list.GetItem(11, 0)
        textctrl = wx.TextCtrl(self.list, -1, "I Am A Simple\nMultiline wx.TexCtrl", style=wx.TE_MULTILINE)
        item.SetWindow(textctrl)
        self.list.SetItem(item)

        # Put an item with overflow
        self.list.SetItemOverFlow(10, 0, True)

        self.currentItem = 0

        fontMask = ULC.ULC_MASK_FONTCOLOUR|ULC.ULC_MASK_FONT
        fullMask = fontMask|ULC.ULC_MASK_BACKCOLOUR

        customRow, customCol, colours = [0, 3], [2, 1], [wx.RED, wx.Colour("Yellow")]

        for row, col, colour in zip(customRow, customCol, colours):
            item = self.list.GetItem(row, col)
            item.SetMask(fullMask)
            item.SetTextColour(wx.GREEN)
            font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font.SetWeight(wx.FONTWEIGHT_BOLD)
            item.SetFont(font)
            item.SetBackgroundColour(colour)
            self.list.SetItem(item)

        standardFont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        italicFont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        italicFont.SetStyle(wx.FONTSTYLE_ITALIC)
        boldFont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        boldFont.SetWeight(wx.FONTWEIGHT_BOLD)

        lenCDB = len(self.colourList)

        for indx in range(11, 20):
            for col in range(self.list.GetColumnCount()):
                result = random.randint(0, 2)
                colourIndex = random.randint(0, lenCDB-1)

                if result == 0:
                    fnt = standardFont
                elif result == 1:
                    fnt = boldFont
                else:
                    fnt = italicFont

                item = self.list.GetItem(indx, col)
                item.SetMask(fontMask)
                item.SetFont(fnt)
                item.SetTextColour(wx.TheColourDatabase.FindColour(self.colourList[colourIndex]))
                self.list.SetItem(item)

        self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(2, 100)
        self.list.SetColumnWidth(3, 130)

##        self.list.SetColumnShown(1, False)

        self.list.Thaw()
        self.list.Update()

        self.timer.Start(300)

##        self.list.EnableSelectionVista(True)
##        self.list.SetGradientStyle(1)
##        self.list.SetBackgroundImage(wx.Bitmap("splash.png", wx.BITMAP_TYPE_PNG))


    def ChangeStyle(self, checks):

        style = 0
        for check in checks:
            if check.GetValue() == 1:
                style = style | eval("ULC." + check.GetLabel())

        if self.list.GetAGWWindowStyleFlag() != style:
            self.list.SetAGWWindowStyleFlag(style)


    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self.list

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)


    def OnTimer(self, event):

        for key, renderer in self.renderers.items():
            renderer.UpdateValue()
            self.list.RefreshItem(key)


    def OnIdle(self, event):

        if self.gauge:
            try:
                if self.gauge.IsEnabled() and self.gauge.IsShown():
                    self.count = self.count + 1

                    if self.count >= 50:
                        self.count = 0

                    self.gauge.SetValue(self.count)

            except:
                self.gauge = None

        event.Skip()


    def OnRightDown(self, event):
        x = event.GetX()
        y = event.GetY()

        self.log.write("x, y = %s\n" % str((x, y)))

        item, flags = self.list.HitTest((x, y))

        if item != wx.NOT_FOUND and flags & wx.LIST_HITTEST_ONITEM:
            self.list.Select(item)

        event.Skip()


    def getColumnText(self, index, col):
        item = self.list.GetItem(index, col)
        return item.GetText()


    def OnItemSelected(self, event):
        self.currentItem = event.Index
        self.log.write("OnItemSelected: %s, %s, %s, %s\n" %(self.currentItem,
                                                            self.list.GetItemText(self.currentItem),
                                                            self.getColumnText(self.currentItem, 1),
                                                            self.getColumnText(self.currentItem, 2)))

        if self.list.GetPyData(self.currentItem):
            self.log.write("PYDATA = %s\n"%repr(self.list.GetPyData(self.currentItem)))

        if self.currentItem == 10:
            self.log.write("OnItemSelected: Veto'd selection\n")
            #event.Veto()  # doesn't work
            # this does
            self.list.SetItemState(10, 0, wx.LIST_STATE_SELECTED)

        event.Skip()


    def OnItemDeselected(self, evt):
        item = evt.GetItem()
        self.log.write("OnItemDeselected: %d\n" % evt.Index)

##        # Show how to reselect something we don't want deselected
##        if evt.Index == 11:
##            wx.CallAfter(self.list.SetItemState, 11, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)


    def OnItemActivated(self, event):
        self.currentItem = event.Index
        self.log.write("OnItemActivated: %s\nTopItem: %s\n" %(self.list.GetItemText(self.currentItem), self.list.GetTopItem()))

    def OnBeginEdit(self, event):
        self.log.write("OnBeginEdit\n")
        event.Allow()

    def OnItemDelete(self, event):
        self.log.write("OnItemDelete\n")

    def OnColClick(self, event):
        self.log.write("OnColClick: %d\n" % event.GetColumn())
        event.Skip()

    def OnColRightClick(self, event):
        item = self.list.GetColumn(event.GetColumn())
        self.log.write("OnColRightClick: %d %s\n" %(event.GetColumn(), (item.GetText(), item.GetAlign(),
                                                                        item.GetWidth(), item.GetImage())))

    def OnColBeginDrag(self, event):
        self.log.write("OnColBeginDrag\n")
        ## Show how to not allow a column to be resized
        #if event.GetColumn() == 0:
        #    event.Veto()


    def OnColDragging(self, event):
        self.log.write("OnColDragging\n")

    def OnColEndDrag(self, event):
        self.log.write("OnColEndDrag\n")

    def OnBeginDrag(self, event):
        self.log.write("OnBeginDrag\n")


    def OnEndDrag(self, event):
        self.log.write("OnEndDrag\n")

    def OnDoubleClick(self, event):
        self.log.write("OnDoubleClick item %s\n" % self.list.GetItemText(self.currentItem))
        event.Skip()

    def OnRightClick(self, event):
        self.log.write("OnRightClick %s\n" % self.list.GetItemText(self.currentItem))

        # only do this part the first time so the events are only bound once
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()
            self.popupID4 = wx.NewId()
            self.popupID5 = wx.NewId()
            self.popupID6 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.OnPopupOne, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnPopupTwo, id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.OnPopupThree, id=self.popupID3)
            self.Bind(wx.EVT_MENU, self.OnPopupFour, id=self.popupID4)
            self.Bind(wx.EVT_MENU, self.OnPopupFive, id=self.popupID5)
            self.Bind(wx.EVT_MENU, self.OnPopupSix, id=self.popupID6)

        # make a menu
        menu = wx.Menu()
        # add some items
        menu.Append(self.popupID1, "FindItem tests")
        menu.Append(self.popupID2, "Iterate Selected")
        menu.Append(self.popupID3, "ClearAll and repopulate")
        menu.Append(self.popupID4, "DeleteAllItems")
        menu.Append(self.popupID5, "GetItem")
        menu.Append(self.popupID6, "Edit")

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()


    def OnPopupOne(self, event):
        self.log.write("Popup one")
        self.log.write("FindItem: %s"%self.list.FindItem(-1, "Roxette"))
        self.log.write("FindItemData: %s\n"%self.list.FindItemData(-1, 11))

    def OnPopupTwo(self, event):
        self.log.write("Selected items:")
        index = self.list.GetFirstSelected()

        while index != -1:
            self.log.write("      %s: %s" % (self.list.GetItemText(index), self.getColumnText(index, 1)))
            index = self.list.GetNextSelected(index)

        self.log.write("\n")

    def OnPopupThree(self, event):
        self.log.write("Popup three")
        self.list.ClearAll()
        wx.CallAfter(self.PopulateList)


    def OnPopupFour(self, event):
        self.list.DeleteAllItems()

    def OnPopupFive(self, event):
        item = self.list.GetItem(self.currentItem)
        self.log.write(("%s, %s, %s")%(item._text, item._itemId, self.list.GetItemData(self.currentItem)))

    def OnPopupSix(self, event):
        self.list.EditLabel(self.currentItem)


#---------------------------------------------------------------------------

class TestFrame(wx.Frame):

    def __init__(self, parent, log):

        wx.Frame.__init__(self, parent, -1, "UltimateListCtrl in wx.LC_REPORT mode", size=(800, 600))

        splitter = wx.SplitterWindow(self, -1, style=wx.CLIP_CHILDREN | wx.SP_LIVE_UPDATE | wx.SP_3D)

        self.log = log
        # Create the CustomTreeCtrl, using a derived class defined below
        self.ulc = UltimateListCtrlPanel(splitter, self.log)

        self.leftpanel = wx.ScrolledWindow(splitter, -1, style=wx.SUNKEN_BORDER)
        self.leftpanel.SetScrollRate(20, 20)
        width = self.PopulateLeftPanel()

        # add the windows to the splitter and split it.
        splitter.SplitVertically(self.leftpanel, self.ulc, width+5)
        splitter.SetMinimumPaneSize(width+5)

        sizer = wx.BoxSizer()
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetIcon(images.Mondrian.GetIcon())
        self.CenterOnScreen()
        self.Show()


    def PopulateLeftPanel(self):

        pnl = wx.Panel(self.leftpanel)
        mainsizer = wx.BoxSizer(wx.VERTICAL)

        staticboxstyles = wx.StaticBox(pnl, -1, "UltimateListCtrl Styles")
        stylesizer = wx.StaticBoxSizer(staticboxstyles, wx.VERTICAL)
        staticboxthemes = wx.StaticBox(pnl, -1, "UltimateListCtrl Themes/Gradients")
        themessizer = wx.StaticBoxSizer(staticboxthemes, wx.VERTICAL)

        self.ulcstyles = []
        sorted_styles = []

        for style in _ulcStyles:
            sorted_styles.append((style, eval("ULC." + style)))

        sorted_styles.sort(key=operator.itemgetter(1))

        count = 0
        for styleName, styleVal in sorted_styles:

            if styleName in ["ULC_VIRTUAL", "ULC_TILE", "ULC_LIST", "ULC_ICON",
                             "ULC_SMALL_ICON", "ULC_AUTOARRANGE"]:
                continue

            if "SORT" in styleName or "ALIGN" in styleName or "VIEWS" in styleName:
                continue

            if count == 0:
                tags = wx.ALL
            else:
                tags = wx.LEFT|wx.RIGHT|wx.BOTTOM

            check = wx.CheckBox(pnl, -1, styleName)
            stylesizer.Add(check, 0, tags, 3)

            if self.ulc.list.HasAGWFlag(styleVal):
                check.SetValue(1)
            else:
                check.SetValue(0)

            if styleName in ["ULC_HAS_VARIABLE_ROW_HEIGHT", "ULC_REPORT"]:
                check.SetValue(1)
                check.Enable(False)

            check.Bind(wx.EVT_CHECKBOX, self.OnCheckStyle)
            self.ulcstyles.append(check)
            count += 1

        sizera = wx.BoxSizer(wx.HORIZONTAL)
        self.checknormal = wx.CheckBox(pnl, -1, "Standard Colours")
        self.checknormal.Bind(wx.EVT_CHECKBOX, self.OnCheckNormal)
        sizera.Add(self.checknormal, 0, wx.ALL, 3)

        sizerb = wx.BoxSizer(wx.VERTICAL)
        self.checkgradient = wx.CheckBox(pnl, -1, "Gradient Theme")
        self.checkgradient.Bind(wx.EVT_CHECKBOX, self.OnCheckGradient)
        sizerb1 = wx.BoxSizer(wx.HORIZONTAL)
        sizerb1.Add((10, 0))
        self.radiohorizontal = wx.RadioButton(pnl, -1, "Horizontal", style=wx.RB_GROUP)
        self.radiohorizontal.Bind(wx.EVT_RADIOBUTTON, self.OnHorizontal)
        sizerb1.Add(self.radiohorizontal, 0, wx.TOP|wx.BOTTOM, 3)
        sizerb2 = wx.BoxSizer(wx.HORIZONTAL)
        sizerb2.Add((10, 0))
        self.radiovertical = wx.RadioButton(pnl, -1, "Vertical")
        self.radiovertical.Bind(wx.EVT_RADIOBUTTON, self.OnVertical)
        sizerb2.Add(self.radiovertical, 0, wx.BOTTOM, 3)
        sizerb3 = wx.BoxSizer(wx.HORIZONTAL)
        self.firstcolour = csel.ColourSelect(pnl, -1, "First Colour",
                                             self.ulc.list.GetFirstGradientColour())
        self.secondcolour = csel.ColourSelect(pnl, -1, "Second Colour",
                                              self.ulc.list.GetSecondGradientColour())
        self.firstcolour.Bind(csel.EVT_COLOURSELECT, self.OnFirstColour)
        self.secondcolour.Bind(csel.EVT_COLOURSELECT, self.OnSecondColour)
        sizerb3.Add(self.firstcolour, 0, wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 3)
        sizerb3.Add(self.secondcolour, 0, wx.LEFT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 3)
        sizerb.Add(self.checkgradient, 0, wx.ALL, 3)
        sizerb.Add(sizerb1, 0)
        sizerb.Add(sizerb2, 0)
        sizerb.Add(sizerb3, 0, wx.ALIGN_CENTER)

        self.checkvista = wx.CheckBox(pnl, -1, "Windows Vista Theme")
        self.checkvista.Bind(wx.EVT_CHECKBOX, self.OnVista)

        themessizer.Add(sizera, 0, wx.EXPAND)
        themessizer.Add(sizerb, 0, wx.EXPAND)
        themessizer.Add((0, 5))
        themessizer.Add(self.checkvista, 0, wx.EXPAND|wx.ALL, 3)

        mainsizer.Add(stylesizer, 0, wx.EXPAND|wx.ALL, 5)
        mainsizer.Add(themessizer, 0, wx.EXPAND|wx.ALL, 5)

        pnl.SetSizer(mainsizer)
        pnl.Fit()

        swsizer = wx.BoxSizer(wx.VERTICAL)
        swsizer.Add(pnl, 0, wx.EXPAND)
        self.leftpanel.SetSizer(swsizer)
        swsizer.Layout()
        swsizer.Fit(self.leftpanel)

        self.checknormal.SetValue(1)
        self.radiohorizontal.Enable(False)
        self.radiovertical.Enable(False)
        self.firstcolour.Enable(False)
        self.secondcolour.Enable(False)

        return mainsizer.CalcMin().width + wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)


    def OnCheckStyle(self, event):

        self.ulc.ChangeStyle(self.ulcstyles)
        event.Skip()


    def OnCheckNormal(self, event):

        self.radiohorizontal.Enable(False)
        self.radiovertical.Enable(False)
        self.firstcolour.Enable(False)
        self.secondcolour.Enable(False)
        self.checkgradient.SetValue(0)
        self.checkvista.SetValue(0)
        self.ulc.list.EnableSelectionGradient(False)
        self.ulc.list.EnableSelectionVista(False)
        event.Skip()


    def OnCheckGradient(self, event):

        self.radiohorizontal.Enable(True)
        self.radiovertical.Enable(True)
        self.firstcolour.Enable(True)
        self.secondcolour.Enable(True)
        self.checknormal.SetValue(0)
        self.checkvista.SetValue(0)
        self.ulc.list.SetGradientStyle(self.radiovertical.GetValue())
        self.ulc.list.EnableSelectionVista(False)
        self.ulc.list.EnableSelectionGradient(True)

        event.Skip()


    def OnHorizontal(self, event):

        self.ulc.list.SetGradientStyle(self.radiovertical.GetValue())
        event.Skip()


    def OnVertical(self, event):

        self.ulc.list.SetGradientStyle(self.radiovertical.GetValue())
        event.Skip()


    def OnFirstColour(self, event):

        col1 = event.GetValue()
        self.ulc.list.SetFirstGradientColour(wx.Colour(col1[0], col1[1], col1[2]))
        event.Skip()


    def OnSecondColour(self, event):

        col1 = event.GetValue()
        self.ulc.list.SetSecondGradientColour(wx.Colour(col1[0], col1[1], col1[2]))
        event.Skip()


    def OnVista(self, event):

        self.radiohorizontal.Enable(False)
        self.radiovertical.Enable(False)
        self.firstcolour.Enable(False)
        self.secondcolour.Enable(False)
        self.checknormal.SetValue(0)
        self.checkgradient.SetValue(0)
        self.ulc.list.EnableSelectionGradient(False)
        self.ulc.list.EnableSelectionVista(True)

        event.Skip()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    app = wx.App(0)
    frame = TestFrame(None, sys.stdout)
    frame.Show(True)
    app.MainLoop()


