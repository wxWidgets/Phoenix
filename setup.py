#----------------------------------------------------------------------
# Name:        setup.py
# Purpose:     Distutils build script for wxPython (phoenix)
#
# Author:      Robin Dunn
#
# Created:     3-Nov-2010
# Copyright:   (c) 2013 by Total Control Software
# License:     wxWindows License
#----------------------------------------------------------------------

import sys, os
import glob

try:
    import setuptools
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()

from setuptools                     import setup, Extension, find_packages
from distutils.command.build        import build as orig_build
from setuptools.command.install     import install as orig_install
from setuptools.command.bdist_egg   import bdist_egg as orig_bdist_egg
from setuptools.command.build_py    import build_py as orig_build_py

from buildtools.config import Config, msg, opj, runcmd, canGetSOName, getSOName 


#----------------------------------------------------------------------

NAME             = "wxPython-Phoenix"
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
Environment :: MacOS X :: Cocoa
Environment :: Win32 (MS Windows)
Environment :: Win64 (MS Windows)
Environment :: X11 Applications :: GTK
Intended Audience :: Developers
License :: OSI Approved
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows :: Windows 2000/XP/Vista/7/8
Operating System :: POSIX
Programming Language :: Python
Topic :: Software Development :: User Interfaces
"""


isWindows = sys.platform.startswith('win')
isDarwin = sys.platform == "darwin"

#----------------------------------------------------------------------
# Classes used in place of some distutils/setuptools classes.

class wx_build(orig_build):
    """
    Delgate to build.py for doing the actual build, (including wxWidgets)
    instead of letting distutils do it all.
    """
    user_options = [
        ('skip-build', None, 'skip building the C/C++ code (assumes it has already been done)'),
        ]
    boolean_options = ['skip-build']
    
    
    def initialize_options(self):
        orig_build.initialize_options(self)
        self.skip_build = '--skip-build' in sys.argv
    
    def run(self):        
        if not self.skip_build:
            # Run build.py to do the actual building of the extension modules
            msg('WARNING: Building this way assumes that all generated files have been \n'
                'generated already.  If that is not the case then use build.py directly \n'
                'to generate the source and perform the build stage.  You can use \n'
                '--skip-build with the bdist_* or install commands to avoid this \n'
                'message and the wxWidgets and Phoenix build steps in the future.\n')       
        
            # Use the executable and version of the Python that is running this script.
            cmd = [sys.executable, '-u', 'build.py', sys.version[:3], 'build']
            cmd = ' '.join(cmd)
            runcmd(cmd)
        
        # Let distutils handle building up the package folder under the
        # build/lib folder like normal.
        orig_build.run(self)



class wx_bdist_egg(orig_bdist_egg):
    def run(self):
        # Ensure that there is a basic library build for bdist_egg to pull from.
        self.run_command("build")
        
        # Clean out any libwx* symlinks in the build_lib folder, as they will
        # turn into copies in the egg since zip files can't handle symlinks.
        # The links are not really needed since the extensions link to
        # specific soname, and they could bloat the egg too much if they were
        # left in.
        #        
        # TODO: can eggs have post-install scripts that would allow us to 
        # restore the links?
        #
        build_lib = self.get_finalized_command('build').build_lib
        build_lib = opj(build_lib, 'wx')
        for libname in glob.glob(opj(build_lib, 'libwx*')):
            
            if os.path.islink(libname):
                if isDarwin:
                    # On Mac the name used by the extension module is the real
                    # file, so we can just get rid of all the links.
                    os.unlink(libname)
                    
                elif canGetSOName():
                    # On linux the soname used in the extension modules may
                    # be (probably is) one of the symlinks, so we have to be
                    # more tricky here. If the named file is a link and it is
                    # the soname, then remove the link and rename the
                    # linked-to file to this name.
                    soname = getSOName(libname)
                    if soname == os.path.basename(libname):
                        realfile = os.path.join(build_lib, os.readlink(libname))
                        os.unlink(libname)
                        os.rename(realfile, libname)
                    else:
                        os.unlink(libname)
                else:
                    # Otherwise just leave the symlink there since we don't
                    # know what to do with it.
                    pass
        
        # Run the default bdist_egg command
        orig_bdist_egg.run(self)
    

class wx_install(orig_install):
    def run(self):
        self.run_command("build")
        orig_install.run(self)

    

# Map these new classes to the appropriate distutils command names.
CMDCLASS = {
    'build'     : wx_build,
    'bdist_egg' : wx_bdist_egg,
    'install'   : wx_install,
    }




#----------------------------------------------------------------------
# Monkey-patch copy_file and copy_tree such that they preserve symlinks. We
# need this since we're copying the wx shared libs into the package folder
# and the default implementations would have copied the file content multiple
# times instead of just copying the symlinks.


def wx_copy_file(src, dst, preserve_mode=1, preserve_times=1, update=0,
                 link=None, verbose=1, dry_run=0):
    if not os.path.islink(src):
        return orig_copy_file(
            src, dst, preserve_mode, preserve_times, update, link, verbose, dry_run)
    else:
        # make a new, matching symlink in dst
        if os.path.isdir(dst):
            dir = dst
            dst = os.path.join(dst, os.path.basename(src))
        linkdst = os.readlink(src)
        if verbose >= 1:
            from distutils import log
            log.info("%s %s -> %s", 'copying symlink', src, dst)
        if not dry_run and not os.path.exists(dst):
            os.symlink(linkdst, dst)
        return (dst, 1)

import distutils.file_util
orig_copy_file = distutils.file_util.copy_file
distutils.file_util.copy_file = wx_copy_file
        
        

def wx_copy_tree(src, dst, preserve_mode=1, preserve_times=1,
                 preserve_symlinks=0, update=0, verbose=1, dry_run=0):
    return orig_copy_tree(
        src, dst, preserve_mode, preserve_times, 1, update, verbose, dry_run)

import distutils.dir_util
orig_copy_tree = distutils.dir_util.copy_tree
distutils.dir_util.copy_tree = wx_copy_tree



#----------------------------------------------------------------------

# Create a buildtools.config.Configuration object
cfg = Config(noWxConfig=True)

WX_PKGLIST = [cfg.PKGDIR] + [cfg.PKGDIR + '.' + pkg for pkg in find_packages('wx')]

ENTRY_POINTS = {
    'console_scripts' : [ 
        "helpviewer = wx.tools.helpviewer:main",
        "img2png = wx.tools.img2png:main",
        "img2py = wx.tools.img2py:main",
        "img2xpm = wx.tools.img2xpm:main",
        "pywxrc = wx.tools.pywxrc:main",
        "pycrust = wx.py.PyCrust:main",
        "pyshell = wx.py.PyShell:main",
        "pyslices = wx.py.PySlices:main",
        "pyslicesshell = wx.py.PySlicesShell:main",        
        ]}

SCRIPTS = []
DATA_FILES = []

HEADERS = None
BUILD_OPTIONS = { } #'build_base' : cfg.BUILD_BASE }
#if cfg.WXPORT == 'msw':
#    BUILD_OPTIONS[ 'compiler' ] = cfg.COMPILER

    
#----------------------------------------------------------------------
    

if __name__ == '__main__':
    setup(name             = NAME, 
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
          zip_safe         = False,
          use_2to3         = False,
          include_package_data = True,
          
          packages         = WX_PKGLIST,
          
          # Add a bogus extension module (will never be built here since we
          # are overriding the build command to do it from build.py) so
          # things like bdist_egg will know that there are extension modules
          # and will name the dist with the full platform info.          
          ext_modules      = [Extension('siplib', [])],           
          ext_package      = cfg.PKGDIR,

          options          = { 'build'     : BUILD_OPTIONS },

          scripts          = SCRIPTS,
          data_files       = DATA_FILES,
          headers          = HEADERS,
          cmdclass         = CMDCLASS,
          entry_points     = ENTRY_POINTS,
        )
