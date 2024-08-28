# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------
# Name:        sphinxtools/constants.py
# Author:      Andrea Gavana
#
# Created:     30-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

# Standard library imports
import os
import re
import datetime

# Phoenix-specific imports
import buildtools.version as version
from buildtools.config import phoenixDir, wxDir

# List of strings that should be ignored when creating inline literals
# such as ``ID_ANY`` or ``HORIZONTAL``, with double backticks
IGNORE = ['wxPython', 'wxWidgets', 'wxOSX', 'wxMGL', 'wxDFB', 'wxMAC', 'wxGTK', 'wxGTK2', 'wxUniversal',
          'OS', 'X', 'OSX', 'DFB', 'MAC', 'GTK', 'GTK2', 'MSW', 'wxMSW', 'X11', 'OS2', 'MS', 'XP', 'GTK+',
          'UI', 'GUI', '--', 'OTOH', 'GDI+', 'API', 'NT', 'RTL', 'GDI', '3D', 'MDI', 'SDI', 'TDI', 'URL',
          'XPM', 'HTML', 'MIME', 'C++', 'XDG', 'A4', 'A5', 'KDE', 'GNOME', 'XFCE', 'CSS', 'IE', 'FONT',
          'SIZE', 'COLOR', 'NOT', 'DOES']

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
            ('deprecated', '.. wxdeprecated::'),   # use the custom admonition for deprecation
            ('warning'   , '.. warning::'),
            ('remarks'   , '.. note::'),
            ('remark'    , '.. note::'),
            ('available' , '.. availability::'),
            ('note'      , '.. note::'),
            ('see'       , '.. seealso::'),
            ('todo'      , '.. todo::'),
            ('pre'       , ':precondition:'),
            ('par'       , '')
            ]


# List of things to remove/ignore (there may be more)
REMOVED_LINKS = ['Library:', 'Category:', 'Predefined objects/pointers:']

# Dictionary mapping the etg module name to the real Phoenix module name
# This needs to be kept up to date when other stuff comes in (i.e., wx.grid,
# wx.html and so on)
MODULENAME_REPLACE = {'_core'    : 'wx.',
                      '_dataview': 'wx.dataview.',
                      '_adv'     : 'wx.adv.',
                      '_stc'     : 'wx.stc.',
                      '_html'    : 'wx.html.',
                      '_html2'   : 'wx.html2.',
                      '_glcanvas': 'wx.glcanvas.',
                      '_xml'     : 'wx.xml.',
                      '_xrc'     : 'wx.xrc.',
                      '_grid'    : 'wx.grid.',
                      '_richtext': 'wx.richtext.',
                      '_webkit'  : 'wx.webkit.',
                      '_media'   : 'wx.media.',
                      '_msw'     : 'wx.msw.',
                      '_ribbon'  : 'wx.ribbon.',
                      '_propgrid': 'wx.propgrid.',
                      '_aui'     : 'wx.aui.',
                      }


# Other C++ specific things to strip away
CPP_ITEMS = ['*', '&', 'const', 'unsigned', '(size_t)', 'size_t', 'void']

# Series of paths containing the input data for Sphinx and for the scripts
# building the ReST docs:

# The location of the Phoenix main folder
PHOENIXROOT          = phoenixDir()

# The location of the Sphinx main folder
SPHINXROOT           = os.path.join(PHOENIXROOT, 'docs', 'sphinx')

# Where the snippets found in the XML docstrings live (There are C++, unconverted and
# converted Python snippets in 3 sub-folders
SNIPPETROOT          = os.path.join(SPHINXROOT,  'rest_substitutions', 'snippets')

# A folder where some of the difficult-to-translate-to-ReST tables are. There are 4 of
# them up to now, for various reasons:
# 1. The wx.Sizer flags table is a grid table, very difficult to ReSTify automatically
# 2. The wx.ColourDatabase table of colour comes up all messy when ReSTified from XML
# 3. The "wxWidgets 2.8 Compatibility Functions" table for wx.VScrolledWindow
# 4. The wx.ArtProvider table
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

DOCSTRING_KEY = '__module_docstring'

# The Doxygen root for the XML docstrings
xmlsrcbase = 'docs/doxygen/out/xml'
WXWIN = wxDir()
XMLSRC = os.path.join(WXWIN, xmlsrcbase)

DOXYROOT             = os.path.join(WXWIN, 'docs', 'doxygen')

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

SECTIONS_EXCLUDE = {
                    'ConfigBase'   : ('Related Include Files', '|phoenix_title| Example'),
                    'KeyboardState': ('This class is implemented ', '.. seealso::'),
                    'Menu'         : ('|phoenix_title| Allocation strategy', '|phoenix_title| Event handling'),
                    'MouseState'   : ('This class is implemented', '.. seealso::'),
                    'Panel'        : ('Please see  :ref:`/', 'if not all characters'),
                    'TextCtrl'     : ('|phoenix_title| TextCtrl and C++ Streams', '|phoenix_title| Event Handling'),
                    'TextEntry'    : ('Notice that you need', 'Currently this method is only '),
                    }

