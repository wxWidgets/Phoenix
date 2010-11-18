#----------------------------------------------------------------------
# Name:        buildtools.config
# Purpose:     Code to set and validate platform options and etc. for
#              the wxPython build.  Moved to their own module and
#              class to help setup.py to be simpler.
#
# Author:      Robin Dunn
#
# Created:     3-Nov-2010
# Copyright:   (c) 2010 by Total Control Software
# License:     wxWindows License
#----------------------------------------------------------------------

import sys
import os
import glob
import fnmatch
import tempfile

from distutils.file_util import copy_file
from distutils.dir_util  import mkpath
from distutils.dep_util  import newer
from distutils.spawn     import spawn


runSilently = False

#----------------------------------------------------------------------
# Set some defaults based on the environment or platform

if os.environ.get('SIP'):
    SIPdefault = os.environ.get('SIP')

elif os.name == 'nt':
    SIPdefault = 'c:/projects/sip/sip/sipgen/sip.exe'

else:
    SIPdefault = '/projects/sip/sip/sipgen/sip' 

    
#----------------------------------------------------------------------

class Configuration(object):
    
    USE_SIP  = True
    SIP      = SIPdefault
    SIPINC   = 'sip/siplib'       # Use our local copy of sip.h
    SIPGEN   = 'sip/gen'          # Where the generated .sip files go
    SIPFILES = 'sip'              # where to find other sip files for %Include or %Import
    SIPOUT   = 'sip/cpp'          # where to put the generated C++ code
    
    SIPOPTS  = ' '.join(['-k',    # turn on keyword args support
                         '-o',    # turn on auto-docstrings
                         '-e',    # turn on exceptions support
                         '-T',    # turn off writing the timestamp to the generated files
                         #'-g',   # always release and reaquire the GIL
                         #'-r',   # turn on function call tracing
                         '-I', 'src'
                         ])

    WX_CONFIG = None
    # Usually you shouldn't need to touch this, but you can set it to
    # pass an alternate version of wx-config or alternate flags,
    # eg. as required by the .deb in-tree build.  By default a
    # wx-config command will be assembled based on version, port,
    # etc. and it will be looked for on the default $PATH.

    WXPORT = 'gtk2'
    # On Linux/Unix there are several ports of wxWidgets available.
    # Setting this value lets you select which will be used for the
    # wxPython build.  Possibilites are 'gtk', 'gtk2' and 'x11'.
    # Currently only gtk and gtk2 works.

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
    
    def __init__(self):
        self.CLEANUP = list()
        
        # load the version numbers into this instance's namespace
        execfile(opj(os.path.split(__file__)[0], 'version.py'), self.__dict__)
        
        # If we're doing a dated build then alter the VERSION strings
        if os.path.exists('DAILY_BUILD'):
            self.VER_FLAGS += '.b' + open('DAILY_BUILD').read().strip()
        self.VERSION = "%s.%s.%s.%s%s" % (self.VER_MAJOR, 
                                          self.VER_MINOR, 
                                          self.VER_RELEASE,
                                          self.VER_SUBREL, 
                                          self.VER_FLAGS)

        self.WXDLLVER = '%d%d' % (self.VER_MAJOR, self.VER_MINOR)

        # change the PORT default for wxMac
        if sys.platform[:6] == "darwin":
            self.WXPORT = 'osx_carbon'

        # and do the same for wxMSW, just for consistency
        if os.name == 'nt':
            self.WXPORT = 'msw'

        self.parseCmdLine()

        if self.WXPORT != 'msw':
            # make sure we only use the compiler value on MSW builds
            self.COMPILER=None

        self.WXPLAT2 = None

        
        if os.environ.has_key('WXWIN'):
            self.WXDIR = os.environ['WXWIN']
        else:
            if os.path.exists('../wxWidgets'):
                self.WXDIR = '../wxWidgets'  # assumes in parallel SVN tree
            else:
                self.WXDIR = '..'  # assumes wxPython is subdir
            msg("WARNING: WXWIN not set in environment. Assuming '%s'" % self.WXDIR)
        
        self.includes = ['sip/siplib']  # to get our version of sip.h
         
        #---------------------------------------
        # MSW specific settings
        if os.name == 'nt' and  self.COMPILER == 'msvc':
            # Set compile flags and such for MSVC.  These values are derived
            # from the wxWidgets makefiles for MSVC, other compilers settings
            # will probably vary...
            self.WXPLAT = '__WXMSW__'
        
            if os.environ.get('CPU', None) == 'AMD64':
                self.VCDLL = 'vc_amd64_dll'
            else:
                self.VCDLL = 'vc_dll'
                
            self.includes = ['include', 'src',
                             opj(self.WXDIR, 'lib', self.VCDLL, 'msw'  + self.libFlag()),
                             opj(self.WXDIR, 'include'),
                             opj(self.WXDIR, 'contrib', 'include'),
                             ]
        
            self.defines = [ ('WIN32', None),
                             ('_WINDOWS', None),
                             (self.WXPLAT, None),
                             ('WXUSINGDLL', '1'),
                             ('ISOLATION_AWARE_ENABLED', None),
                             ('NDEBUG',),  # using a 1-tuple makes it do an undef
                             ]
        
            self.libs = []
            self.libdirs = [ opj(self.WXDIR, 'lib', self.VCDLL) ]
            if self.MONOLITHIC:
                self.libs += makeLibName('')
            else:
                self.libs += [ 'wxbase' + self.WXDLLVER + self.libFlag(), 
                               'wxbase' + self.WXDLLVER + self.libFlag() + '_net',
                               'wxbase' + self.WXDLLVER + self.libFlag() + '_xml',
                               self.makeLibName('core')[0],
                               self.makeLibName('adv')[0],
                               self.makeLibName('html')[0],
                               ]
        
            self.libs += ['kernel32', 'user32', 'gdi32', 'comdlg32',
                          'winspool', 'winmm', 'shell32', 'oldnames', 'comctl32',
                          'odbc32', 'ole32', 'oleaut32', 'uuid', 'rpcrt4',
                          'advapi32', 'wsock32']
        
            self.cflags = [ '/Gy',
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
        elif os.name == 'posix' or COMPILER == 'mingw32':
            self.Verify_WX_CONFIG()
            self.includes = ['include', 'src']
            self.defines = [ ('NDEBUG',),  # using a 1-tuple makes it do an undef                            
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
                    self.cflags.append("-arch")
                    self.cflags.append(self.ARCH)
                    self.lflags.append("-arch")
                    self.lflags.append(self.ARCH)
        
                if not os.environ.get('CC') or not os.environ.get('CXX'):
                    os.environ["CXX"] = self.getWxConfigValue('--cxx')
                    os.environ["CC"]  = self.getWxConfigValue('--cc')
                    
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
                elif self.WXPORT == 'x11':
                    msg("WARNING: The wxX11 port is no supported")
                    self.WXPLAT = '__WXX11__'
                    portcfg = ''
                    self.BUILD_BASE = self.BUILD_BASE + '-' + self.WXPORT
                elif self.WXPORT == 'msw':
                    self.WXPLAT = '__WXMSW__'
                    portcfg = ''
                else:
                    raise SystemExit, "Unknown WXPORT value: " + self.WXPORT
        
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
        
            if self.debug and self.WXPORT == 'msw' and self.COMPILER != 'mingw32':
                self.defines.append( ('_DEBUG', None) )
            

    # ---------------------------------------------------------------
    # Helper functions
    
    def parseCmdLine(self):
        self.debug = '--debug' in sys.argv or '-g' in sys.argv

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
            flags += ' --version=%s.%s' % (self.VER_MAJOR, self.VER_MINOR)

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

            # TODO:  execute WX_CONFIG --list and verify a matching config is found


    def getWxConfigValue(self, flag):
        cmd = "%s %s" % (self.WX_CONFIG, flag)
        value = os.popen(cmd, 'r').read()[:-1]
        return value



    def build_locale_dir(self, destdir, verbose=1):
        """Build a locale dir under the wxPython package for MSW"""
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
        def walk_helper(lst, dirname, files):
            for f in files:
                filename = opj(dirname, f)
                if not os.path.isdir(filename):
                    lst.append( (dirname, [filename]) )
        file_list = []
        os.path.walk(srcdir, walk_helper, file_list)
        return file_list
    
    
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
    
    
    def makeLibName(self, name):
        if os.name == 'posix' or self.COMPILER == 'mingw32':
            libname = '%s_%s-%s' % (self.WXBASENAME, name, self.WXRELEASE)
        elif name:
            libname = 'wxmsw%s%s_%s' % (self.WXDLLVER, self.libFlag(), name)
        else:
            libname = 'wxmsw%s%s' % (self.WXDLLVER, self.libFlag())
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
        print text

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
