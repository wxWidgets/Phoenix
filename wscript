#!/usr/bin/python
#-----------------------------------------------------------------------------
#  WAF script for building and installing the wxPython extension modules.
#
# Author:      Robin Dunn
# Copyright:   (c) 2013 by Total Control Software
# License:     wxWindows License
#-----------------------------------------------------------------------------

import sys
import os

import buildtools.config
cfg = buildtools.config.Config(True)

#-----------------------------------------------------------------------------
# Options and configuration

APPNAME = 'wxPython'
VERSION = cfg.VERSION

isWindows = sys.platform.startswith('win')
isDarwin = sys.platform == "darwin"

top = '.'
out = 'build/waf'


def options(opt):
    if isWindows:
        opt.load('msvc')
    else:
        opt.load('compiler_cc compiler_cxx')
    opt.load('python')

    opt.add_option('--debug', dest='debug', action='store_true', default=False,
                   help='Turn on debug compile options.')        
    opt.add_option('--python', dest='python', default='', action='store',
                   help='Full path to the Python executrable to use.')
    opt.add_option('--wx_config', dest='wx_config', default='wx-config', action='store',
                   help='Full path to the wx-config script to be used for this build.')
    opt.add_option('--no_magic', dest='no_magic', action='store_true', default=False,
                   help='Don\'t use linker magic to enable wx libs to be bundled with '
                   'wxPython.  See build.py for more info.')
    opt.add_option('--mac_arch', dest='mac_arch', default='', action='store',
                   help='One or more comma separated architecture names to be used for '
                   'the Mac builds. Should be at least a subset of the architectures '
                   'used by wxWidgets and Python')
    opt.add_option('--msvc_arch', dest='msvc_arch', default='x86', action='store',
                   help='The architecture to target for MSVC builds. Supported values '
                   'are: "x86" or "x64"')
    #opt.add_option('--msvc_ver', dest='msvc_ver', default='9.0', action='store',
    #               help='The MSVC version to use for the build, if multiple versions are '
    #               'installed. Currently supported values are: "9.0" or "10.0"')

    # TODO: The waf msvc tool has --msvc_version and --msvc_target options
    # already. We should just switch to those instead of adding our own
    # option names...

    opt.add_option('--msvc_relwithdebug', dest='msvc_relwithdebug', action='store_true', default=False,
                   help='Turn on debug info for release builds for MSVC builds.')



