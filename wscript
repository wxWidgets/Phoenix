#!/usr/bin/python
#-----------------------------------------------------------------------------
#  WAF script for building and installing the wxPython extension modules.
#
# Author:      Robin Dunn
# Copyright:   (c) 2013-2020 by Total Control Software
# License:     wxWindows License
#-----------------------------------------------------------------------------

import sys
import os
import setuptools

try:
    from textwrap import indent
except ImportError:
    from buildtools.backports.textwrap3 import indent

from buildtools.config import Config, runcmd, msg
cfg = Config(True)

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
        opt.load('compiler_c compiler_cxx')
    opt.load('python')

    opt.add_option('--debug', dest='debug', action='store_true', default=False,
                   help='Turn on debugger-related compile options.')
    opt.add_option('--python', dest='python', default='', action='store',
                   help='Full path to the Python executable to use.')
    opt.add_option('--wx_config', dest='wx_config', default='wx-config', action='store',
                   help='Full path to the wx-config script to be used for this build.')
    opt.add_option('--no_magic', dest='no_magic', action='store_true', default=False,
                   help='Don\'t use linker magic to enable wx libs to be bundled with '
                   'wxPython.  See build.py for more info.')
    opt.add_option('--mac_arch', dest='mac_arch', default='', action='store',
                   help='One or more comma separated architecture names to be used for '
                   'the Mac builds. Should be at least a subset of the architectures '
                   'used by wxWidgets and Python')
    opt.add_option('--gtk2', dest='gtk2', action='store_true', default=False,
                   help='On Linux build for gtk2 (default gtk3)')
    opt.add_option('--gtk3', dest='gtk3', action='store_true', default=True,
                   help='On Linux build for gtk3')
    opt.add_option('--msvc_arch', dest='msvc_arch', default='x86', action='store',
                   help='The architecture to target for MSVC builds. Supported values '
                   'are: "x86" or "x64"')
    opt.add_option('--msvc_relwithdebug', dest='msvc_relwithdebug', action='store_true', default=False,
                   help='Turn on debug info for release builds for MSVC builds.')



