.. include:: headings.inc


.. _bookctrl overview:

======================================
|phoenix_title|  **BookCtrl Overview**
======================================


Introduction
------------

A book control is a convenient way of displaying multiple pages of information, displayed one page at a time.
wxPython has five variants of this control:

- :ref:`wx.Choicebook`: controlled by a :ref:`wx.Choice`
- :ref:`wx.Listbook`: controlled by a :ref:`wx.ListCtrl`
- :ref:`wx.Notebook`: uses a row of tabs
- :ref:`wx.Treebook`: controlled by a :ref:`wx.TreeCtrl`
- :ref:`wx.Toolbook`: controlled by a :ref:`wx.ToolBar`



Best Book
---------

:ref:`wx.BookCtrlBase` is mapped to the class best suited for a given
platform. Currently it provides :ref:`wx.Choicebook` for smartphones
equipped with WinCE, and :ref:`wx.Notebook` for all other platforms. The
mapping consists of:

=============================================== ==================================================
`wx.BookCtrl`                                   `wx.Choicebook` or `wx.Notebook`
=============================================== ==================================================
``wxEVT_COMMAND_BOOKCTRL_PAGE_CHANGED``	        ``wxEVT_COMMAND_CHOICEBOOK_PAGE_CHANGED`` or ``wxEVT_COMMAND_NOTEBOOK_PAGE_CHANGED``
``wxEVT_COMMAND_BOOKCTRL_PAGE_CHANGING``        ``wxEVT_COMMAND_CHOICEBOOK_PAGE_CHANGING`` or ``wxEVT_COMMAND_NOTEBOOK_PAGE_CHANGING``
EVT_BOOKCTRL_PAGE_CHANGED                       EVT_CHOICEBOOK_PAGE_CHANGED or EVT_NOTEBOOK_PAGE_CHANGED
EVT_BOOKCTRL_PAGE_CHANGING                      EVT_CHOICEBOOK_PAGE_CHANGING or EVT_NOTEBOOK_PAGE_CHANGING
=============================================== ==================================================


For orientation of the book controller, use following flags in style:

- ``wx.BK_TOP``: controller above pages
- ``wx.BK_BOTTOM``: controller below pages
- ``wx.BK_LEFT``: controller on the left
- ``wx.BK_RIGHT``: controller on the right
- ``wx.BK_DEFAULT``: native controller placement

