# -*- coding: utf-8 -*-
#
# #############################################################################
#
# MIT License
#
# Copyright 2022  Kevin G. Schlosser
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#
# #############################################################################

# This tool is used to create an identical build environment to what is created
# when building a Visual Studio project or using any of the vcvars and vsvars
# batch files. There is a similar tool included with SetupTools and it is
# called msvc. The setup tools version is not complete and it is also error
# prone. It does not make an identical build environment.

import os
import sys
import ctypes
import subprocess
import winreg
import distutils.log
from typing import Optional, Union


_IS_WIN = sys.platform.startswith('win')


if _IS_WIN:
    try:
        from . import vswhere
    except ImportError:
        import vswhere


_HRESULT = ctypes.c_long
_BOOL = ctypes.c_bool
_DWORD = ctypes.c_ulong
_LPCVOID = ctypes.c_void_p
_LPCWSTR = ctypes.c_wchar_p
_LPVOID = ctypes.c_void_p
_UINT = ctypes.c_uint
_INT = ctypes.c_int
_HANDLE = ctypes.c_void_p
_HWND = ctypes.c_void_p
_LPWSTR = ctypes.c_wchar_p
_POINTER = ctypes.POINTER
_CHAR = _INT
_PUINT = _POINTER(_UINT)
_LPDWORD = _POINTER(_DWORD)


if _IS_WIN:
    try:
        _vswhere = vswhere.SetupConfiguration.GetSetupConfiguration()
    except:  # NOQA
        _vswhere = None
else:
    _vswhere = None


# noinspection PyPep8Naming
class _VS_FIXEDFILEINFO(ctypes.Structure):
    _fields_ = [
        ("dwSignature", _DWORD),  # will be 0xFEEF04BD
        ("dwStrucVersion", _DWORD),
        ("dwFileVersionMS", _DWORD),
        ("dwFileVersionLS", _DWORD),
        ("dwProductVersionMS", _DWORD),
        ("dwProductVersionLS", _DWORD),
        ("dwFileFlagsMask", _DWORD),
        ("dwFileFlags", _DWORD),
        ("dwFileOS", _DWORD),
        ("dwFileType", _DWORD),
        ("dwFileSubtype", _DWORD),
        ("dwFileDateMS", _DWORD),
        ("dwFileDateLS", _DWORD)
    ]


if _IS_WIN:
    _version = ctypes.windll.version

    _GetFileVersionInfoSize = _version.GetFileVersionInfoSizeW
    _GetFileVersionInfoSize.restype = _DWORD
    _GetFileVersionInfoSize.argtypes = [_LPCWSTR, _LPDWORD]

    _VerQueryValue = _version.VerQueryValueW
    _VerQueryValue.restype = _BOOL
    _VerQueryValue.argtypes = [_LPCVOID, _LPCWSTR, _POINTER(_LPVOID), _PUINT]

    _GetFileVersionInfo = _version.GetFileVersionInfoW
    _GetFileVersionInfo.restype = _BOOL
    _GetFileVersionInfo.argtypes = [_LPCWSTR, _DWORD, _DWORD, _LPVOID]


    def _get_file_version(filename):
        dw_len = _GetFileVersionInfoSize(filename, None)
        if not dw_len:
            raise ctypes.WinError()

        lp_data = (_CHAR * dw_len)()
        if not _GetFileVersionInfo(
            filename,
            0,
            ctypes.sizeof(lp_data), lp_data
        ):
            raise ctypes.WinError()

        u_len = _UINT()
        lpffi = _POINTER(_VS_FIXEDFILEINFO)()
        lplp_buffer = ctypes.cast(ctypes.pointer(lpffi), _POINTER(_LPVOID))
        if not _VerQueryValue(lp_data, "\\", lplp_buffer, ctypes.byref(u_len)):
            raise ctypes.WinError()

        ffi = lpffi.contents
        return (
            ffi.dwFileVersionMS >> 16,
            ffi.dwFileVersionMS & 0xFFFF,
            ffi.dwFileVersionLS >> 16,
            ffi.dwFileVersionLS & 0xFFFF,
        )


    _CSIDL_PROGRAM_FILES = 0x26
    _CSIDL_PROGRAM_FILESX86 = 0x2A

    _SHGFP_TYPE_CURRENT = 0
    _MAX_PATH = 260
    _CSIDL_FLAG_DONT_VERIFY = 16384

    _shell32 = ctypes.windll.Shell32

    # noinspection PyUnboundLocalVariable
    _SHGetFolderPathW = _shell32.SHGetFolderPathW
    _SHGetFolderPathW.restype = _HRESULT
    _SHGetFolderPathW.argtypes = [_HWND, _INT, _HANDLE, _DWORD, _LPWSTR]

    _buf = ctypes.create_unicode_buffer(_MAX_PATH)

    _SHGetFolderPathW(
        0,
        _CSIDL_PROGRAM_FILESX86 | _CSIDL_FLAG_DONT_VERIFY,
        0,
        _SHGFP_TYPE_CURRENT,
        _buf
    )

    _PROGRAM_FILES_X86 = _buf.value

    _buf = ctypes.create_unicode_buffer(_MAX_PATH)

    _SHGetFolderPathW(
        0,
        _CSIDL_PROGRAM_FILES | _CSIDL_FLAG_DONT_VERIFY,
        0,
        _SHGFP_TYPE_CURRENT,
        _buf
    )

    _PROGRAM_FILES = _buf.value

    del _buf
    del _SHGetFolderPathW
    del _shell32
    del _CSIDL_PROGRAM_FILES
    del _CSIDL_PROGRAM_FILESX86
    del _SHGFP_TYPE_CURRENT
    del _MAX_PATH
    del _CSIDL_FLAG_DONT_VERIFY

else:
    def _get_file_version(_):
        pass

    _PROGRAM_FILES_X86 = ''
    _PROGRAM_FILES = ''


_found_cl = {}


def _find_cl(path):
    if path in _found_cl:
        return _found_cl[path]

    for root, dirs, files in os.walk(path):
        if 'cl.exe' not in files:
            continue

        if 'MSVC' in root:
            head, tail = os.path.split(root)

            while head and not head.endswith('MSVC'):
                head, tail = os.path.split(head)

            if head:
                _found_cl[path] = [[head.split('\\VC\\')[0] + '\\VC', tail]]
            else:
                _found_cl[path] = []
        else:
            root = root.split('\\VC\\')[0]
            ver = os.path.split(root)[1]

            _found_cl[path] = [[root + '\\VC', ver.split(' ')[-1]]]

        return _found_cl[path]

    _found_cl[path] = []

    return []


def _get_program_files_vc():
    pths = [
        os.path.join(_PROGRAM_FILES_X86, f)
        for f in os.listdir(_PROGRAM_FILES_X86)
        if 'Visual Studio' in f
    ]
    res = [
        item for pth in pths for item in _find_cl(pth)
    ]

    return res


def _get_reg_value(path, key, wow6432=False):
    d = _read_reg_values(path, wow6432)
    if key in d:
        return d[key]

    return ''


def _read_reg_keys(key, wow6432=False):
    if isinstance(key, tuple):
        root = key[0]
        key = key[1]
    else:
        root = winreg.HKEY_LOCAL_MACHINE
        key = 'SOFTWARE\\Microsoft\\' + key

    try:
        if wow6432:
            handle = winreg.OpenKey(
                root,
                key,
                0,
                winreg.KEY_READ | winreg.KEY_WOW64_32KEY
            )
        else:
            handle = winreg.OpenKeyEx(root, key)
    except winreg.error:
        return []
    res = []

    for i in range(winreg.QueryInfoKey(handle)[0]):
        res += [winreg.EnumKey(handle, i)]

    winreg.CloseKey(handle)
    return res


def _read_reg_values(key, wow6432=False):
    if isinstance(key, tuple):
        root = key[0]
        key = key[1]
    else:
        root = winreg.HKEY_LOCAL_MACHINE
        key = 'SOFTWARE\\Microsoft\\' + key

    try:
        if wow6432:
            handle = winreg.OpenKey(
                root,
                key,
                0,
                winreg.KEY_READ | winreg.KEY_WOW64_32KEY
            )
        else:
            handle = winreg.OpenKeyEx(root, key)
    except winreg.error:
        return {}
    res = {}
    for i in range(winreg.QueryInfoKey(handle)[1]):
        name, value, _ = winreg.EnumValue(handle, i)
        res[_convert_mbcs(name)] = _convert_mbcs(value)

    winreg.CloseKey(handle)

    return res


def _convert_mbcs(s):
    dec = getattr(s, "decode", None)
    if dec is not None:
        try:
            s = dec("mbcs")
        except UnicodeError:
            pass
    return s


def _convert_version(ver):
    if isinstance(ver, str):
        ver = tuple(int(item) for item in ver.split('.'))
    elif isinstance(ver, bytes):
        ver = tuple(
            int(item) for item in ver.decode('utf-8').split('.')
        )
    elif isinstance(ver, int):
        ver = (ver,)
    elif isinstance(ver, float):
        ver = tuple(
            int(item) for item in str(ver).split('.')
        )
    elif isinstance(ver, list):
        ver = tuple(int(item) for item in ver)

    if not isinstance(ver, tuple):
        raise TypeError(
            'Version is not correct type({0})'.format(type(ver))
        )

    ver = '.'.join(str(item) for item in ver)

    return ver


# I have separated the environment into several classes
# Environment - the main environment class.
# the environment class is what is going to get used. this handles all of the
# non specific bits of the environment. all of the rest of the classes are
# brought together in the environment to form a complete build environment.

# NETInfo - Any .NET related environment settings

# WindowsSDKInfo - Any Windows SDK environment settings

# VisualStudioInfo - Any VisualStudios environment settings (if applicable)

# VisualCInfo - Any VisualC environment settings

# PythonInfo - This class really isnt for environment settings as such.
# It is more of a convenience class. it will get things like a list of the
# includes specific to the python build. the architecture of the version of
# python that is running stuff along those lines.
class PythonInfo(object):

    @property
    def architecture(self):
        return 'x64' if sys.maxsize > 2 ** 32 else 'x86'

    @property
    def version(self):
        return '.'.join(str(ver) for ver in sys.version_info)

    @property
    def dependency(self):
        return 'Python%d%d.lib' % sys.version_info[:2]

    @property
    def includes(self):
        python_path = os.path.dirname(sys.executable)
        python_include = os.path.join(python_path, 'include')

        python_includes = [python_include]
        for root, dirs, files in os.walk(python_include):
            for d in dirs:
                python_includes += [os.path.join(root, d)]
        return python_includes

    @property
    def libraries(self):
        python_path = os.path.dirname(sys.executable)
        python_lib = os.path.join(python_path, 'libs')

        python_libs = [python_lib]
        for root, dirs, files in os.walk(python_lib):
            for d in dirs:
                python_libs += [os.path.join(root, d)]
        return python_libs

    def __str__(self):
        template = (
            '== Python =====================================================\n'
            '  version: {py_version}\n'
            '  architecture: {py_architecture}\n'
            '  library: {py_dependency}\n'
            '  libs: {py_libraries}\n'
            '  includes: {py_includes}\n'
        )
        return template.format(
            py_version=self.version,
            py_architecture=self.architecture,
            py_dependency=self.dependency,
            py_libraries=self.libraries,
            py_includes=self.includes
        )


