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
PYTHON = 'UNKNOWN'  # it will be set later

# wx version numbers
version2 = "%d.%d" % (version.VER_MAJOR, version.VER_MINOR) 
version3 = "%d.%d.%d" % (version.VER_MAJOR, version.VER_MINOR, version.VER_RELEASE)
version2_nodot = version2.replace(".", "")
version3_nodot = version3.replace(".", "")
unstable_series = (version.VER_MINOR % 2) == 1  # is the minor version odd or even?
    
isWindows = sys.platform.startswith('win')
isDarwin = sys.platform == "darwin"


# Some tools will be downloaded for the builds. These are the versions and
# MD5s of the tool binaries currently in use.
sipCurrentVersion = '4.13.3-snapshot-377e9e4763f5'
sipMD5 = {
    'darwin' : '23e22703cacf9110730c539d348e6e46',
    'win32'  : '801c477ebe9e02e314e7e153e6ea7356', 
    'linux2' : '07a1676641918106132bb64aa6517734', 
}

wafCurrentVersion = '1.6.11'
wafMD5 = '9a631fda1e570da8e4813faf9f3c49a4'

doxygenCurrentVersion = '1.7.4'
doxygenMD5 = {
    'darwin' : 'dbb76a5317ab1fe9b8d77683b726250e',
    'win32'  : 'b9882b83ec63cc816b91bd7dd05facdc', 
    'linux2' : '8cb4ef98775046428a70737fd0aa3a19', 
}

# And the location where they can be downloaded from
toolsURL = 'http://wxpython.org/Phoenix/tools'

#---------------------------------------------------------------------------

