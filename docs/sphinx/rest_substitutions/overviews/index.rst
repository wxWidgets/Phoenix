.. wxPython Phoenix documentation
   Created:   9-Dec-2011
   Copyright: (c) 2011-2016 by Total Control Software
   License:   wxWindows License

=======================================
Welcome to the wxPython Phoenix Project
=======================================


wxPython
========

wxPython is a **GUI toolkit** for the `Python <http://www.python.org/>`_
programming language. It allows Python programmers to create programs with a
robust, highly functional graphical user interface, simply and easily.

.. figure:: _static/images/sphinxdocs/central_bar.png
   :align: center


|

What is wxPython
----------------

wxPython is a **GUI toolkit** for the `Python <http://www.python.org/>`_
programming language. It allows Python programmers to create programs with a
robust, highly functional graphical user interface, simply and easily. It is
implemented as a Python extension module (native code) that wraps the popular
`wxWidgets <http://wxwidgets.org/>`_ cross platform GUI library, which is
written in C++.

Like Python and wxWidgets, wxPython is *Open Source* which means that it is
free for anyone to use and the source code is available for anyone to look at
and modify. Or anyone can contribute fixes or enhancements to the project.

wxPython is a *cross-platform* toolkit. This means that the same program will
run on multiple platforms without modification. Currently supported platforms
are 32-bit Microsoft Windows, most Unix or unix-like systems, and Macintosh OS
X+, in most cases the native widgets are used on each platform.

Since the language is Python, wxPython programs are **simple, easy** to write
and easy to understand.

As an example, this is a simple "Hello World" program with wxPython::

    import wx

    app = wx.App()

    frame = wx.Frame(None, -1, "Hello World")
    frame.Show()

    app.MainLoop()


The GUI layouts you can build with wxPython are almost infinite: it has an
extremely rich set of widgets (derived from `wxWidgets`) and greatly extended
by a huge set of pure-Python controls written over the years.


What is wxPython Phoenix?
-------------------------

**Phoenix** is the code name of a new implementation of wxPython.  The name comes
from the `mythical bird <https://en.wikipedia.org/wiki/Phoenix_(mythology)>`_
that bursts into flames at the end of its life and from the ashes is reborn as
a new, stronger, and better phoenix.  Likewise the intent with the
*wxPython Phoenix* project is throw almost everything from *wxPython Classic*
into the fire to be built anew from the ashes of its former self, without all
of the old crud that had built up over the long life of Classic.

Much of that crud were rather hacky things which had to be done to
work around limitations of the technology available at the time.  Those are
easy to get rid of.  Others are things that seemed good at the time, but in
retrospect turned out to be bad ideas.  Some of those are a little more
tricky, but still a good idea to change.  The end result will be a new
wxPython that is better, stronger, and faster than he was before, and which is
easier to maintain, extend and document.

Although there hasn't been a formal release yet, Phoenix is already in a
usable state with snapshot builds available after new commits are merged,
and is in active use on a number of projects already.  Progress is still being
made and an official release is on the way.  Stay tuned to the wxPython
developer and user groups for more information and announcements.

Meanwhile, here are some important links:

  * The `MigrationGuide <MigrationGuide.html>`_ will help you understand the
    differences between wxPython Phoenix and Classic.  In addition,
    `classic_vs_phoenix <classic_vs_phoenix.html>`_ documents
    some names that have been changed, or which haven't yet been ported to
    Phoenix.

  * The new wxPython API documentation is available `here <main.html>`_.

  * The `Project Phoenix <http://wiki.wxpython.org/ProjectPhoenix>`_ section
    of the wxPython wiki has information about the background of, and reasons
    for this project, as well as information for developers who want to help
    out.

  * Source code and issue tracking are available at the
    `Phoenix GitHub <https://github.com/wxWidgets/Phoenix>`_ repository. Be
    sure to read the README.rst file there to learn how to build wxWidgets and
    Phoenix for yourself.




.. toctree::
   :maxdepth: 2
   :hidden:
   :glob:
   
   MigrationGuide
   TODO
   DocstringsGuidelines
   wx.functions
   wx.1moduleindex
   app_overview
   bitmap_overview
   bookctrl_overview
   command_overview
   common_dialogs_overview
   config_overview
   dataobject_overview
   datetime_overview
   dc_overview
   dialog_overview
   dnd_overview
   events_overview
   filesystem_overview
   font_encodings
   font_overview
   grid_overview
   html_overview
   internationalization
   writing_non_english_applications
   listctrl_overview
   log_classes_overview
   printing_framework_overview
   refcount_overview
   richtextctrl_overview
   scrolling_overview
   sizers_overview
   splitterwindow_overview
   standard_event_identifiers
   stock_items
   tipprovider_overview
   toolbar_overview
   treectrl_overview
   validator_overview
   window_deletion_overview
   window_ids_overview
   window_sizing_overview
   window_styles_overview
   wx.adv.1moduleindex
   wx.adv.functions
   wx.dataview.1moduleindex
   wx.glcanvas.1moduleindex
   wx.grid.1moduleindex
   wx.html.1moduleindex
   wx.html.functions
   wx.html2.1moduleindex
   wx.richtext.1moduleindex
   wx.richtext.functions
   wx.stc.1moduleindex
   wx.webkit.1moduleindex
   wx.xml.1moduleindex
   wx.xrc.1moduleindex
   wx.xrc.functions
   wx.media.1moduleindex
   wx.msw.1moduleindex
   wx.ribbon.1moduleindex
   wx.aui.1moduleindex
   wx.propgrid.1moduleindex
   wx.lib
   wx.py
   wx.tools


