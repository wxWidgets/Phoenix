#----------------------------------------------------------------------
# Name:        buildtools/wxcmake.py
# Purpose:     Build the wxWidgets libraries bundled with wxPython using
#              CMake.
#
# Licence:     wxWindows license
#----------------------------------------------------------------------

import glob
import os
import re
import shlex
import shutil
import subprocess
import sys

from buildtools.config import msg

isWindows = sys.platform.startswith('win')

# Ninja Multi-Config needs 3.17 and CMAKE_MSVC_DEBUG_INFORMATION_FORMAT 3.25.
MIN_CMAKE_VERSION = (3, 25)

# The settings marked as "wx < 3.4" below work around problems fixed by
# https://github.com/wxWidgets/wxWidgets/pull/27404 and can be removed once
# ext/wxWidgets is at 3.4.0 or later.


def _fail(text):
    msg('ERROR: ' + text)
    sys.exit(1)


def _findTool(name, moduleName, dirAttr):
    """
    Find a tool on the PATH, or else in the Python package from PyPI that
    provides it, which may be installed without its scripts dir being on the
    PATH.
    """
    path = shutil.which(name)
    if path:
        return path
    try:
        module = __import__(moduleName)
    except ImportError:
        return None
    return shutil.which(name, path=getattr(module, dirAttr, None))


def findCMake():
    cmake = _findTool('cmake', 'cmake', 'CMAKE_BIN_DIR')
    want = '.'.join(str(v) for v in MIN_CMAKE_VERSION)
    if not cmake:
        _fail(f'CMake {want} or newer is needed to build wxWidgets. Install it '
              f'with "pip install cmake ninja" or from https://cmake.org/.')
    output = subprocess.run([cmake, '--version'], capture_output=True,
                            text=True).stdout
    match = re.search(r'version (\d+)\.(\d+)', output)
    if not match or tuple(int(v) for v in match.groups()) < MIN_CMAKE_VERSION:
        _fail(f'CMake {want} or newer is needed to build wxWidgets, but '
              f'{cmake} is "{output.strip()}".')
    return cmake


def findNinja():
    ninja = _findTool('ninja', 'ninja', 'BIN_DIR')
    if not ninja:
        _fail('Ninja is needed to build wxWidgets. Install it with '
              '"pip install ninja" or from https://ninja-build.org/.')
    return ninja


def getSettings(wxDir, buildDir, mswArch=None, cairoRoot=None, noMSEdge=False,
                prefix=None):
    """
    Return the CMake cache values for the wxWidgets build wxPython needs. The
    wxUSE_ values set to ON or OFF here are also checked in the generated
    setup.h by checkSetupH(). Values that depend on an option are also given
    when the option is not used, as CMake would keep them from an earlier run.
    """
    settings = {
        'wxBUILD_SHARED':           'ON',
        'wxBUILD_MONOLITHIC':       'OFF',
        'wxBUILD_SAMPLES':          'OFF',
        'wxBUILD_TESTS':            'OFF',
        'wxBUILD_DEMOS':            'OFF',
        # make_allmo() builds the message catalogs
        'wxBUILD_LOCALES':          'OFF',

        'wxUSE_AUTOID_MANAGEMENT':  'ON',
        'wxUSE_DEBUGREPORT':        'OFF',
        'wxUSE_DISPLAY':            'ON',
        'wxUSE_GRAPHICS_CONTEXT':   'ON',
        'wxUSE_OPENGL':             'ON',
        'wxUSE_SOUND':              'ON',
        'wxUSE_UIACTIONSIMULATOR':  'ON',

        # wx < 3.4: the in-place wx-config refers to lib64 instead of lib on
        # some systems.
        'CMAKE_INSTALL_LIBDIR':     'lib',
    }
    if prefix:
        settings['CMAKE_INSTALL_PREFIX'] = os.path.abspath(prefix)

    if isWindows:
        settings.update({
            'CMAKE_CONFIGURATION_TYPES':    'Debug;Release',
            # Keep the debug info in the release DLLs' PDB files
            'CMAKE_MSVC_DEBUG_INFORMATION_FORMAT': 'ProgramDatabase',
            # wx < 3.4: release builds are linked with /DEBUG, which turns
            # these off by default.
            'CMAKE_SHARED_LINKER_FLAGS_RELEASE': '/INCREMENTAL:NO /OPT:REF /OPT:ICF',
            # No "_custom" at the end of the DLL names
            'wxBUILD_VENDOR':               '',

            'wxUSE_ACCESSIBILITY':          'ON',
            'wxUSE_AFM_FOR_POSTSCRIPT':     'OFF',
            'wxUSE_DATEPICKCTRL_GENERIC':   'ON',
            'wxUSE_DIALUP_MANAGER':         'OFF',
            'wxUSE_IFF':                    'ON',
            'wxUSE_INICONF':                'OFF',
            'wxUSE_POSTSCRIPT':             'ON',
            'wxUSE_WEBVIEW_EDGE':           'OFF' if noMSEdge else 'ON',
            'wxUSE_WINRT':                  'OFF',
            'wxUSE_WINSOCK2':               'ON',
        })
        if mswArch == 'arm64':
            # wx < 3.4: ARM64 is only detected with Visual Studio generators.
            settings['CMAKE_VS_PLATFORM_NAME'] = 'ARM64'
        settings['wxUSE_CAIRO'] = 'ON' if cairoRoot else 'OFF'
        if cairoRoot:
            settings['CAIRO_INCLUDE_DIRS'] = os.path.join(cairoRoot, 'include', 'cairo')
            # wx < 3.4: cairo is loaded at run time, so only its headers are
            # needed, but FindCairo also wants a library.
            settings['CAIRO_LIBRARIES'] = os.path.join(cairoRoot, mswArch or 'x86',
                                                       'bin', 'libcairo-2.dll')
        return settings


