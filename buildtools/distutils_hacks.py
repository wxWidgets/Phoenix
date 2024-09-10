#----------------------------------------------------------------------
# Name:        buildtools.distutils_hacks
# Purpose:     Various hacks that have been needed to override features
#              or work-around problems in Python's distutils.
#
# Author:      Robin Dunn
#
# Created:     3-Nov-2010
# Copyright:   (c) 2013-2020 by Total Control Software
# License:     wxWindows License
#----------------------------------------------------------------------

import sys
import os

import distutils.command.install
import distutils.command.install_data
import distutils.command.install_headers
import distutils.command.clean

try:
    from setuptools.modified import newer, newer_group
except ImportError:
    from distutils.dep_util import newer, newer_group

from distutils import log

from .config import Config, posixjoin, loadETG, etg2sip



#----------------------------------------------------------------------
# New command classes


class wx_smart_install_data(distutils.command.install_data.install_data):
    """need to change self.install_dir to the actual library dir"""
    def run(self):
        install_cmd = self.get_finalized_command('install')
        self.install_dir = getattr(install_cmd, 'install_lib')
        return distutils.command.install_data.install_data.run(self)


class wx_extra_clean(distutils.command.clean.clean):
    """
    Also cleans stuff that this setup.py copies itself.  If the
    --all flag was used also searches for .pyc, .pyd, .so files
    """
    def run(self):
        from distutils.filelist import FileList

        distutils.command.clean.clean.run(self)

        cfg = Config()
        if self.all:
            fl = FileList()
            fl.include_pattern("*.pyc", 0)
            fl.include_pattern("*.pyd", 0)
            fl.include_pattern("*.so", 0)
            cfg.CLEANUP += fl.files

        for f in cfg.CLEANUP:
            if os.path.isdir(f):
                try:
                    if not self.dry_run and os.path.exists(f):
                        os.rmdir(f)
                    log.info("removing '%s'", f)
                except IOError:
                    log.warning("unable to remove '%s'", f)

            else:
                try:
                    if not self.dry_run and os.path.exists(f):
                        os.remove(f)
                    log.info("removing '%s'", f)
                except IOError:
                    log.warning("unable to remove '%s'", f)



# The Ubuntu Python adds a --install-layout option to distutils that
# is used in our package build.  If we detect that the current
# distutils does not have it then make sure that it is removed from
# the command-line options, otherwise the build will fail.
for item in distutils.command.install.install.user_options:
    if item[0] == 'install-layout=':
        break
else:
    for arg in sys.argv:
        if arg.startswith('--install-layout'):
            sys.argv.remove(arg)
            break



class wx_install(distutils.command.install.install):
    """
    Turns off install_path_file
    """
    def initialize_options(self):
        distutils.command.install.install.initialize_options(self)
        self.install_path_file = 0


class wx_install_headers(distutils.command.install_headers.install_headers):
    """
    Install the header files to the WXPREFIX, with an extra dir per
    filename too
    """
    def initialize_options(self):
        self.root = None
        distutils.command.install_headers.install_headers.initialize_options(self)

    def finalize_options(self):
        self.set_undefined_options('install', ('root', 'root'))
        distutils.command.install_headers.install_headers.finalize_options(self)

    def run(self):
        if os.name == 'nt':
            return
        headers = self.distribution.headers
        if not headers:
            return

        cfg = Config()
        root = self.root
        #print("WXPREFIX is %s, root is %s" % (WXPREFIX, root))
        # hack for universal builds, which append i386/ppc
        # to the root
        if root is None or cfg.WXPREFIX.startswith(os.path.dirname(root)):
            root = ''
        for header, location in headers:
            install_dir = os.path.normpath(root +
                                           cfg.WXPREFIX +
                                           '/include/wx-%d.%d/wx' % (cfg.VER_MAJOR, cfg.VER_MINOR) +
                                           location)
            self.mkpath(install_dir)
            (out, _) = self.copy_file(header, install_dir)
            self.outfiles.append(out)





#----------------------------------------------------------------------
# These functions and class are copied from distutils in Python 2.5
# and then grafted back into the distutils modules so we can change
# how the -arch and -isysroot compiler args are handled.  Basically if
# -arch is specified in our compiler args then we need to strip all of
# the -arch and -isysroot args provided by Python.

import distutils.unixccompiler
import distutils.sysconfig
from distutils.errors import DistutilsExecError, CompileError

