#!/usr/bin/env python

###############################################################################
# Name: PlateButtonDemo.py                                                    #
# Purpose: PlateButton Test and Demo File                                     #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2007 Cody Precord <staff@editra.org>                         #
# Licence: wxWindows Licence                                                  #
###############################################################################

#-----------------------------------------------------------------------------#
# Imports
import os
import webbrowser
import wx
import wx.lib.scrolledpanel as scrolled
try:
    import wx.lib.platebtn as platebtn
except ImportError:
    import platebtn

#-----------------------------------------------------------------------------#

class TestPanel(scrolled.ScrolledPanel):
    def __init__(self, parent, log):
        self.log = log
        scrolled.ScrolledPanel.__init__(self, parent, size=(400, 400))

        # Layout
        self.__DoLayout()
        self.SetupScrolling()

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnToggleButton)
        self.Bind(wx.EVT_MENU, self.OnMenu)

    def __DoLayout(self):
        """Layout the panel"""
        # Make three different panels of buttons with different backgrounds
        # to test transparency and appearance of buttons under different use
        # cases
        p1 = wx.Panel(self)
        p2 = GradientPanel(self)
        p3 = wx.Panel(self)
        p3.SetBackgroundColour(wx.BLUE)

        self.__LayoutPanel(p1, "Default Background:")
        self.__LayoutPanel(p2, "Gradient Background:", exstyle=True)
        self.__LayoutPanel(p3, "Solid Background:")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddMany([(p1, 0, wx.EXPAND), (p2, 0, wx.EXPAND),
                       (p3, 0, wx.EXPAND)])
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(sizer, 1, wx.EXPAND)
        self.SetSizer(hsizer)
        self.SetAutoLayout(True)

    def __LayoutPanel(self, panel, label, exstyle=False):
        """Puts a set of controls in the panel
        @param panel: panel to layout
        @param label: panels title
        @param exstyle: Set the PB_STYLE_NOBG or not

        """
        # Bitmaps (32x32) and (16x16)
        devil = Devil.GetBitmap() # 32x32
        monkey = Monkey.GetBitmap() # 32x32
        address = Address.GetBitmap() # 16x16
        folder = Home.GetBitmap()
        bookmark = Book.GetBitmap() # 16x16

        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer1.Add((15, 15))
        hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer2.Add((15, 15))
        hsizer3 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer3.Add((15, 15))
        hsizer4 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer4.Add((15, 15))

        # Button Styles
        default = platebtn.PB_STYLE_DEFAULT
        square  = platebtn.PB_STYLE_SQUARE
        sqgrad  = platebtn.PB_STYLE_SQUARE | platebtn.PB_STYLE_GRADIENT
        gradient = platebtn.PB_STYLE_GRADIENT
        droparrow = platebtn.PB_STYLE_DROPARROW
        toggle = default | platebtn.PB_STYLE_TOGGLE

        # Create a number of different PlateButtons
        # Each button is created in the below loop by using the data set in this
        # lists tuple
        #        (bmp,   label,                Style,   Variant, Menu, Color, Enable)
        btype = [(None,  "Normal PlateButton", default, None,    None, None,  True),
                 (devil, "Normal w/Bitmap",    default, None,    None, None,  True),
                 (devil, "Disabled",           default, None,    None, None,  False),
                 (None,  "Normal w/Menu",      default, None,    True, None,  True),
                 (folder, "Home Folder",       default, None,    True, None,  True),
                 # Row 2
                 (None,  "Square PlateButton", square,  None,    None, None,  True),
                 (address, "Square/Bitmap",     square,  None,    None, None,  True),
                 (monkey, "Square/Gradient",   sqgrad,  None,    None, None,   True),
                 (address, "Square/Small",       square,  wx.WINDOW_VARIANT_SMALL, True, None, True),
                 (address, "Small Bitmap",      default, wx.WINDOW_VARIANT_SMALL, None, wx.Colour(33, 33, 33), True),
                 # Row 3
                 (devil, "Custom Color",       default, None,    None, wx.RED, True),
                 (monkey, "Gradient Highlight", gradient, None,  None, None,   True),
                 (monkey, "Custom Gradient",   gradient, None,   None, wx.Colour(245, 55, 245), True),
                 (None,  "Drop Arrow",                  droparrow, None,    None, None,   True),
                 (devil,  "",                  default, None,    None, None,   True),
                 (bookmark,  "",               default, None,    True, None,   True),
                 (monkey,  "",                 square,  None,    None, None,   True),
                 # Row 4
                 (None,  "Toggle PlateButton", toggle, None,    None, None,  True),
                 (devil, "Toggle w/Bitmap",    toggle, None,    None, None,  True),
                 (None,  "Toggle w/Menu",      toggle, None,    True, None,  True),
                 ]

        # Make and layout three rows of buttons in the panel
        for btn in btype:
            if exstyle:
                # With this style flag set the button can appear transparent on
                # on top of a background that is not solid in color, such as the
                # gradient panel in this demo.
                #
                # Note: This flag only has affect on wxMSW and should only be
                #       set when the background is not a solid color. On wxMac
                #       it is a no-op as this type of transparency is achieved
                #       without any help needed. On wxGtk it doesn't hurt to
                #       set but also unfortunatly doesn't help at all.
                bstyle = btn[2] | platebtn.PB_STYLE_NOBG
            else:
                bstyle = btn[2]

            if btype.index(btn) < 5:
                tsizer = hsizer1
            elif btype.index(btn) < 10:
                tsizer = hsizer2
            elif btype.index(btn) < 17:
                tsizer = hsizer3
            else:
                tsizer = hsizer4

            tbtn = platebtn.PlateButton(panel, wx.ID_ANY, btn[1], btn[0], style=bstyle)

            # Set a custom window size variant?
            if btn[3] is not None:
                tbtn.SetWindowVariant(btn[3])

            # Make a menu for the button?
            if btn[4] is not None:
                menu = wx.Menu()
                if btn[0] is not None and btn[0] == folder:
                    for fname in os.listdir(wx.GetHomeDir()):
                        if not fname.startswith('.'):
                            menu.Append(wx.NewId(), fname)
                elif btn[0] is not None and btn[0] == bookmark:
                    for url in ['http://wxpython.org', 'http://slashdot.org',
                                'http://editra.org', 'http://xkcd.com']:
                        menu.Append(wx.NewId(), url, "Open %s in your browser" % url)
                else:
                    menu.Append(wx.NewId(), "Menu Item 1")
                    menu.Append(wx.NewId(), "Menu Item 2")
                    menu.Append(wx.NewId(), "Menu Item 3")
                tbtn.SetMenu(menu)

            # Set a custom colour?
            if btn[5] is not None:
                tbtn.SetPressColor(btn[5])

            if btn[2] == droparrow:

                tbtn.Bind(platebtn.EVT_PLATEBTN_DROPARROW_PRESSED, self.OnDropArrowPressed)

            # Enable/Disable button state
            tbtn.Enable(btn[6])

            tsizer.AddMany([(tbtn, 0, wx.ALIGN_CENTER), ((10, 10))])

        txt_sz = wx.BoxSizer(wx.HORIZONTAL)
        txt_sz.AddMany([((5, 5)), (wx.StaticText(panel, label=label), 0, wx.ALIGN_LEFT)])
        vsizer.AddMany([((10, 10)),
                        (txt_sz, 0, wx.ALIGN_LEFT),
                        ((10, 10)), (hsizer1, 0, wx.EXPAND), ((10, 10)),
                        (hsizer2, 0, wx.EXPAND), ((10, 10)),
                        (hsizer3, 0, wx.EXPAND), ((10, 10)),
                        (hsizer4, 0, wx.EXPAND), ((10, 10))])
        panel.SetSizer(vsizer)

    def OnDropArrowPressed(self, evt):
        self.log.write("DROPARROW PRESSED")

    def OnButton(self, evt):
        self.log.write("BUTTON CLICKED: Id: %d, Label: %s" % \
                       (evt.GetId(), evt.GetEventObject().LabelText))

    def OnToggleButton(self, evt):
        self.log.write("TOGGLE BUTTON CLICKED: Id: %d, Label: %s, Pressed: %s" % \
                       (evt.GetId(), evt.GetEventObject().LabelText,
                        evt.GetEventObject().IsPressed()))

    def OnChildFocus(self, evt):
        """Override ScrolledPanel.OnChildFocus to prevent erratic
        scrolling on wxMac.

        """
        if wx.Platform != '__WXMAC__':
            evt.Skip()

        child = evt.GetWindow()
        self.ScrollChildIntoView(child)

    def OnMenu(self, evt):
        """Events from button menus"""
        self.log.write("MENU SELECTED: %d" % evt.GetId())
        e_obj = evt.GetEventObject()
        mitem = e_obj.FindItemById(evt.GetId())
        if mitem != wx.NOT_FOUND:
            label = mitem.GetItemLabel()
            if label.startswith('http://'):
                webbrowser.open(label, True)

