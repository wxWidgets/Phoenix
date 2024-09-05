# --------------------------------------------------------------------------- #
# SCROLLEDTHUMBNAIL Control wxPython IMPLEMENTATION
# Python Code By:
#
# Michael Eager (eager@eagercon.com), 26 Sep 2020
#
# Based on thumnailctrl.py by
# Andrea Gavana And Peter Damoc, @ 12 Dec 2005, revised 27 Dec 2012
# andrea.gavana@gmail.com
# andrea.gavana@maerskoil.com
#
# Tags:         phoenix-port, documented, unittest, py3-port
#
# End Of Comments
# --------------------------------------------------------------------------- #

"""
:class:`ScrolledThumbnail` is a widget that can be used to display a series of
thumbnails for files in a scrollable window.

Description
===========

:class:`ScrolledThumbnail` is a widget derived from :class:`wx.ScrolledWindow`
which will display the thumbnail image for a file in a scrollable, resizable
window.  It supports selecting one or more thumbnails, rotating the thumbnails,
displaying information for each thumbnail, and popups for both the window and
for individual thumbnails.

The class uses two support classes: :class:`Thumb` and :class:`ImageHandler`.

:class:`Thumb` contains all of the information for a particular thumbnail,
including filename, bitmaped thumbnail image, caption, and other data.  This
class also has methods to perform thumbnail operations such as rotation,
highlighting, setting a file name.

:class:`ImageHandler` provides file/image handling functions, including loading
a file and creating an image from it, rotating an image, or highlighting an image.

The implementations of these two classes included in this file support generating
thumbnails from supported image files, such as JPEG, GIF, PNG, etc., using either
WxPythons native support or the PIL image library.  Additional file types can be
supported by extending these classes, for example, to provide a thumbnail image
for an MP4 file, perhaps the cover photo, an MPEG by providing the image of a
title frame, or a PDF by providing an image of the cover page.  The images for
these files may be generated on the fly by a suitably extended :class:`ImageHandler`,
or may be provided with the instance of :class:`Thumb`.  The list of `Thumb`
instances passed to `ScrolledThumbnail` may contain different derived classes,
as long as each contains the required functions.

NB:  Use of :class:`ScrolledThumbnail` has not been tested with extended classes.

:class:`ScrolledThumbnail`, :class:`Thumb`, and :class:`ImageHandler`, implemented
here are derived from the similarly named classes included in :class:`agw.ThumbnailCtrl`,
written by Andrea Gavana.  That implementation was tightly integrated as a image
file browser application.  The current implementation removes dependencies between
the several classes and narrows the scope of `ScrolledThumbnail` to the placement
and management of thumbnails within a window.

An updated :class:`ThumbnailCtrl` which uses this implementation of
:class:`ScrolledThumbnail`, :class:`Thumb`, and :class:`ImageHandler` provides
all of the previous functionality, which described as a widget that can be used
to display a series of images in a "thumbnail" format; it mimics, for example,
the windows explorer behavior when you select the "view thumbnails" option.
Basically, by specifying a folder that contains some image files, the files
in the folder are displayed as miniature versions of the actual images in
a :class:`ScrolledWindow`.

The code in the previous implementation is partly based on `wxVillaLib`, a
wxWidgets implementation of the :class:`ThumbnailCtrl` control.  Andrea Gavana
notes that :class:`ThumbnailCtrl` wouldn't have been so fast and complete
without the suggestions and hints from Peter Damoc.

Usage:
=====

Usage example::

    import os
    import wx
    from scrolledthumbnail import ScrolledThumbnail, Thumb, NativeImageHandler

    class MyFrame(wx.Frame):

        def __init__(self, parent):
            wx.Frame.__init__(self, parent, -1, "ScrolledThumb Demo", size=(400,300))

            self.scroll = ScrolledThumbnail(self, -1, size=(400,300))

        def ShowDir(self, dir):
            dir = os.getcwd()
            files = os.listdir(dir)
            thumbs = []
            for f in files:
                if os.path.splitext(f)[1] in [".jpg", ".gif", ".png"]:
                    thumbs.append(Thumb(dir, f, caption=f, imagehandler=NativeImageHandler))
            self.scroll.ShowThumbs(thumbs)


    app = wx.App(False)
    frame = MyFrame(None)
    frame.ShowDir(os.getcwd())
    frame.Show(True)

    app.MainLoop()



Methods and Settings
====================

With :class:`ScrolledThumbnail` you can:

- Create different thumbnail outlines (none, images only, full, etc...);
- Highlight thumbnails on mouse hovering;
- Show/hide file names below thumbnails;
- Change thumbnail caption font;
- Zoom in/out thumbnails (done via ``Ctrl`` key + mouse wheel or with ``+`` and ``-`` chars,
  with zoom factor value customizable);
- Rotate thumbnails with these specifications:

  a) ``d`` key rotates 90 degrees clockwise;
  b) ``s`` key rotates 90 degrees counter-clockwise;
  c) ``a`` key rotates 180 degrees.

- Drag and drop thumbnails from :class:`ScrolledThumbnail` to whatever application you want;
- Use local (when at least one thumbnail is selected) or global (no need for
  thumbnail selection) popup menus;
- possibility to show tooltips on thumbnails, which display file information
  (like file name, size, last modification date and thumbnail size).

:note: Using highlight thumbnails on mouse hovering may be slow on slower
 computers.


Window Styles
=============

`No particular window styles are available for this class.`


Events Processing
=================

This class processes the following events:

This class processes the following events:

================================== ==================================================
Event Name                         Description
================================== ==================================================
``EVT_THUMBNAILS_CAPTION_CHANGED`` The thumbnail caption has been changed. Not used at present.
``EVT_THUMBNAILS_DCLICK``          The user has double-clicked on a thumbnail.
``EVT_THUMBNAILS_POINTED``         The mouse cursor is hovering over a thumbnail.
``EVT_THUMBNAILS_SEL_CHANGED``     The user has changed the selected thumbnail.
``EVT_THUMBNAILS_THUMB_CHANGED``   The thumbnail of an image has changed. Used internally.
``EVT_THUMBNAILS_CHAR``            A character has been typed
================================== ==================================================


License And Version
===================

:class:`ScrolledThumbnail` is distributed under the wxPython license.

Latest revision: Michael Eager @ 2 Oct 2020

Version 1.0

"""

#----------------------------------------------------------------------
# Beginning Of ThumbnailCtrl wxPython Code
#----------------------------------------------------------------------

import os
import wx
import six
import zlib
from math import radians

from wx.lib.embeddedimage import PyEmbeddedImage

if six.PY3:
    import _thread as thread
else:
    import thread

#----------------------------------------------------------------------
# Get Default Icon/Data
#----------------------------------------------------------------------

