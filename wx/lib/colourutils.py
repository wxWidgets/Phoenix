#----------------------------------------------------------------------
# Name:        colourutils.py
# Purpose:     Some useful colour-related utility functions.
#
# Author:      Cody Precord
#
# Created:     13-March-2001
# Copyright:   (c) 2001-2017 by Total Control Software
# Licence:     wxWindows license
# Tags:        phoenix-port, documented
#----------------------------------------------------------------------

"""
Some useful colour-related utility functions.
"""

__author__ = "Cody Precord <cprecord@editra.org>"

import wx

# Used on OSX to get access to carbon api constants
if wx.Platform == '__WXMAC__':
    try:
        import Carbon.Appearance
    except ImportError:
        CARBON = False
    else:
        CARBON = True

#-----------------------------------------------------------------------------#

def AdjustAlpha(colour, alpha):
    """
    Adjust the alpha of a given colour

    :param integer `alpha`: the new value for the colour alpha channel (between 0
     and 255).

    :rtype: :class:`wx.Colour`
    :returns: A new :class:`wx.Colour` with the alpha channel specified as input
    """

    return wx.Colour(colour.Red(), colour.Green(), colour.Blue(), alpha)


def AdjustColour(color, percent, alpha=wx.ALPHA_OPAQUE):
    """
    Brighten/darken input colour by `percent` and adjust alpha
    channel if needed. Returns the modified color.

    :param wx.Colour `color`: color object to adjust;
    :param integer `percent`: percent to adjust +(brighten) or -(darken);
    :param integer `alpha`: amount to adjust alpha channel.

    :rtype: :class:`wx.Colour`
    :returns: A new darkened/lightened :class:`wx.Colour` with the alpha channel
     specified as input
    """

    radj, gadj, badj = [ int(val * (abs(percent) / 100.))
                         for val in color.Get(includeAlpha=False) ]

    if percent < 0:
        radj, gadj, badj = [ val * -1 for val in [radj, gadj, badj] ]
    else:
        radj, gadj, badj = [ val or 255 for val in [radj, gadj, badj] ]

    red = min(color.Red() + radj, 255)
    green = min(color.Green() + gadj, 255)
    blue = min(color.Blue() + badj, 255)
    return wx.Colour(red, green, blue, alpha)


def BestLabelColour(color, bw=False):
    """
    Get the best color to use for the label that will be drawn on
    top of the given color.

    :param wx.Colour `color`: background color that text will be drawn on;
    :param bool `bw`: If ``True``, only return black or white.

    :rtype: :class:`wx.Colour`
    """

    avg = sum(color.Get()) / 3
    if avg > 192:
        txt_color = wx.BLACK
    elif avg > 128:
        if bw: txt_color = wx.BLACK
        else: txt_color = AdjustColour(color, -95)
    elif avg < 64:
        txt_color = wx.WHITE
    else:
        if bw: txt_color = wx.WHITE
        else: txt_color = AdjustColour(color, 95)
    return txt_color


def GetHighlightColour():
    """
    Gets the default highlight color.

    :rtype: :class:`wx.Colour`
    """

    if wx.Platform == '__WXMAC__':
        if CARBON:
            if wx.VERSION < (2, 9, 0, 0, ''):
                # kThemeBrushButtonPressedLightHighlight
                brush = wx.Brush(wx.BLACK)
                brush.MacSetTheme(Carbon.Appearance.kThemeBrushFocusHighlight)
                return brush.GetColour()
            else:
                color = wx.MacThemeColour(Carbon.Appearance.kThemeBrushFocusHighlight)
                return color

    # Fallback to text highlight color
    return wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
