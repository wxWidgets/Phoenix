#----------------------------------------------------------------------
# Name:        setup.py
# Purpose:     Distutils build script for wxPython (phoenix)
#
# Author:      Robin Dunn
#
# Created:     3-Nov-2010
# Copyright:   (c) 2010 by Total Control Software
# License:     wxWindows License
#----------------------------------------------------------------------


import sys, os
from distutils.core      import setup, Extension
from distutils.file_util import copy_file
from distutils.dir_util  import mkpath
from distutils.dep_util  import newer
from distutils.spawn     import spawn

from buildtools.config import Config, msg, opj
import buildtools.distutils_hacks as hacks


#----------------------------------------------------------------------

NAME             = "wxPython (phoenix)"
DESCRIPTION      = "Cross platform GUI toolkit for Python"
AUTHOR           = "Robin Dunn"
AUTHOR_EMAIL     = "Robin Dunn <robin@alldunn.com>"
URL              = "http://wxPython.org/"
DOWNLOAD_URL     = "http://wxPython.org/download.php"
LICENSE          = "wxWidgets Library License (LGPL derivative)"
PLATFORMS        = "WIN32,WIN64,OSX,POSIX"
KEYWORDS         = "GUI,wx,wxWindows,wxWidgets,cross-platform,awesome"

LONG_DESCRIPTION = """\
wxPython is a GUI toolkit for Python that is a wrapper around the
wxWidgets C++ GUI library.  wxPython provides a large variety of
window types and controls, all implemented with a native look and
feel, by using the native widgets where possible.
"""

CLASSIFIERS      = """\
Development Status :: 6 - Mature
Environment :: MacOS X :: Carbon
Environment :: Win32 (MS Windows)
Environment :: Win64 (MS Windows)
Environment :: X11 Applications :: GTK
Intended Audience :: Developers
License :: OSI Approved
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows :: Windows 2000/XP/Vista/7
Operating System :: POSIX
Programming Language :: Python
Topic :: Software Development :: User Interfaces
"""

#----------------------------------------------------------------------

# Create a buildtools.config.Configuration object
cfg = Config()


# Ensure that the directory containing this script is on the python
# path for spawned commands so the builder and phoenix packages can be
# found.
thisdir = os.path.abspath(os.path.split(__file__)[0])
os.environ['PYTHONPATH'] = thisdir + os.pathsep + os.environ.get('PYTHONPATH', '')

  
WX_PKGLIST = [ cfg.PKGDIR ]

SCRIPTS = None
DATA_FILES = []
HEADERS = None
BUILD_OPTIONS = { 'build_base' : cfg.BUILD_BASE }
if cfg.WXPORT == 'msw':
    BUILD_OPTIONS[ 'compiler' ] = cfg.COMPILER


    
copy_file('src/__init__.py', cfg.PKGDIR, update=1, verbose=0)
cfg.CLEANUP.append(opj(cfg.PKGDIR, '__init__.py'))

# update the license files
mkpath('license')
for file in ['preamble.txt', 'licence.txt', 'licendoc.txt', 'lgpl.txt']:
    copy_file(opj(cfg.WXDIR, 'docs', file), opj('license',file), update=1, verbose=0)
    cfg.CLEANUP.append(opj('license',file))
cfg.CLEANUP.append('license')


if sys.platform in ['win32', 'darwin']:
    cfg.build_locale_dir(opj(cfg.PKGDIR, 'locale'))
    DATA_FILES += cfg.build_locale_list(opj(cfg.PKGDIR, 'locale'))


if os.name == 'nt':
    rc_file = ['src/wxc.rc']
else:
    rc_file = []


#----------------------------------------------------------------------
    
ext = []

ext.append( 
    Extension('siplib', ['sip/siplib/apiversions.c',
                         'sip/siplib/bool.cpp',
                         'sip/siplib/descriptors.c',
                         'sip/siplib/objmap.c',
                         'sip/siplib/qtlib.c',
                         'sip/siplib/siplib.c',
                         'sip/siplib/threads.c',
                         'sip/siplib/voidptr.c',
                         ], 
              include_dirs       = cfg.includes,
              define_macros      = cfg.defines,
              library_dirs       = cfg.libdirs,
              libraries          = cfg.libs,
              extra_compile_args = cfg.cflags,
              extra_link_args    = cfg.lflags,
              ))
    
ext.append(
    Extension('_core', ['etg/_core.py',
                        'etg/windowid.py',
                        'etg/object.py',
                        
                        'etg/kbdstate.py',
                        'etg/mousestate.py',
                        'etg/tracker.py',
                        'etg/event.py',
                        
                        'etg/gdicmn.py',
                        'etg/geometry.py',
                        ] + rc_file,
              depends = [ 'src/string.sip',
                          'src/clntdata.sip',
                          ],
              include_dirs       = cfg.includes,
              define_macros      = cfg.defines,
              library_dirs       = cfg.libdirs,
              libraries          = cfg.libs,
              extra_compile_args = cfg.cflags,
              extra_link_args    = cfg.lflags,
              ))
cfg.CLEANUP.append(opj(cfg.PKGDIR, 'core.py'))


#----------------------------------------------------------------------

if __name__ == '__main__':
    setup(name             = NAME, #'wxPython',
          version          = cfg.VERSION,
          description      = DESCRIPTION,
          long_description = LONG_DESCRIPTION,
          author           = AUTHOR,
          author_email     = AUTHOR_EMAIL,
          url              = URL,
          download_url     = DOWNLOAD_URL,
          license          = LICENSE,
          platforms        = PLATFORMS,
          classifiers      = [c for c in CLASSIFIERS.split("\n") if c],
          keywords         = KEYWORDS,

          packages         = WX_PKGLIST,
          #extra_path       = EXTRA_PATH,
          ext_package      = cfg.PKGDIR,
          ext_modules      = ext,
           
          options          = { 'build'     : BUILD_OPTIONS,  
                               'build_ext' : {'sip_opts' : cfg.SIPOPTS },
                               },

          scripts          = SCRIPTS,
          data_files       = DATA_FILES,
          headers          = HEADERS,

          # Override some of the default distutils command classes with my own
          cmdclass = { 'install'         : hacks.wx_install,
                       'install_data'    : hacks.wx_smart_install_data,
                       'install_headers' : hacks.wx_install_headers,
                       'clean'           : hacks.wx_extra_clean,
                       'build_ext'       : hacks.etgsip_build_ext,
                       },

        )
