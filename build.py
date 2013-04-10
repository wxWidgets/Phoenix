#!/usr/bin/python
#---------------------------------------------------------------------------
# This script is used to run through the commands used for the various stages
# of building Phoenix, and can also be a front-end for building wxWidgets and
# the Python extension mocdules.
#---------------------------------------------------------------------------

from __future__ import absolute_import

import sys
import glob
import hashlib
import optparse
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import datetime
if sys.version_info < (3,):
    from urllib2 import urlopen
else:
    from urllib.request import urlopen
    

from distutils.dep_util import newer, newer_group
from buildtools.config  import Config, msg, opj, posixjoin, loadETG, etg2sip, findCmd, \
                               phoenixDir, wxDir, copyIfNewer, copyFile, \
                               macFixDependencyInstallName, macSetLoaderNames, \
                               getSvnRev, runcmd, textfile_open, getSipFiles, \
                               getVisCVersion

import buildtools.version as version

# defaults
PYVER = '2.7'
PYSHORTVER = '27'
PYTHON = None  # it will be set later
PYTHON_ARCH = 'UNKNOWN'

# wx version numbers
version2 = "%d.%d" % (version.VER_MAJOR, version.VER_MINOR) 
version3 = "%d.%d.%d" % (version.VER_MAJOR, version.VER_MINOR, version.VER_RELEASE)
version2_nodot = version2.replace(".", "")
version3_nodot = version3.replace(".", "")
unstable_series = (version.VER_MINOR % 2) == 1  # is the minor version odd or even?
    
isWindows = sys.platform.startswith('win')
isDarwin = sys.platform == "darwin"

baseName = 'wxPython_Phoenix'
eggInfoName = baseName + '.egg-info'


# Some tools will be downloaded for the builds. These are the versions and
# MD5s of the tool binaries currently in use.
sipCurrentVersion = '4.14.4'
sipMD5 = {
    'darwin' : 'dd8d1128fc43586072206038bfa35a66',
    'win32'  : '3edfb918fbddc19ac7a26b931addfeed', 
    'linux'  : 'b9fa64b1f6f5a6407777a0dda0de5778', 
}

wafCurrentVersion = '1.7.10'
wafMD5 = '6825d465baf2968c1d20a58dd65a0e9d'

doxygenCurrentVersion = '1.8.2'
doxygenMD5 = {
    'darwin' : '96a3012d97893f4e05387cda544de0e8',
    'win32'  : '71f97ebaa87171c824a7742de5bf3381', 
    'linux'  : '6fca3d2016f8019a7737716eee4d5377', 
}

# And the location where they can be downloaded from
toolsURL = 'http://wxpython.org/Phoenix/tools'

#---------------------------------------------------------------------------

def usage():
    print ("""\
Usage: ./build.py [command(s)] [options]

  Commands:
      N.N NN        Major.Minor version number of the Python to use to run 
                    the other commands.  Default is 2.7.  Or you can use 
                    --python to specify the actual Python executable to use.
                    
      dox           Run Doxygen to produce the XML file used by ETG scripts
      doxhtml       Run Doxygen to create the HTML documetation for wx
      touch         'touch' the etg files so they will all get run the next  
                    time the etg command is run.
      etg           Run the ETG scripts that are out of date to update their 
                    SIP files and their Sphinx input files
      sip           Run sip
      
      wxlib         Build the Sphinx input files for wx.lib
      wxpy          Build the Sphinx input files for wx.py
      wxtools       Build the Sphinx input files for wx.tools
      sphinx        Run the documentation building process using Sphinx
      
      test          Run the unit test suite
      test_*        Run just one test module
        
      build         Build both wxWidgets and wxPython
      build_wx      Do only the wxWidgets part of the build
      build_py      Build wxPython only

      install       Install both wxWidgets and wxPython
      install_wx    Install wxWidgets (but only if this tool was 
                    configured to build it)
      install_py    Install wxPython only
        
      sdist         Build a tarball containing all source files
      bdist         Create a binary release of wxPython Phoenix
      docs_bdist    Build a tarball containing the documentation
      bdist_egg     Build a Python egg.  Requires magic.
        
      clean_wx      Clean the wx parts of the build
      clean_py      Clean the wxPython parts of the build
      clean_sphinx  Clean the sphinx files
      
      clean         Clean both wx and wxPython
      cleanall      Clean all and do a little extra scrubbing too
      """)

    parser = makeOptionParser()
    parser.print_help()
    

def main(args):
    setPythonVersion(args)
    setDevModeOptions(args)
    
    os.environ['PYTHONPATH'] = phoenixDir()
    os.environ['PYTHONUNBUFFERED'] = 'yes'
    os.environ['WXWIN'] = wxDir()
    cfg = Config(noWxConfig=True)
    msg('')

    wxpydir = os.path.join(phoenixDir(), "wx")
    if not os.path.exists(wxpydir):
        os.makedirs(wxpydir)

    if not args or 'help' in args or '--help' in args or '-h' in args:
        usage()
        sys.exit(1)
    
    options, commands = parseArgs(args)
    
    while commands:
        # ensure that each command starts with the CWD being the phoenix dir.
        os.chdir(phoenixDir())
        cmd = commands.pop(0)
        if cmd.startswith('test_'):
            testOne(cmd, options, args)
        elif 'cmd_'+cmd in globals():
            function = globals()['cmd_'+cmd]  
            function(options, args)
        else:
            print('*** Unknown command: ' + cmd)
            usage()
            sys.exit(1)
    msg("Done!")
    
    
