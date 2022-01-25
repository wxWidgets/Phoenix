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
# #############################################################################


# #############################################################################
#
# This software is OSI Certified Open Source Software.
# OSI Certified is a certification mark of the Open Source Initiative.
#
# Copyright (c) 2006-2013, Thomas Heller.
# Copyright (c) 2014, Comtypes Developers.
# All rights reserved.
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
# #############################################################################

import weakref
import ctypes
import sys
import atexit
import datetime
from _ctypes import COMError
from ctypes import POINTER, HRESULT
from ctypes.wintypes import (
    LPCOLESTR,
    ULONG,
    USHORT,
    LPCWSTR,
    LPVOID,
    LCID,
    DWORD,
    LONG,
    WORD,
    BYTE,
    INT,
    BOOL,
    SHORT,
    UINT,
    FLOAT,
    DOUBLE,
    VARIANT_BOOL,
)

UBYTE = ctypes.c_ubyte
ULONGLONG = ctypes.c_ulonglong
LONGLONG = ctypes.c_longlong
VARTYPE = USHORT
PVOID = ctypes.c_void_p
ENUM = ctypes.c_uint
PULONGLONG = POINTER(ctypes.c_ulonglong)

_oleaut32 = ctypes.windll.oleaut32
_ole32_nohresult = ctypes.windll.ole32
_ole32 = ctypes.oledll.ole32
_kernel32 = ctypes.windll.kernel32

_StringFromCLSID = _ole32.StringFromCLSID
_CoTaskMemFree = ctypes.windll.ole32.CoTaskMemFree
_CLSIDFromString = _ole32.CLSIDFromString
_VariantClear = _oleaut32.VariantClear

_SafeArrayLock = _oleaut32.SafeArrayLock
_SafeArrayLock.restype = HRESULT

_SafeArrayUnlock = _oleaut32.SafeArrayUnlock
_SafeArrayUnlock.restype = HRESULT

_GetUserDefaultLCID = _kernel32.GetUserDefaultLCID
_GetUserDefaultLCID.restype = LCID

_FileTimeToSystemTime = _kernel32.FileTimeToSystemTime
_FileTimeToSystemTime.restype = BOOL

_SystemTimeToFileTime = _kernel32.SystemTimeToFileTime
_SystemTimeToFileTime.restype = BOOL

ctypes.pythonapi.PyInstanceMethod_New.argtypes = [ctypes.py_object]
ctypes.pythonapi.PyInstanceMethod_New.restype = ctypes.py_object
PyInstanceMethod_Type = type(ctypes.pythonapi.PyInstanceMethod_New(id))

CLSCTX_SERVER = 5
CLSCTX_ALL = 7
COINIT_APARTMENTTHREADED = 0x2
MAXUINT = 0xFFFFFFFF

ERROR_FILE_NOT_FOUND = 0x00000002
ERROR_NOT_FOUND = 0x00000490


def HRESULT_FROM_WIN32(x):
    return x


# Constants
E_NOTFOUND = HRESULT_FROM_WIN32(ERROR_NOT_FOUND)
E_FILENOTFOUND = HRESULT_FROM_WIN32(ERROR_FILE_NOT_FOUND)

VT_EMPTY = 0
VT_NULL = 1
VT_I2 = 2
VT_I4 = 3
VT_R4 = 4
VT_R8 = 5
VT_CY = 6
VT_DATE = 7
VT_BSTR = 8
VT_BOOL = 11
VT_I1 = 16
VT_UI1 = 17
VT_UI2 = 18
VT_UI4 = 19
VT_I8 = 20
VT_UI8 = 21
VT_INT = 22
VT_UINT = 23


_PARAMFLAGS = {
    "in": 1,
    "out": 2,
    "lcid": 4,
    "retval": 8,
    "optional": 16,
}


def instancemethod(func, inst, _):
    mth = PyInstanceMethod_Type(func)
    if inst is None:
        return mth
    return mth.__get__(inst)


def CoInitialize():
    flags = getattr(sys, "coinit_flags", COINIT_APARTMENTTHREADED)
    _ole32.CoInitializeEx(None, flags)


def CoUninitialize():
    _ole32_nohresult.CoUninitialize()


def CoCreateInstance(clsid, interface=None, clsctx=None, punkouter=None):
    if clsctx is None:
        clsctx = CLSCTX_SERVER

    if interface is None:
        interface = IUnknown

    p = POINTER(interface)()
    iid = interface._iid_  # NOQA
    _ole32.CoCreateInstance(
        ctypes.byref(clsid),
        punkouter,
        clsctx,
        ctypes.byref(iid),
        ctypes.byref(p)
    )
    return p


def _shutdown(
    func=_ole32_nohresult.CoUninitialize,
    _exc_clear=getattr(sys, "exc_clear", lambda: None)
):
    _exc_clear()

    try:
        func()
    except WindowsError:
        pass

    if _cominterface_meta is not None:
        _cominterface_meta._com_shutting_down = True


class ReferenceEmptyClass(object):
    pass


class Patch(object):
    def __init__(self, target):
        self.target = target

    def __call__(self, patches):
        for name, value in list(vars(patches).items()):
            if name in vars(ReferenceEmptyClass):
                continue
            n_replace = getattr(value, '__no_replace', False)
            if n_replace and hasattr(self.target, name):
                continue

            setattr(self.target, name, value)


def no_replace(f):
    f.__no_replace = True
    return f


class tagSAFEARRAYBOUND(ctypes.Structure):
    _fields_ = [
        ('cElements', DWORD),
        ('lLbound', LONG),
    ]


SAFEARRAYBOUND = tagSAFEARRAYBOUND


class tagSAFEARRAY(ctypes.Structure):
    _fields_ = [
        ('cDims', USHORT),
        ('fFeatures', USHORT),
        ('cbElements', DWORD),
        ('cLocks', DWORD),
        ('pvData', PVOID),
        ('rgsabound', SAFEARRAYBOUND * 1),
    ]


SAFEARRAY = tagSAFEARRAY
LPSAFEARRAY = POINTER(SAFEARRAY)

_SafeArrayLock.argtypes = [POINTER(SAFEARRAY)]
_SafeArrayUnlock.argtypes = [POINTER(SAFEARRAY)]


class BSTR(ctypes.c_wchar_p):
    _needsfree = False

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.value)

    def __ctypes_from_outparam__(self):
        self._needsfree = True
        return self.value

    def __del__(self, _free=_oleaut32.SysFreeString):
        if self._b_base_ is None or self._needsfree:  # NOQA
            _free(self)

    def from_param(cls, value):
        if isinstance(value, cls):
            return value

        return cls(value)

    from_param = classmethod(from_param)