class VisualCInfo(object):

    def __init__(
        self, 
        environ: "Environment",
        minimum_c_version: Optional[Union[int, float]] = None,
        strict_c_version: Optional[Union[int, float]] = None,
        minimum_toolkit_version: Optional[int] = None,
        strict_toolkit_version: Optional[int] = None,
        vs_version: Optional[Union[str, int]] = None
    ):
        self.environment = environ
        self.platform = environ.platform
        self.strict_c_version = strict_c_version
        self.__installed_versions = None
        self._cpp_installation = None
        self._ide_install_directory = None
        self._install_directory = None
        self._cpp_version = None
        self._tools_version = None
        self._toolset_version = None
        self._msvc_dll_path = None
        self._tools_redist_directory = None
        self._tools_install_directory = None
        self._msbuild_version = None
        self._msbuild_path = None
        self._product_semantic_version = None
        self._devinit_path = None

        self._strict_toolkit_version = strict_toolkit_version
        self._minimum_toolkit_version = minimum_toolkit_version
        py_version = sys.version_info[:2]
        if py_version in ((3, 4),):
            min_visual_c_version = 10.0
        elif py_version in ((3, 5), (3, 6), (3, 7), (3, 8)):
            min_visual_c_version = 14.0
        elif py_version in ((3, 9), (3, 10)):
            min_visual_c_version = 14.2
        else:
            raise RuntimeError(
                'This library does not support '
                'python version %d.%d' % py_version
            )

        if (
            strict_c_version is not None and
            strict_c_version < min_visual_c_version
        ):
            raise RuntimeError(
                'The set minimum compiler version is lower then the '
                'required compiler version for Python'
            )

        if minimum_c_version is None:
            minimum_c_version = min_visual_c_version

        if strict_toolkit_version is not None:
            strict_toolkit_version = str(strict_toolkit_version / 10.0)

        if minimum_toolkit_version is not None:
            minimum_toolkit_version = str(minimum_toolkit_version / 10.0)

        self.minimum_c_version = minimum_c_version
        self._strict_toolkit_version = strict_toolkit_version
        self._minimum_toolkit_version = minimum_toolkit_version

        if _vswhere is not None:
            distutils.log.debug('\n' + str(_vswhere))

            cpp_id = 'Microsoft.VisualCpp.Tools.Host{0}.Target{1}'.format(
                environ.machine_architecture.upper(),
                environ.python.architecture.upper()
            )

            tools_id = (
                'Microsoft.VisualCpp.Premium.Tools.'
                'Host{0}.Target{1}'
            ).format(
                environ.machine_architecture.upper(),
                environ.python.architecture.upper()
            )

            cpp_version = None
            cpp_installation = None

            for installation in _vswhere:
                if vs_version is not None:
                    try:
                        if isinstance(vs_version, str):
                            display_version = str(
                                installation.catalog.product_display_version
                            )

                            if (
                                installation.version != vs_version and
                                display_version != vs_version
                            ):
                                continue
                        else:
                            product_line_version = int(
                                installation.catalog.product_line_version
                            )

                            if product_line_version != vs_version:
                                continue

                    except:  # NOQA
                        continue

                for package in installation.packages.vsix:
                    if package.id == cpp_id:
                        if (
                            self.strict_c_version is not None and
                            package != self.strict_c_version
                        ):
                            continue

                        if (
                            self.minimum_c_version is not None and
                            package < self.minimum_c_version
                        ):
                            continue

                        if cpp_version is None:
                            cpp_version = package
                            cpp_installation = installation
                        elif package > cpp_version:
                            cpp_version = package
                            cpp_installation = installation

            if cpp_installation is not None:
                self._cpp_version = cpp_version.version
                self._cpp_installation = cpp_installation

                tools_version = None
                tools_path = os.path.join(
                    cpp_installation.path,
                    'VC',
                    'Tools',
                    'MSVC'
                )

                for package in cpp_installation.packages.vsix:
                    if package.id == tools_id:
                        if not os.path.exists(
                            os.path.join(tools_path, package.version)
                        ):
                            continue

                        if strict_toolkit_version is not None:
                            if package == strict_toolkit_version:
                                tools_version = package
                                break

                        if minimum_toolkit_version is not None:
                            if package <= minimum_toolkit_version:
                                continue

                        if tools_version is None:
                            tools_version = package
                        elif tools_version > package:
                            tools_version = package

                if tools_version is None:
                    for file in os.listdir(tools_path):
                        if strict_toolkit_version is not None:
                            tk_version = file[:len(strict_toolkit_version)]
                            if tk_version == strict_toolkit_version:
                                tools_version = file
                                break

                        if minimum_toolkit_version is not None:
                            tk_version = file[:len(minimum_toolkit_version)]
                            if tk_version < minimum_toolkit_version:
                                continue

                        if tools_version is None:
                            tools_version = file
                        elif tools_version < file:
                            tools_version = file

                else:
                    tools_version = tools_version.version

                if tools_version is not None:
                    tools_version = tools_version.split('.')
                    self._toolset_version = (
                        'v' + tools_version[0] +
                        tools_version[1][0]
                    )
                    self._tools_version = '.'.join(tools_version)

                    self._tools_install_directory = os.path.join(
                        tools_path, self._tools_version
                    )

                    tools_redist_directory = (
                        self._tools_install_directory.replace(
                            'Tools',
                            'Redist'
                        )
                    )

                    if os.path.exists(tools_redist_directory):
                        self._tools_redist_directory = (
                            tools_redist_directory + '\\'
                        )

                        msvc_dll_path = os.path.join(
                            tools_redist_directory,
                            environ.python.architecture,
                            'Microsoft.VC{0}.CRT'.format(
                                self._toolset_version[1:]
                            )
                        )

                        if os.path.exists(msvc_dll_path):
                            self._msvc_dll_path = msvc_dll_path

                install_directory = os.path.join(
                    cpp_installation.path, 'VC'
                )
                if os.path.exists(install_directory):
                    self._install_directory = install_directory

                msbuild_path = os.path.join(
                    cpp_installation.path,
                    'MSBuild',
                    'Current',
                    'Bin',
                    'MSBuild.exe'
                )

                if os.path.exists(msbuild_path):
                    msbuild_version = _get_file_version(msbuild_path)
                    self._msbuild_version = '.'.join(
                        str(item) for item in msbuild_version
                    )
                    self._msbuild_path = msbuild_path

                ide_directory = os.path.join(
                    cpp_installation.path,
                    'Common7',
                    'IDE',
                    'VC'
                )
                if os.path.exists(ide_directory):
                    self._ide_install_directory = ide_directory

                product_semantic_version = (
                    cpp_installation.catalog.product_semantic_version
                )
                if product_semantic_version is not None:
                    self._product_semantic_version = (
                        product_semantic_version.split('+')[0]
                    )

                devinit_path = os.path.join(
                    cpp_installation.path,
                    'Common7',
                    'Tools',
                    'devinit',
                    'devinit.exe'
                )
                if os.path.exists(devinit_path):
                    self._devinit_path = devinit_path

    @property
    def has_ninja(self):
        ide_path = os.path.split(self.ide_install_directory)[0]
        ninja_path = os.path.join(
            ide_path,
            'CommonExtensions',
            'Microsoft',
            'CMake',
            'Ninja',
            'ninja.exe'
        )
        return os.path.exists(ninja_path)

    @property
    def has_cmake(self):
        ide_path = os.path.split(self.ide_install_directory)[0]

        cmake_path = os.path.join(
            ide_path,
            'CommonExtensions',
            'Microsoft',
            'CMake',
            'CMake',
            'bin',
            'cmake.exe'
        )
        return os.path.exists(cmake_path)

    @property
    def cmake_paths(self) -> list:
        paths = []
        ide_path = os.path.split(self.ide_install_directory)[0]

        cmake_path = os.path.join(
            ide_path,
            'CommonExtensions',
            'Microsoft',
            'CMake'
        )

        if os.path.exists(cmake_path):
            bin_path = os.path.join(cmake_path, 'CMake', 'bin')
            ninja_path = os.path.join(cmake_path, 'Ninja')
            if os.path.exists(bin_path):
                paths += [bin_path]

            if os.path.exists(ninja_path):
                paths += [ninja_path]

        return paths

    @property
    def cpp_installation(
        self
    ) -> Union[vswhere.ISetupInstance, vswhere.ISetupInstance2]:
        return self._cpp_installation

    @property
    def f_sharp_path(self) -> Optional[str]:
        version = float(int(self.version.split('.')[0]))

        reg_path = (
            winreg.HKEY_LOCAL_MACHINE,
            r'SOFTWARE\Microsoft\VisualStudio'
            r'\{0:.1f}\Setup\F#'.format(version)
        )

        f_sharp_path = _get_reg_value(reg_path, 'ProductDir')
        if f_sharp_path and os.path.exists(f_sharp_path):
            return f_sharp_path

        path = r'C:\Program Files (x86)\Microsoft SDKs\F#'
        if os.path.exists(path):
            versions = os.listdir(path)
            max_ver = 0.0
            found_version = ''

            for version in versions:
                try:
                    ver = float(version)
                except ValueError:
                    continue

                if ver > max_ver:
                    max_ver = ver
                    found_version = version

            f_sharp_path = os.path.join(
                path,
                found_version,
                'Framework',
                'v' + found_version
            )

            if os.path.exists(f_sharp_path):
                return f_sharp_path

        install_dir = os.path.split(self.install_directory)[0]
        f_sharp_path = os.path.join(
            install_dir,
            'Common7',
            'IDE',
            'CommonExtensions',
            'Microsoft',
            'FSharp',
            'Tools'
        )
        if os.path.exists(f_sharp_path):
            return f_sharp_path

    @property
    def ide_install_directory(self) -> str:
        if self._ide_install_directory is None:
            directory = self.install_directory
            ide_directory = os.path.abspath(
                os.path.join(directory, '..')
            )

            ide_directory = os.path.join(
                ide_directory,
                'Common7',
                'IDE',
                'VC'
            )
            if os.path.exists(ide_directory):
                self._ide_install_directory = ide_directory

        return self._ide_install_directory

    @property
    def install_directory(self) -> str:
        """
        Visual C path
        :return: Visual C path
        """
        if self._install_directory is None:
            self._install_directory = (
                self._installed_c_paths[self.version]['base']
            )

        return self._install_directory

    @property
    def _installed_c_paths(self):
        if self.__installed_versions is None:
            self.__installed_versions = {}

            def add(vers):
                for base_pth, ver in vers:
                    if os.path.exists(base_pth):
                        base_ver = float(int(ver.split('.')[0]))

                        self.__installed_versions[ver] = dict(
                            base=base_pth,
                            root=base_pth
                        )
                        self.__installed_versions[base_ver] = dict(
                            base=base_pth,
                            root=base_pth
                        )

            add(_get_program_files_vc())

            reg_path = (
                winreg.HKEY_LOCAL_MACHINE,
                r'SOFTWARE\Policies\Microsoft'
                r'\VisualStudio\Setup'
            )

            vs_path = _get_reg_value(reg_path, 'SharedInstallationPath')

            if vs_path:
                vs_path = os.path.split(vs_path)[0]
                if os.path.exists(vs_path):
                    res = []

                    pths = [
                        os.path.join(vs_path, vs_ver)
                        for vs_ver in os.listdir(vs_path)
                        if vs_ver.isdigit()
                    ]
                    res.extend(
                        [item for pth in pths for item in _find_cl(pth)]
                    )

                    add(res)

            reg_path = (
                winreg.HKEY_CLASSES_ROOT,
                r'Local Settings\Software'
                r'\Microsoft\Windows\Shell\MuiCache'
            )

            paths = []

            for key in _read_reg_values(reg_path):
                if 'cl.exe' in key:
                    value = _get_reg_value(reg_path, key)
                    if 'C++ Compiler Driver' in value:
                        paths += [key]

                elif 'devenv.exe' in key:
                    if not os.path.exists(key):
                        continue

                    value = _get_reg_value(reg_path, key)

                    if value.startswith('Microsoft Visual Studio '):

                        head, tail = os.path.split(key)
                        while tail != 'Common7' and head:
                            head, tail = os.path.split(head)

                        if head:
                            add(_find_cl(head))

            for path in paths:
                if not os.path.exists(path):
                    continue

                if '\\VC\\bin' in path:
                    version = path.split('\\VC\\bin')[0]
                elif '\\bin\\Host' in path:
                    version = path.split('\\bin\\Host')[0]
                else:
                    continue

                version = os.path.split(version)[1]
                version = version.replace(
                    'Microsoft Visual Studio',
                    ''
                ).strip()
                base_version = float(int(version.split('.')[0]))

                base_path = path.split('\\VC\\')[0] + '\\VC'
                if os.path.exists(os.path.join(base_path, 'include')):
                    vc_root = base_path
                else:
                    vc_root = path.split('\\bin\\')[0]

                self.__installed_versions[version] = dict(
                    base=base_path,
                    root=vc_root
                )
                self.__installed_versions[base_version] = dict(
                    base=base_path,
                    root=vc_root
                )

            reg_path = (
                winreg.HKEY_LOCAL_MACHINE,
                'SOFTWARE\\Microsoft\\VisualStudio\\SxS\\VS7'
            )

            for key in _read_reg_values(reg_path):
                try:
                    version = float(key)
                except ValueError:
                    continue

                path = _get_reg_value(reg_path, key)

                if (
                    (
                        os.path.exists(path) and
                        version not in self.__installed_versions
                    ) or version == 15.0
                ):

                    if version == 15.0:
                        version = 14.0

                    if not os.path.split(path)[1] == 'VC':
                        path = os.path.join(path, 'VC')

                    self.__installed_versions[version] = dict(
                        base=path,
                        root=path
                    )
                    self.__installed_versions[key] = dict(
                        base=path,
                        root=path
                    )

        return self.__installed_versions

    @property
    def version(self) -> str:
        """
        Visual C version

        Sometimes when building extension in python the version of the compiler
        that was used to compile Python has to also be used to compile an
        extension. I have this system set so it will automatically pick the
        most recent compiler installation. this can be overridden in 2 ways.
        The first way being that the compiler version that built Python has to
        be used. The second way is you can set a minimum compiler version to
        use.

        :return: found Visual C version
        """
        if self._cpp_version is None:
            if self.strict_c_version is not None:
                if self.strict_c_version not in self._installed_c_paths:
                    raise RuntimeError(
                        'No Compatible Visual C version found.'
                    )

                self._cpp_version = str(self.strict_c_version)
                return self._cpp_version

            match = None
            for version in self._installed_c_paths:
                if not isinstance(version, float):
                    continue
                
                if version >= self.minimum_c_version:
                    if match is None:
                        match = version
                    elif version < match:
                        match = version
                        
            if match is None:
                raise RuntimeError(
                    'No Compatible Visual C\\C++ version found.'
                )
            
            self._cpp_version = str(match)

        return self._cpp_version

    @property
    def tools_version(self) -> str:
        if self._tools_version is None:
            version = os.path.split(self.tools_install_directory)[1]
            if not version.split('.')[-1].isdigit():
                version = str(self.version)

            self._tools_version = version

        return self._tools_version

    @property
    def toolset_version(self) -> str:
        """
        The platform toolset gets written to the solution file. this instructs
        the compiler to use the matching MSVCPxxx.dll file.
        """

        if self._toolset_version is None:
            tools_version = self.tools_version.split('.')

            self._toolset_version = (
                'v' +
                tools_version[0] +
                tools_version[1][:1]
            )

        return self._toolset_version

    @property
    def msvc_dll_version(self) -> Optional[str]:
        msvc_dll_path = self.msvc_dll_path
        if not msvc_dll_path:
            return
            
        for f in os.listdir(msvc_dll_path):
            if f.endswith('dll'):
                version = _get_file_version(
                    os.path.join(msvc_dll_path, f)
                )
                return '.'.join(str(ver) for ver in version)

    @property
    def msvc_dll_path(self) -> Optional[str]:
        if self._msvc_dll_path is None:
            x64 = self.platform == 'x64'

            toolset_version = self.toolset_version

            if toolset_version is None:
                return None

            folder_names = (
                'Microsoft.VC{0}.CRT'.format(toolset_version[1:]),
            )

            redist_path = self.tools_redist_directory

            for root, dirs, files in os.walk(redist_path):
                def pass_directory():
                    for item in ('onecore', 'arm', 'spectre'):
                        if item in root.lower():
                            return True
                    return False

                if pass_directory():
                    continue

                for folder_name in folder_names:
                    if folder_name in dirs:
                        if x64 and ('amd64' in root or 'x64' in root):
                            self._msvc_dll_path = os.path.join(
                                root,
                                folder_name
                            )
                            break
                        elif (
                            not x64 and
                            'amd64' not in root
                            and 'x64' not in root
                        ):
                            self._msvc_dll_path = os.path.join(
                                root,
                                folder_name
                            )
                            break

        return self._msvc_dll_path

    @property
    def tools_redist_directory(self) -> Optional[str]:
        if self._tools_redist_directory is None:
            tools_install_path = self.tools_install_directory

            if 'MSVC' in tools_install_path:
                redist_path = tools_install_path.replace(
                    'Tools',
                    'Redist'
                )
                if (
                    not os.path.exists(redist_path) and
                    'BuildTools' in tools_install_path
                ):
                    redist_path = redist_path.replace(
                        'BuildRedist', 'BuildTools'
                    )
            else:
                redist_path = os.path.join(
                    tools_install_path,
                    'Redist'
                )

            if not os.path.exists(redist_path):
                redist_path = os.path.split(redist_path)[0]
                tools_version = None

                for version in os.listdir(redist_path):
                    if not os.path.isdir(
                        os.path.join(redist_path, version)
                    ):
                        continue

                    if version.startswith('v'):
                        continue

                    if self._strict_toolkit_version is not None:
                        tk_version = (
                            version[:len(self._strict_toolkit_version)]
                        )
                        if tk_version == self._strict_toolkit_version:
                            tools_version = version
                            break

                    if self._minimum_toolkit_version is not None:
                        tk_version = (
                            version[:len(self._minimum_toolkit_version)]
                        )
                        if tk_version < self._minimum_toolkit_version:
                            continue

                    if tools_version is None:
                        tools_version = version
                    elif tools_version < version:
                        tools_version = version

                if tools_version is not None:
                    self._tools_redist_directory = (
                        os.path.join(redist_path, tools_version)
                    )
                else:
                    self._tools_redist_directory = ''

            else:
                self._tools_redist_directory = redist_path

            if (
                self._tools_redist_directory and
                not self._tools_redist_directory.endswith('\\')
            ):
                self._tools_redist_directory += '\\'

        return self._tools_redist_directory

    @property
    def tools_install_directory(self) -> Optional[str]:
        """
        Visual C compiler tools path.
        :return: Path to the compiler tools
        """
        if self._tools_install_directory is None:

            vc_version = float(int(self.version.split('.')[0]))
            if vc_version >= 14.0:
                vc_tools_path = self._installed_c_paths[vc_version]['root']
            else:
                vc_tools_path = self._installed_c_paths[vc_version]['base']

            # lib_path = os.path.join(vc_tools_path, 'lib')
            tools_path = os.path.join(vc_tools_path, 'Tools', 'MSVC')

            if os.path.exists(tools_path):
                versions = os.listdir(tools_path)
                tools_version = None

                for version in versions:
                    if self._strict_toolkit_version is not None:
                        tk_version = (
                            version[:len(self._strict_toolkit_version)]
                        )
                        if tk_version == self._strict_toolkit_version:
                            tools_version = version
                            break

                    if self._minimum_toolkit_version is not None:
                        tk_version = (
                            version[:len(self._minimum_toolkit_version)]
                        )
                        if tk_version < self._minimum_toolkit_version:
                            continue

                    if tools_version is None:
                        tools_version = version
                    elif tools_version < version:
                        tools_version = version

                if tools_version is not None:
                    self._tools_install_directory = os.path.join(
                        tools_path,
                        tools_version
                    )

                else:
                    raise RuntimeError('Unable to locate build tools')

            else:
                raise RuntimeError('Unable to locate build tools')

        return self._tools_install_directory

    @property
    def msbuild_version(self) -> Optional[str]:
        """
        MSBuild versions are specific to the Visual C version
        :return: MSBuild version, 3.5, 4.0, 12, 14, 15
        """
        if self._msbuild_version is None:
            vc_version = str(float(int(self.version.split('.')[0])))
            
            if vc_version == 9.0:
                self._msbuild_version = '3.5'
            elif vc_version in (10.0, 11.0):
                self._msbuild_version = '4.0'
            else:
                self._msbuild_version = vc_version
        return self._msbuild_version

    @property
    def msbuild_path(self) -> Optional[str]:
        if self._msbuild_path is not None:
            program_files = os.environ.get(
                'ProgramFiles(x86)',
                'C:\\Program Files (x86)'
            )

            version = float(int(self.version.split('.')[0]))

            ms_build_path = os.path.join(
                program_files,
                'MSBuild',
                '{0:.1f}'.format(version),
                'bin'
            )

            if self.platform == 'x64':
                if os.path.exists(os.path.join(ms_build_path, 'x64')):
                    ms_build_path = os.path.join(ms_build_path, 'x64')
                else:
                    ms_build_path = os.path.join(ms_build_path, 'amd64')

            elif os.path.exists(os.path.join(ms_build_path, 'x86')):
                ms_build_path = os.path.join(ms_build_path, 'x86')

            if os.path.exists(ms_build_path):
                self._msbuild_path = ms_build_path

        return self._msbuild_path

    @property
    def html_help_path(self) -> Optional[str]:

        reg_path = (
            winreg.HKEY_LOCAL_MACHINE,
            r'SOFTWARE\Wow6432Node\Microsoft\Windows'
            r'\CurrentVersion\App Paths\hhw.exe'
        )

        html_help_path = _get_reg_value(reg_path, 'Path')
        if html_help_path and os.path.exists(html_help_path):
            return html_help_path

        if os.path.exists(
            r'C:\Program Files (x86)\HTML Help Workshop'
        ):
            return r'C:\Program Files (x86)\HTML Help Workshop'

    @property
    def path(self) -> list:
        tools_path = self.tools_install_directory
        base_path = os.path.join(tools_path, 'bin')

        path = []

        f_sharp_path = self.f_sharp_path
        msbuild_path = self.msbuild_path

        ide_base_path = os.path.split(self.install_directory)[0]
        perf_tools_x64_path = os.path.join(
            ide_base_path,
            'Team Tools',
            'Performance Tools',
            'x64'
        )

        if os.path.exists(perf_tools_x64_path):
            path += [perf_tools_x64_path]

        perf_tools_path = os.path.join(
            ide_base_path,
            'Team Tools',
            'Performance Tools'
        )
        if os.path.exists(perf_tools_path):
            path += [perf_tools_path]

        com7_ide_path = os.path.join(
            ide_base_path,
            'Common7',
            'IDE'
        )

        vc_packages_path = os.path.join(
            com7_ide_path,
            'VC',
            'VCPackages'
        )
        if os.path.exists(vc_packages_path):
            path += [vc_packages_path]

        team_explorer_path = os.path.join(
            com7_ide_path,
            'CommonExtensions',
            'Microsoft',
            'TeamFoundation',
            'Team Explorer'
        )
        if os.path.exists(team_explorer_path):
            path += [team_explorer_path]

        intellicode_cli_path = os.path.join(
            com7_ide_path,
            'Extensions',
            'Microsoft',
            'IntelliCode',
            'CLI'
        )
        if os.path.exists(intellicode_cli_path):
            path += [intellicode_cli_path]

        roslyn_path = os.path.join(
            ide_base_path,
            'MSBuild',
            'Current',
            'bin',
            'Roslyn'
        )
        if os.path.exists(roslyn_path):
            path += [roslyn_path]

        devinit_path = os.path.join(
            ide_base_path,
            'Common7',
            'Tools',
            'devinit'
        )
        if os.path.exists(devinit_path):
            path += [devinit_path]

        vs_path = os.path.split(ide_base_path)[0]
        vs_path, edition = os.path.split(vs_path)

        collection_tools_path = os.path.join(
            vs_path,
            'Shared',
            'Common',
            'VSPerfCollectionTools',
            'vs' + edition
        )
        if os.path.exists(collection_tools_path):
            path += [collection_tools_path]

        collection_tools_path_x64 = os.path.join(
            collection_tools_path,
            'x64'
        )
        if os.path.exists(collection_tools_path_x64):
            path += [collection_tools_path_x64]

        if msbuild_path is not None:
            path += [os.path.split(msbuild_path)[0]]

        if f_sharp_path is not None:
            path += [f_sharp_path]

        html_help_path = self.html_help_path
        if html_help_path is not None:
            path += [html_help_path]

        bin_path = os.path.join(
            base_path,
            'Host' + self.platform,
            self.platform
        )

        if not os.path.exists(bin_path):
            if self.platform == 'x64':
                bin_path = os.path.join(base_path, 'x64')
                if not os.path.exists(bin_path):
                    bin_path = os.path.join(base_path, 'amd64')
            else:
                bin_path = os.path.join(base_path, 'x86')
                if not os.path.exists(bin_path):
                    bin_path = base_path

        if os.path.exists(bin_path):
            path += [bin_path]

        path += self.cmake_paths

        return path

    @property
    def atlmfc_lib_path(self) -> Optional[str]:
        atlmfc_path = self.atlmfc_path
        if not atlmfc_path:
            return

        atlmfc = os.path.join(atlmfc_path, 'lib')
        if self.platform == 'x64':
            atlmfc_path = os.path.join(atlmfc, 'x64')
            if not os.path.exists(atlmfc_path):
                atlmfc_path = os.path.join(atlmfc, 'amd64')
        else:
            atlmfc_path = os.path.join(atlmfc, 'x86')
            if not os.path.exists(atlmfc_path):
                atlmfc_path = atlmfc

        if os.path.exists(atlmfc_path):
            return atlmfc_path

    @property
    def lib(self) -> list:
        tools_path = self.tools_install_directory
        path = os.path.join(tools_path, 'lib')

        if self.platform == 'x64':
            lib_path = os.path.join(path, 'x64')
            if not os.path.exists(lib_path):
                lib_path = os.path.join(path, 'amd64')

        else:
            lib_path = os.path.join(path, 'x86')

            if not os.path.exists(lib_path):
                lib_path = path

        lib = []
        if os.path.exists(lib_path):
            lib += [lib_path]

        atlmfc_path = self.atlmfc_lib_path
        if atlmfc_path is not None:
            lib += [atlmfc_path]

        return lib

    @property
    def lib_path(self) -> list:
        tools_path = self.tools_install_directory
        path = os.path.join(tools_path, 'lib')

        if self.platform == 'x64':
            lib = os.path.join(path, 'x64')
            if not os.path.exists(lib):
                lib = os.path.join(path, 'amd64')
        else:
            lib = os.path.join(path, 'x86')
            if not os.path.exists(lib):
                lib = path

        references_path = os.path.join(
            lib,
            'store',
            'references'
        )

        lib_path = []
        if os.path.exists(lib):
            lib_path += [lib]

        atlmfc_path = self.atlmfc_lib_path

        if atlmfc_path is not None:
            lib_path += [atlmfc_path]

        if os.path.exists(references_path):
            lib_path += [references_path]
        else:
            references_path = os.path.join(path, 'x86', 'store', 'references')
            if os.path.exists(references_path):
                lib_path += [references_path]

        return lib_path

    @property
    def atlmfc_path(self) -> Optional[str]:
        tools_path = self.tools_install_directory
        atlmfc_path = os.path.join(tools_path, 'ATLMFC')

        if os.path.exists(atlmfc_path):
            return atlmfc_path

    @property
    def atlmfc_include_path(self) -> Optional[str]:
        atlmfc_path = self.atlmfc_path
        if atlmfc_path is None:
            return

        atlmfc_include_path = os.path.join(
            atlmfc_path,
            'include'
        )
        if os.path.exists(atlmfc_include_path):
            return atlmfc_include_path

    @property
    def include(self) -> list:
        tools_path = self.tools_install_directory
        include_path = os.path.join(tools_path, 'include')
        atlmfc_path = self.atlmfc_include_path

        include = []
        if os.path.exists(include_path):
            include += [include_path]

        if atlmfc_path is not None:
            include += [atlmfc_path]
        return include

    def __iter__(self):
        ide_install_directory = self.ide_install_directory
        tools_install_directory = self.tools_install_directory
        install_directory = self.install_directory

        if ide_install_directory:
            ide_install_directory += '\\'

        if tools_install_directory:
            tools_install_directory += '\\'

        if install_directory:
            install_directory += '\\'

        env = dict(
            VCIDEInstallDir=ide_install_directory,
            VCToolsVersion=self.tools_version,
            VCToolsInstallDir=tools_install_directory,
            VCINSTALLDIR=install_directory,
            VCToolsRedistDir=self.tools_redist_directory,
            Path=self.path,
            LIB=self.lib,
            INCLUDE=self.include,
            LIBPATH=self.lib_path,
            FSHARPINSTALLDIR=self.f_sharp_path
        )

        html_help = self.html_help_path

        if html_help is not None:
            env['HTMLHelpDir'] = html_help

        if self._product_semantic_version is not None:
            env['VSCMD_VER'] = self._product_semantic_version

        if self._devinit_path is not None:
            env['__devinit_path'] = self._devinit_path

        for key, value in env.items():
            if value is not None and value:
                if isinstance(value, list):
                    value = os.pathsep.join(value)
                yield key, str(value)

    def __str__(self):
        template = (
            '== Visual C ===================================================\n'
            '   version:   {visual_c_version}\n'
            '   path:      {visual_c_path}\n'
            '   has cmake: {has_cmake}\n'
            '   has ninja: {has_ninja}\n'
            '\n'
            '   -- Tools ---------------------------------------------------\n'
            '      version:     {tools_version}\n'
            '      path:        {tools_install_path}\n'
            '      redist path: {vc_tools_redist_path}\n'
            '   -- F# ------------------------------------------------------\n'
            '      path: {f_sharp_path}\n'
            '   -- DLL -----------------------------------------------------\n'
            '      version: {platform_toolset}-{msvc_dll_version}\n'
            '      path:    {msvc_dll_path}\n'
            '\n'
            '== MSBuild ====================================================\n'
            '   version: {msbuild_version}\n'
            '   path:    {msbuild_path}\n'
            '\n'
            '== HTML Help ==================================================\n'
            '   path: {html_help_path}\n'
            '\n'
            '== ATLMFC =====================================================\n'
            '   path:         {atlmfc_path}\n'
            '   include path: {atlmfc_include_path}\n'
            '   lib path:     {atlmfc_lib_path}\n'
        )

        return template.format(
            visual_c_version=self.version,
            visual_c_path=self.install_directory,
            has_cmake=self.has_cmake,
            has_ninja=self.has_ninja,
            tools_version=self.tools_version,
            tools_install_path=self.tools_install_directory,
            vc_tools_redist_path=self.tools_redist_directory,
            platform_toolset=self.toolset_version,
            msvc_dll_version=self.msvc_dll_version,
            msvc_dll_path=self.msvc_dll_path,
            msbuild_version=self.msbuild_version,
            msbuild_path=self.msbuild_path,
            f_sharp_path=self.f_sharp_path,
            html_help_path=self.html_help_path,
            atlmfc_lib_path=self.atlmfc_lib_path,
            atlmfc_include_path=self.atlmfc_include_path,
            atlmfc_path=self.atlmfc_path,
        )


