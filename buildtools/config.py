#----------------------------------------------------------------------
# Name:        buildtools.config
# Purpose:     Code to set and validate platform options and etc. for
#              the wxPython build.  Moved to their own module and
#              class to help setup.py to be simpler.
#
# Author:      Robin Dunn
#
# Created:     3-Nov-2010
# Copyright:   (c) 2013-2017 by Total Control Software
# License:     wxWindows License
#----------------------------------------------------------------------

import sys
import os
import glob
import fnmatch
import re
import shutil
import subprocess
import platform

from distutils.file_util import copy_file
from distutils.dir_util  import mkpath
from distutils.dep_util  import newer

import distutils.sysconfig

runSilently = False

#----------------------------------------------------------------------

class Configuration(object):

    ##SIP      = SIPdefault         # Where is the sip binary?
    SIPINC   = 'sip/siplib'       # Use our local copy of sip.h
    SIPGEN   = 'sip/gen'          # Where the generated .sip files go
    SIPFILES = 'sip'              # where to find other sip files for %Include or %Import
    SIPOUT   = 'sip/cpp'          # where to put the generated C++ code

    ROOT_DIR = os.path.abspath(os.path.split(__file__)[0]+'/..')

    # we need the WXWIN dir to configure this, see __init__
    DOXY_XML_DIR = None

    WX_CONFIG = None
    # Usually you shouldn't need to touch this, but you can set it to
    # pass an alternate version of wx-config or alternate flags,
    # eg. as required by the .deb in-tree build.  By default a
    # wx-config command will be assembled based on version, port,
    # etc. and it will be looked for on the default $PATH.

    WXPORT = 'gtk3'
    # On Linux/Unix there are several ports of wxWidgets available.
    # Setting this value lets you select which will be used for the
    # wxPython build.  Possibilities are 'gtk', 'gtk2', 'gtk3' and 'x11'.
    # Currently only gtk, gtk2 and gtk3 work.

    BUILD_BASE = "build"
    # Directory to use for temporary build files.

    MONOLITHIC = 0
    # The core wxWidgets lib can be built as either a single
    # monolithic DLL or as a collection of DLLs.  This flag controls
    # which set of libs will be used on Windows.  (For other platforms
    # it is automatic via using wx-config.)

    WXDLLVER = None
    # Version part of wxWidgets LIB/DLL names

    COMPILER = 'msvc'
    # Used to select which compiler will be used on Windows.  This not
    # only affects distutils, but also some of the default flags and
    # other assumptions in this script.  Current supported values are
    # 'msvc' and 'mingw32'

    ARCH = ''
    # If this is set, add an -arch XXX flag to cflags. Only tested (and
    # presumably, needed) for OS X.

    NO_SCRIPTS = False
    # Don't install the tools/script files

    PKGDIR = 'wx'
    # The name of the top-level package

    # ---------------------------------------------------------------
    # Basic initialization and configuration code

    def __init__(self, noWxConfig=False):
        self.CLEANUP = list()

        self.resetVersion()

        # change the PORT default for wxMac
        if sys.platform[:6] == "darwin":
            self.WXPORT = 'osx_cocoa'

        # and do the same for wxMSW, just for consistency
        if os.name == 'nt':
            self.WXPORT = 'msw'

        self.parseCmdLine()

        if self.WXPORT != 'msw':
            # make sure we only use the compiler value on MSW builds
            self.COMPILER=None

        self.WXPLAT2 = None
        self.WXDIR = wxDir()

        self.includes = [phoenixDir() + '/sip/siplib',  # to get our version of sip.h
                         phoenixDir() + '/src',         # for any hand-written headers
                         ]

        self.DOXY_XML_DIR = os.path.join(self.WXDIR, 'docs/doxygen/out/xml')

        self.SIPOPTS  = ' '.join([
                         '-w',    # enable warnings
                         '-o',    # turn on auto-docstrings
                         '-g',    # turn on acquire/release of GIL for everything
                         #'-e',    # turn on exceptions support
                         #'-T',    # turn off writing the timestamp to the generated files                         '-g',    # always release and reaquire the GIL
                         #'-r',    # turn on function call tracing
                         '-I', os.path.join(phoenixDir(), 'src'),
                         '-I', os.path.join(phoenixDir(), 'sip', 'gen'),
                         ])

        if noWxConfig:
            # this is as far as we go for now
            return

        # otherwise do the rest of it
        self.finishSetup()


    def finishSetup(self, wx_config=None, debug=None):
        if wx_config is not None:
            self.WX_CONFIG = wx_config

        if debug is not None:
            self.debug = debug

        #---------------------------------------
        # MSW specific settings
        if os.name == 'nt' and  self.COMPILER == 'msvc':
            # Set compile flags and such for MSVC.  These values are derived
            # from the wxWidgets makefiles for MSVC, other compilers settings
            # will probably vary...
            self.WXPLAT = '__WXMSW__'

            if os.environ.get('CPU', None) in ['AMD64', 'X64']:
                self.VCDLL = 'vc%s_x64_dll' % getVisCVersion()
            else:
                self.VCDLL = 'vc%s_dll' % getVisCVersion()

            self.includes += ['include',
                              opj(self.WXDIR, 'lib', self.VCDLL, 'msw'  + self.libFlag()),
                              opj(self.WXDIR, 'include'),
                              opj(self.WXDIR, 'contrib', 'include'),
                              ]

            self.defines = [ ('WIN32', None),
                             ('_WINDOWS', None),
                             (self.WXPLAT, None),
                             ('WXUSINGDLL', '1'),
                             ('ISOLATION_AWARE_ENABLED', None),
                             #('NDEBUG',),  # using a 1-tuple makes it do an undef
                             ]

            self.libs = []
            self.libdirs = [ opj(self.WXDIR, 'lib', self.VCDLL) ]
            if self.MONOLITHIC:
                self.libs += makeLibName('')
            else:
                self.libs += [ 'wxbase' + self.WXDLLVER + self.libFlag(),
                               'wxbase' + self.WXDLLVER + self.libFlag() + '_net',
                               self.makeLibName('core')[0],
                               ]

            self.libs += ['kernel32', 'user32', 'gdi32', 'comdlg32',
                          'winspool', 'winmm', 'shell32', 'oldnames', 'comctl32',
                          'odbc32', 'ole32', 'oleaut32', 'uuid', 'rpcrt4',
                          'advapi32', 'wsock32']

            self.cflags = [ '/UNDEBUG',
                            '/Gy',
                            '/EHsc',
                            # '/GX-'  # workaround for internal compiler error in MSVC on some machines
                            ]
            self.lflags = None

            # Other MSVC flags...
            # Uncomment these to have debug info for all kinds of builds
            #self.cflags += ['/Od', '/Z7']
            #self.lflags = ['/DEBUG', ]


        #---------------------------------------
        # Posix (wxGTK, wxMac or mingw32) settings
        elif os.name == 'posix' or self.COMPILER == 'mingw32':
            self.Verify_WX_CONFIG()
            self.includes += ['include']
            self.defines = [ #('NDEBUG',),  # using a 1-tuple makes it do an undef
                             ]
            self.libdirs = []
            self.libs = []

            self.cflags = self.getWxConfigValue('--cxxflags')
            self.cflags = self.cflags.split()
            if self.debug:
                self.cflags.append('-ggdb')
                self.cflags.append('-O0')
            else:
                self.cflags.append('-O3')

            lflags = self.getWxConfigValue('--libs')
            self.MONOLITHIC = (lflags.find("_xrc") == -1)
            self.lflags = lflags.split()

            self.WXBASENAME = self.getWxConfigValue('--basename')
            self.WXRELEASE  = self.getWxConfigValue('--release')
            self.WXPREFIX   = self.getWxConfigValue('--prefix')

            self.CC = self.CXX = self.LDSHARED = None

            # wxMac settings
            if sys.platform[:6] == "darwin":
                self.WXPLAT = '__WXMAC__'

                if self.WXPORT == 'osx_carbon':
                # Flags and such for a Darwin (Max OS X) build of Python
                    self.WXPLAT2 = '__WXOSX_CARBON__'
                else:
                    self.WXPLAT2 = '__WXOSX_COCOA__'

                self.libs = ['stdc++']
                if not self.ARCH == "":
                    for arch in self.ARCH.split(','):
                        self.cflags.append("-arch")
                        self.cflags.append(arch)
                        self.lflags.append("-arch")
                        self.lflags.append(arch)

                if not os.environ.get('CC') or not os.environ.get('CXX'):
                    self.CC =  os.environ["CC"]  = self.getWxConfigValue('--cc')
                    self.CXX = os.environ["CXX"] = self.getWxConfigValue('--cxx')

                    # We want to use the linker command from wx to make sure
                    # we get the right sysroot, but we also need to ensure that
                    # the other linker flags that distutils wants to use are
                    # included as well.
                    LDSHARED = distutils.sysconfig.get_config_var('LDSHARED').split()
                    # remove the compiler command
                    del LDSHARED[0]
                    # remove any -sysroot flags and their arg
                    while 1:
                        try:
                            index = LDSHARED.index('-isysroot')
                            # Strip this argument and the next one:
                            del LDSHARED[index:index+2]
                        except ValueError:
                            break
                    LDSHARED = ' '.join(LDSHARED)
                    # Combine with wx's ld command and stash it in the env
                    # where distutils will get it later.
                    LDSHARED = self.getWxConfigValue('--ld').replace(' -o', '') + ' ' + LDSHARED
                    os.environ["LDSHARED"]  = LDSHARED


            # wxGTK settings
            else:
                # Set flags for other Unix type platforms
                if self.WXPORT == 'gtk':
                    msg("WARNING: The GTK 1.x port is not supported")
                    self.WXPLAT = '__WXGTK__'
                    portcfg = os.popen('gtk-config --cflags', 'r').read()[:-1]
                    self.BUILD_BASE = self.BUILD_BASE + '-' + self.WXPORT
                elif self.WXPORT == 'gtk2':
                    self.WXPLAT = '__WXGTK__'
                    portcfg = os.popen('pkg-config gtk+-2.0 --cflags', 'r').read()[:-1]
                elif self.WXPORT == 'gtk3':
                    self.WXPLAT = '__WXGTK__'
                    portcfg = os.popen('pkg-config gtk+-3.0 --cflags', 'r').read()[:-1]
                elif self.WXPORT == 'x11':
                    msg("WARNING: The wxX11 port is no supported")
                    self.WXPLAT = '__WXX11__'
                    portcfg = ''
                    self.BUILD_BASE = self.BUILD_BASE + '-' + self.WXPORT
                elif self.WXPORT == 'msw':
                    self.WXPLAT = '__WXMSW__'
                    portcfg = ''
                else:
                    raise SystemExit("Unknown WXPORT value: " + self.WXPORT)

                self.cflags += portcfg.split()

                # Some distros (e.g. Mandrake) put libGLU in /usr/X11R6/lib, but
                # wx-config doesn't output that for some reason.  For now, just
                # add it unconditionally but we should really check if the lib is
                # really found there or wx-config should be fixed.
                if self.WXPORT != 'msw':
                    self.libdirs.append("/usr/X11R6/lib")

            # Move the various -I, -D, etc. flags we got from the config scripts
            # into the distutils lists.
            self.cflags = self.adjustCFLAGS(self.cflags, self.defines, self.includes)
            self.lflags = self.adjustLFLAGS(self.lflags, self.libdirs, self.libs)

            self.cflags.insert(0, '-UNDEBUG')

            if self.debug and self.WXPORT == 'msw' and self.COMPILER != 'mingw32':
                self.defines.append( ('_DEBUG', None) )

        # WAF wants a simple list of strings, so convert self.defines in case
        # we'll be using that instead of distutils
        self.wafDefines = []
        for d in self.defines:
            if len(d) > 1:
                name, val = d
                if val:
                    name = name+'='+val
                self.wafDefines.append(name)


    # ---------------------------------------------------------------
    # Helper functions

    def resetVersion(self):
        # load the version numbers into this instance's namespace
        versionfile = opj(os.path.split(__file__)[0], 'version.py')
        myExecfile(versionfile, self.__dict__)

        # Include the subversion revision in the version number? REV.txt can
        # be created using the build.py setrev command. If it doesn't exist
        # then the version number is built without a revision number. IOW, it
        # is a release build.  (In theory)
        if os.path.exists('REV.txt'):
            f = open('REV.txt')
            self.VER_FLAGS += f.read().strip()
            self.BUILD_TYPE = 'snapshot'
            f.close()
        elif os.environ.get('WXPYTHON_RELEASE') == 'yes':
            self.BUILD_TYPE = 'release'
        else:
            self.BUILD_TYPE = 'development'

        self.VERSION = "%s.%s.%s%s" % (self.VER_MAJOR,
                                       self.VER_MINOR,
                                       self.VER_RELEASE,
                                       self.VER_FLAGS)

        self.WXDLLVER = '%d%d' % (self.wxVER_MAJOR, self.wxVER_MINOR)


    def parseCmdLine(self):
        self.debug = '--debug' in sys.argv or '-g' in sys.argv

        if '--gtk2' in sys.argv:
            self.WXPORT = 'gtk2'
        if '--gtk3' in sys.argv:
            self.WXPORT = 'gtk3'

        # the values of the items in the class namespace that start
        # with an upper case letter can be overridden on the command
        # line
        for key, default in Configuration.__dict__.items():
            if key[0] < 'A' or key[0] > 'Z':
                continue
            for idx, arg in enumerate(sys.argv):
                if arg and arg.startswith(key + '='):
                    value = arg.split('=', 1)[1]
                    if isinstance(default, int):
                        value = int(value)
                    setattr(self, key, value)
                    sys.argv[idx] = None

        # remove the cmd line args that we recognized
        sys.argv = [arg for arg in sys.argv if arg is not None]


    def Verify_WX_CONFIG(self):
        """
        Called for the builds that need wx-config. If WX_CONFIG is
        not set then determines the flags needed based on build
        options and searches for wx-config on the PATH.
        """
        # if WX_CONFIG hasn't been set to an explicit value then construct one.
        if self.WX_CONFIG is None:
            self.WX_CONFIG='wx-config'
            port = self.WXPORT
            if port == "x11":
                port = "x11univ"
            flags =  ' --toolkit=%s' % port
            flags += ' --unicode=yes'
            flags += ' --version=%s.%s' % (self.wxVER_MAJOR, self.wxVER_MINOR)

            searchpath = os.environ["PATH"]
            for p in searchpath.split(':'):
                fp = os.path.join(p, 'wx-config')
                if os.path.exists(fp) and os.access(fp, os.X_OK):
                    # success
                    msg("Found wx-config: " + fp)
                    msg("    Using flags: " + flags)
                    self.WX_CONFIG = fp + flags
                    if runSilently:
                        self.WX_CONFIG += " 2>/dev/null "
                    break
            else:
                msg("ERROR: WX_CONFIG not specified and wx-config not found on the $PATH")
                sys.exit(1)
            # TODO:  execute WX_CONFIG --list and verify a matching config is found


    def getWxConfigValue(self, flag):
        cmd = "%s %s" % (self.WX_CONFIG, flag)
        value = os.popen(cmd, 'r').read()[:-1]
        return value



    def build_locale_dir(self, destdir, verbose=1):
        """Build a locale dir under the wxPython package."""
        moFiles = glob.glob(opj(self.WXDIR, 'locale', '*.mo'))
        for src in moFiles:
            lang = os.path.splitext(os.path.basename(src))[0]
            dest = opj(destdir, lang, 'LC_MESSAGES')
            mkpath(dest, verbose=verbose)
            copy_file(src, opj(dest, 'wxstd.mo'), update=1, verbose=verbose)
            self.CLEANUP.append(opj(dest, 'wxstd.mo'))
            self.CLEANUP.append(dest)


    def build_locale_list(self, srcdir):
        # get a list of all files under the srcdir, to be used for install_data
        if sys.version_info[0] == 2:
            def walk_helper(lst, dirname, files):
                for f in files:
                    filename = opj(dirname, f)
                    if not os.path.isdir(filename):
                        lst.append( (dirname, [filename]) )
            file_list = []
            os.path.walk(srcdir, walk_helper, file_list)
            return file_list
        else:
            # TODO: Python3 version using os.walk generator
            return []


    def find_data_files(self, srcdir, *wildcards, **kw):
        # get a list of all files under the srcdir matching wildcards,
        # returned in a format to be used for install_data

        def walk_helper(arg, dirname, files):
            if '.svn' in dirname:
                return
            names = []
            lst, wildcards = arg
            for wc in wildcards:
                wc_name = opj(dirname, wc)
                for f in files:
                    filename = opj(dirname, f)

                    if fnmatch.fnmatch(filename, wc_name) and not os.path.isdir(filename):
                        names.append(filename)
            if names:
                lst.append( (dirname, names ) )

        file_list = []
        recursive = kw.get('recursive', True)
        if recursive:
            os.path.walk(srcdir, walk_helper, (file_list, wildcards))
        else:
            walk_helper((file_list, wildcards),
                        srcdir,
                        [os.path.basename(f) for f in glob.glob(opj(srcdir, '*'))])
        return file_list


    def makeLibName(self, name, checkMonolithic=False, isMSWBase=False):
        if checkMonolithic and self.MONOLITHIC:
            return []
        basename = 'base' if isMSWBase else 'msw'
        if os.name == 'posix' or self.COMPILER == 'mingw32':
            libname = '%s_%s-%s' % (self.WXBASENAME, name, self.WXRELEASE)
        elif name:
            libname = 'wx%s%s%s_%s' % (basename, self.WXDLLVER, self.libFlag(), name)
        else:
            libname = 'wx%s%s%s' % (basename, self.WXDLLVER, self.libFlag())
        return [libname]


    def libFlag(self):
        if not self.debug:
            rv = ''
        else:
            rv = 'd'
        if True: ##UNICODE:
            rv = 'u' + rv
        return rv


    def findLib(self, name, libdirs):
        name = self.makeLibName(name)[0]
        if os.name == 'posix' or self.COMPILER == 'mingw32':
            lflags = self.getWxConfigValue('--libs')
            lflags = lflags.split()

            # if wx-config --libs output does not start with -L, wx is
            # installed with a standard prefix and wx-config does not
            # output these libdirs because they are already searched by
            # default by the compiler and linker.
            if lflags[0][:2] != '-L':
                dirs = libdirs + ['/usr/lib', '/usr/local/lib']
            else:
                dirs = libdirs
            name = 'lib'+name
        else:
            dirs = libdirs[:]
        for d in dirs:
            p = os.path.join(d, name)
            if glob.glob(p+'*') != []:
                return True
        return False




    def adjustCFLAGS(self, cflags, defines, includes):
        """
        Extract the raw -I, -D, and -U flags from cflags and put them into
        defines and includes as needed.
        """
        newCFLAGS = []
        for flag in cflags:
            if flag[:2] == '-I':
                includes.append(flag[2:])
            elif flag[:2] == '-D':
                flag = flag[2:]
                if flag.find('=') == -1:
                    defines.append( (flag, None) )
                else:
                    defines.append( tuple(flag.split('=')) )
            elif flag[:2] == '-U':
                defines.append( (flag[2:], ) )
            else:
                newCFLAGS.append(flag)
        return newCFLAGS



    def adjustLFLAGS(self, lflags, libdirs, libs):
        """
        Extract the -L and -l flags from lflags and put them in libdirs and
        libs as needed
        """
        newLFLAGS = []
        for flag in lflags:
            if flag[:2] == '-L':
                libdirs.append(flag[2:])
            elif flag[:2] == '-l':
                libs.append(flag[2:])
            else:
                newLFLAGS.append(flag)
        return newLFLAGS