#----------------------------------------------------------------------
file_broken = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAABGdBTUEAAK/INwWK6QAADU9J"
    b"REFUeJzNWn1QE2cefja7yRI+lAKiAgKCVIqegUYMFMsM4kfvzk7nmFrnvHGcOT3bq3P/OJ1p"
    b"b+zYf+r0HGxt6VVFqpYqWq9TW23RVnp6R7FXiq0UPAGhyFeQSCQJISHZ7Mf9gZuGkE02IeA9"
    b"M5k3u/vuu+/z/H7v7/297y4BPzh//vxfSJIsIgjC5a/eTIPn+UnHgiDIqisIAsUwTNfmzZtf"
    b"A8D7qk/5e3B0dPS6wsLCp/09MFTIbdO7ntR9vs5HRESgvr6+E0AlAD2AKZX8CsDzvEKtVsvq"
    b"aKjw7LggCO7jcJQqlQoMw6gBpAIYRAgCECGxCgDPTsohEopI4n+e5xXww1MRHkry4d1Zf9fk"
    b"uv90MOsCeMKfGN51pO6ZrmizKsBsWt976EjhoQ+BYMQItpSDWRNAjptPZ4xLCfl/PQTCaX2p"
    b"+wNhVgSYbet7tumdRXpj1ofAbFhfqn1fmHEBHpb1AYAgAudxMy4AQRB+LReuSB/MGsETMyqA"
    b"2WyG1WqVZQl/CDUZeuge0NvbKwwODk7bC7zryYFI/qF6QGNj42BnZ6dZ6rocQtNNhQNhxgQw"
    b"Go24fPnyDy0tLTcFQfDpBZ7/w2198RcIMyZAW1vb+KVLlxoGBwfr7927B4Vi8qO8CfnqbCjW"
    b"D4Y8MEMCCIKA77777me73d7a1tb25dDQkNXzmud/giDgdDrBsqzkuA1l7CuVSgCA0+n0y3FG"
    b"BBgYGMCVK1eub926dRFN04aBgYH/el73JKRUKjE4OIi+vj5QFDWtaVG0fGRkJHiex7lz5xyn"
    b"T59uBMBI9TWsAoidaW1tNTc1Nd1cv379zuzs7F91dHT8x+l0TooDnuju7h779ttvjdOdLlUq"
    b"FaKjo9HV1YX9+/d379q16+QXX3xxFsAAMHU7DAgggNw1tQiCIOByuXDt2rWbK1asUOfk5KxM"
    b"SUlZW19f39LX18eTJDmpbbG8cePGndra2mtDQ0NQKpUhJUPR0dHgeR6ffvqpbdeuXV+9/vrr"
    b"R4eGhs4A+ArA3ZAECAXd3d24dOnSD2VlZavy8vKQmppaUFdXN2gwGO561yVJEmazGR0dHV3n"
    b"z5//+NatW0MU5XebcgooikJMTAy6urqwb9++zp07d1ZfvXq1GsAn8+bNa6qsrEyGxJY4EGBT"
    b"lCAIhVR0ZhgGTqcTTqcTDocDDocDgiDgm2++0Y+MjNxbuXLl7wmCQFpaWtbcuXMje3p6fly9"
    b"enWyeL8gCCBJEj09PUJLS0s7z/PXWlpavigoKNhBURRYlnU/S6qMjIwEwzD47LPPbIcOHWq4"
    b"cuXKPwF8D+DHF154QV1cXFxpsVjiAGwGYIUPL/ArgNFoNNbV1dmtVqvdarW6LBaLY2xszOFw"
    b"OBiLxWKz2WxOs9lsHx0ddZhMJpvZbB7v7u7+effu3elZWVmJAJCUlBS1bt26nNbW1kaj0fj0"
    b"I4884iYHAHfu3Lnf2dnZDWC4oaHhH08++eRWrVZLe9bxJk9RFNRqNTo6OvDhhx92Hj16tG5k"
    b"ZKQBwHUAneXl5cVarfaQVqtddurUqesAUgC0BysAsWfPngOjo6ONY2NjUQzDOACMA7ADcGAi"
    b"sjoBuB6U4jFTWlp6Kj4+HjzPIzExEbm5uSuPHz9+csuWLfaEhIRIl8sFgiDA8zxu3rz585Yt"
    b"W3SpqanX9u7d+93GjRuv5eXlrRGvT+oQQUCtVsPhcODcuXO2w4cPi1ZvAnADgP3EiRN7NBrN"
    b"ntzcXDXHcXA6nREAJF9u+BNA6OnpuQ1gGAD5gCjrUXIPFOUflAIA7siRI8Xp6ekaYOI1lVKp"
    b"RGZmpqatre2QXq/v1mg0y4EJKxoMBrS1tQ2UlJQ8abPZjAD23Lhx46Pi4uI1aWlp7mEl1qdp"
    b"Grdu3UJNTU1nVVVV3cjIyDUAPwJof+WVVzJ0Ol1NQUHBbxMTEyHOOoEQKOKMP/jJxoIFC/6Q"
    b"mZlJidYTBAHp6emp2dnZCV1dXY0MwywnCAIkSUKv1zu7u7uNu3fvTh8aGtoE4Pj7779/ec2a"
    b"NZ0ZGRlZwC9Wt9vt+Pzzz22VlZUNV69eFa3+EwDTkSNHynJyct5ZtWpVikKhgMPhgEKhkJx2"
    b"gxFgSv1t27ZRUVFRFMuyZGZmZmJcXNwcpVIZT9N0tMvlWpiSklKmVConBbGkpCRq3bp1Kxsb"
    b"G69v3Lhxe3p6OgRBQHt7u2Hx4sVRycnJ9Ny5czO3bdv2VHV19XvNzc2frF69+pXY2FgoFAop"
    b"q3ds2rQp6plnnnkzLy9v99KlS8EwDDiOC2r5LSnAiRMnIubNm/dHkiSzaZqOIUkygabpGIqi"
    b"4iiKmkuSZDRJkiqVSkWRJKmkaZqMiIhAZGQkOI5zk+c4DnFxccjOztZWVVV9+eKLLw5nZGTM"
    b"YxgGzc3Ndx577LGF8fHxiI2NhU6n+111dfWZixcvnispKfmzTqebe+HCBW+rtwK4/8Ybb+Rp"
    b"NJojBQUFq2JiYuB0OgH8kgqLpdiXoAVobW2NfvbZZ/cWFhbOly3ngwf6yvczMzNzWJZV9Pb2"
    b"/lRUVLR2cHAQt2/fvrt9+3YtSZJQKBRYtmxZYXFx8ar6+vqrTU1NF7/++mtdZWXll0ajsQET"
    b"Qa4TE3HmBY1Gsz8/P3+Oy+Vyj3dP8nK9QFKA/v5+Cn7GfzBZmiAISE5OTiwqKsq4fft2k91u"
    b"X9vf3283GAyWtLS0ZNFTsrOzI0pKSsrq6+v//c477/xNr9evwMRr7ZsAhl966aUFOp3uzfz8"
    b"/C2LFi3C+Pj4JMLeAsjJYiUFYFk2oIRyReA4DikpKSgqKlpZW1t7saysjOvo6NAvXbo0NjEx"
    b"MZLneXAchzlz5kCj0TwVGxu7RK/Xt2Mihx8DwBw4cGBDbm5uRWFh4aNKpRJ2u30S8VCsD8hY"
    b"CwRzXqouz/OIiopCVlaWtrm5+X57e/tAS0uLPicnJzEhIcE9TnmeR05OTvJzzz33a0xMtyNa"
    b"rVY4fvz4a6WlpRdKSkoeFZfPYpSXIi93SyzYWWASMTmlZ/2MjIys+Pj4mI6Ojoa+vj5h/fr1"
    b"xaKrikIlJyfj8ccfLwNw7NVXX43TarV/LyoqWhsXF4fx8XF3TPFF2Pv/tPIAu93ul7g/+BJD"
    b"EAQsXLgwqrS0NLexsfE8RVHLFi1atNn7PpVKhdzc3OUvv/zyvg0bNvwmPz8/WeyPt8sHEkLO"
    b"anZaQyCYDUmO47BgwQIsX758VW1t7bc6nU5ISkpSeuYLHMeBYRhkZWWpd+zY8afCwsJklmXB"
    b"MMwUlw9EXjwOhIDL4dHRUQwMDMBms4Hn+YCuJSUKz/NQqVRYsmTJcgDzlixZsnzOnDlu1xfj"
    b"AMdxoGkaqampsNvtEATBvZ8olzxBEO57whIDxsbGMD4+DrVajaioKERGRoKiKMmdXn9IT09P"
    b"Li4ufiIxMVEHACzLThGW47gp54IhHwz8CiCSEt3P4XDA6XTCYrGApmnQNA2VSuUWwzvyescA"
    b"l8uF+fPnK59//vm/zp8/f6FoebF98VlSBOWS99WXkATwfrhnw+JmiEKhgEKhAEmSEDM6KTEI"
    b"gkBcXBwRExOTkpCQAJfLNSPkg4EsD/Algncs4Hl+ktv6+onjOS0tDTRNT1q4hJN8MCKE5AFS"
    b"nQx0DQAYhkFqaqpbrJkmH5YPJMJFXqFQTBmTM0E+LB5gt9slXTpU8t4E5JKXSnsDkfV+HReU"
    b"AJ6YLnlf1pNLXhAEmM1msCw7KSZ598/7PEEQ4DgOLMv6VSHQt8JhIS/HG/y5vV6vh9FohFqt"
    b"ducN3r8pxCgKJpMJvb29o/hlzzI4AUSEk7yUtfyJwTAMMjMzsXjxYr/zuuf7wbt376K8vLz/"
    b"7NmzlzCxpA5NgHCTl1vHFzkAPjNE774aDAaUl5f3V1RU1HAc9y9MbKr4RMA8QIr4TJP3LEU3"
    b"5zjOnTtItWUwGLB//36R/CVMbKXZQhbAV2dnk7zYD3G1KI537/oURbndvqKi4hTHcV9iYvd4"
    b"zB/HkFPh6ZL3JurvHIBJXuB9XfzG4MCBA/3vvvtujVzysgTwR2I65KVmAl/3iUtmlmUnDQGR"
    b"/P3793H48GH9A/Ki2wckH1AAzxjgS4yZJO/dD899A7EORVEYGRlBVVWV8b333vs4GMvLEsAT"
    b"oQ4Ff+Q92/YniGcMEAUQ5/ljx44Nv/XWWx9ZrdaLAJqDIR9QAO/9gHCTlxsERRFEAZRKJUwm"
    b"E6qrq4cPHjx4xmq11mLi1bglGPIBBfBF8mGQFyHmACaTCSdPnhx+++23z4yOjtZi4pWZKVjy"
    b"sgTwFiIU8v7GuVzyIsxmM06fPj188ODBjx5Y/nsAkl+jBoLsPECEryDl7ziQMHLJkyQJi8WC"
    b"mpqa4YqKCtHtmzAN8oCM9wJKpRIRERGyyAQi6CvwyeokRcFsNqOurm64oqLijMVimZbbT2pb"
    b"6gJN04TNZlNZLBYwDOOeEgNtMsqpF+y1sbEx1NbWDn/wwQdhJQ8AkmZYsWJFVEZGxtZ79+49"
    b"wbIsDa/VlBQJqS0of6QD3UMQBHp7e++YTKYrCIPbe8KfHyoALACwGIAqXA8MEQImPnO7A2Ak"
    b"nA3/D+/OyD/Ur3BPAAAAAElFTkSuQmCC")


