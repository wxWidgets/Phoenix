# -*- coding: utf-8 -*-

# Describe classes, methods and functions in a module.
# Works with user-defined modules, all Python library
# modules, including built-in modules.

import os
import sys
import types
import traceback
import pkgutil


from buildtools.config import phoenixDir

from inspect import getargspec, ismodule, getdoc, getmodule, getcomments, isfunction
from inspect import ismethoddescriptor, getsource, ismemberdescriptor, isgetsetdescriptor
from inspect import isbuiltin, isclass, getfile, ismethod

from .librarydescription import Library, Module, Class
from .librarydescription import Method, Property, Attribute

from . import inheritance

from .utilities import isPython3, PickleFile
from .constants import object_types, EXCLUDED_ATTRS, MODULE_TO_ICON
from .constants import CONSTANT_RE

if sys.version_info < (3,):
    reload(sys)
    sys.setdefaultencoding('utf-8')

if isPython3():
    MethodTypes = (classmethod, types.MethodType, types.ClassMethodDescriptorType)
else:
    MethodTypes = (classmethod, types.MethodType)

try:
    import wx
except ImportError:

    wxPath = ''
    basePath = ''

    for path in sys.path:
        if 'wx-' in path:
            dummy, newPath = os.path.split(path)
            if newPath > wxPath:
                wxPath = newPath
                basePath = dummy

    if not wxPath:
        raise Exception('Unable to find the wx package')

    sys.path.insert(0, os.path.join(basePath, wxPath))

import wx

print(('\nUSING VERSION: %s\n'%wx.VERSION_STRING))


if hasattr(os.path, 'relpath'):
    relpath = os.path.relpath # since Python 2.6
else:
    def relpath(path, start=os.path.curdir):
        """Return a relative version of a path"""

        if not path:
            raise ValueError('no path specified')

        start_list = os.path.abspath(start).split(os.path.sep)
        path_list = os.path.abspath(path).split(os.path.sep)

        # Work out how much of the filepath is shared by start and path.
        i = len(os.path.commonprefix([start_list, path_list]))

        rel_list = [os.path.pardir] * (len(start_list)-i) + path_list[i:]
        if not rel_list:
            return os.path.curdir

        return os.path.join(*rel_list)


def format_traceback():

    t, v = sys.exc_info()[:2]
    message = ''.join(traceback.format_exception_only(t, v)).replace('\n', ' ')
    return message.strip()


def format_method(method):

    method = method.strip()

    if 'def ' not in method:
        return None, None

    indx1, indx2, indx3 = method.index('def '), method.index('('), method.rindex(')')
    name = method[indx1+4:indx2]
    signature = method[indx2+1:indx3]

    if '\n' in signature:
        sig = signature.split('\n')
        params = ''
        for s in sig:
            params += s.strip() + ' '
        params = params.rstrip()
    else:
        params = signature

    return name, params


def analyze_params(obj, signature):

    params = signature.split(',')
    if 'self' in params:
        params.remove('self')
        signature = ','.join(params)

    param_tuple = []

    if not params:
        return signature, param_tuple

    try:
        arginfo = getargspec(obj)
        # TODO: Switch to getfullargspec
    except (TypeError, ValueError):
        arginfo = None

    pevals = {}

    if arginfo:
        args = arginfo[0]
        argsvar = arginfo[1]

        if arginfo[3]:

            dl = len(arginfo[3])
            al = len(args)
            defargs = args[al-dl:al]
            info = arginfo[3]

            for d, i in zip(defargs, info):
                pevals[d] = i

    for par in params:
        p = par.strip()
        pvalue = peval = None

        if '=' in p:
            all_values = p.split('=')
            pname, pvalue = all_values[0].strip(), '='.join(all_values[1:]).strip()
            pvalue = pvalue.strip()
            if pname in pevals:
                try:
                    if isPython3():
                        peval = str(pevals[pname])
                    else:
                        peval = unicode(pevals[pname])
                except UnicodeDecodeError:
                    peval = repr(pevals[pname])
                except TypeError:
                    peval = ''
        else:
            pname = p

        param_tuple.append((pname, pvalue, peval))

    return signature, param_tuple