# We'll use a factory function so we can use the Configuration class as a singleton
_config = None

def Config(*args, **kw):
    global _config
    if _config is None:
        _config = Configuration(*args, **kw)
    return _config


#----------------------------------------------------------------------
# other helpers

def msg(text):
    if not runSilently:
        print(text)


def opj(*args):
    path = os.path.join(*args)
    return os.path.normpath(path)


def posixjoin(a, *p):
    """Join two or more pathname components, inserting sep as needed"""
    path = a
    for b in p:
        if os.path.isabs(b):
            path = b
        elif path == '' or path[-1:] in '/\\:':
            path = path + b
        else:
            path = path + '/' + b
    return path


def loadETG(name):
    """
    Execute an ETG script so we can load a namespace with its contents (such
    as a list of dependencies, etc.) for use by setup.py
    """
    class _Namespace(object):
        def __init__(self):
            self.__dict__['__name__'] = 'namespace'
        def nsdict(self):
            return self.__dict__

    ns = _Namespace()
    myExecfile(name, ns.nsdict())
    return ns


def etg2sip(etgfile):
    cfg = Config()
    sipfile = os.path.splitext(os.path.basename(etgfile))[0] + '.sip'

    sipfile = posixjoin(cfg.SIPGEN, sipfile)
    return sipfile