def getDataSH():
    """ Return the first part of the shadow dropped behind thumbnails. """

    return zlib.decompress(
b'x\xda\xeb\x0c\xf0s\xe7\xe5\x92\xe2b``\xe0\xf5\xf4p\t\x02\xd2_A\x98\x83\rHvl\
\xdc\x9c\n\xa4X\x8a\x9d<C8\x80\xa0\x86#\xa5\x83\x81\x81y\x96\xa7\x8bcH\xc5\
\x9c\xb7\xd7\xd7\xf6\x85D2\xb4^\xbc\x1b\xd0\xd0p\xa6\x85\x9d\xa1\xf1\xc0\xc7\
\x7f\xef\x8d\x98\xf89_:p]\xaew\x0c\xe9\x16[\xbc\x8bSt\xdf\x9aT\xad\xef\xcb\
\x8e\x98\xc5\xbf\xb3\x94\x9ePT\xf8\xff\xf7\xfbm\xf5\xdb\xfeZ<\x16{\xf01o[l\
\xee\xee\xbd7\xbe\x95\xdd\xde\x9d+\xbf\xfdo\xf9\xb9\xd0\x03\x8be\xb7\xc7\xe6\
Y\xcb\xbd\x8b\xdfs\xe3[\xd6\xed\xe5\x9b}\x99\xe6=:\xbd\xed\xfc\xedu|\xfcq\
\xfb\xec/K<\xf8\xfec\xd7\xdb\xdb\x87W\xec\xcf\xfd]\xb0\xcc\xf0\xc0\xe5=\xf7^\
\x1e\xf9\xfb\xe6\xe6\xce\xe9\x0c\xfb\xa7\xafPt\xbb"\xa0\x9c\xd5!hz\xa4C*\xc9\
\x85\xd7pQ\x9bD\xa0s\xcf\xa8\xf0\xa8\xf0\x00\x0b\x9fyX\x7fo\xef\xdf\xc7\xda\
\r\xcbw\xd4\xfcx\xe0\xcdk\xd8\x9e[~{\xdd\xf6\xbfw\xbe\xfd\xddS\xdc\xe0\xfec_\
\xf0\xfe\xeb\xb7\xdf\xf1\xdd\xce\xdb&\xbb\xbdv\xe7\xff\xc3\xaf\x8dy\x99\xe5\
\x9e?\xf7\xfb+\xb7\xfdnLN\xf5\xc6\xb7g\xfd\xca_\x9a\x7f?\x7f\xe0\xfe\xe3\xaa\
\xe5\x0b\xf4\xb7\xcb\xea\x97\xed\n\xb7\xbf\xff\xadh\xf9\xe3\x1d\xd5f\x7fb\
\xdf\x95Y\x15\xc6\xe7\xee\xfe\xcbz7Y\xbd\xde[\xf3y\x1f0\xd72x\xba\xfa\xb9\
\xacsJh\x02\x00\xc4i\x8dN' )


def getDataBL():
    """ Return the second part of the shadow dropped behind thumbnails. """

    return zlib.decompress(
b"x\xda\xeb\x0c\xf0s\xe7\xe5\x92\xe2b``\xe0\xf5\xf4p\t\x02\xd2\xac \xcc\xc1\
\x06${\xf3\xd5\x9e\x02)\x96b'\xcf\x10\x0e \xa8\xe1H\xe9\x00\xf2\xed=]\x1cC8f\
\xea\x9e\xde\xcb\xd9` \xc2\xf0P\xdf~\xc9y\xaeu\x0f\xfe1\xdf\xcc\x14\x1482A\
\xe9\xfd\x83\x1d\xaf\x84\xac\xf8\xe6\\\x8c3\xfc\x98\xf8\xa0\xb1\xa9K\xec\x9f\
\xc4\xd1\xb4GG{\xb5\x15\x8f_|t\x8a[a\x1fWzG\xa9\xc4,\xa0Q\x0c\x9e\xae~.\xeb\
\x9c\x12\x9a\x00\x7f1,7" )


def getDataTR():
    """ Return the third part of the shadow dropped behind thumbnails. """

    return zlib.decompress(
b'x\xda\xeb\x0c\xf0s\xe7\xe5\x92\xe2b``\xe0\xf5\xf4p\t\x02\xd2\xac \xcc\xc1\
\x06${\xf3\xd5\x9e\x02)\x96b\'\xcf\x10\x0e \xa8\xe1H\xe9\x00\xf2m=]\x1cC8f\
\xe6\x9e\xd9\xc8\xd9` \xc2p\x91\xbd\xaei\xeeL\x85\xdcUo\xf6\xf7\xd6\xb2\x88\
\x0bp\x9a\x89i\x16=-\x94\xe16\x93\xb9!\xb8y\xcd\t\x0f\x89\n\xe6\xb7\xfcV~6\
\x8dFo\xf5\xee\xc8\x1fOaw\xc9\x88\x0c\x16\x05\x1a\xc4\xe0\xe9\xea\xe7\xb2\
\xce)\xa1\t\x00"\xf9$\x83' )


def getShadow():
    """ Creates a shadow behind every thumbnail. """

    sh_tr = wx.Image(six.BytesIO(getDataTR())).ConvertToBitmap()
    sh_bl = wx.Image(six.BytesIO(getDataBL())).ConvertToBitmap()
    sh_sh = wx.Image(six.BytesIO(getDataSH())).Rescale(500, 500, wx.IMAGE_QUALITY_HIGH)
    return (sh_tr, sh_bl, sh_sh.ConvertToBitmap())


#-----------------------------------------------------------------------------
# PATH & FILE FILLING (OS INDEPENDENT)
#-----------------------------------------------------------------------------

def opj(path):
    """
    Convert paths to the platform-specific separator.

    :param `path`: the path to convert.
    """

    strs = os.path.join(*tuple(path.split('/')))
    # HACK: on Linux, a leading / gets lost...
    if path.startswith('/'):
        strs = '/' + strs

    return strs

#-----------------------------------------------------------------------------

# Different Outline On Thumb Selection:
# THUMB_OUTLINE_NONE: No Outline Drawn On Selection
# THUMB_OUTLINE_FULL: Full Outline Drawn On Selection
# THUMB_OUTLINE_RECT: Only Maximum Image Rect Outlined On Selection
# THUMB_OUTLINE_IMAGE: Only Image Rect Outlined On Selection

THUMB_OUTLINE_NONE = 0
""" No outline drawn on selection. """
THUMB_OUTLINE_FULL = 1
""" Full outline drawn on selection. """
THUMB_OUTLINE_RECT = 2
""" Only the maximum image rectangle outlined on selection. """
THUMB_OUTLINE_IMAGE = 4
""" Only the image rectangle outlined on selection. """

# ThumbnailCtrl Events:
# wxEVT_THUMBNAILS_SEL_CHANGED: Event Fired When You Change Thumb Selection
# wxEVT_THUMBNAILS_POINTED: Event Fired When You Point A Thumb
# wxEVT_THUMBNAILS_DCLICK: Event Fired When You Double-Click A Thumb
# wxEVT_THUMBNAILS_CAPTION_CHANGED: Not Used At Present
# wxEVT_THUMBNAILS_THUMB_CHANGED: Used nternally
# wxEVT_THUMBNAILS_CHAR: Event Fired when character typed

wxEVT_THUMBNAILS_SEL_CHANGED = wx.NewEventType()
wxEVT_THUMBNAILS_POINTED = wx.NewEventType()
wxEVT_THUMBNAILS_DCLICK = wx.NewEventType()
wxEVT_THUMBNAILS_CAPTION_CHANGED = wx.NewEventType()
wxEVT_THUMBNAILS_THUMB_CHANGED = wx.NewEventType()
wxEVT_THUMBNAILS_CHAR = wx.NewEventType()

#-----------------------------------#
#        ThumbnailCtrlEvent
#-----------------------------------#

EVT_THUMBNAILS_SEL_CHANGED = wx.PyEventBinder(wxEVT_THUMBNAILS_SEL_CHANGED, 1)
""" The user has changed the selected thumbnail. """
EVT_THUMBNAILS_POINTED = wx.PyEventBinder(wxEVT_THUMBNAILS_POINTED, 1)
""" The mouse cursor is hovering over a thumbnail. """
EVT_THUMBNAILS_DCLICK = wx.PyEventBinder(wxEVT_THUMBNAILS_DCLICK, 1)
""" The user has double-clicked on a thumbnail. """
EVT_THUMBNAILS_THUMB_CHANGED = wx.PyEventBinder(wxEVT_THUMBNAILS_THUMB_CHANGED, 1)
""" The thumbnail of an image has changed. Used internally"""
EVT_THUMBNAILS_CHAR = wx.PyEventBinder(wxEVT_THUMBNAILS_CHAR, 1)
""" A character has been typed. """

# ---------------------------------------------------------------------------- #
# Class PILImageHandler, handles loading and highlighting images with PIL
# ---------------------------------------------------------------------------- #