def _darwin_compiler_fixup(compiler_so, cc_args):
    """
    This function will strip '-isysroot PATH' and '-arch ARCH' from the
    compile flags if the user has specified one of them in extra_compile_flags.

    This is needed because '-arch ARCH' adds another architecture to the
    build, without a way to remove an architecture. Furthermore GCC will
    barf if multiple '-isysroot' arguments are present.

    I've further modified our copy of this function to check if there
    is a -isysroot flag in the CC/CXX values in the environment. If so then we
    want to make sure that we keep that one and strip the others, instead of
    stripping it and leaving Python's.
    """
    ccHasSysroot = '-isysroot' in os.environ.get('CC', '') \
                 or '-isysroot' in os.environ.get('CXX', '')

    stripArch = stripSysroot = 0

    compiler_so = list(compiler_so)
    kernel_version = os.uname()[2] # 8.4.3
    major_version = int(kernel_version.split('.')[0])

    if major_version < 8:
        # OSX before 10.4.0, these don't support -arch and -isysroot at
        # all.
        stripArch = stripSysroot = True
    else:
        stripArch = '-arch' in cc_args
        stripSysroot = '-isysroot' in cc_args

    if stripArch:
        while 1:
            try:
                index = compiler_so.index('-arch')
                # Strip this argument and the next one:
                del compiler_so[index:index+2]
            except ValueError:
                break

    if stripSysroot:
        index = 0
        if ccHasSysroot:
            index = compiler_so.index('-isysroot') + 1
        while 1:
            try:
                index = compiler_so.index('-isysroot', index)
                # Strip this argument and the next one:
                del compiler_so[index:index+2]
            except ValueError:
                break

    # Check if the SDK that is used during compilation actually exists,
    # the universal build requires the usage of a universal SDK and not all
    # users have that installed by default.
    sysroot = None
    if '-isysroot' in cc_args:
        idx = cc_args.index('-isysroot')
        sysroot = cc_args[idx+1]
    elif '-isysroot' in compiler_so:
        idx = compiler_so.index('-isysroot')
        sysroot = compiler_so[idx+1]

    if sysroot and not os.path.isdir(sysroot):
        log.warn("Compiling with an SDK that doesn't seem to exist: %s",
                sysroot)
        log.warn("Please check your Xcode installation")

    return compiler_so


def _darwin_compiler_fixup_24(compiler_so, cc_args):
    compiler_so = _darwin_compiler_fixup(compiler_so, cc_args)
    return compiler_so, cc_args


class MyUnixCCompiler(distutils.unixccompiler.UnixCCompiler):
    def _compile(self, obj, src, ext, cc_args, extra_postargs, pp_opts):
        compiler_so = self.compiler_so
        if sys.platform == 'darwin':
            compiler_so = _darwin_compiler_fixup(compiler_so, cc_args + extra_postargs)
        try:
            self.spawn(compiler_so + cc_args + [src, '-o', obj] +
                       extra_postargs)
        except DistutilsExecError as msg:
            raise CompileError(msg)

_orig_parse_makefile = distutils.sysconfig.parse_makefile
def _parse_makefile(filename, g=None):
    rv = _orig_parse_makefile(filename, g)

    # If a different deployment target is specified in the
    # environment then make sure it is put in the global
    # config dict.
    if os.getenv('MACOSX_DEPLOYMENT_TARGET'):
        val = os.getenv('MACOSX_DEPLOYMENT_TARGET')
        rv['MACOSX_DEPLOYMENT_TARGET'] = val
        rv['CONFIGURE_MACOSX_DEPLOYMENT_TARGET'] = val

    return rv


distutils.unixccompiler.UnixCCompiler = MyUnixCCompiler
distutils.unixccompiler._darwin_compiler_fixup = _darwin_compiler_fixup
distutils.unixccompiler._darwin_compiler = _darwin_compiler_fixup_24
distutils.sysconfig.parse_makefile = _parse_makefile


# Inject a little code into the CCompiler class that will check if the object
# file is up to date with respect to its source file and any other
# dependencies associated with the extentension. If so then it is removed from
# the collection of files to build.
_orig_setup_compile = distutils.ccompiler.CCompiler._setup_compile
def _setup_compile(self, outdir, macros, incdirs, sources, depends, extra):
    macros, objects, extra, pp_opts, build = \
          _orig_setup_compile(self, outdir, macros, incdirs, sources, depends, extra)

    # Remove items from the build collection that don't need to be built
    # because their obj file is newer than the source file and any other
    # dependencies.
    for obj in objects:
        src, ext = build[obj]
        if not newer_group([src] + depends, obj):
            del build[obj]
    return macros, objects, extra, pp_opts, build