#---------------------------------------------------------------------------
# Helper functions  (see also buildtools.config for more)
#---------------------------------------------------------------------------

            
def setPythonVersion(args):
    global PYVER
    global PYSHORTVER
    global PYTHON
    global PYTHON_ARCH

    havePyVer = False
    havePyPath = False
    
    for idx, arg in enumerate(args):
        if re.match(r'^[0-9]\.[0-9]$', arg):
            havePyVer = True
            PYVER = arg
            PYSHORTVER = arg[0] + arg[2]
            del args[idx]
            break
        if re.match(r'^[0-9][0-9]$', arg):
            havePyVer = True
            PYVER = '%s.%s' % (arg[0], arg[1])
            PYSHORTVER = arg
            del args[idx]
            break
        if arg.startswith('--python'):
            havePyPath = True
            if '=' in arg:
                PYTHON = arg.split('=')[1]
                del args[idx]
            else:
                PYTHON = args[idx+1]
                del args[idx:idx+2]
            PYVER = runcmd('%s -c "import sys; print(sys.version[:3])"' % PYTHON, 
                           getOutput=True, echoCmd=False)
            PYSHORTVER = PYVER[0] + PYVER[2]
            break
        
    if havePyVer:
        if isWindows and os.environ.get('TOOLS'):
            # Use $TOOLS to find the correct Python. It should be the install
            # root of all Python's on the system, with the 64-bit ones in an
            # amd64 subfolder, like this:
            #
            # $TOOLS\Python27\python.exe
            # $TOOLS\Python33\python.exe
            # $TOOLS\amd64\Python27\python.exe
            # $TOOLS\amd64\Python33\python.exe
            #            
            TOOLS = os.environ.get('TOOLS')
            if 'cygdrive' in TOOLS:
                TOOLS = runcmd('c:/cygwin/bin/cygpath -w '+TOOLS, True, False)
            use64flag = '--x64' in args
            if use64flag:
                args.remove('--x64')
            CPU = os.environ.get('CPU')
            if use64flag or CPU in ['AMD64', 'X64', 'amd64', 'x64']:
                TOOLS = posixjoin(TOOLS, 'amd64')
            PYTHON = posixjoin(TOOLS, 
                               'python%s' % PYSHORTVER,
                               'python.exe')
            
        elif isWindows:
            # Otherwise check if the invoking Python is the right version
            if sys.version[:3] != PYVER:
                msg('ERROR: The invoking Python is not the requested version.  Perhaps you should use --python')
                sys.exit(1)
            PYTHON = sys.executable
            PYVER = sys.version[:3]
            PYSHORTVER = PYVER[0] + PYVER[2]
                
        elif not isWindows:
            # find a pythonX.Y on the PATH
            PYTHON = runcmd("which python%s" % PYVER, True, False)
            
        
    if not PYTHON:
        # If no version or path were specified then default to the python
        # that invoked this script
        PYTHON = sys.executable
        PYVER = sys.version[:3]
        PYSHORTVER = PYVER[0] + PYVER[2]
        
    PYTHON = os.path.abspath(PYTHON)
    msg('Build using: %s' % PYTHON)
        
    msg(runcmd('%s -c "import sys; print(sys.version)"' % PYTHON, True, False))
    PYTHON_ARCH = runcmd('%s -c "import platform; print(platform.architecture()[0])"' 
                         % PYTHON, True, False)
    msg('Python\'s architecture is %s' % PYTHON_ARCH)
    os.environ['PYTHON'] = PYTHON

    if PYTHON_ARCH == '64bit':
        # Make sure this is set in case it wasn't above.
        os.environ['CPU'] = 'X64'
        


def setDevModeOptions(args):
    # Using --dev is a shortcut for setting several build options that I use
    # while working on the code in my local workspaces. Most people will
    # probably not use this so it is not part for the documented options and
    # is explicitly handled here before the options parser is created. If
    # anybody besides Robin is using this option do not depend on the options
    # it inserts into the args list being consistent. They could change at any
    # update from the repository.
    myDevModeOptions = [
            #'--build_dir=../bld',
            #'--prefix=/opt/wx/2.9',
            '--jobs=%s' % numCPUs(),

            # These will be ignored on the other platforms so it is okay to
            # include them unconditionally
            '--osx_cocoa',
            '--mac_arch=x86_64',
            #'--osx_carbon',
            #'--mac_arch=i386',
            #'--mac_arch=i386,x86_64',
            ]
    if not isWindows:
        myDevModeOptions.append('--debug')
    if isWindows:
        myDevModeOptions.append('--cairo')
        
    if '--dev' in args:
        idx = args.index('--dev')
        # replace the --dev item with the items from the list
        args[idx:idx+1] = myDevModeOptions


def numCPUs():
    """
    Detects the number of CPUs on a system.
    This approach is from detectCPUs here: http://www.artima.com/weblogs/viewpost.jsp?thread=230001
    """
    # Linux, Unix and MacOS:
    if hasattr(os, "sysconf"):
        if "SC_NPROCESSORS_ONLN" in os.sysconf_names:
            # Linux & Unix:
            ncpus = os.sysconf("SC_NPROCESSORS_ONLN")
            if isinstance(ncpus, int) and ncpus > 0:
                return ncpus
        else: # OSX:
            p = subprocess.Popen("sysctl -n hw.ncpu", shell=True, stdout=subprocess.PIPE)
            return int(p.stdout.read())
            
    # Windows:
    if "NUMBER_OF_PROCESSORS" in os.environ:
            ncpus = int(os.environ["NUMBER_OF_PROCESSORS"]);
            if ncpus > 0:
                return ncpus
    return 1 # Default
    

def getMSWSettings(options):
    checkCompiler(quiet=True)
    class MSWsettings(object):
        pass
    msw = MSWsettings()
    msw.CPU = os.environ.get('CPU')
    if msw.CPU in ['AMD64', 'X64'] or PYTHON_ARCH == '64bit':
        msw.dllDir = posixjoin(wxDir(), "lib", "vc%s_x64_dll" % getVisCVersion())        
    else:
        msw.dllDir = posixjoin(wxDir(), "lib", "vc%s_dll" % getVisCVersion())
    msw.buildDir = posixjoin(wxDir(), "build", "msw")

    msw.dll_type = "u"
    if options.debug:
        msw.dll_type = "ud"
    return msw
        



def makeOptionParser():
    OPTS = [
        ("python",         ("",    "The python executable to build for.")),
        ("debug",          (False, "Build wxPython with debug symbols")),
        ("keep_hash_lines",(False, "Don't remove the '#line N' lines from the SIP generated code")),
        ("osx_cocoa",      (True,  "Build the OSX Cocoa port on Mac (default)")),
        ("osx_carbon",     (False, "Build the OSX Carbon port on Mac")),
        ("mac_framework",  (False, "Build wxWidgets as a Mac framework.")),
        ("mac_arch",       ("",    "Comma separated list of architectures to build on Mac")),
        
        ("use_syswx",      (False, "Try to use an installed wx rather than building the "
                                   "one in this source tree.  The wx-config in {prefix}/bin "
                                   "or the first found on the PATH determines which wx is "
                                   "used.  Implies --no_magic.")),
        ("force_config",   (False, "Run configure when building even if the script "
                                   "determines it's not necessary.")),
        ("no_config",      (False, "Turn off configure step on autoconf builds")),

        ("no_magic",       (False, "Do NOT use the magic that will enable the wxWidgets "
                                   "libraries to be bundled with wxPython. (Such as when "
                                   "using an uninstalled wx/wxPython from the build dir, "
                                   "or when distributing wxPython as an egg.)  When using "
                                   "this flag you should either build with an already "
                                   "installed wxWidgets, or allow this script to install "
                                   "wxWidgets.")),
        
        ("build_dir",      ("",    "Directory to store wx build files. (Not used on Windows)")),
        ("prefix",         ("",    "Prefix value to pass to the wx build.")), 
        ("destdir",        ("",    "Installation root for wxWidgets, files will go to {destdir}/{prefix}")),
        
        ("extra_setup",    ("", "Extra args to pass on setup.py's command line.")),
        ("extra_make",     ("", "Extra args to pass on [n]make's command line.")),
        ("extra_waf",      ("", "Extra args to pass on waf's command line.")),   
        
        ("jobs",           ("",    "Number of parallel compile jobs to do, if supported.")), 
        ("both",           (False, "Build both a debug and release version. (Only used on Windows)")),
        ("unicode",        (True,  "Build wxPython with unicode support (always on for wx2.9+)")),
        ("verbose",        (False, "Print out more information.")),
        ("nodoc",          (False, "Do not run the default docs generator")),
        ("upload_package", (False, "Upload bdist and/or sdist packages to nightly server.")),
        ("cairo",          (False, "Allow Cairo use with wxGraphicsContext (Windows only)")),
        ("x64",            (False, "Use and build for the 64bit version of Python on Windows")),
        ("jom",            (False, "Use jom instead of nmake for the wxMSW build")),
        ]

    parser = optparse.OptionParser("build options:")
    for opt, info in OPTS:
        default, txt = info
        action = 'store'
        if type(default) == bool:
            action = 'store_true'
        parser.add_option('--'+opt, default=default, action=action,
                          dest=opt, help=txt)
         
    return parser

        
