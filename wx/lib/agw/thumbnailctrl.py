# --------------------------------------------------------------------------- #
# THUMBNAILCTRL Control wxPython IMPLEMENTATION
# Python Code By:
#
# Andrea Gavana And Peter Damoc, @ 12 Dec 2005
# Latest Revision: 27 Dec 2012, 21.00 GMT
# andrea.gavana@gmail.com
# andrea.gavana@maerskoil.com
#
# Refactored and reorganized:  Michael Eager (eager@eagercon.com), 26 Sep 2020
#
# Tags:         phoenix-port, documented, unittest, py3-port
#
# End Of Comments
# --------------------------------------------------------------------------- #


"""
:class:`~wx.lib.agw.thumbnailctrl.ThumbnailCtrl` is a widget that can be used to display a series of images in
a "thumbnail" format.


Description
===========

:class:`ThumbnailCtrl` is a widget that can be used to display a series of images in
a "thumbnail" format; it mimics, for example, the windows explorer behavior
when you select the "view thumbnails" option.
Basically, by specifying a folder that contains some image files, the files
in the folder are displayed as miniature versions of the actual images in
a :class:`ScrolledWindow`.

The code is partly based on `wxVillaLib`, a wxWidgets implementation of this
control. However, :class:`ThumbnailCtrl` wouldn't have been so fast and complete
without the suggestions and hints from Peter Damoc. So, if he accepts the
mention, this control is his as much as mine.

:class:`ThumbnailCtrl` is more of a demo application than a widget.
The :class:`ScrolledThumbnail` is a freestanding widget, accepting a list of
:class:`Thumb` objects which represent files and which returns a thumbnail
on request.  :class:`Thumb` can be extended by the user to provide thumbnails
for other data types, such as text, audio, video, or PDF files.

Usage
=====

Usage example::

    import os

    import wx
    import wx.lib.agw.thumbnailctrl as TC

    class MyFrame(wx.Frame):

        def __init__(self, parent):

            wx.Frame.__init__(self, parent, -1, "ThumbnailCtrl Demo")

            panel = wx.Panel(self)

            sizer = wx.BoxSizer(wx.VERTICAL)

            thumbnail = TC.ThumbnailCtrl(panel, imagehandler=TC.NativeImageHandler)
            sizer.Add(thumbnail, 1, wx.EXPAND | wx.ALL, 10)

            thumbnail.ShowDir(os.getcwd())
            panel.SetSizer(sizer)


    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()



Methods and Settings
====================

With :class:`ThumbnailCtrl` you can:

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

- Delete files/thumbnails (via the ``del`` key);
- Drag and drop thumbnails from :class:`ThumbnailCtrl` to whatever application you want;
- Use local (when at least one thumbnail is selected) or global (no need for
  thumbnail selection) popup menus;
- Show/hide a :class:`ComboBox` at the top of :class:`ThumbnailCtrl`: this combobox contains
  working directory information and it has history entries;
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

================================== ==================================================
Event Name                         Description
================================== ==================================================
``EVT_THUMBNAILS_DCLICK``          The user has double-clicked on a thumbnail.
``EVT_THUMBNAILS_POINTED``         The mouse cursor is hovering over a thumbnail.
``EVT_THUMBNAILS_SEL_CHANGED``     The user has changed the selected thumbnail.
``EVT_THUMBNAILS_THUMB_CHANGED``   The thumbnail of an image has changed. Used internally.
``EVT_THUMBNAILS_CHAR``            A key was typed in the widget
================================== ==================================================


License And Version
===================

:class:`ThumbnailCtrl` is distributed under the wxPython license.

Latest revision: Michael Eager @ 26 Sep 2020

Version 1.0

"""


#----------------------------------------------------------------------
# Beginning Of ThumbnailCtrl wxPython Code
#----------------------------------------------------------------------

import wx
import os
import time

from wx.lib.agw.scrolledthumbnail import (ScrolledThumbnail, EVT_THUMBNAILS_CHAR,
PILImageHandler, NativeImageHandler, Thumb)

# Image File Name Extensions: Am I Missing Some Extensions Here?
extensions = [".jpeg", ".jpg", ".bmp", ".png", ".ico", ".tiff", ".ani", ".cur", ".gif",
              ".iff", ".icon", ".pcx", ".tif", ".xpm", ".xbm", ".mpeg", ".mpg", ".mov"]

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

# Options For Filtering Files -- Not used, provided for backward-compatiblity
THUMB_FILTER_IMAGES = 1

TIME_FMT = '%d %b %Y, %H:%M:%S'
""" Time format string for the :class:`Thumb` representation on screen. """


# ---------------------------------------------------------------------------- #
# Class ScrolledTextDialog
# Create dialog with scrolling text box
# ---------------------------------------------------------------------------- #