def parseCMakeArgs(args):
    """
    Return the cache values set with -D in a list of extra CMake arguments.
    """
    values = {}
    for arg in args:
        match = re.match(r'-D([^:=]+)(:[^=]*)?=(.*)$', arg)
        if match:
            values[match.group(1)] = match.group(3)
    return values


def checkSetupH(buildDir, settings):
    """
    Check that wxWidgets didn't turn off (or on) any of the features in
    settings, which it may do with only a warning, e.g. when a library a
    feature needs isn't found.
    """
    expected = {}
    for name, value in settings.items():
        if name.startswith('wxUSE_') and value.upper() in ('ON', 'OFF'):
            expected[name] = '1' if value.upper() == 'ON' else '0'

    setupFiles = sorted(glob.glob(os.path.join(buildDir, 'lib', '**', 'setup.h'),
                                  recursive=True))
    if not setupFiles:
        _fail('No setup.h found in ' + buildDir)
    errors = []
    for setupFile in setupFiles:
        text = open(setupFile).read()
        for name, value in sorted(expected.items()):
            for found in re.findall(r'#define\s+%s\s+(\d+)' % name, text):
                if found != value:
                    errors.append('%s is %s in %s' % (name, found, setupFile))
    if errors:
        _fail('wxWidgets was configured differently than wxPython needs, see '
              'the CMake output above for why:\n    ' + '\n    '.join(errors))


def _run(cmd, cwd=None):
    msg(shlex.join(cmd))
    if subprocess.run(cmd, cwd=cwd).returncode != 0:
        _fail('Command failed: ' + shlex.join(cmd))


def configure(wxDir, buildDir, settings, extraArgs=(), fresh=False):
    cmake = findCMake()
    ninja = findNinja()
    os.makedirs(buildDir, exist_ok=True)

    cmd = [cmake, '-S', wxDir, '-B', buildDir, '-G', 'Ninja Multi-Config',
           '-DCMAKE_MAKE_PROGRAM=' + ninja]
    if fresh:
        cmd.append('--fresh')
    cmd += ['-D%s=%s' % item for item in sorted(settings.items())]
    cmd += list(extraArgs)
    _run(cmd)

    allSettings = dict(settings)
    allSettings.update(parseCMakeArgs(extraArgs))
    checkSetupH(buildDir, allSettings)


def build(buildDir, configs=(None,), jobs=None, verbose=False, extraArgs=()):
    cmake = findCMake()
    for config in configs:
        cmd = [cmake, '--build', buildDir]
        if config:
            cmd += ['--config', config]
        if jobs:
            cmd += ['--parallel', str(jobs)]
        if verbose:
            cmd.append('--verbose')
        if extraArgs:
            cmd += ['--'] + list(extraArgs)
        _run(cmd)