def configure(conf):    
    if isWindows:        
        # For now simply choose the compiler version based on the Python
        # version. We have a chicken-egg problem here. The compiler needs to
        # be selected before the Python stuff can be configured, but we need
        # Python to know what version of the compiler to use.
        # TODO: Fix this
        msvc_version = '9.0' #conf.options.msvc_ver
        if conf.options.python and '33' in conf.options.python:
            msvc_version = '10.0'

        conf.env['MSVC_VERSIONS'] = ['msvc ' + msvc_version]
        conf.env['MSVC_TARGETS'] = [conf.options.msvc_arch]
        conf.load('msvc')
    else:
        conf.load('compiler_cc compiler_cxx')

    if conf.options.python:
        conf.env.PYTHON = conf.options.python
    conf.load('python')
    conf.check_python_version(minver=(2,7,0))
    if isWindows:
        # Search for the Python headers without doing some stuff that could
        # iccorectly fail on Windows. See my_check_python_headers below.
        conf.my_check_python_headers()  
    else:
        conf.check_python_headers()

    # fetch and save the debug option
    conf.env.debug = conf.options.debug

    # Ensure that the headers in siplib and Phoenix's src dir can be found
    conf.env.INCLUDES_WXPY = ['sip/siplib', 'src']

    if isWindows:
        # Windows/MSVC specific stuff

        cfg.finishSetup(debug=conf.env.debug)

        conf.env.INCLUDES_WX = cfg.includes
        conf.env.DEFINES_WX = cfg.wafDefines
        conf.env.CFLAGS_WX = cfg.cflags
        conf.env.CXXFLAGS_WX = cfg.cflags
        conf.env.LIBPATH_WX = cfg.libdirs
        conf.env.LIB_WX = cfg.libs
        conf.env.LIBFLAGS_WX = cfg.lflags

        _copyEnvGroup(conf.env, '_WX', '_WXADV')
        conf.env.LIB_WXADV += cfg.makeLibName('adv')

        _copyEnvGroup(conf.env, '_WX', '_WXSTC')
        conf.env.LIB_WXSTC += cfg.makeLibName('stc')

        _copyEnvGroup(conf.env, '_WX', '_WXHTML')
        conf.env.LIB_WXHTML += cfg.makeLibName('html')

        _copyEnvGroup(conf.env, '_WX', '_WXGL')
        conf.env.LIB_WXGL += cfg.makeLibName('gl')

        _copyEnvGroup(conf.env, '_WX', '_WXWEBVIEW')
        conf.env.LIB_WXWEBVIEW += cfg.makeLibName('webview')

        _copyEnvGroup(conf.env, '_WX', '_WXXML')
        conf.env.LIB_WXXML += cfg.makeLibName('xml', isMSWBase=True)

        _copyEnvGroup(conf.env, '_WX', '_WXXRC')
        conf.env.LIB_WXXRC += cfg.makeLibName('xrc')

        _copyEnvGroup(conf.env, '_WX', '_WXRICHTEXT')
        conf.env.LIB_WXRICHTEXT += cfg.makeLibName('richtext')

        # ** Add code for new modules here (and below for non-MSW)

        # tweak the PYEXT compile and link flags if making a --debug build
        if conf.env.debug:
            for listname in ['CFLAGS_PYEXT', 'CXXFLAGS_PYEXT']:
                lst = conf.env[listname]
                for opt in '/Ox /MD /DNDEBUG'.split():
                    try:
                        lst.remove(opt)
                    except ValueError:
                        pass
                lst[1:1] = '/Od /MDd /Z7 /D_DEBUG'.split()

            conf.env['LINKFLAGS_PYEXT'].append('/DEBUG')
            conf.env['LIB_PYEXT'][0] += '_d'

        # And similar tweaks for non-debug builds with the relwithdebug flag
        # turned on.
        elif conf.options.msvc_relwithdebug:
            for listname in ['CFLAGS_PYEXT', 'CXXFLAGS_PYEXT']:
                lst = conf.env[listname]
                lst[1:1] = ['/Z7']
            conf.env['LINKFLAGS_PYEXT'].append('/DEBUG')

    else: 
        # Configuration stuff for non-Windows ports using wx-config
        conf.env.CFLAGS_WX   = list()
        conf.env.CXXFLAGS_WX = list()
        conf.env.CFLAGS_WXPY   = list()
        conf.env.CXXFLAGS_WXPY = list()

        # finish configuring the Config object
        conf.env.wx_config = conf.options.wx_config
        cfg.finishSetup(conf.env.wx_config, conf.env.debug)

        # Check wx-config exists and fetch some values from it
        rpath = ' --no-rpath' if not conf.options.no_magic else ''
        conf.check_cfg(path=conf.options.wx_config, package='', 
                       args='--cxxflags --libs core,net' + rpath, 
                       uselib_store='WX', mandatory=True)

        # Run it again with different libs options to get different
        # sets of flags stored to use with varous extension modules below.
        conf.check_cfg(path=conf.options.wx_config, package='', 
                       args='--cxxflags --libs adv,core,net' + rpath, 
                       uselib_store='WXADV', mandatory=True)

        libname = '' if cfg.MONOLITHIC else 'stc,' # workaround bug in wx-config
        conf.check_cfg(path=conf.options.wx_config, package='', 
                       args=('--cxxflags --libs %score,net' % libname) + rpath, 
                       uselib_store='WXSTC', mandatory=True)

        conf.check_cfg(path=conf.options.wx_config, package='', 
                       args='--cxxflags --libs html,core,net' + rpath, 
                       uselib_store='WXHTML', mandatory=True)

        conf.check_cfg(path=conf.options.wx_config, package='', 
                       args='--cxxflags --libs gl,core,net' + rpath, 
                       uselib_store='WXGL', mandatory=True)

        conf.check_cfg(path=conf.options.wx_config, package='', 
                       args='--cxxflags --libs webview,core,net' + rpath, 
                       uselib_store='WXWEBVIEW', mandatory=True)

        if isDarwin:
            conf.check_cfg(path=conf.options.wx_config, package='', 
                           args='--cxxflags --libs core,net' + rpath, 
                           uselib_store='WXWEBKIT', mandatory=True)

        conf.check_cfg(path=conf.options.wx_config, package='', 
                       args='--cxxflags --libs xml,core,net' + rpath, 
                       uselib_store='WXXML', mandatory=True)

        conf.check_cfg(path=conf.options.wx_config, package='', 
                       args='--cxxflags --libs xrc,xml,core,net' + rpath, 
                       uselib_store='WXXRC', mandatory=True)

        libname = '' if cfg.MONOLITHIC else 'richtext,' # workaround bug in wx-config
        conf.check_cfg(path=conf.options.wx_config, package='', 
                       args='--cxxflags --libs %score,net' % libname + rpath, 
                       uselib_store='WXRICHTEXT', mandatory=True)

        # ** Add code for new modules here


        # NOTE: This assumes that if the platform is not win32 (from
        # the test above) and not darwin then we must be using the
        # GTK2 port of wxWidgets.  If we ever support other ports then
        # this code will need to be adjusted.
        if not isDarwin:
            gtkflags = os.popen('pkg-config gtk+-2.0 --cflags', 'r').read()[:-1]
            conf.env.CFLAGS_WX   += gtkflags.split()
            conf.env.CXXFLAGS_WX += gtkflags.split()

        # clear out Python's default NDEBUG and make sure it is undef'd too just in case
        if 'NDEBUG' in conf.env.DEFINES_PYEXT:
            conf.env.DEFINES_PYEXT.remove('NDEBUG')
        conf.env.CFLAGS_WXPY.append('-UNDEBUG')
        conf.env.CXXFLAGS_WXPY.append('-UNDEBUG')

        # Add basic debug info for all builds
        conf.env.CFLAGS_WXPY.append('-g')
        conf.env.CXXFLAGS_WXPY.append('-g')

        # And if --debug is set turn on more detailed debug info and turn off optimization
        if conf.env.debug:
            conf.env.CFLAGS_WXPY.extend(['-ggdb', '-O0'])
            conf.env.CXXFLAGS_WXPY.extend(['-ggdb', '-O0'])

        # Remove some compile flags we don't care about, ones that we may be
        # replacing ourselves anyway, or ones which may have duplicates.
        flags = ['CFLAGS_PYEXT',    'CXXFLAGS_PYEXT',    'LINKFLAGS_PYEXT',
                 'CFLAGS_cshlib',   'CXXFLAGS_cshlib',   'LINKFLAGS_cshlib',
                 'CFLAGS_cxxshlib', 'CXXFLAGS_cxxshlib', 'LINKFLAGS_cxxshlib']
        for key in flags:
            _cleanFlags(conf, key)


        # Use the same compilers that wxWidgets used
        if cfg.CC:
            conf.env.CC = cfg.CC.split()
        if cfg.CXX:
            conf.env.CXX = cfg.CXX.split()


        # Some Mac-specific stuff
        if isDarwin:
            conf.env.MACOSX_DEPLOYMENT_TARGET = "10.5"  

            if conf.options.mac_arch:
                conf.env.ARCH_WXPY = conf.options.mac_arch.split(',')        

    #import pprint
    #pprint.pprint( [(k, conf.env[k]) for k in conf.env.keys()] )



