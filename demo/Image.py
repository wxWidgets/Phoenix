#!/usr/bin/env python

import os
from collections import OrderedDict

import wx
import wx.lib.scrolledpanel as scrolled
from Main import opj

# IMG_QUALITY = wx.IMAGE_QUALITY_NORMAL
IMG_QUALITY = wx.IMAGE_QUALITY_HIGH

supportedBitmapTypes = OrderedDict([
(wx.BITMAP_TYPE_ANI  , 'BITMAP_TYPE_ANI:  Load a Windows animated cursor file (ANI).'),
(wx.BITMAP_TYPE_BMP  , 'BITMAP_TYPE_BMP:  Load a Windows bitmap file.'),
(wx.BITMAP_TYPE_CUR  , 'BITMAP_TYPE_CUR:  Load a Windows cursor file (CUR).'),
(wx.BITMAP_TYPE_GIF  , 'BITMAP_TYPE_GIF:  Load a GIF bitmap file.'),
(wx.BITMAP_TYPE_ICO  , 'BITMAP_TYPE_ICO:  Load a Windows icon file (ICO).'),
(wx.BITMAP_TYPE_JPEG , 'BITMAP_TYPE_JPEG: Load a JPEG bitmap file.'),
(wx.BITMAP_TYPE_PCX  , 'BITMAP_TYPE_PCX:  Load a PCX bitmap file.'),
(wx.BITMAP_TYPE_PNG  , 'BITMAP_TYPE_PNG:  Load a PNG bitmap file.'),
(wx.BITMAP_TYPE_PNM  , 'BITMAP_TYPE_PNM:  Load a PNM bitmap file.'),
(wx.BITMAP_TYPE_TGA  , 'BITMAP_TYPE_TGA:  Load a TGA bitmap file.'),
(wx.BITMAP_TYPE_TIFF , 'BITMAP_TYPE_TIFF: Load a TIFF bitmap file.'),
(wx.BITMAP_TYPE_XPM  , 'BITMAP_TYPE_XPM:  Load a XPM bitmap file.'),
(wx.BITMAP_TYPE_ANY  , 'BITMAP_TYPE_ANY:  Will try to autodetect the format.'),
])

description = """\
This sample demonstrates some of the capabilities of the wx.Image class, both the
variety of source image formats, and some of the operations that can be performed
on an image object.
"""

#----------------------------------------------------------------------