# A regex to split a string keeping the whitespaces
RE_KEEP_SPACES = re.compile(r'(\s+)')

# A list of things used in the post-processing of the HTML files generated by Sphinx
# This list is used only to insert a HTML horizontal line (<hr>) after each method/function
# description
HTML_REPLACE = ['module', 'function', 'method', 'class', 'classmethod', 'staticmethod', 'attribute']

# Today's date representation for the Sphinx HTML docs
TODAY = datetime.date.today().strftime('%d %B %Y')

# Inheritance diagram external hyperlinks

PYTHON_DOCS = 'http://docs.python.org/library/'
NUMPY_DOCS = 'http://docs.scipy.org/doc/numpy/reference/generated/'

EXTERN_INHERITANCE = {'UserDict.'  : PYTHON_DOCS,
                      'ctypes.'    : PYTHON_DOCS,
                      'code.'      : PYTHON_DOCS,
                      'exceptions.': PYTHON_DOCS,
                      'threading.' : PYTHON_DOCS,
                      'numpy.'     : NUMPY_DOCS
                      }

# wx.lib and other pure-Python stuff

class Enumeration(object):

    def __init__(self, name, enumList):

        self.__doc__ = name
        lookup = { }
        reverseLookup = { }
        i = 0
        uniqueNames = [ ]
        uniqueValues = [ ]

        for item in enumList:
            x = item.upper()
            uniqueNames.append(x)
            uniqueValues.append(i)
            lookup[x] = i
            reverseLookup[i] = x
            i = i + 1

        self.lookup = lookup
        self.reverseLookup = reverseLookup

    def __getattr__(self, attr):

        if not attr in self.lookup:
            raise AttributeError

        return self.lookup[attr]

    def whatis(self, value):

        return self.reverseLookup[value]


CONSTANT_RE = re.compile(r'^([\w\s,]+)=', re.M)

EXCLUDED_ATTRS = ['__builtins__', '__doc__', '__name__', '__file__', '__path__',
                  '__module__', '__all__', '__cached__', '__loader__', '__package__',
                  '__spec__', ]

TYPE_DESCRIPTION = ['library',
                    'package',
                    'py_module', 'pyd_module', 'pyc_module', 'pyw_module',
                    'klass',
                    'function',
                    'method', 'static_method', 'class_method', 'instance_method',
                    'method_descriptor', 'builtin_method', 'builtin_function',
                    'property',
                    'booltype', 'classtype', 'complextype', 'dictproxytype', 'dicttype', 'filetype',
                    'floattype', 'instancetype', 'inttype', 'lambdatype', 'listtype', 'longtype',
                    'nonetype', 'objecttype', 'slicetype', 'strtype', 'tracebacktype', 'tupletype',
                    'typetype', 'unicodetype', 'unknowntype', 'xrangetype']

object_types = Enumeration('Object_Types', TYPE_DESCRIPTION)

MODULE_TO_ICON = [(".py",  object_types.PY_MODULE, "Py_Module"),   (".pyd", object_types.PYD_MODULE, "Pyd_Module"),
                  (".pyc", object_types.PYC_MODULE, "Pyc_Module"), (".pyw", object_types.PYW_MODULE, "Pyw_Module"),
                  (".so",  object_types.PYD_MODULE, "Pyd_Module")]

# wx.tools and other stuff

DOXY_2_REST = [('@author:',        '\n.. moduleauthor:: '),
               ('@deprecated:',    '\n.. deprecated:: '),
               ('@param',          ':param'),
               ('@var',            ':param'),
               ('@keyword',        ':keyword'),
               ('@kwarg',          ':keyword'),
               ('@note:',          '\n.. note:: '),
               ('@package:',       '\n**Package:** '),
               ('@package',        '\n**Package:** '),
               ('@postcondition:', '\n:postcondition: '),
               ('@pre:',           '\n:precondition: '),
               ('@precondition:',  '\n:precondition: '),
               ('@pre',            '\n:precondition: '),
               ('@precondition',   '\n:precondition: '),
               ('@requires:',      '\n:requires: '),
               ('@returns:',       '\n:returns: '),
               ('@return:',        '\n:returns: '),
               ('@returns',        '\n:returns: '),
               ('@return',         '\n:returns: '),
               ('@rtype:',         '\n:rtype: '),
               # ('@section',      XXX),      Deal with this separately
               ('@see:',           '\n.. seealso:: '),
               ('@status:',        '\n.. todo:: '),
               ('@summary:',       '\n**Summary:** '),
               ('@throws:',        '\n:raise: '),
               ('@todo:',          '\n.. todo:: '),
               ('@verbatim ',      ''),       # TODO This one
               ('@verbatim',       ''),       # TODO This one
               ('@endverbatim ',   ''),       # TODO This one
               ('@endverbatim',    ''),       # TODO This one
               ('@version:',        '\n:version: ')]

