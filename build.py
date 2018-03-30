#!/usr/bin/python
#----------------------------------------------------------------------
# Name:        build.py
# Purpose:     Master build controller script.
#              This script is used to run through the commands used for the
#              various stages of building Phoenix, and can also be a front-end
#              for building wxWidgets and the wxPython distribution files.
#
# Author:      Robin Dunn
#
# Created:     3-Dec-2010
# Copyright:   (c) 2010-2017 by Total Control Software
# License:     wxWindows License
#----------------------------------------------------------------------

from __future__ import absolute_import

import sys
import glob
import hashlib
import optparse
import os
import re
import shutil
import subprocess
import tarfile
import tempfile
import datetime

from distutils.dep_util import newer, newer_group
from buildtools.config  import Config, msg, opj, posixjoin, loadETG, etg2sip, findCmd, \
                               phoenixDir, wxDir, copyIfNewer, copyFile, \
                               macSetLoaderNames, \
                               getVcsRev, runcmd, textfile_open, getSipFiles, \
                               getVisCVersion, getToolsPlatformName, updateLicenseFiles

import buildtools.version as version


# which version of Python is running this script
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


# defaults
PYVER = '2.7'
PYSHORTVER = '27'
PYTHON = None  # it will be set later
PYTHON_ARCH = 'UNKNOWN'

# convenience access to the wxPython version digits
version2 = "%d.%d" % (version.VER_MAJOR, version.VER_MINOR)
version3 = "%d.%d.%d" % (version.VER_MAJOR, version.VER_MINOR, version.VER_RELEASE)
version2_nodot = version2.replace(".", "")
version3_nodot = version3.replace(".", "")

# same for the wxWidgets version
wxversion2 = "%d.%d" % (version.wxVER_MAJOR, version.wxVER_MINOR)
wxversion3 = "%d.%d.%d" % (version.wxVER_MAJOR, version.wxVER_MINOR, version.wxVER_RELEASE)
wxversion2_nodot = wxversion2.replace(".", "")
wxversion3_nodot = wxversion3.replace(".", "")

unstable_series = (version.wxVER_MINOR % 2) == 1  # is the minor version odd or even?

isWindows = sys.platform.startswith('win')
isDarwin = sys.platform == "darwin"
devMode = False

baseName = version.PROJECT_NAME
eggInfoName = baseName + '.egg-info'
defaultMask='%s-%s*' % (baseName, version.VER_MAJOR)

pyICON = 'docs/sphinx/_static/images/sphinxdocs/phoenix_title.png'
wxICON = 'docs/sphinx/_static/images/sphinxdocs/mondrian.png'

# Some tools will be downloaded for the builds. These are the versions and
# MD5s of the tool binaries currently in use.
sipCurrentVersion = '4.19.7'
sipMD5 = {
    'darwin'   : 'd30ca1ffb09c0dbb6326e99d012c55b8',
    'win32'    : 'dbb882f4f95b1a7419a436280407899c',
    'linux32'  : '56a763acdf7c0b5725b31a71a9a56160',
    'linux64'  : 'b349127a4d46452936e4181d96b12c2d',
}

wafCurrentVersion = '1.7.15-p1'
wafMD5 = 'e44003373c965f4221bbdc4c9b846128'

doxygenCurrentVersion = '1.8.8'
doxygenMD5 = {
    'darwin' : '71c590e6cab47100f23919a2696cc7fd',
    'win32'  : 'a3dcff227458e423c132f16f57e26510',
    'linux'  : '083b3d8f614b538696041c7364e0f334',
}

# And the location where they can be downloaded from
toolsURL = 'https://wxpython.org/Phoenix/tools'


#---------------------------------------------------------------------------