class ImagePanel(scrolled.ScrolledPanel):
    defBackgroundColour = '#FFBB66'

    def __init__(self, parent, id=wx.ID_ANY):
        scrolled.ScrolledPanel.__init__(self, parent, id)
        # self.log = log
        # self.SetDoubleBuffered(True)

        hdrFont = wx.Font(18, wx.FONTFAMILY_DEFAULT,
                              wx.FONTSTYLE_NORMAL,
                              wx.FONTWEIGHT_BOLD)

        StatText1 = wx.StaticText(self, wx.ID_ANY, 'wx.Image',)
        StatText1.SetFont(wx.Font(wx.FontInfo(24).Bold()))

        StatText2 = wx.StaticText(self, wx.ID_ANY, 'Supported Bitmap Types')
        StatText2.SetFont(hdrFont)

        vsizer0 = wx.BoxSizer(wx.VERTICAL)
        vsizer0.Add(StatText1, 0, wx.ALL|wx.ALIGN_CENTER, 10)
        vsizer0.Add(wx.StaticText(self, wx.ID_ANY, description),
                    0, wx.LEFT|wx.BOTTOM, 10)
        vsizer0.Add(StatText2, 0, wx.ALL, 10)

        fgsizer1 = wx.FlexGridSizer(cols=2, vgap=10, hgap=10)
        fgsizer1.AddGrowableCol(0)
        bmp = wx.Image(opj('bitmaps/image.bmp'), wx.BITMAP_TYPE_BMP)
        gif = wx.Image(opj('bitmaps/image.gif'), wx.BITMAP_TYPE_GIF)
        png = wx.Image(opj('bitmaps/image.png'), wx.BITMAP_TYPE_PNG)
        jpg = wx.Image(opj('bitmaps/image.jpg'), wx.BITMAP_TYPE_JPEG)
        ico = wx.Image(opj('bitmaps/image.ico'), wx.BITMAP_TYPE_ICO)
        tif = wx.Image(opj('bitmaps/image.tif'), wx.BITMAP_TYPE_TIF)
        dict = OrderedDict([
            (bmp, 'bmp\n*.bmp;*rle;*dib'),
            (gif, 'gif\n*.gif'),
            (png, 'png\n*.png'),
            (jpg, 'jpg\n*.jpg;*.jpeg;*.jpe'),
            (ico, 'ico\n*.ico'),
            (tif, 'tif\n*.tif;*.tiff'),
            ])
        for bmpType, tip in list(dict.items()):
            statBmp = wx.StaticBitmap(self, wx.ID_ANY, bmpType.ConvertToBitmap())
            type = bmpType.GetType()
            if type in supportedBitmapTypes:
                typeStr = 'wx.' + supportedBitmapTypes[type][:supportedBitmapTypes[type].find(':')]
            statText = wx.StaticText(self, -1, typeStr)
            fgsizer1.Add(statText)
            fgsizer1.Add(statBmp)

        vsizer0.Add(fgsizer1, 0, wx.LEFT, 25)
        vsizer0.AddSpacer(35)

        StatText3 = wx.StaticText(self, wx.ID_ANY, 'Basic Image Manipulation Operations')
        StatText3.SetFont(hdrFont)
        vsizer0.Add(StatText3, 0, wx.LEFT|wx.BOTTOM, 10)


        self.imgPath = 'bitmaps/image.png'
        self.imgType = wx.BITMAP_TYPE_ANY
        self.fgsizer2 = fgsizer2 = wx.FlexGridSizer(cols=2, vgap=10, hgap=10)
        fgsizer2.AddGrowableCol(0)

        self.colorbutton = wx.ColourPickerCtrl(self, wx.ID_ANY,
                                               size=(175, -1),
                                               style=wx.CLRP_USE_TEXTCTRL)
        self.colorbutton.Bind(wx.EVT_COLOURPICKER_CHANGED, self.ChangePanelColor)
        vsizer1 = wx.BoxSizer(wx.VERTICAL)
        vsizer1.Add(wx.StaticText(self, -1, "Panel colour:"))
        vsizer1.Add(self.colorbutton, 0, wx.LEFT, 15)
        fgsizer2.Add(vsizer1)


        self.SetBackgroundColour(self.defBackgroundColour)
        self.colorbutton.SetColour(self.defBackgroundColour)
        self.colorbutton.SetToolTip('Change Panel Color')

        self.filebutton = wx.FilePickerCtrl(self, wx.ID_ANY,
                                            path=os.path.abspath(opj(self.imgPath)),
                                            message='',
                                            wildcard=wx.Image.GetImageExtWildcard(),
                                            style=wx.FLP_OPEN
                                                | wx.FLP_FILE_MUST_EXIST
                                                | wx.FLP_USE_TEXTCTRL
                                                | wx.FLP_CHANGE_DIR
                                                # | wx.FLP_SMALL
                                                )
        self.filebutton.SetToolTip('Browse for a image to preview modifications')
        self.filebutton.Bind(wx.EVT_FILEPICKER_CHANGED, self.ChangeModdedImages)
        vsizer2 = wx.BoxSizer(wx.VERTICAL)
        vsizer2.Add(wx.StaticText(self, -1, "Load test image:"))
        vsizer2.Add(self.filebutton, 0, wx.EXPAND|wx.LEFT, 15)
        fgsizer2.Add(vsizer2, 0, wx.EXPAND)

        fgsizer2.AddSpacer(10)
        fgsizer2.AddSpacer(10)

        def getImg():
            # Start with a fresh copy of the image to mod.
            path = opj(self.imgPath)
            type = self.imgType
            return wx.Image(path, type)

        self.allModdedStatBmps = []
        self.img = getImg()
        self.imgWidth = getImg().GetWidth()
        self.imgHeight = getImg().GetHeight()
        self.imgCenterPt = wx.Point(self.imgWidth//2, self.imgHeight//2)

        imgBmp = wx.StaticBitmap(self, wx.ID_ANY, self.img.ConvertToBitmap())
        fgsizer2.Add(wx.StaticText(self, -1, "Original test image:"))
        fgsizer2.Add(imgBmp)
        self.allModdedStatBmps.append(imgBmp)

        self.DoImageMods()

        dict = OrderedDict([
            (self.greyscale  , 'img.ConvertToGreyscale()'),
            (self.disabled   , 'img.ConvertToDisabled()'),
            (self.mono       , 'img.ConvertToMono(r=255, g=255, b=255)'),
            (self.mask       , 'img.SetMaskColour(\n\tred=255, green=255, blue=255)'),
            (self.blur       , 'img.Blur(blurRadius=3)'),
            (self.blurH      , 'img.BlurHorizontal(blurRadius=3)'),
            (self.blurV      , 'img.BlurVertical(blurRadius=3)'),
            (self.mirrorH    , 'img.Mirror(horizontally=True)'),
            (self.mirrorV    , 'img.Mirror(horizontally=False)'),
            (self.mirrorBoth , 'img.Mirror(horizontally=True).\n\tMirror(horizontally=False)'),
            (self.adjustChan , 'img.AdjustChannels(factor_red=2.0,\n\tfactor_green=1.0,\n\tfactor_blue=1.0,\n\tfactor_alpha=1.0)'),
            (self.rotate     , 'img.Rotate(angle=45.0,\n\trotationCentre=imgCenterPt,\n\tinterpolating=True,\n\toffsetAfterRotation=None)'),
            (self.rotate90   , 'img.Rotate90(clockwise=True)'),
            (self.rotate180  , 'img.Rotate180()'),
            (self.replace    , 'img.Replace(r1=0, g1=0, b1=0,\n\tr2=0, g2=255, b2=0)'),
            (self.scale      , 'img.Scale(width=128, height=32,\n\tquality=wx.IMAGE_QUALITY_NORMAL)'),
            (self.rescale    , 'img.Rescale(width=128, height=32,\n\tquality=wx.IMAGE_QUALITY_NORMAL)'),
            (self.resize     , 'img.Resize(size=(256 + 16, 64 + 8),\n\tpos=(0+8, 0+4),\n\tred=0, green=0, blue=255)'),
            (self.paste      , 'img.Paste(image=getImg(), x=16, y=16)'),
            (self.rotatehue  , 'img.RotateHue(0.5)'),
            ])

        for imgModification, tip in list(dict.items()):
            statBmp = wx.StaticBitmap(self, wx.ID_ANY,
                                      imgModification.ConvertToBitmap())
            self.allModdedStatBmps.append(statBmp)
            tip = tip.replace('\t', ' '*8)
            statText = wx.StaticText(self, -1, tip)
            fgsizer2.Add(statText) #, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)
            fgsizer2.Add(statBmp)#, 0, wx.ALL, 5)

        vsizer0.Add(fgsizer2, 0, wx.LEFT, 25)
        self.SetSizer(vsizer0)
        self.SetupScrolling()


    def getImg(self):
        # Start with a fresh copy of the image to mod.
        path = opj(self.filebutton.GetPath())
        type = self.imgType
        return wx.Image(path, type)


    def DoImageMods(self):
        getImg = self.getImg  # local opt
        self.greyscale = getImg().ConvertToGreyscale()
        self.disabled = getImg().ConvertToDisabled()
        self.mono = getImg().ConvertToMono(r=255,g=255,b=255)
        self.maskIMG = getImg()
        self.maskIMG.SetMaskColour(red=255,green=255,blue=255)
        self.mask = self.maskIMG
        self.blur = getImg().Blur(blurRadius=3)
        self.blurH = getImg().BlurHorizontal(blurRadius=3)
        self.blurV = getImg().BlurVertical(blurRadius=3)
        self.mirrorH = getImg().Mirror(horizontally=True)
        self.mirrorV = getImg().Mirror(horizontally=False)
        self.mirrorBoth = getImg().Mirror(True).Mirror(False)
        self.adjustChan = getImg().AdjustChannels(factor_red=2.0,
                                                  factor_green=1.0,
                                                  factor_blue=1.0,
                                                  factor_alpha=1.0)
        self.rotate = getImg().Rotate(angle=45.0,
                                      rotationCentre=self.imgCenterPt,
                                      interpolating=True,
                                      offsetAfterRotation=None)
        self.rotate90 = getImg().Rotate90(clockwise=True)
        self.rotate180 = getImg().Rotate180()
        self.replaceIMG = getImg()
        self.replaceIMG.Replace(r1=0, g1=0, b1=0, r2=0, g2=255, b2=0)
        self.replace = self.replaceIMG
        self.scale = getImg().Scale(width=128, height=32, quality=IMG_QUALITY)
        self.rescale = getImg().Rescale(width=128, height=32, quality=IMG_QUALITY)
        self.resize = getImg().Resize(size=(256 + 16, 64 + 8),
                                      pos=(0+8, 0+4), red=0, green=0, blue=255)
        self.pasteIMG = getImg()
        self.pasteIMG.Paste(image=getImg(), x=16, y=16)
        self.paste = self.pasteIMG
        self.rotatehueIMG = getImg()
        self.rotatehueIMG.RotateHue(0.5)
        self.rotatehue = self.rotatehueIMG

    def ChangePanelColor(self, event):
        color = event.GetColour()
        self.SetBackgroundColour(color)
        self.Refresh()

    def ChangeModdedImages(self, event=None):
        self.img = img = self.getImg()
        self.imgWidth = img.GetWidth()
        self.imgHeight = img.GetHeight()
        self.imgCenterPt = wx.Point(self.imgWidth//2, self.imgHeight//2)

        self.DoImageMods()

        list = [self.img        ,
                self.greyscale  ,
                self.disabled   ,
                self.mono       ,
                self.mask       ,
                self.blur       ,
                self.blurH      ,
                self.blurV      ,
                self.mirrorH    ,
                self.mirrorV    ,
                self.mirrorBoth ,
                self.adjustChan ,
                self.rotate     ,
                self.rotate90   ,
                self.rotate180  ,
                self.replace    ,
                self.scale      ,
                self.rescale    ,
                self.resize     ,
                self.paste      ,
                self.rotatehue
               ]

        for imgModification in range(len(list)):
            self.allModdedStatBmps[imgModification].SetBitmap(list[imgModification].ConvertToBitmap())
        self.fgsizer2.RecalcSizes()
        self.PostSizeEvent()


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(ImagePanel(self), 1, wx.EXPAND | wx.ALL, 0)
        self.SetAutoLayout(1)
        self.SetSizer(vsizer)

def runTest(frame, nb, log):
    panel = TestPanel(nb, log)

    return panel

#----------------------------------------------------------------------



overview = """\
<html>
<body>
This class encapsulates a platform-independent image. An image can be created
 from data, or using <code>wxBitmap.ConvertToImage</code>. An image can be loaded
 from a file in a variety of formats, and is extensible to new formats via image
 format handlers. Functions are available to set and get image bits, so it can
 be used for basic image manipulation.

<p>The following image handlers are available. wxBMPHandler is always installed
 by default. To use other image formats, install the appropriate handler or use
<code>wx.InitAllImageHandlers()</code>.

<p>
<table>
<tr><td width=25%>wxBMPHandler</td>  <td>For loading and saving, always installed.</td></tr>
<tr><td>wxPNGHandler</td>  <td>For loading and saving.</td>  </tr>
<tr><td>wxJPEGHandler</td>  <td>For loading and saving.</td>  </tr>
<tr><td>wxGIFHandler</td>  <td>Only for loading, due to legal issues.</td>  </tr>
<tr><td>wxPCXHandler</td>  <td>For loading and saving.</td>  </tr>
<tr><td>wxPNMHandler</td>  <td>For loading and saving.</td>  </tr>
<tr><td>wxTIFFHandler</td>  <td>For loading and saving.</td>  </tr>
<tr><td>wxIFFHandler</td>  <td>For loading only.</td>  </tr>
<tr><td>wxXPMHandler</td>  <td>For loading and saving.</td> </tr>
<tr><td>wxICOHandler</td>  <td>For loading and saving.</td>  </tr>
<tr><td>wxCURHandler</td>  <td>For loading and saving.</td>  </tr>
<tr><td>wxANIHandler</td>  <td>For loading only.</td> </tr>
</table>

<p>When saving in PCX format, wxPCXHandler will count the number of different
colours in the image; if there are 256 or less colours, it will save as 8 bit,
else it will save as 24 bit.

<p>Loading PNMs only works for ASCII or raw RGB images. When saving in PNM format,
wxPNMHandler will always save as raw RGB.

</body>
</html>"""

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

