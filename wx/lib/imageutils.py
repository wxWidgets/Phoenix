#----------------------------------------------------------------------
# Name:        wx.lib.imageutils
# Purpose:     A collection of functions for simple image manipulations
#
# Author:      Robb Shecter
#
# Created:     7-Nov-2002
# Copyright:   (c) 2002 by
# Licence:     wxWindows license
# Tags:        phoenix-port, unittest, documented
#----------------------------------------------------------------------

"""
This module contains a collection of functions for simple image manipulations.


Description
===========

This module contains a collection of functions for simple image manipulations.
The 2 functions defined here (:func:`grayOut`, :func:`makeGray` and :func:`stepColour`)
can be used to convert a given image into a grey-scale representation and to
darken/lighten a specific wxPython :class:`wx.Colour`.


Usage
=====

Sample usage::

    import wx
    from wx.lib.imageutils import grayOut, stepColour

    app = wx.App(0)

    bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (32, 32))
    disabled_bmp = wx.Bitmap(grayOut(bmp.ConvertToImage()))

    colour = wx.Colour(100, 120, 130)

    # Darker
    dark_colour = stepColour(colour, 50)

    # Lighter
    light_colour = stepColour(colour, 120)

    app.MainLoop()

"""


import wx

def grayOut(anImage):
    """
    Convert the given image (in place) to a grayed-out
    version, appropriate for a 'disabled' appearance.

    :param wx.Image `anImage`: the image we want to convert to gray-scale.

    :rtype: :class:`wx.Image`
    :returns: The modified (greyed out) image.

    .. note:: the image is converted in place, i.e. the input image will
       be modified to a greyed out version.

    """

    factor = 0.7        # 0 < f < 1.  Higher is grayer.
    if anImage.HasMask():
        maskColor = (anImage.GetMaskRed(), anImage.GetMaskGreen(), anImage.GetMaskBlue())
    else:
        maskColor = None
    if anImage.HasAlpha():
        alpha = anImage.GetAlpha()
    else:
        alpha = None

    data = anImage.GetData()

    for i in range(0, len(data), 3):
        pixel = (data[i], data[i+1], data[i+2])
        pixel = makeGray(pixel, factor, maskColor)
        for x in range(3):
            data[i+x] = pixel[x]
    anImage.SetData(data)  # ''.join(map(chr, data)))
    if alpha:
        anImage.SetAlpha(alpha)


def makeGray(rgb, factor, maskColor):
    """
    Make a pixel grayed-out. If the pixel matches the maskColor, it won't be
    changed.

    :param tuple `rgb`: a tuple of red, green, blue integers, defining the pixel :class:`wx.Colour`;
    :param float `factor`: the amount for which we want to grey out a pixel colour;
    :param `maskColor`: the mask colour.

    :type `maskColor`: tuple or :class:`wx.Colour`.

    :rtype: tuple
    :returns: An RGB tuple with the greyed out pixel colour.
    """

    if rgb != maskColor:
        return tuple([int((230 - x)*factor) + x for x in rgb])
    else:
        return rgb



def stepColour(c, step):
    """
    An utility function that simply darkens or lightens a
    color, based on the specified step value.  A step of 0 is
    completely black and a step of 200 is totally white, and 100
    results in the same color as was passed in.

    :param wx.Colour `c`: the input colour to be modified (darkened or lightened);
    :param integer `step`: the step value.

    :rtype: :class:`wx.Colour`
    :returns: A new colour, darkened or lightened depending on the input `step` value.
    """

    def _blendColour(fg, bg, dstep):
        result = bg + (dstep * (fg - bg))
        if result < 0:
            result = 0
        if result > 255:
            result = 255
        return result

    if step == 100:
        return c

    r = c.Red()
    g = c.Green()
    b = c.Blue()

    # step is 0..200 where 0 is completely black
    # and 200 is completely white and 100 is the same
    # convert that to a range of -1.0 .. 1.0
    step = min(step, 200)
    step = max(step, 0)
    dstep = (step - 100.0)/100.0

    if step > 100:
        # blend with white
        bg = 255.0
        dstep = 1.0 - dstep  # 0 = transparent fg; 1 = opaque fg
    else:
        # blend with black
        bg = 0.0
        dstep = 1.0 + dstep;  # 0 = transparent fg; 1 = opaque fg

    r = _blendColour(r, bg, dstep)
    g = _blendColour(g, bg, dstep)
    b = _blendColour(b, bg, dstep)

    return wx.Colour(int(r), int(g), int(b))

