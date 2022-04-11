.. wxPython Phoenix documentation
   Created:   9-Dec-2011
   Copyright: (c) 2011-2017 by Total Control Software
   License:   wxWindows License

.. include:: headings.inc

==========================
wxPython API Documentation
==========================

!WELCOME!

If you are porting your code from Classic wxPython, be sure to read the
`Migration Guide <MigrationGuide.html>`_  to get a better feel for
how some things have changed.

You can download a local copy of this documentation using a new utility script
included with wxPython called ``wxdocs``. It will open the local copy of the
documentation in your default browser, downloading it first if needed. There
is also a similar tool called ``wxdemo`` that will download (if needed)
and launch the wxPython demo for you.

.. note:: If you wish to help in the documentation effort, the main
   docstrings guidelines are outlined in the
   `Docstring Guidelines <https://docs.wxpython.org/DocstringsGuidelines.html>`_
   document.


.. raw:: html

     <h2>Sections</h2>

     <table class="contentstable" align="center" style="margin-left: 25px">
       <tr><td>
         <p class="mybiglink"><a class="mybiglink" href="Overviews.html">wx Overview Documents</a><br/>
            <span class="linkdescr">A collection of overview and how-to documents about various wx topics. </span></p>

         <p class="mybiglink"><a class="mybiglink" href="wx.functions.html">wx functions</a><br/>
            <span class="linkdescr">The index of top-level functions available in the wx package. </span></p>

       </td></tr>
      </table>

     <h3>Modules</h3>

     <table class="contentstable" align="center" style="margin-left: 25px">
       <tr>
       <td width="50%" valign="top">
         <p class="mybiglink"><a class="mybiglink" href="wx.1moduleindex.html">wx</a><br/>
            <span class="linkdescr">The classes which appear in the main wx namespace</span></p>

         <p class="mybiglink"><a class="mybiglink" href="wx.adv.1moduleindex.html">wx.adv</a><br/>
            <span class="linkdescr">Less commonly used or more advanced classes</span></p>

         <p class="mybiglink"><a class="mybiglink" href="wx.grid.1moduleindex.html">wx.grid</a><br/>
            <span class="linkdescr">Widget and supporting classes for displaying and editing tabular data</span></p>

         <p class="mybiglink"><a class="mybiglink" href="wx.dataview.1moduleindex.html">wx.dataview</a><br/>
            <span class="linkdescr">Classes for viewing tabular or hierarchical data</span></p>

         <p class="mybiglink"><a class="mybiglink" href="wx.richtext.1moduleindex.html">wx.richtext</a><br/>
            <span class="linkdescr">A generic, ground-up implementation of a text control capable of showing multiple text styles and images.</span></p>

         <p class="mybiglink"><a class="mybiglink" href="wx.ribbon.1moduleindex.html">wx.ribbon</a><br/>
            <span class="linkdescr">A set of classes for writing a ribbon-based UI, typically a combination of tabs and toolbar, similar to the UI in MS Office and Windows 10.</span></p>

         <p class="mybiglink"><a class="mybiglink" href="wx.html.1moduleindex.html">wx.html</a><br/>
            <span class="linkdescr">Widget and supporting classes for a generic html renderer</span></p>

         <p class="mybiglink"><a class="mybiglink" href="wx.html2.1moduleindex.html">wx.html2</a><br/>
            <span class="linkdescr">Widget and supporting classes for a native html renderer, with CSS and javascript support</span></p>

         <p class="mybiglink"><a class="mybiglink" href="wx.aui.1moduleindex.html">wx.aui</a><br/>
            <span class="linkdescr">Docking/floating window panes, draggable notebook tabs, etc.</span></p>

         <p class="mybiglink"><a class="mybiglink" href="wx.svg.html">wx.svg</a><br/>
            <span class="linkdescr">Classes to parse and render Scalable Vector Graphics files.</span></p>

       </td>
       <td valign="top" width="50%" style="margin-left: 5px">
         <p class="mybiglink"><a class="mybiglink" href="wx.lib.html">wx.lib</a><br/>
            <span class="linkdescr">Our pure-Python library of widgets</span></p>

         <p class="mybiglink"><a class="mybiglink" href="wx.glcanvas.1moduleindex.html">wx.glcanvas</a><br/>
            <span class="linkdescr">Classes for embedding OpenGL views in a window</span></p>

         <p class="mybiglink"><a class="mybiglink" href="wx.stc.1moduleindex.html">wx.stc</a><br/>
            <span class="linkdescr">Classes for Styled Text Control, a.k.a Scintilla</span></p>

         <p class="mybiglink"><a class="mybiglink" href="wx.msw.1moduleindex.html">wx.msw</a><br/>
            <span class="linkdescr">A few classes available only on Windows</span></p>

         <p class="mybiglink"><a class="mybiglink" href="wx.media.1moduleindex.html">wx.media</a><br/>
            <span class="linkdescr">MediaCtrl and related classes</span></p>

         <p class="mybiglink"><a class="mybiglink" href="wx.propgrid.1moduleindex.html">wx.propgrid</a><br/>
            <span class="linkdescr">PropertyGrid and related classes for editing a grid of name/value pairs. </span></p>

         <p class="mybiglink"><a class="mybiglink" href="wx.xrc.1moduleindex.html">wx.xrc</a><br/>
            <span class="linkdescr">Classes for loading widgets and layout from XML</span></p>

         <p class="mybiglink"><a class="mybiglink" href="wx.xml.1moduleindex.html">wx.xml</a><br/>
            <span class="linkdescr">Some simple XML classes for use with XRC</span></p>

         <p class="mybiglink"><a class="mybiglink" href="wx.py.html">wx.py</a><br/>
            <span class="linkdescr">The py package, containing PyCrust and related modules</span></p>

         <p class="mybiglink"><a class="mybiglink" href="wx.tools.html">wx.tools</a><br/>
            <span class="linkdescr">Some useful tools and utilities for wxPython.</span></p>

         <p class="mybiglink"><a class="mybiglink" href="wx.functions.html">functions</a><br/>
            <span class="linkdescr">Top-level functions in the wx package.</span></p>

       </td></tr>
     </table>




.. toctree::
   :maxdepth: 2
   :hidden:
   :glob:

   MigrationGuide
   DocstringsGuidelines
   Overviews
   wx.functions
   wx.1moduleindex
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
   wx.svg