class PILImageHandler(object):
    """
    This image handler loads and manipulates the thumbnails with the help
    of PIL (the Python Imaging Library).
    """

    def __init__(self):
        """
        Default class constructor.

        :note: If PIL is not installed, this will raise an exception. PIL
         can be downloaded from http://www.pythonware.com/products/pil/ .
        """

        try:

            import PIL.Image as Image
            import PIL.ImageEnhance as ImageEnhance

        except ImportError:

            errstr = ("\nThumbnailCtrl *requires* PIL (Python Imaging Library).\n"
                      "You can get it at:\n\n"
                      "http://www.pythonware.com/products/pil/\n\n"
                      "ThumbnailCtrl can not continue. Exiting...\n")

            raise Exception(errstr)


    def Load(self, filename):
        """
        Load the file.

        :param `filename`: a file containing an image;
        """

        import PIL.Image as Image

        try:
            with Image.open(filename) as pil:
                originalsize = pil.size

                img = wx.Image(pil.size[0], pil.size[1])

                img.SetData(pil.convert("RGB").tobytes())

                alpha = False
                if "A" in pil.getbands():
                    img.SetAlpha(pil.convert("RGBA").tobytes()[3::4])
                    alpha = True
        except:
            img = file_broken.GetImage()
            originalsize = (img.GetWidth(), img.GetHeight())
            alpha = False

        return img, originalsize, alpha


    def HighlightImage(self, img, factor):
        """
        Adjust overall image brightness to highlight.

        :param `img`: an instance of :class:`wx.Image`;
        :param `factor`: unused in :class:`PILImageHandler`.
        """

        import PIL.Image as Image
        import PIL.ImageEnhance as ImageEnhance

        pil = Image.new('RGB', (img.GetWidth(), img.GetHeight()))
        pil.frombytes(bytes(img.GetData()))
        enh = ImageEnhance.Brightness(pil)
        enh = enh.enhance(1.5)
        img.SetData(enh.convert('RGB').tobytes())
        return img

    def Rotate(self, img, angle):
        """
        Rotate image by angle degrees.

        :param img: an instance of :class:wx.Image;
        :param angle:  angle in degrees
        :return: rotated image
        """

        img = img.Rotate(radians(angle), (img.GetWidth(), img.GetHeight()), True)
        return img

# ---------------------------------------------------------------------------- #
# Class NativeImageHandler, handles loading and highlighting images with wx
# ---------------------------------------------------------------------------- #

class NativeImageHandler(object):
    """
    This image handler loads and manipulates the thumbnails with the help of
    wxPython's own image related functions.
    """

    def Load(self, filename):
        """
        Load the file.

        :param `filename`: a file containing an image;
        """

        img = wx.Image(filename)

        # Don't stop when a corrupt file is to be loaded, show Mondrian instead
        try:
            originalsize = (img.GetWidth(), img.GetHeight())
            alpha = img.HasAlpha()
            assert img.IsOk()
        except:
            img = file_broken.GetImage()
            originalsize = (img.GetWidth(), img.GetHeight())
            alpha = False

        return img, originalsize, alpha


    def HighlightImage(self, img, factor):
        """
        Adjust overall image brightness to highlight.

        :param `img`: an instance of :class:`wx.Image`;
        :param `factor`: a floating point number representing the highlight factor.
        """

        return img.AdjustChannels(factor, factor, factor, factor)


    def Rotate(self, img, angle):
        """
        Rotate image by angle degrees.

        :param img: an instance of :class:wx.Image;
        :param angle:  angle in degrees
        :return: rotated image
        """

        img = img.Rotate(radians(angle), (img.GetWidth(), img.GetHeight()), True)
        return img


# ---------------------------------------------------------------------------- #
# Class Thumb
# Auxiliary Class, To Handle Single Thumb Information For Every Thumb.
# ---------------------------------------------------------------------------- #

class Thumb(object):
    """
    This is an auxiliary class, to handle single thumbnail information for every thumb.

    Used internally.
    """

    def __init__(self, folder, filename, caption="", size=0, lastmod=0, imagehandler=None):
        """
        Default class constructor.

        :param `folder`: the directory containing the images;
        :param `filename`: a file containing an image;
        :param `caption`: the thumbnail caption string;
        :param `size`: the file size;
        :param `lastmod`: the file last modification time.
        """

        self._filename = filename
        self.SetCaption(caption)
        self._id = 0
        self._dir = folder
        self._filesize = size
        self._lastmod = lastmod
        self._captionbreaks = []
        self._image = wx.Image(1, 1)
        self._alpha = None
        self._imagehandler = imagehandler()
        self._bitmap = None


    def SetCaption(self, caption=""):
        """
        Sets the thumbnail caption.

        :param `caption`: the thumbnail caption string.
        """

        self._caption = caption
        self._captionbreaks = []


    def GetImage(self):
        """ Returns the thumbnail image. """

        return self._image


    def SetImage(self, image):
        """
        Sets the thumbnail image.

        :param `image`: a :class:`wx.Image` object.
        """

        self._image = image


    def GetFileName(self):
        """ Returns the file name associated with this thumbnail. """

        return self._filename


    def SetFileName(self, filename):
        """
        Sets the file name associated with this thumbnail.

        :param `filename`: the file containing the image.
        """

        self._filename = filename


    def GetId(self):
        """ Returns the thumbnail identifier. """

        return self._id


    def SetId(self, id=-1):
        """
        Sets the thumbnail identifier.

        :param `id`: an integer specifying the thumbnail identifier.
        """

        self._id = id


    def GetThumbnail(self, width, height):
        """
        Returns the wx.Image of the thumbnail

        :param `width`: the associated bitmap width;
        :param `height`: the associated bitmap height.
        """

        img = self._image
        imgwidth, imgheight = (img.GetWidth(), img.GetHeight())
        if width < imgwidth or height < imgheight:
            scale = float(width)/imgwidth

            if scale > float(height)/imgheight:
                scale = float(height)/imgheight

            newW, newH = int(imgwidth*scale), int(imgheight*scale)
            if newW < 1:
                newW = 1
            if newH < 1:
                newH = 1

            img = img.Scale(newW, newH)

        return img


    def GetBitmap(self, width, height):
        """
        Returns the bitmap of the thumbnail

        :param `width`: the associated bitmap width;
        :param `height`: the associated bitmap height.
        """

        if self._bitmap:
            if self._bitmap.GetWidth() == width and self._bitmap.GetHeight() == height:
                return self._bitmap

        img = self.GetThumbnail(width, height)
        bmp = img.ConvertToBitmap()

        return bmp


    def GetFullFileName(self):
        """ Returns the full filename of the thumbnail. """

        return os.path.join(self._dir, self._filename)


    def GetCaption(self, line):
        """
        Returns the caption associated to a thumbnail.

        :param `line`: the caption line we wish to retrieve (useful for multilines
         caption strings).
        """

        if line + 1 >= len(self._captionbreaks):
            return ""

        strs = self._caption

        return strs


    def GetFileSize(self):
        """ Returns the file size in bytes associated to a thumbnail. """

        return self._filesize


    def GetDisplayFileSize(self):
        """ Return printable file size (with bytes, Kb, Mb suffix). """

        size = self.GetFileSize()
        if size < 1000:
            size = str(size) + " bytes"
        elif size < 1000000:
            size = str(int(round(size/1000.0))) + " Kb"
        else:
            size = str(round(size/1000000.0, 2)) + " Mb"
        return size


    def GetCreationDate(self):
        """ Returns the file last modification date associated to a thumbnail. """

        return self._lastmod


    def GetOriginalSize(self):
        """ Returns a tuple containing the original image width and height, in pixels. """

        return self._originalsize


    def GetCaptionLinesCount(self, width):
        """
        Returns the number of lines for the caption.

        :param `width`: the maximum width, in pixels, available for the caption text.
        """

        self.BreakCaption(width)
        return len(self._captionbreaks) - 1


    def BreakCaption(self, width):
        """
        Breaks the caption in several lines of text (if needed).

        :param `width`: the maximum width, in pixels, available for the caption text.
        """

        if len(self._captionbreaks) > 0 or width < 16:
            return

        self._captionbreaks.append(0)

        if len(self._caption) == 0:
            return

        pos = width//16
        beg = 0
        end = 0

        dc = wx.MemoryDC()
        bmp = wx.Bitmap(10, 10)
        dc.SelectObject(bmp)

        while 1:

            if pos >= len(self._caption):

                self._captionbreaks.append(len(self._caption))
                break

            sw, sh = dc.GetTextExtent(self._caption[beg:pos-beg])

            if  sw > width:

                if end > 0:

                    self._captionbreaks.append(end)
                    beg = end

                else:

                    self._captionbreaks.append(pos)
                    beg = pos

                pos = beg + width//16
                end = 0

            if pos < len(self._caption) and self._caption[pos] in [" ", "-", ",", ".", "_"]:
                end = pos + 1

            pos = pos + 1


        dc.SelectObject(wx.NullBitmap)


    def GetInfo(self):
        """ Returns info for thumbnain in display format. """
        thumbinfo = "Name: " + self.GetFileName() + "\n" \
                    "Size: " + self.GetDisplayFileSize() + "\n" \
                    "Modified: " + self.GetCreationDate() + "\n" \
                    "Dimensions: " + str(self.GetOriginalSize()) + "\n"
        return thumbinfo


    def LoadImage(self):
        """ Load image using imagehandler. """
        filename = self.GetFullFileName()
        img, size, alpha = self._imagehandler.Load(filename)
        self._image = img
        self._originalsize = size
        self._alpha = alpha


    def Rotate(self, angle):
        """ Rotate image using imagehandler. """
        img = self._imagehandler.Rotate(self._image, angle)
        self._image = img
        self._originalsize = (img.GetWidth, img.GetHeight)
        self._alpha = img.HasAlpha()
        # Clear _bitmap so thumbnail is recreated after rotate
        self._bitmap = None


    def GetHighlightBitmap(self, width, height, factor):
        """ Returned highlighted bitmap of thumbnail. """

        img = self.GetThumbnail(width, height)
        img = self._imagehandler.HighlightImage(img, factor)

        bmp = img.ConvertToBitmap()

        return bmp