#
# This is a copy of WAF's check_python_headers with some problematic stuff ripped out.
#
from waflib.Configure import conf

@conf
def my_check_python_headers(conf):
    """
    Check for headers and libraries necessary to extend or embed python by using the module *distutils*.
    On success the environment variables xxx_PYEXT and xxx_PYEMBED are added:

    * PYEXT: for compiling python extensions
    * PYEMBED: for embedding a python interpreter
    """

    env = conf.env
    if not env['CC_NAME'] and not env['CXX_NAME']:
        conf.fatal('load a compiler first (gcc, g++, ..)')

    if not env['PYTHON_VERSION']:
        conf.check_python_version()

    pybin = conf.env.PYTHON
    if not pybin:
        conf.fatal('Could not find the python executable')

    v = 'prefix SO LDFLAGS LIBDIR LIBPL INCLUDEPY Py_ENABLE_SHARED MACOSX_DEPLOYMENT_TARGET LDSHARED CFLAGS'.split()
    try:
        lst = conf.get_python_variables(["get_config_var('%s') or ''" % x for x in v])
    except RuntimeError:
        conf.fatal("Python development headers not found (-v for details).")

    vals = ['%s = %r' % (x, y) for (x, y) in zip(v, lst)]
    conf.to_log("Configuration returned from %r:\n%r\n" % (pybin, '\n'.join(vals)))

    dct = dict(zip(v, lst))
    x = 'MACOSX_DEPLOYMENT_TARGET'
    if dct[x]:
        conf.env[x] = conf.environ[x] = dct[x]

    env['pyext_PATTERN'] = '%s' + dct['SO'] # not a mistake

    # Check for python libraries for embedding
    all_flags = dct['LDFLAGS'] + ' ' + dct['CFLAGS']
    conf.parse_flags(all_flags, 'PYEMBED')

    all_flags = dct['LDFLAGS'] + ' ' + dct['LDSHARED'] + ' ' + dct['CFLAGS']
    conf.parse_flags(all_flags, 'PYEXT')

    if isWindows:
        libname = 'python' + conf.env['PYTHON_VERSION'].replace('.', '')
        
        # TODO: libpath will be incorrect in virtualenv's.  Fix this...
        libpath = [os.path.join(dct['prefix'], "libs")]       
        
        conf.env['LIBPATH_PYEMBED'] = libpath
        conf.env.append_value('LIB_PYEMBED', [libname])
        conf.env['LIBPATH_PYEXT'] = conf.env['LIBPATH_PYEMBED']
        conf.env['LIB_PYEXT'] = conf.env['LIB_PYEMBED']
       
    else:
        result = None
        for name in ('python' + env['PYTHON_VERSION'], 'python' + env['PYTHON_VERSION'].replace('.', '')):
    
            # LIBPATH_PYEMBED is already set; see if it works.
            if not result and env['LIBPATH_PYEMBED']:
                path = env['LIBPATH_PYEMBED']
                conf.to_log("\n\n# Trying default LIBPATH_PYEMBED: %r\n" % path)
                result = conf.check(lib=name, uselib='PYEMBED', libpath=path, mandatory=False, msg='Checking for library %s in LIBPATH_PYEMBED' % name)
    
            if not result and dct['LIBDIR']:
                path = [dct['LIBDIR']]
                conf.to_log("\n\n# try again with -L$python_LIBDIR: %r\n" % path)
                result = conf.check(lib=name, uselib='PYEMBED', libpath=path, mandatory=False, msg='Checking for library %s in LIBDIR' % name)
    
            if not result and dct['LIBPL']:
                path = [dct['LIBPL']]
                conf.to_log("\n\n# try again with -L$python_LIBPL (some systems don't install the python library in $prefix/lib)\n")
                result = conf.check(lib=name, uselib='PYEMBED', libpath=path, mandatory=False, msg='Checking for library %s in python_LIBPL' % name)
    
            if not result:
                path = [os.path.join(dct['prefix'], "libs")]
                conf.to_log("\n\n# try again with -L$prefix/libs, and pythonXY name rather than pythonX.Y (win32)\n")
                result = conf.check(lib=name, uselib='PYEMBED', libpath=path, mandatory=False, msg='Checking for library %s in $prefix/libs' % name)
    
            if result:
                break # do not forget to set LIBPATH_PYEMBED
    
        if result:
            env['LIBPATH_PYEMBED'] = path
            env.append_value('LIB_PYEMBED', [name])
        else:
            conf.to_log("\n\n### LIB NOT FOUND\n")


    conf.to_log("Include path for Python extensions "
                "(found via distutils module): %r\n" % (dct['INCLUDEPY'],))
    env['INCLUDES_PYEXT'] = [dct['INCLUDEPY']]
    env['INCLUDES_PYEMBED'] = [dct['INCLUDEPY']]

    # Code using the Python API needs to be compiled with -fno-strict-aliasing
    if env['CC_NAME'] == 'gcc':
        env.append_value('CFLAGS_PYEMBED', ['-fno-strict-aliasing'])
        env.append_value('CFLAGS_PYEXT', ['-fno-strict-aliasing'])
    if env['CXX_NAME'] == 'gcc':
        env.append_value('CXXFLAGS_PYEMBED', ['-fno-strict-aliasing'])
        env.append_value('CXXFLAGS_PYEXT', ['-fno-strict-aliasing'])

    if env.CC_NAME == "msvc":
        from distutils.msvccompiler import MSVCCompiler
        dist_compiler = MSVCCompiler()
        dist_compiler.initialize()
        env.append_value('CFLAGS_PYEXT', dist_compiler.compile_options)
        env.append_value('CXXFLAGS_PYEXT', dist_compiler.compile_options)
        env.append_value('LINKFLAGS_PYEXT', dist_compiler.ldflags_shared)