def _getSbfValue(etg, keyName):
    cfg = Config()
    sbf = opj(cfg.SIPOUT, etg.NAME + '.sbf')
    out = list()
    for line in open(sbf):
        key, value = line.split('=')
        if key.strip() == keyName:
            return sorted([opj(cfg.SIPOUT, v) for v in value.strip().split()])
    return None

def getEtgSipCppFiles(etg):
    return _getSbfValue(etg, 'sources')

def getEtgSipHeaders(etg):
    return _getSbfValue(etg, 'headers')


def findCmd(cmd):
    """
    Search the PATH for a matching command
    """
    PATH = os.environ['PATH'].split(os.pathsep)
    if os.name == 'nt' and not cmd.endswith('.exe'):
        cmd += '.exe'
    for p in PATH:
        c = os.path.join(p, cmd)
        if os.path.exists(c):
            return c
    return None


def phoenixDir():
    return os.path.abspath(posixjoin(os.path.dirname(__file__), '..'))


def wxDir():
    WXWIN = os.environ.get('WXWIN')
    if not WXWIN:
        WXWIN = os.path.abspath(os.path.join(phoenixDir(), 'ext/wxWidgets'))
    assert WXWIN not in [None, '']
    assert os.path.exists(WXWIN) and os.path.isdir(WXWIN)
    return WXWIN