def get_constructor(source):

    description = ''
    hasComma = False

    for line in source.split('\n'):

        if '#' in line:
            line = line[0:line.index('#')].strip()

        if ':' in line:
            hasComma = True
            commaPos = line.index(':')

        if ('"""' in line or "'''" in line) and hasComma:
            break

        if hasComma and ' def ' in line:
            defPos = line.index(' def ')
            if defPos > commaPos:
                break

        description += ' ' + line.strip()

        if '):' in line or ') :' in line or ')  :' in line:
            break

    return description


def inspect_source(method_class, obj, source):

    description = get_constructor(source)
    name, params = format_method(description)

    if name is None:
        return

    signature, param_tuple = analyze_params(obj, params)

    method_class.arguments = param_tuple
    method_class.signature = description.strip()

    if 'classmethod ' in description or is_classmethod(obj):
        method_class.kind = object_types.CLASS_METHOD
    elif 'staticmethod ' in description:
        method_class.kind = object_types.STATIC_METHOD


def is_classmethod(instancemethod):
    """ Determine if an instancemethod is a classmethod. """

    # attribute = (isPython3() and ['__self__'] or ['im_self'])[0]
    # if hasattr(instancemethod, attribute):
    #     return getattr(instancemethod, attribute) is not None
    # return False

    return isinstance(instancemethod, MethodTypes)


def describe_func(obj, parent_class, module_name):
    """
    Describe the function object passed as argument.
    If this is a method object, the second argument will
    be passed as True.
    """

    try:
        name = obj.__name__
    except AttributeError:
        # Funny comtypes...
        return

    if name.startswith('_') and '__init__' not in name:
        return

    name = parent_class.name + '.' + name

    docs = getdoc(obj)
    comments = getcomments(obj)

    if isfunction(obj):
        # in Py3 unbound methods have same type as functions.
        if isinstance(parent_class, Class):
            method = object_types.METHOD
        else:
            method = object_types.FUNCTION
    elif ismethod(obj):
        method = object_types.METHOD
    elif ismethoddescriptor(obj):
        method = object_types.METHOD_DESCRIPTOR

    if isinstance(obj, types.MethodType):
        method = object_types.INSTANCE_METHOD

    try:
        source_code = getsource(obj)
    except (IOError, TypeError):
        source_code = ''

    klass = Method(name, method)
    klass.docs = docs

    klass_module = getmodule(obj)
    if klass_module and klass_module.__name__ != module_name:
        klass.is_redundant = True

    if source_code:
        inspect_source(klass, obj, source_code)
        klass.number_lines = '%d' % len(source_code.split('\n'))

    if isinstance(obj, staticmethod):
        klass.kind = method = object_types.STATIC_METHOD

    if is_classmethod(obj):
        klass.kind = method = object_types.CLASS_METHOD

    try:
        code = None
        if method in [object_types.METHOD, object_types.METHOD_DESCRIPTOR, object_types.INSTANCE_METHOD]:
            if isPython3():
                code = obj.__func__.__code__
            else:
                code = obj.im_func.func_code
        elif method == object_types.STATIC_METHOD:
            if isPython3():
                code = obj.__func__.__code__
            else:
                code = obj.im_func.func_code
        else:
            if isPython3():
                code = obj.__code__
            else:
                code = obj.func_code
    except AttributeError:
        code = None

    if code is not None:
        klass.firstlineno = '%d' % code.co_firstlineno

    parent_class.Add(klass)


