#!/usr/bin/python
#---------------------------------------------------------------------------
# This script is used to run through the commands used for the various stages
# of building Phoenix, and can also be a front-end for building wxWidgets and
# the Python extension mocdules.
#---------------------------------------------------------------------------

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
import urllib2

from distutils.dep_util import newer, newer_group
from buildtools.config  import Config, msg, opj, posixjoin, loadETG, etg2sip, findCmd
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

sipCurrentVersion = '4.13.1-snapshot-7ab562ae0e39'
sipCurrentVersionMD5 = {
    'darwin' : '2da0cc2ba853b2787499da0596b4e8ac', 
    'win32'  : '45673b36d6885632ad0f273c496a1383', 
    'linux2' : 'f7971044b97f7fc7650fef2189517937', 
}
toolsURL = 'http://wxpython.org/Phoenix/tools'

#---------------------------------------------------------------------------

def usage():
    print """\
Usage: ./build.py [command(s)] [options]

    Commands:
        N.N NN      Major.Minor version number of the Python to use to run 
                    the other commands.  Default is 2.7
        dox         Run Doxygen to produce the XML file used by ETG scripts
        doxhtml     Run Doxygen to create the HTML documetation for wx
        touch       'touch' the etg files so they will all get run in the 
                    next build
        etg         Run the ETG scripts that are out of date to update their 
                    SIP files
        sip         Run sip
        test        Run the unit test suite
        test_*      Run just one test module
        
        build_wx    Do the wxWidgets part of the build
        build_py    Build wxPython only
        build       Build both wxWidgets and wxPython
        
        bdist       Create a binary release of wxPython Phoenix
        
        clean_wx    Clean the wx parts of the build
        clean_py    Clean the wxPython parts of the build
        clean       Clean both wx and wxPython
"""
#        cleanall    Clean both wx and wxPython, and a little extra scrubbing

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
                     'build_wx', 'build_py', 'build', 'bdist',
                     'clean', 'clean_wx', 'clean_py', 'cleanall']:
            function = globals()[cmd]
            function(options, args)
        else:
            print '*** Unknown command:', cmd
            usage()
            sys.exit(1)
    msg("Done!")
    
#---------------------------------------------------------------------------
            
            
def runcmd(cmd, getOutput=False, echoCmd=True):
    if echoCmd:
        msg(cmd)

    otherKwArgs = dict()
    if getOutput:
        otherKwArgs = dict(stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
        
    sp = subprocess.Popen(cmd, shell=True, **otherKwArgs)

    output = None
    if getOutput:
        output = sp.stdout.read()
        output = output.rstrip()
        
    rval = sp.wait()
    if rval:
        # Failed!
        #raise subprocess.CalledProcessError(rval, cmd)
        print "Command '%s' failed with exit code %d." % (cmd, rval)
        sys.exit(rval)
    
    return output
        
    
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
                TOOLS = runcmd('cygpath -w '+TOOLS, True, False)
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
    msg(runcmd('%s -c "import sys; print sys.version"' % PYTHON, True, False))
        

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

            # These will be ignored on the other platforms so it is okay to
            # include them unconditionally
            '--osx_cocoa',
            #'--osx_carbon',
            '--mac_arch=i386',
            ]
    if not isWindows:
        myDevModeOptions.append('--debug')
    if '--dev' in args:
        idx = args.index('--dev')
        # replace the --dev item with the items from the list
        args[idx:idx+1] = myDevModeOptions

    
def phoenixDir():
    return os.path.abspath(os.path.split(__file__)[0])


def wxDir():
    WXWIN = os.environ.get('WXWIN')
    if not WXWIN:
        for rel in ['../wxWidgets', '../wx', '..']:
            path = os.path.join(phoenixDir(), rel)
            if path and os.path.exists(path) and os.path.isdir(path):
                WXWIN = os.path.abspath(os.path.join(phoenixDir(), rel))
                break
    assert WXWIN not in [None, '']
    return WXWIN