def copyFile(src, dest, verbose=False):
    """
    Copy file from src to dest, preserving permission bits, etc. If src is a
    symlink then dest will be a symlink as well instead of just copying the
    linked file's contents to a new file.
    """
    if verbose:
        msg('copying %s --> %s' % (src, dest))
    if os.path.islink(src):
        if os.path.exists(dest):
            os.unlink(dest)
        linkto = os.readlink(src)
        os.symlink(linkto, dest)
    else:
        shutil.copy2(src, dest)


def copyIfNewer(src, dest, verbose=False):
    if os.path.isdir(dest):
        dest = os.path.join(dest, os.path.basename(src))
    if newer(src, dest):
        copyFile(src, dest, verbose)


def writeIfChanged(filename, text):
    """
    Check the current contents of filename and only overwrite with text if
    the content is different (therefore preserving the timestamp if there is
    no update.)
    """

    if os.path.exists(filename):
        f = textfile_open(filename, 'rt')
        current = f.read()
        f.close()

        if current == text:
            return

    f = textfile_open(filename, 'wt')
    f.write(text)
    f.close()


# TODO: we might be able to get rid of this when the install code is updated...
def macFixDependencyInstallName(destdir, prefix, extension, buildDir):
    print("**** macFixDependencyInstallName(%s, %s, %s, %s)" % (destdir, prefix, extension, buildDir))
    pwd = os.getcwd()
    os.chdir(destdir+prefix+'/lib')
    dylibs = glob.glob('*.dylib')
    for lib in dylibs:
        #cmd = 'install_name_tool -change %s/lib/%s %s/lib/%s %s' % \
        #      (destdir+prefix,lib,  prefix,lib,  extension)
        cmd = 'install_name_tool -change %s/lib/%s %s/lib/%s %s' % \
              (buildDir,lib,  prefix,lib,  extension)
        print(cmd)
        os.system(cmd)
    os.chdir(pwd)