distutils.ccompiler.CCompiler._setup_compile = _setup_compile

#----------------------------------------------------------------------
# Another hack-job for the CygwinCCompiler class, this time replacing
# the _compile function with one that will pass the -I flags to windres.

import distutils.cygwinccompiler
from distutils.errors import DistutilsExecError, CompileError

def _compile(self, obj, src, ext, cc_args, extra_postargs, pp_opts):
    if ext == '.rc' or ext == '.res':
        # gcc needs '.res' and '.rc' compiled to object files !!!
        try:
            #self.spawn(["windres", "-i", src, "-o", obj])
            self.spawn(["windres", "-i", src, "-o", obj] +
                       [arg for arg in cc_args if arg.startswith("-I")] )
        except DistutilsExecError as msg:
            raise CompileError(msg)
    else: # for other files use the C-compiler
        try:
            self.spawn(self.compiler_so + cc_args + [src, '-o', obj] +
                       extra_postargs)
        except DistutilsExecError as msg:
            raise CompileError(msg)

distutils.cygwinccompiler.CygwinCCompiler._compile = _compile


#----------------------------------------------------------------------
# Yet another distutils hack, this time for the msvc9compiler.  There
# is a bug in at least version distributed with Python 2.6 where it
# adds '/pdb:None' to the linker command-line, but that just results
# in a 'None' file being created instead of putting the debug info
# into the .pyd files as expected.  So we'll strip out that option via
# a monkey-patch of the msvc9compiler.MSVCCompiler.initialize method.

if os.name == 'nt' and  sys.version_info >= (2,6):
    import distutils.msvc9compiler
    _orig_initialize = distutils.msvc9compiler.MSVCCompiler.initialize

    def _initialize(self, *args, **kw):
        rv = _orig_initialize(self, *args, **kw)
        try:
            self.ldflags_shared_debug.remove('/pdb:None')
        except ValueError:
            pass
        return rv

    distutils.msvc9compiler.MSVCCompiler.initialize = _initialize


#----------------------------------------------------------------------


from .sipdistutils import build_ext

class etgsip_build_ext(build_ext):
    """
    Override some parts of the SIP build command class so we can better
    control how SIP is used
    """
    def _find_sip(self):
        cfg = Config()
        return cfg.SIP

    def _sip_inc_dir(self):
        cfg = Config()
        return cfg.SIPINC

    def _sip_sipfiles_dir(self):
        cfg = Config()
        return cfg.SIPFILES

    def _sip_output_dir(self):
        cfg = Config()
        return cfg.SIPOUT


    def build_extension(self, extension):
        """
        Modify the dependency list, adding the sip files generated
        from the etg files.
        """
        sources = extension.sources
        if sources is not None and isinstance(sources, (list, tuple)):
            etg_sources = [s for s in sources if s.startswith('etg/')]
            for e in etg_sources:
                extension.depends.append(etg2sip(e))

        # let the base class do the rest
        return build_ext.build_extension(self, extension)


    def swig_sources (self, sources, extension):
        """
        Run our ETG scripts to generate their .sip files, and adjust
        the sources list before passing on to the base class, which
        will then be responsible for running SIP and building the
        generated C++ files.
        """
        if not self.extensions:
            return

        cfg = Config()

        etg_sources = [s for s in sources if s.startswith('etg/')]
        other_sources = [s for s in sources if not s.startswith('etg/')]

        for etg in etg_sources:
            sipfile = etg2sip(etg)

            deps = [etg]
            ns = loadETG(etg)
            if hasattr(ns, 'OTHERDEPS'):
                deps += ns.OTHERDEPS
            if newer_group(deps, sipfile):
                cmd = [sys.executable, etg, '--sip']
                #if cfg.verbose:
                #    cmd.append('--verbose')
                self.spawn(cmd)

            if '%Module(' in file(sipfile).read():
                other_sources.append(sipfile)

        # now call the base class version of this method
        return build_ext.swig_sources(self, other_sources, extension)


    def _sip_compile(self, sip_bin, source, sbf):
        cfg = Config()

        other_opts = []
        base = os.path.basename(source)
        if base.startswith('_'):
            pycode = os.path.splitext(base[1:])[0] + '.py'
            pycode = posixjoin(cfg.PKGDIR, pycode)
            other_opts = ['-X', 'pycode:'+pycode]
        self.spawn([sip_bin] + self.sip_opts +
                   other_opts +
                   ["-c", self._sip_output_dir(),
                    "-b", sbf,
                    "-I", self._sip_sipfiles_dir(),
                    source])
