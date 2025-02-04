#----------------------------------------------------------------------
# Name:        setup-wxsvg.py
# Purpose:     Distutils build script for wxPython's wx.svg package
#
# Author:      Robin Dunn
#
# Created:     25-July-2019
# Copyright:   (c) 2019-2020 by Total Control Software
# License:     wxWindows License
#----------------------------------------------------------------------

import sys
import os
import textwrap
from setuptools import setup, Extension
try:
    from Cython.Build import cythonize
    have_cython = True
except ImportError:
    have_cython = False

# Create a buildtools.config.Configuration object, to get the VERSION
from buildtools.config import Config
cfg = Config(noWxConfig=True)

DESCRIPTION      = 'Wrapper for nanosvg library, plus code for integrating with wxPython'
LONG_DESCRIPTION = ''
AUTHOR           = 'Robin Dunn'
AUTHOR_EMAIL     = 'robin@alldunn.com'
URL              = "http://wxPython.org/"
DOWNLOAD_URL     = "https://pypi.org/project/wxPython"
LICENSE          = "wxWindows Library License (https://opensource.org/licenses/wxwindows.php)"
PLATFORMS        = "WIN32,WIN64,OSX,POSIX"
KEYWORDS         = "GUI,wx,wxWindows,wxWidgets,cross-platform,user-interface,awesome"

CLASSIFIERS      = """\
Development Status :: 6 - Mature
Environment :: MacOS X :: Cocoa
Environment :: Win32 (MS Windows)
Environment :: X11 Applications :: GTK
Intended Audience :: Developers
License :: OSI Approved
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows :: Windows 7
Operating System :: Microsoft :: Windows :: Windows 10
Operating System :: POSIX
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Programming Language :: Python :: 3.11
Programming Language :: Python :: 3.12
Programming Language :: Python :: Implementation :: CPython
Topic :: Software Development :: User Interfaces
"""

HERE = os.path.abspath(os.path.dirname(__file__))
PACKAGE = 'wx.svg'
PACKAGEDIR = 'wx/svg'
BUILD_OPTIONS = { 'build_base' : 'build/wxsvg' }

if have_cython:
    SOURCE = os.path.join(PACKAGEDIR, '_nanosvg.pyx')
else:
    SOURCE = os.path.join(PACKAGEDIR, '_nanosvg.c')

module = Extension(name='wx.svg._nanosvg',
                   sources=[SOURCE],
                   include_dirs=['ext/nanosvg/src'],
                   define_macros=[('NANOSVG_IMPLEMENTATION', '1'),
                                  ('NANOSVGRAST_IMPLEMENTATION', '1'),
                                  ('NANOSVG_ALL_COLOR_KEYWORDS', '1'),
                                  ])

if have_cython:
    modules = cythonize([module],
                        compiler_directives={'embedsignature': True,
                                             'language_level':2,
                                            })
else:
    modules = [module]


setup(name             = 'wx.svg',
      version          = cfg.VERSION,
      description      = DESCRIPTION,
      long_description = LONG_DESCRIPTION,
      author           = AUTHOR,
      author_email     = AUTHOR_EMAIL,
      url              = URL,
      download_url     = DOWNLOAD_URL,
      license          = LICENSE,
      classifiers      = [c for c in CLASSIFIERS.split("\n") if c],
      keywords         = KEYWORDS,
      #packages         = [PACKAGE],
      ext_modules      = modules,
      options          = { 'build' : BUILD_OPTIONS,  },
      scripts          = [],
)