def macSetLoaderNames(filenames):
    """
    Scan the list of dynamically loaded files for each file in filenames,
    replacing the path for the wxWidgets libraries with "@loader_path"
    """
    for filename in filenames:
        if not os.path.isfile(filename):
            continue
        # TODO: Change the -id too?
        for line in os.popen('otool -L %s' % filename, 'r').readlines():  # -arch all  ??
            if line.startswith('\t') and 'libwx_' in line:
                line = line.strip()
                endPos = line.rfind(' (')
                curName = line[:endPos]
                newName = '@loader_path/' + os.path.basename(curName)
                cmd = 'install_name_tool -change %s %s %s' % (curName, newName, filename)
                os.system(cmd)


def getVcsRev():
    # Some helpers for the code below
    def _getDate():
        import datetime
        now = datetime.datetime.now()
        return "%d%02d%02d.%02d%02d" % (now.year, now.month, now.day, now.hour, now.minute)

    def _getSvnRevision():
        if not os.path.exists('.svn'):
            return None
        svnrev = None
        try:
            rev = runcmd('svnversion', getOutput=True, echoCmd=False)
        except:
            return None
        svnrev = rev.split(':')[0]
        return svnrev

    def _getGitRevision():
        try:
            revcount = runcmd('git rev-list --count HEAD', getOutput=True, echoCmd=False)
            revhash  = runcmd('git rev-parse --short HEAD', getOutput=True, echoCmd=False)
        except:
            return None
        return "{}+{}".format(revcount, revhash)

    # Try getting the revision number from SVN, or GIT, or just fall back
    # to the date.
    svnrev = _getSvnRevision()
    if not svnrev:
        svnrev = _getGitRevision()
    if not svnrev:
        svnrev = _getDate()
        msg('WARNING: Unable to determine SVN revision, using date (%s) instead.' % svnrev)
    return svnrev


