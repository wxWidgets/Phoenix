#---------------------------------------------------------------------------
# This setup file serves as a model for how to structure your
# distutils setup files for making self-updating applications using
# Esky.  When you run this script use
#
#    python setup.py bdist_esky
#
# Esky will then use py2app or py2exe as appropriate to create the
# bundled application and also its own shell that will help manage
# doing the updates.  See wx.lib.softwareupdate for the class you can
# use to add self-updates to your applications, and you can see how
# that code is used here in the superdoodle.py module.
#---------------------------------------------------------------------------


import sys, os
from esky import bdist_esky
from setuptools import setup

import version


# platform specific settings for Windows/py2exe
if sys.platform == "win32":
    import py2exe
    
    FREEZER = 'py2exe'
    FREEZER_OPTIONS = dict(compressed = 0,
                           optimize = 0,
                           bundle_files = 3,
                           dll_excludes = ['MSVCP90.dll',
                                           'mswsock.dll',
                                           'powrprof.dll', 
                                           'USP10.dll',],
                        )
    exeICON = 'mondrian.ico'
    
                 
# platform specific settings for Mac/py2app
elif sys.platform == "darwin":
    import py2app
    
    FREEZER = 'py2app'
    FREEZER_OPTIONS = dict(argv_emulation = False, 
                           iconfile = 'mondrian.icns',
                           )
    exeICON = None
    

    
# Common settings    
NAME = "SuperDoodle"
APP = [bdist_esky.Executable("superdoodle.py", 
                             gui_only=True,
                             icon=exeICON,
                             )]
DATA_FILES = [ 'mondrian.ico' ]
ESKY_OPTIONS = dict( freezer_module     = FREEZER,
                     freezer_options    = FREEZER_OPTIONS,
                     enable_appdata_dir = True,
                     bundle_msvcrt      = True,
                     )
    

# Build the app and the esky bundle
setup( name       = NAME,
       scripts    = APP,
       version    = version.VERSION,
       data_files = DATA_FILES,
       options    = dict(bdist_esky=ESKY_OPTIONS),
       )