def parseArgs(args):
    parser = makeOptionParser()
    options, args = parser.parse_args(args)
    if isWindows:
        # We always use magic on Windows
        options.no_magic = False
        options.use_syswx = False
    elif options.use_syswx:
        options.no_magic = True
    return options, args


class pushDir(object):
    def __init__(self, newDir):
        self.cwd = os.getcwd()
        os.chdir(newDir)
        
    def __del__(self):
        # pop back to the original dir
        os.chdir(self.cwd)

        
def getBuildDir(options):
    BUILD_DIR = opj(phoenixDir(), 'build', 'wxbld')
    if options.build_dir:
        BUILD_DIR = os.path.abspath(options.build_dir)        
    return BUILD_DIR


def deleteIfExists(deldir, verbose=True):
    if os.path.exists(deldir) and os.path.isdir(deldir):
        try:
            if verbose:
                msg("Removing folder: %s" % deldir)
            shutil.rmtree(deldir)
        except:
            if verbose:
                import traceback
                msg("Error: %s" % traceback.format_exc(1))
        
def delFiles(fileList, verbose=True):
    for afile in fileList:
        if verbose:
            print("Removing file: %s" % afile)
        os.remove(afile)


def getTool(cmdName, version, MD5, envVar, platformBinary):
    # Check in the bin dir for the specified version of the tool command. If
    # it's not there then attempt to download it. Validity of the binary is
    # checked with an MD5 hash.
    if os.environ.get(envVar):
        # Setting a a value in the environment overrides other options
        return os.environ.get(envVar)
    else:
        if platformBinary:
            platform = 'linux' if sys.platform.startswith('linux') else sys.platform
            ext = ''
            if platform == 'win32':
                ext = '.exe'
            cmd = opj(phoenixDir(), 'bin', '%s-%s-%s%s' % (cmdName, version, platform, ext))
            md5 = MD5[platform]
        else:
            cmd = opj(phoenixDir(), 'bin', '%s-%s' % (cmdName, version))
            md5 = MD5

        msg('Checking for %s...' % cmd)
        if os.path.exists(cmd):
            m = hashlib.md5()
            m.update(open(cmd, 'rb').read())
            if m.hexdigest() != md5:
                print('ERROR: MD5 mismatch, got "%s"' % m.hexdigest())
                print('       expected          "%s"' % md5)
                print('       Set %s in the environment to use a local build of %s instead' % (envVar, cmdName))
                sys.exit(1)
            return cmd
            
        msg('Not found.  Attempting to download...')
        url = '%s/%s.bz2' % (toolsURL, os.path.basename(cmd))
        try:
            connection = urlopen(url)
            msg('Connection successful...')
            data = connection.read()
            msg('Data downloaded...')
        except:
            print('ERROR: Unable to download ' + url)
            print('       Set %s in the environment to use a local build of %s instead' % (envVar, cmdName))
            import traceback
            traceback.print_exc()
            sys.exit(1)
            
        import bz2
        data = bz2.decompress(data)
        with open(cmd, 'wb') as f:
            f.write(data)
        os.chmod(cmd, 0o755)
        
        # Recursive call so the MD5 value will be double-checked on what was
        # just downloaded
        return getTool(cmdName, version, MD5, envVar, platformBinary)


            
# The download and MD5 check only needs to happen once per run, cache the sip
# cmd value here the first time through.
_sipCmd = None
def getSipCmd():
    global _sipCmd
    if _sipCmd is None:
        _sipCmd = getTool('sip', sipCurrentVersion, sipMD5, 'SIP', True)
    return _sipCmd


# Same thing for WAF
_wafCmd = None
def getWafCmd():
    global _wafCmd
    if _wafCmd is None:
        _wafCmd = getTool('waf', wafCurrentVersion, wafMD5, 'WAF', False)
    return _wafCmd

# and Doxygen
_doxCmd = None
def getDoxCmd():
    global _doxCmd
    if _doxCmd is None:
        _doxCmd = getTool('doxygen', doxygenCurrentVersion, doxygenMD5, 'DOXYGEN', True)
    return _doxCmd
    
    


class CommandTimer(object):
    def __init__(self, name):
        self.name = name
        self.startTime = datetime.datetime.now()
        msg('Running command: %s' % self.name)
        
    def __del__(self):
        delta = datetime.datetime.now() - self.startTime
        time = ""
        if delta.seconds / 60 > 0:
            time = "%dm" % (delta.seconds / 60)
        time += "%d.%ds" % (delta.seconds % 60, delta.microseconds / 1000)
        msg('Finished command: %s (%s)' % (self.name, time))            



def uploadPackage(fileName, matchString, keep=5):
    """
    Upload the given filename to the configured package server location.
    Only the `keep` number of files containing `matchString` will be
    kept, any others will be removed from the server. It is assumed that
    if the files are in sorted order then the end of the list will be the
    newest files.
    """
    msg("Preparing to upload %s..." % fileName)
    configfile = os.path.join(os.getenv("HOME"), "phoenix_package_server.cfg")
    if not os.path.exists(configfile):
        msg("ERROR: Can not upload, server configuration not set.")
        return
        
    import ConfigParser
    parser = ConfigParser.ConfigParser()
    parser.read(configfile)
    
    msg("Connecting to FTP server...")
    from ftplib import FTP
    ftp = FTP(parser.get("FTP", "host"))
    ftp.login(parser.get("FTP", "user"), parser.get("FTP", "pass"))
    ftp_dir = parser.get("FTP", "dir")
    ftp_path = '%s/%s' % (ftp_dir, os.path.basename(fileName))
    msg("Uploading package (this may take some time)...")
    f = open(fileName, 'rb')
    ftp.storbinary('STOR %s' % ftp_path, f)
    f.close()
    
    allFiles = [name for name in ftp.nlst(ftp_dir) if matchString in name]
    allFiles.sort()  # <== if an alpha sort is not the correct order, pass a cmp function!
    
    # leave the last 5 builds, including this new one, on the server
    for name in allFiles[:-keep]:
        msg("Deleting %s" % name)
        ftp.delete(name)

    ftp.close()
    msg("Upload complete!")