#-----------------------------------------------------------------------------#

class GradientPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        col1 = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DSHADOW)
        col2 = platebtn.AdjustColour(col1, -90)
        col1 = platebtn.AdjustColour(col1, 90)
        rect = self.GetClientRect()
        grad = gc.CreateLinearGradientBrush(0, 1, 0, rect.height - 1, col2, col1)

        pen_col = tuple([min(190, x) for x in platebtn.AdjustColour(col1, -60)])
        gc.SetPen(gc.CreatePen(wx.Pen(pen_col, 1)))
        gc.SetBrush(grad)
        gc.DrawRectangle(0, 1, rect.width - 0.5, rect.height - 0.5)

        evt.Skip()
#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

class TestLog:
    def __init__(self):
        pass

    def write(self, msg):
        print(msg)

#----------------------------------------------------------------------

overview = platebtn.__doc__

#----------------------------------------------------------------------
# Icon Data
# All icons from the Tango Icon Set
from wx.lib.embeddedimage import PyEmbeddedImage

Book = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAkdJ"
    b"REFUOI2VkslrU1EUh787vJeXNNpMGA01DlECrd0UWrD+A06oIIoLwY24FwQRNIu6EBeKy4Jb"
    b"XRS6dEK0WrC2XSgFFZq0RUoHmg4WYslrxuuiGpJWKv4295zLOd/vnssR/FbX8ZvXQTzAGPPn"
    b"ziAMgJAie//ifKL7ZC6pjOwylJc01WGiHUsaoLe3tz+bzZ6fmJwisxQTd25d3iAIwMDde09i"
    b"L76W3GhbjL37jyLtfaysvP0QXf52VQF0dnb2pVIpdvj9DAx/JxiN8Dk9x+TMMm6hxMT4NDeu"
    b"HaG97RB281ksZz9Se+OyNDqvqVMul6NcyrOyukp2cRUAR1cpl/LkfpYpV8voiotQkmJ+Bo+U"
    b"OVkPqFQqVErrFAsuBXeNortGad2lXHT5Ml5gZk5QyQ9g8q+ZnR6magqfGgAAQtlobWPZHpTl"
    b"QWkLIS32xOKEdp/ArbYjrBijYxaW+2OsASCEQFteLMeH7fjxeJuwHC/a8jI3O0c6M4URMbA7"
    b"mF9sQhwYXNebXyClQkqF0hYASllIpWlpaSGZTIIQCKExRgDQALBtuxbvCvmpVmsrgeNVm702"
    b"DOsTn88HgDHw8c0IIwOjtb1q8jUjhNge4PF4AHj/aoh4bCcH4wHevRzCGMPCwgLpdHoLoGEE"
    b"x3EAuHLhGJfOdSOlpP/ZCI+fDtLa2koikdgeEIlEeHj7NEopMpkMQgjaDwd5lDpDMBgE2DJG"
    b"AyAQCBAIBBBC1Arrz7/9QQMgFAptKfiXNEA4HH7e09Nz6n8aw+FwH8AvVXjA30OIWrcAAAAA"
    b"SUVORK5CYII=")

