#!/usr/bin/python
#---------------------------------------------------------------------------
# A simple wrapper script that assists with the building of the project for 
# day-to-day development work.  Instead of needing to remember lots of 
# commands and options for setup.py or build-wxpython.py this script uses
# some defaults that are good for development (debug mode, etc.)
#---------------------------------------------------------------------------

import sys
import os
import re
import glob
import subprocess
import optparse

from distutils.dep_util import newer, newer_group
from buildtools.config  import Config, msg, opj, posixjoin, loadETG, etg2sip
import buildtools.version as version

PYVER = '2.6'
PYSHORTVER = '26'
PYTHON = 'UNKNOWN'  # it will be set later

# wx version numbers
version2 = "%d.%d" % (version.VER_MAJOR, version.VER_MINOR) 
version3 = "%d.%d.%d" % (version.VER_MAJOR, version.VER_MINOR, version.VER_RELEASE)
version2_nodot = version2.replace(".", "")
version3_nodot = version3.replace(".", "")
    
#---------------------------------------------------------------------------

def usage():
    print """\
Usage: ./build.py [command(s)] [options]

    Commands:
        N.N NN    Major.Minor version number of the Python to use to run 
                  the other commands.  Default is 2.6
        dox       Run Doxygen to produce the XML file used by ETG scripts
        doxhtml   Run Doxygen to create the HTML documetation for wx
        touch     'touch' the etg files so they will all get run in the 
                  next build
        etg       Run the ETG scripts that are out of date to update their 
                  SIP files
        test      Run the unit test suite
        
        build_wx  Do the wxWidgets part of the build
        build_py  Build wxPython only
        build     Builds both wxWidgets and wxPython.
        
        clean_wx
        clean_py
        cleanall
"""
    parser = makeOptionParser()
    parser.print_help()
    

def main(args):
    setPythonVersion(args)
    setDevModeOptions(args)
    
    os.environ['PYTHONPATH'] = phoenixDir()
    os.environ['WXWIN'] = wxDir()
    cfg = Config(noWxConfig=True)
    msg('')

    if not args or 'help' in args or '--help' in args or '-h' in args:
        usage()
        sys.exit(1)
    
    options, commands = parseArgs(args)
    
    while commands:
        cmd = commands[0]
        commands = commands[1:]
        if cmd in ['dox', 'doxhtml', 'etg', 'touch', 'test', 
                   'build_wx', 'build_py', 'build',
                   'clean_wx', 'clean_py', 'cleanall']:
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
    # TODO: Should we default to the python that is running this script if a
    # version was not given? Probably YES on Windows, but only if TOOLS is not
    # set in the environment.
    
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
    if sys.platform.startswith('win'):
        PYTHON = posixjoin(os.environ.get('TOOLS'), 
                           'python%s' % PYSHORTVER,
                           'python.exe')
    findPython = runcmd("which %s" % PYTHON, True, False)
    msg('Found %s at %s' % (PYTHON, findPython))
    msg(runcmd('%s -c "import sys; print sys.version"' % PYTHON, True, False))
        

def setDevModeOptions(args):
    # Using --dev is a shortcut for setting several build options that I use
    # while working on the code in my local workspaces. Most people will
    # probably not use this so it is not part for the documented options and
    # is explicitly handled here before the options parser is created.
    myDevModeOptions = [
            '--sip',
            '--debug',
            '--build_dir=../bld',
            '--prefix=/opt/wx/2.9',
            '--osx_cocoa',
            '--mac_arch=i386',
            ]
    if '--dev' in args:
        idx = args.index('--dev')
        # replace the --dev item with the items from the list
        args[idx:idx+1] = myDevModeOptions

    
def phoenixDir():
    return os.path.abspath(os.path.split(__file__)[0])


def wxDir():
    WXWIN = os.environ.get('WXWIN')
    if not WXWIN:
        for rel in ['../wxWidgets', '..']:
            path = os.path.join(phoenixDir(), rel)
            if path and os.path.exists(path):
                WXWIN = os.path.abspath(os.path.join(phoenixDir(), rel))
                break
    assert WXWIN not in [None, '']
    return WXWIN


if sys.platform.startswith("win"):
    CPU = os.environ.get('CPU')
    if CPU == 'AMD64':
        dllDir = os.path.join(wxDir(), "lib", "vc_amd64_dll")        
    else:
        dllDir = os.path.join(wxDir(), "lib", "vc_dll")
    buildDir = os.path.join(wxDir(), "build", "msw")




