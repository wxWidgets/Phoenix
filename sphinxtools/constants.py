# -*- coding: utf-8 -*-
#!/usr/bin/env python

#---------------------------------------------------------------------------
# Name:        sphinxtools/constants.py
# Author:      Andrea Gavana
#
# Created:     30-Nov-2010
# Copyright:   (c) 2011 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

# Standard library imports
import os
import re
import datetime

# Phoenix-specific imports
import buildtools.version as version

# List of strings that should be ignored when creating inline literals
# such as ``ID_ANY`` or ``HORIZONtAL``, with double backticks
IGNORE = ['wxPython', 'wxWidgets', 'wxOSX', 'wxMGL', 'wxDFB', 'wxMAC', 'wxGTK', 'wxGTK2', 'wxUniversal',
          'OS', 'X', 'OSX', 'DFB', 'MAC', 'GTK', 'GTK2', 'MSW', 'wxMSW', 'X11', 'OS2', 'MS', 'XP', 'GTK+',
          'UI', 'GUI', '--', 'OTOH', 'GDI+', 'API', 'NT', 'RTL', 'GDI', '3D', 'MDI']

# C++ stuff to Python/ReST stuff
VALUE_MAP = {'true':  '``True``',
             'false': '``False``',
             '``NULL``': '``None``',
             'NULL':  '``None``',
             'L{OSX}': '`OSX`',
             'ctor': 'constructor',
             }

# This is a list of instances in Phoenix (i.e., without documentation strings), and
# For the sake of beauty of the docs they get the inline literal treatment (double backticks)
CONSTANT_INSTANCES = ['NullAcceleratorTable', 'TheApp', 'DefaultPosition', 'DefaultSize',
                      'DefaultCoord', 'Coord', 'TheBrushList', 'TheColourDatabase',
                      'NullFont', 'NullBrush', 'NullPalette', 'NullPen', 'EmptyString',
                      'TheFontList', 'NullIcon', 'NullBitmap', 'constructor', 'ThePenList',
                      'DefaultValidator', 'String.Capitalize']
                      
# Phoenix full version
VERSION = '%d.%d.%d' % (version.VER_MAJOR, version.VER_MINOR, version.VER_RELEASE)

# Things to chop away when ReST-ifying the docstrings
PUNCTUATION = '!"#$%\'()*,./:;<=>?@\\^{|}~'

# Conversion between XML sections and ReST sections
SECTIONS = [('return'    , ':returns:'),
            ('since'     , '.. versionadded::'),
            ('deprecated', '.. deprecated::'),
            ('warning'   , '.. warning::'),            
            ('remarks'   , '.. note::'),
            ('remark'    , '.. note::'),
            ('available' , '.. availability::'),
            ('note'      , '.. note::'),            
            ('see'       , '.. seealso::'),
            ('todo'      , '.. todo::')]


# List of things to remove/ignore (there may be more)
REMOVED_LINKS = ['Library:', 'Category:', 'Predefined objects/pointers:']

# Dictionary mapping the etg module name to the real Phoenix module name
# This needs to be kept up to date when other stuff comes in (i.e., wx.grid,
# wx.html and so on)
MODULENAME_REPLACE = {'_core'    : '',
                      '_dataview': 'dataview.'
                      }

# Other C++ specific things to strip away
CPP_ITEMS = ['*', '&', 'const', 'unsigned', '(size_t)', 'size_t', 'void']

# Serie of paths containing the input data for Sphinx and for the scripts
# building the ReST docs:

# The location of the Phoenix main folder
PHOENIXROOT          = os.path.abspath(os.path.split(__file__)[0] + '/..')

# The location of the Sphinx main folder
SPHINXROOT           = os.path.join(PHOENIXROOT, 'docs', 'sphinx')

# Where the snippets found in the XML docstrings live (There are C++, unconverted and
# converted Python snippets in 3 sub-folders
SNIPPETROOT          = os.path.join(SPHINXROOT,  'rest_substitutions', 'snippets')

# A folder where some of the difficult-to-translate-to-ReST tables are. There are 3 of
# them up to now, for various reasons:
# 1. The wx.Sizer flags table is a grid table, very difficult to ReSTify automatically
# 2. The wx.ColourDatabase table of colour comes up all messy when ReSTified from XML
# 3. The "wxWidgets 2.8 Compatibility Functions" table for wx.VScrolledWindow
TABLEROOT            = os.path.join(SPHINXROOT,  'rest_substitutions', 'tables')

# Folder where to save the inheritance diagrams for the classes
INHERITANCEROOT      = os.path.join(SPHINXROOT,  '_static', 'images', 'inheritance')

# Folder where to save the images found in the wxWidgets overviews or in the XML
# docstrings
OVERVIEW_IMAGES_ROOT = os.path.join(SPHINXROOT,  '_static', 'images', 'overviews')

# Folder where to save the widgets screenshots (full-size, no thumbnails here)
WIDGETS_IMAGES_ROOT  = os.path.join(SPHINXROOT,  '_static', 'images', 'widgets', 'fullsize')

# Folder for the icons used for titles, sub-titles and so on for the Sphinx documentation
SPHINX_IMAGES_ROOT   = os.path.join(SPHINXROOT,  '_static', 'images', 'sphinxdocs')

# The Doxygen root for the XML docstrings
DOXYROOT             = os.path.join(os.environ['WXWIN'], 'docs', 'doxygen')

# Dictionary copied over from tweaker_tools
MAGIC_METHODS = {
    'operator!='    : '__ne__',
    'operator=='    : '__eq__',
    'operator+'     : '__add__',
    'operator-'     : '__sub__',
    'operator*'     : '__mul__',
    'operator/'     : '__div__',
    'operator+='    : '__iadd__',
    'operator-='    : '__isub__',
    'operator*='    : '__imul__',
    'operator/='    : '__idiv__',
    'operator bool' : '__int__',  # Why not __nonzero__?
    # TODO: add more
    }

# A regex to split a string keeping the whitespaces
RE_KEEP_SPACES = re.compile(r'(\s+)')

# A list of things used in the post-processing of the HTML files generated by Sphinx
# This list is used only to insert a HTML horizontal line (<hr>) after each method/function
# description
HTML_REPLACE = ['module', 'function', 'method', 'class', 'classmethod', 'staticmethod', 'attribute']

# The SVN revision of wxWidgets/Phoenix used to build the Sphinx docs.
# There must be a more intelligent way to get this information automatically.
SVN_REVISION = '70154'

# Today's date representation for the Sphinx HTML docs
TODAY = datetime.date.today().strftime('%d %B %Y')