def runcmd(cmd, getOutput=False, echoCmd=True, fatal=True):
    """
    Runs a give command-line command, optionally returning the output.
    """
    if isinstance(cmd, list):
        # add quotes to elements of the command that need it
        cmd = cmd[:]
        for idx, item in enumerate(cmd):
            if ' ' in item or '\t' in item or ';' in item:
                if item[0] not in ['"', "'"]:
                    if '"' in item:
                        item = item.replace('"', '\\"')
                    item = '"{}"'.format(item)
                    cmd[idx] = item
        # convert the resulting command to a string
        cmd = ' '.join(cmd)

    if echoCmd:
        msg(cmd)

    otherKwArgs = dict()
    if getOutput:
        otherKwArgs = dict(stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)

    sp = subprocess.Popen(cmd, shell=True, env=os.environ, **otherKwArgs)

    output = None
    if getOutput:
        outputEncoding = 'cp1252' if sys.platform == 'win32' else 'utf-8'
        output = sp.stdout.read()
        if sys.version_info > (3,):
            output = output.decode(outputEncoding)
        output = output.rstrip()

    rval = sp.wait()
    if rval:
        # Failed!
        #raise subprocess.CalledProcessError(rval, cmd)
        print("Command '%s' failed with exit code %d." % (cmd, rval))
        if getOutput:
            print(output)
        if fatal:
            sys.exit(rval)

    return output