Address = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAmtJ"
    b"REFUOI19kstLlFEYxn/nfN+ZizPOeBnHS1OklmQSFVjRH9CiTUKbIKRl4V8QuFBwIUTtgqBF"
    b"u3BfuW0XtAhsYWk6BqOZl7mgc/+c73JafKmZ1gNnc+D9ned5ziu0fqievep/Hg83HpXqAVa2"
    b"2inXgmgE/9HUzPToJICYfvn0xe0r22MXL9wEM0WusEQ6N8DmbjMaiZQ+aB9XtRqUNmd5cH2c"
    b"eMfIY1NJPTbQP4QZuQUiRDJhkC/OsZrrI7haQdX38JRBpStBPRGnsy1CCYh3jFDMvXliWrbC"
    b"A/AskBLX3sauS2KrWQo9Z2hEmzCtPeKZTVxlQFuEpmDjIIu5stlGrtxGB+9xXYHjZimmY+wk"
    b"ezAaNsn5FbQQ7JxLEfuRhd5OwgH7EGC7BmU9jFXcIp9dIpG8RimTYW8wSmIhQymVJLpVwAkF"
    b"UDULgI/fLGy1zNe5JiRAQIWxvG62iuepub14tkQLgXRctGGAEATLNZxw4Nh3SAAh/I61MPyr"
    b"SAhVtbBam/3XA4rY2jal050AeEQPIxzl+SCvt4tY+ifFs9044SCIozsRyijuzsDlxZoP0GjQ"
    b"kGyP+046WijtOcTWs6hqHTegyA/1nbhRvgMNSpm0tESxbIfO1gixcBAGTh34ih/x+BegUq3z"
    b"bvYDptR42j+OoxFSEFAGQggE4LoemfW811Ury++LiwD3TIAv8yvcGIwcrO1JklJSEy0sFxpy"
    b"rfcSw7/NmAC7lSp9yWZSqZ5jg+KPAhfSGyd2MPUpnZ9w6jVvI9+QoZDCsZ0jgfcRjutx52q7"
    b"fvu5cEAVgLw//noSmPin/xM0Mz0qAH4B9vTxRRZgeg8AAAAASUVORK5CYII=")