def checkCompiler(quiet=False):
    if isWindows:
        # Make sure that the compiler that Python wants to use can be found.
        # It will terminate if the compiler is not found or other exceptions
        # are raised.
        cmd = "import distutils.msvc9compiler as msvc; " \
              "mc = msvc.MSVCCompiler(); " \
              "mc.initialize(); " \
              "print(mc.cc)"
        CC = runcmd('%s -c "%s"' % (PYTHON, cmd), getOutput=True, echoCmd=False)
        if not quiet:
            msg("MSVC: %s" % CC)
        
        # Now get the environment variables which that compiler needs from
        # its vcvarsall.bat command and load them into this process's
        # environment.
        cmd = "import distutils.msvc9compiler as msvc; " \
              "arch = msvc.PLAT_TO_VCVARS[msvc.get_platform()]; " \
              "env = msvc.query_vcvarsall(msvc.VERSION, arch); " \
              "print(env)"
        env = eval(runcmd('%s -c "%s"' % (PYTHON, cmd), getOutput=True, echoCmd=False))
        os.environ['PATH'] = bytes(env['path'])
        os.environ['INCLUDE'] = bytes(env['include'])
        os.environ['LIB'] = bytes(env['lib'])
        os.environ['LIBPATH'] = bytes(env['libpath'])
        
        
def getWafBuildBase():    
    base = posixjoin('build', 'waf', PYVER)
    if isWindows:
        if PYTHON_ARCH == '64bit':
            base = posixjoin(base, 'x64')
        else:
            base = posixjoin(base, 'x86')
    return base
    
        
#---------------------------------------------------------------------------
# Command functions and helpers
#---------------------------------------------------------------------------


def _doDox(arg):
    doxCmd = getDoxCmd()
    doxCmd = os.path.abspath(doxCmd)
    
    if isWindows:
        doxCmd = doxCmd.replace('\\', '/')
        doxCmd = runcmd('c:/cygwin/bin/cygpath -u '+doxCmd, True, False)
        os.environ['DOXYGEN'] = doxCmd
        os.environ['WX_SKIP_DOXYGEN_VERSION_CHECK'] = '1'
        d = posixjoin(wxDir(), 'docs/doxygen')
        d = d.replace('\\', '/')
        cmd = 'c:/cygwin/bin/bash.exe -l -c "cd %s && ./regen.sh %s"' % (d, arg)
    else:
        os.environ['DOXYGEN'] = doxCmd
        os.environ['WX_SKIP_DOXYGEN_VERSION_CHECK'] = '1'
        pwd = pushDir(posixjoin(wxDir(), 'docs/doxygen'))
        cmd = './regen.sh %s' % arg
    runcmd(cmd)

    
def cmd_dox(options, args):
    cmdTimer = CommandTimer('dox')
    _doDox('xml')
    
    
def cmd_doxhtml(options, args):
    cmdTimer = CommandTimer('doxhtml')
    _doDox('html')
    _doDox('chm')
    
    

def cmd_etg(options, args):
    cmdTimer = CommandTimer('etg')
    cfg = Config()
    assert os.path.exists(cfg.DOXY_XML_DIR), "Doxygen XML folder not found: " + cfg.DOXY_XML_DIR
    
    pwd = pushDir(cfg.ROOT_DIR)

    # TODO: Better support for selecting etg cmd-line flags...
    flags = '--sip'
    if options.nodoc:
        flags += ' --nodoc'

    # get the files to run, moving _core the to the front of the list
    etgfiles = glob.glob(opj('etg', '_*.py'))
    core_file = opj('etg', '_core.py')
    if core_file in etgfiles:
        etgfiles.remove(core_file)
        etgfiles.insert(0, core_file)

    for script in etgfiles:
        sipfile = etg2sip(script)
        deps = [script]
        ns = loadETG(script)
        if hasattr(ns, 'ETGFILES'):
            etgfiles += ns.ETGFILES[1:] # all but itself
        if hasattr(ns, 'DEPENDS'):
            deps += ns.DEPENDS
        if hasattr(ns, 'OTHERDEPS'):
            deps += ns.OTHERDEPS
        
        # run the script only if any dependencies are newer
        if newer_group(deps, sipfile):
            runcmd('%s %s %s' % (PYTHON, script, flags))

    
def cmd_sphinx(options, args):
    from sphinxtools.postprocess import SphinxIndexes, MakeHeadings, PostProcess, GenGallery

    cmdTimer = CommandTimer('sphinx')
    pwd = pushDir(phoenixDir())

    sphinxDir = os.path.join(phoenixDir(), 'docs', 'sphinx')

    if not os.path.isdir(sphinxDir):
        raise Exception('Missing sphinx folder in the distribution') 

    textFiles = glob.glob(sphinxDir + '/*.txt')
    if not textFiles:
        raise Exception('No documentation files found. Please run "build.py touch etg" first')

    # Copy the rst files into txt files
    restDir = os.path.join(sphinxDir, 'rest_substitutions', 'overviews')
    rstFiles = glob.glob(restDir + '/*.rst')  
    for rst in rstFiles:
        rstName = os.path.split(rst)[1]
        txt = os.path.join(sphinxDir, os.path.splitext(rstName)[0] + '.txt')
        copyIfNewer(rst, txt)

    SphinxIndexes(sphinxDir)
    GenGallery()

    todo = os.path.join(phoenixDir(), 'TODO.txt')
    copyIfNewer(todo, sphinxDir)
    txtFiles = glob.glob(os.path.join(phoenixDir(), 'docs', '*.txt'))
    for txtFile in txtFiles:
        copyIfNewer(txtFile, sphinxDir)
    
    MakeHeadings()

    pwd2 = pushDir(sphinxDir)
    buildDir = os.path.join(sphinxDir, 'build')
    htmlDir = os.path.join(phoenixDir(), 'docs', 'html')
    runcmd('sphinx-build -b html -d %s/doctrees . %s' % (buildDir, htmlDir))
    del pwd2
    
    msg('Postprocesing sphinx output...')
    PostProcess(htmlDir)


def cmd_wxlib(options, args):
    from sphinxtools.modulehunter import ModuleHunter

    cmdTimer = CommandTimer('wx.lib')
    pwd = pushDir(phoenixDir())

    libDir = os.path.join(phoenixDir(), 'wx', 'lib')

    if not os.path.isdir(libDir):
        raise Exception('Missing wx.lib folder in the distribution')

    init_name = os.path.join(libDir, '__init__.py')
    import_name = 'lib'
    version = version3

    ModuleHunter(init_name, import_name, version)
    