class VisualStudioInfo(object):

    def __init__(
        self, 
        environ: "Environment",
        c_info: VisualCInfo
    ):
        self.environment = environ
        self.__devenv_version = None
        self.c_info = c_info
        self._install_directory = None
        self._dev_env_directory = None
        self._common_tools = None

        installation = c_info.cpp_installation

        self.__name__ = 'VisualStudioInfo'

        if installation is not None:
            if installation.path.endswith('BuildTools'):
                self.__name__ = 'BuildToolsInfo'
            version = installation.version.split('.')[0]
            self.__devenv_version = (
                str(float(int(version))),
                installation.version
            )

            install_directory = installation.path
            if os.path.exists(install_directory):
                self._install_directory = install_directory

                dev_env_directory = os.path.join(
                    install_directory,
                    os.path.split(installation.product_path)[0]
                )
                if os.path.exists(dev_env_directory):
                    self._dev_env_directory = dev_env_directory

                common_tools = os.path.join(
                    install_directory, 'Common7', 'Tools'
                )
                if os.path.exists(common_tools):
                    self._common_tools = common_tools + '\\'

    @property
    def install_directory(self) -> str:
        if self._install_directory is None:
            install_dir = os.path.join(
                self.c_info.install_directory,
                '..'
            )

            self._install_directory = (
                os.path.abspath(install_dir)
            )
        return self._install_directory

    @property
    def dev_env_directory(self) -> str:
        if self._dev_env_directory is None:
            self._dev_env_directory = os.path.join(
                self.install_directory,
                'Common7',
                'IDE'
            )

        return self._dev_env_directory

    @property
    def common_tools(self) -> str:
        if self._common_tools is None:

            common_tools = os.path.join(
                self.install_directory,
                'Common7',
                'Tools'
            )
            if os.path.exists(common_tools):
                self._common_tools = common_tools + '\\'
            else:
                self._common_tools = ''

        return self._common_tools

    @property
    def path(self) -> list:
        path = []

        dev_env_directory = self.dev_env_directory
        if dev_env_directory:
            path.append(dev_env_directory)

        common_tools = self.common_tools

        if common_tools:
            path.append(common_tools[:-1])

        collection_tools_dir = _get_reg_value(
            'VisualStudio\\VSPerf',
            'CollectionToolsDir'
        )
        if (
            collection_tools_dir and
            os.path.exists(collection_tools_dir)
        ):
            path.append(collection_tools_dir)

        vs_ide_path = self.dev_env_directory

        test_window_path = os.path.join(
            vs_ide_path,
            'CommonExtensions',
            'Microsoft',
            'TestWindow'
        )

        vs_tdb_path = os.path.join(
            vs_ide_path,
            'VSTSDB',
            'Deploy'
        )

        if os.path.exists(vs_tdb_path):
            path.append(vs_tdb_path)

        if os.path.exists(test_window_path):
            path.append(test_window_path)

        return path

    @property
    def __version(self):
        if not isinstance(self.__devenv_version, tuple):
            dev_env_dir = self.dev_env_directory

            if dev_env_dir is not None:
                command = ''.join([
                    '"',
                    os.path.join(dev_env_dir, 'devenv'),
                    '" /?\n'
                ])

                proc = subprocess.Popen(
                    'cmd',
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    shell=True
                )

                proc.stdin.write(command.encode('utf-8'))
                out, err = proc.communicate()
                proc.stdin.close()

                err = err.strip()

                if err:
                    self.__devenv_version = (None, None)
                    return self.__devenv_version

                for line in out.decode('utf-8').split('\n'):
                    if ' Visual Studio ' in line:
                        break
                else:
                    self.__devenv_version = (None, None)
                    return self.__devenv_version

                line = line.rstrip('.').strip()
                line = line.split(' Visual Studio ')[-1]

                common_version, version = line.split(' Version ')

                self.__devenv_version = (common_version, version)
            else:
                self.__devenv_version = (None, None)

        return self.__devenv_version

    @property
    def common_version(self) -> Optional[str]:
        return self.__version[0]

    @property
    def uncommon_version(self) -> Optional[str]:
        return self.__version[1]

    @property
    def version(self) -> Optional[float]:
        version = self.uncommon_version

        if version is not None:
            return float(int(version.split('.')[0]))

    def __iter__(self):
        install_directory = self.install_directory
        dev_env_directory = self.dev_env_directory

        if install_directory:
            install_directory += '\\'

        if dev_env_directory:
            dev_env_directory += '\\'

        env = dict(
            Path=self.path,
            VSINSTALLDIR=install_directory,
            DevEnvDir=dev_env_directory,
            VisualStudioVersion=self.version
        )

        toolsets = {
            'v142': '160',
            'v141': '150',
            'v140': '140',
            'v120': '120',
            'v110': '110',
            'v100': '100',
            'v90': '90'
        }

        toolset_version = self.c_info.toolset_version

        if toolset_version in toolsets:
            comn_tools = 'VS{0}COMNTOOLS'.format(
                toolsets[toolset_version]
            )
            env[comn_tools] = self.common_tools

        for key, value in env.items():
            if value is not None and value:
                if isinstance(value, list):
                    value = os.pathsep.join(value)
                yield key, str(value)

    def __str__(self):
        installation = self.c_info.cpp_installation

        if installation is None:
            return ''

        template = (
            '== {name} \n'
            '   description:        {description}\n'
            '   install date:       {install_date}\n'
            '   version:            {version}\n'
            '   version (friendly): {product_line_version}\n'
            '   display version:    {product_display_version}\n'
            '   path:               {path}\n'
            '   executable:         {product_path}\n'
            '   is complete:        {is_complete}\n'
            '   is prerelease:      {is_prerelease}\n'
            '   is launchable:      {is_launchable}\n'
            '   state:              {state}\n'
        )

        name = installation.display_name

        if name is None:
            if self.__name__ == 'VisualStudioInfo':
                name = 'Visual Studio'
            else:
                name = 'Build Tools'

        description = installation.description
        path = installation.path
        install_date = installation.install_date.strftime('%c')
        version = installation.version
        is_complete = installation.is_complete
        is_prerelease = installation.is_prerelease
        is_launchable = installation.is_launchable
        state = ', '.join(installation.state)
        product_path = os.path.join(path, installation.product_path)

        catalog = installation.catalog
        product_display_version = catalog.product_display_version
        product_line_version = catalog.product_line_version

        res = template.format(
            name=name,
            description=description,
            install_date=install_date,
            path=path,
            version=version,
            is_complete=is_complete,
            is_prerelease=is_prerelease,
            is_launchable=is_launchable,
            product_path=product_path,
            product_display_version=product_display_version,
            product_line_version=product_line_version,
            state=state
        )

        res = res.split('\n', 1)
        res[0] += '=' * (63 - len(res[0]))
        return '\n'.join(res)


