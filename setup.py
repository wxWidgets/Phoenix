#----------------------------------------------------------------------
# Name:        setup.py
# Purpose:     Distutils build script for wxPython (phoenix)
#
# Author:      Robin Dunn
#
# Created:     3-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#----------------------------------------------------------------------

import sys, os
import glob
import stat

from setuptools                     import setup, find_packages
from distutils.command.build        import build as orig_build
from setuptools.command.install     import install as orig_install
from setuptools.command.bdist_egg   import bdist_egg as orig_bdist_egg
from setuptools.command.sdist       import sdist as orig_sdist
try:
    from wheel.bdist_wheel import bdist_wheel as orig_bdist_wheel
    haveWheel = True
except ImportError:
    haveWheel = False

from buildtools.config import Config, msg, opj, runcmd, canGetSOName, getSOName
import buildtools.version as version


# Create a buildtools.config.Configuration object
cfg = Config(noWxConfig=True)
DOCS_BASE='http://docs.wxPython.org'

#----------------------------------------------------------------------

NAME             = version.PROJECT_NAME
DESCRIPTION      = "Cross platform GUI toolkit for Python, \"Phoenix\" version"
AUTHOR           = "Robin Dunn"
AUTHOR_EMAIL     = "robin@alldunn.com"
URL              = "http://wxPython.org/"
PROJECT_URLS     = {
                    "Source": "https://github.com/wxWidgets/Phoenix",
                    "Documentation": "https://docs.wxpython.org/",
                   }
DOWNLOAD_URL     = "https://pypi.org/project/{}".format(NAME)
LICENSE          = "wxWindows Library License (https://opensource.org/licenses/wxwindows.php)"
PLATFORMS        = "WIN32,WIN64,OSX,POSIX"
KEYWORDS         = "GUI,wx,wxWindows,wxWidgets,cross-platform,user-interface,awesome"