def usage():
    print ("""\
Usage: ./build.py [command(s)] [options]

  Commands:
      N.N NN        Major.Minor version number of the Python to use to run 
                    the other commands.  Default is 2.7
      dox           Run Doxygen to produce the XML file used by ETG scripts
      doxhtml       Run Doxygen to create the HTML documetation for wx
      touch         'touch' the etg files so they will all get run in the 
                    next build
      etg           Run the ETG scripts that are out of date to update their 
                    SIP files
      sphinx        Run the documentation building process using Sphinx (this
                    needs to be done after dox and etg)
      wxlib         Run the documentation building process using Sphinx for wx.lib
      wxpy          Run the documentation building process using Sphinx for wx.py
      wxtools       Run the documentation building process using Sphinx for wx.tools
      sip           Run sip
      
      test          Run the unit test suite
      test_*        Run just one test module
        
      build         Build both wxWidgets and wxPython
      build_wx      Do only the wxWidgets part of the build

      setup_py      Build wxPython only, using setup.py
      waf_py        Build wxPython only, using waf
      build_py      Alias for "setup_py"
        
      bdist         Create a binary release of wxPython Phoenix
      docs_bdist    Build a tarball containing the documentation
        
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
        cmd = commands[0]
        commands = commands[1:]
        if cmd.startswith('test_'):
            testOne(cmd, options, args)
        elif cmd in ['dox', 'doxhtml', 'etg', 'sip', 'touch', 'test', 
                     'build_wx', 'build_py', 'setup_py', 'waf_py', 'build', 'bdist',
                     'clean', 'clean_wx', 'clean_py', 'cleanall', 'clean_sphinx',
                     'sphinx', 'wxlib', 'wxpy', 'wxtools', 'docs_bdist']:
            function = globals()[cmd]
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
    # TODO: Should we have a --option for specifying the path to the python
    # executable that should be used?

    global PYVER
    global PYSHORTVER
    global PYTHON
    for idx, arg in enumerate(args):
        if re.match(r'^[0-9]\.[0-9]$', arg):
            PYVER = arg
            PYSHORTVER = arg[0] + arg[2]
            del args[idx]
            break
        if re.match(r'^[0-9][0-9]$', arg):
            PYVER = '%s.%s' % (arg[0], arg[1])
            PYSHORTVER = arg
            del args[idx]
            break

    PYTHON = 'python%s' % PYVER
    if isWindows:
        if os.environ.get('TOOLS'):
            TOOLS = os.environ.get('TOOLS')
            if 'cygdrive' in TOOLS:
                TOOLS = runcmd('c:/cygwin/bin/cygpath -w '+TOOLS, True, False)
            PYTHON = posixjoin(TOOLS, 
                               'python%s' % PYSHORTVER,
                               'python.exe')
        else:
            # if TOOLS is not set then default to the python that invoked 
            # this script
            PYTHON = sys.executable
            PYVER = sys.version[:3]
            PYSHORTVER = PYVER[0] + PYVER[2]
        msg('Using %s' % PYTHON)
    else:
        findPython = runcmd("which %s" % PYTHON, True, False)
        msg('Found %s at %s' % (PYTHON, findPython))
        PYTHON = findPython
    msg(runcmd('%s -c "import sys; print(sys.version)"' % PYTHON, True, False))
        

def setDevModeOptions(args):
    # Using --dev is a shortcut for setting several build options that I use
    # while working on the code in my local workspaces. Most people will
    # probably not use this so it is not part for the documented options and
    # is explicitly handled here before the options parser is created. If
    # anybody besides Robin is using this option do not depend on the options
    # it inserts into the args list being consistent. They could change at any
    # update from the repository.
    myDevModeOptions = [
            '--build_dir=../bld',
            '--prefix=/opt/wx/2.9',
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
    class MSWsettings(object):
        pass
    msw = MSWsettings()
    msw.CPU = os.environ.get('CPU')
    if msw.CPU == 'AMD64':
        msw.dllDir = posixjoin(wxDir(), "lib", "vc%s_amd64_dll" % getVisCVersion())        
    else:
        msw.dllDir = posixjoin(wxDir(), "lib", "vc%s_dll" % getVisCVersion())
    msw.buildDir = posixjoin(wxDir(), "build", "msw")

    msw.dll_type = "u"
    if options.debug:
        msw.dll_type = "ud"
    return msw
        



def makeOptionParser():
    OPTS = [
        ("debug",          (False, "Build wxPython with debug symbols")),
        ("keep_hash_lines",(False, "Don't remove the '#line N' lines from the SIP generated code")),
        ("osx_cocoa",      (True,  "Build the OSX Cocoa port on Mac (default)")),
        ("osx_carbon",     (False, "Build the OSX Carbon port on Mac")),
        ("mac_framework",  (False, "Build wxWidgets as a Mac framework.")),
        ("mac_arch",       ("", "Comma separated list of architectures to build on Mac")),
        ("force_config",   (False, "Run configure when building even if the script determines it's not necessary.")),
        ("no_config",      (False, "Turn off configure step on autoconf builds")),
        ("prefix",         ("/usr/local", "Prefix value to pass to the wx build.")),
        ("install",        (False, "Install the built wxPython into installdir or standard location")),
        ("installdir",     ("", "Installation root for wxWidgets, files will go to {installdir}/{prefix}")),
        ("wxpy_installdir",("", "Installation root for wxPython, defaults to Python's site-packages.")),
        ("build_dir",      ("", "Directory to store wx build files. (Not used on Windows)")),
        ("extra_setup",    ("", "Extra args to pass on setup.py's command line.")),
        ("extra_make",     ("", "Extra args to pass on [n]make's command line.")),
        ("extra_waf",      ("", "Extra args to pass on waf's command line.")),   
        ("jobs",           ("", "Number of parallel compile jobs to do, if supported.")), 
        ("both",           (False, "Build both a debug and release version. (Only used on Windows)")),
        ("unicode",        (True, "Build wxPython with unicode support (always on for wx2.9)")),
        ("verbose",        (False, "Print out more information.")),
        ("nodoc",          (False, "Do not run the default docs generator")),
        ("upload_package", (False, "Upload bdist package to nightly server.")),
        ("cairo",          (False, "Allow Cairo use with wxGraphicsContext (Windows only)")),
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
    return options, args


class pushDir(object):
    def __init__(self, newDir):
        self.cwd = os.getcwd()
        os.chdir(newDir)
        
    def __del__(self):
        # pop back to the original dir
        os.chdir(self.cwd)

        
def getBuildDir(options):
    BUILD_DIR = opj(phoenixDir(), 'bld')
    if options.build_dir:
        BUILD_DIR = os.path.abspath(options.build_dir)        
    if isDarwin:
        port = 'cocoa'
        if options.osx_carbon:
            port = 'carbon'
        BUILD_DIR = opj(BUILD_DIR, port)
    return BUILD_DIR


def deleteIfExists(deldir, verbose=True):
    if os.path.exists(deldir) and os.path.isdir(deldir):
        if verbose:
            print("Removing folder: %s" % deldir)
        shutil.rmtree(deldir)
        
        
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
            platform = sys.platform
            ext = ''
            if platform == 'win32':
                ext = '.exe'
            cmd = opj('bin', '%s-%s-%s%s' % (cmdName, version, platform, ext))
            md5 = MD5[platform]
        else:
            cmd = opj('bin', '%s-%s' % (cmdName, version))
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



#---------------------------------------------------------------------------
# Command functions
#---------------------------------------------------------------------------


def _doDox(arg):
    doxCmd = getDoxCmd()
    doxCmd = os.path.abspath(doxCmd)
    
    if isWindows:
        doxCmd = doxCmd.replace('\\', '/')
        doxCmd = runcmd('c:/cygwin/bin/cygpath -u '+doxCmd, True, False)
        os.environ['DOXYGEN'] = doxCmd
        d = posixjoin(wxDir(), 'docs/doxygen')
        d = d.replace('\\', '/')
        cmd = 'c:/cygwin/bin/bash.exe -l -c "cd %s && ./regen.sh %s"' % (d, arg)
    else:
        os.environ['DOXYGEN'] = doxCmd
        pwd = pushDir(posixjoin(wxDir(), 'docs/doxygen'))
        cmd = './regen.sh %s' % arg
    runcmd(cmd)

    
def dox(options, args):
    cmdTimer = CommandTimer('dox')
    _doDox('xml')
    
    
def doxhtml(options, args):
    cmdTimer = CommandTimer('doxhtml')
    _doDox('html')
    _doDox('chm')
    
    

def etg(options, args):
    cmdTimer = CommandTimer('etg')
    pwd = pushDir(phoenixDir())

    # TODO: Better support for selecting etg cmd-line flags...
    flags = '--sip'
    if options.nodoc:
        flags += ' --nodoc'

    etgfiles = glob.glob('etg/_*.py')
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

    
def sphinx(options, args):
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
    migration_guide = os.path.join(phoenixDir(), 'docs', 'MigrationGuide.txt')
    copyIfNewer(todo, sphinxDir)
    copyIfNewer(migration_guide, sphinxDir)
    
    MakeHeadings()

    pwd2 = pushDir(sphinxDir)
    buildDir = os.path.join(sphinxDir, 'build')
    htmlDir = os.path.join(phoenixDir(), 'docs', 'html')
    runcmd('sphinx-build -b html -d %s/doctrees . %s' % (buildDir, htmlDir))
    del pwd2
    
    msg('Postprocesing sphinx output...')
    PostProcess(htmlDir)


def wxlib(options, args):
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
    

def wxpy(options, args):
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


def wxtools(options, args):
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


def docs_bdist(options, args):
    cmdTimer = CommandTimer('docs_bdist')
    pwd = pushDir(phoenixDir())

    svnrev = getSvnRev()
        
    rootname = "wxPython-Phoenix-%s-docs" % svnrev
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
    
    
def sip(options, args):
    cmdTimer = CommandTimer('sip')
    cfg = Config()
    modules = glob.glob(opj(cfg.SIPGEN, '_*.sip'))
    # move _core the to the front of the list
    modules.remove(opj(cfg.SIPGEN, '_core.sip'))
    modules.insert(0, opj(cfg.SIPGEN, '_core.sip'))
    
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
        sipFiles = getSipFiles(etg.INCLUDES)
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
    
    
    
def touch(options, args):
    cmdTimer = CommandTimer('touch')
    pwd = pushDir(phoenixDir())
    runcmd('touch etg/*.py')
    
    
def test(options, args):
    cmdTimer = CommandTimer('test')
    pwd = pushDir(phoenixDir())
    runcmd(PYTHON + ' unittests/runtests.py %s' % ('-v' if options.verbose else ''), fatal=False)

    
def testOne(name, options, args):
    cmdTimer = CommandTimer('test %s:' % name)
    pwd = pushDir(phoenixDir())
    runcmd(PYTHON + ' unittests/%s.py %s' % (name, '-v' if options.verbose else ''), fatal=False)
    
    
def build(options, args):
    cmdTimer = CommandTimer('build')
    build_wx(options, args)
    build_py(options, args)



def build_wx(options, args):
    cmdTimer = CommandTimer('build_wx')
    
    build_options = ['--wxpython', '--unicode']

    if options.jobs:
        build_options.append('--jobs=%s' % options.jobs)

    if isWindows:
        # Windows-specific pre build stuff 
        if options.cairo:
            build_options.append('--cairo')
            if not os.environ.get("CAIRO_ROOT"):
                msg("WARNING: Expected CAIRO_ROOT set in the environment!")

    else:  
        # Platform is something other than MSW
        if options.osx_carbon:
            options.osx_cocoa = False
        
        BUILD_DIR = getBuildDir(options)
        DESTDIR = options.installdir
        PREFIX = options.prefix
        if options.mac_framework and isDarwin:
            # TODO:  Don't hard-code this path
            PREFIX = "/Library/Frameworks/wx.framework/Versions/%s" %  version2
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
        
        if options.install:
            build_options.append('--installdir=%s' % DESTDIR)
            build_options.append("--install")
        
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
        

    
            
def build_py(options, args):
    cmdTimer = CommandTimer('build_py')
    #setup_py(options, args)
    waf_py(options, args)


    
def copyWxDlls(options):
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
                
    
    
def setup_py(options, args):
    cmdTimer = CommandTimer('setup_py')

    BUILD_DIR = getBuildDir(options)
    DESTDIR = options.installdir
    PREFIX = options.prefix
    
    build_options = list()
    
    if options.debug or (isWindows and options.both):
        build_options.append("--debug")
    if isDarwin and options.mac_arch: 
        build_options.append("ARCH=%s" % options.mac_arch)
        
    if isDarwin and options.osx_cocoa:
        build_options.append("WXPORT=osx_cocoa")
    if isDarwin and options.osx_carbon:
        build_options.append("WXPORT=osx_carbon")

    build_base = 'build'
    if isDarwin:
        if options.osx_cocoa:
            build_base += '/cocoa'
        else:
            build_base += '/carbon'

    build_options.append("BUILD_BASE=%s" % build_base)
    build_mode = "build_ext --inplace"
    if options.install:
        build_mode = "build"
    
    if not isWindows:
        if options.install:
            wxlocation = DESTDIR + PREFIX
            build_options.append('WX_CONFIG="%s/bin/wx-config --prefix=%s"' %
                                 (wxlocation, wxlocation))
        else:
            build_options.append("WX_CONFIG=%s/wx-config" % BUILD_DIR)
    
    pwd = pushDir(phoenixDir())
    
    # Do the build step
    command = PYTHON + " -u ./setup.py %s %s %s" % \
            (build_mode, " ".join(build_options), options.extra_setup)
    
    runcmd(command)

    if isWindows and options.both:
        build_options.remove('--debug')
        command = PYTHON + " -u ./setup.py %s %s %s" % \
            (build_mode, " ".join(build_options), options.extra_setup)
        runcmd(command)
        
    copyWxDlls(options)
    
    # Do an install?
    if options.install:
        # only add the --prefix flag if we have an explicit request to do
        # so, otherwise let distutils install in the default location.
        install_dir = DESTDIR or PREFIX
        WXPY_PREFIX = ""
        if options.wxpy_installdir:
            install_dir = options.wxpy_installdir
            WXPY_PREFIX = "--prefix=%s" % options.wxpy_installdir
        
        # do the install step
        command = PYTHON + " -u ./setup.py install %s %s %s --record installed_files.txt" % \
            (WXPY_PREFIX, " ".join(build_options), options.extra_setup)
        runcmd(command)
    
        # NOTE: Can probably get rid of this if we keep the code that is
        # setting @loader_path in the install names...
        if isDarwin and DESTDIR:
            # Now that we are finished with the build fix the ids and
            # names in the wx .dylibs
            wxbuild.macFixupInstallNames(DESTDIR, PREFIX, BUILD_DIR)

            # and also adjust the dependency names in the wxPython extensions
            for line in open("installed_files.txt"):
                line = line.strip()
                if line.endswith('.so'):
                    macFixDependencyInstallName(DESTDIR, PREFIX, line, BUILD_DIR)
                
    print("\n------------ BUILD FINISHED ------------")
    print("To run the wxPython demo:")
    print(" - Set your PYTHONPATH variable to %s." % phoenixDir())
    if not isWindows and not options.install:
        print(" - Set your (DY)LD_LIBRARY_PATH to %s" % BUILD_DIR + "/lib")
    print(" - Run python demo/demo.py")
    print("")



def waf_py(options, args):
    cmdTimer = CommandTimer('waf_py')
    waf = getWafCmd()

    BUILD_DIR = getBuildDir(options)
    DESTDIR = options.installdir
    PREFIX = options.prefix

    wafBuildBase = posixjoin('build_waf', PYVER)
    wafBuildDir  = wafBuildBase
    if isWindows:
        wafBuildDir = posixjoin(wafBuildBase, 'release')
        
    build_options = list()
    build_options.append('--prefix=%s' % PREFIX)
    if options.debug or (isWindows and options.both):
        build_options.append("--debug")
        if isWindows:
            wafBuildDir = posixjoin(wafBuildBase, 'debug')
    if isDarwin and options.mac_arch: 
        build_options.append("--mac_arch=%s" % options.mac_arch)
    if not isWindows:
        build_options.append('--wx_config=%s' % posixjoin(BUILD_DIR, 'wx-config'))
    if options.verbose:
        build_options.append('--verbose')
    if options.jobs:
        build_options.append('--jobs=%s' % options.jobs)

    build_options.append('--python=%s' % PYTHON)
    build_options.append('--out=%s' % wafBuildDir)
        
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

    # Do an install?
    if options.install:
        pass # TODO...
    
    
    print("\n------------ BUILD FINISHED ------------")
    print("To run the wxPython demo:")
    print(" - Set your PYTHONPATH variable to %s." % phoenixDir())
    if not isWindows and not options.install:
        print(" - Set your (DY)LD_LIBRARY_PATH to %s" % BUILD_DIR + "/lib")
    print(" - Run python demo/demo.py")
    print("")


    
def clean_wx(options, args):
    cmdTimer = CommandTimer('clean_wx')
    if isWindows:
        if options.both:
            options.debug = True
        msw = getMSWSettings(options)
        cfg = Config()  
        deleteIfExists(opj(msw.dllDir, 'msw'+msw.dll_type))
        delFiles(glob.glob(opj(msw.dllDir, 'wx*%s%s*' % (version2_nodot, msw.dll_type))))
        delFiles(glob.glob(opj(msw.dllDir, 'wx*%s%s*' % (version3_nodot, msw.dll_type))))  
        deleteIfExists(opj(msw.buildDir, 'vc%s_msw%sdll' % (getVisCVersion(), msw.dll_type)))
        
        if options.both:
            options.debug = False
            options.both = False
            clean_wx(options, args)
            options.both = True
    else:
        BUILD_DIR = getBuildDir(options)
        deleteIfExists(BUILD_DIR)
    

def clean_py(options, args):
    cmdTimer = CommandTimer('clean_py')
    assert os.getcwd() == phoenixDir()
    if isWindows and options.both:
        options.debug = True
    cfg = Config()
    build_base = 'build'
    if isDarwin:
        if options.osx_cocoa:
            build_base += '/cocoa'
        else:
            build_base += '/carbon'
    deleteIfExists(build_base)
    deleteIfExists('build_waf')  # make this smarter later, or just use 'build' for waf too
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
        clean_py(options, args)
        options.both = True


    
def clean_sphinx(options, args):
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

        
def clean(options, args):
    clean_wx(options, args)
    clean_py(options, args)
    
    
def cleanall(options, args):
    # These take care of all the object, lib, shared lib files created by the
    # compilation part of build
    clean_wx(options, args)
    clean_py(options, args)
    
    # Clean all the intermediate and generated files from the sphinx command
    clean_sphinx(options, args)
    
    # Now also scrub out all of the SIP and C++ source files that are
    # generated by the Phoenix ETG system.
    cmdTimer = CommandTimer('cleanall')
    assert os.getcwd() == phoenixDir()
    files = list()
    for wc in ['sip/cpp/*.h', 'sip/cpp/*.cpp', 'sip/cpp/*.sbf', 'sip/gen/*.sip']:
        files += glob.glob(wc)
    delFiles(files)

    
def buildall(options, args):
    # (re)build everything
    build_wx(options, args)
    dox(options, args)
    touch(options, args)
    etg(options, args)
    sip(options, args)
    build_py(options, args)
    test(options, args)
    
    
def sdist(options, args):
    # Build a source tarball that includes the generated SIP and CPP files.
    pass


def bdist(options, args):
    # Build a tarball and/or installer that includes all the files needed at
    # runtime for the current platform and the current version of Python.
    
    cmdTimer = CommandTimer('bdist')
    assert os.getcwd() == phoenixDir()

    dllext = ".so"
    environ_script="packaging/phoenix_environ.sh"
    readme = "packaging/README.txt"
    wxlibdir = os.path.join(getBuildDir(options), "lib") 
    if sys.platform.startswith('win'):
        environ_script = None 
    elif sys.platform.startswith('darwin'):
        dllext = ".dylib"
     
    svnrev = getSvnRev()
        
    rootname = "wxPython-Phoenix-%s-%s-py%s" % (svnrev, sys.platform, PYVER)
    tarfilename = "dist/%s.tar.gz" % rootname

    if not os.path.exists('dist'):
        os.makedirs('dist')
    
    if os.path.exists(tarfilename):
        os.remove(tarfilename)
    msg("Archiving Phoenix bindings...")
    tarball = tarfile.open(name=tarfilename, mode="w:gz")
    tarball.add('wx', os.path.join(rootname, 'wx'), 
                filter=lambda info: None if '.svn' in info.name else info)
    if not isDarwin and not isWindows:
        # The DLLs have already been copied to wx on Windows, and so are
        # already in the tarball. For other platforms fetch them now.
        msg("Archiving wxWidgets shared libraries...")
        dlls = glob.glob(os.path.join(wxlibdir, "*%s" % dllext))
        for dll in dlls:
            tarball.add(dll, os.path.join(rootname, 'wx', os.path.basename(dll)))

    if environ_script:
        tarball.add(environ_script, os.path.join(rootname, os.path.basename(environ_script)))
    tarball.add(readme, os.path.join(rootname, os.path.basename(readme)))
    tarball.close()

    if options.upload_package:
        uploadPackage(tarfilename, '-%s-py%s' % (sys.platform, PYVER))
                
    msg("Release built at %s" % tarfilename)

    
#---------------------------------------------------------------------------

if __name__ == '__main__':
    main(sys.argv[1:]) 