def usage():
    print ("""\
Usage: ./build.py [command(s)] [options]

  Commands:
      N.N NN        Major.Minor version number of the Python to use to run
                    the other commands.  Default is 2.7.  Or you can use
                    --python to specify the actual Python executable to use.

      dox           Run Doxygen to produce the XML file used by ETG scripts
      doxhtml       Run Doxygen to create the HTML documentation for wx
      touch         'touch' the etg files so they will all get run the next
                    time the etg command is run.
      etg           Run the ETG scripts that are out of date to update their
                    SIP files and their Sphinx input files
      sip           Run sip to generate the C++ wrapper source

      wxlib         Build the Sphinx input files for wx.lib
      wxpy          Build the Sphinx input files for wx.py
      wxtools       Build the Sphinx input files for wx.tools
      sphinx        Run the documentation building process using Sphinx

      docset        Build Dash or Zeal compatible docsets

      build         Build both wxWidgets and wxPython
      build_wx      Do only the wxWidgets part of the build
      build_py      Build wxPython only

      install       Install both wxWidgets and wxPython
      install_wx    Install wxWidgets (but only if this tool was used to
                    build it)
      install_py    Install wxPython only

      sdist         Build a tarball containing all source files
      sdist_demo    Build a tarball containing just the demo and samples folders
      bdist         Create a binary tarball release of wxPython Phoenix
      bdist_docs    Build a tarball containing the documentation
      bdist_egg     Build a Python egg.  Requires magic.
      bdist_wheel   Build a Python wheel.  Requires magic.

      test          Run the unit test suite
      test_*        Run just the one named test module

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

    wxpydir = os.path.join(phoenixDir(), "wx")
    if not os.path.exists(wxpydir):
        os.makedirs(wxpydir)

    if not havePyVer ^ havePyPath or 'help' in args or '--help' in args or '-h' in args:
        usage()
        sys.exit(1)

    options, commands = parseArgs(args)

    cfg = Config(noWxConfig=True)
    msg('cfg.VERSION: %s' % cfg.VERSION)
    msg('')

    # For collecting test names or files, to be run after all have been pulled
    # off the command line
    test_names = []

    while commands:
        # ensure that each command starts with the CWD being the phoenix dir.
        os.chdir(phoenixDir())
        cmd = commands.pop(0)
        if not cmd:
            continue # ignore empty command-line args (possible with the buildbot)
        elif cmd.startswith('test_'):
            test_names.append('unittests/%s.py' % cmd)
        elif cmd.startswith('unittests/test_'):
            test_names.append(cmd)
        elif 'cmd_'+cmd in globals():
            function = globals()['cmd_'+cmd]
            function(options, args)
        else:
            print('*** Unknown command: ' + cmd)
            usage()
            sys.exit(1)

    # Now run the collected tests names, if any
    if test_names:
        cmd_test(options, args, test_names)

    msg("Done!")


#---------------------------------------------------------------------------
# Helper functions  (see also buildtools.config for more)
#---------------------------------------------------------------------------


def setPythonVersion(args):
    global PYVER
    global PYSHORTVER
    global PYTHON
    global PYTHON_ARCH
    global havePyVer
    global havePyPath

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
            PYVER = runcmd([PYTHON, '-c', 'import sys; print(sys.version[:3])'],
                           getOutput=True, echoCmd=False)
            PYSHORTVER = PYVER[0] + PYVER[2]
            break

    if havePyVer:
        if isWindows and os.environ.get('TOOLS'):
            # Use $TOOLS to find the correct Python. If set then it should be
            # the install root of all Python's on the system, with the 64-bit
            # ones in an amd64 subfolder, like this:
            #
            # $TOOLS\Python27\python.exe
            # $TOOLS\Python33\python.exe
            # $TOOLS\amd64\Python27\python.exe
            # $TOOLS\amd64\Python33\python.exe
            #
            TOOLS = os.environ.get('TOOLS')
            if 'cygdrive' in TOOLS:
                TOOLS = runcmd(getCygwinPath()+'/bin/cygpath -w '+TOOLS, True, False)
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
    msg('Will build using: "%s"' % PYTHON)

    msg(runcmd([PYTHON, '-c', 'import sys; print(sys.version)'], True, False))
    PYTHON_ARCH = runcmd(
        [PYTHON, '-c', 'import platform; print(platform.architecture()[0])'],
        True, False)

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
            '--jobs=6', #  % numCPUs(),

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
        global devMode
        devMode = True
        idx = args.index('--dev')
        # replace the --dev item with the items from the list
        args[idx:idx+1] = myDevModeOptions


def numCPUs():
    """
    Detects the number of CPUs on a system.
    This approach is from detectCPUs here:
    http://www.artima.com/weblogs/viewpost.jsp?thread=230001
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
        ncpus = int(os.environ["NUMBER_OF_PROCESSORS"])
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
        ("relwithdebug",   (False, "Turn on the generation of debug info for release builds on MSW.")),
        ("release",        (False, "Turn off some development options for a release build.")),
        ("keep_hash_lines",(False, "Don't remove the '#line N' lines from the SIP generated code")),
        ("gtk2",           (False, "On Linux build for gtk2 (default gtk3)")),
        ("gtk3",           (True,  "On Linux build for gtk3")),
        ("osx_cocoa",      (True,  "Build the OSX Cocoa port on Mac (default)")),
        ("osx_carbon",     (False, "Build the OSX Carbon port on Mac (unsupported)")),
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
                                   "installed wxWidgets, or allow this script to build and "
                                   "install wxWidgets independently of wxPython.")),

        ("build_dir",      ("",    "Directory to store wx build files. (Not used on Windows)")),
        ("prefix",         ("",    "Prefix value to pass to the wx build.")),
        ("destdir",        ("",    "Installation root for wxWidgets, files will go to {destdir}/{prefix}")),

        ("extra_setup",    ("",    "Extra args to pass on setup.py's command line.")),
        ("extra_make",     ("",    "Extra args to pass on [n]make's command line.")),
        ("extra_waf",      ("",    "Extra args to pass on waf's command line.")),
        ("extra_pytest",   ("",    "Extra args to pass on py.test's command line.")),

        (("j","jobs"),     ("",    "Number of parallel compile jobs to do, if supported.")),
        ("both",           (False, "Build both a debug and release version. (Only used on Windows)")),
        ("unicode",        (True,  "Build wxPython with unicode support (always on for wx2.9+)")),
        (("v", "verbose"), (False, "Print out more information during the build.")),
        ("nodoc",          (False, "Do not run the default docs generator")),
        ("upload",         (False, "Upload bdist and/or sdist packages to snapshot server.")),
        ("cairo",          (False, "Allow Cairo use with wxGraphicsContext (Windows only)")),
        ("x64",            (False, "Use and build for the 64bit version of Python on Windows")),
        ("jom",            (False, "Use jom instead of nmake for the wxMSW build")),
        ("pytest_timeout", ("0",   "Timeout, in seconds, for stopping stuck test cases. (Currently not working as expected, so disabled by default.)")),
        ("pytest_jobs",    ("",    "Number of parallel processes py.test should run")),
        ("vagrant_vms",    ("all", "Comma separated list of VM names to use for the build_vagrant command. Defaults to \"all\"")),
        ]

    parser = optparse.OptionParser("build options:")
    for opt, info in OPTS:
        default, txt = info
        action = 'store'
        if type(default) == bool:
            action = 'store_true'
        if isinstance(opt, str):
            opts = ('--'+opt, )
            dest = opt
        else:
            opts = ('-'+opt[0], '--'+opt[1])
            dest = opt[1]
        parser.add_option(*opts, default=default, action=action,
                          dest=dest, help=txt)
    return parser


def parseArgs(args):
    # If WXPYTHON_BUILD_ARGS is set in the environment, split it and add to args
    if os.environ.get('WXPYTHON_BUILD_ARGS', None):
        import shlex
        args += shlex.split(os.environ.get('WXPYTHON_BUILD_ARGS'))

    # Parse the args into options
    parser = makeOptionParser()
    options, args = parser.parse_args(args)

    if isWindows:
        # We always use magic on Windows
        options.no_magic = False
        options.use_syswx = False
    elif options.use_syswx:
        # Turn off magic if using the system wx
        options.no_magic = True

    # Some options don't make sense for release builds
    if options.release:
        options.debug = False
        options.both = False
        if os.path.exists('REV.txt'):
            os.unlink('REV.txt')

    if options.gtk2:
        options.gtk3 = False

    return options, args


class pushDir(object):
    def __init__(self, newDir):
        self.cwd = os.getcwd()
        os.chdir(newDir)

    def __del__(self):
        # pop back to the original dir
        os.chdir(self.cwd)


def getBuildDir(options):
    if not isDarwin and not isWindows:
        BUILD_DIR = opj(phoenixDir(), 'build', 'wxbld', 'gtk3' if options.gtk3 else 'gtk2')
    else:
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
        except Exception:
            if verbose:
                import traceback
                msg("Error: %s" % traceback.format_exc(1))

