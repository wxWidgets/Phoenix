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

try:
    import comtypes
except ImportError:
    raise RuntimeError('the comtypes library is needed to run this script')

import weakref
import ctypes
from ctypes.wintypes import (
    LPFILETIME,
    LPCOLESTR,
    ULONG,
    LPCWSTR,
    LPVOID,
    LCID
)

from comtypes.automation import (
    tagVARIANT,
    BSTR
)
from comtypes import (
    GUID,
    COMMETHOD,
    POINTER,
    IUnknown,
    HRESULT
)
from comtypes._safearray import (  # NOQA
    SAFEARRAY,
    VARIANT_BOOL,
    SafeArrayLock,
    SafeArrayUnlock
)

LPVARIANT = POINTER(tagVARIANT)
VARIANT = tagVARIANT
ENUM = ctypes.c_uint
IID = GUID
CLSID = GUID
MAXUINT = 0xFFFFFFFF
PULONGLONG = POINTER(ctypes.c_ulonglong)
LPSAFEARRAY = POINTER(SAFEARRAY)
_CoTaskMemFree = ctypes.windll.ole32.CoTaskMemFree


def HRESULT_FROM_WIN32(x):
    return x


ERROR_FILE_NOT_FOUND = 0x00000002
ERROR_NOT_FOUND = 0x00000490

# Constants
E_NOTFOUND = HRESULT_FROM_WIN32(ERROR_NOT_FOUND)
E_FILENOTFOUND = HRESULT_FROM_WIN32(ERROR_FILE_NOT_FOUND)


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
        return self.GetInstallDate()

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
            return self.GetDisplayName()
        except OSError:
            pass

    @property
    def description(self):
        try:
            # noinspection PyUnresolvedReferences
            return self.GetDescription()
        except OSError:
            pass

    def __str__(self):
        res = [
            'id: ' + str(self.id),
            'name: ' + str(self.name),
            'display name: ' + str(self.display_name),
            'description: ' + str(self.description),
            'path: ' + str(self.path),
            'version: ' + str(self.version),
            'full version: ' + str(self.full_version),
            'install date: ' + str(self.install_date)
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

        SafeArrayLock(safearray)

        # noinspection PyTypeChecker
        packs = comtypes.cast(
            safearray.contents.pvData,
            POINTER(POINTER(ISetupPackageReference))
        )

        cPackages = safearray.contents.rgsabound[0].cElements

        res = []
        for i in range(cPackages):
            p = packs[i]
            res.append(p)

        SafeArrayUnlock(safearray)
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
        return catalog.IsPrerelease()

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
            '{catalog}'
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

            except comtypes.COMError:
                break


IID_ISetupConfiguration = IID("{42843719-DB4C-46C2-8E7C-64F1816EFD5B}")


# Gets information about product instances set up on the machine.
class ISetupConfiguration(IUnknown):
    _iid_ = IID_ISetupConfiguration

    def __call__(self):
        try:
            return self.QueryInterface(ISetupConfiguration2)
        except ValueError:
            return self

    def __iter__(self):
        # noinspection PyUnresolvedReferences
        setup_enum = self.EnumInstances()
        helper = self.QueryInterface(ISetupHelper)

        for si in setup_enum:
            if not si:
                break

            yield si(helper)


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

        SafeArrayLock(safearray)

        # noinspection PyTypeChecker
        packs = comtypes.cast(
            safearray.contents.pvData,
            POINTER(POINTER(ISetupFailedPackageReference))
        )

        cPackages = safearray.contents.rgsabound[0].cElements

        res = []
        for i in range(cPackages):
            p = packs[i]
            p = p.QueryInterface(ISetupFailedPackageReference2)
            res.append(p)

        SafeArrayUnlock(safearray)
        res = Packages(res)
        return res

    @property
    def skipped_packages(self) -> Packages:
        try:
            # noinspection PyUnresolvedReferences
            safearray = self.GetSkippedPackages()
        except ValueError:
            return Packages([])

        SafeArrayLock(safearray)

        # noinspection PyTypeChecker
        packs = comtypes.cast(
            safearray.contents.pvData,
            POINTER(POINTER(ISetupFailedPackageReference))
        )

        cPackages = safearray.contents.rgsabound[0].cElements

        res = []
        for i in range(cPackages):
            p = packs[i]
            p = p.QueryInterface(ISetupFailedPackageReference2)
            res.append(p)

        SafeArrayUnlock(safearray)
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

        SafeArrayLock(safearray)

        names = comtypes.cast(safearray.contents.pvData, POINTER(BSTR))
        cPackages = safearray.contents.rgsabound[0].cElements

        res = []
        for i in range(cPackages):
            res.append(names[i])

        SafeArrayUnlock(safearray)

        return res

    def __iter__(self):
        for n in self.names:
            # noinspection PyUnresolvedReferences
            v = VARIANT()

            self.GetValue(n, ctypes.byref(v))

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

        SafeArrayLock(safearray)

        names = comtypes.cast(safearray.contents.pvData, POINTER(BSTR))
        cPackages = safearray.contents.rgsabound[0].cElements

        res = []
        for i in range(cPackages):
            res.append(names[i])

        SafeArrayUnlock(safearray)

        return res

    def __iter__(self):
        for n in self.names:
            # noinspection PyUnresolvedReferences
            v = VARIANT()

            self.GetValue(n, ctypes.byref(v))

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
        (['out'], POINTER(BSTR), "pbstrDisplayName")
    ),
    # Gets the description of the product installed in this instance.
    COMMETHOD(
        [],
        HRESULT,
        "GetDescription",
        # (['in'], LCID, "lcid"),
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
        comtypes.CoUninitialize()

    @classmethod
    def GetSetupConfiguration(cls):
        if cls._instance_ is None:
            comtypes.CoInitialize()
            instance = comtypes.CoCreateInstance(
                CLSID_SetupConfiguration,
                ISetupConfiguration,
                comtypes.CLSCTX_ALL
            )()

            cls._instance_ = weakref.ref(instance, cls._callback)
        else:
            instance = cls._instance_()

        return instance


if __name__ == '__main__':
    setup_config = SetupConfiguration.GetSetupConfiguration()
    for instance_config in setup_config:
        print(instance_config)