#-----------------------------------------------------------------------------
# Build command

def build(bld):
    # Ensure that the directory containing this script is on the python
    # path for spawned commands so the builder and phoenix packages can be
    # found.
    thisdir = os.path.abspath(".")
    sys.path.insert(0, thisdir)

    from distutils.file_util import copy_file
    from distutils.dir_util  import mkpath
    from distutils.dep_util  import newer, newer_group
    from buildtools.config   import opj, loadETG, getEtgSipCppFiles

    cfg.finishSetup(bld.env.wx_config)

    # update the license files
    mkpath('license')
    for filename in ['preamble.txt', 'licence.txt', 'licendoc.txt', 'lgpl.txt']:
        copy_file(opj(cfg.WXDIR, 'docs', filename), opj('license',filename), update=1, verbose=1)

    # create the package's __version__ module
    open(opj(cfg.PKGDIR, '__version__.py'), 'w').write(
        "# This file was generated by Phoenix's wscript.\n\n"
        "VERSION_STRING    = '%(VERSION)s'\n"
        "MAJOR_VERSION     = %(VER_MAJOR)s\n"
        "MINOR_VERSION     = %(VER_MINOR)s\n"
        "RELEASE_NUMBER    = %(VER_RELEASE)s\n\n"
        "VERSION = (MAJOR_VERSION, MINOR_VERSION, RELEASE_NUMBER, '%(VER_FLAGS)s')\n"
        % cfg.__dict__)
    # and one for the demo folder too
    open('demo/version.py', 'w').write(
        "# This file was generated by Phoenix's wscript.\n\n"
        "VERSION_STRING = '%(VERSION)s'\n"
        % cfg.__dict__)
        

    # copy the wx locale message catalogs to the package dir
    if isWindows or isDarwin:
        cfg.build_locale_dir(opj(cfg.PKGDIR, 'locale'))

    # copy __init__.py
    copy_file('src/__init__.py', cfg.PKGDIR, update=1, verbose=1)


    # Create the build tasks for each of our extension modules.
    siplib = bld(
        features = 'c cxx cshlib cxxshlib pyext',
        target   = makeTargetName(bld, 'siplib'),
        source   = ['sip/siplib/apiversions.c',
                    'sip/siplib/bool.cpp',
                    'sip/siplib/descriptors.c',
                    'sip/siplib/objmap.c',
                    'sip/siplib/qtlib.c',
                    'sip/siplib/siplib.c',
                    'sip/siplib/threads.c',
                    'sip/siplib/voidptr.c',
                    ],
        uselib   = 'WX WXPY',
    )  
    makeExtCopyRule(bld, 'siplib')


    etg = loadETG('etg/_core.py')
    rc = ['src/wxc.rc'] if isWindows else []
    bld(features = 'c cxx cxxshlib pyext',
        target   = makeTargetName(bld, '_core'),
        source   = getEtgSipCppFiles(etg) + rc,
        uselib   = 'WX WXPY',
        )
    makeExtCopyRule(bld, '_core')


    etg = loadETG('etg/_adv.py')
    bld(features = 'c cxx cxxshlib pyext',
        target   = makeTargetName(bld, '_adv'),
        source   = getEtgSipCppFiles(etg) + rc,
        uselib   = 'WXADV WXPY',
        )
    makeExtCopyRule(bld, '_adv')


    etg = loadETG('etg/_dataview.py')
    bld(features = 'c cxx cxxshlib pyext',
        target   = makeTargetName(bld, '_dataview'),
        source   = getEtgSipCppFiles(etg) + rc,
        uselib   = 'WXADV WXPY',    # dataview classes are also in the adv library
        )
    makeExtCopyRule(bld, '_dataview')


    etg = loadETG('etg/_grid.py')
    bld(features = 'c cxx cxxshlib pyext',
        target   = makeTargetName(bld, '_grid'),
        source   = getEtgSipCppFiles(etg) + rc,
        uselib   = 'WXADV WXPY',    # grid classes are also in the adv library
        )
    makeExtCopyRule(bld, '_grid')


    etg = loadETG('etg/_stc.py')
    bld(features = 'c cxx cxxshlib pyext',
        target   = makeTargetName(bld, '_stc'),
        source   = getEtgSipCppFiles(etg) + rc,
        uselib   = 'WXSTC WXPY',
        )
    makeExtCopyRule(bld, '_stc')


    etg = loadETG('etg/_html.py')
    bld(features = 'c cxx cxxshlib pyext',
        target   = makeTargetName(bld, '_html'),
        source   = getEtgSipCppFiles(etg) + rc,
        uselib   = 'WXHTML WXPY',
        )
    makeExtCopyRule(bld, '_html')


    etg = loadETG('etg/_glcanvas.py')
    bld(features = 'c cxx cxxshlib pyext',
        target   = makeTargetName(bld, '_glcanvas'),
        source   = getEtgSipCppFiles(etg) + rc,
        uselib   = 'WXGL WXPY',
        )
    makeExtCopyRule(bld, '_glcanvas')


    etg = loadETG('etg/_html2.py')
    bld(features = 'c cxx cxxshlib pyext',
        target   = makeTargetName(bld, '_html2'),
        source   = getEtgSipCppFiles(etg) + rc,
        uselib   = 'WXWEBVIEW WXPY',
        )
    makeExtCopyRule(bld, '_html2')

    if isDarwin:
        etg = loadETG('etg/_webkit.py')
        bld(features = 'c cxx cxxshlib pyext',
            target   = makeTargetName(bld, '_webkit'),
            source   = getEtgSipCppFiles(etg) + rc,
            uselib   = 'WXWEBKIT WXPY',
            )
        makeExtCopyRule(bld, '_webkit')

    etg = loadETG('etg/_xml.py')
    bld(features = 'c cxx cxxshlib pyext',
        target   = makeTargetName(bld, '_xml'),
        source   = getEtgSipCppFiles(etg) + rc,
        uselib   = 'WXXML WXPY',
        )
    makeExtCopyRule(bld, '_xml')


    etg = loadETG('etg/_xrc.py')
    bld(features = 'c cxx cxxshlib pyext',
        target   = makeTargetName(bld, '_xrc'),
        source   = getEtgSipCppFiles(etg) + rc,
        uselib   = 'WXXRC WXPY',
        )
    makeExtCopyRule(bld, '_xrc')


    etg = loadETG('etg/_richtext.py')
    bld(features = 'c cxx cxxshlib pyext',
        target   = makeTargetName(bld, '_richtext'),
        source   = getEtgSipCppFiles(etg) + rc,
        uselib   = 'WXHTML WXRICHTEXT WXPY',
        )
    makeExtCopyRule(bld, '_richtext')



    # ** Add code for new modules here