def describe_class(obj, module_class, module_name, constants):
    """
    Describe the class object passed as argument,
    including its methods.
    """

    class_name = obj.__name__

    if class_name == 'object':
        return

    class_name = module_class.name + '.' + class_name

    docs = getdoc(obj)
    comments = getcomments(obj)

    obj_dict = obj.__dict__

    klass = Class(class_name, obj)

    count = 0

    for name in obj_dict:

        if name.startswith('_') and '__init__' not in name:
            continue

        if name in EXCLUDED_ATTRS:
            continue

        try:
            # item = getattr(obj, name)   # ????
            item = obj_dict.get(name)
        except AttributeError:
            # Thanks to ReportLab for this funny exception...
            continue
        except ImportError:
            # This can come from the pseudo module in six
            message = "ImportError from '%s.%s'.\n         Exception was: %s"%(obj, name, format_traceback())
            print(('\nWARNING: %s\n' % message))
            continue

        if ismodule(item):
            continue

        if isbuiltin(item):
            count += 1
        elif ismethod(item) or isfunction(item) or ismethoddescriptor(item) or \
             isinstance(item, MethodTypes):
            count += 1
            describe_func(item, klass, module_name)
        elif isclass(item):
            count += 1
            describe_class(item, klass, module_name, constants)
        else:
            name = class_name + '.' + name
            if isinstance(item, property) or isgetsetdescriptor(item):
                item_class = Property(name, item)
                klass.Add(item_class)

                item_module = getmodule(obj)
                if item_module and item_module.__name__ != module_name:
                    item_class.is_redundant = True

            else:
                item_class = Attribute(name, type(item), item)
                klass.Add(item_class)

                if constants:
                    item_class.is_redundant = name not in constants

        count += 1

    klass.docs = docs
    klass.comments = comments

    klass_module = getmodule(obj)
    if klass_module and klass_module.__name__ != module_name:
        klass.is_redundant = True
    else:
        klass.inheritance_diagram = inheritance.InheritanceDiagram([obj], klass)

    module_class.Add(klass)

    try:
        source_code = getsource(obj)
    except (IOError, TypeError):
        source_code = ''

    if source_code:
        description = get_constructor(source_code)
        if '(' not in description and ':' in description:
            description = description[0:description.index(':')]

        klass.signature = description.strip()
        klass.number_lines = '%d' % len(source_code.split('\n'))

    if not klass.signature:
        if klass.superClasses:
            klass.signature = '{}({})'.format(obj.__name__, ','.join(klass.superClasses))
        else:
            klass.signature = '{}(object)'.format(obj.__name__)


def describe_module(module, kind, constants=[]):
    """
    Describe the module object passed as argument
    including its classes and functions.
    """

    module_name = module.__name__

    if kind == object_types.LIBRARY:
        klass = Library(module_name)
    else:
        klass = Module(module_name, kind)

    klass.docs = getdoc(module)
    klass.comments = getcomments(module)

    klass.filename = module.__file__
    inheritance_diagram = []

    count = 0

    for name in dir(module):

        if name in EXCLUDED_ATTRS:
            continue

        obj = getattr(module, name)

        if ismodule(obj):
            continue

        if ismemberdescriptor(obj) or isgetsetdescriptor(obj):
            continue

        if isclass(obj):
            count += 1
            describe_class(obj, klass, module_name, constants)

            if obj.__module__ == module.__name__:
                inheritance_diagram.append(obj)

        elif isbuiltin(obj):
            count += 1
        elif ismethod(obj) or isfunction(obj) or ismethoddescriptor(obj) or \
             isinstance(obj, types.MethodType):
            count +=1
            describe_func(obj, klass, module_name)
        else:
            attribute = Attribute(module_name + '.' + name, type(obj), obj)
            klass.Add(attribute)

            if constants:
                attribute.is_redundant = name not in constants

    if kind not in [object_types.PACKAGE, object_types.LIBRARY]:
        if inheritance_diagram and len(inheritance_diagram) < 20:
            klass.inheritance_diagram = inheritance.InheritanceDiagram(inheritance_diagram, klass)

    return klass, count


def Import(init_name, import_name, full_process=True):

    directory, module_name = os.path.split(init_name)
    dirname = os.path.dirname(directory)

    if not full_process:
        path = list(sys.path)
        sys.path.insert(0, dirname)

    try:
        #mainmod = importlib.import_module(import_name)
        terminal_module = import_name.split('.')[-1]
        mainmod = __import__(import_name, globals(), fromlist=[terminal_module])
    except (ImportError, NameError):
        message = format_traceback()
        print('Error: %s' % message)

        if not full_process:
            sys.path = path[:]

        return

    if not full_process:
        sys.path = path[:]
        try:
            version = mainmod.__version__
        except AttributeError:
            try:
                version = mainmod.__VERSION__
            except AttributeError:
                print(('Warning: Library "%s" has no __version__ or __VERSION__ attribute.'%import_name))
                return

        print(version)

    return mainmod


def PrintProgress(name, looped_names):

    looped_names.append(name)
    if len(looped_names) == 4:
        message = ', '.join(looped_names)
        looped_names = []
        print(message)

    return looped_names