class WindowsSDKInfo(object):

    def __init__(
        self, 
        environ: "Environment",
        c_info: VisualCInfo, 
        minimum_sdk_version: Optional[str] = None,
        strict_sdk_version: Optional[str] = None
    ):
        self.environment = environ
        self.c_info = c_info
        self.platform = environ.platform
        self.vc_version = c_info.version

        if (
            strict_sdk_version is not None and
            strict_sdk_version.startswith('10.0')
        ):
            if strict_sdk_version.count('.') == 2:
                strict_sdk_version += '.0'

        if (
            minimum_sdk_version is not None and
            minimum_sdk_version.startswith('10.0')
        ):
            if minimum_sdk_version.count('.') == 2:
                minimum_sdk_version += '.0'

        self._minimum_sdk_version = minimum_sdk_version
        self._strict_sdk_version = strict_sdk_version

        self._directory = None
        self._sdk_version = None
        self._version = None

    @property
    def extension_sdk_directory(self) -> Optional[str]:
        version = self.version

        if version.startswith('10'):
            extension_path = os.path.join(
                _PROGRAM_FILES_X86,
                'Microsoft SDKs',
                'Windows Kits',
                '10',
                'ExtensionSDKs'
            )
            if os.path.exists(extension_path):
                return extension_path

        sdk_path = _get_reg_value(
            'Microsoft SDKs\\Windows\\v' + version,
            'InstallationFolder'
        )

        if sdk_path:
            sdk_path = sdk_path.replace(
                'Windows Kits',
                'Microsoft SDKs\\Windows Kits'
            )
            extension_path = os.path.join(
                sdk_path[:-1],
                'Extension SDKs'
            )

            if os.path.exists(extension_path):
                return extension_path

    @property
    def lib_version(self) -> str:
        return self.sdk_version

    @property
    def ver_bin_path(self) -> str:
        bin_path = self.bin_path[:-1]

        version = self.version

        if version == '10.0':
            version = self.sdk_version

        ver_bin_path = os.path.join(bin_path, version)
        if os.path.exists(ver_bin_path):
            return ver_bin_path
        else:
            return bin_path

    @property
    def mssdk(self) -> Optional[str]:
        return self.directory

    @property
    def ucrt_version(self) -> Optional[str]:
        if self.version == '10.0':
            sdk_version = self.sdk_version
        else:
            sdk_versions = _read_reg_keys(
                'Microsoft SDKs\\Windows',
                True
            )
            if 'v10.0' in sdk_versions:
                sdk_version = _get_reg_value(
                    'Microsoft SDKs\\Windows\\v10.0',
                    'ProductVersion',
                    True
                )
            else:
                return

        if sdk_version.endswith('0'):
            return sdk_version
        else:
            return sdk_version[:-1]

    @property
    def ucrt_lib_directory(self) -> Optional[str]:
        if self.version == '10.0':
            directory = self.directory
            directory = os.path.join(
                directory,
                'Lib',
                self.sdk_version,
                'ucrt',
                self.platform
            )

        else:
            sdk_versions = _read_reg_keys(
                'Microsoft SDKs\\Windows',
                True
            )
            if 'v10.0' in sdk_versions:
                sdk_version = _get_reg_value(
                    'Microsoft SDKs\\Windows\\v10.0',
                    'ProductVersion',
                    True
                )
                directory = _get_reg_value(
                    'Microsoft SDKs\\Windows\\v10.0',
                    'InstallationFolder',
                    True
                )
                directory = os.path.join(
                    directory,
                    'Lib',
                    sdk_version,
                    'ucrt',
                    self.platform
                )
            else:
                return

        if os.path.exists(directory):
            if not directory.endswith('\\'):
                return directory + '\\'

            return directory

    @property
    def ucrt_headers_directory(self) -> Optional[str]:
        if self.version == '10.0':
            directory = self.directory
            directory = os.path.join(
                directory,
                'Include',
                self.sdk_version,
                'ucrt'
            )

        else:
            sdk_versions = _read_reg_keys(
                'Microsoft SDKs\\Windows',
                True
            )
            if 'v10.0' in sdk_versions:
                sdk_version = _get_reg_value(
                    'Microsoft SDKs\\Windows\\v10.0',
                    'ProductVersion',
                    True
                )
                directory = _get_reg_value(
                    'Microsoft SDKs\\Windows\\v10.0',
                    'InstallationFolder',
                    True
                )
                directory = os.path.join(
                    directory,
                    'Include',
                    sdk_version,
                    'ucrt'
                )
            else:
                return

        if os.path.exists(directory):
            if not directory.endswith('\\'):
                return directory + '\\'

            return directory

    @property
    def ucrt_sdk_directory(self) -> Optional[str]:
        directory = self.directory

        if self.version != '10.0':
            sdk_versions = _read_reg_keys(
                'Microsoft SDKs\\Windows',
                True
            )
            if 'v10.0' in sdk_versions:
                directory = _get_reg_value(
                    'Microsoft SDKs\\Windows\\v10.0',
                    'InstallationFolder',
                    True
                )
            else:
                return

        if os.path.exists(directory):
            if not directory.endswith('\\'):
                return directory + '\\'

            return directory

    @property
    def bin_path(self) -> Optional[str]:
        directory = self.directory
        if directory:
            bin_path = os.path.join(
                self.directory,
                'bin'
            )

            return bin_path + '\\'

    @property
    def lib(self) -> list:
        directory = self.directory
        if not directory:
            return []

        version = self.version
        if version == '10.0':
            version = self.sdk_version

        lib = []

        base_lib = os.path.join(
            directory,
            'lib',
            version,
        )
        if not os.path.exists(base_lib):
            base_lib = os.path.join(
                directory,
                'lib'
            )

        if os.path.exists(base_lib):
            if self.platform == 'x64':
                if os.path.exists(os.path.join(base_lib, 'x64')):
                    lib += [os.path.join(base_lib, 'x64')]

                ucrt = os.path.join(base_lib, 'ucrt', self.platform)
                um = os.path.join(base_lib, 'um', self.platform)
                if not os.path.exists(ucrt):
                    ucrt = os.path.join(base_lib, 'ucrt', 'amd64')

                if not os.path.exists(um):
                    um = os.path.join(base_lib, 'um', 'amd64')

            else:
                lib += [base_lib]
                ucrt = os.path.join(base_lib, 'ucrt', self.platform)
                um = os.path.join(base_lib, 'um', self.platform)

                if not os.path.exists(ucrt):
                    ucrt = os.path.join(base_lib, 'ucrt')

                if not os.path.exists(um):
                    um = os.path.join(base_lib, 'um')

            if os.path.exists(ucrt):
                lib += [ucrt]
            else:
                ucrt = self.ucrt_lib_directory
                if ucrt is not None:
                    lib += [ucrt]

            if os.path.exists(um):
                lib += [um]

        return lib

    @property
    def path(self) -> list:
        path = []
        ver_bin_path = self.ver_bin_path

        if self.platform == 'x64':
            bin_path = os.path.join(ver_bin_path, 'x64')
            if not os.path.exists(bin_path):
                bin_path = os.path.join(
                    ver_bin_path,
                    'amd64'
                )
        else:
            bin_path = os.path.join(ver_bin_path, 'x86')

            if not os.path.exists(bin_path):
                bin_path = ver_bin_path

        if os.path.exists(bin_path):
            path += [bin_path]

        bin_path = self.bin_path
        bin_path = os.path.join(
            bin_path,
            'x64'
        )

        if os.path.exists(bin_path):
            path += [bin_path]

        type_script_path = self.type_script_path
        if type_script_path is not None:
            path += [type_script_path]

        return path

    @property
    def type_script_path(self) -> Optional[str]:
        program_files = os.environ.get(
            'ProgramFiles(x86)',
            'C:\\Program Files (x86)'
        )
        type_script_path = os.path.join(
            program_files,
            'Microsoft SDKs',
            'TypeScript'
        )

        if os.path.exists(type_script_path):
            max_ver = 0.0
            for version in os.listdir(type_script_path):
                try:
                    version = float(version)
                except ValueError:
                    continue
                max_ver = max(max_ver, version)

            type_script_path = os.path.join(
                type_script_path,
                str(max_ver)
            )

            if os.path.exists(type_script_path):
                return type_script_path

    @property
    def include(self) -> list:
        directory = self.directory
        if self.version == '10.0':
            include_path = os.path.join(
                directory,
                'include',
                self.sdk_version
            )
        else:
            include_path = os.path.join(
                directory,
                'include'
            )

        includes = [include_path]

        for path in ('ucrt', 'cppwinrt', 'shared', 'um', 'winrt'):
            pth = os.path.join(include_path, path)
            if os.path.exists(pth):
                includes += [pth]
            elif path == 'ucrt' and self.version != '10.0':
                ucrt = self.ucrt_headers_directory
                if ucrt is not None:
                    includes += [ucrt]

        gl_include = os.path.join(include_path, 'gl')

        if os.path.exists(gl_include):
            includes += [gl_include]

        return includes

    @property
    def lib_path(self) -> list:
        return self.sdk_lib_path

    @property
    def sdk_lib_path(self) -> list:
        directory = self.directory
        version = self.version

        if version == '10.0':
            version = self.sdk_version

        union_meta_data = os.path.join(
            directory,
            'UnionMetadata',
            version
        )
        references = os.path.join(
            directory,
            'References',
            version
        )

        lib_path = []

        if os.path.exists(union_meta_data):
            lib_path += [union_meta_data]

        if os.path.exists(references):
            lib_path += [references]

        return lib_path

    @property
    def windows_sdks(self) -> list:
        """
        Windows SDK versions that are compatible with Visual C
        :return: compatible Windows SDK versions
        """
        ver = int(self.vc_version.split('.')[0])

        sdk_versions = []
        if ver >= 14:
            sdk_versions.extend(['v10.0'])
        if ver >= 12:
            sdk_versions.extend(['v8.1a', 'v8.1'])
        if ver >= 11:
            sdk_versions.extend(['v8.0a', 'v8.0'])
        if ver >= 10:
            sdk_versions.extend(['v7.1a', 'v7.1', 'v7.0a'])

        sdk_versions.extend(['v7.0', 'v6.1', 'v6.0a'])

        if (
            self._minimum_sdk_version is not None and
            self._minimum_sdk_version in sdk_versions
        ):
            index = sdk_versions.index(self._minimum_sdk_version)
            sdk_versions = sdk_versions[:index + 1]

        return sdk_versions

    @property
    def version(self) -> str:
        """
        This is used in the solution file to tell the compiler what SDK to use.
        We obtain a list of compatible Windows SDK versions for the
        Visual C version. We check and see if any  of the compatible SDK's are
        installed and if so we return that version.

        :return: Installed Windows SDK version
        """

        if self._version is None:
            sdk_versions = _read_reg_keys('Microsoft SDKs\\Windows', True)
            if self._strict_sdk_version is not None:
                if self._strict_sdk_version.startswith('10.0'):
                    keys = _read_reg_keys('Windows Kits\\Installed Roots')
                    if self._strict_sdk_version in keys:
                        self._version = '10.0'
                        return self._version

                    raise RuntimeError(
                        'Unable to locate Windows SDK ' +
                        self._strict_sdk_version
                    )

                if 'v' + self._strict_sdk_version in sdk_versions:
                    self._version = self._strict_sdk_version
                    return self._version

            for sdk in self.windows_sdks:
                if sdk in sdk_versions:
                    sdk_version = _get_reg_value(
                        'Microsoft SDKs\\Windows\\' + sdk,
                        'ProductVersion',
                        True
                    )

                    if sdk_version.startswith('10.0'):
                        while sdk_version.count('.') < 3:
                            sdk_version += '.0'

                    if self._strict_sdk_version is not None:
                        if self._strict_sdk_version == sdk_version:
                            self._version = sdk[1:]
                            return self._version

                        continue

                    if self._minimum_sdk_version is not None:
                        if self._minimum_sdk_version.count('.') > 1:
                            if sdk_version < self._minimum_sdk_version:
                                break

                    self._version = sdk[1:]
                    return self._version

            if self._strict_sdk_version is not None:
                raise RuntimeError(
                    'Unable to locate Windows SDK version ' +
                    self._strict_sdk_version
                )

            if self._minimum_sdk_version is not None:
                raise RuntimeError(
                    'Unable to locate Windows SDK vesion >= ' +
                    self._minimum_sdk_version
                )

            raise RuntimeError('Unable to locate Windows SDK')

        return self._version

    @property
    def sdk_version(self) -> str:
        """
        This is almost identical to target_platform. Except it returns the
        actual version of the Windows SDK not the truncated version.

        :return: actual Windows SDK version
        """

        if self._sdk_version is None:
            version = self.version

            if self._strict_sdk_version is None:
                self._sdk_version = _get_reg_value(
                    'Microsoft SDKs\\Windows\\v' + version,
                    'ProductVersion',
                    True
                )
                if self._sdk_version.startswith('10.0'):
                    while self._sdk_version.count('.') < 3:
                        self._sdk_version += '.0'

                return self._sdk_version

            if self._strict_sdk_version == version:
                self._sdk_version = _get_reg_value(
                    'Microsoft SDKs\\Windows\\v' + version,
                    'ProductVersion',
                    True
                )

                if self._sdk_version.startswith('10.0'):
                    while self._sdk_version.count('.') < 3:
                        self._sdk_version += '.0'

                return self._sdk_version

            sdk_version = _get_reg_value(
                'Microsoft SDKs\\Windows\\v' + version,
                'ProductVersion',
                True
            )

            if sdk_version.startswith('10.0'):
                while sdk_version.count('.') < 3:
                    sdk_version += '.0'

            if self._strict_sdk_version == sdk_version:
                self._sdk_version = sdk_version
                return self._sdk_version

            if self._strict_sdk_version.startswith('10.0'):
                keys = _read_reg_keys('Windows Kits\\Installed Roots')
                if self._strict_sdk_version in keys:
                    self._sdk_version = self._strict_sdk_version
                    return self._sdk_version

        return self._sdk_version

    @property
    def directory(self) -> Optional[str]:
        """
        Path to the Windows SDK version that has been found.
        :return: Windows SDK path
        """

        if self._directory is None:
            version = self.version

            if self._strict_sdk_version is None:
                self._directory = _get_reg_value(
                    'Microsoft SDKs\\Windows\\v' + version,
                    'InstallationFolder',
                    True
                )
                return self._directory

            if self._strict_sdk_version == version:
                self._directory = _get_reg_value(
                    'Microsoft SDKs\\Windows\\v' + version,
                    'InstallationFolder',
                    True
                )
                return self._directory

            sdk_version = _get_reg_value(
                'Microsoft SDKs\\Windows\\v' + version,
                'ProductVersion'
            )

            if sdk_version.startswith('10.0'):
                while sdk_version.count('.') < 3:
                    sdk_version += '.0'

            if self._strict_sdk_version == sdk_version:
                self._directory = _get_reg_value(
                    'Microsoft SDKs\\Windows\\v' + version,
                    'InstallationFolder',
                    True
                )
                return self._directory

            if self._strict_sdk_version.startswith('10.0'):
                keys = _read_reg_keys('Windows Kits\\Installed Roots')
                if self._strict_sdk_version in keys:
                    self._directory = _get_reg_value(
                        'Microsoft SDKs\\Windows\\v' + version,
                        'InstallationFolder',
                        True
                    )

                    return self._directory

        return self._directory

    def __iter__(self):
        ver_bin_path = self.ver_bin_path
        directory = self.directory

        if ver_bin_path:
            ver_bin_path += '\\'

        if directory and not directory.endswith('\\'):
            directory += '\\'

        lib_version = self.lib_version
        if not lib_version.endswith('\\'):
            lib_version += '\\'

        sdk_version = self.sdk_version
        if not sdk_version.endswith('\\'):
            sdk_version += '\\'

        env = dict(
            LIB=self.lib,
            Path=self.path,
            LIBPATH=self.lib_path,
            INCLUDE=self.include,
            UniversalCRTSdkDir=self.ucrt_sdk_directory,
            ExtensionSdkDir=self.extension_sdk_directory,
            WindowsSdkVerBinPath=ver_bin_path,
            UCRTVersion=self.ucrt_version,
            WindowsSDKLibVersion=lib_version,
            WindowsSDKVersion=sdk_version,
            WindowsSdkDir=directory,
            WindowsLibPath=self.lib_path,
            WindowsSdkBinPath=self.bin_path,
            DISTUTILS_USE_SDK=1,
            MSSDK=self.directory
        )

        for key, value in env.items():
            if value is not None and value:
                if isinstance(value, list):
                    value = os.pathsep.join(value)
                yield key, str(value)

    def __str__(self):
        template = (
            '== Windows SDK ================================================\n'
            '   version:     {target_platform}\n'
            '   sdk version: {windows_sdk_version}\n'
            '   path:        {target_platform_path}\n'
            '\n'
            '== Universal CRT ==============================================\n'
            '   version:           {ucrt_version}\n'
            '   path:              {ucrt_sdk_directory}\n'
            '   lib directory:     {ucrt_lib_directory}\n'
            '   headers directory: {ucrt_headers_directory}\n'
            '\n'
            '== Extension SDK ==============================================\n'
            '   path: {extension_sdk_directory}\n'
            '\n'
            '== TypeScript =================================================\n'
            '   path: {type_script_path}\n'
        )

        return template.format(
            target_platform=self.version,
            windows_sdk_version=self.sdk_version,
            target_platform_path=self.directory,
            extension_sdk_directory=self.extension_sdk_directory,
            ucrt_sdk_directory=self.ucrt_sdk_directory,
            ucrt_headers_directory=self.ucrt_headers_directory,
            ucrt_lib_directory=self.ucrt_lib_directory,
            ucrt_version=self.ucrt_version,
            type_script_path=self.type_script_path,
        )


