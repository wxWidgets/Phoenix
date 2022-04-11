# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------
# Name:        sphinxtools/templates.py
# Author:      Andrea Gavana
#
# Created:     30-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------


# Main class description, with class name repeated twice
TEMPLATE_DESCRIPTION = '''

.. _%s:

==========================================================================================================================================
|phoenix_title|  **%s**
==========================================================================================================================================

'''


# Inheritance diagram template, containing the class name, the PNG file representing
# the inheritance diagram, the "ALT" HTML flag (the class name again) and the full
# "MAP" HTML flag used for mouse navigation in the inheritance diagram boxes
TEMPLATE_INHERITANCE = '''

|

|class_hierarchy| Class Hierarchy
=================================

.. raw:: html

   <div id="toggleBlock" onclick="return toggleVisibility(this)" class="closed" style="cursor:pointer;">
   <img id="toggleBlock-trigger" src="_static/images/closed.png"/>
   Inheritance diagram for %s <strong>%s</strong>:
   </div>
   <div id="toggleBlock-summary" style="display:block;"></div>
   <div id="toggleBlock-content" style="display:none;">
   <p class="graphviz">
   <center><img src="_static/images/inheritance/%s" alt="Inheritance diagram of %s" usemap="#dummy" class="inheritance"/></center>
   <script type="text/javascript">toggleVisibilityOnLoad(document.getElementById('toggleBlock'))</script>
   %s
   </p>
   </div>

|

'''


# Template for the widget screenshots, with one screenshots image file for
# each platform
TEMPLATE_APPEARANCE = '''
|appearance| Control Appearance
===============================

|

.. figure:: _static/images/widgets/fullsize/wxmsw/%s
   :alt: wxMSW
   :figclass: floatleft

   **wxMSW**


.. figure:: _static/images/widgets/fullsize/wxmac/%s
   :alt: wxMAC
   :figclass: floatright

   **wxMAC**


.. figure:: _static/images/widgets/fullsize/wxgtk/%s
   :alt: wxGTK
   :figclass: floatcenter

   **wxGTK**


|

'''


# Template for the subclasses of a class, with a string containing a list
# of comma separated class names with their ReST role as :ref: prepended
TEMPLATE_SUBCLASSES = '''
|sub_classes| Known Subclasses
==============================

%s

|

'''

# Template for the superclasses of a class, with a string containing a list
# of comma separated class names with their ReST role as :ref: prepended
TEMPLATE_SUPERCLASSES = '''
|super_classes| Known Superclasses
==================================

%s

|

'''


# Template for the method summary of a class, containing a table made of
# ``method_name``      ``method description``
TEMPLATE_METHOD_SUMMARY = '''
|method_summary| Methods Summary
================================

%s

|

'''


# Template for the property summary of a class, containing a table made of
# ``property_name``      ``property description``
TEMPLATE_PROPERTY_SUMMARY = '''
|property_summary| Properties Summary
=====================================

%s

|

'''


# Template for the Class API title, no input
TEMPLATE_API = '''
|api| Class API
===============

'''

# Template for the standalone function summary for a module (wx, wx.dataview
# and so on).

TEMPLATE_FUNCTION_SUMMARY = '''
.. include:: headings.inc

=========================================================================
**%s** Functions
=========================================================================

The functions and macros defined in the **%s** module are described here: you can look up a function using the alphabetical listing of them.

Function Summary
================


'''


# Template for the main class index for a module (wx, wx.dataview and so on).
TEMPLATE_CLASS_INDEX = '''
.. include:: headings.inc

=========================================================================
**%s**
=========================================================================

%s

Class Summary
=============

'''

# Template for the functions header in the module index
TEMPLATE_MODULE_FUNCTION_SUMMARY = '''
Functions Summary
=================

'''


# Template for the class window styles, with the class name as input
TEMPLATE_WINDOW_STYLES = '''

.. _%s-styles:

|styles| Window Styles
================================

'''


# Template for the class window extra styles, with the class name as input
TEMPLATE_WINDOW_EXTRASTYLES = '''

.. _%s-extra-styles:

|extra_styles| Window Extra Styles
==================================

'''


# Template for the class events, with the class name as input
TEMPLATE_EVENTS = '''

.. _%s-events:

|events| Events Emitted by this Class
=====================================

'''

TEMPLATE_CONTRIB = '''

|user| Contributed Examples
===========================

'''

# Template used to generate the widgets gallery (this needs some work)
TEMPLATE_GALLERY = '''

{%% extends "layout.html" %%}
{%% set title = "Thumbnail gallery" %%}


{%% block body %%}

<h3>Click on any image to go to the relevant documentation</h3>
<br/>
The gallery is generated by randomly choosing a widget image between the 3 main
available ports of wxPython, namely <tt>wxMSW</tt>, <tt>wxGTK</tt> and <tt>wxMAC</tt> every
time the <b>Phoenix</b> documentation is built.

<br/>
<br/>
<br/>
<br/>
<br/>

<div class="gallery_class">

%s

</div>
<br clear="all">

{%% endblock %%}
'''


# Template to generate the "headings.inc" file containing the substitution reference
# for the small icons used in the Sphinx titles, sub-titles and so on.
TEMPLATE_HEADINGS = '''

.. |%s| image:: %s
   :align: middle
   :width: %dpx

'''

# Templates for the summary of modules/packages, containing a table made of
# ``module name``      ``short description``
TEMPLATE_MODULE_SUMMARY = '''
|module_summary| Modules Summary
================================

%s

|

'''

TEMPLATE_PACKAGE_SUMMARY = '''
|package_summary| Packages Summary
==================================

%s

|

'''

TEMPLATE_STD_FUNCTION_SUMMARY = '''
|function_summary| Functions Summary
====================================

%s

|

'''

TEMPLATE_STD_CLASS_SUMMARY = '''
|class_summary| Classes Summary
===============================

%s

|

'''


TEMPLATE_TOCTREE = '''
.. toctree::
   :maxdepth: 1
   :hidden:

%s
'''