class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", DWORD),
        ("Data2", WORD),
        ("Data3", WORD),
        ("Data4", BYTE * 8)
    ]

    def __init__(self, name=None):
        ctypes.Structure.__init__(self)

        if name is not None:
            _CLSIDFromString(str(name), ctypes.byref(self))

    def __repr__(self):
        return 'GUID("%s")' % str(self)

    def __str__(self):
        p = ctypes.c_wchar_p()
        _StringFromCLSID(ctypes.byref(self), ctypes.byref(p))
        result = p.value
        _CoTaskMemFree(p)
        return result

    def __eq__(self, other):
        # noinspection PyTypeChecker
        return isinstance(other, GUID) and bytes(self) == bytes(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        # noinspection PyTypeChecker
        return hash(bytes(self))


IID = GUID
CLSID = GUID


def _encode_idl(names):
    # sum up all values found in _PARAMFLAGS, ignoring all others.
    return sum([_PARAMFLAGS.get(n, 0) for n in names])


def COMMETHOD(idlflags, restype, methodname, *argspec):
    paramflags = []
    argtypes = []

    for item in argspec:
        idl, typ, argname = item
        pflags = _encode_idl(idl)
        paramflags.append((pflags, argname))
        argtypes.append(typ)

    return (
        restype,
        methodname,
        tuple(argtypes),
        tuple(paramflags),
        tuple(idlflags),
        None
    )


com_interface_registry = {}


class _cominterface_meta(type):
    _com_shutting_down = False

    def __new__(self, name, bases, namespace):  # NOQA
        methods = namespace.pop("_methods_", None)
        cls = type.__new__(self, name, bases, namespace)

        if methods is not None:
            cls._methods_ = methods

        if bases == (object,):
            _ptr_bases = (cls, _compointer_base)
        else:
            _ptr_bases = (cls, POINTER(bases[0]))

        p = type(_compointer_base)(
            "POINTER(%s)" % cls.__name__,
            _ptr_bases,
            {
                "__com_interface__": cls,
                "_needs_com_addref_": None
            }
        )

        from ctypes import _pointer_type_cache  # NOQA
        _pointer_type_cache[cls] = p

        @Patch(POINTER(p))
        class ReferenceFix(object):  # NOQA
            def __setitem__(self, index, value):
                if index != 0:
                    if bool(value):
                        value.AddRef()

                    super(POINTER(p), self).__setitem__(index, value)  # NOQA
                    return

                from _ctypes import CopyComPointer
                CopyComPointer(value, self)

        return cls

    def __setattr__(self, name, value):
        if name == "_methods_":
            self._make_methods(value)

        type.__setattr__(self, name, value)

    def __get_baseinterface_methodcount(self):
        itf_name = None
        try:
            result = 0
            for itf in self.mro()[1:-1]:
                itf_name = itf.__name__
                result += len(itf.__dict__["_methods_"])
            return result

        except KeyError as err:
            (name,) = err.args
            if name == "_methods_":
                raise TypeError(
                    "baseinterface '%s' has no _methods_" % itf_name
                )
            raise

    def _fix_inout_args(self, func, argtypes, paramflags):  # NOQA
        SIMPLETYPE = type(INT)
        BYREFTYPE = type(ctypes.byref(INT()))

        def call_with_inout(self_, *args, **kw):
            args = list(args)
            outargs = {}
            outnum = 0
            for i, info in enumerate(paramflags):
                direction = info[0]
                if direction & 3 == 3:
                    name = info[1]
                    atyp = argtypes[i]._type_  # NOQA

                    try:
                        try:
                            v = args[i]
                        except IndexError:
                            v = kw[name]
                    except KeyError:
                        v = atyp()
                    else:
                        if getattr(v, "_type_", None) is atyp:
                            pass
                        elif type(atyp) is SIMPLETYPE:
                            v = atyp(v)
                        else:
                            v = atyp.from_param(v)
                            assert not isinstance(v, BYREFTYPE)
                    outargs[outnum] = v
                    outnum += 1
                    if len(args) > i:
                        args[i] = v
                    else:
                        kw[name] = v
                elif direction & 2 == 2:
                    outnum += 1

            rescode = func(self_, *args, **kw)

            if outnum == 1:
                if len(outargs) == 1:
                    rescode = rescode.__ctypes_from_outparam__()
                return rescode

            rescode = list(rescode)
            for outnum, o in list(outargs.items()):
                rescode[outnum] = o.__ctypes_from_outparam__()
            return rescode

        return call_with_inout

    def _make_methods(self, methods):
        iid = self.__dict__["_iid_"]

        iid = str(iid)
        com_interface_registry[iid] = self
        del iid

        vtbl_offset = self.__get_baseinterface_methodcount()

        for i, item in enumerate(methods):
            restype, name, argtypes, paramflags, idlflags, doc = item
            prototype = ctypes.WINFUNCTYPE(restype, *argtypes)

            if restype == HRESULT:
                # noinspection PyTypeChecker
                raw_func = prototype(
                    i + vtbl_offset,
                    name,
                    None,
                    self._iid_  # NOQA
                )

                func = prototype(
                    i + vtbl_offset,
                    name,
                    paramflags,
                    self._iid_  # NOQA
                )
            else:
                # noinspection PyTypeChecker
                raw_func = prototype(i + vtbl_offset, name, None, None)
                # noinspection PyTypeChecker
                func = prototype(i + vtbl_offset, name, paramflags, None)

            setattr(
                self,
                "_%s__com_%s" % (self.__name__, name),
                instancemethod(raw_func, None, self)
            )

            if paramflags:
                dirflags = [(p[0] & 3) for p in paramflags]
                if 3 in dirflags:
                    func = self._fix_inout_args(func, argtypes, paramflags)

            func.__doc__ = doc
            func.__name__ = name

            mth = instancemethod(func, None, self)

            if hasattr(self, name):
                setattr(self, "_" + name, mth)
            else:
                setattr(self, name, mth)


class _compointer_meta(type(ctypes.c_void_p), _cominterface_meta):
    pass


class _compointer_base(ctypes.c_void_p, metaclass=_compointer_meta):

    def __del__(self):
        if self:
            if not type(self)._com_shutting_down:  # NOQA
                self.Release()  # NOQA

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if not isinstance(other, _compointer_base):
            return False

        val1 = super(_compointer_base, self).value
        val2 = super(_compointer_base, other).value

        return val1 == val2

    def __hash__(self):
        return hash(super(_compointer_base, self).value)

    def __get_value(self):
        return self

    value = property(__get_value, doc="""Return self.""")

    def __repr__(self):
        ptr = super(_compointer_base, self).value
        return "<%s ptr=0x%x at %x>" % (
            self.__class__.__name__,
            ptr or 0,
            id(self)
        )

    def from_param(cls, value):
        if value is None:
            return None
        if value == 0:
            return None
        if isinstance(value, cls):
            return value

        if cls._iid_ == getattr(value, "_iid_", None):  # NOQA
            return value

        try:
            table = value._com_pointers_  # NOQA
        except AttributeError:
            pass
        else:
            try:
                return table[cls._iid_]  # NOQA
            except KeyError:
                raise TypeError(
                    "Interface %s not supported" % cls._iid_  # NOQA
                )

        return value.QueryInterface(cls.__com_interface__)  # NOQA

    from_param = classmethod(from_param)


class IUnknown(object, metaclass=_cominterface_meta):
    _case_insensitive_ = False
    _iid_ = GUID("{00000000-0000-0000-C000-000000000046}")

    _methods_ = [
        COMMETHOD(
            [],
            HRESULT,
            "QueryInterface",
            (['in'], POINTER(GUID), "riid"),
            (['in'], POINTER(PVOID), "ppvObject")
        ),
        COMMETHOD(
            [],
            ULONG,
            "AddRef"
        ),
        COMMETHOD(
            [],
            ULONG,
            "Release"
        )
    ]

    def QueryInterface(self, interface, iid=None):
        p = POINTER(interface)()

        if iid is None:
            iid = interface._iid_  # NOQA

        self.__com_QueryInterface(ctypes.byref(iid), ctypes.byref(p))  # NOQA

        clsid = self.__dict__.get('__clsid')
        if clsid is not None:
            p.__dict__['__clsid'] = clsid

        return p

    def AddRef(self):
        return self.__com_AddRef()  # NOQA

    def Release(self):
        return self.__com_Release()  # NOQA


class tagDEC(ctypes.Structure):
    _fields_ = [
        ("wReserved", ctypes.c_ushort),
        ("scale", ctypes.c_ubyte),
        ("sign", ctypes.c_ubyte),
        ("Hi32", ctypes.c_ulong),
        ("Lo64", ctypes.c_ulonglong)
    ]


DECIMAL = tagDEC


class _FILETIME(ctypes.Structure):
    _fields_ = [
        ('dwLowDateTime', DWORD),
        ('dwHighDateTime', DWORD)
    ]

    @property
    def value(self):
        system_time = SYSTEMTIME()
        _FileTimeToSystemTime(ctypes.byref(self), ctypes.byref(system_time))
        return system_time.value

    @value.setter
    def value(self, dt):
        system_time = SYSTEMTIME()
        system_time.value = dt
        _SystemTimeToFileTime(ctypes.byref(system_time), ctypes.byref(self))


FILETIME = _FILETIME
LPFILETIME = POINTER(FILETIME)


class _SYSTEMTIME(ctypes.Structure):
    _fields_ = [
        ('wYear', WORD),
        ('wMonth', WORD),
        ('wDayOfWeek', WORD),
        ('wDay', WORD),
        ('wHour', WORD),
        ('wMinute', WORD),
        ('wSecond', WORD),
        ('wMilliseconds', WORD),
    ]

    @property
    def value(self):
        dt = datetime.datetime(
            year=self.wYear,
            month=self.wMonth,
            day=self.wDay,
            hour=self.wHour,
            minute=self.wMinute,
            second=self.wSecond,
            microsecond=self.wMilliseconds * 1000
        )

        return dt

    # noinspection PyAttributeOutsideInit
    @value.setter
    def value(self, dt):
        if isinstance(dt, (int, float)):
            dt = datetime.datetime.fromtimestamp(dt)

        weekday = dt.weekday() + 1
        if weekday == 7:
            weekday = 0

        self.wYear = dt.year
        self.wMonth = dt.month
        self.wDayOfWeek = weekday
        self.wDay = dt.day
        self.wHour = dt.hour
        self.wMinute = dt.minute
        self.wSecond = dt.second
        self.wMilliseconds = int(dt.microsecond / 1000)


SYSTEMTIME = _SYSTEMTIME


class tagVARIANT(ctypes.Structure):
    class U_VARIANT1(ctypes.Union):
        class __tagVARIANT(ctypes.Structure):
            class U_VARIANT2(ctypes.Union):
                class _tagBRECORD(ctypes.Structure):
                    # noinspection PyTypeChecker
                    _fields_ = [
                        ("pvRecord", PVOID),
                        ("pRecInfo", POINTER(IUnknown))
                    ]

                _fields_ = [
                    ("VT_BOOL", VARIANT_BOOL),
                    ("VT_I1", BYTE),
                    ("VT_I2", SHORT),
                    ("VT_I4", LONG),
                    ("VT_I8", LONGLONG),
                    ("VT_INT", INT),
                    ("VT_UI1", UBYTE),
                    ("VT_UI2", USHORT),
                    ("VT_UI4", ULONG),
                    ("VT_UI8", ULONGLONG),
                    ("VT_UINT", UINT),
                    ("VT_R4", FLOAT),
                    ("VT_R8", DOUBLE),
                    ("VT_CY", LONGLONG),
                    ("c_wchar_p", ctypes.c_wchar_p),
                    ("c_void_p", PVOID),
                    ("pparray", POINTER(POINTER(tagSAFEARRAY))),
                    ("bstrVal", BSTR),
                    ("_tagBRECORD", _tagBRECORD),
                ]
                _anonymous_ = ["_tagBRECORD"]

            _fields_ = [
                ("vt", VARTYPE),
                ("wReserved1", USHORT),
                ("wReserved2", USHORT),
                ("wReserved3", USHORT),
                ("_", U_VARIANT2)
            ]

        _fields_ = [
            ("__VARIANT_NAME_2", __tagVARIANT),
            ("decVal", DECIMAL)
        ]
        _anonymous_ = ["__VARIANT_NAME_2"]

    _fields_ = [
        ("__VARIANT_NAME_1", U_VARIANT1)
    ]
    _anonymous_ = ["__VARIANT_NAME_1"]

    def __init__(self):
        ctypes.Structure.__init__(self)

    def __del__(self):
        if self._b_needsfree_:
            _VariantClear(self)

    @property
    def value(self):
        vt = self.vt
        if vt in (VT_EMPTY, VT_NULL):
            return None
        elif vt == VT_I1:
            return self._.VT_I1
        elif vt == VT_I2:
            return self._.VT_I2
        elif vt == VT_I4:
            return self._.VT_I4
        elif vt == VT_I8:
            return self._.VT_I8
        elif vt == VT_UI8:
            return self._.VT_UI8
        elif vt == VT_INT:
            return self._.VT_INT
        elif vt == VT_UI1:
            return self._.VT_UI1
        elif vt == VT_UI2:
            return self._.VT_UI2
        elif vt == VT_UI4:
            return self._.VT_UI4
        elif vt == VT_UINT:
            return self._.VT_UINT
        elif vt == VT_R4:
            return self._.VT_R4
        elif vt == VT_R8:
            return self._.VT_R8
        elif vt == VT_BOOL:
            return self._.VT_BOOL
        elif vt == VT_BSTR:
            return self._.bstrVal

    def __ctypes_from_outparam__(self):
        result = self.value
        self.vt = VT_EMPTY
        return result


LPVARIANT = POINTER(tagVARIANT)
VARIANT = tagVARIANT

_VariantClear.argtypes = (POINTER(VARIANT),)


# Enumerations
# The state of an instance.
class InstanceState(ENUM):
    # The instance state has not been determined.
    eNone = 0
    # The instance installation path exists.
    eLocal = 1
    # A product is registered to the instance.
    eRegistered = 2
    # No reboot is required for the instance.
    eNoRebootRequired = 4
    # do not know what this bit does
    eUnknown = 8
    # The instance represents a complete install.
    eComplete = MAXUINT

    @property
    def value(self):
        # noinspection PyUnresolvedReferences
        value = ENUM.value.__get__(self)
        if value == self.eComplete:
            return ['local', 'registered', 'no reboot required']
        if value == self.eNone:
            return ['remote', 'unregistered', 'reboot required']

        res = []

        if value | self.eLocal == value:
            res += ['local']
        else:
            res += ['remote']
        if value | self.eRegistered == value:
            res += ['registered']
        else:
            res += ['unregistered']
        if value | self.eNoRebootRequired == value:
            res += ['no reboot required']
        else:
            res += ['reboot required']

        if value | self.eUnknown == value:
            res.append('unknown flag set')

        return res


eNone = InstanceState.eNone
eLocal = InstanceState.eLocal
eRegistered = InstanceState.eRegistered
eNoRebootRequired = InstanceState.eNoRebootRequired
eUnknown = InstanceState.eUnknown
eComplete = InstanceState.eComplete


class Packages(object):

    def __init__(self, packages):
        self._packages = packages

    def __iter__(self):
        return iter(self._packages)

    def __str__(self):
        res = []

        def _add(items):
            for item in items:
                res.append('\n'.join(
                    '    ' + line
                    for line in str(item).split('\n')
                ))
                res.append('')

        res.append('vsix:')
        _add(self.vsix)
        res.append('group:')
        _add(self.group)
        res.append('component:')
        _add(self.component)
        res.append('workload:')
        _add(self.workload)
        res.append('product:')
        _add(self.product)
        res.append('msi:')
        _add(self.msi)
        res.append('exe:')
        _add(self.exe)
        res.append('msu:')
        _add(self.msu)
        res.append('other:')
        _add(self.other)

        return '\n'.join(res)

    @property
    def vsix(self):
        return [
            package for package in self
            if package.type == 'Vsix'
        ]

    @property
    def group(self):
        return [
            package for package in self
            if package.type == 'Group'
        ]

    @property
    def component(self):
        return [
            package for package in self
            if package.type == 'Component'
        ]

    @property
    def workload(self):
        return [
            package for package in self
            if package.type == 'Workload'
        ]

    @property
    def product(self):
        return [
            package for package in self
            if package.type == 'Product'
        ]

    @property
    def msi(self):
        return [
            package for package in self
            if package.type == 'Msi'
        ]

    @property
    def exe(self):
        return [
            package for package in self
            if package.type == 'Exe'
        ]

    @property
    def msu(self):
        return [
            package for package in self
            if package.type == 'Msu'
        ]

    @property
    def other(self):
        return [
            package for package in self
            if package.type not in (
                'Exe', 'Msi', 'Product', 'Vsix',
                'Group', 'Component', 'Workload', 'Msu'
            )
        ]


# Forward declarations


IID_ISetupPackageReference = IID("{da8d8a16-b2b6-4487-a2f1-594ccccd6bf5}")


# A reference to a package.
class ISetupPackageReference(IUnknown):
    _iid_ = IID_ISetupPackageReference

    def __gt__(self, other):
        if isinstance(other, ISetupPackageReference):
            return self.version > other.version

        other = _convert_version(other)

        if not isinstance(other, tuple):
            return False

        return self.version > other

    def __lt__(self, other):
        if isinstance(other, ISetupPackageReference):
            return self.version < other.version

        other = _convert_version(other)

        if not isinstance(other, str):
            return False

        return self.version < other

    def __ge__(self, other):
        if isinstance(other, ISetupPackageReference):
            return self.version >= other.version

        other = _convert_version(other)

        if not isinstance(other, str):
            return False

        return self.version >= other

    def __le__(self, other):
        if isinstance(other, ISetupPackageReference):
            return self.version <= other.version

        other = _convert_version(other)

        if not isinstance(other, str):
            return False

        return self.version <= other

    def __eq__(self, other):
        if isinstance(other, ISetupPackageReference):
            return self.version == other.version

        other = _convert_version(other)

        if not isinstance(other, str):
            return object.__eq__(self, other)

        return self.version == other

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def name(self):
        # noinspection PyUnresolvedReferences
        return self.GetId()

    @property
    def id(self):
        # noinspection PyUnresolvedReferences
        return self.GetId()

    @property
    def version(self):
        # noinspection PyUnresolvedReferences
        return self.GetVersion()

    @property
    def chip(self):
        # noinspection PyUnresolvedReferences
        return self.GetChip()

    @property
    def language(self):
        # noinspection PyUnresolvedReferences
        return self.GetLanguage()

    @property
    def branch(self):
        # noinspection PyUnresolvedReferences
        return self.GetBranch()

    @property
    def type(self):
        # noinspection PyUnresolvedReferences
        return self.GetType()

    @property
    def unique_id(self):
        # noinspection PyUnresolvedReferences
        return self.GetUniqueId()

    @property
    def is_extension(self):
        # noinspection PyUnresolvedReferences
        return self.GetIsExtension()

    def __str__(self):
        res = [
            'id: ' + str(self.id),
            'version: ' + str(self.version),
            'chip: ' + str(self.chip),
            'language: ' + str(self.language),
            'branch: ' + str(self.branch),
            'type: ' + str(self.type),
            'unique id: ' + str(self.unique_id),
            'is extension: ' + str(self.is_extension)
        ]
        return '\n'.join(res)


IID_ISetupInstance = IID("{B41463C3-8866-43B5-BC33-2B0676F7F42E}")


def _convert_version(other):
    if isinstance(other, str):
        other = tuple(int(item) for item in other.split('.'))
    elif isinstance(other, bytes):
        other = tuple(
            int(item) for item in other.decode('utf-8').split('.')
        )
    elif isinstance(other, list):
        other = tuple(other)
    elif isinstance(other, int):
        other = (other,)
    elif isinstance(other, float):
        other = tuple(int(item) for item in str(other).split('.'))

    if isinstance(other, tuple):
        other = '.'.join(str(item) for item in other)

    return other


# Information about an instance of a product.
class ISetupInstance(IUnknown):
    _iid_ = IID_ISetupInstance
    _helper = None

    def __call__(self, helper):
        self._helper = helper
        return self

    @property
    def id(self):
        # noinspection PyUnresolvedReferences
        return self.GetInstanceId()

    @property
    def install_date(self):
        # noinspection PyUnresolvedReferences
        return self.GetInstallDate().value

    @property
    def name(self):
        # noinspection PyUnresolvedReferences
        return self.GetInstallationName()

    @property
    def path(self):
        # noinspection PyUnresolvedReferences
        return self.GetInstallationPath()

    @property
    def version(self):
        # noinspection PyUnresolvedReferences
        return self.GetInstallationVersion()

    @property
    def full_version(self):
        if self._helper is not None:
            return self._helper.ParseVersion(self.version)

    @property
    def display_name(self):
        try:
            # noinspection PyUnresolvedReferences
            return self.GetDisplayName(_GetUserDefaultLCID())
        except (OSError, ValueError, COMError):
            pass

    @property
    def description(self):
        try:
            # noinspection PyUnresolvedReferences
            return self.GetDescription(_GetUserDefaultLCID())
        except (OSError, ValueError, COMError):
            pass

    def __str__(self):
        title_bar = '-- ' + str(self.display_name) + ' '
        title_bar += '-' * (63 - len(title_bar))
        res = [
            title_bar,
            'description: ' + str(self.description),
            'version: ' + str(self.version),
            'id: ' + str(self.id),
            'name: ' + str(self.name),
            'path: ' + str(self.path),
            'full version: ' + str(self.full_version),
            'install date: ' + self.install_date.strftime('%c')
        ]
        return '\n'.join(res)


IID_ISetupInstance2 = IID("{89143C9A-05AF-49B0-B717-72E218A2185C}")


# Information about an instance of a product.
class ISetupInstance2(ISetupInstance):
    _iid_ = IID_ISetupInstance2

    @property
    def packages(self) -> Packages:
        # noinspection PyUnresolvedReferences
        safearray = self.GetPackages()

        _SafeArrayLock(safearray)

        # noinspection PyTypeChecker
        packs = ctypes.cast(
            safearray.contents.pvData,
            POINTER(POINTER(ISetupPackageReference))
        )

        cPackages = safearray.contents.rgsabound[0].cElements

        res = []
        for i in range(cPackages):
            p = packs[i]
            res.append(p)

        _SafeArrayUnlock(safearray)
        res = Packages(res)
        return res

    @property
    def properties(self):
        # noinspection PyUnresolvedReferences
        return self.GetProperties()

    @property
    def product(self):
        """
        version
        chip
        language
        branch
        type
        unique_id
        is_extension
        """
        if 'registered' in self.state:
            # noinspection PyUnresolvedReferences
            return self.GetProduct()

    @property
    def state(self):
        # noinspection PyUnresolvedReferences
        return self.GetState().value

    @property
    def product_path(self):
        # noinspection PyUnresolvedReferences
        return self.GetProductPath()

    @property
    def errors(self):
        # noinspection PyUnresolvedReferences
        errors = self.GetErrors()
        try:
            return errors.QueryInterface(ISetupErrorState2)
        except ValueError:
            return errors

    @property
    def is_launchable(self):
        # noinspection PyUnresolvedReferences
        return self.IsLaunchable()

    @property
    def is_complete(self):
        # noinspection PyUnresolvedReferences
        return self.IsComplete()

    @property
    def is_prerelease(self):
        catalog = self.QueryInterface(ISetupInstanceCatalog)
        return catalog.IsPrerelease()  # NOQA

    @property
    def catalog(self):
        return self.QueryInterface(ISetupInstanceCatalog)

    @property
    def engine_path(self):
        # noinspection PyUnresolvedReferences
        return self.GetEnginePath()

    @property
    def localised_properties(self):
        return self.QueryInterface(ISetupLocalizedProperties)

    def __str__(self):
        res = [
            ISetupInstance.__str__(self),
            'product path: ' + str(self.product_path),
            'is launchable: ' + str(self.is_launchable),
            'is complete: ' + str(self.is_complete),
            'is prerelease: ' + str(self.is_prerelease),
            'state: ' + str(self.state),
            'engine path: ' + str(self.engine_path),
            'errors:',
            '{errors}',
            'product: ',
            '{product}',
            'packages:',
            '{packages}',
            'properties:',
            '{properties}',
            'catalog:',
            '{catalog}',
            '-' * 63
        ]

        res = '\n'.join(res)

        return res.format(
            errors='\n'.join(
                '    ' + line
                for line in str(self.errors).split('\n')
            ),
            product='\n'.join(
                '    ' + line
                for line in str(self.product).split('\n')
            ),
            packages='\n'.join(
                '    ' + line
                for line in str(self.packages).split('\n')
            ),
            properties='\n'.join(
                '    ' + line
                for line in str(self.properties).split('\n')
            ),
            catalog='\n'.join(
                '    ' + line
                for line in str(self.catalog).split('\n')
            )
        )


IID_ISetupInstanceCatalog = IID("{9AD8E40F-39A2-40F1-BF64-0A6C50DD9EEB}")


# Information about a catalog used to install an instance.
class ISetupInstanceCatalog(IUnknown):
    _iid_ = IID_ISetupInstanceCatalog

    @property
    def id(self):
        for prop in self:
            if prop.name == 'id':
                return prop.value

    @property
    def build_branch(self):
        for prop in self:
            if prop.name == 'buildBranch':
                return prop.value

    @property
    def build_version(self):
        for prop in self:
            if prop.name == 'buildVersion':
                return prop.value

    @property
    def local_build(self):
        for prop in self:
            if prop.name == 'localBuild':
                return prop.value

    @property
    def manifest_name(self):
        for prop in self:
            if prop.name == 'manifestName':
                return prop.value

    @property
    def manifest_type(self):
        for prop in self:
            if prop.name == 'manifestType':
                return prop.value

    @property
    def product_display_version(self):
        for prop in self:
            if prop.name == 'productDisplayVersion':
                return prop.value

    @property
    def product_line(self):
        for prop in self:
            if prop.name == 'productLine':
                return prop.value

    @property
    def product_line_version(self):
        for prop in self:
            if prop.name == 'productLineVersion':
                return prop.value

    @property
    def product_milestone(self):
        for prop in self:
            if prop.name == 'productMilestone':
                return prop.value

    @property
    def product_milestone_is_prerelease(self):
        for prop in self:
            if prop.name == 'productMilestoneIsPreRelease':
                return prop.value

    @property
    def product_name(self):
        for prop in self:
            if prop.name == 'productName':
                return prop.value

    @property
    def product_patch_version(self):
        for prop in self:
            if prop.name == 'productPatchVersion':
                return prop.value

    @property
    def product_prerelease_milestone_suffix(self):
        for prop in self:
            if prop.name == 'productPreReleaseMilestoneSuffix':
                return prop.value

    @property
    def product_semantic_version(self):
        for prop in self:
            if prop.name == 'productSemanticVersion':
                return prop.value

    def __iter__(self):
        # noinspection PyUnresolvedReferences
        for prop in self.GetCatalogInfo():
            yield prop

    def __str__(self):
        res = [prop.name + ': ' + str(prop.value) for prop in self]
        return '\n'.join(res)


IID_ISetupLocalizedProperties = IID("{F4BD7382-FE27-4AB4-B974-9905B2A148B0}")


# Provides localized properties of an instance of a product.
class ISetupLocalizedProperties(IUnknown):
    _iid_ = IID_ISetupLocalizedProperties


IID_IEnumSetupInstances = IID("{6380BCFF-41D3-4B2E-8B2E-BF8A6810C848}")


# A enumerator of installed ISetupInstance objects.
class IEnumSetupInstances(IUnknown):
    _iid_ = IID_IEnumSetupInstances

    def __iter__(self):
        while True:
            try:
                # noinspection PyUnresolvedReferences
                set_instance, num = self.Next(1)
                yield set_instance

            except COMError:
                break


IID_ISetupConfiguration = IID("{42843719-DB4C-46C2-8E7C-64F1816EFD5B}")


# Gets information about product instances set up on the machine.
class ISetupConfiguration(IUnknown):
    _iid_ = IID_ISetupConfiguration

    def __call__(self):
        try:
            return self.QueryInterface(ISetupConfiguration2)
        except (ValueError, OSError, COMError):
            return self

    def __iter__(self):
        # noinspection PyUnresolvedReferences
        setup_enum = self.EnumInstances()
        helper = self.QueryInterface(ISetupHelper)

        for si in setup_enum:
            if not si:
                break

            yield si(helper)

    def __str__(self):
        res = []
        for instance_config in self:
            res += [str(instance_config)]

        return '\n\n\n'.join(res)


IID_ISetupConfiguration2 = IID("{26AAB78C-4A60-49D6-AF3B-3C35BC93365D}")


# Gets information about product instances.
class ISetupConfiguration2(ISetupConfiguration):
    _iid_ = IID_ISetupConfiguration2

    def __iter__(self):
        # noinspection PyUnresolvedReferences
        setup_enum = self.EnumAllInstances()
        helper = self.QueryInterface(ISetupHelper)

        for si in setup_enum:
            if not si:
                break

            yield si.QueryInterface(ISetupInstance2)(helper)


IID_ISetupHelper = IID("{42b21b78-6192-463e-87bf-d577838f1d5c}")


class ISetupHelper(IUnknown):
    _iid_ = IID_ISetupHelper


IID_ISetupErrorState = IID("{46DCCD94-A287-476A-851E-DFBC2FFDBC20}")


# Information about the error state of an instance.
class ISetupErrorState(IUnknown):
    _iid_ = IID_ISetupErrorState

    @property
    def failed_packages(self) -> Packages:
        try:
            # noinspection PyUnresolvedReferences
            safearray = self.GetFailedPackages()
        except ValueError:
            return Packages([])

        _SafeArrayLock(safearray)

        # noinspection PyTypeChecker
        packs = ctypes.cast(
            safearray.contents.pvData,
            POINTER(POINTER(ISetupFailedPackageReference))
        )

        cPackages = safearray.contents.rgsabound[0].cElements

        res = []
        for i in range(cPackages):
            p = packs[i]
            p = p.QueryInterface(ISetupFailedPackageReference2)
            res.append(p)

        _SafeArrayUnlock(safearray)
        res = Packages(res)
        return res

    @property
    def skipped_packages(self) -> Packages:
        try:
            # noinspection PyUnresolvedReferences
            safearray = self.GetSkippedPackages()
        except ValueError:
            return Packages([])

        _SafeArrayLock(safearray)

        # noinspection PyTypeChecker
        packs = ctypes.cast(
            safearray.contents.pvData,
            POINTER(POINTER(ISetupFailedPackageReference))
        )

        cPackages = safearray.contents.rgsabound[0].cElements

        res = []
        for i in range(cPackages):
            p = packs[i]
            p = p.QueryInterface(ISetupFailedPackageReference2)
            res.append(p)

        _SafeArrayUnlock(safearray)
        res = Packages(res)
        return res

    def __str__(self):
        res = ['failed packages: ']
        res.extend([
            '    ' + line for line in
            str(self.failed_packages).split('\n')
        ])

        res += ['skipped packages: ']
        res.extend([
            '    ' + line for line in
            str(self.skipped_packages).split('\n')
        ])

        return '\n'.join(res)


IID_ISetupErrorState2 = IID("{9871385B-CA69-48F2-BC1F-7A37CBF0B1EF}")


# Information about the error state of an instance.
class ISetupErrorState2(ISetupErrorState):
    _iid_ = IID_ISetupErrorState2

    @property
    def error_log_file_path(self):
        # noinspection PyUnresolvedReferences
        return self.GetErrorLogFilePath()

    @property
    def log_file_path(self):
        # noinspection PyUnresolvedReferences
        return self.GetLogFilePath()

    def __str__(self):
        res = [
            'error log file path: ' + self.error_log_file_path,
            'log file path: ' + self.log_file_path,
            ISetupErrorState.__str__(self)
        ]
        return '\n'.join(res)


IID_ISetupFailedPackageReference = IID(
    "{E73559CD-7003-4022-B134-27DC650B280F}"
    )


# A reference to a failed package.
class ISetupFailedPackageReference(ISetupPackageReference):
    _iid_ = IID_ISetupFailedPackageReference


IID_ISetupFailedPackageReference2 = IID(
    "{0FAD873E-E874-42E3-B268-4FE2F096B9CA}"
    )


# A reference to a failed package.
class ISetupFailedPackageReference2(ISetupFailedPackageReference):
    _iid_ = IID_ISetupFailedPackageReference2


IID_ISetupPropertyStore = IID("{C601C175-A3BE-44BC-91F6-4568D230FC83}")


class Property(object):

    def __init__(self, name, value):
        self._name = name
        self._value = value

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    def __str__(self):
        return self.name + ': ' + str(self.value)


# Provides named properties.
class ISetupPropertyStore(IUnknown):
    _iid_ = IID_ISetupPropertyStore

    @property
    def names(self):
        # noinspection PyUnresolvedReferences
        safearray = self.GetNames()

        _SafeArrayLock(safearray)

        names = ctypes.cast(safearray.contents.pvData, POINTER(BSTR))
        cPackages = safearray.contents.rgsabound[0].cElements

        res = []
        for i in range(cPackages):
            res.append(names[i])

        _SafeArrayUnlock(safearray)

        return res

    def __iter__(self):
        for n in self.names:
            # noinspection PyUnresolvedReferences
            v = VARIANT()

            self.GetValue(n, ctypes.byref(v))  # NOQA

            v = v.value
            if isinstance(v, BSTR):
                v = v.value

            yield Property(n.value, v)

    def __str__(self):
        return '\n'.join(str(prop) for prop in self)


IID_ISetupLocalizedPropertyStore = IID(
    "{5BB53126-E0D5-43DF-80F1-6B161E5C6F6C}"
    )


# Provides localized named properties.
class ISetupLocalizedPropertyStore(IUnknown):
    _iid_ = IID_ISetupLocalizedPropertyStore

    @property
    def names(self):
        # noinspection PyUnresolvedReferences
        safearray = self.GetNames()

        _SafeArrayLock(safearray)

        names = ctypes.cast(safearray.contents.pvData, POINTER(BSTR))
        cPackages = safearray.contents.rgsabound[0].cElements

        res = []
        for i in range(cPackages):
            res.append(names[i])

        _SafeArrayUnlock(safearray)

        return res

    def __iter__(self):
        for n in self.names:
            # noinspection PyUnresolvedReferences
            v = VARIANT()

            self.GetValue(n, ctypes.byref(v))  # NOQA

            v = v.value
            if isinstance(v, BSTR):
                v = v.value

            yield Property(n.value, v)

    def __str__(self):
        return '\n'.join(str(prop) for prop in self)


ISetupPackageReference._methods_ = [
    # Gets the general package identifier.
    COMMETHOD(
        [],
        HRESULT,
        "GetId",
        (['out'], POINTER(BSTR), "pbstrId")
    ),
    # Gets the version of the package.
    COMMETHOD(
        [],
        HRESULT,
        "GetVersion",
        (['out'], POINTER(BSTR), "pbstrVersion")

    ),
    # Gets the target process architecture of the package.
    COMMETHOD(
        [],
        HRESULT,
        "GetChip",
        (['out'], POINTER(BSTR), "pbstrChip")
    ),
    # Gets the language and optional region identifier.
    COMMETHOD(
        [],
        HRESULT,
        "GetLanguage",
        (['out'], POINTER(BSTR), "pbstrLanguage")
    ),
    # Gets the build branch of the package.
    COMMETHOD(
        [],
        HRESULT,
        "GetBranch",
        (['out'], POINTER(BSTR), "pbstrBranch")
    ),
    # Gets the type of the package.
    COMMETHOD(
        [],
        HRESULT,
        "GetType",
        (['out'], POINTER(BSTR), "pbstrType")
    ),
    # Gets the unique identifier consisting of all defined tokens.
    COMMETHOD(
        [],
        HRESULT,
        "GetUniqueId",
        (['out'], POINTER(BSTR), "pbstrUniqueId")
    ),
    # Gets a value indicating whether the package refers to
    # an external extension.
    COMMETHOD(
        [],
        HRESULT,
        "GetIsExtension",
        (['out'], POINTER(VARIANT_BOOL), "pfIsExtension")
    )
]

ISetupInstance._methods_ = [
    # Gets the instance identifier (should match the name of the
    # parent instance directory).
    COMMETHOD(
        [],
        HRESULT,
        "GetInstanceId",
        (['out'], POINTER(BSTR), "pbstrInstanceId")
    ),
    # Gets the local date and time when the installation
    # was originally installed.
    COMMETHOD(
        [],
        HRESULT,
        "GetInstallDate",
        (['out'], LPFILETIME, "pInstallDate")
    ),
    # Gets the unique name of the installation, often
    # indicating the branch and other information used for telemetry.
    COMMETHOD(
        [],
        HRESULT,
        "GetInstallationName",
        (['out'], POINTER(BSTR), "pbstrInstallationName")
    ),
    # Gets the path to the installation root of the product.
    COMMETHOD(
        [],
        HRESULT,
        "GetInstallationPath",
        (['out'], POINTER(BSTR), "pbstrInstallationPath")
    ),
    # Gets the version of the product installed in this instance.
    COMMETHOD(
        [],
        HRESULT,
        "GetInstallationVersion",
        (['out'], POINTER(BSTR), "pbstrInstallationVersion")
    ),
    # Gets the display name (title) of the product installed
    # in this instance.
    COMMETHOD(
        [],
        HRESULT,
        "GetDisplayName",
        (['in'], LCID, "lcid"),
        (['out'], POINTER(BSTR), "pbstrDisplayName")
    ),
    # Gets the description of the product installed in this instance.
    COMMETHOD(
        [],
        HRESULT,
        "GetDescription",
        (['in'], LCID, "lcid"),
        (['out'], POINTER(BSTR), "pbstrDescription")
    ),
    # Resolves the optional relative path to the root path of the instance.
    COMMETHOD(
        [],
        HRESULT,
        "ResolvePath",
        (['in'], LPCOLESTR, "pwszRelativePath"),
        (['out'], POINTER(BSTR), "pbstrAbsolutePath")

    )
]

# noinspection PyTypeChecker
ISetupInstance2._methods_ = [
    # Gets the state of the instance.
    COMMETHOD(
        [],
        HRESULT,
        "GetState",
        (['out'], POINTER(InstanceState), "pState")
    ),
    # Gets an array of package references registered to the instance.
    COMMETHOD(
        [],
        HRESULT,
        "GetPackages",
        (['out'], POINTER(LPSAFEARRAY), "ppsaPackages")
    ),
    # Gets a pointer to the ISetupPackageReference that represents
    # the registered product.
    COMMETHOD(
        [],
        HRESULT,
        "GetProduct",
        (['out'], POINTER(POINTER(ISetupPackageReference)), "ppPackage")
    ),
    # Gets the relative path to the product application, if available.
    COMMETHOD(
        [],
        HRESULT,
        "GetProductPath",
        (['out'], POINTER(BSTR), "pbstrProductPath")
    ),
    # Gets the error state of the instance, if available.
    COMMETHOD(
        [],
        HRESULT,
        "GetErrors",
        (['out'], POINTER(POINTER(ISetupErrorState)), "ppErrorState")
    ),
    # Gets a value indicating whether the instance can be launched.
    COMMETHOD(
        [],
        HRESULT,
        "IsLaunchable",
        (['out'], POINTER(VARIANT_BOOL), "pfIsLaunchable")
    ),
    # Gets a value indicating whether the instance is complete.
    COMMETHOD(
        [],
        HRESULT,
        "IsComplete",
        (['out'], POINTER(VARIANT_BOOL), "pfIsComplete")
    ),
    # Gets product-specific properties.
    COMMETHOD(
        [],
        HRESULT,
        "GetProperties",
        (['out'], POINTER(POINTER(ISetupPropertyStore)), "ppProperties")
    ),
    # Gets the directory path to the setup engine
    # that installed the instance.
    COMMETHOD(
        [],
        HRESULT,
        "GetEnginePath",
        (['out'], POINTER(BSTR), "pbstrEnginePath")
    )
]

# noinspection PyTypeChecker
ISetupInstanceCatalog._methods_ = [
    # Gets catalog information properties.
    COMMETHOD(
        [],
        HRESULT,
        "GetCatalogInfo",
        (['out'], POINTER(POINTER(ISetupPropertyStore)), "ppCatalogInfo")
    ),
    # Gets a value indicating whether the catalog is a prerelease.
    COMMETHOD(
        [],
        HRESULT,
        "IsPrerelease",
        (['out'], POINTER(VARIANT_BOOL), "pfIsPrerelease")
    )
]

# noinspection PyTypeChecker
ISetupLocalizedProperties._methods_ = [
    # Gets localized product-specific properties.
    COMMETHOD(
        [],
        HRESULT,
        "GetLocalizedProperties",
        (
            ['out'],
            POINTER(POINTER(ISetupLocalizedPropertyStore)),
            "ppLocalizedProperties"
        )
    ),
    # Gets localized channel-specific properties.
    COMMETHOD(
        [],
        HRESULT,
        "GetLocalizedChannelProperties",
        (
            ['out'],
            POINTER(POINTER(ISetupLocalizedPropertyStore)),
            "ppLocalizedChannelProperties"
        )
    )
]

# noinspection PyTypeChecker
IEnumSetupInstances._methods_ = [
    # Retrieves the next set of product instances in the
    # enumeration sequence.
    COMMETHOD(
        [],
        HRESULT,
        "Next",
        (['in'], ULONG, "celt"),
        (['out'], POINTER(POINTER(ISetupInstance)), "rgelt"),
        (['out'], POINTER(ULONG), "pceltFetched")
    ),
    # Skips the next set of product instances in the enumeration sequence.
    COMMETHOD(
        [],
        HRESULT,
        "Skip",
        (['in'], ULONG, "celt")
    ),
    # Resets the enumeration sequence to the beginning.
    COMMETHOD(
        [],
        HRESULT,
        "Reset"
    ),
    # Creates a new enumeration object in the same state as the current
    # enumeration object: the new object points to the same place in the
    # enumeration sequence.
    COMMETHOD(
        [],
        HRESULT,
        "Clone",
        (['out'], POINTER(POINTER(IEnumSetupInstances)), "ppenum")
    )
]

# noinspection PyTypeChecker
ISetupConfiguration._methods_ = [
    # Enumerates all completed product instances installed.
    COMMETHOD(
        [],
        HRESULT,
        "EnumInstances",
        (['out'], POINTER(POINTER(IEnumSetupInstances)), "ppEnumInstances")
    ),
    # Gets the instance for the current process path.
    COMMETHOD(
        [],
        HRESULT,
        "GetInstanceForCurrentProcess",
        (['out'], POINTER(POINTER(ISetupInstance)), "ppInstance")
    ),
    # Gets the instance for the given path.
    COMMETHOD(
        [],
        HRESULT,
        "GetInstanceForPath",
        (['in'], LPCWSTR, "wzPath"),
        (['out'], POINTER(POINTER(ISetupInstance)), "ppInstance")
    )
]

# noinspection PyTypeChecker
ISetupConfiguration2._methods_ = [
    # Enumerates all product instances.
    COMMETHOD(
        [],
        HRESULT,
        "EnumAllInstances",
        (['out'], POINTER(POINTER(IEnumSetupInstances)), "ppEnumInstances")
    )
]

ISetupHelper._methods_ = [
    # Parses a dotted quad version string into a 64-bit unsigned integer.
    COMMETHOD(
        [],
        HRESULT,
        "ParseVersion",
        (['in'], LPCOLESTR, "pwszVersion"),
        (['out'], PULONGLONG, "pullVersion")
    ),
    # Parses a dotted quad version string into a 64-bit unsigned integer.
    COMMETHOD(
        [],
        HRESULT,
        "ParseVersionRange",
        (['in'], LPCOLESTR, "pwszVersionRange"),
        (['out'], PULONGLONG, "pullMinVersion"),
        (['out'], PULONGLONG, "pullMaxVersion")
    )
]

ISetupErrorState._methods_ = (
    # Gets an array of failed package references.
    COMMETHOD(
        [],
        HRESULT,
        "GetFailedPackages",
        (['out'], POINTER(LPSAFEARRAY), "ppsaFailedPackages")
    ),
    # Gets an array of skipped package references.
    COMMETHOD(
        [],
        HRESULT,
        "GetSkippedPackages",
        (['out'], POINTER(LPSAFEARRAY), "ppsaSkippedPackages")
    )
)

ISetupErrorState2._methods_ = (
    # Gets the path to the error log.
    COMMETHOD(
        [],
        HRESULT,
        "GetErrorLogFilePath",
        (['out'], POINTER(BSTR), "pbstrErrorLogFilePath")
    ),
    # Gets the path to the main setup log.
    COMMETHOD(
        [],
        HRESULT,
        "GetLogFilePath",
        (['out'], POINTER(BSTR), "pbstrLogFilePath")
    )
)

ISetupFailedPackageReference._methods_ = ()

ISetupFailedPackageReference2._methods_ = (
    # Gets the path to the optional package log.
    COMMETHOD(
        [],
        HRESULT,
        "GetLogFilePath",
        (['out'], POINTER(BSTR), "pbstrLogFilePath")
    ),
    # Gets the description of the package failure.
    COMMETHOD(
        [],
        HRESULT,
        "GetDescription",
        (['out'], POINTER(BSTR), "pbstrDescription")
    ),
    # Gets the signature to use for feedback reporting.
    COMMETHOD(
        [],
        HRESULT,
        "GetSignature",
        (['out'], POINTER(BSTR), "pbstrSignature")
    ),
    # Gets the array of details for this package failure.
    COMMETHOD(
        [],
        HRESULT,
        "GetDetails",
        (['out'], POINTER(LPSAFEARRAY), "ppsaDetails")
    ),
    # Gets an array of packages affected by this package failure.
    COMMETHOD(
        [],
        HRESULT,
        "GetAffectedPackages",
        (['out'], POINTER(LPSAFEARRAY), "ppsaAffectedPackages")
    )
)

ISetupPropertyStore._methods_ = (
    # Gets an array of property names in this property store.
    COMMETHOD(
        [],
        HRESULT,
        "GetNames",
        (['out'], POINTER(LPSAFEARRAY), "ppsaNames")
    ),
    # Gets the value of a named property in this property store.
    COMMETHOD(
        [],
        HRESULT,
        "GetValue",
        (['in'], LPCOLESTR, "pwszName"),
        (['in'], LPVARIANT, "pvtValue")
    )
)

ISetupLocalizedPropertyStore._methods_ = (
    # Gets an array of property names in this property store.
    COMMETHOD(
        [],
        HRESULT,
        "GetNames",
        (['in'], LCID, "lcid"),
        (['out'], POINTER(LPSAFEARRAY), "ppsaNames")
    ),
    # Gets the value of a named property in this property store.
    COMMETHOD(
        [],
        HRESULT,
        "GetValue",
        (['in'], LPCOLESTR, "pwszName"),
        (['in'], LCID, "lcid"),
        (['out'], LPVARIANT, "pvtValue")
    )
)

CLSID_SetupConfiguration = CLSID("{177F0C4A-1CD3-4DE7-A32C-71DBBB9FA36D}")


# This class implements ISetupConfiguration, ISetupConfiguration2 and
# ISetupHelper.
class SetupConfiguration(IUnknown):
    _instance_ = None
    _iid_ = CLSID_SetupConfiguration

    ISetupConfiguration = ISetupConfiguration
    ISetupConfiguration2 = ISetupConfiguration2
    ISetupHelper = ISetupHelper

    # Gets an ISetupConfiguration that provides information about
    # product instances installed on the machine.
    # noinspection PyTypeChecker
    _methods_ = [
        COMMETHOD(
            [],
            HRESULT,
            "GetSetupConfiguration",
            (
                ['out'],
                POINTER(POINTER(ISetupConfiguration)),
                "ppConfiguration"
            ),
            ([], LPVOID, "pReserved")
        )
    ]

    @classmethod
    def _callback(cls, _):
        cls._instance_ = None
        CoUninitialize()

    @classmethod
    def GetSetupConfiguration(cls):
        if cls._instance_ is None:
            CoInitialize()
            # noinspection PyCallingNonCallable
            instance = CoCreateInstance(
                CLSID_SetupConfiguration,
                ISetupConfiguration,
                CLSCTX_ALL
            )()

            cls._instance_ = weakref.ref(instance, cls._callback)
        else:
            instance = cls._instance_()

        return instance


atexit.register(_shutdown)


if __name__ == '__main__':
    setup_config = SetupConfiguration.GetSetupConfiguration()
    print(setup_config)