def cmd_wxpy(options, args):
    from sphinxtools.modulehunter import ModuleHunter

    cmdTimer = CommandTimer('wx.py')
    pwd = pushDir(phoenixDir())

    libDir = os.path.join(phoenixDir(), 'wx', 'py')

    if not os.path.isdir(libDir):
        raise Exception('Missing wx.py folder in the distribution')

    init_name = os.path.join(libDir, '__init__.py')
    import_name = 'py'
    version = version3

    ModuleHunter(init_name, import_name, version)


def cmd_wxtools(options, args):
    from sphinxtools.modulehunter import ModuleHunter

    cmdTimer = CommandTimer('wx.tools')
    pwd = pushDir(phoenixDir())

    libDir = os.path.join(phoenixDir(), 'wx', 'tools')

    if not os.path.isdir(libDir):
        raise Exception('Missing wx.tools folder in the distribution')

    init_name = os.path.join(libDir, '__init__.py')
    import_name = 'tools'
    version = version3

    ModuleHunter(init_name, import_name, version)


def cmd_docs_bdist(options, args):
    cmdTimer = CommandTimer('docs_bdist')
    pwd = pushDir(phoenixDir())

    cfg = Config()
        
    rootname = "%s-%s-docs" % (baseName, cfg.VERSION)
    tarfilename = "dist/%s.tar.gz" % rootname

    if not os.path.exists('dist'):
        os.makedirs('dist')
    if os.path.exists(tarfilename):
        os.remove(tarfilename)
        
    msg("Archiving Phoenix documentation...")
    tarball = tarfile.open(name=tarfilename, mode="w:gz")
    tarball.add('docs/html', os.path.join(rootname, 'docs/html'), 
                filter=lambda info: None if '.svn' in info.name else info)    
    tarball.close()
    
    if options.upload_package:
        uploadPackage(tarfilename, '-docs')    
    
    msg('Documentation tarball built at %s' % tarfilename)
    
    
def cmd_sip(options, args):
    cmdTimer = CommandTimer('sip')
    cfg = Config()
    pwd = pushDir(cfg.ROOT_DIR)
    modules = glob.glob(opj(cfg.SIPGEN, '_*.sip'))
    # move _core the to the front of the list
    core_file = opj(cfg.SIPGEN, '_core.sip')
    if core_file in modules:
        modules.remove(core_file)
        modules.insert(0, core_file)
    
    for src_name in modules:
        tmpdir = tempfile.mkdtemp()
        tmpdir = tmpdir.replace('\\', '/')
        src_name = src_name.replace('\\', '/')
        base = os.path.basename(os.path.splitext(src_name)[0])
        sbf = posixjoin(cfg.SIPOUT, base) + '.sbf'
        pycode = base[1:] # remove the leading _
        pycode = posixjoin(cfg.PKGDIR, pycode) + '.py'
        
        # Check if any of the included files are newer than the .sbf file
        # produced by the previous run of sip. If not then we don't need to
        # run sip again.
        etg = loadETG(posixjoin('etg', base + '.py'))
        sipFiles = getSipFiles(etg.INCLUDES) + [opj(cfg.SIPGEN, base+'.sip')]
        if not newer_group(sipFiles, sbf) and os.path.exists(pycode):
            continue
        
        pycode = '-X pycode'+base+':'+pycode        
        sip = getSipCmd()
        cmd = '%s %s -c %s -b %s %s %s'  % \
            (sip, cfg.SIPOPTS, tmpdir, sbf, pycode, src_name)
        runcmd(cmd)

                
        def processSrc(src, keepHashLines=False):
            with textfile_open(src, 'rt') as f:
                srcTxt = f.read()
                if keepHashLines:
                    # Either just fix the pathnames in the #line lines...
                    srcTxt = srcTxt.replace(tmpdir, cfg.SIPOUT)
                else:
                    # ...or totally remove them by replacing those lines with ''
                    import re
                    srcTxt = re.sub(r'^#line.*\n', '', srcTxt, flags=re.MULTILINE)
            return srcTxt
        
        # Check each file in tmpdir to see if it is different than the same file
        # in cfg.SIPOUT. If so then copy the new one to cfg.SIPOUT, otherwise
        # ignore it.
        for src in glob.glob(tmpdir + '/*'):
            dest = opj(cfg.SIPOUT, os.path.basename(src))
            if not os.path.exists(dest):
                msg('%s is a new file, copying...' % os.path.basename(src))
                srcTxt = processSrc(src, options.keep_hash_lines)
                f = textfile_open(dest, 'wt')
                f.write(srcTxt)
                f.close()
                continue

            srcTxt = processSrc(src, options.keep_hash_lines)
            with textfile_open(dest, 'rt') as f:
                destTxt = f.read()
                
            if srcTxt == destTxt:
                pass
            else:
                msg('%s is changed, copying...' % os.path.basename(src))
                f = textfile_open(dest, 'wt')
                f.write(srcTxt)
                f.close()
                
        # Remove tmpdir and its contents
        shutil.rmtree(tmpdir)
    
    
    
def cmd_touch(options, args):
    cmdTimer = CommandTimer('touch')
    pwd = pushDir(phoenixDir())
    runcmd('touch etg/*.py')
    
    
def cmd_test(options, args):
    cmdTimer = CommandTimer('test')
    pwd = pushDir(phoenixDir())
    runcmd(PYTHON + ' unittests/runtests.py %s' % ('-v' if options.verbose else ''), fatal=False)

    
def testOne(name, options, args):
    cmdTimer = CommandTimer('test %s:' % name)
    pwd = pushDir(phoenixDir())
    runcmd(PYTHON + ' unittests/%s.py %s' % (name, '-v' if options.verbose else ''), fatal=False)
    
    
def cmd_build(options, args):
    cmdTimer = CommandTimer('build')
    cmd_build_wx(options, args)
    cmd_build_py(options, args)



