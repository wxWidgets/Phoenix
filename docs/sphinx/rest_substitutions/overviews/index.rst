.. wxPython (Phoenix) documentation master file, created by
   sphinx-quickstart on Fri Dec 09 11:27:02 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==============================================
Welcome to wxPython (Phoenix)'s documentation!
==============================================


wxPython
========

wxPython is a **GUI toolkit** for the `Python <http://www.python.org/>`_ programming language. It allows Python programmers to 
create programs with a robust, highly functional graphical user interface, simply and easily. 

.. figure:: _static/images/sphinxdocs/central_bar.png
   :align: center


|

What is wxPython
----------------

wxPython is a **GUI toolkit** for the `Python <http://www.python.org/>`_ programming language. It allows Python programmers to 
create programs with a robust, highly functional graphical user interface, simply and easily. 
It is implemented as a Python extension module (native code) that wraps the popular `wxWidgets <http://wxwidgets.org/>`_ cross 
platform GUI library, which is written in C++. 

Like Python and wxWidgets, wxPython is *Open Source* which means that it is free for anyone to use and 
the source code is available for anyone to look at and modify. Or anyone can contribute fixes or 
enhancements to the project. 

wxPython is a *cross-platform* toolkit. This means that the same program will run on multiple platforms 
without modification. Currently supported platforms are 32-bit Microsoft Windows, most Unix or unix-like 
systems, and Macintosh OS X+, in most cases the native widgets are used on each platform.

Since the language is Python, wxPython programs are **simple, easy** to write and easy to understand.

As an example, this is a simple "Hello World" program with wxPython::

    import wx

    app = wx.App()

    frame = wx.Frame(None, -1, "Hello World")
    frame.Show()

    app.MainLoop()


The GUI layouts you can build with wxPython are almost infinite: it has an extremely rich set of widgets (derived from `wxWidgets`) and
greatly extended by a huge set of pure-Python controls written over the years.

 
Prerequisites
-------------

Like any other complex piece of software, wxPython requires other software in order to function properly. 
Obviously you'll need `Python <http://www.python.org/>`_ itself, but if you're reading this you've probably already got 
Python and are just here looking for the `best GUI toolkit <http://www.wxpython.org/quotes.php>`_ available for Python. 
Check out the details for your platform of choice here: 

Win32
^^^^^

* If you have a modern up to date version of Windows and use the binary installer for wxPython found below, you probably 
  don't need anything else. 

* If your tree controls have strange background colors, try loading this `MS Common Controls Update <http://download.microsoft.com/download/platformsdk/Comctl32/5.80.2614.3600/W9XNT4/EN-US/50comupd.exe>`_ 
  as wxWidgets does something that causes a bug in one of the older versions to manifest itself. Another way to get this update 
  is to install Internet Explorer or MS Office apps, so if the system has those already then you probably don't need to worry about this. 

* wxPython's `wx.glcanvas.GLCanvas` class only provides the GL Context and a wx.Window to put it in, so if you want to use 
  the wxGLCanvas you will also need the `PyOpenGL <http://pyopengl.sourceforge.net/>`_ Python extension modules as well. 


Linux/Unix/Etc.
^^^^^^^^^^^^^^^

* The first thing you'll need are the `glib and gtk+ <http://www.gtk.org/>`_ libraries. Before you run off and download the sources 
  check your system, you probably already have it. Most distributions of Linux come with it and you'll start seeing it on many 
  other systems too now that Sun and others have chosen GNOME as the desktop of choice. If you don't have glib and gtk+ already, 
  you can get the sources `here <ftp://ftp.gtk.org/pub/gtk/>`_. Build and install them following the directions included. 

* In order to use the wxGLCanvas you'll need to have either OpenGL or the `Mesa3D <http://www.mesa3d.org/>`_ library on your system. 
  wxPython's `wx.glcanvas.GLCanvas` only provides the GL Context and a :class:`Window` to put it in, so you will also need the PyOpenGL 
  Python extension modules as well, if you want to use OpenGL. 

  If you are building wxPython yourself and don't care to use OpenGL/Mesa then you can easily skip building it and can ignore 
  this step. See the `build instructions <http://www.wxpython.org/BUILD.html>`_ for details. 


Mac OS X
^^^^^^^^

The wxPython binaries for OSX are mountable disk images. Simply double click to mount the image and then run the installer application
in the image. Download the image that matches the version of Python that you want to use it with, and unless you know for sure that you
need the ansi build please get the Unicode build. 

These binaries should work on all versions of OSX from 10.3.9 onwards on either PPC or i386 architectures. Since they use the Carbon API
 they are limited to running in 32-bit mode.


OK, I'm interested. What do I do next?
--------------------------------------

You can download the `Prebuild binary of wxPython
<http://www.wxpython.org/download.php#binaries>`_ which includes
the source code for wxPython.

Prebuilt binaries are available for Microsoft Windows, Linux and Mac OS X.

Don't forget to download the wxPython demo and the documentation!


Bleeding-edge source
--------------------

If you are a very keen developer, you can access the SVN repository directly for this
project in the `wxWidgets SVN <http://svn.wxwidgets.org/viewvc/wx/wxPython>`_.



wxPython Documentation
----------------------

The new wxPython API documentation is available `in this page <main.html>`_.


.. toctree::
   :maxdepth: 2
   :hidden:
   :glob:
   
   MigrationGuide
   TODO
   DocstringsGuidelines
   functions
   1classindex
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
   html_overview
   internationalization
   writing_non_english_applications
   listctrl_overview
   log_classes_overview
   printing_framework_overview
   refcount_overview
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
   adv.1classindex
   adv.functions
   dataview.1classindex
   glcanvas.1classindex
   grid.1classindex
   html.1classindex
   html.functions
   html2.1classindex
   stc.1classindex
   xml.1classindex
   xrc.1classindex
   xrc.functions
   lib
   py
   tools


Indices and tables
==================

* `genindex`
* `modindex`
* `search`