Home = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAABqNJ"
    b"REFUWIXVl2uMlOUVx3/P817mtjN77Sxy2WFZroLQBbEtyYaAbSG1Ng1JJVZrQ6Jp1ARMI0m/"
    b"mX7wi58MprGXBARTUW6JtiZuJSUFSXBrEQxWQcCVhWVhWYady84777zP8/TDXNhdhmvih57k"
    b"Td6Z97zn/M///M+ZZ+D/2d6R8sW/CjG6E2bcawxxLy/tAhfL2pFsa1s7taEhcay/f7Ck1A+f"
    b"gC+/dQA7IBm2rA/ndnXN7Zw6NVwcGSGTy/HpwMAlPwh+9gT03U08eTfOb8LSqOt++uDSpYs6"
    b"Z84MIyUGiLgu3R0d7SHHef8t+NG3AmCXlL9KxGL/6OnpmdqWTEqkBMsCITBAyHHoTqXaQq77"
    b"9jtSPn6ncW/bgpdA3m9Zr7Umk79ctnx5kyUlKAVao69dQ6fTFJRCAQYItObEwMBVz/d/v17r"
    b"LbeLb92yamhMWtb+rnnz1i5+6KGEtCruQqBHRjDpNCWlCFkWyhiUMSAEbYlEJON53/+51ond"
    b"xvzznhjYDnOjtt3bvWLF9PZUykZrUAoTBOhz5whGRzmeHuHi5SssS6WYEo0ypjWeMRhAA2eH"
    b"hjKZfH7PL5R6WpQJusHqauAty3okEYt91PPoozPb58yxsSyQEqMU+uxZxq5e5eORyzS+sIkH"
    b"jx7lm8YYZ3JZolISrmgCY+hsb0+0JBKP7bbtdw+AfUcM7LLtlxKtrZu+t3ZtsxOJlKvWGpPJ"
    b"oE6e5Go2y+eFHKk/vE7kgcUopRBaM/S7F7GOHmdhPEERyCiFoVz2UDpdGE6n/5NWas1vYKwu"
    b"gG0Qjkm5d8a8eT2LVq+Oi/Fiu3QJdeoU53I5LkTCdL2xHdnaShAESCmRUqK1ZuSPr5PbuZPu"
    b"xiaUEFxTCg0YY7iWzRYvXLlyMq/Uyg1wrZrXAngTpkcs6/CSnp5lc1aujFbHCyHQ/f0Ep07x"
    b"eS5H7v4FzN6+AxmPo5QiEonQ0tJCLBZDKUV46TKcjhl80dvLFNshatt4xqABNxSyo6FQqzc2"
    b"9thPjNn9LuRqDLwt5WDPunVTmrq6yoxojQkC1Gef4Q0McCybpfmpp2h/7jmUUmiticVihMPh"
    b"Ce0rFAoUCgW8Eyc48+yzPBAK0RAKMawUpYo4i56nv7l48YJSatXjcEYC2FIWm2bPFlgWWBZG"
    b"KYK+PjJff01fJsP0V15hyvPPY4zBsiwaGxtxXRetde1SSuG6Lg0NDcSWLGH+3r2ckJIrhQJJ"
    b"28atiNMJhWTntGkzLMv618QpqGw2k88THDzI0PnzHNOahXv20LhqFcYYbNsmGo1WSJqYvHov"
    b"hCASiRCeNo1F773HuWSS/nyepG0TqYCQjoMtpblhDM2lS5QOHODU5cucu+8+unt7Cc+aBYDj"
    b"ODiOMyHx5OTjL8dxcBobWbBrF/nly/lvNst3LIu4lEhxffhqANTp0xQPHeLI4CDB6tUs3rcP"
    b"GY9jjEFKiRDijpJPZkM6DrNefZXwk0/y8cgIzVLSLK/XbQMEWoeHjhzhZDqdHVu/Prb05Zel"
    b"1hpMeXkZYzBm4iKrfhZCYNs2QogbfKp+SimmbdzIwdOnS8H+/cH8RCJSVKqhBqCo9epPBgYO"
    b"d27Y8Nt9zc3bHrYsgiBg//4PyY/la4kmWzQSY82aNWzZ8hq+X7zhOYDjhnhh00Z832d49uyg"
    b"8/DhH38yOPj3ktYragB+DV9gTAtbt7J58+ZtNVWHXL46c3JCQCFEDcyC+QsxxuD7RVTqEVzH"
    b"wrElSmn8kqZYCuDCBxhjKJVKSCkL6y5e/AhoukED463aw44ZHdi2XROg67q1e8dxSHWk0FpX"
    b"gIEUYAlRFtk4wqptMHV6VPcHwhiD1ppUKoVt13UBoK2trQZgzAso+oqxYsBovkgmX6RQVPwg"
    b"Wi6osrb9uwJg2XatElG5kYxhi358Mx8ENQD//nKoPsrodUaB0uTHt2xBNbGgQqkAR3zFT1f8"
    b"DUtkgfrKr2dKKYBg8vc3ZUApBcZMVL8An++y+9CiWmvKS8dlVdPxuoltp7yyS6USQgjvrgDY"
    b"jkO5+Ikj6DhOGY8Az/N45pmn645pNVaxWKzuktsyEKpWpbVGClk38HhAvu/j+9e1Va8lUkpK"
    b"pRJBEGigjfJ5IJgMwAVagcDzPDsej0+Y+ZtZPB6/5fMqoOHhYXzfV8CUSt7LgB4PwAbc0dHR"
    b"N7Zu3brBGHPLEzPAn//0l9u5jDevr69vJxCmXKyAiWdCQZmBViBRcbr5Erg78ymfvgrAKHAe"
    b"8CYDqJoDRCpI7+nPax0zlHeAV7lqQvkfoK5c5SC5ZcEAAAAASUVORK5CYII=")