def getMSWSettings(options):
    class MSWsettings(object):
        pass
    msw = MSWsettings()
    msw.CPU = os.environ.get('CPU')
    if msw.CPU == 'AMD64':
        msw.dllDir = posixjoin(wxDir(), "lib", "vc_amd64_dll")        
    else:
        msw.dllDir = posixjoin(wxDir(), "lib", "vc_dll")
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
        ("mac_universal_binary",(False, "Build Mac version as a universal binary")),
        ("mac_arch",       ("", "Build just the specified architecture on Mac")),
        ("force_config",   (False, "Run configure when building even if the script determines it's not necessary.")),
        ("no_config",      (False, "Turn off configure step on autoconf builds")),
        ("prefix",         ("/usr/local", "Prefix value to pass to the wx build.")),
        ("install",        (False, "Install the built wxPython into installdir or standard location")),
        ("installdir",     ("", "Installation root for wxWidgets, files will go to {installdir}/{prefix}")),
        ("wxpy_installdir",("", "Installation root for wxPython, defaults to Python's site-packages.")),
        ("build_dir",      ("", "Directory to store wx build files. (Not used on Windows)")),
        ("extra_setup",    ("", "Extra args to pass on setup.py's command line.")),
        ("extra_make",     ("", "Extra args to pass on [n]make's command line.")),
        ("both",           (False, "Build both a debug and release version. (Only used on Windows)")),
        ("unicode",        (True, "Build wxPython with unicode support (always on for wx2.9)")),
        ("waf",            (False, "Use waf to build the bindings.")),
        ("verbose",        (False, "Print out more information.")),
        ("upload_package", (False, "Upload package to nightly server.")),
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
            print "Removing folder: %s" % deldir
        shutil.rmtree(deldir)
        
        
def delFiles(fileList, verbose=True):
    for afile in fileList:
        if verbose:
            print "Removing file: %s" % afile
        os.remove(afile)


def macFixDependencyInstallName(destdir, prefix, extension, buildDir):
    print "**** macFixDependencyInstallName(%s, %s, %s, %s)" % (destdir, prefix, extension, buildDir)
    pwd = os.getcwd()
    os.chdir(destdir+prefix+'/lib')
    dylibs = glob.glob('*.dylib')   
    for lib in dylibs:
        #cmd = 'install_name_tool -change %s/lib/%s %s/lib/%s %s' % \
        #      (destdir+prefix,lib,  prefix,lib,  extension)
        cmd = 'install_name_tool -change %s/lib/%s %s/lib/%s %s' % \
              (buildDir,lib,  prefix,lib,  extension)
        print cmd
        os.system(cmd)        
    os.chdir(pwd)

    
    
def getSipCmd():
    # Returns the sip command to use, checking for an explicit version and
    # attempts to download it if it is not found in the bin dir. Validity of
    # the binary is checked with an MD5 hash.
    global _sipCmd
    if os.environ.get('SIP'):
        # Setting a a value in the environment overrides other options
        return os.environ.get('SIP')
    elif _sipCmd is not None:
        # use the cached value is there is one
        return _sipCmd
    else:
        platform = sys.platform
        ext = ''
        if platform == 'win32':
            ext = '.exe'
        cmd = opj('bin', 'sip-%s-%s%s' % (sipCurrentVersion, platform, ext))
        msg('Checking for %s...' % cmd)
        if os.path.exists(cmd):
            m = hashlib.md5()
            m.update(open(cmd, 'rb').read())
            if m.hexdigest() != sipCurrentVersionMD5[platform]:
                print 'ERROR: MD5 mismatch, got "%s"' % m.hexdigest()
                print '       expected          "%s"' % sipCurrentVersionMD5[platform]
                print '       Set SIP in the environment to use a local build of sip instead'
                sys.exit(1)
            _sipCmd = cmd
            return cmd
        
        msg('Not found.  Attempting to download...')
        url = '%s/sip-%s-%s%s.bz2' % (toolsURL, sipCurrentVersion, platform, ext)
        try:
            connection = urllib2.urlopen(url)
            msg('Connection successful...')
            data = connection.read()
            msg('Data downloaded...')
        except:
            print "ERROR: Unable to download", url
            print "       Set SIP in the environment to use a local build of sip instead"
            import traceback
            traceback.print_exc()
            sys.exit(1)
            
        import bz2
        data = bz2.decompress(data)
        with open(cmd, 'wb') as f:
            f.write(data)
        os.chmod(cmd, 0755)
        return getSipCmd()
            