def myExecfile(filename, ns):
    if sys.version_info < (3,):
        execfile(filename, ns)
    else:
        with open(filename, 'r') as f:
            exec(f.read(), ns)


def textfile_open(filename, mode='rt'):
    """
    Simple wrapper around open() that will use codecs.open on Python2 and
    on Python3 will add the encoding parameter to the normal open(). The
    mode parameter must include the 't' to put the stream into text mode.
    """
    assert 't' in mode
    if sys.version_info < (3,):
        import codecs
        mode = mode.replace('t', '')
        return codecs.open(filename, mode, encoding='utf-8')
    else:
        return open(filename, mode, encoding='utf-8')


def getSipFiles(names):
    """
    Returns a list of the coresponding .sip files for each of the names in names.
    """
    files = list()
    for template in ['sip/gen/%s.sip', 'src/%s.sip']:
        for name in names:
            name = template % name
            if os.path.exists(name):
                files.append(name)
    return files



def getVisCVersion():
    text = runcmd("cl.exe", getOutput=True, echoCmd=False)
    if 'Version 13' in text:
        return '71'
    if 'Version 15' in text:
        return '90'
    if 'Version 16' in text:
        return '100'
    if 'Version 18' in text:
        return '120'
    if 'Version 19' in text:
        return '140'
    # TODO: Add more tests to get the other versions...
    else:
        return 'FIXME'


_haveObjDump = None
def canGetSOName():
    global _haveObjDump
    if _haveObjDump is None:
        _haveObjDump = findCmd('objdump') is not None
    return _haveObjDump


def getSOName(filename):
    output = runcmd('objdump -p %s' % filename, True)
    result = re.search('^\s+SONAME\s+(.+)$', output, re.MULTILINE)
    if result:
        return result.group(1)
    return None


def getToolsPlatformName(useLinuxBits=False):
    name = sys.platform
    if name.startswith('linux'):
        name = 'linux'
        if useLinuxBits:
            name += platform.architecture()[0][:2]
    return name


def updateLicenseFiles(cfg):
    from distutils.file_util import copy_file
    from distutils.dir_util  import mkpath

    # Copy the license files from wxWidgets
    mkpath('license')
    for filename in ['preamble.txt', 'licence.txt', 'lgpl.txt', 'gpl.txt']:
        copy_file(opj(cfg.WXDIR, 'docs', filename), opj('license',filename), update=1, verbose=1)

    # Combine the relevant files into a single LICENSE.txt file
    text = ''
    for filename in ['preamble.txt', 'licence.txt', 'lgpl.txt']:
        with open(opj('license', filename), 'r') as f:
            text += f.read() + '\n\n'
    with open('LICENSE.txt', 'w') as f:
        f.write(text)