Monkey = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAACDhJ"
    b"REFUWIXtlmuMXVUVgL+99zn33HvnPmbmDtOZYabTKXSGmdAWi6JAi6U1GgMN2qAIgYgaMAKJ"
    b"4g8jRhN+GGNMTESDxogQEhtjIiAYqT+0pfZhkdBSSqedFqbTofN+3Lnv89zbH/dOGNtiUjXR"
    b"H65kZWc/17fWXmftA/+X/7KIy1m8eSg1JNB3xIS+UxvRE2nRDKCkWZLCvOsb+VuDfPHAcHn4"
    b"Pwqwub9pg23rJ1PJ1KYN67qsdb1dsZZMikQiAUCtWiVfLHNmfNI/dnoyqNYqR/1APnzgdOXN"
    b"fxtg6zWJh51E4gcfv3F9/Jq+LlmdG6OanyCoLmGCGgBWLImVzJJs7SbZtoaTo+/q3QePu4Hn"
    b"feOVU7Un/2WAW4fi32zONn/77ttubgoWzpEfPw7aRwmQDRWAAbSpK5ZDa+91iHQHu36/v1Ks"
    b"VL67d9j9/mUD3DLQtL4pLvffv3N7dv7sEZbKFdxIYjAkbEkyLJBRPlJAKYpRUllqgUYiiCtN"
    b"W7aZ5tVD/PK5PYWax5a/jFSOXxbAtsHE8O23XDvoBEvMlYps2fwxBoc2oKwY09MT7NmzG7M0"
    b"Xj+geTXbtt1GZ+eVhFHIqVNvsX/vbjraWikHNn84dPrknpO1ofcFuGkgl46p6o+M4W6MUFLy"
    b"11Tc/sB9OzZnRk68xu07PktXRwdRdRETBQhlo+0MT+96FoAv3ns/0i9iQg+hLKzUFUzNzfPS"
    b"C7sYWv9hnn5+T7EamKNacyPCRELwaz9Kfu3QyEJJAfR3ij1dzeoTH+qLJVpTUpU9VvddmYvH"
    b"TIVMppkbNl1PsDSFCV1M6GN8Fxm5XDO0if6rB0iEBbRbwEQhJvTRboFsayeTM9OU8guEBqfm"
    b"easHu2xroMOyQ82gFwTbzs4GT6tb+pOfbM+Ihwa7nNTpWcnQVWuZz1dF96pWjF9k44braYkL"
    b"tFfChAEm8jGRj/arWGEVJ6rU56IAowOMDiGKAIN0UoyOjqBiTcwXamLT+iFOnS/Ql1NW1Quz"
    b"uSb7mIzHeWxjj5U9u6j41hd2sPPmIXo7WjCA0YZkwkG7JUzgYoxmMu/xzJ/PMlUCYcUQlsNU"
    b"GZ7Ze47JQoSQFsZotFsimUyitQZgoDvHzi3r+c5D93K+aLGxx8rG4zwmo4iBQAuG1vaQiQlM"
    b"FNDelqNcqSGkwPUCUDYylkI6KR78yX4e3/U3HnjiFaSTRjppHnjiFR7/1as8+ON9SKe+TtpJ"
    b"/AikUpSqLu25FrRfI2HBxsF1hFoQRQxIQGhtsASY0EfGkvT39TBb9InFU0zNzmI15ZBOEzLW"
    b"xNhMAYCxmUIdIJ5mbHp5rFgHjTVhpduZmJrESaSYWqyyrrcHE3iY0MdSCq0NgJCWEmdiSnBi"
    b"9Dyu6yKUw5qeKzk3tUgm28bJkWHCeBvCSSOdFI9+bivppMOj92xHOmmUk+LRe7bXx+6+te59"
    b"PINOdXLixBuk0i1MzJfp6+4AKQmCgDdPnsFWAkuJM2LrYOKOzmb17Np2JztTVmy/YSMvHThB"
    b"SyZGT4sg197NHZ+6F1OeRUgLoWyEskEqhJAs10JjNOiokYwRKtvN8889Q356lNHpGnPFgJ2b"
    b"+zk8PE7Ccjk/7xamlqLPq7H5cGRV1v6MJGrtbtbW0bcnWSi4bLo6RyqVZvPWT/PG0ddZKFao"
    b"+JpIKFAOltOEFUsirBghinItIF+sMDEzz9vnJjg5cpLrb7iVmakxMnHD6fEFphcXySU95pYC"
    b"b3LJjOwdrn5dAHxkKNOaJPxZoNmpJOq6vmaRa4I77/oyuUySwA+YWaoys1hkdnGJ+XyRhaUi"
    b"rusSaY1tW7Rks7TnWljV1kpXWwuduQxO3CFf9fnNsz9kruBzbLxiIk1kS56vYn3l8HBx0QI4"
    b"PFxcBO766EexzGxitiWdaPH9Ei1tHRg3j+3EWd3dQm/fVUgrjrDjCMupX4eQGKProQ89TOCi"
    b"Q7fRerRc0Y0XBLRmmjCmvCRX1dr37CNcLsVyZV3et49QQ0JKCcYglIWQCiFV/c6lArWcBw7S"
    b"Tta/BDuJUHUgGnuQCqksEAKMQSqJhsS+FcYvAgBQMFeuuVjKIj8/jbATYExDaagBdN1zHdYT"
    b"EH3RGmknWZybwLJsKjUfBXMX2rsIAMyL0wuVINRwaP9urGRr3Qsd1o1F/nuh9spor4T2yvVK"
    b"GXr1eR0gAJVu49De36E1TOUrAZgXL+HwP0rPKuutUiX8Uk97OlFYmsVSkp7+TRD69TrPcjSi"
    b"ej/034MKPUzkIaSFne3gtYMvc+z1/WgR4/hYsRhJ7hufC4v/FGB8Liz25iy9WPZu7GhNxd4d"
    b"O8X83AS9/ZtwUs1gDEZHjUep8TjpsJEzNirZjGckf3zhKY4c/hNGORx5J192Pf29/afc3Rfa"
    b"u9QPiQ3ENw8kfpFO2DvW96aTNh5KWVw1cC3XXreZ9q41NKVzWI4DCMIwoFpcZG56nLeOHuDM"
    b"8BGiKCTA4fi5UrVY9V8+eNp9BHABr9FeEiDe0AQQ/+Ba55F0wnqoO5ewenJxy0QutpIIKYl0"
    b"VE+2xilKKrTRhKFGqjjn8144PlcNC5XgqSNj/s8bRl2g1mirgLkQILFC40CiM6uuXtNuf9VW"
    b"8qbWtBO1pa1EOm7hOArV2B0Z8PyIshsxVwzcxZKn/DB6dXQ2+OlsUY+uMLoMUAUql4qAABwg"
    b"2QBwlttMk7qip9nakkmKLUqxTiJaNSJW32QCg1kMQ/NOocrB8/nwUKkWzTfCvazLxsuN/vvm"
    b"wLIoILbiWmKAtUKXX6LlM+rFAUIgAoIVXruA35i/yOPLEXGB4WVdzga9AsRc6oD/Ofk7fswD"
    b"nMQUbKYAAAAASUVORK5CYII=")