# The download and MD5 check only needs to happen once per run, cache the sip
# cmd value here the first time through.
_sipCmd = None



#---------------------------------------------------------------------------
# Command functions
#---------------------------------------------------------------------------


def _doDox(arg):
    if isWindows:
        d = posixjoin(wxDir(), 'docs/doxygen')
        d = d.replace('\\', '/')
        cmd = 'c:/cygwin/bin/bash.exe -l -c "cd %s && ./regen.sh %s"' % (d, arg)
    else:
        pwd = pushDir(posixjoin(wxDir(), 'docs/doxygen'))
        cmd = './regen.sh %s' % arg
    runcmd(cmd)

    
def dox(options, args):
    msg('Running command: dox')
    _doDox('xml')
    
    
def doxhtml(options, args):
    msg('Running command: doxhtml')
    #_doDox('html')
    _doDox('chm')
    
    

def etg(options, args):
    msg('Running command: etg')
    pwd = pushDir(phoenixDir())
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
        
        # run the script if any dependencies are newer
        if newer_group(deps, sipfile):
            runcmd('%s %s --sip' % (PYTHON, script))

            
def sip(options, args):
    msg('Running command: sip')
    cfg = Config()
    for src_name in glob.glob(opj(cfg.SIPGEN, '_*.sip')):
        tmpdir = tempfile.mkdtemp()
        tmpdir = tmpdir.replace('\\', '/')
        src_name = src_name.replace('\\', '/')
        base = os.path.basename(os.path.splitext(src_name)[0])
        sbf = posixjoin(cfg.SIPOUT, base) + '.sbf'
        pycode = base.replace('_', '')
        pycode = posixjoin(cfg.PKGDIR, pycode) + '.py'
        pycode = '-X pycode'+base+':'+pycode        
        sip = getSipCmd()
        cmd = '%s %s -c %s -b %s %s %s'  % \
            (sip, cfg.SIPOPTS, tmpdir, sbf, pycode, src_name)
        runcmd(cmd)

                
        def processSrc(src, keepHashLines=False):
            with file(src, 'rt') as f:
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
                f = file(dest, 'wt')
                f.write(srcTxt)
                f.close()
                continue

            srcTxt = processSrc(src, options.keep_hash_lines)
            with file(dest, 'rt') as f:
                destTxt = f.read()
                
            if srcTxt == destTxt:
                pass
            else:
                msg('%s is changed, copying...' % os.path.basename(src))
                f = file(dest, 'wt')
                f.write(srcTxt)
                f.close()
                
        # Remove tmpdir and its contents
        shutil.rmtree(tmpdir)
    
    
    
def touch(options, args):
    msg('Running command: touch')
    pwd = pushDir(phoenixDir())
    runcmd('touch etg/*.py')
    
    
def test(options, args):
    msg('Running command: test')
    pwd = pushDir(phoenixDir())
    runcmd(PYTHON + ' unittests/runtests.py %s' % ('-v' if options.verbose else ''))

    
def testOne(name, options, args):
    msg('Running test %s:' % name)
    pwd = pushDir(phoenixDir())
    runcmd(PYTHON + ' unittests/%s.py %s' % (name, '-v' if options.verbose else ''))
    
    
def build(options, args):
    msg('Running command: build')
    build_wx(options, args)
    build_py(options, args)

    

