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
import shutil

from setuptools                     import setup
from setuptools.command.build       import build as orig_build
from setuptools.command.build_py    import build_py as orig_build_py
from setuptools.command.install     import install as orig_install
from setuptools.command.install_lib import install_lib as orig_install_lib
from setuptools.command.sdist       import sdist as orig_sdist
from setuptools.command.bdist_wheel import bdist_wheel as orig_bdist_wheel

# Alter the path so that buildtools can be imported from the current directory.
sys.path.insert(0, os.path.dirname(__file__))

from buildtools.config import Config, msg, opj, runcmd, canGetSOName, getSOName
import buildtools.version as version

# Create a buildtools.config.Configuration object
cfg = Config(noWxConfig=True)
DOCS_BASE='http://docs.wxPython.org'

#----------------------------------------------------------------------

PLATFORMS        = "WIN32,WIN64,OSX,POSIX"

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


with open('requirements/install.txt') as fid:
    INSTALL_REQUIRES = [line.strip()
                        for line in fid.readlines()
                        if not line.startswith('#')]

isWindows = sys.platform.startswith('win')
isDarwin = sys.platform == "darwin"

#----------------------------------------------------------------------
# Classes used in place of some setuptools command classes.

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

        # Let setuptools handle building up the package folder under the
        # build/lib folder like normal.
        orig_build.run(self)


def _cleanup_symlinks(cmd):
    # Clean out any libwx* symlinks in the build_lib folder, as they will
    # turn into copies in the wheel since zip files can't handle symlinks.
    # The links are not really needed since the extensions link to the
    # specific soname, and they could bloat the wheel too much if they were
    # left in.
    build_lib = cmd.get_finalized_command('build').build_lib
    build_lib = opj(build_lib, 'wx')
    for libname in sorted(glob.glob(opj(build_lib, 'libwx*'))):

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
        # Ensure that there is a basic library build for bdist_wheel to pull from.
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



# The wx shared libs are staged into the package as a versioned symlink chain
# (libwx_foo.so -> libwx_foo.so.3 -> libwx_foo.so.3.0.0). These two commands
# keep the symlinks intact rather than letting the copy dereference them into
# a full (large) copy per link name.

class wx_build_py(orig_build_py):
    def copy_file(self, infile, outfile, preserve_mode=True, preserve_times=True,
                  link=None, level=1):
        if os.path.islink(infile):
            if os.path.isdir(outfile):
                outfile = os.path.join(outfile, os.path.basename(infile))
            if not self.dry_run and not os.path.exists(outfile):
                os.symlink(os.readlink(infile), outfile)
            return (outfile, True)
        return super().copy_file(infile, outfile, preserve_mode,
                                 preserve_times, link, level)


class wx_install_lib(orig_install_lib):
    def install(self):
        # setuptools' install_lib.copy_tree asserts preserve_symlinks is off,
        # so do the tree copy here with shutil instead. get_outputs() is
        # recomputed from build_lib and doesn't rely on this return value.
        if not os.path.isdir(self.build_dir):
            self.warn("'%s' does not exist -- no Python modules to install"
                      % self.build_dir)
            return None
        if self.get_exclusions():
            # namespace-package exclusions aren't something wxPython uses; let
            # the default implementation handle that case if it ever arises.
            return super().install()
        self.mkpath(self.install_dir)
        if not self.dry_run:
            shutil.copytree(self.build_dir, self.install_dir,
                            symlinks=True, dirs_exist_ok=True)
        return [os.path.join(root, f)
                for root, _dirs, files in os.walk(self.install_dir)
                for f in files]



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




# Map these new classes to the appropriate setuptools command names.
CMDCLASS = {
    'build'       : wx_build,
    'build_py'    : wx_build_py,
    'install'     : wx_install,
    'install_lib' : wx_install_lib,
    'sdist'       : wx_sdist,
    'bdist_wheel' : wx_bdist_wheel,
    }


#----------------------------------------------------------------------

# setuptools' build_py.build_package_data calls the module-level make_writable
# on each file right after copying it. When that file is a symlink whose target
# hasn't been copied yet, os.stat() follows the dangling link and raises, so
# patch in a version that leaves symlinks alone.
def wx_make_writable(target):
    if not os.path.islink(target):
        os.chmod(target, os.stat(target).st_mode | stat.S_IWRITE)

import setuptools.command.build_py
setuptools.command.build_py.make_writable = wx_make_writable


#----------------------------------------------------------------------

HEADERS = None
BUILD_OPTIONS = { } #'build_base' : cfg.BUILD_BASE }
#if cfg.WXPORT == 'msw':
#    BUILD_OPTIONS[ 'compiler' ] = cfg.COMPILER


#----------------------------------------------------------------------


if __name__ == '__main__':
    setup(version          = cfg.VERSION,
          long_description = LONG_DESCRIPTION,
          long_description_content_type = 'text/x-rst',
          platforms        = PLATFORMS,
          install_requires = INSTALL_REQUIRES,
          zip_safe         = False,
          include_package_data = True,

          ext_package      = cfg.PKGDIR,

          options          = { 'build'     : BUILD_OPTIONS },

          headers          = HEADERS,
          cmdclass         = CMDCLASS,
        )
