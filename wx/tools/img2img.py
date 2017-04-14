#----------------------------------------------------------------------
# Name:        wx.tools.img2img
# Purpose:     Common routines for the image converter utilities.
#
# Author:      Robin Dunn
#
# Copyright:   (c) 2002-2017 by Total Control Software
# Licence:     wxWindows license
# Tags:        phoenix-port, py3-port
#----------------------------------------------------------------------
# 12/21/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o V2.5 compatibility update
#

import  getopt
import  glob
import  os
import  sys

import  wx

def convert(file, maskClr, outputDir, outputName, outType, outExt):
    img = wx.Bitmap(file, wx.BITMAP_TYPE_ANY)
    if not img.IsOk():
        return 0, file + " failed to load!"
    else:
        if maskClr:
            om = img.GetMask()
            mask = wx.Mask(img, maskClr)
            img.SetMask(mask)
            if om is not None:
                om.Destroy()
        if outputName:
            newname = outputName
        else:
            newname = os.path.join(outputDir,
                                   os.path.basename(os.path.splitext(file)[0]) + outExt)
        if img.SaveFile(newname, outType):
            return 1, file + " converted to " + newname
        else:
            img = img.ConvertToImage()
            if img.SaveFile(newname, outType):
                return 1, "ok"
            else:
                return 0, file + " failed to save!"




def main(args, outType, outExt, doc):
    if not args or ("-h" in args):
        print(doc)
        return

    outputDir = ""
    maskClr = None
    outputName = None

    try:
        opts, fileArgs = getopt.getopt(args, "m:n:o:")
    except getopt.GetoptError:
        print(__doc__)
        return

    for opt, val in opts:
        if opt == "-m":
            maskClr = val
        elif opt == "-n":
            outputName = val
        elif opt == "-o":
            outputDir = val

    if not fileArgs:
        print(doc)
        return

    for arg in fileArgs:
        for file in glob.glob(arg):
            if not os.path.isfile(file):
                continue
            ok, msg = convert(file, maskClr, outputDir, outputName,
                              outType, outExt)
            print(msg)