def build_wx(options, args):
    msg('Running command: build_wx')

    build_options = ['--wxpython', '--unicode']

    if isWindows:
        # Windows-specific pre build stuff 
        pass
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
        if options.mac_universal_binary:
            build_options.append("--mac_universal_binary")
        if  options.mac_arch: 
            build_options.append("--mac_arch=%s" % options.mac_arch)

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

        print 'wxWidgets build options:', build_options
        wxbuild.main(wxscript, build_options)
        
        # build again without the --debug flag?
        if isWindows and options.both:
            build_options.remove('--debug')
            print 'wxWidgets build options:', build_options
            wxbuild.main(wxscript, build_options)
            
    except:
        print "ERROR: failed building wxWidgets"
        import traceback
        traceback.print_exc()
        sys.exit(1)
        
    # Build the wx message catalogs, but first check that there is a msgfmt
    # command available
    if findCmd('msgfmt'):
        locale_pwd = pushDir(posixjoin(wxDir(), 'locale'))
        print 'Building message catalogs in', os.getcwd()
        runcmd('make allmo')
        del locale_pwd
    else:
        print "WARNING: msgfmt command not found, message catalogs not rebulit.\n" \
              "         Please install gettext and associated tools."
    
            
    
def build_py(options, args):
    msg('Running command: build_py')

    if isWindows:
        # Copy the wxWidgets DLLs to the wxPython pacakge folder
        msw = getMSWSettings(options)
        cfg = Config()

        # NOTE: this will copy both debug and release DLLs if they both
        # exist... TODO: It would probably be a good idea to filter out the
        # debug files unless --debug is given.
        ver = version3_nodot if unstable_series else version2_nodot
        dlls = list()
        if not options.debug or options.both:
            dlls += glob.glob(os.path.join(msw.dllDir, "wx*%su_*.dll" % ver))
        if options.debug or options.both:
            dlls += glob.glob(os.path.join(msw.dllDir, "wx*%sud_*.dll" % ver))
            dlls += glob.glob(os.path.join(msw.dllDir, "wx*%sud_*.pdb" % ver))
            
        for dll in dlls:
            shutil.copyfile(dll, posixjoin(phoenixDir(), cfg.PKGDIR, os.path.basename(dll)))

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
    if options.waf:
        os.environ["PATH"] = BUILD_DIR + os.pathsep + os.environ["PATH"]
        
        waf_args = "configure build install"
        for arg in args:
            if arg.startswith("clean"):
                waf_args = "clean distclean"
                
        command = "./waf %s -v -j6 --wx-config=%s/wx-config" % (waf_args, BUILD_DIR)
    else:
        command = PYTHON + " -u ./setup.py %s %s %s" % \
            (build_mode, " ".join(build_options), options.extra_setup)
    
    runcmd(command)

    if isWindows and options.both:
        build_options.remove('--debug')
        command = PYTHON + " -u ./setup.py %s %s %s" % \
            (build_mode, " ".join(build_options), options.extra_setup)
        runcmd(command)
        
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
    
        if isDarwin and DESTDIR:
            # Now that we are finished with the build fix the ids and
            # names in the wx .dylibs
            wxbuild.macFixupInstallNames(DESTDIR, PREFIX, BUILD_DIR)

            # and also adjust the dependency names in the wxPython extensions
            for line in file("installed_files.txt"):
                line = line.strip()
                if line.endswith('.so'):
                    macFixDependencyInstallName(DESTDIR, PREFIX, line, BUILD_DIR)
                
    ## update the language files
    #command = PYTHON + " -u " + os.path.join(phoenixDir(), "distrib", "makemo.py")
    #runcmd(command)

    print "\n------------ BUILD FINISHED ------------"
    print "To run the wxPython demo:"
    print " - Set your PYTHONPATH variable to %s." % phoenixDir()
    if not isWindows and not options.install:
        print " - Set your (DY)LD_LIBRARY_PATH to %s" % BUILD_DIR + "/lib"
    print " - Run python demo/demo.py"
    print

    