def configure(conf):
    if isWindows:
        # For now simply choose the compiler version based on the Python
        # version. We have a chicken-egg problem here. The compiler needs to
        # be selected before the Python stuff can be configured, but we need
        # Python to know what version of the compiler to use.
        import distutils.msvc9compiler
        msvc_version = str( distutils.msvc9compiler.get_build_version() )

        # When building for Python 3.7 the msvc_version returned will be
        # "14.1" as that is the version of the BasePlatformToolkit that stock
        # Python 3.7 was built with, a.k.a v141, which is the default in
        # Visual Studio 2017. However, waf is using "msvc 15.0" to designate
        # that version rather than "14.1" so we'll need to catch that case and
        # fix up the msvc_version accordingly.
        if msvc_version in ["14.1", "14.2"] and sys.version_info >= (3,7):
            ##msvc_version = '15.0'

            # On the other hand, microsoft says that v141 and v140 (Visual
            # Studio 2015) are binary compatible, so for now let's just drop
            # it back to "14.0" until I get all the details worked out for
            # using VS 2017 everywhere for Python 3.7+.
            msvc_version = '14.0'

        # In some cases (Azure DevOps at least) we're getting "14.1" for Python
        # 3.6 too. Smash it down to '14.0'
        if msvc_version == "14.1" and sys.version_info[:2] == (3,6):
            msvc_version = '14.0'

        conf.env['MSVC_VERSIONS'] = ['msvc ' + msvc_version]
        conf.env['MSVC_TARGETS'] = [conf.options.msvc_arch]
        conf.load('msvc')
    else:
        conf.load('compiler_c compiler_cxx')

    if conf.options.python:
        conf.env.PYTHON = conf.options.python
    conf.load('python')
    conf.check_python_version(minver=(2,7,0))
    if isWindows:
        # Search for the Python headers without doing some stuff that could
        # incorrectly fail on Windows. See my_check_python_headers below.
        # TODO: Check if it can/should be used on other platforms too.
        conf.my_check_python_headers()
    else:
        conf.check_python_headers(features='pyext')

    # fetch and save the debug options
    conf.env.debug = conf.options.debug
    conf.env.msvc_relwithdebug = conf.options.msvc_relwithdebug

    # Ensure that the headers in siplib and Phoenix's src dir can be found
    conf.env.INCLUDES_WXPY = ['sip/siplib', 'wx/include', 'src']

    if isWindows:
        # Windows/MSVC specific stuff

        cfg.finishSetup(debug=conf.env.debug)

        conf.env.INCLUDES_WX = cfg.includes
        conf.env.DEFINES_WX = cfg.wafDefines
        conf.env.CFLAGS = cfg.cflags
        conf.env.CXXFLAGS = cfg.cxxflags
        conf.env.CFLAGS_WX = list()
        conf.env.CXXFLAGS_WX = list()
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
        conf.env.LIB_WXRICHTEXT += cfg.makeLibName('adv')

        _copyEnvGroup(conf.env, '_WX', '_WXMEDIA')
        conf.env.LIB_WXMEDIA += cfg.makeLibName('media')

        _copyEnvGroup(conf.env, '_WX', '_WXRIBBON')
        conf.env.LIB_WXRIBBON += cfg.makeLibName('ribbon')

        _copyEnvGroup(conf.env, '_WX', '_WXPROPGRID')
        conf.env.LIB_WXPROPGRID += cfg.makeLibName('propgrid')

        _copyEnvGroup(conf.env, '_WX', '_WXAUI')
        conf.env.LIB_WXAUI += cfg.makeLibName('aui')

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
                # NOTE: For --debug builds the /Z7 flag is used so the debug
                # info will be in each object file instead of a separate PDB
                # file. This will result in much faster builds since VC won't
                # have to serialize access to the .pdb file. OTOH, separate
                # PDB files are generated for the --msvc_relwithdebug option,
                # which is handled below in the makeETGRule() function.
                lst[1:1] = '/Od /MDd /Z7 /D_DEBUG'.split()

            conf.env['LINKFLAGS_PYEXT'].append('/DEBUG')
            conf.env['LIB_PYEXT'][0] += '_d'


    else: # not isWindows
        # TODO: Double-check that this works when using an installed wxWidgets
        wxConfigDir = cfg.findWxConfigDir(conf.options.wx_config)

        # Configuration stuff for non-Windows ports using wx-config
        # First finish configuring the Config object
        conf.env.wx_config = conf.options.wx_config
        cfg.finishSetup(conf.env.wx_config, conf.env.debug)

        conf.env.CFLAGS = cfg.cflags[:]
        conf.env.CXXFLAGS = cfg.cxxflags[:]
        conf.env.CFLAGS_WX = list()
        conf.env.CXXFLAGS_WX = list()
        conf.env.CFLAGS_WXPY = list()
        conf.env.CXXFLAGS_WXPY = list()

        # Check wx-config exists and fetch some values from it
        rpath = ' --no-rpath' if not conf.options.no_magic else ''
        conf.check_cfg(path=conf.options.wx_config, package='',
                       args='--cxxflags --libs core,net' + rpath,
                       uselib_store='WX', mandatory=True,
                       msg='Finding libs for WX')

        # Run it again with different libs options to get different
        # sets of flags stored to use with varous extension modules below.
        conf.check_cfg(path=conf.options.wx_config, package='',
                       args='--cxxflags --libs adv,core,net' + rpath,
                       uselib_store='WXADV', mandatory=True,
                       msg='Finding libs for WXADV')

        libname = '' if cfg.MONOLITHIC else 'stc,' # workaround bug in wx-config
        conf.check_cfg(path=conf.options.wx_config, package='',
                       args=('--cxxflags --libs %score,net' % libname) + rpath,
                       uselib_store='WXSTC', mandatory=True,
                       msg='Finding libs for WXSTC')

        conf.check_cfg(path=conf.options.wx_config, package='',
                       args='--cxxflags --libs html,core,net' + rpath,
                       uselib_store='WXHTML', mandatory=True,
                       msg='Finding libs for WXHTML')

        if cfg.checkSetup(wxConfigDir, 'wxUSE_GLCANVAS'):
            gl_libs = '--libs gl,core,net'
        else:
            gl_libs = '--libs core,net'
        conf.check_cfg(path=conf.options.wx_config, package='',
                       args='--cxxflags ' + gl_libs + rpath,
                       uselib_store='WXGL', mandatory=True,
                       msg='Finding libs for WXGL')

        if cfg.checkSetup(wxConfigDir, 'wxUSE_WEBVIEW'):
            wv_libs = '--libs webview,core,net'
        else:
            wv_libs = '--libs core,net'
        conf.check_cfg(path=conf.options.wx_config, package='',
                       args='--cxxflags ' + wv_libs + rpath,
                       uselib_store='WXWEBVIEW', mandatory=True,
                       msg='Finding libs for WXWEBVIEW')

        if isDarwin:
            conf.check_cfg(path=conf.options.wx_config, package='',
                           args='--cxxflags --libs core,net' + rpath,
                           uselib_store='WXWEBKIT', mandatory=True,
                           msg='Finding libs for WXWEBKIT')

        conf.check_cfg(path=conf.options.wx_config, package='',
                       args='--cxxflags --libs xml,core,net' + rpath,
                       uselib_store='WXXML', mandatory=True,
                       msg='Finding libs for WXXML')

        conf.check_cfg(path=conf.options.wx_config, package='',
                       args='--cxxflags --libs xrc,xml,core,net' + rpath,
                       uselib_store='WXXRC', mandatory=True,
                       msg='Finding libs for WXXRC')

        libname = '' if cfg.MONOLITHIC else 'richtext,' # workaround bug in wx-config
        conf.check_cfg(path=conf.options.wx_config, package='',
                       args='--cxxflags --libs %score,net' % libname + rpath,
                       uselib_store='WXRICHTEXT', mandatory=True,
                       msg='Finding libs for WXRICHTEXT')

        if cfg.checkSetup(wxConfigDir, 'wxUSE_MEDIACTRL'):
            mc_libs = '--libs media,core,net'
        else:
            mc_libs = '--libs core,net'
        conf.check_cfg(path=conf.options.wx_config, package='',
                       args='--cxxflags ' + mc_libs + rpath,
                       uselib_store='WXMEDIA', mandatory=True,
                       msg='Finding libs for WXMEDIA')

        conf.check_cfg(path=conf.options.wx_config, package='',
                       args='--cxxflags --libs ribbon,core,net' + rpath,
                       uselib_store='WXRIBBON', mandatory=True,
                       msg='Finding libs for WXRIBBON')

        conf.check_cfg(path=conf.options.wx_config, package='',
                       args='--cxxflags --libs propgrid,core' + rpath,
                       uselib_store='WXPROPGRID', mandatory=True,
                       msg='Finding libs for WXPROPGRID')

        conf.check_cfg(path=conf.options.wx_config, package='',
                       args='--cxxflags --libs aui,core' + rpath,
                       uselib_store='WXAUI', mandatory=True,
                       msg='Finding libs for WXAUI')

        # ** Add code for new modules here


        # NOTE: This assumes that if the platform is not win32 (from the test
        # above) and not darwin then we must be using the GTK2 or GTK3 port of
        # wxWidgets.  If we ever support other ports then this code will need
        # to be adjusted.
        if not isDarwin:
            if conf.options.gtk2:
                conf.options.gtk3 = False
            if conf.options.gtk2:
                gtkflags = os.popen('pkg-config gtk+-2.0 --cflags', 'r').read()[:-1]
            else:
                gtkflags = os.popen('pkg-config gtk+-3.0 --cflags', 'r').read()[:-1]

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
            for flags in [conf.env.CFLAGS_PYEXT, conf.env.CXXFLAGS_PYEXT]:
                flags.extend(['-ggdb', '-O0'])

        # Remove some compile flags we don't care about, ones that we may be
        # replacing ourselves anyway, or ones which may have duplicates.
        flags = ['CFLAGS_PYEXT',    'CXXFLAGS_PYEXT',    'LINKFLAGS_PYEXT',
                 'CFLAGS_cshlib',   'CXXFLAGS_cshlib',   'LINKFLAGS_cshlib',
                 'CFLAGS_cxxshlib', 'CXXFLAGS_cxxshlib', 'LINKFLAGS_cxxshlib']
        for key in flags:
            _cleanFlags(conf, key)

        # Waf 2 is now calling pythonX.Y-config for fetching libs and flags,
        # and it may be outputting flags that will cause an explicit link to
        # Python's lib, which we don't want as that could tie us to that
        # specific Python instance instead of the one that is loading the
        # wxPython extension modules. That's okay for PYEMBED but not for PYEXT
        # configs.
        conf.env.LIBPATH_PYEXT = []
        conf.env.LIB_PYEXT = []


        # Use the same compilers that wxWidgets used
        if cfg.CC:
            conf.env.CC = cfg.CC.split()
        if cfg.CXX:
            conf.env.CXX = cfg.CXX.split()
        if cfg.LDSHARED:
            conf.env.LINK_CC = cfg.LDSHARED.split()
            conf.env.LINK_CXX = cfg.LDSHARED.split()

        # Some Mac-specific stuff
        if isDarwin:
            conf.env.MACOSX_DEPLOYMENT_TARGET = "10.10"

            if conf.options.mac_arch:
                conf.env.ARCH_WXPY = conf.options.mac_arch.split(',')

    # import pprint
    # pprint.pprint( [(k, conf.env[k]) for k in conf.env.keys()] )
    # sys.exit(0)


