# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:         oglmisc.py
# Purpose:      Miscellaneous OGL support functions
#
# Author:       Pierre Hjälm (from C++ original by Julian Smart)
#
# Created:      2004-05-08
# Copyright:    (c) 2004 Pierre Hjälm - 1998 Julian Smart
# Licence:      wxWindows license
# Tags:         phoenix-port, unittest, py3-port, documented
#----------------------------------------------------------------------------
"""
Miscellaneous support functions for OGL.

params marked with '???' need review!
"""
import math

import wx

# Control point types
# Rectangle and most other shapes
CONTROL_POINT_VERTICAL = 1
CONTROL_POINT_HORIZONTAL = 2
CONTROL_POINT_DIAGONAL = 3

# Line
CONTROL_POINT_ENDPOINT_TO = 4
CONTROL_POINT_ENDPOINT_FROM = 5
CONTROL_POINT_LINE = 6

# Types of formatting: can be combined in a bit list
FORMAT_NONE = 0             # Left justification
FORMAT_CENTRE_HORIZ = 1     # Centre horizontally
FORMAT_CENTRE_VERT = 2      # Centre vertically
FORMAT_SIZE_TO_CONTENTS = 4 # Resize shape to contents

# Attachment modes
ATTACHMENT_MODE_NONE, ATTACHMENT_MODE_EDGE, ATTACHMENT_MODE_BRANCHING = 0, 1, 2

# Shadow mode
SHADOW_NONE, SHADOW_LEFT, SHADOW_RIGHT = 0, 1, 2

OP_CLICK_LEFT, OP_CLICK_RIGHT, OP_DRAG_LEFT, OP_DRAG_RIGHT = 1, 2, 4, 8
OP_ALL = OP_CLICK_LEFT | OP_CLICK_RIGHT | OP_DRAG_LEFT | OP_DRAG_RIGHT

# Sub-modes for branching attachment mode
BRANCHING_ATTACHMENT_NORMAL = 1
BRANCHING_ATTACHMENT_BLOB = 2

# logical function to use when drawing rubberband boxes, etc.
OGLRBLF = wx.INVERT

CONTROL_POINT_SIZE = 6

# Types of arrowhead
# (i) Built-in
ARROW_HOLLOW_CIRCLE   = 1
ARROW_FILLED_CIRCLE   = 2
ARROW_ARROW           = 3
ARROW_SINGLE_OBLIQUE  = 4
ARROW_DOUBLE_OBLIQUE  = 5
# (ii) Custom
ARROW_METAFILE        = 20

# Position of arrow on line
ARROW_POSITION_START  = 0
ARROW_POSITION_END    = 1
ARROW_POSITION_MIDDLE = 2

# Line alignment flags
# Vertical by default
LINE_ALIGNMENT_HORIZ              = 1
LINE_ALIGNMENT_VERT               = 0
LINE_ALIGNMENT_TO_NEXT_HANDLE     = 2
LINE_ALIGNMENT_NONE               = 0

# was defined in canvas and in composit
KEY_SHIFT = 1
KEY_CTRL = 2



def FormatText(dc, text, width, height, formatMode):
    """
    Format a text

    :param `dc`: the :class:`wx.MemoryDC`
    :param `text`: the text to format
    :param `width`: the width of the box???
    :param `height`: the height of the box??? it is not used in the code!
    :param `formatMode`: one of the format modes, can be combined in a bit list

      ======================================== ==================================
      Format mode name                         Description
      ======================================== ==================================
      `FORMAT_NONE`                            Left justification
      `FORMAT_CENTRE_HORIZ`                    Centre horizontally
      `FORMAT_CENTRE_VERT`                     Centre vertically
      `FORMAT_SIZE_TO_CONTENTS`                Resize shape to contents
      ======================================== ==================================

    :returns: a list of strings fitting in the box

    """
    i = 0
    word = ""
    word_list = []
    end_word = False
    new_line = False
    while i < len(text):
        if text[i] == "%":
            i += 1
            if i == len(text):
                word += "%"
            else:
                if text[i] == "n":
                    new_line = True
                    end_word = True
                    i += 1
                else:
                    word += "%" + text[i]
                    i += 1
        elif text[i] in ["\012","\015"]:
            new_line = True
            end_word = True
            i += 1
        elif text[i] == " ":
            end_word = True
            i += 1
        else:
            word += text[i]
            i += 1

        if i == len(text):
            end_word = True

        if end_word:
            word_list.append(word)
            word = ""
            end_word = False
        if new_line:
            word_list.append(None)
            new_line = False

    # Now, make a list of strings which can fit in the box
    string_list = []
    buffer = ""
    for s in word_list:
        oldBuffer = buffer
        if s is None:
            # FORCE NEW LINE
            if len(buffer) > 0:
                string_list.append(buffer)
            buffer = ""
        else:
            if len(buffer):
                buffer += " "
            buffer += s
            x, y = dc.GetTextExtent(buffer)

            # Don't fit within the bounding box if we're fitting
            # shape to contents
            if (x > width) and not (formatMode & FORMAT_SIZE_TO_CONTENTS):
                # Deal with first word being wider than box
                if len(oldBuffer):
                    string_list.append(oldBuffer)
                buffer = s
    if len(buffer):
        string_list.append(buffer)

    return string_list