def cmd_build_wx(options, args):
    cmdTimer = CommandTimer('build_wx')
    if not isWindows and options.use_syswx:
        msg("use_syswx option specified, skipping wxWidgets build")
        return 
    
    checkCompiler()
    
    build_options = ['--wxpython', '--unicode']

    if options.jobs:
        build_options.append('--jobs=%s' % options.jobs)

    if isWindows:
        # Windows-specific pre build stuff 
        if options.cairo:
            build_options.append('--cairo')
            if not os.environ.get("CAIRO_ROOT"):
                msg("WARNING: Expected CAIRO_ROOT set in the environment!")

        if options.jom:
            build_options.append('--jom')

    else:  
        # Platform is something other than MSW
        if options.osx_carbon:
            options.osx_cocoa = False
        
        BUILD_DIR = getBuildDir(options)
        DESTDIR = options.destdir
        PREFIX = options.prefix
        if options.mac_framework and isDarwin:
            # TODO:  Don't hard-code this path
            PREFIX = "/Library/Frameworks/wx.framework/Versions/%s" %  version2
        if PREFIX:
            build_options.append('--prefix=%s' % PREFIX)
            
        if not os.path.exists(BUILD_DIR):
            os.makedirs(BUILD_DIR)
        if  options.mac_arch: 
            build_options.append("--mac_universal_binary=%s" % options.mac_arch)

        if options.no_config:
            build_options.append('--no_config')
        elif not options.force_config:
            dependencies = [ os.path.join(wxDir(), 'Makefile.in'),
                             os.path.join(wxDir(), 'configure'),
                             os.path.join(wxDir(), 'setup.h.in'),
                             os.path.join(wxDir(), 'version-script.in'),
                             os.path.join(wxDir(), 'wx-config.in'),
                             ]
            for dep in dependencies:
                if newer(dep, os.path.join(BUILD_DIR, "Makefile")):
                    break
            else:
                build_options.append("--no_config")
            
        if isDarwin and options.osx_cocoa:
            build_options.append("--osx_cocoa")
        
        #if options.install:
        #    build_options.append('--installdir=%s' % DESTDIR)
        #    build_options.append("--install")
        
        if options.mac_framework and isDarwin:
            build_options.append("--mac_framework")
                                
        # Change to what will be the wxWidgets build folder
        # (Note, this needs to be after any testing for file/path existance, etc.
        # because they may be specified as relative paths.)
        pwd = pushDir(BUILD_DIR)

    if options.debug or (isWindows and options.both):
        build_options.append('--debug')
    
    if options.extra_make:
        build_options.append('--extra_make="%s"' % options.extra_make)
                    
    try:
        # Import and run the wxWidgets build script
        wxscript = os.path.join(wxDir(), "build/tools/build-wxwidgets.py")
        sys.path.insert(0, os.path.dirname(wxscript))
        wxbuild = __import__('build-wxwidgets')

        print('wxWidgets build options: ' + str(build_options))
        wxbuild.main(wxscript, build_options)
        
        # build again without the --debug flag?
        if isWindows and options.both:
            build_options.remove('--debug')
            print('wxWidgets build options: ' + str(build_options))
            wxbuild.main(wxscript, build_options)
            
    except:
        print("ERROR: failed building wxWidgets")
        import traceback
        traceback.print_exc()
        sys.exit(1)
        
    # Build the wx message catalogs, but first check that there is a msgfmt
    # command available
    if findCmd('msgfmt'):
        locale_pwd = pushDir(posixjoin(wxDir(), 'locale'))
        print('Building message catalogs in ' + os.getcwd())
        runcmd('make allmo')
        del locale_pwd
    else:
        print("WARNING: msgfmt command not found, message catalogs not rebulit.\n"
              "         Please install gettext and associated tools.")
        

    
def copyWxDlls(options):
    if options.no_magic or options.use_syswx:
        return 
    
    if isWindows:
        # Copy the wxWidgets DLLs to the wxPython pacakge folder
        msw = getMSWSettings(options)
        cfg = Config()

        ver = version3_nodot if unstable_series else version2_nodot
        dlls = list()
        if not options.debug or options.both:
            dlls += glob.glob(os.path.join(msw.dllDir, "wx*%su_*.dll" % ver))
        if options.debug or options.both:
            dlls += glob.glob(os.path.join(msw.dllDir, "wx*%sud_*.dll" % ver))
            dlls += glob.glob(os.path.join(msw.dllDir, "wx*%sud_*.pdb" % ver))

        # Also copy the cairo DLLs if needed
        if options.cairo:
            dlls += glob.glob(os.path.join(os.environ['CAIRO_ROOT'], 'bin', '*.dll'))

        for dll in dlls:
            copyIfNewer(dll, posixjoin(phoenixDir(), cfg.PKGDIR, os.path.basename(dll)), verbose=True)

    elif isDarwin:
        # Copy the wxWidgets dylibs
        cfg = Config()        
        wxlibdir = os.path.join(getBuildDir(options), "lib") 
        dlls = glob.glob(wxlibdir + '/*.dylib')
        for dll in dlls:
            copyIfNewer(dll, posixjoin(phoenixDir(), cfg.PKGDIR, os.path.basename(dll)), verbose=True)
                         
        # Now use install_name_tool to change the extension modules to look
        # in the same folder for the wx libs, instead of the build dir. Also
        # change the wx libs the same way.
        macSetLoaderNames(glob.glob(opj(phoenixDir(), cfg.PKGDIR, '*.so')) + 
                     glob.glob(opj(phoenixDir(), cfg.PKGDIR, '*.dylib')))
                
    else:
        # Not Windows and not OSX.  For now that means that we'll assume it's wxGTK.
        cfg = Config()        
        wxlibdir = os.path.join(getBuildDir(options), "lib") 
        dlls = glob.glob(wxlibdir + '/libwx_*.so')
        dlls += glob.glob(wxlibdir + '/libwx_*.so.[0-9]*')
        for dll in dlls:
            copyIfNewer(dll, posixjoin(phoenixDir(), cfg.PKGDIR, os.path.basename(dll)), verbose=True)
    
        # If all went well the wxPython extensions should already be looking
        # for the wxlib's in $ORIGIN, so there is nothing else to do here



# just an alias for build_py now
def cmd_waf_py(options, args):
    cmdTimer = CommandTimer('waf_py')
    cmd_build_py(options, args)
    


def cmd_build_py(options, args):
    cmdTimer = CommandTimer('build_py')
    waf = getWafCmd()
    checkCompiler()

    BUILD_DIR = getBuildDir(options)

    if not isWindows:
        WX_CONFIG = posixjoin(BUILD_DIR, 'wx-config')
        if options.use_syswx:
            wxcfg = posixjoin(options.prefix, 'bin', 'wx-config')
            if options.prefix and os.path.exists(wxcfg):
                WX_CONFIG = wxcfg
            else:
                WX_CONFIG = 'wx-config' # hope it is on the PATH
                
            
    wafBuildBase = wafBuildDir  = getWafBuildBase()
    if isWindows:
        wafBuildDir = posixjoin(wafBuildBase, 'release')
        
    build_options = list()
    if options.verbose:
        build_options.append('--verbose')
    
    if options.debug or (isWindows and options.both):
        build_options.append("--debug")
        if isWindows:
            wafBuildDir = posixjoin(wafBuildBase, 'debug')
    if isDarwin and options.mac_arch: 
        build_options.append("--mac_arch=%s" % options.mac_arch)
    if isWindows:
        if PYTHON_ARCH == '64bit':
            build_options.append('--msvc_arch=x64')
        else:
            build_options.append('--msvc_arch=x86')
    if not isWindows:
        build_options.append('--wx_config=%s' % WX_CONFIG)
    if options.verbose:
        build_options.append('--verbose')
    if options.jobs:
        build_options.append('--jobs=%s' % options.jobs)

    build_options.append('--python=%s' % PYTHON)
    build_options.append('--out=%s' % wafBuildDir)
        
    if not isWindows and not isDarwin and not options.no_magic and not options.use_syswx:
        # Using $ORIGIN in the rpath will cause the dynamic linker to look
        # for shared libraries in a folder relative to the loading binary's
        # location. Here we'll use just $ORIGIN so it should look in the same
        # folder as the wxPython extension modules.
        os.environ['LD_RUN_PATH'] = '$ORIGIN'
        
    # Run waf to perform the builds
    pwd = pushDir(phoenixDir())
    cmd = '%s %s %s configure build %s' % (PYTHON, waf, ' '.join(build_options), options.extra_waf)
    runcmd(cmd)

    if isWindows and options.both:
        build_options.remove('--debug')
        del build_options[-1]
        wafBuildDir = posixjoin(wafBuildBase, 'release')
        build_options.append('--out=%s' % wafBuildDir)
        cmd = '%s %s %s configure build %s' % (PYTHON, waf, ' '.join(build_options), options.extra_waf)
        runcmd(cmd)

    copyWxDlls(options)
    
    print("\n------------ BUILD FINISHED ------------")
    print("To use wxPython from the build folder (without installing):")
    print(" - Set your PYTHONPATH variable to %s." % phoenixDir())
    if not isWindows:
        print(" - You may also need to set your (DY)LD_LIBRARY_PATH to %s/lib, or wherever the wxWidgets libs have been installed." % BUILD_DIR)
    #print(" - Run python demo/demo.py")
    print("")