def FindModuleType(filename):

    splitext = os.path.splitext(filename)[0]
    for extension, icon, description in MODULE_TO_ICON:
        if os.path.isfile(splitext + extension):
            return icon


def SubImport(import_string, module, parent_class, ispkg):

    try:
        #submod = importlib.import_module(import_string)
        submod = __import__(import_string, globals(), fromlist=[module])
    except:
        # pubsub and Editra can be funny sometimes...
        message = "Unable to import module/package '%s.%s'.\n         Exception was: %s"%(import_string, module, format_traceback())
        print(('\nWARNING: %s\n'%message))
        return None, 0

    if not ismodule(submod):
        return None, 0

    filename = getfile(submod)

    subpath = os.path.dirname(filename)
    if subpath not in sys.path:
        sys.path.append(subpath)   # *** WHY?

    if ispkg:
        kind = object_types.PACKAGE
    else:
        kind = FindModuleType(filename)

    constants = []

    if kind in [object_types.PY_MODULE, object_types.PACKAGE]:

        with open(filename, 'rt') as f:
            contents = f.read()
            consts = CONSTANT_RE.findall(contents)

        for c in consts:
            if ',' in c:
                c = c.split(',')
                constants.extend([v.strip() for v in c])
            else:
                constants.append(c.strip())

    module_class, count = describe_module(submod, kind=kind, constants=constants)
    parent_class.Add(module_class)

    return module_class, count


def ToRest(import_name):

    sphinxDir = os.path.join(phoenixDir(), 'docs', 'sphinx')
    pickle_file = os.path.join(sphinxDir, '%s.pkl' % import_name)

    pf = PickleFile(pickle_file)
    library_class = pf.read()

    pf = PickleFile(os.path.join(sphinxDir, 'class_summary.pkl'))
    class_summary = pf.read()

    library_class.Walk(library_class, class_summary)


def ModuleHunter(init_name, import_name, version):

    sphinxDir = os.path.join(phoenixDir(), 'docs', 'sphinx')
    pickle_file = os.path.join(sphinxDir, '%s.pkl' % import_name)

    # TODO: instead of just skipping to generating the ReST files, do some
    # dependency checking and rescan those files that are newer than the
    # pickle file.
    if os.path.isfile(pickle_file):
        ToRest(import_name)
        return

    directory, module_name = os.path.split(init_name)
    path = list(sys.path)

    mainmod = Import(init_name, import_name)

    if mainmod is None:
        return

    message = "Importing main library '%s'..." % import_name
    print('Message: %s' % message)

    module_name = os.path.splitext(getfile(mainmod))[0] + '.py'
    with open(module_name, 'rt') as fid:
        contents = fid.read()
    constants = CONSTANT_RE.findall(contents)

    library_class, count = describe_module(mainmod, kind=object_types.LIBRARY, constants=constants)
    library_class.name = '%s-%s'%(import_name, version)

    message = "Main library '%s' imported..." % library_class.name
    print('Message: %s' % message)

    message = "Importing sub-modules and sub-packages...\n"
    print('Message: %s' % message)

    looped_names = []
    ancestors_dict = {import_name: library_class}

    for importer, module_name, ispkg in pkgutil.walk_packages(path=[directory],
                                                              prefix=import_name+'.',
                                                              onerror=lambda x: None):
        import_string = module_name
        splitted = module_name.split('.')

        fromlist = splitted[-1]
        parent_name = '.'.join(splitted[0:-1])

        parent_class = ancestors_dict[parent_name]
        module_class, count = SubImport(import_string, fromlist, parent_class, ispkg)

        if module_class is None:
            continue

        looped_names = PrintProgress(module_name, looped_names)

        if module_name not in ancestors_dict:
            ancestors_dict[module_name] = module_class

    major, minor, micro, release = sys.version_info[0:-1]
    pythonVersion = '%d.%d.%d-%s'%(major, minor, micro, release)

    library_class.python_version = pythonVersion
    library_class.Save()

    sys.path[:] = path # restore

    pf = PickleFile(pickle_file)
    pf.write(library_class)

    ToRest(import_name)


if __name__ == '__main__':

    argv = sys.argv[1:]

    if len(argv) == 2:
        init_name, import_name = argv
        Import(init_name, import_name, full_process=False)
    else:
        init_name, import_name, version, save_dir = argv
        ModuleHunter(init_name, import_name, version, save_dir)