def GetCentredTextExtent(dc, text_list, xpos=0, ypos=0, width=0, height=0):
    """
    Get the centred text extend

    :param `dc`: the :class:`wx.MemoryDC`
    :param `text_list`: a list of text lines
    :param `xpos`: unused
    :param `ypos`: unused
    :param `width`: unused
    :param `height`: unused

    :returns: maximum width and the height

    """
    if not text_list:
        return 0, 0

    max_width = 0
    for line in text_list:
        current_width, char_height = dc.GetTextExtent(line.GetText())
        if current_width > max_width:
            max_width = current_width

    return max_width, len(text_list) * char_height


def CentreText(dc, text_list, xpos, ypos, width, height, formatMode):
    """
    Centre a text

    :param `dc`: the :class:`wx.MemoryDC`
    :param `text_list`: a list of texts
    :param `xpos`: the x position
    :param `ypos`: the y position
    :param `width`: the width of the box???
    :param `height`: the height of the box???
    :param `formatMode`: one of the format modes, can be combined in a bit list

      ======================================== ==================================
      Format mode name                         Description
      ======================================== ==================================
      `FORMAT_NONE`                            Left justification
      `FORMAT_CENTRE_HORIZ`                    Centre horizontally
      `FORMAT_CENTRE_VERT`                     Centre vertically
      `FORMAT_SIZE_TO_CONTENTS`                Resize shape to contents
      ======================================== ==================================

    """
    if not text_list:
        return

    # First, get maximum dimensions of box enclosing text
    char_height = 0
    max_width = 0
    current_width = 0

    # Store text extents for speed
    widths = []
    for line in text_list:
        current_width, char_height = dc.GetTextExtent(line.GetText())
        widths.append(current_width)
        if current_width > max_width:
            max_width = current_width

    max_height = len(text_list) * char_height

    if formatMode & FORMAT_CENTRE_VERT:
        if max_height < height:
            yoffset = ypos - height / 2.0 + (height - max_height) / 2.0
        else:
            yoffset = ypos - height / 2.0
        yOffset = ypos
    else:
        yoffset = 0.0
        yOffset = 0.0

    if formatMode & FORMAT_CENTRE_HORIZ:
        xoffset = xpos - width / 2.0
        xOffset = xpos
    else:
        xoffset = 0.0
        xOffset = 0.0

    for i, line in enumerate(text_list):
        if formatMode & FORMAT_CENTRE_HORIZ and widths[i] < width:
            x = (width - widths[i]) / 2.0 + xoffset
        else:
            x = xoffset
        y = i * char_height + yoffset

        line.SetX(x - xOffset)
        line.SetY(y - yOffset)


def DrawFormattedText(dc, text_list, xpos, ypos, width, height, formatMode):
    """
    Draw formated text

    :param `dc`: the :class:`wx.MemoryDC`
    :param `text_list`: a list of texts
    :param `xpos`: the x position
    :param `ypos`: the y position
    :param `width`: the width of the box???
    :param `height`: the height of the box???
    :param `formatMode`: one of the format modes, can be combined in a bit list

      ======================================== ==================================
      Format mode name                         Description
      ======================================== ==================================
      `FORMAT_NONE`                            Left justification
      `FORMAT_CENTRE_HORIZ`                    Centre horizontally
      `FORMAT_CENTRE_VERT`                     Centre vertically
      `FORMAT_SIZE_TO_CONTENTS`                Resize shape to contents
      ======================================== ==================================

    """
    if formatMode & FORMAT_CENTRE_HORIZ:
        xoffset = xpos
    else:
        xoffset = xpos - width / 2.0

    if formatMode & FORMAT_CENTRE_VERT:
        yoffset = ypos
    else:
        yoffset = ypos - height / 2.0

    # +1 to allow for rounding errors
    dc.SetClippingRegion(xpos - width / 2.0, ypos - height / 2.0, width + 1, height + 1)

    for line in text_list:
        dc.DrawText(line.GetText(), xoffset + line.GetX(), yoffset + line.GetY())

    dc.DestroyClippingRegion()


