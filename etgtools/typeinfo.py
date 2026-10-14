#---------------------------------------------------------------------------
# Name:        etgtools/typeinfo.py
# Purpose:     Type information shared between the etg scripts
#
# License:     wxWindows License
#---------------------------------------------------------------------------

"""
Each etg script runs in its own process, but the type hints generated for one
module can depend on things defined by other scripts, such as which Python
types a class can be automatically converted from, or which module a name
lives in. So build_wxpy.py runs the etg scripts in two passes. In the first pass,
with --typeinfo on the command line, each script only saves that information
to its own file. Those files are then merged into one, and the second, normal
pass reads it while generating the code.
"""

import ast
import glob
import json
import os
import re
import sys

phoenixRoot = os.path.abspath(os.path.split(__file__)[0]+'/..')
TYPEINFO_DIR = os.path.join(phoenixRoot, 'sip', 'gen', 'typeinfo')
MERGED_FILE = os.path.join(TYPEINFO_DIR, 'typeinfo.json')

_merged = None
_nameSets = None
_eventClasses = None
_enumSet = None

#---------------------------------------------------------------------------

def scriptInfoFile(scriptId):
    return os.path.join(TYPEINFO_DIR, 'scripts', scriptId + '.json')


def pyModuleName(module):
    """The name of the Python module (and .pyi file) that items in module go in"""
    name = module.module
    return name[1:] if name.startswith('_') else name


def topLevelNames(code):
    """The names defined at the top level of some Python code"""
    def _processItem(item, names):
        if isinstance(item, ast.Assign):
            for t in item.targets:
                _processItem(t, names)
        elif isinstance(item, ast.Name):
            names.append(item.id)
        elif isinstance(item, (ast.ClassDef, ast.FunctionDef)):
            names.append(item.name)
        elif isinstance(item, ast.AnnAssign):
            if isinstance(item.target, ast.Name):
                # Exclude private TypeAliases like _TwoInts, which every
                # .pyi file defines for itself
                isTypeAlias = isinstance(item.annotation, ast.Name) and item.annotation.id == 'TypeAlias'
                if not (isTypeAlias and item.target.id.startswith('_')):
                    names.append(item.target.id)

    names = []
    for item in ast.parse(code).body:
        _processItem(item, names)
    return names


def collect(module):
    """Gather the type information that module provides for other scripts"""
    from etgtools.generators import Utf8EncodingStream
    from etgtools.pi_generator import PiWrapperGenerator
    from etgtools.extractors import ClassDef, EnumDef, GlobalVarDef, TypedefDef
    from etgtools.tweaker_tools import FixWxPrefix, getWrapperGenerator, isCharString, removeWxPrefix

    # Generating the .pyi code is the simplest way to find exactly which names
    # this script will add to the module's .pyi file. As in the normal run,
    # the wrapper generator needs to run first, since it fills in things like
    # docstrings that the .pyi generator uses. Its output isn't needed.
    getWrapperGenerator().generateModule(module, Utf8EncodingStream())
    stream = Utf8EncodingStream()
    generator = PiWrapperGenerator()
    generator.forwardDeclarations = False
    generator.generateModule(module, stream)

    # Classes given a different name in Python, like wxPoint2DDouble -> Point2D
    renames = {}
    # and typedefs that don't become classes in Python, which are replaced by
    # the type they are an alias of.
    typedefs = {}
    for item in module.allItems():
        if isinstance(item, ClassDef) and item.pyName and not item.ignored:
            name = removeWxPrefix(item.name)
            if item.pyName != name:
                renames[name] = item.pyName
    # Typedefs inside classes, like value_type, could mean different things in
    # different classes, so only the module level ones are used.
    # Enums that aren't scoped also accept ints, so record their names, like
    # FontWeight or GridCellAttr.AttrKind
    enums = []
    def findEnums(items, path):
        for item in items:
            if isinstance(item, ClassDef):
                findEnums(list(item.items) + list(item.innerclasses),
                          path + [item.pyName or removeWxPrefix(item.name)])
            elif (isinstance(item, EnumDef) and not item.isScoped and item.name
                    and '@' not in item.name and not item.ignored):
                enums.append('.'.join(path + [removeWxPrefix(item.name)]))
    findEnums(module.items, [])
    # and the constants that are bytes, since SIP converts char* to bytes
    bytesConstants = []
    for item in module.items:
        if isinstance(item, TypedefDef) and not item.docAsClass:
            if not any(c in item.type for c in '<(['):
                typedefs[removeWxPrefix(item.name)] = item.type
        elif isinstance(item, GlobalVarDef) and item.type and isCharString(item.type):
            bytesConstants.append(item.pyName or removeWxPrefix(item.name))

    return {
        'module': pyModuleName(module),
        'names': sorted(set(topLevelNames(stream.getvalue()))),
        'renames': dict(sorted(renames.items())),
        'typedefs': dict(sorted(typedefs.items())),
        'bytesConstants': sorted(bytesConstants),
        'enums': sorted(set(enums)),
        'autoConversions': {name: list(types) for name, types
                            in sorted(FixWxPrefix._auto_conversions.items())},
    }


