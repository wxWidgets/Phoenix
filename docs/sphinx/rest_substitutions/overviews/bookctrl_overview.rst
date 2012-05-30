.. include:: headings.inc


.. _bookctrl overview:

===============================================
|phoenix_title|  **BookCtrl Overview**
===============================================


Introduction
------------

A book control is a convenient way of displaying multiple pages of information, displayed one page at a time. 
wxPython has five variants of this control:

- :ref:`Choicebook`: controlled by a :ref:`Choice`
- :ref:`Listbook`: controlled by a :ref:`ListCtrl`
- :ref:`Notebook`: uses a row of tabs
- :ref:`Treebook`: controlled by a :ref:`TreeCtrl`
- :ref:`Toolbook`: controlled by a :ref:`ToolBar`



Best Book
---------

:ref:`BookCtrlBase` is mapped to the class best suited for a given platform. Currently it provides :ref:`Choicebook`
for smartphones equipped with WinCE, and :ref:`Notebook` for all other platforms. The mapping consists of:

=============================================== ==================================================
`BookCtrl`                                      `Choicebook` or `Notebook`
=============================================== ==================================================
``wxEVT_COMMAND_BOOKCTRL_PAGE_CHANGED``	        ``wxEVT_COMMAND_CHOICEBOOK_PAGE_CHANGED`` or ``wxEVT_COMMAND_NOTEBOOK_PAGE_CHANGED``
``wxEVT_COMMAND_BOOKCTRL_PAGE_CHANGING``        ``wxEVT_COMMAND_CHOICEBOOK_PAGE_CHANGING`` or ``wxEVT_COMMAND_NOTEBOOK_PAGE_CHANGING``
EVT_BOOKCTRL_PAGE_CHANGED                       EVT_CHOICEBOOK_PAGE_CHANGED or EVT_NOTEBOOK_PAGE_CHANGED
EVT_BOOKCTRL_PAGE_CHANGING                      EVT_CHOICEBOOK_PAGE_CHANGING or EVT_NOTEBOOK_PAGE_CHANGING
=============================================== ==================================================


For orientation of the book controller, use following flags in style:

- ``BK_TOP``: controller above pages
- ``BK_BOTTOM``: controller below pages
- ``BK_LEFT``: controller on the left
- ``BK_RIGHT``: controller on the right
- ``BK_DEFAULT``: native controller placement