def cmd_install(options, args):
    cmdTimer = CommandTimer('install')
    cmd_install_wx(options, args)
    cmd_install_py(options, args)
    
    
def cmd_install_wx(options, args):
    cmdTimer = CommandTimer('install_wx')
    if isWindows:
        msg('No wxWidgets installation required on Windows')
        return
    
    if options.use_syswx:
        msg("use_syswx option specified, skipping wxWidgets install")
        return     
    
    if not options.no_magic:
        msg('Magic is in use, wxWidgets will be installed with wxPython')
        return 
    
    # Otherwise, run 'make install' in the wx build folder
    BUILD_DIR = getBuildDir(options)
    DESTDIR = '' if not options.destdir else 'DESTDIR=' + options.destdir
    pwd = pushDir(BUILD_DIR)
    runcmd("make install %s %s" % (DESTDIR, options.extra_make))
        


def cmd_install_py(options, args):
    cmdTimer = CommandTimer('install_py')
    DESTDIR = '' if not options.destdir else '--root=' + options.destdir
    VERBOSE = '--verbose' if options.verbose else ''
    cmd = "%s setup.py install --skip-build  %s %s %s" % (
        PYTHON, DESTDIR, VERBOSE, options.extra_setup)
    runcmd(cmd)

  
def _doSimpleSetupCmd(options, args, setupCmd):
    cmdTimer = CommandTimer(setupCmd)
    VERBOSE = '--verbose' if options.verbose else ''
    cmd = "%s setup.py %s --skip-build  %s %s" % (PYTHON, setupCmd, VERBOSE, options.extra_setup)
    runcmd(cmd)
     

def cmd_bdist_egg(options, args):
    _doSimpleSetupCmd(options, args, 'bdist_egg')
    
def cmd_bdist_wininst(options, args):
    _doSimpleSetupCmd(options, args, 'bdist_wininst')

# bdist_msi requires the version number to be only 3 components, but we're
# using 4.  TODO: Can we fix this?
#def cmd_bdist_msi(options, args):
#    _doSimpleSetupCmd(options, args, 'bdist_msi')


def cmd_egg_info(options, args, egg_base=None):
    cmdTimer = CommandTimer('egg_info')
    VERBOSE = '--verbose' if options.verbose else ''
    BASE = '--egg-base '+egg_base if egg_base is not None else ''
    cmd = "%s setup.py egg_info %s %s" % (PYTHON, VERBOSE, BASE)
    runcmd(cmd)



    

def cmd_clean_wx(options, args):
    cmdTimer = CommandTimer('clean_wx')
    if isWindows:
        if options.both:
            options.debug = True
        msw = getMSWSettings(options)
        cfg = Config()  
        deleteIfExists(opj(msw.dllDir, 'msw'+msw.dll_type))
        delFiles(glob.glob(opj(msw.dllDir, 'wx*%s%s*' % (version2_nodot, msw.dll_type))))
        delFiles(glob.glob(opj(msw.dllDir, 'wx*%s%s*' % (version3_nodot, msw.dll_type))))  
        if PYTHON_ARCH == '64bit':
            deleteIfExists(opj(msw.buildDir, 'vc%s_msw%sdll_x64' % (getVisCVersion(), msw.dll_type)))
        else:
            deleteIfExists(opj(msw.buildDir, 'vc%s_msw%sdll' % (getVisCVersion(), msw.dll_type)))
        
        if options.both:
            options.debug = False
            options.both = False
            cmd_clean_wx(options, args)
            options.both = True
    else:
        BUILD_DIR = getBuildDir(options)
        deleteIfExists(BUILD_DIR)
    

def cmd_clean_py(options, args):
    cmdTimer = CommandTimer('clean_py')
    assert os.getcwd() == phoenixDir()
    if isWindows and options.both:
        options.debug = True
    cfg = Config()
    deleteIfExists(getWafBuildBase())
    files = list()
    for wc in ['*.py', '*.pyc', '*.so', '*.dylib', '*.pyd', '*.pdb', '*.pi']:
        files += glob.glob(opj(cfg.PKGDIR, wc))
    if isWindows:
        msw = getMSWSettings(options)
        for wc in [ 'wx*' + version2_nodot + msw.dll_type + '*.dll',
                    'wx*' + version3_nodot + msw.dll_type + '*.dll']:
            files += glob.glob(opj(cfg.PKGDIR, wc))            
    delFiles(files)

    if options.both:
        options.debug = False
        options.both = False
        cmd_clean_py(options, args)
        options.both = True


    
def cmd_clean_sphinx(options, args):
    cmdTimer = CommandTimer('clean_sphinx')
    assert os.getcwd() == phoenixDir()

    sphinxDir = opj(phoenixDir(), 'docs', 'sphinx')
         
    globs = [ opj(sphinxDir, '*.txt'),
              opj(sphinxDir, '*.inc'),
              opj(sphinxDir, '*.pkl'),
              opj(sphinxDir, '*.lst'),
              opj(sphinxDir, '_templates/gallery.html'),
              opj(sphinxDir, 'rest_substitutions/snippets/python/*.py'),
              opj(sphinxDir, 'rest_substitutions/snippets/cpp/*.cpp'),
              opj(sphinxDir, '_static/images/inheritance/*.*'),
              ]
    for wc in globs:
        for f in glob.glob(wc):
            os.remove(f)

    dirs = [opj(sphinxDir, 'build'),
            opj(phoenixDir(), 'docs/html'),
            ]
    for d in dirs:
        if os.path.exists(d):
            shutil.rmtree(d)

        
def cmd_clean(options, args):
    cmd_clean_wx(options, args)
    cmd_clean_py(options, args)
    
    