def makeOptionParser():
    OPTS = [
        ("debug",          (False, "Build wxPython with debug symbols")),
        ("sip",            (False, "Allow SIP to regenerate the wrappers if needed")),
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
    if sys.platform == 'darwin':
        port = 'cocoa'
        if options.osx_carbon:
            port = 'carbon'
        BUILD_DIR = opj(BUILD_DIR, port)
    return BUILD_DIR



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
    


#---------------------------------------------------------------------------
# Command functions
#---------------------------------------------------------------------------


def dox(options, args):
    msg('Running command: dox')
    pwd = pushDir(posixjoin(wxDir(), 'docs/doxygen'))
    runcmd('./regen.sh xml')

    
def doxhtml(options, args):
    msg('Running command: doxhtml')
    pwd = pushDir(posixjoin(wxDir(), 'docs/doxygen'))
    runcmd('./regen.sh html chm')


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


def touch(options, args):
    msg('Running command: touch')
    pwd = pushDir(phoenixDir())
    runcmd('touch etg/*.py')
    
    
def test(options, args):
    msg('Running command: test')
    pwd = pushDir(phoenixDir())
    runcmd(PYTHON + ' unittests/runtests.py -v')

    
    
def build(options, args):
    msg('Running command: build')
    build_wx(options, args)
    build_py(options, args)

    

def build_wx(options, args):
    msg('Running command: build_wx')

    build_options = list()

    if sys.platform.startswith('win'):
        # TODO:  Add Windows specific build stuff here
        pass
    else:
        if options.osx_carbon:
            options.osx_cocoa = False
        
        BUILD_DIR = getBuildDir(options)
        DESTDIR = options.installdir
        PREFIX = options.prefix
        if options.mac_framework and sys.platform.startswith("darwin"):
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
            
        if sys.platform.startswith("darwin") and options.osx_cocoa:
            build_options.append("--osx_cocoa")
        
        if options.install:
            build_options.append('--installdir=%s' % DESTDIR)
            build_options.append("--install")
        
        if options.mac_framework and sys.platform.startswith("darwin"):
            build_options.append("--mac_framework")
                                
        # Change to what will be the wxWidgets build folder
        # (Note, this needs to be after any testing for file/path existance, etc.
        # because they may be specified as relative paths.)
        pwd = pushDir(BUILD_DIR)

    if options.debug:
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
    except:
        print "ERROR: failed building wxWidgets"
        import traceback
        traceback.print_exc()
        sys.exit(1)
        
            
    
def build_py(options, args):
    msg('Running command: build_py')

    if False:
        # For now, just run setup.py.  
        # This will need more work later, either to call build-wxpython 
        # or to implement its important parts here
        pwd = pushDir(phoenixDir())
        runcmd(PYTHON + ' setup.py build_ext '
                        '--inplace '
                        '--debug '
                        'USE_SIP=1 '
                        'WXPORT=osx_cocoa '
                        'ARCH=i386 '
                        'WX_CONFIG=/projects/wx/2.9/bld/osx_cocoa/wx-config'
                        + extraArgs)
        return

    if sys.platform.startswith("win"):
        # Copy the wxWidgets DLLs to the wxPython pacakge folder
        dlls = glob.glob(os.path.join(dllDir, "wx*" + version2_nodot + dll_type + "*.dll")) + \
               glob.glob(os.path.join(dllDir, "wx*" + version3_nodot + dll_type + "*.dll")) 
        for dll in dlls:
            shutil.copyfile(dll, os.path.join(phoenixDir(), "wxPhoenix", os.path.basename(dll)))

    BUILD_DIR = getBuildDir(options)
    DESTDIR = options.installdir
    PREFIX = options.prefix
    
    build_options = list()
    
    if options.debug:
        build_options.append("--debug")
    if options.sip:
        build_options.append('USE_SIP=1')
    if options.mac_arch: 
        build_options.append("ARCH=%s" % options.mac_arch)
        
    if sys.platform.startswith("darwin") and options.osx_cocoa:
        build_options.append("WXPORT=osx_cocoa")
    if sys.platform.startswith("darwin") and options.osx_carbon:
        build_options.append("WXPORT=osx_carbon")

    build_base = 'build'
    if sys.platform.startswith("darwin"):
        if options.osx_cocoa:
            build_base += '/cocoa'
        else:
            build_base += '/carbon'

    build_options.append("BUILD_BASE=%s" % build_base)
    build_mode = "build_ext --inplace"
    if options.install:
        build_mode = "build"
    
    if not sys.platform.startswith("win"):
        if options.install:
            wxlocation = DESTDIR + PREFIX
            #print '-='*20
            #print 'DESTDIR:', DESTDIR
            #print 'PREFIX:', PREFIX
            #print 'wxlocation:', wxlocation
            #print '-='*20
            build_options.append('WX_CONFIG="%s/bin/wx-config --prefix=%s"' %
                                 (wxlocation, wxlocation))
        else:
            build_options.append("WX_CONFIG=%s/wx-config" % BUILD_DIR)
    
    pwd = pushDir(phoenixDir())
    
    # Do the build step
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
    
        if sys.platform.startswith("darwin") and DESTDIR:
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

    print "------------ BUILD FINISHED ------------"
    print "To run the wxPython demo:"
    print " - Set your PYTHONPATH variable to %s." % phoenixDir()
    if not sys.platform.startswith("win") and not options.install:
        print " - Set your (DY)LD_LIBRARY_PATH to %s" % BUILD_DIR + "/lib"
    print " - Run python demo/demo.py"
    print

        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    main(sys.argv[1:]) 