def RoughlyEqual(val1, val2, tol=0.00001):
    """
    Check if values are roughtly equal

    :param `val1`: the first value to check
    :param `val2`: the second value to check
    :param `tol`: the tolerance, defaults to 0.00001

    :returns: True or False

    """
    return val1 < (val2 + tol) and val1 > (val2 - tol) and \
           val2 < (val1 + tol) and val2 > (val1 - tol)


def FindEndForBox(width, height, x1, y1, x2, y2):
    """
    Find the end for a box

    :param `width`: the width of the box
    :param `height`: the height of the box
    :param `x1`: x1 position
    :param `y1`: y1 position
    :param `x2`: x2 position
    :param `y2`: y2 position

    :returns: the end position

    """
    xvec = [x1 - width / 2.0, x1 - width / 2.0, x1 + width / 2.0, x1 + width / 2.0, x1 - width / 2.0]
    yvec = [y1 - height / 2.0, y1 + height / 2.0, y1 + height / 2.0, y1 - height / 2.0, y1 - height / 2.0]

    return FindEndForPolyline(xvec, yvec, x2, y2, x1, y1)


def CheckLineIntersection(x1, y1, x2, y2, x3, y3, x4, y4):
    """
    Check for line intersection

    :param `x1`: x1 position
    :param `y1`: y1 position
    :param `x2`: x2 position
    :param `y2`: y2 position
    :param `x3`: x3 position
    :param `y3`: y3 position
    :param `x4`: x4 position
    :param `y4`: y4 position

    :returns: a lenght ratio and a k line???

    """
    denominator_term = (y4 - y3) * (x2 - x1) - (y2 - y1) * (x4 - x3)
    numerator_term = (x3 - x1) * (y4 - y3) + (x4 - x3) * (y1 - y3)

    length_ratio = 1.0
    k_line = 1.0

    # Check for parallel lines
    if denominator_term < 0.005 and denominator_term > -0.005:
        line_constant = -1.0
    else:
        line_constant = float(numerator_term) / denominator_term

    # Check for intersection
    if line_constant < 1.0 and line_constant > 0.0:
        # Now must check that other line hits
        if (y4 - y3) < 0.005 and (y4 - y3) > -0.005:
            k_line = (x1 - x3 + line_constant * (x2 - x1)) / (x4 - x3)
        else:
            k_line = (y1 - y3 + line_constant * (y2 - y1)) / (y4 - y3)
        if k_line >= 0 and k_line < 1:
            length_ratio = line_constant
        else:
            k_line = 1

    return length_ratio, k_line


def FindEndForPolyline(xvec, yvec, x1, y1, x2, y2):
    """
    Find the end for a polyline

    :param `xvec`: x vector ???
    :param `yvec`: y vector ???
    :param `x1`: x1 position
    :param `y1`: y1 position
    :param `x2`: x2 position
    :param `y2`: y2 position

    :returns: the end position

    """
    lastx = xvec[0]
    lasty = yvec[0]

    min_ratio = 1.0

    for i in range(1, len(xvec)):
        line_ratio, other_ratio = CheckLineIntersection(x1, y1, x2, y2, lastx, lasty, xvec[i], yvec[i])
        lastx = xvec[i]
        lasty = yvec[i]

        if line_ratio < min_ratio:
            min_ratio = line_ratio

    # Do last (implicit) line if last and first doubles are not identical
    if not (xvec[0] == lastx and yvec[0] == lasty):
        line_ratio, other_ratio = CheckLineIntersection(x1, y1, x2, y2, lastx, lasty, xvec[0], yvec[0])
        if line_ratio < min_ratio:
            min_ratio = line_ratio

    return x1 + (x2 - x1) * min_ratio, y1 + (y2 - y1) * min_ratio


def PolylineHitTest(xvec, yvec, x1, y1, x2, y2):
    """
    Hittest for a polyline

    :param `xvec`: x vector ???
    :param `yvec`: y vector ???
    :param `x1`: x1 position
    :param `y1`: y1 position
    :param `x2`: x2 position
    :param `y2`: y2 position

    :returns: True or False

    """
    isAHit = False
    lastx = xvec[0]
    lasty = yvec[0]

    min_ratio = 1.0

    for i in range(1, len(xvec)):
        line_ratio, other_ratio = CheckLineIntersection(x1, y1, x2, y2, lastx, lasty, xvec[i], yvec[i])
        if line_ratio != 1.0:
            isAHit = True
        lastx = xvec[i]
        lasty = yvec[i]

        if line_ratio < min_ratio:
            min_ratio = line_ratio

    # Do last (implicit) line if last and first doubles are not identical
    if not (xvec[0] == lastx and yvec[0] == lasty):
        line_ratio, other_ratio = CheckLineIntersection(x1, y1, x2, y2, lastx, lasty, xvec[0], yvec[0])
        if line_ratio != 1.0:
            isAHit = True

    return isAHit