class NETInfo(object):

    def __init__(
        self,
        environ: "Environment",
        c_info: VisualCInfo,
        sdk_version: str,
        minimum_net_version: Optional[str] = None,
        strict_net_version: Optional[str] = None
    ):

        self.environment = environ
        self.platform = environ.platform
        self.c_info = c_info
        self.vc_version = c_info.version
        self.sdk_version = sdk_version
        self._minimum_net_version = minimum_net_version
        self._strict_net_version = strict_net_version
        self._version_32 = None
        self._version_64 = None

    @property
    def version(self) -> str:
        """
        .NET Version
        :return: returns the version associated with the architecture
        """
        if self.platform == 'x64':
            return self.version_64
        else:
            return self.version_32

    @property
    def version_32(self) -> str:
        """
        .NET 32bit framework version
        :return: x86 .NET framework version
        """
        if self._version_32 is None:
            target_framework = None
            installation = self.c_info.cpp_installation

            if installation is not None:
                for package in installation.packages.msi:
                    if (
                        package.id.startswith('Microsoft.Net') and
                        package.id.endswith('TargetingPack')
                    ):

                        if self._strict_net_version is not None:
                            if self._strict_net_version == package:
                                self._version_32 = 'v' + package.version
                                return self._version_32
                            else:
                                continue

                        if self._minimum_net_version is not None:
                            if package < self._minimum_net_version:
                                continue

                        if target_framework is None:
                            target_framework = package
                        elif package > target_framework:
                            target_framework = package

                if target_framework is not None:
                    self._version_32 = 'v' + target_framework.version
                    return self._version_32

            target_framework = _get_reg_value(
                'VisualStudio\\SxS\\VC7',
                'FrameworkVer32'
            )

            if target_framework:
                if self._strict_net_version is not None:
                    if target_framework[1:] == self._strict_net_version:
                        self._version_32 = target_framework
                        return self._version_32
                elif self._minimum_net_version is not None:
                    if target_framework[1:] >= self._strict_net_version:
                        self._version_32 = target_framework
                        return self._version_32
                else:
                    self._version_32 = target_framework
                    return self._version_32

            versions = list(
                key for key in _read_reg_keys('.NETFramework\\', True)
                if key.startswith('v')
            )

            target_framework = None

            if self._strict_net_version is not None:
                if 'v' + self._strict_net_version in versions:
                    self._version_32 = 'v' + self._strict_net_version
                    return self._version_32
            else:
                for version in versions:
                    if self._minimum_net_version is not None:
                        if version[1:] < self._minimum_net_version:
                            continue

                    if target_framework is None:
                        target_framework = version[1:]
                    elif target_framework < version[1:]:
                        target_framework = version[1:]

                if target_framework is not None:
                    self._version_32 = 'v' + target_framework
                    return self._version_32

            net_path = os.path.join(
                '%SystemRoot%',
                'Microsoft.NET',
                'Framework'
            )
            net_path = os.path.expandvars(net_path)
            if os.path.exists(net_path):
                versions = [item[1:] for item in os.listdir(net_path)]
                if self._strict_net_version is not None:
                    if self._strict_net_version in versions:
                        self._version_32 = 'v' + self._strict_net_version
                        return self._version_32

                    raise RuntimeError(
                        'Unable to locate .NET version ' +
                        self._strict_net_version
                    )

                for version in versions:
                    if (
                        self._minimum_net_version is not None and
                        version < self._minimum_net_version
                    ):
                        continue

                    if target_framework is None:
                        target_framework = version
                    elif target_framework < version:
                        target_framework = version

                if target_framework:
                    self._version_32 = 'v' + target_framework
                    return self._version_32

            if self._strict_net_version is not None:
                raise RuntimeError(
                    'Unable to locate .NET version ' +
                    self._strict_net_version
                )

            if self._minimum_net_version is not None:
                raise RuntimeError(
                    'Unable to locate .NET version ' +
                    self._minimum_net_version +
                    ' or above.'
                )

            self._version_32 = ''

        return self._version_32

    @property
    def version_64(self) -> str:
        """
        .NET 64bit framework version
        :return: x64 .NET framework version
        """

        if self._version_64 is None:
            target_framework = None
            installation = self.c_info.cpp_installation

            if installation is not None:
                for package in installation.packages.msi:
                    if (
                        package.id.startswith('Microsoft.Net') and
                        package.id.endswith('TargetingPack')
                    ):

                        if self._strict_net_version is not None:
                            if self._strict_net_version == package:
                                self._version_64 = 'v' + package.version
                                return self._version_64
                            else:
                                continue

                        if self._minimum_net_version is not None:
                            if package < self._minimum_net_version:
                                continue

                        if target_framework is None:
                            target_framework = package
                        elif package > target_framework:
                            target_framework = package

                if target_framework is not None:
                    self._version_64 = 'v' + target_framework.version
                    return self._version_64

            target_framework = _get_reg_value(
                'VisualStudio\\SxS\\VC7',
                'FrameworkVer64'
            )

            if target_framework:
                if self._strict_net_version is not None:
                    if target_framework[1:] == self._strict_net_version:
                        self._version_64 = target_framework
                        return self._version_64

                elif self._minimum_net_version is not None:
                    if target_framework[1:] >= self._strict_net_version:
                        self._version_64 = target_framework
                        return self._version_64

                else:
                    self._version_64 = target_framework
                    return self._version_64

            versions = list(
                key for key in _read_reg_keys('.NETFramework\\', True)
                if key.startswith('v')
            )

            target_framework = None

            if self._strict_net_version is not None:
                if 'v' + self._strict_net_version in versions:
                    self._version_64 = 'v' + self._strict_net_version
                    return self._version_64
            else:
                for version in versions:
                    if self._minimum_net_version is not None:
                        if version[1:] < self._minimum_net_version:
                            continue

                    if target_framework is None:
                        target_framework = version[1:]
                    elif target_framework < version[1:]:
                        target_framework = version[1:]

                if target_framework is not None:
                    self._version_64 = 'v' + target_framework
                    return self._version_64

            net_path = os.path.join(
                '%SystemRoot%',
                'Microsoft.NET',
                'Framework64'
            )
            net_path = os.path.expandvars(net_path)
            if os.path.exists(net_path):
                versions = [item[1:] for item in os.listdir(net_path)]
                if self._strict_net_version is not None:
                    if self._strict_net_version in versions:
                        self._version_64 = 'v' + self._strict_net_version
                        return self._version_64

                    raise RuntimeError(
                        'Unable to locate .NET version ' +
                        self._strict_net_version
                    )

                for version in versions:
                    if (
                        self._minimum_net_version is not None and
                        version < self._minimum_net_version
                    ):
                        continue

                    if target_framework is None:
                        target_framework = version
                    elif target_framework < version:
                        target_framework = version

                if target_framework:
                    self._version_64 = 'v' + target_framework
                    return self._version_64

            if self._strict_net_version is not None:
                raise RuntimeError(
                    'Unable to locate .NET version ' +
                    self._strict_net_version
                )

            if self._minimum_net_version is not None:
                raise RuntimeError(
                    'Unable to locate .NET version ' +
                    self._minimum_net_version +
                    ' or above.'
                )

            self._version_64 = ''

        return self._version_64

    @property
    def directory(self) -> str:
        if self.platform == 'x64':
            return self.directory_64
        else:
            return self.directory_32

    @property
    def directory_32(self) -> str:
        """
        .NET 32bit path
        :return: path to x86 .NET
        """
        directory = _get_reg_value(
            'VisualStudio\\SxS\\VC7\\',
            'FrameworkDir32'
        )
        if not directory:
            directory = os.path.join(
                '%SystemRoot%',
                'Microsoft.NET',
                'Framework'
            )
            directory = os.path.expandvars(directory)
        else:
            directory = directory[:-1]

        if os.path.exists(directory):
            return directory

        return ''

    @property
    def directory_64(self) -> str:
        """
        .NET 64bit path
        :return: path to x64 .NET
        """

        directory = _get_reg_value(
            'VisualStudio\\SxS\\VC7\\',
            'FrameworkDir64'
        )
        if not directory:
            directory = os.path.join(
                '%SystemRoot%',
                'Microsoft.NET',
                'Framework64'
            )
            directory = os.path.expandvars(directory)
        else:
            directory = directory[:-1]

        if os.path.exists(directory):
            return directory

        return ''

    @property
    def preferred_bitness(self) -> str:
        return '32' if self.platform == 'x86' else '64'

    @property
    def netfx_sdk_directory(self) -> Optional[str]:
        framework = '.'.join(self.version[1:].split('.')[:2])
        ver = float(int(self.vc_version.split('.')[0]))

        if ver in (9.0, 10.0, 11.0, 12.0):
            key = 'Microsoft SDKs\\Windows\\v{0}\\'.format(self.sdk_version)
        else:
            key = 'Microsoft SDKs\\NETFXSDK\\{0}\\'.format(framework)

        net_fx_path = _get_reg_value(
            key,
            'KitsInstallationFolder',
            wow6432=True
        )

        if net_fx_path and os.path.exists(net_fx_path):
            return net_fx_path

    @property
    def net_fx_tools_directory(self) -> Optional[str]:
        framework = self.version[1:].split('.')[:2]

        if framework[0] == '4':
            net_framework = '40'
        else:
            net_framework = ''.join(framework)

        net_fx_key = (
            'WinSDK-NetFx{framework}Tools-{platform}'
        ).format(
            framework=''.join(net_framework),
            platform=self.platform
        )

        framework = '.'.join(framework)
        ver = float(int(self.vc_version.split('.')[0]))

        if ver in (9.0, 10.0, 11.0, 12.0):
            key = 'Microsoft SDKs\\Windows\\v{0}\\{1}\\'.format(
                self.sdk_version,
                net_fx_key
            )

            if self.sdk_version in ('6.0A', '6.1'):
                key = key.replace(net_fx_key, 'WinSDKNetFxTools')

            net_fx_path = _get_reg_value(
                key,
                'InstallationFolder',
                wow6432=True
            )
        else:
            key = 'Microsoft SDKs\\NETFXSDK\\{0}\\{1}\\'.format(
                framework,
                net_fx_key
            )
            net_fx_path = _get_reg_value(
                key,
                'InstallationFolder',
                wow6432=True
            )

        if net_fx_path and os.path.exists(net_fx_path):
            return net_fx_path

    @property
    def add(self) -> str:
        return '__DOTNET_ADD_{0}BIT'.format(self.preferred_bitness)

    @property
    def net_tools(self) -> list:

        version = float(int(self.vc_version.split('.')[0]))
        if version <= 10.0:
            include32 = True
            include64 = self.platform == 'x64'
        else:
            include32 = self.platform == 'x86'
            include64 = self.platform == 'x64'

        tools = []
        if include32:
            tools += [
                os.path.join(self.directory_32, self.version_32)
            ]
        if include64:
            tools += [
                os.path.join(self.directory_64, self.version_64)
            ]

        return tools

    @property
    def executable_path_x64(self) -> Optional[str]:
        tools_directory = self.net_fx_tools_directory
        if not tools_directory:
            return

        if 'NETFX' in tools_directory:
            if 'x64' in tools_directory:
                return tools_directory
            else:
                tools_directory = os.path.join(tools_directory, 'x64')
                if os.path.exists(tools_directory):
                    return tools_directory

    @property
    def executable_path_x86(self) -> Optional[str]:
        tools_directory = self.net_fx_tools_directory
        if not tools_directory:
            return

        if 'NETFX' in tools_directory:
            if 'x64' in tools_directory:
                return (
                    os.path.split(os.path.split(tools_directory)[0])[0] + '\\'
                )
            else:
                return tools_directory
        return None

    @property
    def lib(self) -> list:
        sdk_directory = self.netfx_sdk_directory
        if not sdk_directory:
            return []

        sdk_directory = os.path.join(sdk_directory, 'lib', 'um')

        if self.platform == 'x64':
            lib_dir = os.path.join(sdk_directory, 'x64')
            if not os.path.exists(lib_dir):
                lib_dir = os.path.join(sdk_directory, 'amd64')
        else:
            lib_dir = os.path.join(sdk_directory, 'x86')
            if not os.path.exists(lib_dir):
                lib_dir = sdk_directory

        if os.path.exists(lib_dir):
            return [lib_dir]

        return []

    @property
    def path(self) -> list:
        path = []
        directory = self.directory

        pth = os.path.join(
            directory,
            self.version
        )

        if os.path.exists(pth):
            path += [pth]
        else:
            match = None
            version = self.version
            versions = [
                item[1:] for item in os.listdir(directory)
                if item.startswith('v')
            ]
            for ver in versions:
                if version > ver:
                    if match is None:
                        match = ver
                    elif ver > match:
                        match = ver

            if match is not None:
                pth = os.path.join(
                    directory,
                    'v' + match
                )
                path += [pth]

        net_fx_tools = self.net_fx_tools_directory
        if net_fx_tools:
            path += [net_fx_tools]

        return path

    @property
    def lib_path(self) -> list:
        path = []
        directory = self.directory

        pth = os.path.join(
            directory,
            self.version
        )

        if os.path.exists(pth):
            path += [pth]
        else:
            match = None
            version = self.version
            versions = [
                item[1:] for item in os.listdir(directory)
                if item.startswith('v')
            ]
            for ver in versions:
                if version > ver:
                    if match is None:
                        match = ver
                    elif ver > match:
                        match = ver

            if match is not None:
                pth = os.path.join(
                    directory,
                    'v' + match
                )
                path += [pth]

        return path

    @property
    def include(self) -> list:
        sdk_directory = self.netfx_sdk_directory

        if sdk_directory:
            include_dir = os.path.join(sdk_directory, 'include', 'um')

            if os.path.exists(include_dir):
                return [include_dir]

        return []

    def __iter__(self):
        directory = self.directory
        if directory:
            directory += '\\'

        env = dict(
            WindowsSDK_ExecutablePath_x64=self.executable_path_x64,
            WindowsSDK_ExecutablePath_x86=self.executable_path_x86,
            LIB=self.lib,
            Path=self.path,
            LIBPATH=self.lib_path,
            INCLUDE=self.include,
            __DOTNET_PREFERRED_BITNESS=self.preferred_bitness,
            FrameworkDir=directory,
            NETFXSDKDir=self.netfx_sdk_directory,
        )

        version = self.version[1:].split('.')
        if version[0] == '4':
            version = ['4', '0']
        else:
            version = version[:2]

        net_p = 'v' + ('.'.join(version))

        env[self.add] = '1'
        if self.platform == 'x64':
            directory_64 = self.directory_64

            if directory_64:
                loc = os.path.join(directory_64, net_p)

                if os.path.exists(loc):
                    version_64 = loc
                else:
                    for p in os.listdir(directory_64):
                        if not os.path.isdir(os.path.join(directory_64, p)):
                            continue

                        if p[1:] < net_p[1:]:
                            continue

                        version_64 = p
                        break
                    else:
                        version_64 = self.version_64

                directory_64 += '\\'
            else:
                version_64 = None

            env['FrameworkDir64'] = directory_64
            env['FrameworkVersion64'] = version_64
            env['FrameworkVersion'] = version_64

        else:
            directory_32 = self.directory_32

            if directory_32:
                loc = os.path.join(directory_32, net_p)

                if not os.path.exists(loc):
                    for p in os.listdir(directory_32):
                        if not os.path.isdir(os.path.join(directory_32, p)):
                            continue

                        if p[1:] < net_p[1:]:
                            continue

                        version_32 = p
                        break
                    else:
                        version_32 = self.version_64

                else:
                    version_32 = loc

                directory_32 += '\\'
            else:
                version_32 = None

            env['FrameworkDir32'] = directory_32
            env['FrameworkVersion32'] = version_32
            env['FrameworkVersion'] = version_32

        framework = env['FrameworkVersion'][1:].split('.')[:2]

        framework_version_key = (
            'Framework{framework}Version'.format(framework=''.join(framework))
        )
        env[framework_version_key] = 'v' + '.'.join(framework)

        for key, value in env.items():
            if value is not None and value:
                if isinstance(value, list):
                    value = os.pathsep.join(value)
                yield key, str(value)

    def __str__(self):
        template = (
            '== .NET =======================================================\n'
            '   version:    {target_framework}\n'
            '\n'
            '   -- x86 -----------------------------------------------------\n'
            '      version: {framework_version_32}\n'
            '      path:    {framework_dir_32}\n'
            '   -- x64 -----------------------------------------------------\n'
            '      version: {framework_version_64}\n'
            '      path:    {framework_dir_64}\n'
            '   -- NETFX ---------------------------------------------------\n'
            '      path:         {net_fx_tools_directory}\n'
            '      x86 exe path: {executable_path_x86}\n'
            '      x64 exe path: {executable_path_x64}\n'
        )
        return template.format(
            target_framework=self.version,
            framework_version_32=self.version_32,
            framework_dir_32=self.directory_32,
            framework_version_64=self.version_64,
            framework_dir_64=self.directory_64,
            net_fx_tools_directory=self.net_fx_tools_directory,
            executable_path_x64=self.executable_path_x64,
            executable_path_x86=self.executable_path_x86,
        )