# ---------------------------------------------------------------------------- #
# Class ScrolledThumbnail
# This Is The Main Class Implementation
# ---------------------------------------------------------------------------- #

class ScrolledThumbnail(wx.ScrolledWindow):
    """ This is the main class implementation of :class:`ThumbnailCtrl`. """

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, thumboutline=THUMB_OUTLINE_IMAGE,
                 imagehandler=None):
        """
        Default class constructor.

        :param `parent`: parent window. Must not be ``None``;
        :param `id`: window identifier. A value of -1 indicates a default value;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `thumboutline`: outline style for :class:`ScrolledThumbnail`, which may be:

         =========================== ======= ==================================
         Outline Flag                 Value  Description
         =========================== ======= ==================================
         ``THUMB_OUTLINE_NONE``            0 No outline is drawn on selection
         ``THUMB_OUTLINE_FULL``            1 Full outline (image+caption) is drawn on selection
         ``THUMB_OUTLINE_RECT``            2 Only thumbnail bounding rectangle is drawn on selection (default)
         ``THUMB_OUTLINE_IMAGE``           4 Only image bounding rectangle is drawn.
         =========================== ======= ==================================

        :param `imagehandler`: can be :class:`PILImageHandler` if PIL is installed (faster), or
         :class:`NativeImageHandler` which only uses wxPython image methods.
        """

        wx.ScrolledWindow.__init__(self, parent, id, pos, size)

        self._items = []
        self.SetThumbSize(96, 80)
        self._tOutline = thumboutline
        self._selected = -1
        self._pointed = -1
        self._pmenu = None
        self._gpmenu = None
        self._dragging = False
        self._checktext = False
        self._dropShadow = True

        self._tCaptionHeight = []
        self._selectedarray = []
        self._tTextHeight = 16
        self._tCaptionBorder = 8
        self._tOutlineNotSelected = True
        self._mouseeventhandled = False
        self._highlight = False
        self._zoomfactor = 1.4
        self.SetCaptionFont()

        self._enabletooltip = False

        self._parent = parent

        self._selectioncolour = "#009EFF"
        self.grayPen = wx.Pen("#A2A2D2", 1, wx.SHORT_DASH)
        self.grayPen.SetJoin(wx.JOIN_MITER)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOX))

        t, b, s = getShadow()
        self.shadow = wx.MemoryDC()
        self.shadow.SelectObject(s)

        self.ShowFileNames(True)

        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnMouseDClick)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Bind(EVT_THUMBNAILS_THUMB_CHANGED, self.OnThumbChanged)
        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)

        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)
        self.Bind(wx.EVT_PAINT, self.OnPaint)


    def GetSelectedItem(self, index):
        """
        Returns the selected thumbnail.

        :param `index`: the thumbnail index (i.e., the selection).
        """

        return self.GetItem(self.GetSelection(index))


    def GetPointed(self):
        """ Returns the pointed thumbnail index. """

        return self._pointed


    def GetHighlightPointed(self):
        """
        Returns whether the thumbnail pointed should be highlighted or not.

        :note: Please be aware that this functionality may be slow on slower computers.
        """

        return self._highlight


    def SetHighlightPointed(self, highlight=True):
        """
        Sets whether the thumbnail pointed should be highlighted or not.

        :param `highlight`: ``True`` to enable highlight-on-point with the mouse,
         ``False`` otherwise.

        :note: Please be aware that this functionality may be slow on slower computers.
        """

        self._highlight = highlight


    def SetThumbOutline(self, outline):
        """
        Sets the thumbnail outline style on selection.

        :param `outline`: the outline to use on selection. This can be one of the following
         bits:

         =========================== ======= ==================================
         Outline Flag                 Value  Description
         =========================== ======= ==================================
         ``THUMB_OUTLINE_NONE``            0 No outline is drawn on selection
         ``THUMB_OUTLINE_FULL``            1 Full outline (image+caption) is drawn on selection
         ``THUMB_OUTLINE_RECT``            2 Only thumbnail bounding rectangle is drawn on selection (default)
         ``THUMB_OUTLINE_IMAGE``           4 Only image bounding rectangle is drawn.
         =========================== ======= ==================================

        """

        if outline not in [THUMB_OUTLINE_NONE, THUMB_OUTLINE_FULL, THUMB_OUTLINE_RECT,
                           THUMB_OUTLINE_IMAGE]:
            return

        self._tOutline = outline


    def GetThumbOutline(self):
        """
        Returns the thumbnail outline style on selection.

        :see: :meth:`~ScrolledThumbnail.SetThumbOutline` for a list of possible return values.
        """

        return self._tOutline


    def SetDropShadow(self, drop):
        """
        Sets whether to drop a shadow behind thumbnails or not.

        :param `drop`: ``True`` to drop a shadow behind each thumbnail, ``False`` otheriwise.
        """

        self._dropShadow = drop
        self.Refresh()


    def GetDropShadow(self):
        """
        Returns whether to drop a shadow behind thumbnails or not.
        """

        return self._dropShadow


    def GetPointedItem(self):
        """ Returns the pointed thumbnail. """

        return self.GetItem(self._pointed)


    def GetItem(self, index):
        """
        Returns the item at position `index`.

        :param `index`: the thumbnail index position.
        """

        return index >= 0 and (index < len(self._items) and [self._items[index]] or [None])[0]


    def GetItemCount(self):
        """ Returns the number of thumbnails. """

        return len(self._items)


    def GetThumbWidth(self):
        """ Returns the thumbnail width. """

        return self._tWidth


    def GetThumbHeight(self):
        """ Returns the thumbnail height. """

        return self._tHeight


    def GetThumbBorder(self):
        """ Returns the thumbnail border. """

        return self._tBorder


    def ShowFileNames(self, show=True):
        """
        Sets whether the user wants to show file names under the thumbnails or not.

        :param `show`: ``True`` to show file names under the thumbnails, ``False`` otherwise.
        """

        self._showfilenames = show
        self.Refresh()


    def SetPopupMenu(self, menu):
        """
        Sets the thumbnails popup menu when at least one thumbnail is selected.

        :param `menu`: an instance of :class:`wx.Menu`.
        """

        self._pmenu = menu


    def GetPopupMenu(self):
        """ Returns the thumbnails popup menu when at least one thumbnail is selected. """

        return self._pmenu


    def SetGlobalPopupMenu(self, gpmenu):
        """
        Sets the global thumbnails popup menu (no need of thumbnail selection).

        :param `gpmenu`: an instance of :class:`wx.Menu`.
        """

        self._gpmenu = gpmenu


    def GetGlobalPopupMenu(self):
        """ Returns the global thumbnailss popup menu (no need of thumbnail selection). """

        return self._gpmenu


    def GetSelectionColour(self):
        """ Returns the colour used to indicate a selected thumbnail. """

        return self._selectioncolour


    def SetSelectionColour(self, colour=None):
        """
        Sets the colour used to indicate a selected thumbnail.

        :param `colour`: a valid :class:`wx.Colour` object. If defaulted to ``None``, it
         will be taken from the system settings.
        """

        if colour is None:
            colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)

        self._selectioncolour = colour


    def EnableDragging(self, enable=True):
        """
        Enables/disables thumbnails drag and drop.

        :param `enable`: ``True`` to enable drag and drop, ``False`` to disable it.
        """

        self._dragging = enable


    def EnableToolTips(self, enable=True):
        """
        Globally enables/disables thumbnail file information.

        :param `enable`: ``True`` to enable thumbnail file information, ``False`` to disable it.
        """

        self._enabletooltip = enable

        if not enable and hasattr(self, "_tipwindow"):
            self._tipwindow.Enable(False)


    def GetThumbInfo(self, thumb=-1):
        """
        Returns the thumbnail information.

        :param `thumb`: the index of the thumbnail for which we are collecting information.
        """

        thumbinfo = None

        if thumb >= 0:
            thumbinfo = self._items[thumb].GetInfo() + \
                        "Thumb: " + str(self.GetThumbSize()[0:2])
        return thumbinfo

    def SetThumbSize(self, width, height, border=6):
        """
        Sets the thumbnail size as width, height and border.

        :param `width`: the desired thumbnail width;
        :param `height`: the desired thumbnail height;
        :param `border`: the spacing between thumbnails.
        """

        if width > 350 or height > 280:
            return

        self._tWidth = width
        self._tHeight = height
        self._tBorder = border
        self.SetScrollRate((self._tWidth + self._tBorder)//4,
                           (self._tHeight + self._tBorder)//4)
        self.SetSizeHints(self._tWidth + self._tBorder*2 + 16,
                          self._tHeight + self._tBorder*2 + 8)
        if self._items:
            self.UpdateShow()


    def GetThumbSize(self):
        """ Returns the thumbnail size as width, height and border. """

        return self._tWidth, self._tHeight, self._tBorder


    def Clear(self):
        """ Clears :class:`ThumbnailCtrl`. """

        self._items = []
        self._selected = -1
        self._selectedarray = []
        self.UpdateProp()
        self.Refresh()


    def ThreadImage(self, filenames):
        """
        Threaded method to load images. Used internally.

        :param `filenames`: a Python list of file names containing images.
        """

        count = 0

        while count < len(filenames):

            if not self._isrunning:
                self._isrunning = False
                thread.exit()
                return

            self.LoadImages(filenames[count], count)
            if count < 4:
                self.Refresh()
            elif count%4 == 0:
                self.Refresh()

            count = count + 1

        self._isrunning = False
        thread.exit()


    def LoadImages(self, newfile, imagecount):
        """
        Threaded method to load images. Used internally.

        :param `newfile`: a file name containing an image to thumbnail;
        :param `imagecount`: the number of images loaded until now.
        """

        if not self._isrunning:
            thread.exit()
            return

        self._items[imagecount].LoadImage()


    def ShowThumbs(self, thumbs):
        """
        Shows all the thumbnails.

        :param `thumbs`: should be a sequence with instances of :class:`Thumb`;
        """

        self._isrunning = False

        # update items
        self._items = thumbs
        myfiles = [thumb.GetFullFileName() for thumb in thumbs]

        self._isrunning = True

        thread.start_new_thread(self.ThreadImage, (myfiles,))
        wx.MilliSleep(20)

        self._selectedarray = []
        self.UpdateProp()
        self.Refresh()



    def SetSelection(self, value=-1):
        """
        Sets thumbnail selection.

        :param `value`: the thumbnail index to select.
        """

        self._selected = value

        if value != -1:
            self._selectedarray = [value]
            eventOut = ThumbnailEvent(wxEVT_THUMBNAILS_SEL_CHANGED, self.GetId())
            self.GetEventHandler().ProcessEvent(eventOut)
            self.ScrollToSelected()
            self.Refresh()


    def SetZoomFactor(self, zoom=1.4):
        """
        Sets the zoom factor.

        :param `zoom`: a floating point number representing the zoom factor. Must be
         greater than or equal to 1.0.
        """

        if zoom <= 1.0:
            raise Exception("\nERROR: Zoom Factor Must Be Greater Than 1.0")

        self._zoomfactor = zoom


    def GetZoomFactor(self):
        """ Returns the zoom factor. """

        return self._zoomfactor


    def UpdateItems(self):
        """ Updates thumbnail items. """

        selected = self._selectedarray
        selectedfname = []
        selecteditemid = []

        for ii in range(len(self._selectedarray)):
            selectedfname.append(self.GetSelectedItem(ii).GetFileName())
            selecteditemid.append(self.GetSelectedItem(ii).GetId())

        self.UpdateShow()

        if len(selected) > 0:
            self._selectedarray = []
            for ii in range(len(self._items)):
                for jj in range(len(selected)):
                    if self._items[ii].GetFileName() == selectedfname[jj] and \
                            self._items[ii].GetId() == selecteditemid[jj]:

                        self._selectedarray.append(ii)
                        if len(self._selectedarray) == 1:
                            self.ScrollToSelected()

            if len(self._selectedarray) > 0:
                self.Refresh()
                eventOut = ThumbnailEvent(wxEVT_THUMBNAILS_SEL_CHANGED, self.GetId())
                self.GetEventHandler().ProcessEvent(eventOut)


    def SetCaptionFont(self, font=None):
        """
        Sets the font for all the thumbnail captions.

        :param `font`: a valid :class:`wx.Font` object. If defaulted to ``None``, a standard
         font will be generated.
        """

        if font is None:
            font = wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False)

        self._captionfont = font


    def GetCaptionFont(self):
        """ Returns the font for all the thumbnail captions. """

        return self._captionfont


    def UpdateShow(self):
        """ Updates thumbnail items. """

        self.ShowThumbs(self._items)


    def GetCaptionHeight(self, begRow, count=1):
        """
        Returns the height for the file name caption.

        :param `begRow`: the caption line at which we start measuring the height;
        :param `count`: the number of lines to measure.
        """

        capHeight = 0
        for ii in range(begRow, begRow + count):
            if ii < len(self._tCaptionHeight):
                capHeight = capHeight + self._tCaptionHeight[ii]

        return capHeight*self._tTextHeight


    def GetItemIndex(self, x, y):
        """
        Returns the thumbnail index at position (x, y).

        :param `x`: the mouse `x` position;
        :param `y`: the mouse `y` position.
        """

        col = (x - self._tBorder)//(self._tWidth + self._tBorder)

        if col >= self._cols:
            col = self._cols - 1

        row = -1
        y = y - self._tBorder

        while y > 0:

            row = row + 1
            y = y - (self._tHeight + self._tBorder + self.GetCaptionHeight(row))

        if row < 0:
            row = 0

        index = row*self._cols + col

        if index >= len(self._items):
            index = -1

        return index


    def UpdateProp(self, checkSize=True):
        """
        Updates :class:`ThumbnailCtrl` and its visible thumbnails.

        :param `checkSize`: ``True`` to update the items visibility if the window
         size has changed.
        """

        width = self.GetClientSize().GetWidth()
        self._cols = (width - self._tBorder)//(self._tWidth + self._tBorder)

        if self._cols <= 0:
            self._cols = 1

        tmpvar = (len(self._items)%self._cols and [1] or [0])[0]
        self._rows = len(self._items)//self._cols + tmpvar

        self._tCaptionHeight = []

        for row in range(self._rows):

            capHeight = 0

            for col in range(self._cols):

                ii = row*self._cols + col

                if len(self._items) > ii and \
                        self._items[ii].GetCaptionLinesCount(self._tWidth - self._tCaptionBorder) > capHeight:

                    capHeight = self._items[ii].GetCaptionLinesCount(self._tWidth - self._tCaptionBorder)

            self._tCaptionHeight.append(capHeight)

        self.SetVirtualSize((self._cols*(self._tWidth + self._tBorder) + self._tBorder,
                             self._rows*(self._tHeight + self._tBorder) + \
                             self.GetCaptionHeight(0, self._rows) + self._tBorder))

        self.SetSizeHints(self._tWidth + 2*self._tBorder + 16,
                          self._tHeight + 2*self._tBorder + 8 + \
                          (self._rows and [self.GetCaptionHeight(0)] or [0])[0])

        if checkSize and width != self.GetClientSize().GetWidth():
            self.UpdateProp(False)


    def GetItem(self, pos):
        """
        Return thumbnail at specified position.

        :param pos: the index of the thumbnail
        :return:  the Thumb
        """

        return self._items[pos]

    def InsertItem(self, thumb, pos):
        """
        Inserts a thumbnail in the specified position.

        :param `pos`: the index at which we wish to insert the new thumbnail.
        """

        if pos < 0 or pos > len(self._items):
            self._items.append(thumb)
        else:
            self._items.insert(pos, thumb)

        self.UpdateProp()


    def RemoveItemAt(self, pos):
        """
        Removes a thumbnail at the specified position.

        :param `pos`: the index at which we wish to remove the thumbnail.
        """

        del self._items[pos]

        self.UpdateProp()


    def GetPaintRect(self):
        """ Returns the paint bounding rect for the :meth:`~ScrolledThumbnail.OnPaint` method. """

        size = self.GetClientSize()
        paintRect = wx.Rect(0, 0, size.GetWidth(), size.GetHeight())
        paintRect.x, paintRect.y = self.GetViewStart()
        xu, yu = self.GetScrollPixelsPerUnit()
        paintRect.x = paintRect.x*xu
        paintRect.y = paintRect.y*yu

        return paintRect


    def IsSelected(self, indx):
        """
        Returns whether a thumbnail is selected or not.

        :param `indx`: the index of the thumbnail to check for selection.
        """

        return self._selectedarray.count(indx) != 0


    def GetSelection(self, selIndex=-1):
        """
        Returns the selected thumbnail.

        :param `selIndex`: if not equal to -1, the index of the selected thumbnail.
        """

        return (selIndex == -1 and [self._selected] or
                [self._selectedarray[selIndex]])[0]


    def ScrollToSelected(self):
        """ Scrolls the :class:`ScrolledWindow` to the selected thumbnail. """

        if self.GetSelection() == -1:
            return

        # get row
        row = self.GetSelection()//self._cols
        # calc position to scroll view

        paintRect = self.GetPaintRect()
        y1 = row*(self._tHeight + self._tBorder) + self.GetCaptionHeight(0, row)
        y2 = y1 + self._tBorder + self._tHeight + self.GetCaptionHeight(row)

        if y1 < paintRect.GetTop():
            sy = y1 # scroll top
        elif y2 > paintRect.GetBottom():
            sy = y2 - paintRect.height # scroll bottom
        else:
            return

        # scroll view
        xu, yu = self.GetScrollPixelsPerUnit()
        sy = sy//yu + (sy%yu and [1] or [0])[0] # convert sy to scroll units
        x, y = self.GetViewStart()

        self.Scroll(x,sy)


    def CalculateBestCaption(self, dc, caption, sw, width):
        """
        Calculates the best caption string to show based on the actual zoom factor.

        :param `dc`: an instance of :class:`wx.DC`;
        :param `caption`: the original caption string;
        :param `sw`: the maximum width allowed for the caption string, in pixels;
        :param `width`: the caption string width, in pixels.
        """

        caption = caption + "..."

        while sw > width:
            caption = caption[1:]
            sw, sh = dc.GetTextExtent(caption)

        return "..." + caption[0:-3]


    def DrawThumbnail(self, bmp, thumb, index):
        """
        Draws a visible thumbnail.

        :param `bmp`: the thumbnail version of the original image;
        :param `thumb`: an instance of :class:`Thumb`;
        :param `index`: the index of the thumbnail to draw.
        """

        dc = wx.MemoryDC()
        dc.SelectObject(bmp)

        x = self._tBorder/2
        y = self._tBorder/2

        # background
        dc.SetPen(wx.Pen(wx.BLACK, 0, wx.TRANSPARENT))
        dc.SetBrush(wx.Brush(self.GetBackgroundColour(), wx.BRUSHSTYLE_SOLID))
        dc.DrawRectangle(0, 0, bmp.GetWidth(), bmp.GetHeight())

        # image
        if index == self.GetPointed() and self.GetHighlightPointed():
            factor = 1.5
            img = thumb.GetHighlightBitmap(self._tWidth, self._tHeight, factor)
        else:
            img = thumb.GetBitmap(self._tWidth, self._tHeight)

        ww = img.GetWidth()
        hh = img.GetHeight()
        imgRect = wx.Rect(int(x + (self._tWidth - img.GetWidth())/2),
                          int(y + (self._tHeight - img.GetHeight())/2),
                          img.GetWidth(), img.GetHeight())

        if not thumb._alpha and self._dropShadow:
            dc.Blit(imgRect.x+5, imgRect.y+5, imgRect.width, imgRect.height, self.shadow, 500-ww, 500-hh)
        dc.DrawBitmap(img, imgRect.x, imgRect.y, True)

        colour = self.GetSelectionColour()
        selected = self.IsSelected(index)

        colour = self.GetSelectionColour()

        # draw caption
        sw, sh = 0, 0
        if self._showfilenames:
            textWidth = 0
            dc.SetFont(self.GetCaptionFont())
            mycaption = thumb.GetCaption(0)
            sw, sh = dc.GetTextExtent(mycaption)

            if sw > self._tWidth:
                mycaption = self.CalculateBestCaption(dc, mycaption, sw, self._tWidth)
                sw = self._tWidth

            textWidth = sw + 8
            tx = x + (self._tWidth - textWidth)/2
            ty = y + self._tHeight

            txtcolour = "#7D7D7D"
            dc.SetTextForeground(txtcolour)

            tx = x + (self._tWidth - sw)/2
            if hh >= self._tHeight:
                ty = y + self._tHeight + (self._tTextHeight - sh)/2 + 3
            else:
                ty = y + hh + (self._tHeight-hh)/2 + (self._tTextHeight - sh)/2 + 3

            dc.DrawText(mycaption, int(tx), int(ty))

        # outline
        if self._tOutline != THUMB_OUTLINE_NONE and (self._tOutlineNotSelected or self.IsSelected(index)):

            dotrect = wx.Rect()
            dotrect.x = int(x) - 2
            dotrect.y = int(y) - 2
            dotrect.width = bmp.GetWidth() - self._tBorder + 4
            dotrect.height = bmp.GetHeight() - self._tBorder + 4

            dc.SetPen(wx.Pen((self.IsSelected(index) and [colour] or [wx.LIGHT_GREY])[0],
                             0, wx.PENSTYLE_SOLID))
            dc.SetBrush(wx.Brush(wx.BLACK, wx.BRUSHSTYLE_TRANSPARENT))

            if self._tOutline == THUMB_OUTLINE_FULL or self._tOutline == THUMB_OUTLINE_RECT:

                imgRect.x = int(x)
                imgRect.y = int(y)
                imgRect.width = bmp.GetWidth() - self._tBorder
                imgRect.height = bmp.GetHeight() - self._tBorder

                if self._tOutline == THUMB_OUTLINE_RECT:
                    imgRect.height = self._tHeight

            dc.SetBrush(wx.TRANSPARENT_BRUSH)

            if selected:

                dc.SetPen(self.grayPen)
                dc.DrawRoundedRectangle(dotrect, 2)

                dc.SetPen(wx.Pen(wx.WHITE))
                dc.DrawRectangle(imgRect.x, imgRect.y,
                                 imgRect.width, imgRect.height)

                pen = wx.Pen((selected and [colour] or [wx.LIGHT_GREY])[0], 2)
                pen.SetJoin(wx.JOIN_MITER)
                dc.SetPen(pen)
                if self._tOutline == THUMB_OUTLINE_FULL:
                    dc.DrawRoundedRectangle(imgRect.x - 1, imgRect.y - 1,
                                            imgRect.width + 3, imgRect.height + 3, 2)
                else:
                    dc.DrawRectangle(imgRect.x - 1, imgRect.y - 1,
                                     imgRect.width + 3, imgRect.height + 3)
            else:
                dc.SetPen(wx.Pen(wx.LIGHT_GREY))

                dc.DrawRectangle(imgRect.x - 1, imgRect.y - 1,
                                 imgRect.width + 2, imgRect.height + 2)


        dc.SelectObject(wx.NullBitmap)


    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`ThumbnailCtrl`.

        :param `event`: a :class:`PaintEvent` event to be processed.
        """

        paintRect = self.GetPaintRect()

        dc = wx.BufferedPaintDC(self)
        self.PrepareDC(dc)

        dc.SetPen(wx.Pen(wx.BLACK, 0, wx.PENSTYLE_TRANSPARENT))
        dc.SetBrush(wx.Brush(self.GetBackgroundColour(), wx.BRUSHSTYLE_SOLID))

        w, h = self.GetClientSize()

        # items
        row = -1
        xwhite = self._tBorder

        for ii in range(len(self._items)):

            col = ii%self._cols
            if col == 0:
                row = row + 1

            xwhite = ((w - self._cols*(self._tWidth + self._tBorder)))//(self._cols+1)
            tx = xwhite + col*(self._tWidth + self._tBorder)

            ty = self._tBorder//2 + row*(self._tHeight + self._tBorder) + \
                 self.GetCaptionHeight(0, row)
            tw = self._tWidth + self._tBorder
            th = self._tHeight + self.GetCaptionHeight(row) + self._tBorder
            # visible?
            if not paintRect.Intersects(wx.Rect(tx, ty, tw, th)):
                continue

            thmb = wx.Bitmap(tw, th)
            self.DrawThumbnail(thmb, self._items[ii], ii)
            dc.DrawBitmap(thmb, tx, ty)

        rect = wx.Rect(xwhite, self._tBorder//2,
                       self._cols*(self._tWidth + self._tBorder),
                       self._rows*(self._tHeight + self._tBorder) + \
                       self.GetCaptionHeight(0, self._rows))

        w = max(self.GetClientSize().GetWidth(), rect.width)
        h = max(self.GetClientSize().GetHeight(), rect.height)
        dc.DrawRectangle(0, 0, w, rect.y)
        dc.DrawRectangle(0, 0, rect.x, h)
        dc.DrawRectangle(rect.GetRight(), 0, w - rect.GetRight(), h + 50)
        dc.DrawRectangle(0, rect.GetBottom(), w, h - rect.GetBottom() + 50)

        col = len(self._items)%self._cols

        if col > 0:
            rect.x = rect.x + col*(self._tWidth + self._tBorder)
            rect.y = rect.y + (self._rows - 1)*(self._tHeight + self._tBorder) + \
                     self.GetCaptionHeight(0, self._rows - 1)
            dc.DrawRectangle(rect)


    def OnResize(self, event):
        """
        Handles the ``wx.EVT_SIZE`` event for :class:`ThumbnailCtrl`.

        :param `event`: a :class:`wx.SizeEvent` event to be processed.
        """

        self.UpdateProp()
        self.ScrollToSelected()
        self.Refresh()


    def OnMouseDown(self, event):
        """
        Handles the ``wx.EVT_LEFT_DOWN`` and ``wx.EVT_RIGHT_DOWN`` events for :class:`ThumbnailCtrl`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        x = event.GetX()
        y = event.GetY()
        x, y = self.CalcUnscrolledPosition(x, y)
        # get item number to select
        lastselected = self._selected
        self._selected = self.GetItemIndex(x, y)

        self._mouseeventhandled = False
        update = False

        if event.ControlDown():
            if self._selected == -1:
                self._mouseeventhandled = True
            elif not self.IsSelected(self._selected):
                self._selectedarray.append(self._selected)
                update = True
                self._mouseeventhandled = True

        elif event.ShiftDown():
            if self._selected != -1:
                begindex = self._selected
                endindex = lastselected
                if lastselected < self._selected:
                    begindex = lastselected
                    endindex = self._selected
                self._selectedarray = []

                for ii in range(begindex, endindex+1):
                    self._selectedarray.append(ii)

                update = True

            self._selected = lastselected
            self._mouseeventhandled = True

        else:

            if self._selected == -1:
                update = len(self._selectedarray) > 0
                self._selectedarray = []
                self._mouseeventhandled = True
            elif len(self._selectedarray) <= 1:
                try:
                    update = len(self._selectedarray)== 0 or self._selectedarray[0] != self._selected
                except:
                    update = True
                self._selectedarray = []
                self._selectedarray.append(self._selected)
                self._mouseeventhandled = True

        if update:
            self.ScrollToSelected()
            self.Refresh()
            eventOut = ThumbnailEvent(wxEVT_THUMBNAILS_SEL_CHANGED, self.GetId())
            self.GetEventHandler().ProcessEvent(eventOut)

        self.SetFocus()


    def OnMouseUp(self, event):
        """
        Handles the ``wx.EVT_LEFT_UP`` and ``wx.EVT_RIGHT_UP`` events for :class:`ThumbnailCtrl`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        # get item number to select
        x = event.GetX()
        y = event.GetY()
        x, y = self.CalcUnscrolledPosition(x, y)
        lastselected = self._selected
        self._selected = self.GetItemIndex(x,y)

        if not self._mouseeventhandled:
            # set new selection
            if event.ControlDown():
                if self._selected in self._selectedarray:
                    self._selectedarray.remove(self._selected)

                self._selected = -1
            else:
                self._selectedarray = []
                self._selectedarray.append(self._selected)

            self.ScrollToSelected()
            self.Refresh()
            eventOut = ThumbnailEvent(wxEVT_THUMBNAILS_SEL_CHANGED, self.GetId())
            self.GetEventHandler().ProcessEvent(eventOut)

        # Popup menu
        if event.RightUp():
            if self._selected >= 0 and self._pmenu:
                self.PopupMenu(self._pmenu)
            elif self._selected >= 0 and not self._pmenu and self._gpmenu:
                self.PopupMenu(self._gpmenu)
            elif self._selected == -1 and self._gpmenu:
                self.PopupMenu(self._gpmenu)

        if event.ShiftDown():
            self._selected = lastselected


    def OnMouseDClick(self, event):
        """
        Handles the ``wx.EVT_LEFT_DCLICK`` event for :class:`ThumbnailCtrl`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        eventOut = ThumbnailEvent(wxEVT_THUMBNAILS_DCLICK, self.GetId())
        self.GetEventHandler().ProcessEvent(eventOut)


    def OnMouseMove(self, event):
        """
        Handles the ``wx.EVT_MOTION`` event for :class:`ThumbnailCtrl`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        # -- drag & drop --
        if self._dragging and event.Dragging() and len(self._selectedarray) > 0:

            files = wx.FileDataObject()
            for ii in range(len(self._selectedarray)):
                files.AddFile(opj(self.GetSelectedItem(ii).GetFullFileName()))

            source = wx.DropSource(self)
            source.SetData(files)
            source.DoDragDrop(wx.Drag_DefaultMove)

        # -- light-effect --
        x = event.GetX()
        y = event.GetY()
        x, y = self.CalcUnscrolledPosition(x, y)

        # get item number
        sel = self.GetItemIndex(x, y)

        if sel == self._pointed:
            if self._enabletooltip and sel >= 0:
                if not hasattr(self, "_tipwindow"):
                    self._tipwindow = wx.ToolTip(self.GetThumbInfo(sel))
                    self._tipwindow.SetDelay(1000)
                    self.SetToolTip(self._tipwindow)
                else:
                    self._tipwindow.SetDelay(1000)
                    self._tipwindow.SetTip(self.GetThumbInfo(sel))

            event.Skip()
            return

        if self._enabletooltip:
            if hasattr(self, "_tipwindow"):
                self._tipwindow.Enable(False)

        # update thumbnail
        self._pointed = sel

        if self._enabletooltip and sel >= 0:
            if not hasattr(self, "_tipwindow"):
                self._tipwindow = wx.ToolTip(self.GetThumbInfo(sel))
                self._tipwindow.SetDelay(1000)
                self._tipwindow.Enable(True)
                self.SetToolTip(self._tipwindow)
            else:
                self._tipwindow.SetDelay(1000)
                self._tipwindow.Enable(True)
                self._tipwindow.SetTip(self.GetThumbInfo(sel))

        self.Refresh()
        eventOut = ThumbnailEvent(wxEVT_THUMBNAILS_POINTED, self.GetId())
        self.GetEventHandler().ProcessEvent(eventOut)
        event.Skip()


    def OnMouseLeave(self, event):
        """
        Handles the ``wx.EVT_LEAVE_WINDOW`` event for :class:`ThumbnailCtrl`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if self._pointed != -1:

            self._pointed = -1
            self.Refresh()
            eventOut = ThumbnailEvent(wxEVT_THUMBNAILS_POINTED, self.GetId())
            self.GetEventHandler().ProcessEvent(eventOut)


    def OnThumbChanged(self, event):
        """
        Handles the ``EVT_THUMBNAILS_THUMB_CHANGED`` event for :class:`ThumbnailCtrl`.

        :param `event`: a :class:`ThumbnailEvent` event to be processed.
        """

        for ii in range(len(self._items)):
            if self._items[ii].GetFileName() == event.GetString():

                self._items[ii].SetFilename(self._items[ii].GetFileName())
                if event.GetClientData():

                    img = wx.Image(event.GetClientData())
                    self._items[ii].SetImage(img)

        self.Refresh()


    def OnChar(self, event):
        """
        Handles the ``wx.EVT_CHAR`` event for :class:`ThumbnailCtrl`.

        :param `event`: a :class:`KeyEvent` event to be processed.

        :note: You have these choices:

         (1) ``d`` key rotates 90 degrees clockwise the selected thumbnails;
         (2) ``s`` key rotates 90 degrees counter-clockwise the selected thumbnails;
         (3) ``a`` key rotates 180 degrees the selected thumbnails;
         (4) ``+`` key zooms in;
         (5) ``-`` key zooms out.
         All other keys cause an EVT_THUMBNAILS_CHAR event to be thrown.
        """

        if event.KeyCode == ord("s"):
            self.Rotate()
        elif event.KeyCode == ord("d"):
            self.Rotate(270)
        elif event.KeyCode == ord("a"):
            self.Rotate(180)
        elif event.KeyCode in [wx.WXK_ADD, wx.WXK_NUMPAD_ADD]:
            self.ZoomIn()
        elif event.KeyCode in [wx.WXK_SUBTRACT, wx.WXK_NUMPAD_SUBTRACT]:
            self.ZoomOut()

        selected = []
        for ii in range(len(self._items)):
            if self.IsSelected(ii):
                selected.append(ii)

        eventOut = ThumbnailEvent(wxEVT_THUMBNAILS_CHAR, self.GetId(),
                                  thumbs=selected, keycode=event.KeyCode)
        self.GetEventHandler().ProcessEvent(eventOut)

        event.Skip()

    def Rotate(self, angle=90):
        """
        Rotates the selected thumbnails by the angle specified by `angle`.

        :param `angle`: the rotation angle for the thumbnail, in degrees.
        """

        wx.BeginBusyCursor()

        selected = []
        for ii in range(len(self._items)):
            if self.IsSelected(ii):
                selected.append(self._items[ii])

        for thumb in selected:
            thumb.Rotate(angle)

        wx.EndBusyCursor()

        if self.GetSelection() != -1:
            self.Refresh()


    def OnMouseWheel(self, event):
        """
        Handles the ``wx.EVT_MOUSEWHEEL`` event for :class:`ThumbnailCtrl`.

        :param `event`: a :class:`MouseEvent` event to be processed.

        :note: If you hold down the ``Ctrl`` key, you can zoom in/out with the mouse wheel.
        """

        if event.ControlDown():
            if event.GetWheelRotation() > 0:
                self.ZoomIn()
            else:
                self.ZoomOut()
        else:
            event.Skip()


    def ZoomOut(self):
        """ Zooms the thumbnails out. """

        w, h, b = self.GetThumbSize()

        if w < 40 or h < 40:
            return

        zoom = self.GetZoomFactor()
        neww = float(w)/zoom
        newh = float(h)/zoom

        self.SetThumbSize(int(neww), int(newh))
        self.OnResize(None)
        self._checktext = True

        self.Refresh()


    def ZoomIn(self):
        """ Zooms the thumbnails in. """

        size = self.GetClientSize()
        w, h, b = self.GetThumbSize()
        zoom = self.GetZoomFactor()

        if w*zoom + b > size.GetWidth() or h*zoom + b > size.GetHeight():
            if w*zoom + b > size.GetWidth():
                neww = size.GetWidth() - 2*self._tBorder
                newh = (float(h)/w)*neww
            else:
                newh = size.GetHeight() - 2*self._tBorder
                neww = (float(w)/h)*newh

        else:
            neww = float(w)*zoom
            newh = float(h)*zoom

        self.SetThumbSize(int(neww), int(newh))
        self.OnResize(None)
        self._checktext = True

        self.Refresh()


# ---------------------------------------------------------------------------- #
# Class ThumbnailEvent
# ---------------------------------------------------------------------------- #

class ThumbnailEvent(wx.PyCommandEvent):
    """
    This class is used to send events when a thumbnail is hovered, selected,
    double-clicked or when its caption has been changed.
    """
    def __init__(self, evtType, evtId=-1, thumbs=None, keycode=None):
        """
        Default class constructor.

        :param `evtType`: the event type;
        :param `evtId`: the event identifier.
        """

        wx.PyCommandEvent.__init__(self, evtType, evtId)
        self.thumbs = thumbs
        self.keycode = keycode