def GraphicsStraightenLine(point1, point2):
    """
    Straighten a line in graphics

    :param `point1`: a point list???
    :param `point2`: a point list???

    """
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]

    if dx == 0:
        return
    elif abs(float(dy) / dx) > 1:
        point2[0] = point1[0]
    else:
        point2[1] = point1[1]


def GetPointOnLine(x1, y1, x2, y2, length):
    """
    Get point on a line

    :param `x1`: x1 position
    :param `y1`: y1 position
    :param `x2`: x2 position
    :param `y2`: y2 position
    :param `length`: length ???

    :returns: point on line

    """
    l = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
    if l < 0.01:
        l = 0.01

    i_bar = (x2 - x1) / l
    j_bar = (y2 - y1) / l

    return -length * i_bar + x2, -length * j_bar + y2


def GetArrowPoints(x1, y1, x2, y2, length, width):
    """
    Get point on arrow

    :param `x1`: x1 position
    :param `y1`: y1 position
    :param `x2`: x2 position
    :param `y2`: y2 position
    :param `length`: length ???
    :param `width`: width ???

    :returns: point on line

    """
    l = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))

    if l < 0.01:
        l = 0.01

    i_bar = (x2 - x1) / l
    j_bar = (y2 - y1) / l

    x3 = -length * i_bar + x2
    y3 = -length * j_bar + y2

    return x2, y2, width * -j_bar + x3, width * i_bar + y3, -width * -j_bar + x3, -width * i_bar + y3


def DrawArcToEllipse(x1, y1, width1, height1, x2, y2, x3, y3):
    """
    Draw arc to ellipse

    :param `x1`: x1 position
    :param `y1`: y1 position
    :param `width1`: width
    :param `height1`: height
    :param `x2`: x2 position
    :param `y2`: y2 position
    :param `x3`: x3 position
    :param `y3`: y3 position

    :returns: ellipse points ???

    """
    a1 = width1 / 2.0
    b1 = height1 / 2.0

    # Check that x2 != x3
    if abs(x2 - x3) < 0.05:
        x4 = x2
        if y3 > y2:
            y4 = y1 - math.sqrt((b1 * b1 - (((x2 - x1) * (x2 - x1)) * (b1 * b1) / (a1 * a1))))
        else:
            y4 = y1 + math.sqrt((b1 * b1 - (((x2 - x1) * (x2 - x1)) * (b1 * b1) / (a1 * a1))))
        return x4, y4

    # Calculate the x and y coordinates of the point where arc intersects ellipse
    A = (1 / (a1 * a1))
    B = ((y3 - y2) * (y3 - y2)) / ((x3 - x2) * (x3 - x2) * b1 * b1)
    C = (2 * (y3 - y2) * (y2 - y1)) / ((x3 - x2) * b1 * b1)
    D = ((y2 - y1) * (y2 - y1)) / (b1 * b1)
    E = (A + B)
    F = (C - (2 * A * x1) - (2 * B * x2))
    G = ((A * x1 * x1) + (B * x2 * x2) - (C * x2) + D - 1)
    H = (float(y3 - y2) / (x3 - x2))
    K = ((F * F) - (4 * E * G))

    if K >= 0:
        # In this case the line intersects the ellipse, so calculate intersection
        if x2 >= x1:
            ellipse1_x = ((F * -1) + math.sqrt(K)) / (2 * E)
            ellipse1_y = ((H * (ellipse1_x - x2)) + y2)
        else:
            ellipse1_x = (((F * -1) - math.sqrt(K)) / (2 * E))
            ellipse1_y = ((H * (ellipse1_x - x2)) + y2)
    else:
        # in this case, arc does not intersect ellipse, so just draw arc
        ellipse1_x = x3
        ellipse1_y = y3

    return ellipse1_x, ellipse1_y


def FindEndForCircle(radius, x1, y1, x2, y2):
    """
    Find end for a circle

    :param `radius`: radius
    :param `x1`: x1 position
    :param `y1`: y1 position
    :param `x2`: x2 position
    :param `y2`: y2 position

    :returns: end position

    """
    H = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))

    if H == 0:
        return x1, y1
    else:
        return radius * (x2 - x1) / H + x1, radius * (y2 - y1) / H + y1