class Environment(object):
    _original_environment = {k_: v_ for k_, v_ in os.environ.items()}

    def __init__(
        self,
        minimum_c_version: Optional[Union[int, float]] = None,
        strict_c_version: Optional[Union[int, float]] = None,
        minimum_toolkit_version: Optional[int] = None,
        strict_toolkit_version: Optional[int] = None,
        minimum_sdk_version: Optional[str] = None,
        strict_sdk_version: Optional[str] = None,
        minimum_net_version: Optional[str] = None,
        strict_net_version: Optional[str] = None,
        vs_version: Optional[Union[str, int]] = None
    ):
        self.python = PythonInfo()

        self.visual_c = VisualCInfo(
            self,
            minimum_c_version,
            strict_c_version,
            minimum_toolkit_version,
            strict_toolkit_version,
            vs_version
        )

        self.visual_studio = VisualStudioInfo(
            self,
            self.visual_c
        )

        self.windows_sdk = WindowsSDKInfo(
            self,
            self.visual_c,
            minimum_sdk_version,
            strict_sdk_version
        )

        self.dot_net = NETInfo(
            self,
            self.visual_c,
            self.windows_sdk.version,
            minimum_net_version,
            strict_net_version
        )

    def reset_environment(self):
        for key in list(os.environ.keys())[:]:
            if key not in self._original_environment:
                del os.environ[key]

        os.environ.update(self._original_environment)

    @property
    def machine_architecture(self):
        import platform
        return 'x64' if '64' in platform.machine() else 'x86'

    @property
    def platform(self):
        """
        :return: x86 or x64
        """
        import platform

        win_64 = self.machine_architecture == 'x64'
        python_64 = platform.architecture()[0] == '64bit' and win_64

        return 'x64' if python_64 else 'x86'

    @property
    def configuration(self):
        """
        Build configuration
        :return: one of ReleaseDLL, DebugDLL
        """

        if os.path.splitext(sys.executable)[0].endswith('_d'):
            config = 'Debug'
        else:
            config = 'Release'

        return config

    def __iter__(self):
        for item in self.build_environment.items():
            yield item

    @property
    def build_environment(self):
        """
        This would be the work horse. This is where all of the gathered
        information is put into a single container and returned.
        The information is then added to os.environ in order to allow the
        build process to run properly.

        List of environment variables generated:
        PATH
        LIBPATH
        LIB
        INCLUDE
        Platform
        FrameworkDir
        FrameworkVersion
        FrameworkDIR32
        FrameworkVersion32
        FrameworkDIR64
        FrameworkVersion64
        VCToolsRedistDir
        VCINSTALLDIR
        VCToolsInstallDir
        VCToolsVersion
        WindowsLibPath
        WindowsSdkDir
        WindowsSDKVersion
        WindowsSdkBinPath
        WindowsSdkVerBinPath
        WindowsSDKLibVersion
        __DOTNET_ADD_32BIT
        __DOTNET_ADD_64BIT
        __DOTNET_PREFERRED_BITNESS
        Framework{framework version}Version
        NETFXSDKDir
        UniversalCRTSdkDir
        UCRTVersion
        ExtensionSdkDir

        These last 2 are set to ensure that distuils uses these environment
        variables when compiling libopenzwave.pyd
        MSSDK
        DISTUTILS_USE_SDK

        :return: dict of environment variables
        """
        path = os.environ.get('Path', '')

        env = dict(
            __VSCMD_PREINIT_PATH=path,
            Platform=self.platform,
            VSCMD_ARG_app_plat='Desktop',
            VSCMD_ARG_HOST_ARCH=self.platform,
            VSCMD_ARG_TGT_ARCH=self.platform,
            __VSCMD_script_err_count='0'
        )

        path = set(item.strip() for item in path.split(';') if item.strip())
        env_path = set()

        def update_env(cls):
            for key, value in cls:
                if key == 'Path':
                    for item in value.split(';'):
                        env_path.add(item)
                    continue

                if key in env:
                    env[key] += ';' + value
                else:
                    env[key] = value

        update_env(self.visual_c)
        update_env(self.visual_studio)
        update_env(self.windows_sdk)
        update_env(self.dot_net)

        env_path = [item for item in env_path if item not in path]
        env_path = ';'.join(env_path)

        if env_path:
            env_path += ';'

        env['Path'] = env_path + ';'.join(path)

        return env

    def __str__(self):
        template = (
            'Machine architecture: {machine_architecture}\n'
            'Build architecture: {architecture}\n'
        )

        res = [
            template.format(
                machine_architecture=self.machine_architecture,
                architecture=self.platform
            ),
            str(self.python),
            str(self.visual_studio),
            str(self.visual_c),
            str(self.windows_sdk),
            str(self.dot_net),
        ]

        return '\n'.join(res)