def delFiles(fileList, verbose=True):
    for afile in fileList:
        if verbose:
            print("Removing file: %s" % afile)
        os.remove(afile)


def getTool(cmdName, version, MD5, envVar, platformBinary, linuxBits=False):
    # Check in the bin dir for the specified version of the tool command. If
    # it's not there then attempt to download it. Validity of the binary is
    # checked with an MD5 hash.
    if os.environ.get(envVar):
        # Setting a value in the environment overrides other options
        return os.environ.get(envVar)
    else:
        # setup
        if platformBinary:
            platform = getToolsPlatformName(linuxBits)
            ext = ''
            if platform == 'win32':
                ext = '.exe'
            cmd = opj(phoenixDir(), 'bin', '%s-%s-%s%s' % (cmdName, version, platform, ext))
            md5 = MD5[platform]
        else:
            cmd = opj(phoenixDir(), 'bin', '%s-%s' % (cmdName, version))
            md5 = MD5


        def _error_msg(txt):
            msg('ERROR: ' + txt)
            msg('       Set %s in the environment to use a local build of %s instead' % (envVar, cmdName))


        msg('Checking for %s...' % cmd)
        if os.path.exists(cmd):
            # if the file exists run some verification checks on it

            # first make sure it is a normal file
            if not os.path.isfile(cmd):
                _error_msg('%s exists but is not a regular file.' % cmd)
                sys.exit(1)

            # now check the MD5 if not in dev mode and it's set to None
            if not (devMode and md5 is None):
                m = hashlib.md5()
                m.update(open(cmd, 'rb').read())
                if m.hexdigest() != md5:
                    _error_msg('MD5 mismatch, got "%s"\n       '
                               'expected          "%s"' % (m.hexdigest(), md5))
                    sys.exit(1)

            # If the cmd is a script run by some interpreter, or similar,
            # then we don't need to check anything else
            if not platformBinary:
                return cmd

            # Ensure that commands that are platform binaries are executable
            if not os.access(cmd, os.R_OK | os.X_OK):
                _error_msg('Cannot execute %s due to permissions error' % cmd)
                sys.exit(1)

            try:
                p = subprocess.Popen([cmd, '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ)
                p.wait()
            except OSError as e:
                _error_msg('Could not execute %s, got "%s"' % (cmd, e))
                sys.exit(1)

            # if we get this far then all is well, the cmd is good to go
            return cmd


        msg('Not found.  Attempting to download...')
        url = '%s/%s.bz2' % (toolsURL, os.path.basename(cmd))
        try:
            import requests
            resp = requests.get(url)
            resp.raise_for_status()
            msg('Connection successful...')
            data = resp.content
            msg('Data downloaded...')
        except Exception:
            _error_msg('Unable to download ' + url)
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
        return getTool(cmdName, version, MD5, envVar, platformBinary, linuxBits)



# The download and MD5 check only needs to happen once per run, cache the sip
# cmd value here the first time through.
_sipCmd = None
def getSipCmd():
    global _sipCmd
    if _sipCmd is None:
        _sipCmd = getTool('sip', sipCurrentVersion, sipMD5, 'SIP', True, True)
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


def uploadPackage(fileName, options, mask=defaultMask, keep=75):
    """
    Upload the given filename to the configured package server location. Only
    the `keep` most recent files matching `mask` will be kept so the server
    space is not overly consumed. It is assumed that if the files are in
    sorted order then the end of the list will be the newest files.
    """
    fileName = fileName.replace('\\', '/')
    msg("Uploading %s..." % fileName)

    # NOTE: It is expected that there will be a host entry defined in
    # ~/.ssh/config named wxpython-rbot, with the proper host, user, identity
    # file, etc. needed for making an SSH connection to the snapshots server.
    # Release builds work similarly with their own host configuration defined
    # in the ~/.ssh/config file.
    if options.release:
        host = 'wxpython-release'
        uploadDir = 'release-builds'
    else:
        host = 'wxpython-rbot'
        uploadDir = 'snapshot-builds'

    # copy the new file to the server
    cmd = 'scp {} {}:{}'.format(fileName, host, uploadDir)
    runcmd(cmd)

    # Make sure it is readable by all
    cmd = 'ssh {} "cd {}; chmod a+r {}"'.format(host, uploadDir, os.path.basename(fileName))
    runcmd(cmd)

    if not options.release:
        # get the list of all snapshot files on the server
        cmd = 'ssh {} "cd {}; ls {}"'.format(host, uploadDir, mask)
        allFiles = runcmd(cmd, getOutput=True)
        allFiles = allFiles.strip().split('\n')
        allFiles.sort()

        # Leave the last keep number of builds, including this new one, on the server.
        # Delete the rest.
        rmFiles = allFiles[:-keep]
        if rmFiles:
            msg("Deleting %s" % ", ".join(rmFiles))
            cmd = 'ssh {} "cd {}; rm {}"'.format(host, uploadDir, " ".join(rmFiles))
            runcmd(cmd)

    msg("Upload complete!")


def uploadTree(srcPath, destPath, options, days=30):
    """
    Similar to the above but uploads a tree of files.
    """
    msg("Uploading tree at {}...".format(srcPath))

    if options.release:
        host = 'wxpython-release'
        uploadDir = opj('release-builds', destPath)
    else:
        host = 'wxpython-rbot'
        uploadDir = opj('snapshot-builds', destPath)

    # Ensure the destination exists
    cmd = 'ssh {0} "if [ ! -d {1} ]; then mkdir -p {1}; fi"'.format(host, uploadDir)
    runcmd(cmd)

    # Upload the tree
    cmd = 'scp -r {} {}:{}'.format(srcPath, host, uploadDir)
    runcmd(cmd)

    # Make sure it is readable by all
    cmd = 'ssh {} "chmod -R a+r {}"'.format(host, uploadDir)
    runcmd(cmd)

    if not options.release:
        # Remove files that were last modified more than `days` days ago
        msg("Cleaning up old builds.")
        cmd = 'ssh {} "find {} -type f -mtime +{} -delete"'.format(host, uploadDir, days)
        runcmd(cmd)

    msg("Tree upload and cleanup complete!")


def checkCompiler(quiet=False):
    if isWindows:
        # Make sure that the compiler that Python wants to use can be found.
        # It will terminate if the compiler is not found or other exceptions
        # are raised.
        cmd = "import distutils.msvc9compiler as msvc; " \
              "mc = msvc.MSVCCompiler(); " \
              "mc.initialize(); " \
              "print(mc.cc)"
        CC = runcmd('"%s" -c "%s"' % (PYTHON, cmd), getOutput=True, echoCmd=False)
        if not quiet:
            msg("MSVC: %s" % CC)

        # Now get the environment variables which that compiler needs from
        # its vcvarsall.bat command and load them into this process's
        # environment.
        cmd = "import distutils.msvc9compiler as msvc; " \
              "arch = msvc.PLAT_TO_VCVARS[msvc.get_platform()]; " \
              "env = msvc.query_vcvarsall(msvc.VERSION, arch); " \
              "print(env)"
        env = eval(runcmd('"%s" -c "%s"' % (PYTHON, cmd), getOutput=True, echoCmd=False))

        def _b(v):
            return str(v)
            #if PY2:
            #    return bytes(v)
            #else:
            #    return bytes(v, 'utf8')

        os.environ['PATH'] = _b(env['path'])
        os.environ['INCLUDE'] = _b(env['include'])
        os.environ['LIB'] = _b(env['lib'])
        os.environ['LIBPATH'] = _b(env['libpath'])

    # NOTE: SIP is now generating code with scoped-enums. Older linux
    # platforms like what we're using for builds, and also TravisCI for
    # example, are using GCC versions that are still defaulting to C++98,
    # so this flag is needed to turn on the C++11 mode. If this flag
    # causes problems with other non-Windows, non-Darwin compilers then
    # we'll need to make this a little smarter about what flag (if any)
    # needs to be used.
    #
    # NOTE 2: SIP chenged its output such that this doesn't appear to be
    # needed anymore, but we'll leave the code in place to make it easy to
    # turn it back on again if/when needed.
    if False and not isWindows and not isDarwin:
        stdflag = '-std=c++11'
        curflags = os.environ.get('CXXFLAGS', '')
        if stdflag not in curflags:
            os.environ['CXXFLAGS'] = '{} {}'.format(stdflag, curflags)
    #print('**** Using CXXFLAGS:', os.environ.get('CXXFLAGS', ''))


def getWafBuildBase():
    base = posixjoin('build', 'waf', PYVER)
    if isWindows:
        if PYTHON_ARCH == '64bit':
            base = posixjoin(base, 'x64')
        else:
            base = posixjoin(base, 'x86')
    return base


def getCygwinPath():
    """
    Try to locate the path where cygwin is installed.

    If CYGWIN_BASE is set in the environment then use that. Otherwise look in
    default install locations.
    """
    if os.environ.get('CYGWIN_BASE'):
        return os.environ.get('CYGWIN_BASE')

    for path in ['c:/cygwin', 'c:/cygwin64']:
        if os.path.isdir(path):
            return path

    return None



#---------------------------------------------------------------------------
# Command functions and helpers
#---------------------------------------------------------------------------


def _doDox(arg):
    doxCmd = getDoxCmd()
    doxCmd = os.path.abspath(doxCmd)

    if isWindows:
        cygwin_path = getCygwinPath()
        doxCmd = doxCmd.replace('\\', '/')
        doxCmd = runcmd(cygwin_path+'/bin/cygpath -u '+doxCmd, True, False)
        os.environ['DOXYGEN'] = doxCmd
        os.environ['WX_SKIP_DOXYGEN_VERSION_CHECK'] = '1'
        d = posixjoin(wxDir(), 'docs/doxygen')
        d = d.replace('\\', '/')
        cmd = '%s/bin/bash.exe -l -c "cd %s && ./regen.sh %s"' % (cygwin_path, d, arg)
    else:
        os.environ['DOXYGEN'] = doxCmd
        os.environ['WX_SKIP_DOXYGEN_VERSION_CHECK'] = '1'
        pwd = pushDir(posixjoin(wxDir(), 'docs/doxygen'))
        cmd = 'bash ./regen.sh %s' % arg
    runcmd(cmd)


def cmd_dox(options, args):
    cmdTimer = CommandTimer('dox')
    _doDox('xml')


def cmd_doxhtml(options, args):
    cmdTimer = CommandTimer('doxhtml')
    _doDox('html')
    _doDox('chm')


# NOTE: Because of the use of defaults and plutil the following docset
# commands will only work correctly on OSX.
def cmd_docset_wx(options, args):
    cmdTimer = CommandTimer('docset_wx')
    cfg = Config()

    # Use Doxygen to generate the docset
    _doDox('docset')

    # Remove any existing docset in the dist dir and move the new docset in
    srcname = posixjoin(wxDir(), 'docs/doxygen/out/docset',
                        'wxWidgets-%s.docset' % wxversion2)
    destname = 'dist/wxWidgets-%s.docset' % wxversion3
    if not os.path.isdir(srcname):
        msg('ERROR: %s not found' % srcname)
        sys.exit(1)
    if os.path.isdir(destname):
        shutil.rmtree(destname)
    shutil.move(srcname, destname)
    shutil.copyfile(wxICON, posixjoin(destname, 'icon.png'))
    runcmd('plutil -convert xml1 {}/Contents/Info.plist'.format(destname))


def cmd_docset_py(options, args):
    cmdTimer = CommandTimer('docset_py')
    if not os.path.isdir('docs/html'):
        msg('ERROR: No docs/html, has the sphinx build command been run?')
        sys.exit(1)

    # clear out any old docset build
    name = 'wxPython-{}'.format(version3)
    docset = posixjoin('dist', '{}.docset'.format(name))
    if os.path.isdir(docset):
        shutil.rmtree(docset)

    # run the docset generator
    VERBOSE = '--verbose' if options.verbose else ''
    runcmd('doc2dash {} --name "{}" --icon {} --destination dist docs/html'
           .format(VERBOSE, name, pyICON))

    # update its Info.plist file
    docset = os.path.abspath(docset)
    runcmd('defaults write {}/Contents/Info isJavaScriptEnabled true'.format(docset))
    runcmd('defaults write {}/Contents/Info dashIndexFilePath index.html'.format(docset))
    runcmd('defaults write {}/Contents/Info DocSetPlatformFamily wxpy'.format(docset))
    runcmd('plutil -convert xml1 {}/Contents/Info.plist'.format(docset))


def cmd_docset(options, args):
    cmd_docset_wx(options, args)
    cmd_docset_py(options, args)



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
            runcmd('"%s" %s %s' % (PYTHON, script, flags))


def cmd_sphinx(options, args):
    from sphinxtools.postprocess import genIndexes, makeHeadings, postProcess, genGallery

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

    genIndexes(sphinxDir)
    genGallery()

    # Copy the hand-edited top level doc files too
    rstFiles = glob.glob(os.path.join(phoenixDir(), 'docs', '*.rst'))
    for rst in rstFiles:
        txt = os.path.join(sphinxDir, os.path.splitext(os.path.basename(rst))[0] + '.txt')
        copyIfNewer(rst, txt)

    makeHeadings()

    pwd2 = pushDir(sphinxDir)
    buildDir = os.path.join(sphinxDir, 'build')
    htmlDir = os.path.join(phoenixDir(), 'docs', 'html')
    runcmd('sphinx-build -b html -d %s/doctrees . %s' % (buildDir, htmlDir))
    del pwd2

    msg('Postprocessing sphinx output...')
    postProcess(htmlDir, options)


def cmd_wxlib(options, args):
    from sphinxtools.modulehunter import ModuleHunter

    cmdTimer = CommandTimer('wx.lib')
    pwd = pushDir(phoenixDir())

    for wx_pkg in ['lib', 'py', 'tools']:
        libDir = os.path.join(phoenixDir(), 'wx', wx_pkg)

        if not os.path.isdir(libDir):
            raise Exception('Missing wx.{} folder in the distribution'.format(wx_pkg))

        init_name = os.path.join(libDir, '__init__.py')
        import_name = 'wx.{}'.format(wx_pkg)

        ModuleHunter(init_name, import_name, version3)



def cmd_wxpy(options, args):
    msg('Command wxpy has been folded into command wxlib.')


def cmd_wxtools(options, args):
    msg('Command wxtools has been folded into command wxlib.')


def cmd_bdist_docs(options, args):
    cmdTimer = CommandTimer('bdist_docs')
    pwd = pushDir(phoenixDir())

    cfg = Config()

    msg("Archiving wxPython Phoenix documentation...")
    rootname = "%s-docs-%s" % (baseName, cfg.VERSION)
    tarfilename = "dist/%s.tar.gz" % rootname

    if not os.path.exists('dist'):
        os.makedirs('dist')
    if os.path.exists(tarfilename):
        os.remove(tarfilename)

    with tarfile.open(name=tarfilename, mode="w:gz") as tarball:
        tarball.add('docs/html', os.path.join(rootname, 'docs/html'),
                    filter=lambda info: None if '.svn' in info.name else info)

    if options.upload:
        uploadPackage(tarfilename, options, keep=5,
                      mask='%s-docs-%s*' % (baseName, cfg.VER_MAJOR))

    msg('Documentation tarball built at %s' % tarfilename)


    # # pythonhosted.org can host the wxPython documentation for us, so let's
    # # use it for the docs associated with the latest release of wxPython.  It
    # # requires that the docs be in a .zip file with an index.html file at the
    # # top level. To build this we'll just need to do like the above tarball
    # # code, except add the files from within the docs/html folder so they will
    # # all be at the top level of the archive.  shutil.make_archive can be used
    # # in this case because we don't need to rewrite the pathnames in the
    # # archive.
    # if options.release:
    #     msg("Archiving wxPython Phoenix documentation for pythonhosted.org...")
    #     rootname = "%s-docs-pythonhosted-%s" % (baseName, cfg.VERSION)
    #     zipfilename = "dist/%s.zip" % rootname
    #
    #     if os.path.exists(zipfilename):
    #         os.remove(zipfilename)
    #
    #     # with zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_DEFLATED) as zip:
    #     #     pwd2 = pushDir('docs/html')
    #
    #     zipfilename = shutil.make_archive(base_name=os.path.splitext(zipfilename)[0],
    #                                       format="zip",
    #                                       root_dir="docs/html")
    #     zipfilename = os.path.relpath(zipfilename)
    #     zipfilename = zipfilename.replace('\\', '/')
    #
    #     if options.upload:
    #         uploadPackage(zipfilename, options, keep=5,
    #                       mask='%s-docs-pythonhosted-%s*' % (baseName, cfg.VER_MAJOR))
    #
    #     msg('Pythonhosted zip file built at %s' % zipfilename)



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

        classesNeedingClassInfo = { 'sip_corewxTreeCtrl.cpp' : 'wxTreeCtrl', }

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
                className = classesNeedingClassInfo.get(os.path.basename(src))
                if className:
                    srcTxt = injectClassInfo(className, srcTxt)
            return srcTxt

        def injectClassInfo(className, srcTxt):
            # inject wxClassInfo macros into the sip generated wrapper class
            lines = srcTxt.splitlines()
            # find the beginning of the class declaration
            for idx, line in enumerate(lines):
                if line.startswith('class sip{}'.format(className)):
                    # next line is '{', insert after that
                    lines[idx+2:idx+2] = ['wxDECLARE_ABSTRACT_CLASS(sip{});'.format(className)]
                    break
            # find the '};' that terminates the class
            for idx, line in enumerate(lines[idx+2:], idx+2):
                if line.startswith('};'):
                    lines[idx+1:idx+1] = ['\nwxIMPLEMENT_ABSTRACT_CLASS(sip{0}, {0});'.format(className)]
                    break
            # join it back up and return
            return '\n'.join(lines)


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



def cmd_test(options, args, tests=None):
    # Run all tests
    cmdTimer = CommandTimer('test')
    pwd = pushDir(phoenixDir())

    # --boxed runs each test in a new process (only for posix *&##$#@$^!!)
    # -n is the number of processes to run in parallel
    # --timeout will kill the test process if it gets stuck
    jobs = '-n{}'.format(options.pytest_jobs) if options.pytest_jobs else ''
    boxed = '--boxed' if not isWindows else ''
    sec = options.pytest_timeout
    timeout = '--timeout={}'.format(sec) if sec and sec != "0" else ''
    cmd = '"{}" -m pytest {} {} {} {} {} '.format(
        PYTHON,
        '-v' if options.verbose else '',
        boxed,
        jobs,
        timeout,
        options.extra_pytest)

    if not tests:
        # let pytest find all tests in the unittest folder
        cmd += 'unittests'
    else:
        # otherwise, run only the test modules given
        cmd += ' '.join(tests)

    runcmd(cmd, fatal=False)



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
            cairo_root = os.path.join(phoenixDir(), 'packaging', 'cairo-msw')
            os.environ['CAIRO_ROOT'] = cairo_root

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
            PREFIX = "/Library/Frameworks/wx.framework/Versions/%s" %  wxversion2
        if PREFIX:
            build_options.append('--prefix=%s' % PREFIX)

        if not os.path.exists(BUILD_DIR):
            os.makedirs(BUILD_DIR)
        if  isDarwin and options.mac_arch:
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

        if not isDarwin:
            if options.gtk2:
                build_options.append('--gtk2')
            if options.gtk3:
                build_options.append('--gtk3')

        # Change to what will be the wxWidgets build folder
        # (Note, this needs to be after any testing for file/path existance, etc.
        # because they may be specified as relative paths.)
        pwd = pushDir(BUILD_DIR)

    if options.debug or (isWindows and options.both):
        build_options.append('--debug')

    if options.extra_make:
        build_options.append('--extra_make="%s"' % options.extra_make)

    if not isWindows and not isDarwin and not options.no_magic and not options.use_syswx:
        # Using $ORIGIN in the rpath will cause the dynamic linker to look
        # for shared libraries in a folder relative to the loading binary's
        # location. Here we'll use just $ORIGIN so it should look in the same
        # folder as the wxPython extension modules.
        os.environ['LD_RUN_PATH'] = '$ORIGIN'

    try:
        # Import and run the wxWidgets build script
        from buildtools import build_wxwidgets as wxbuild

        print('wxWidgets build options: ' + str(build_options))
        wxbuild.main(wxDir(), build_options)

        # build again without the --debug flag?
        if isWindows and options.both:
            build_options.remove('--debug')
            print('wxWidgets build options: ' + str(build_options))
            wxbuild.main(wxDir(), build_options)

    except Exception:
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
        # Copy the wxWidgets DLLs to the wxPython package folder
        msw = getMSWSettings(options)
        cfg = Config()

        ver = wxversion3_nodot if unstable_series else wxversion2_nodot
        arch = 'x64' if PYTHON_ARCH == '64bit' else 'x86'
        dlls = list()
        if not options.debug or options.both:
            dlls += glob.glob(os.path.join(msw.dllDir, "wx*%su_*.dll" % ver))
            if options.relwithdebug:
                dlls += glob.glob(os.path.join(msw.dllDir, "wx*%su_*.pdb" % ver))
        if options.debug or options.both:
            dlls += glob.glob(os.path.join(msw.dllDir, "wx*%sud_*.dll" % ver))
            dlls += glob.glob(os.path.join(msw.dllDir, "wx*%sud_*.pdb" % ver))

        # Also copy the cairo DLLs if needed
        if options.cairo:
            cairo_root = os.path.join(phoenixDir(), 'packaging', 'cairo-msw')
            dlls += glob.glob(os.path.join(cairo_root, arch, 'bin', '*.dll'))

        # For Python 3.5 and 3.6 builds we also need to copy some VC14 redist DLLs
        if PYVER in ['3.5', '3.6']:
            redist_dir = os.path.join(
                phoenixDir(), 'packaging', 'Py3.5', 'vcredist',
                arch, 'Microsoft.VC140.CRT', '*.dll')
            dlls += glob.glob(redist_dir)

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

    if options.release:
        os.environ['WXPYTHON_RELEASE'] = 'yes'

    if not isWindows:
        WX_CONFIG = posixjoin(BUILD_DIR, 'wx-config')
        if options.use_syswx:
            wxcfg = posixjoin(options.prefix, 'bin', 'wx-config')
            if options.prefix and os.path.exists(wxcfg):
                WX_CONFIG = wxcfg
            else:
                WX_CONFIG = 'wx-config' # hope it is on the PATH


    wafBuildBase = wafBuildDir = getWafBuildBase()
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
    if options.relwithdebug:
        build_options.append('--msvc_relwithdebug')
    if not isDarwin and not isWindows:
        if options.gtk2:
            build_options.append('--gtk2')
            wafBuildDir = posixjoin(wafBuildBase, 'gtk2')
        if options.gtk3:
            build_options.append('--gtk3')
            wafBuildDir = posixjoin(wafBuildBase, 'gtk3')

    build_options.append('--python="%s"' % PYTHON)
    build_options.append('--out=%s' % wafBuildDir) # this needs to be the last option

    if not isWindows and not isDarwin and not options.no_magic and not options.use_syswx:
        # Using $ORIGIN in the rpath will cause the dynamic linker to look
        # for shared libraries in a folder relative to the loading binary's
        # location. Here we'll use just $ORIGIN so it should look in the same
        # folder as the wxPython extension modules.
        os.environ['LD_RUN_PATH'] = '$ORIGIN'

    # Run waf to perform the builds
    pwd = pushDir(phoenixDir())
    cmd = '"%s" %s %s configure build %s' % (PYTHON, waf, ' '.join(build_options), options.extra_waf)
    runcmd(cmd)

    if isWindows and options.both:
        build_options.remove('--debug')
        del build_options[-1]
        wafBuildDir = posixjoin(wafBuildBase, 'release')
        build_options.append('--out=%s' % wafBuildDir)
        cmd = '"%s" %s %s configure build %s' % (PYTHON, waf, ' '.join(build_options), options.extra_waf)
        runcmd(cmd)

    copyWxDlls(options)

    cfg = Config()
    cfg.build_locale_dir(opj(cfg.PKGDIR, 'locale'))

    print("\n------------ BUILD FINISHED ------------")
    print("To use wxPython from the build folder (without installing):")
    print(" - Set your PYTHONPATH variable to %s." % phoenixDir())
    if not isWindows:
        print(" - You may also need to set your (DY)LD_LIBRARY_PATH to %s/lib,\n   or wherever the wxWidgets libs have been installed." % BUILD_DIR)
    print("")


def cmd_build_vagrant(options, args):
    # Does a build and bdist_wheel for each of the Vagrant based VMs defined
    # in {phoenixDir}/vagrant. Requires Vagrant and VirtualBox to be installed
    # and ready for use.  Also requires a source tarball to be present in
    # {phoenixDir}/dist, such as what is produced with cmd_sdist.
    cmdTimer = CommandTimer('bdist_vagrant')
    cfg = Config(noWxConfig=True)
    if not options.vagrant_vms or options.vagrant_vms == 'all':
        VMs = [ 'centos-7     all all',
                'debian-8     all all',
                'debian-9     all all',
                'fedora-23    all all',
                'fedora-26    all all',
                'fedora-27    all gtk3', # no webkitgtk for gtk2??
                'ubuntu-14.04 all all',
                'ubuntu-16.04 all all',
                ]
    elif options.vagrant_vms == 'none':
        VMs = [] # to skip building anything and just upload
    else:
        VMs = options.vagrant_vms.split(',')

    for vmName in VMs:
        vmDir = opj(phoenixDir(), 'vagrant', vmName.split()[0])
        pwd = pushDir(vmDir)
        msg('Starting Vagrant VM in {}'.format(vmDir))
        runcmd('vagrant up')
        runcmd('vagrant ssh -c "scripts/build.sh %s"' % vmName)
        runcmd('vagrant halt')
        del pwd

    if options.upload:
        for tag in ['gtk2', 'gtk3']:
            src = opj(phoenixDir(), 'dist', 'linux', tag)
            if os.path.isdir(src):
                uploadTree(src, 'linux', options)



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
    cmd = '"%s" setup.py install --skip-build  %s %s %s' % (
        PYTHON, DESTDIR, VERBOSE, options.extra_setup)
    runcmd(cmd)


def cmd_build_pdbzip(options, args):
    if isWindows and options.relwithdebug:
        cmdTimer = CommandTimer('build_pdbzip')

        if not os.path.exists('dist'):
            os.mkdir('dist')

        cfg = Config()
        filenames = glob.glob('./wx/*.pdb')
        if not filenames:
            msg('No PDB files found in ./wx!')
            return
        arch = 'win_amd64' if PYTHON_ARCH == '64bit' else 'win32'
        pyver = 'py{}'.format(PYSHORTVER)
        zipname = 'dist/{}-pdb-{}-{}-{}.zip'.format(baseName, cfg.VERSION, pyver, arch)
        from zipfile import ZipFile, ZIP_DEFLATED
        with ZipFile(zipname, 'w', ZIP_DEFLATED) as zip:
            for name in filenames:
                zip.write(name)
        msg('PDB zip file created at: {}'.format(zipname))

        for name in filenames:
            os.unlink(name)
        msg('PDB files removed from ./wx')
        return zipname


def _doSimpleSetupCmd(options, args, setupCmd):
    cmdTimer = CommandTimer(setupCmd)
    VERBOSE = '--verbose' if options.verbose else ''
    cmd = '"%s" setup.py %s --skip-build  %s %s' % (PYTHON, setupCmd, VERBOSE, options.extra_setup)
    runcmd(cmd)


def cmd_bdist_egg(options, args):
    pdbzip = cmd_build_pdbzip(options, args)
    _doSimpleSetupCmd(options, args, 'bdist_egg')
    cfg = Config()
    if options.upload:
        filemask = "dist/%s-%s-*.egg" % (baseName, cfg.VERSION)
        filenames = glob.glob(filemask)
        assert len(filenames) == 1, "Unknown files found:"+repr(filenames)
        uploadPackage(filenames[0], options)
        if pdbzip:
            uploadPackage(pdbzip, options, keep=24,
                          mask='%s-pdb-%s*' % (baseName, cfg.VER_MAJOR))

def cmd_bdist_wheel(options, args):
    pdbzip = cmd_build_pdbzip(options, args)
    _doSimpleSetupCmd(options, args, 'bdist_wheel')
    cfg = Config()
    if options.upload:
        filemask = "dist/%s-%s-*.whl" % (baseName, cfg.VERSION)
        filenames = glob.glob(filemask)
        assert len(filenames) == 1, "Unknown files found:"+repr(filenames)
        uploadPackage(filenames[0], options)
        if pdbzip:
            uploadPackage(pdbzip, options, keep=24,
                          mask='%s-pdb-%s*' % (baseName, cfg.VER_MAJOR))


def cmd_bdist_wininst(options, args):
    pdbzip = cmd_build_pdbzip(options, args)
    _doSimpleSetupCmd(options, args, 'bdist_wininst')
    cfg = Config()
    if options.upload:
        filemask = "dist/%s-%s-*.exe" % (baseName, cfg.VERSION)
        filenames = glob.glob(filemask)
        assert len(filenames) == 1, "Unknown files found:"+repr(filenames)
        uploadPackage(filenames[0], options)
        if pdbzip:
            uploadPackage(pdbzip, options, keep=24,
                          mask='%s-pdb-%s*' % (baseName, cfg.VER_MAJOR))


def cmd_bdist_msi(options, args):
    cmd_build_pdbzip(options, args)
    _doSimpleSetupCmd(options, args, 'bdist_msi')


def cmd_egg_info(options, args, egg_base=None):
    cmdTimer = CommandTimer('egg_info')
    VERBOSE = '--verbose' if options.verbose else ''
    BASE = '--egg-base '+egg_base if egg_base is not None else ''
    cmd = '"%s" setup.py egg_info %s %s' % (PYTHON, VERBOSE, BASE)
    runcmd(cmd)


def cmd_clean_wx(options, args):
    cmdTimer = CommandTimer('clean_wx')
    if isWindows:
        if options.both:
            options.debug = True
        msw = getMSWSettings(options)
        deleteIfExists(opj(msw.dllDir, 'msw'+msw.dll_type))
        delFiles(glob.glob(opj(msw.dllDir, 'wx*%s%s*' % (wxversion2_nodot, msw.dll_type))))
        delFiles(glob.glob(opj(msw.dllDir, 'wx*%s%s*' % (wxversion3_nodot, msw.dll_type))))
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
    for wc in ['*.py', '*.pyc', '*.so', '*.dylib', '*.pyd', '*.pdb', '*.pi', '*.pyi']:
        files += glob.glob(opj(cfg.PKGDIR, wc))
    if isWindows:
        msw = getMSWSettings(options)
        for wc in [ 'wx*' + wxversion2_nodot + msw.dll_type + '*.dll',
                    'wx*' + wxversion3_nodot + msw.dll_type + '*.dll']:
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
              opj(sphinxDir, '*.rst'),
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


def cmd_clean_vagrant(options, args):
    cmdTimer = CommandTimer('clean_vagrant')
    assert os.getcwd() == phoenixDir()

    d = opj(phoenixDir(), 'dist', 'linux')
    if os.path.exists(d):
        shutil.rmtree(d)

def cmd_clean_all(options, args):
    cmd_cleanall(options, args)

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

    cmd_clean_vagrant(options, args)


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
    if not isGit:
        msg("Sorry, I don't know what to do in this source tree, no git workspace found.")
        return

    # make a tree for building up the archive files
    PDEST = 'build/sdist'
    WSRC  = 'ext/wxWidgets'
    WDEST = posixjoin(PDEST, WSRC)
    if not os.path.exists(PDEST):
        os.makedirs(PDEST)

    # and a place to put the final tarball
    if not os.path.exists('dist'):
        os.mkdir('dist')

    # pull out an archive copy of the repo files
    msg('Exporting Phoenix...')
    runcmd('git archive HEAD | tar -x -C %s' % PDEST, echoCmd=False)
    msg('Exporting wxWidgets...')
    runcmd('(cd %s; git archive HEAD) | tar -x -C %s' % (WSRC, WDEST), echoCmd=False)

    # copy Phoenix's generated code into the archive tree
    msg('Copying generated files...')
    for srcdir in ['cpp', 'gen']:
        destdir = posixjoin(PDEST, 'sip', srcdir)
        for name in glob.glob(posixjoin('sip', srcdir, '*')):
            copyFile(name, destdir)
    for wc in ['*.py', '*.pi', '*.pyi']:
        destdir = posixjoin(PDEST, cfg.PKGDIR)
        for name in glob.glob(posixjoin(cfg.PKGDIR, wc)):
            copyFile(name, destdir)

    # Copy the license files from wxWidgets
    msg('Copying license files...')
    updateLicenseFiles(cfg)
    shutil.copytree('license', opj(PDEST, 'license'))
    copyFile('LICENSE.txt', PDEST)

    # Copy the locale message catalogs
    msg('Copying message catalog files...')
    cfg.build_locale_dir(opj(cfg.PKGDIR, 'locale'))
    shutil.copytree(opj(cfg.PKGDIR, 'locale'), opj(PDEST, cfg.PKGDIR, 'locale'))

    # Also add the waf executable, fetching it first if we don't already have it
    getWafCmd()
    copyFile('bin/waf-%s' % wafCurrentVersion, os.path.join(PDEST, 'bin'))

    # And the REV.txt if there is one
    if os.path.exists('REV.txt'):
        copyFile('REV.txt', PDEST)

    # Copy the Sphinx source files in the docs tree, excluding the html and
    # sphinx/build folders, if present.
    shutil.rmtree(opj(PDEST, 'docs'), ignore_errors=True)
    shutil.copytree('docs', opj(PDEST, 'docs'),
                    ignore=shutil.ignore_patterns('html', 'build', '__pycache__', 'cpp'))

    # Add some extra stuff to the root folder
    cmd_egg_info(options, args, egg_base=PDEST)
    copyFile(opj(PDEST, '{}.egg-info/PKG-INFO'.format(baseName)),
             opj(PDEST, 'PKG-INFO'))

    # build the tarball
    msg('Archiving Phoenix source...')
    rootname = "%s-%s" % (baseName, cfg.VERSION)
    tarfilename = "dist/%s.tar.gz" % rootname
    if os.path.exists(tarfilename):
        os.remove(tarfilename)
    tarball = tarfile.open(name=tarfilename, mode="w:gz")
    pwd = pushDir(PDEST)
    for name in glob.glob('*'):
        tarball.add(name, os.path.join(rootname, name))
    tarball.close()
    msg('Cleaning up...')
    del pwd
    shutil.rmtree(PDEST)

    if options.upload:
        uploadPackage(tarfilename, options)

    msg("Source release built at %s" % tarfilename)



def cmd_sdist_demo(options, args):
    # Build a tarball containing the demo and samples
    cmdTimer = CommandTimer('sdist_demo')
    assert os.getcwd() == phoenixDir()

    cfg = Config()

    isGit = os.path.exists('.git')
    if not isGit:
        msg("Sorry, I don't know what to do in this source tree, no git workspace found.")
        return

    # make a tree for building up the archive files
    PDEST = 'build/sdist_demo'
    if not os.path.exists(PDEST):
        os.makedirs(PDEST)

    # and a place to put the final tarball
    if not os.path.exists('dist'):
        os.mkdir('dist')

    # pull out an archive copy of the repo files
    msg('Exporting Phoenix/demo...')
    runcmd('git archive HEAD demo | tar -x -C %s' % PDEST, echoCmd=False)
    msg('Exporting Phoenix/demo/samples...')
    runcmd('git archive HEAD samples | tar -x -C %s' % PDEST, echoCmd=False)

    # Add in the README file
    copyFile('packaging/README-sdist_demo.txt', posixjoin(PDEST, 'README.txt'))

    # build the tarball
    msg('Archiving Phoenix demo and samples...')
    rootname = "%s-demo-%s" % (baseName, cfg.VERSION)
    tarfilename = "dist/%s.tar.gz" % rootname
    if os.path.exists(tarfilename):
        os.remove(tarfilename)
    tarball = tarfile.open(name=tarfilename, mode="w:gz")
    pwd = pushDir(PDEST)
    for name in glob.glob('*'):
        tarball.add(name, os.path.join(rootname, name))
    tarball.close()
    msg('Cleaning up...')
    del pwd
    shutil.rmtree(PDEST)

    if options.upload:
        uploadPackage(tarfilename, options, keep=5,
                      mask='%s-demo-%s*' % (baseName, cfg.VER_MAJOR))

    msg("demo and samples tarball built at %s" % tarfilename)



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
    msg("Archiving Phoenix binaries to %s..." % tarfilename)
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

    if options.upload:
        uploadPackage(tarfilename, options)

    msg("Binary release built at %s" % tarfilename)



def cmd_setrev(options, args):
    # Grab the current revision number from the version control system
    # (if possible) and write it to a file we'll use later for
    # building the package version number
    cmdTimer = CommandTimer('setrev')
    assert os.getcwd() == phoenixDir()

    if options.release:
        # Ignore this command for release builds, they are not supposed to
        # include current VCS revision info in the version number.
        msg('This is a release build, setting REV.txt skipped')

    else:
        svnrev = getVcsRev()
        f = open('REV.txt', 'w')
        svnrev = '.dev'+svnrev
        f.write(svnrev)
        f.close()
        msg('REV.txt set to "%s"' % svnrev)

    cfg = Config()
    cfg.resetVersion()
    msg('cfg.VERSION: %s' % cfg.VERSION)



#---------------------------------------------------------------------------

if __name__ == '__main__':
    main(sys.argv[1:])