def writeScriptInfo(module, scriptId):
    from etgtools.generators import textfile_open
    info = collect(module)
    filename = scriptInfoFile(scriptId)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with textfile_open(filename, 'wt') as f:
        json.dump(info, f, indent=1)


def mergeScriptInfo(scriptIds):
    """
    Merge the info files for scriptIds into MERGED_FILE. The file is only
    rewritten when its contents change, since build_wxpy.py uses its timestamp to
    decide which scripts need to run again. Returns True if it was rewritten.
    """
    names = {}
    renames = {}
    typedefs = {}
    bytesConstants = set()
    enums = set()
    autoConversions = {}
    for scriptId in scriptIds:
        with open(scriptInfoFile(scriptId), encoding='utf-8') as f:
            info = json.load(f)
        names.setdefault(info['module'], set()).update(info['names'])
        renames.update(info['renames'])
        typedefs.update(info['typedefs'])
        bytesConstants.update(info['bytesConstants'])
        enums.update(info['enums'])
        autoConversions.update(info['autoConversions'])

    merged = {
        'names': {m: sorted(n) for m, n in sorted(names.items())},
        'renames': dict(sorted(renames.items())),
        'typedefs': dict(sorted(typedefs.items())),
        'bytesConstants': sorted(bytesConstants),
        'enums': sorted(enums),
        'autoConversions': dict(sorted(autoConversions.items())),
    }
    text = json.dumps(merged, indent=1)
    if os.path.exists(MERGED_FILE):
        with open(MERGED_FILE, encoding='utf-8') as f:
            if f.read() == text:
                return False
    with open(MERGED_FILE, 'w', encoding='utf-8') as f:
        f.write(text)
    return True


def load():
    """The merged type info, from the latest first pass"""
    global _merged
    if _merged is None:
        if os.path.exists(MERGED_FILE):
            with open(MERGED_FILE, encoding='utf-8') as f:
                _merged = json.load(f)
        else:
            # The first pass runs before the file exists, but doesn't need it
            if '--typeinfo' not in sys.argv:
                print('WARNING: %s not found, run "build_wxpy.py etg" to create it.' %
                      os.path.relpath(MERGED_FILE, phoenixRoot))
            _merged = {}
        _merged.setdefault('names', {})
        _merged.setdefault('renames', {})
        _merged.setdefault('typedefs', {})
        _merged.setdefault('bytesConstants', [])
        _merged.setdefault('enums', [])
        _merged.setdefault('autoConversions', {})
    return _merged


def moduleOf(name, fromModule):
    """
    The Python module that a top-level name used in fromModule comes from:
    fromModule itself, core, or else whichever other module defines it. Returns
    None if that isn't known, or is ambiguous.
    """
    global _nameSets
    if _nameSets is None:
        _nameSets = {m: set(names) for m, names in load()['names'].items()}
    for m in (fromModule, 'core'):
        if name in _nameSets.get(m, ()):
            return m
    others = [m for m, names in _nameSets.items() if name in names]
    return others[0] if len(others) == 1 else None


def eventClasses():
    """
    The C++ event class for each wxEVT_* event type, from their declarations
    in the wxWidgets headers, like
    wxDECLARE_EXPORTED_EVENT(WXDLLIMPEXP_CORE, wxEVT_BUTTON, wxCommandEvent)
    """
    global _eventClasses
    if _eventClasses is None:
        from buildtools.config import wxDir
        pattern = re.compile(r'wxDECLARE_(?:EXPORTED_)?EVENT\(\s*(?:\w+\s*,\s*)?(wxEVT_\w+)\s*,\s*(\w+)\s*\)')
        _eventClasses = {}
        for filename in glob.glob(os.path.join(wxDir(), 'include', 'wx', '**', '*.h'), recursive=True):
            with open(filename, encoding='utf-8', errors='replace') as f:
                for m in pattern.finditer(f.read()):
                    _eventClasses[m.group(1)] = m.group(2)
    return _eventClasses


def isEnum(name):
    """
    Whether name is an enum that isn't scoped, optionally qualified with
    the name of its module, like adv.CalendarDateBorder
    """
    global _enumSet
    if _enumSet is None:
        _enumSet = set(load()['enums'])
    if name in _enumSet:
        return True
    module, _, rest = name.partition('.')
    return module in load()['names'] and rest in _enumSet