def cmd_cleanall(options, args):
    # These take care of all the object, lib, shared lib files created by the
    # compilation part of build
    cmd_clean_wx(options, args)
    cmd_clean_py(options, args)
    
    # Clean all the intermediate and generated files from the sphinx command
    cmd_clean_sphinx(options, args)
    
    # Now also scrub out all of the SIP and C++ source files that are
    # generated by the Phoenix ETG system.
    cmdTimer = CommandTimer('cleanall')
    assert os.getcwd() == phoenixDir()
    files = list()
    for wc in ['sip/cpp/*.h', 'sip/cpp/*.cpp', 'sip/cpp/*.sbf', 'sip/gen/*.sip']:
        files += glob.glob(wc)
    delFiles(files)

    
def cmd_buildall(options, args):
    # (re)build everything
    cmd_build_wx(options, args)
    cmd_dox(options, args)
    cmd_touch(options, args)
    cmd_etg(options, args)
    cmd_sip(options, args)
    cmd_build_py(options, args)
    cmd_test(options, args)
    
    
def cmd_sdist(options, args):
    # Build a source tarball that includes the generated SIP and CPP files.
    cmdTimer = CommandTimer('sdist')
    assert os.getcwd() == phoenixDir()

    cfg = Config()

    isGit = os.path.exists('.git')
    isSvn = os.path.exists('.svn')
    if not isGit and not isSvn:
        msg("Sorry, I don't know what to do in this source tree, no git or svn workspace found.")
        return
            
    # make a tree for building up the archive files
    ADEST = 'build/sdist'
    PDEST = posixjoin(ADEST, 'Phoenix')
    WDEST = posixjoin(ADEST, 'wxWidgets')
    if not os.path.exists(PDEST):
        os.makedirs(PDEST)
    if not os.path.exists(WDEST):
        os.makedirs(WDEST)
    
    # and a place to put the final tarball
    if not os.path.exists('dist'):
        os.mkdir('dist')
    
    if isGit:        
        # pull out an archive copy of the repo files
        msg('Exporting Phoenix...')
        runcmd('git archive HEAD | tar -x -C %s' % PDEST, echoCmd=False)
        msg('Exporting wxWidgets...')
        runcmd('(cd %s; git archive HEAD) | tar -x -C %s' % (wxDir(), WDEST), echoCmd=False)
    elif isSvn:
        msg('Exporting Phoenix...')
        runcmd('svn export --force . %s' % PDEST, echoCmd=False)
        msg('Exporting wxWidgets...')
        runcmd('(cd %s; svn export --force . %s)' % (wxDir(), os.path.abspath(WDEST)), echoCmd=False)
        
        
    # copy Phoenix's generated code into the archive tree
    msg('Copying generated files...')
    for srcdir in ['cpp', 'gen']:
        destdir = posixjoin(PDEST, 'sip', srcdir)
        for name in glob.glob(posixjoin('sip', srcdir, '*')):
            copyFile(name, destdir)
    for wc in ['*.py', '*.pi']:
        destdir = posixjoin(PDEST, 'wx')
        for name in glob.glob(posixjoin('wx', wc)):
            copyFile(name, destdir)

    # Also add the waf executable
    copyFile('bin/waf-%s' % wafCurrentVersion, os.path.join(PDEST, 'bin'))

    # Add some extra stuff to the root folder
    copyFile('packaging/setup.py', ADEST)
    copyFile('packaging/README-sdist.txt', opj(ADEST, 'README.txt'))
    cmd_egg_info(options, args, egg_base=ADEST)
    copyFile(opj(ADEST, 'wxPython_Phoenix.egg-info/PKG-INFO'),
             opj(ADEST, 'PKG-INFO'))
            
    # build the tarball
    msg('Archiving Phoenix source...')
    rootname = "%s-%s-src" % (baseName, cfg.VERSION)
    tarfilename = "dist/%s.tar.gz" % rootname
    if os.path.exists(tarfilename):
        os.remove(tarfilename)
    tarball = tarfile.open(name=tarfilename, mode="w:gz")
    pwd = pushDir(ADEST)
    for name in glob.glob('*'):
        tarball.add(name, os.path.join(rootname, name)) 
    tarball.close()
    msg('Cleaning up...')
    del pwd
    shutil.rmtree(ADEST)

    if options.upload_package:
        uploadPackage(tarfilename, '-src')
    
    msg("Source release built at %s" % tarfilename)



def cmd_bdist(options, args):
    # Build a tarball and/or installer that includes all the files needed at
    # runtime for the current platform and the current version of Python.
    cmdTimer = CommandTimer('bdist')
    assert os.getcwd() == phoenixDir()

    cmd_egg_info(options, args)
    cfg = Config()

    dllext = ".so"
    wxlibdir = os.path.join(getBuildDir(options), "lib") 
    if sys.platform.startswith('darwin'):
        dllext = ".dylib"
     
    platform = sys.platform
    if isWindows and PYTHON_ARCH == '64bit':
        platform = 'win64'
    rootname = "%s-%s-%s-py%s" % (baseName, cfg.VERSION, platform, PYVER)
    tarfilename = "dist/%s.tar.gz" % rootname

    if not os.path.exists('dist'):
        os.makedirs('dist')
    
    if os.path.exists(tarfilename):
        os.remove(tarfilename)
    msg("Archiving Phoenix binaries...")
    tarball = tarfile.open(name=tarfilename, mode="w:gz")
    tarball.add('wx', opj(rootname, 'wx'), 
                filter=lambda info: None if '.svn' in info.name \
                                            or info.name.endswith('.pyc') \
                                            or '__pycache__' in info.name else info)
    tarball.add(eggInfoName, opj(rootname, eggInfoName)) 
    
    if not isDarwin and not isWindows and not options.no_magic and not options.use_syswx:
        # If the DLLs are not already in the wx package folder then go fetch
        # them now.
        msg("Archiving wxWidgets shared libraries...")
        dlls = glob.glob(os.path.join(wxlibdir, "*%s" % dllext))
        for dll in dlls:
            tarball.add(dll, os.path.join(rootname, 'wx', os.path.basename(dll)))

    tarball.add('packaging/README-bdist.txt', os.path.join(rootname, 'README.txt'))
    tarball.close()

    if options.upload_package:
        uploadPackage(tarfilename, '-%s-py%s' % (platform, PYVER))
                
    msg("Binary release built at %s" % tarfilename)


    
def cmd_setrev(options, args):
    # Grab the current SVN revision number (if possible) and write it to a
    # file we'll use later for building the package version number
    cmdTimer = CommandTimer('setrev')
    assert os.getcwd() == phoenixDir()

    svnrev = getSvnRev()
    f = open('REV.txt', 'w')
    f.write(svnrev)
    f.close()
    msg('REV.txt set to "%s"' % svnrev)    
        
    

#---------------------------------------------------------------------------

if __name__ == '__main__':
    main(sys.argv[1:]) 