#
# This is a copy of WAF's check_python_headers with some problematic stuff ripped out.
#
from waflib.Configure import conf

@conf
def my_check_python_headers(conf):
    """
    Check for headers and libraries necessary to extend or embed python by
    using the module *distutils*. On success the environment variables
    xxx_PYEXT and xxx_PYEMBED are added:

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

        if dct['LIBDIR'] and os.path.isdir(dct['LIBDIR']):
            libpath = [dct['LIBDIR']]
        else:
            base_prefix = get_windows_base_prefix(conf, dct['prefix'])
            libpath = [os.path.join(base_prefix, "libs")]

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


def get_windows_base_prefix(conf, default):
    # If the python being used for the build in running from a virtual
    # environment then sys.prefix will not be the correct path to find
    # the Python libs folder.
    import waflib.Errors

    # If we're running in a Py3 style venv then there is a
    # sys.base_prefix we can use instead.
    try:
        base_prefix = conf.get_python_variables(
            ["base_prefix"],
            ["import sys",
             "base_prefix = getattr(sys, 'base_prefix')"])[0]
        return base_prefix
    except waflib.Errors.WafError:
        pass

    # Otherwise try importing a python library module that should
    # always be in the Lib folder (at least for the versions of Python
    # we're interested in) and use it's location to figure out the
    # real prefix;
    # TODO: There has got to be a better way to do this!
    try:
        base_prefix = conf.get_python_variables(
            ["base_prefix"],
            ["import os.path as op",
             "import base64",
             "base_prefix = op.dirname(op.dirname(base64.__file__))"])[0]
        return base_prefix
    except waflib.Errors.WafError:
        pass

    return default


#-----------------------------------------------------------------------------
# Build command

def build(bld):
    # Ensure that the directory containing this script is on the python
    # sys.path for spawned commands so the builder and phoenix packages can be
    # found.
    thisdir = os.path.abspath(".")
    sys.path.insert(0, thisdir)

    from distutils.file_util import copy_file
    from buildtools.config   import opj, updateLicenseFiles

    cfg.finishSetup(bld.env.wx_config)

    if not isWindows:
        cmd = ' '.join(bld.env.CC) + ' --version'
        copmpiler = runcmd(cmd, getOutput=True, echoCmd=False)
        copmpiler = indent(copmpiler, ' '*5)
        msg("**** Compiler: {}\n{}".format(cmd, copmpiler))

    # Copy the license files from wxWidgets
    updateLicenseFiles(cfg)

    # create the package's __version__ module
    with open(opj(cfg.PKGDIR, '__version__.py'), 'w') as fid:
        fid.write("# This file was generated by wxPython's wscript.\n\n"
                  "VERSION_STRING    = '%(VERSION)s'\n"
                  "MAJOR_VERSION     = %(VER_MAJOR)s\n"
                  "MINOR_VERSION     = %(VER_MINOR)s\n"
                  "RELEASE_NUMBER    = %(VER_RELEASE)s\n"
                  "BUILD_TYPE        = '%(BUILD_TYPE)s'\n\n"
                  "VERSION = (MAJOR_VERSION, MINOR_VERSION, RELEASE_NUMBER, '%(VER_FLAGS)s')\n"
                  % cfg.__dict__)
    # and one for the demo folder too
    with open('demo/version.py', 'w') as fid:
        fid.write("# This file was generated by wxPython's wscript.\n\n"
                  "VERSION_STRING = '%(VERSION)s'\n"
                  % cfg.__dict__)


    # copy the wx locale message catalogs to the package dir
    cfg.build_locale_dir(opj(cfg.PKGDIR, 'locale'))

    # copy .py files that need to go into the root wx package dir
    for name in ['src/__init__.py', 'src/gizmos.py',]:
        copy_file(name, cfg.PKGDIR, update=1, verbose=1)

    # Copy sip's sip.h for distribution with wxPython's header
    copy_file('sip/siplib/sip.h', 'wx/include/wxPython', update=1, verbose=1)

    # Create the build tasks for each of our extension modules.
    addRelwithdebugFlags(bld, 'siplib')
    siplib = bld(
        features = 'c cxx cshlib cxxshlib pyext',
        target   = makeTargetName(bld, 'siplib'),
        source   = ['sip/siplib/apiversions.c',
                    'sip/siplib/array.c',
                    'sip/siplib/bool.cpp',
                    'sip/siplib/descriptors.c',
                    'sip/siplib/int_convertors.c',
                    'sip/siplib/objmap.c',
                    'sip/siplib/qtlib.c',
                    'sip/siplib/siplib.c',
                    'sip/siplib/threads.c',
                    'sip/siplib/voidptr.c',
                    ],
        uselib   = 'siplib WX WXPY',
    )
    makeExtCopyRule(bld, 'siplib')

    # Add build rules for each of our ETG generated extension modules
    makeETGRule(bld, 'etg/_core.py',       '_core',      'WX')
    makeETGRule(bld, 'etg/_adv.py',        '_adv',       'WXADV')
    makeETGRule(bld, 'etg/_dataview.py',   '_dataview',  'WXADV')
    makeETGRule(bld, 'etg/_grid.py',       '_grid',      'WXADV')
    makeETGRule(bld, 'etg/_stc.py',        '_stc',       'WXSTC')
    makeETGRule(bld, 'etg/_html.py',       '_html',      'WXHTML')
    makeETGRule(bld, 'etg/_glcanvas.py',   '_glcanvas',  'WXGL')
    makeETGRule(bld, 'etg/_html2.py',      '_html2',     'WXWEBVIEW')
    makeETGRule(bld, 'etg/_xml.py',        '_xml',       'WXXML')
    makeETGRule(bld, 'etg/_xrc.py',        '_xrc',       'WXXRC')
    makeETGRule(bld, 'etg/_richtext.py',   '_richtext',  'WXHTML WXRICHTEXT')
    makeETGRule(bld, 'etg/_media.py',      '_media',     'WXMEDIA')
    makeETGRule(bld, 'etg/_ribbon.py',     '_ribbon',    'WXRIBBON')
    makeETGRule(bld, 'etg/_propgrid.py',   '_propgrid',  'WXPROPGRID')
    makeETGRule(bld, 'etg/_aui.py',        '_aui',       'WXAUI')

    # Modules that are platform-specific
    if isDarwin:
        makeETGRule(bld, 'etg/_webkit.py', '_webkit',    'WXWEBKIT')
    if isWindows:
        makeETGRule(bld, 'etg/_msw.py',    '_msw',       'WX')

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
    # just a name to be touched to serve as the timestamp of the copy
    tgt = 'pkg.%s' % os.path.splitext(src)[0]
    bld(rule=copyFileToPkg, source=src, target=tgt, after=name)


# This is the task function to be called by the above rule.
def copyFileToPkg(task):
    from distutils.file_util import copy_file
    from buildtools.config   import opj
    src = task.inputs[0].abspath()
    tgt = task.outputs[0].abspath()
    open(tgt, "wb").close() # essentially just a unix 'touch' command
    tgt = opj(cfg.PKGDIR, os.path.basename(src))
    copy_file(src, tgt, verbose=1)
    if isWindows and task.env.msvc_relwithdebug:
        # also copy the .pdb file
        src = src.replace('.pyd', '.pdb')
        tgt = opj(cfg.PKGDIR, os.path.basename(src))
        copy_file(src, tgt, verbose=1)
    return 0


def simpleCopy(task):
    import shutil
    src = task.inputs[0].abspath()
    tgt = task.outputs[0].abspath()
    print("{} --> {}".format(src, tgt))
    shutil.copy(src, tgt)
    return 0


# Copy all the items in env with a matching postfix to a similarly
# named item with the dest postfix.
def _copyEnvGroup(env, srcPostfix, destPostfix):
    import copy
    for key in env.keys():
        if key.endswith(srcPostfix):
            newKey = key[:-len(srcPostfix)] + destPostfix
            env[newKey] = copy.copy(env[key])


# Make extension module build rules using info gleaned from an ETG script
def makeETGRule(bld, etgScript, moduleName, libFlags):
    from buildtools.config   import loadETG, getEtgSipCppFiles

    addRelwithdebugFlags(bld, moduleName)

    rc = []
    if isWindows:
        rc_name = moduleName + '.rc'
        bld(rule=simpleCopy,
            source='src/wxc.rc',
            target=rc_name,
            #before=moduleName+'.res'
            )
        rc = [rc_name]

    etg = loadETG(etgScript)
    bld(features='c cxx cxxshlib pyext',
        target=makeTargetName(bld, moduleName),
        source=getEtgSipCppFiles(etg) + rc,
        uselib='{} {} WXPY'.format(moduleName, libFlags),
        )
    makeExtCopyRule(bld, moduleName)


# Add flags to create .pdb files for debugging with MSVC
def addRelwithdebugFlags(bld, moduleName):
    if isWindows and bld.env.msvc_relwithdebug:
        compile_flags = ['/Zi', '/Fd_tmp_{}.pdb'.format(moduleName)]
        if sys.version_info > (3,5):
            # It looks like the /FS flag doesn't exist in the compilers used
            # by the earlier Pythons. But it also appears that it isn't needed
            # there either.  :)
            # TODO: It would be better to base this on the actual compiler being
            # used, not the Python version
            compile_flags.append('/FS')
        bld.env['CFLAGS_{}'.format(moduleName)] = compile_flags
        bld.env['CXXFLAGS_{}'.format(moduleName)] = compile_flags
        bld.env['LINKFLAGS_{}'.format(moduleName)] = ['/DEBUG']


#-----------------------------------------------------------------------------