class ScrolledTextDialog(wx.Dialog):
    """
    :class:`ScrolledTextDialog` is a dialog widget which displays a scrolled
    text box and OK/CANCEL buttons.
    """

    def __init__(self, parent, title="Title", msg="Message"):
        wx.Dialog.__init__(self, parent, title=title)

        text = wx.TextCtrl(self, -1, msg, size=(600,240),
                           style=wx.TE_MULTILINE|wx.TE_DONTWRAP|wx.TE_READONLY)
        sizer = wx.BoxSizer(wx.VERTICAL)
        buttonsizer = wx.BoxSizer()
        OKbutton = wx.Button(self, wx.ID_OK)
        buttonsizer.Add(OKbutton, 0, wx.ALL, 5)
        buttonsizer.Add((5,-1), 0, wx.ALL, 5)
        CANCELbutton = wx.Button(self, wx.ID_CANCEL)
        buttonsizer.Add(CANCELbutton, 0, wx.ALL, 5)
        sizer.Add(text, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(buttonsizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.SetSizerAndFit(sizer)



# ---------------------------------------------------------------------------- #
# Class ThumbnailCtrl
# Auxiliary Class, All Useful Methods Are Defined On ScrolledThumbnail Class.
# ---------------------------------------------------------------------------- #

class ThumbnailCtrl(wx.Panel):
    """
    :class:`ThumbnailCtrl` is a widget that can be used to display a series of images in
    a "thumbnail" format.
    """

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, thumboutline=THUMB_OUTLINE_IMAGE,
                 thumbfilter=None,   # Ignored, included for backward compatibility
                 imagehandler=PILImageHandler):
        """
        Default class constructor.

        :param `parent`: parent window. Must not be ``None``;
        :param `id`: window identifier. A value of -1 indicates a default value;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `thumboutline`: outline style for :class:`ThumbnailCtrl`, which may be:

         =========================== ======= ==================================
         Outline Flag                 Value  Description
         =========================== ======= ==================================
         ``THUMB_OUTLINE_NONE``            0 No outline is drawn on selection
         ``THUMB_OUTLINE_FULL``            1 Full outline (image+caption) is drawn on selection
         ``THUMB_OUTLINE_RECT``            2 Only thumbnail bounding rectangle is drawn on selection (default)
         ``THUMB_OUTLINE_IMAGE``           4 Only image bounding rectangle is drawn.
         =========================== ======= ==================================

        :param `thumbfilter`: filter for image/video/audio files.  Ignored.
        :param `imagehandler`: can be :class:`PILImageHandler` if PIL is installed (faster), or
         :class:`NativeImageHandler` which only uses wxPython image methods.
        """

        wx.Panel.__init__(self, parent, id, pos, size)

        self._sizer = wx.BoxSizer(wx.VERTICAL)

        self._combo = wx.ComboBox(self, -1, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self._scrolled = ScrolledThumbnail(self, -1, thumboutline=thumboutline,
                                           imagehandler = imagehandler)

        subsizer = wx.BoxSizer(wx.HORIZONTAL)
        subsizer.Add((3, 0), 0)
        subsizer.Add(self._combo, 0, wx.EXPAND | wx.TOP, 3)
        subsizer.Add((3, 0), 0)
        self._sizer.Add(subsizer, 0, wx.EXPAND | wx.ALL, 3)
        self._sizer.Add(self._scrolled, 1, wx.EXPAND)

        self.SetSizer(self._sizer)

        self._sizer.Show(0, False)
        self._sizer.Layout()

        methods = ["GetSelectedItem", "GetPointed", "GetHighlightPointed", "SetHighlightPointed",
                   "SetThumbOutline", "GetThumbOutline", "GetPointedItem", "GetItem",
                   "GetItemCount", "GetThumbWidth", "GetThumbHeight", "GetThumbBorder",
                   "SetPopupMenu", "GetPopupMenu", "SetGlobalPopupMenu",
                   "GetGlobalPopupMenu", "SetSelectionColour", "GetSelectionColour",
                   "EnableDragging", "SetThumbSize", "GetThumbSize", "ShowThumbs",
                   "SetSelection", "GetSelection", "SetZoomFactor",
                   "GetZoomFactor", "SetCaptionFont", "GetCaptionFont", "GetItemIndex",
                   "InsertItem", "RemoveItemAt", "IsSelected", "Rotate", "ZoomIn", "ZoomOut",
                   "EnableToolTips", "GetThumbInfo", "SetDropShadow", "GetDropShadow"]

        for method in methods:
            setattr(self, method, getattr(self._scrolled, method))

        self._combochoices = []
        self._showcombo = False
        self._subsizer = subsizer

        self._combo.Bind(wx.EVT_COMBOBOX, self.OnComboBox)
        self.Bind(EVT_THUMBNAILS_CHAR, self.OnThumbChar)

        self._imagehandler = imagehandler


    def ShowComboBox(self, show=True):
        """
        Shows/Hide the top folder :class:`ComboBox`.

        :param `show`: ``True`` to show the combobox, ``False`` otherwise.
        """

        if show:
            self._showcombo = True
            self._sizer.Show(0, True)
            self._sizer.Layout()
        else:
            self._showcombo = False
            self._sizer.Show(0, False)
            self._sizer.Layout()

        self._scrolled.Refresh()


    def GetShowComboBox(self):
        """ Returns whether the folder combobox is shown. """

        return self._showcombo


    def OnComboBox(self, event):
        """
        Handles the ``wx.EVT_COMBOBOX`` for the folder combobox.

        :param `event`: a :class:`CommandEvent` event to be processed.
        """

        dirs = self._combo.GetValue()

        if os.path.isdir(opj(dirs)):
            self._scrolled.ShowDir(opj(dirs))

        event.Skip()


    def RecreateComboBox(self, newdir):
        """
        Recreates the folder combobox every time a new directory is explored.

        :param `newdir`: the new folder to be explored.
        """

        newdir = newdir.strip()

        if opj(newdir) in self._combochoices:
            return

        self.Freeze()

        self._sizer.Detach(0)
        self._subsizer.Detach(1)
        self._subsizer.Destroy()
        self._combo.Destroy()

        subsizer = wx.BoxSizer(wx.HORIZONTAL)

        self._combochoices.insert(0, opj(newdir))

        self._combo = wx.ComboBox(self, -1, value=newdir, choices=self._combochoices,
                                  style=wx.CB_DROPDOWN | wx.CB_READONLY)

        subsizer.Add((3, 0), 0)
        subsizer.Add(self._combo, 1, wx.EXPAND | wx.TOP, 3)
        subsizer.Add((3, 0), 0)
        self._sizer.Insert(0, subsizer, 0, wx.EXPAND | wx.ALL, 3)

        self._subsizer = subsizer

        self._subsizer.Layout()

        if not self.GetShowComboBox():
            self._sizer.Show(0, False)

        self._sizer.Layout()

        self._combo.Bind(wx.EVT_COMBOBOX, self.OnComboBox)

        self.Thaw()


    def SetBackgroundColour(self, colour):
        """
        Set the background color of the widget.

        :param `colour`: the color to which the background is set.
        """
        return self.thumbnail_ctrl._scrolled.SetBackgroundColour(colour)


    def ShowDir(self, folder):
        """
        Shows thumbnails for a particular folder.

        :param `folder`: a directory containing the images to thumbnail;
        """

        self._dir = folder

        self.RecreateComboBox(folder)

        # update items
        thumbs = []

        filenames = self.ListDirectory(self._dir, extensions)

        filenames.sort()
        for files in filenames:

            caption = (self._showfilenames and [files] or [""])[0]
            fullfile = opj(self._dir + "/" + files)
            if not os.path.isfile(fullfile):
                continue

            stats = os.stat(fullfile)
            size = stats[6]

            lastmod = time.strftime(TIME_FMT, time.localtime(stats[8]))

            thumbs.append(Thumb(folder, files, caption, size, lastmod,
                                imagehandler=self._imagehandler))

        return self.ShowThumbs(thumbs)


    def GetShowDir(self):
        """ Returns the working directory with images. """

        return self._dir

    def ListDirectory(self, directory, fileExtList):
        """
        Returns list of file info objects for files of particular extensions.

        :param `directory`: the folder containing the images to thumbnail;
        :param `fileExtList`: a Python list of file extensions to consider.
        """

        lSplitExt = os.path.splitext
        return [f for f in os.listdir(directory) if lSplitExt(f)[1].lower() in fileExtList]


    def ShowFileNames(self, show=True):
        """
        Sets whether the user wants to show file names under the thumbnails or not.

        :param `show`: ``True`` to show file names under the thumbnails, ``False`` otherwise.
        """

        self._showfilenames = show
        self._scrolled.ShowFileNames(show)


    def OnThumbChar(self, ev):
        for th in ev.thumbs:
            thumb = self._scrolled.GetItem(th)

        if ev.keycode == wx.WXK_DELETE:
            self.DeleteFiles(ev.thumbs)

    def DeleteFiles(self, thumbs):
        """
        Deletes the selected thumbnails and their associated files.
        .. warning:: This method deletes the original files too.

        :param `thumbs`:  List of indexes to thumbnails.

        """

        msg = ""
        for index in thumbs:
            thumb = self._scrolled.GetItem(index)
            msg += thumb.GetFileName() + '\n'

        dlg = ScrolledTextDialog(self, 'Delete these files?', msg)

        if dlg.ShowModal() == wx.ID_OK:
            errordelete = []
            count = 0

            dlg.Destroy()

            wx.BeginBusyCursor()

            # Delete thumbnails & files from highest index to lowest
            for index in reversed(thumbs):
                thumb = self._scrolled.GetItem(index)
                filename = thumb.GetFullFileName()
                try:
                    os.remove(filename)
                    self._scrolled.RemoveItemAt(index)
                    count = count + 1
                except:
                    errordelete.append(self._scrolled.GetFileName(index))

            wx.EndBusyCursor()

            if errordelete:
                strs = "Unable to remove the following files:\n\n"
                for fil in errordelete:
                    strs = strs + fil + "\n"
                strs = strs + "\n"
                strs = strs + "Please check your privileges and file permissions."
                dlg = wx.MessageDialog(self, strs,
                                       'Error in removing files',
                                       wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()