Devil = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAABrpJ"
    b"REFUWIXtlluMlVcVx3/7u57LzLkMc5gbw2UovFRupQ1INdRkkkrIPDRpLSFREqk8oFKrPhmR"
    b"oEkfNLFJ39SQkrZGJGRMarCpVWmlLa2OCjOtpVBmgJnOfc79zHf/tg/nO5PTEQEbE1/6T/45"
    b"315n7b3+e+21sjd8iv8zRPPgtKKc9aV8UArxfT0Mf/4lcI+BocMXNME+BT4XQi6UtCqCigJz"
    b"oeQNH055cO44uKfB8BTlGwKOqvDW42G49+4FmGrx4Z9uSt98J+988JupwmzFe6mi8NjKroS6"
    b"bmOqNbcqKWKtOnpMxbMCrIrH3ERNXr9SrsxOLwatIYMrs8bAvY91Z7q3ZIyz37xU2h/KzO0E"
    b"qM2DR6QwWztzu9ZoG81W22ipFQr39XQl4jv2dJlpLKHnC4iZBeTEHCyUMGoW6bQm+j7TbspJ"
    b"J55NZ+974KEHkh2dveqNkXln+r35Hw9K+fpdZ+AFSKmKMvX5desSLYZB1XG4MH6d7dtBjYNq"
    b"gtDqs2QAoQuhDUFNMjQs2L2uj5iuU3Vdzo+OLi5K2fkEVG4nQGse3IDWFVJyZWGOvkwbw9OT"
    b"rO4FrQW0JKgxgdCbBDgQGBIUQU8nDH00zqbObq7lFyiDnIcUdxCgND4kCB3ObtycM4uexd8n"
    b"b7Kyw6NrLWgtAq1VoKVBzwqMrEDPgJ6K/ktCzxrIZFyGJm5Q8izWb8zGdDgrl2V5OZZqwIB9"
    b"3e3xL9+7tT3eVsjT2SVJrRR4cfj6JcmTb4f88SPYuUHQ2S5wEHz1lZAnL4Scm4dtGUFvAlYY"
    b"kJYh2b52pVhyEr+zg7E/wbu3zcAx0DR4ZuuWlSnn0hRIiVDr5/3sqKQ3BdcOaRy4X/Dt34fo"
    b"GcFP/hqyOiu4ckBl/3rB0ashiibq85A478+zeWNbSoNnji076mYIgB9Bf097/Mxnt3aknXeu"
    b"o2cEepZ6qrMCLQtmZNMyAi0OXgGcgsQvSrwC2HlJUASvIHELEq8Ise1dXLicL02VnEePwh+i"
    b"o44jxBmggpRPKwAm7Ovtbkn5ExVkWPdCggxBhhIR1ItOehBa4JchdCT4kT0ARYKUEtmYK8Gf"
    b"rtHTnkiZsE+CKoX4IfAEMA4EwEgjNbuzKxLCvzgTLSiRvkD6IN16uwW2RGgCGUhQIptVb8PQ"
    b"q1N61OcE9eX9gk3bPW0C2O3BTl3KUQEnpZQGoAmQGkAIuVhMZcSGMNBRanGCqXKUik+OlJak"
    b"V1cIIVeA6Tg8DpwU4FJnvTgCSGuGigxCNgwOkuzoIJHLMTo6yrZt2zBNE9M0UdV604yMjLBp"
    b"06aPBQvDkKGhIfr6+rBtm9nz57l++DCGJggg3QHXJiA7Df2dUT1A1AUqlLxFD+l56D09qKkU"
    b"ALqu33Jnmnbrom72N7q68F0Hz/ZRoQSQhyNVeHYCdn1MgAJzds1Da0niTU7eMdDdCPALBTRF"
    b"wbIDFJgD2AyFCnytDL/9EDYsCQBeX5i3ZFxXsC9fvuWCdyOg2W5duYKphCyUHAksXUjb4M0S"
    b"/KoEJ5cEOHBqYqZWzrVr5J9//n+SgfkXXySb0pgs2GUHTjX7VeFEFXa9AesVAB9eWyg5lpbQ"
    b"8D+8SnVo6BNloOFfHR7GHRtFM1UKNc/y4bVmvzJkK0ANQgXgOPg+PPXutWJ59eoEY0eO4C0s"
    b"/MdAjW64lQCvVOKfBw+yqk3lvclq2YenjoMPcBrUX8BABV4ow5sPw9jSbfg9+PVsxR0r2H6Q"
    b"M1yG9+4lnJ39rzIgy2X+0t9Pyi2Td8Nw0vKtSbj/u/CzH8Cr12CmDC+VYbYK+6DpOhYgyzBw"
    b"8UapoKQM2pVFRvbs4caJE8gwvKOAm6dO8daOHbRU5tCTGv+YqSnXocOC75Tg0Dz0z8L4NHzr"
    b"Kuw8BBNR3CUYQOwg7LhHcGZrbyqZM1V1fMZHJpKsO3CAnoEBkmvXEiYSqJZFbXycqZdfZuy5"
    b"5wjyC/SkBbO+5OJMTV6GiSpMSphwYXgO3v4bfABYgB3RbQhQgHiDD0FfP5zMpYzOzd2tMcX2"
    b"KRY9bHRc18N1HHTTwNB1YoFLulVDmiqX5hbdmZqX/yU8fbW+w0YwaxkbtlpzBmJNImJJaPkK"
    b"7F8FhzNJXV2TMuIrErowNAVdUXD9ANcLmK/58mbVtYuWL0dgcBBe9WCxaZfWLb4t6k81f/lz"
    b"SQcSgBkJMtPQ8kV4cC3saYEtCmQExCXYAZSK8P5l+PM5uGSBA3gRGxeO00QLqEW/cnkNNENE"
    b"NdEQYkTitIhqdGwiYvQKIKR+z/sR3aYdu5Ht3wLdLRoBlSY2oyGgwYaoT3Fb/At4CANJRbmY"
    b"kwAAAABJRU5ErkJggg==")


#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    try:
        import sys
        import run
    except ImportError:
        app = wx.App(False)
        frame = wx.Frame(None, title="PlateButton Test")
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(TestPanel(frame, TestLog()), 1, wx.EXPAND)
        frame.CreateStatusBar()
        frame.SetSizer(sizer)
        frame.SetInitialSize()
        frame.Show()
        app.MainLoop()
    else:
        run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