#-----------------------------------------------------------------------------
# helpers

# Remove some unwanted flags from the given key in the context's environment
def _cleanFlags(ctx, key):
    cleaned = list()
    skipnext = False
    for idx, flag in enumerate(ctx.env[key]):
        if flag in ['-arch', '-isysroot', '-compatibility_version', '-current_version']:
            skipnext = True  # implicitly skips this one too
        elif not skipnext:
            cleaned.append(flag)
        else:
            skipnext = False
    ctx.env[key] = cleaned


def makeTargetName(bld, name):
    if isWindows and bld.env.debug:
        name += '_d'
    return name


# Make a rule that will copy a built extension module to the in-place package
# dir so we can test locally without doing an install.
def makeExtCopyRule(bld, name):
    name = makeTargetName(bld, name)
    src = bld.env.pyext_PATTERN % name
    tgt = 'pkg.%s' % name  # just a name to be touched to serve as a timestamp of the copy
    bld(rule=copyFileToPkg, source=src, target=tgt, after=name)


# This is the task function to be called by the above rule.
def copyFileToPkg(task): 
    from distutils.file_util import copy_file
    from buildtools.config   import opj
    src = task.inputs[0].abspath() 
    tgt = task.outputs[0].abspath() 
    task.exec_command('touch %s' % tgt)
    tgt = opj(cfg.PKGDIR, os.path.basename(src))
    copy_file(src, tgt, verbose=1)
    return 0


# Copy all the items in env with a matching postfix to a similarly
# named item with the dest postfix.
def _copyEnvGroup(env, srcPostfix, destPostfix):
    import copy
    for key in env.keys():
        if key.endswith(srcPostfix):
            newKey = key[:-len(srcPostfix)] + destPostfix
            env[newKey] = copy.copy(env[key])

#-----------------------------------------------------------------------------