def clean_wx(options, args):
    msg('Running command: clean_wx')
    if isWindows:
        if options.both:
            options.debug = True
        msw = getMSWSettings(options)
        cfg = Config()  
        deleteIfExists(opj(msw.dllDir, 'msw'+msw.dll_type))
        delFiles(glob.glob(opj(msw.dllDir, 'wx*%s%s*' % (version2_nodot, msw.dll_type))))
        delFiles(glob.glob(opj(msw.dllDir, 'wx*%s%s*' % (version3_nodot, msw.dll_type))))  
        deleteIfExists(opj(msw.buildDir, 'vc_msw'+msw.dll_type+'dll'))
        
        if options.both:
            options.debug = False
            options.both = False
            clean_wx(options, args)
            options.both = True
    else:
        BUILD_DIR = getBuildDir(options)
        deleteIfExists(BUILD_DIR)
    

def clean_py(options, args):
    msg('Running command: clean_py')
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
    files = list()
    for wc in ['*.py', '*.pyc', '*.so', '*.pyd', '*.pdb',
               ]:
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
    
        
def clean(options, args):
    clean_wx(options, args)
    clean_py(options, args)
   
    
def cleanall(options, args):
    # These take care of all the object, lib, shared lib files created by the
    # compilation part of build
    clean_wx(options, args)
    clean_py(options, args)
    
    # Now also scrub out all of the SIP and C++ source files that are
    # generated by the Phoenix ETG system.
    msg('Running command: cleanall')
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
    
    dllext = ".so"
    environ_script="packaging/phoenix_environ.sh"
    wxlibdir = os.path.join(getBuildDir(options), "lib") 
    if sys.platform.startswith('win'):
        #dllext = ".dll"
        #wxlibdir = os.path.join(wxDir(), "lib", "vc_dll")
        environ_script = None #"packaging/phoenix_environ.bat"
    elif sys.platform.startswith('darwin'):
        dllext = ".dylib"
     
    def _getDate():
        import datetime
        today = datetime.date.today()
        return "%d%02d%02d" % (today.year, today.month, today.day)
        
    svnrev = None
    try:
        rev = runcmd('svnversion', getOutput=True, echoCmd=False)
        if rev == 'exported':
            svnrev = _getDate()
        else:
            svnrev = "r" + rev.split(':')[0]
    except:
        svnrev = _getDate()
        
    rootname = "wxPython-Phoenix-%s-%s-py%s" % (svnrev, sys.platform, PYVER)
    tarfilename = "dist/%s.tar.gz" % rootname

    if not os.path.exists('dist'):
        os.makedirs('dist')
    
    if os.path.exists(tarfilename):
        os.remove(tarfilename)
    print "Archiving Phoenix bindings..."
    tarball = tarfile.open(name=tarfilename, mode="w:gz")
    tarball.add('wx', os.path.join(rootname, 'wx'))
    if not sys.platform.startswith('win'):
        # The DLLs have already been copied to wx on Windows, and so are
        # already in the tarball. For other platforms fetch them now.
        print "Archiving wxWidgets shared libraries..."
        dlls = glob.glob(os.path.join(wxlibdir, "*%s" % dllext))
        for dll in dlls:
            tarball.add(dll, os.path.join(rootname, 'wx', os.path.basename(dll)))

    if environ_script:
        tarball.add(environ_script, os.path.join(rootname, os.path.basename(environ_script)))
    tarball.close()
    
    if options.upload_package:
        print "Preparing to upload package..."
        configfile = os.path.join(os.getenv("HOME"), "phoenix_package_server.cfg")
        if not os.path.exists(configfile):
            print "Cannot upload, server configuration not set."
            #sys.exit(1)
            
        import ConfigParser
        parser = ConfigParser.ConfigParser()
        parser.read(configfile)
        
        print "Connecting to FTP server..."
        from ftplib import FTP
        ftp = FTP(parser.get("FTP", "host"))
        ftp.login(parser.get("FTP", "user"), parser.get("FTP", "pass"))
        f = open(tarfilename, 'rb')
        ftp_path = '%s/%s' % (parser.get("FTP", "dir"), os.path.basename(tarfilename))
        print "Uploading package (this may take some time)..."
        ftp.storbinary('STOR %s' % ftp_path, f)

        ftp.close()
        print "Upload complete!"
    
    print "Release built at %s" % tarfilename

    
#---------------------------------------------------------------------------

if __name__ == '__main__':
    main(sys.argv[1:]) 