def setup_environment(
    minimum_c_version: Optional[Union[int, float]] = None,
    strict_c_version: Optional[Union[int, float]] = None,
    minimum_toolkit_version: Optional[int] = None,
    strict_toolkit_version: Optional[int] = None,
    minimum_sdk_version: Optional[str] = None,
    strict_sdk_version: Optional[str] = None,
    minimum_net_version: Optional[str] = None,
    strict_net_version: Optional[str] = None,
    vs_version: Optional[Union[str, int]] = None
):
    """
    Main entry point.

    :param minimum_c_version: The lowest MSVC compiler version to allow.
    :type minimum_c_version: optional - int, float

    :param strict_c_version: The MSVC compiler version that MUST be used.
      ie 14.0, 14.2
    :type strict_c_version: optional - int or float

    :param minimum_toolkit_version: The lowest build tools version to allow.
    :type minimum_toolkit_version: optional - int

    :param strict_toolkit_version: The build tools version that MUST be used.
      ie 142, 143
    :type strict_toolkit_version: optional - int

    :param minimum_sdk_version: The lowest SDK version to allow.
      This can work several ways, if you want to specify a specific version as
      the minimum `"10.0.22000.0"` or if you want to make sure that only
      Windows 10 SDK's get used `"10.0"`
    :type minimum_sdk_version: optional - str

    :param strict_sdk_version: The Windows SDK that MUST be used.
      Whole version only.
    :type strict_sdk_version: optional - str

    :param minimum_net_version: Works the same as minimum_sdk_version
    :type minimum_net_version: optional - str

    :param strict_net_version: works the same as strict_sdk_version
    :type strict_net_version: optional - str

    :param vs_version: The version of visual studio you want to use.
      This can be one of the following version types.

         * version: `str("16.10.31515.178")`
         * display version:`str("16.10.4")`
         * product line version: `int(2019)`.

      If you have 2 installations that share the same product line version
      the installation with the  higher version will get used. An example of
      this is Visual Studio 20019 and Build Tools 2019. If you want to specify
      a specific installation  in this case then use the version or
      display version options.
    :type vs_version: optional - str, int

    :return: Environment instance
    :rtype: Environment
    """

    distutils.log.set_threshold(distutils.log.DEBUG)

    if not _IS_WIN:
        raise RuntimeError(
            'This script will only work with a Windows opperating system.'
        )

    distutils.log.debug(
        'Setting up Windows build environment, please wait.....'
    )

    python_version = sys.version_info[:2]
    if minimum_c_version is None:
        if python_version == (3, 10):
            minimum_c_version = 14.2
        elif python_version == (3, 9):
            minimum_c_version = 14.2
        elif python_version == (3, 8):
            minimum_c_version = 14.0
        elif python_version == (3, 7):
            minimum_c_version = 14.0
        elif python_version == (3, 6):
            minimum_c_version = 14.0
        elif python_version == (3, 5):
            minimum_c_version = 12.0
        elif python_version == (3, 4):
            minimum_c_version = 12.0
        else:
            raise RuntimeError(
                'ozw does not support this version of python'
            )

    environment = Environment(
        minimum_c_version,
        strict_c_version,
        minimum_toolkit_version,
        strict_toolkit_version,
        minimum_sdk_version,
        strict_sdk_version,
        minimum_net_version,
        strict_net_version,
        vs_version
    )

    distutils.log.debug('\n' + str(environment) + '\n\n')
    distutils.log.debug('SET ENVIRONMENT VARIABLES')
    distutils.log.debug('------------------------------------------------')
    distutils.log.debug('\n')

    for key, value in environment.build_environment.items():
        old_val = os.environ.get(key, value)
        if old_val != value:
            if ';' in old_val or ';' in value:
                old_val = set(old_val.split(';'))
                value = set(';'.split(value))

                value = old_val.union(value)
                value = ';'.join(item for item in value)

        distutils.log.debug(key + '=' + value)
        os.environ[key] = value

    distutils.log.debug('\n\n')
    distutils.log.set_threshold(distutils.log.ERROR)

    return environment


if __name__ == '__main__':
    distutils.log.set_threshold(distutils.log.DEBUG)

    # build tools   2019 '16.10.31515.178'  '16.10.4'
    # visual studio 2019 '16.11.31729.503'  '16.11.5'

    envr = setup_environment()  # vs_version='16.10.4')
    print()
    print()
    print('SET ENVIRONMENT VARIABLES')
    print('------------------------------------------------')
    print()
    for k, v in envr:
        if os.pathsep in v:
            v = v.split(';')
            if not v[-1]:
                v = v[:-1]

        print(k + ':', v)
        print()