LONG_DESCRIPTION = """\
Welcome to wxPython's Project Phoenix! Phoenix is the improved next-generation
wxPython, "better, stronger, faster than he was before." This new
implementation is focused on improving speed, maintainability and
extensibility. Just like "Classic" wxPython, Phoenix wraps the wxWidgets C++
toolkit and provides access to the user interface portions of the wxWidgets
API, enabling Python applications to have a native GUI on Windows, Macs or
Unix systems, with a native look and feel and requiring very little (if any)
platform specific code.

For more information please refer to the
`README file <https://github.com/wxWidgets/Phoenix/blob/wxPython-{version}/README.rst>`_,
the `Migration Guide <{docs_base}/MigrationGuide.html>`_,
or the `wxPython API documentation <{docs_base}/index.html>`_.

Archive files containing a copy of the wxPython documentation, the demo and
samples, and also a set of MSVC .pdb files for Windows are available
`here <https://extras.wxPython.org/wxPython4/extras/>`_.

The utility tools wxdocs and wxdemo will download the appropriate files with wxget,
(if necessary), unpack them, (if necessary) and launch the appropriate version of
the respective items. (Documents are launched in the default browser and demo is started
with python).
""".format(version=cfg.VERSION, docs_base=DOCS_BASE)


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
Programming Language :: Python :: Implementation :: CPython
Topic :: Software Development :: User Interfaces
"""

with open('requirements/install.txt') as fid:
    INSTALL_REQUIRES = [line.strip()
                        for line in fid.readlines()
                        if not line.startswith('#')]

isWindows = sys.platform.startswith('win')
isDarwin = sys.platform == "darwin"

#----------------------------------------------------------------------
# Classes used in place of some distutils/setuptools classes.

class wx_build(orig_build):
    """
    Delegate to build.py for doing the actual build, (including wxWidgets)
    instead of letting distutils do it all.
    """
    user_options = [
        ('skip-build', None, 'skip building the C/C++ code (assumes it has already been done)'),
        ]
    boolean_options = ['skip-build']


    def initialize_options(self):
        orig_build.initialize_options(self)
        self.skip_build = '--skip-build' in sys.argv

    def finalize_options(self):
        orig_build.finalize_options(self)
        self.build_lib = self.build_platlib

    def run(self):
        if not self.skip_build:
            # Run build.py to do the actual building of the extension modules
            msg('WARNING: Building this way assumes that all generated files have been \n'
                'generated already.  If that is not the case then use build.py directly \n'
                'to generate the source and perform the build stage.  You can use \n'
                '--skip-build with the bdist_* or install commands to avoid this \n'
                'message and the wxWidgets and Phoenix build steps in the future.\n')

            # Use the same Python that is running this script.
            cmd = ['"{}"'.format(sys.executable), '-u', 'build.py', 'build']
            cmd = ' '.join(cmd)
            runcmd(cmd)

        # Let distutils handle building up the package folder under the
        # build/lib folder like normal.
        orig_build.run(self)


def _cleanup_symlinks(cmd):
    # Clean out any libwx* symlinks in the build_lib folder, as they will
    # turn into copies in the egg since zip files can't handle symlinks.
    # The links are not really needed since the extensions link to the
    # specific soname, and they could bloat the egg too much if they were
    # left in.
    #
    # TODO: can eggs have post-install scripts that would allow us to
    # restore the links? No.
    #
    build_lib = cmd.get_finalized_command('build').build_lib
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


class wx_bdist_egg(orig_bdist_egg):
    def finalize_options(self):
        orig_bdist_egg.finalize_options(self)

        # Redo the calculation of the egg's filename since we always have
        # extension modules, but they are not built by setuptools so it
        # doesn't know about them.
        from pkg_resources import Distribution
        from sysconfig import get_python_version
        basename = Distribution(
            None, None, self.ei_cmd.egg_name, self.ei_cmd.egg_version,
            get_python_version(),
            self.plat_name
        ).egg_name()
        self.egg_output = os.path.join(self.dist_dir, basename+'.egg')


    def run(self):
        # Ensure that there is a basic library build for bdist_egg to pull from.
        self.run_command("build")

        _cleanup_symlinks(self)

        # Run the default bdist_egg command
        orig_bdist_egg.run(self)


if haveWheel:
    class wx_bdist_wheel(orig_bdist_wheel):
        def finalize_options(self):
            # Do a bit of monkey-patching to let bdist_wheel know that there
            # really are extension modules in this build, even though they are
            # not built here.
            def _has_ext_modules(self):
                return True
            from setuptools.dist import Distribution
            #Distribution.is_pure = _is_pure
            Distribution.has_ext_modules = _has_ext_modules

            orig_bdist_wheel.finalize_options(self)


        def run(self):
            # Ensure that there is a basic library build for bdist_egg/wheel to pull from.
            self.run_command("build")

            _cleanup_symlinks(self)

            # Run the default bdist_wheel command
            orig_bdist_wheel.run(self)


class wx_install(orig_install):
    def finalize_options(self):
        orig_install.finalize_options(self)
        self.install_lib = self.install_platlib

    def run(self):
        self.run_command("build")
        orig_install.run(self)



class wx_sdist(orig_sdist):
    def run(self):
        # Use build.py to perform the sdist
        cmd = ['"{}"'.format(sys.executable), '-u', 'build.py', 'sdist']
        cmd = ' '.join(cmd)
        runcmd(cmd)

        # Put the filename in dist_files in case the upload command is used.
        # On the other hand, PyPI's upload size limit is waaaaaaaaay too
        # small so it probably doesn't matter too much...
        sdist_file = opj(self.dist_dir, self.distribution.get_fullname()+'.tar.gz')
        self.distribution.dist_files.append(('sdist', '', sdist_file))




# Map these new classes to the appropriate distutils command names.
CMDCLASS = {
    'build'       : wx_build,
    'bdist_egg'   : wx_bdist_egg,
    'install'     : wx_install,
    'sdist'       : wx_sdist,
    }
if haveWheel:
    CMDCLASS['bdist_wheel'] = wx_bdist_wheel



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


# Monkey-patch make_writeable too. Sometimes the link is copied before the
# target, and the original make_writable will fail on a link to a missing
# target.
def wx_make_writable(target):
    if not os.path.islink(target):
        os.chmod(target, os.stat(target).st_mode | stat.S_IWRITE)

import setuptools.command.build_py
setuptools.command.build_py.make_writable = wx_make_writable


#----------------------------------------------------------------------

WX_PKGLIST = [cfg.PKGDIR] + [cfg.PKGDIR + '.' + pkg for pkg in find_packages('wx')]

ENTRY_POINTS = {
    'console_scripts' : [
        "img2png = wx.tools.img2png:main",
        "img2py = wx.tools.img2py:main",
        "img2xpm = wx.tools.img2xpm:main",
        "pywxrc = wx.tools.pywxrc:main",
#        ],
#    'gui_scripts' : [  # TODO: Why was this commented out?
        "wxget = wx.tools.wxget:main",  # New wx wget
        "wxdocs = wx.tools.wxget_docs_demo:docs_main",  # Get/Launch Docs
        "wxdemo = wx.tools.wxget_docs_demo:demo_main",  # Get/Launch Demo
        "helpviewer = wx.tools.helpviewer:main",
        "pycrust = wx.py.PyCrust:main",
        "pyshell = wx.py.PyShell:main",
        "pyslices = wx.py.PySlices:main",
        "pyslicesshell = wx.py.PySlicesShell:main",
        ],
    }

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
          project_urls     = PROJECT_URLS,
          download_url     = DOWNLOAD_URL,
          license          = LICENSE,
          platforms        = PLATFORMS,
          classifiers      = [c for c in CLASSIFIERS.split("\n") if c],
          keywords         = KEYWORDS,
          install_requires = INSTALL_REQUIRES,
          zip_safe         = False,
          include_package_data = True,

          packages         = WX_PKGLIST,
          ext_package      = cfg.PKGDIR,

          options          = { 'build'     : BUILD_OPTIONS },

          scripts          = SCRIPTS,
          data_files       = DATA_FILES,
          headers          = HEADERS,
          cmdclass         = CMDCLASS,
          entry_points     = ENTRY_POINTS,
        )
