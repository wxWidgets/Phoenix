import sys
import os
import re

if sys.version_info < (3,):
    from StringIO import StringIO
else:
    from io import StringIO

from inspect import getmro, getclasstree, getdoc, getcomments

from .utilities import makeSummary, chopDescription, writeSphinxOutput, PickleFile
from .utilities import findControlImages, formatExternalLink, isPython3
from .constants import object_types, MODULE_TO_ICON, DOXY_2_REST, SPHINXROOT
from . import templates

EPYDOC_PATTERN = re.compile(r'\S+{\S+}', re.DOTALL)

if sys.version_info < (3,):
    reload(sys)
    sys.setdefaultencoding('utf-8')


def make_class_tree(tree):

    class_tree = []

    if isinstance(tree, list):
        for node in tree:
            class_tree.append(make_class_tree(node))
    else:
        name = tree[0].__name__
        class_tree.append(name)

    return class_tree


def generic_summary(libraryItem, stream):

    write_toc = True
    add_tilde = [True, True]

    if libraryItem.kind in [object_types.LIBRARY, object_types.PACKAGE]:
        list1 = libraryItem.GetItemByKind(object_types.PACKAGE)
        list2 = libraryItem.GetItemByKind(object_types.PY_MODULE, object_types.PYW_MODULE)
        list3 = libraryItem.GetItemByKind(object_types.FUNCTION)
        list4 = libraryItem.GetItemByKind(object_types.KLASS, recurse=True)

        all_lists = [list1, list2, list3, list4]
        templ = [ templates.TEMPLATE_PACKAGE_SUMMARY,
                  templates.TEMPLATE_MODULE_SUMMARY,
                  templates.TEMPLATE_STD_FUNCTION_SUMMARY,
                  templates.TEMPLATE_STD_CLASS_SUMMARY
                  ]
        refs = ['mod', 'mod', 'func', 'ref']
        add_tilde = [True, True, True, True]

    elif libraryItem.kind in range(object_types.PY_MODULE, object_types.PYW_MODULE+1):
        list1 = libraryItem.GetItemByKind(object_types.FUNCTION)
        list2 = libraryItem.GetItemByKind(object_types.KLASS, recurse=True)

        all_lists = [list1, list2]
        templ = [templates.TEMPLATE_STD_FUNCTION_SUMMARY, templates.TEMPLATE_STD_CLASS_SUMMARY]
        refs = ['func', 'ref']
        add_tilde = [True, True]

    elif libraryItem.kind == object_types.KLASS:
        write_toc = False
        list1 = libraryItem.GetItemByKind(object_types.METHOD, object_types.BUILTIN_FUNCTION)
        list2 = libraryItem.GetItemByKind(object_types.PROPERTY)

        all_lists = [list1, list2]
        templ = [templates.TEMPLATE_METHOD_SUMMARY, templates.TEMPLATE_PROPERTY_SUMMARY]
        refs = ['meth', 'attr']
        add_tilde = [True, True]

    else:
        raise Exception('Invalid library item: %s'%libraryItem.GetShortName())

    toctree = ''

    for index, sub_list in enumerate(all_lists):
        table = []
        for item in sub_list:

            if item.is_redundant:
                continue

            item_docs = replaceWxDot(item.docs)
            item_docs = killEpydoc(item, item_docs)
            docs = chopDescription(item_docs)
            table.append((item.name, docs))

            if item.kind != object_types.FUNCTION:
                toctree += '   %s\n'%item.name

        if table:
            summary = makeSummary(libraryItem.name, table, templ[index], refs[index], add_tilde[index])
            stream.write(summary)

    if toctree and write_toc:
        stream.write(templates.TEMPLATE_TOCTREE%toctree)
        stream.write('\n\n')


def makeSphinxFile(name):

    return os.path.join(os.getcwd(), 'docs', 'sphinx', '%s.txt' % name)


def replaceWxDot(text):

    # Masked is funny...
    text = text.replace('</LI>', '')

    space_added = False
    for old, new in DOXY_2_REST:

        if old not in text:
            continue

        if new in [':keyword', ':param']:
            if not space_added:
                space_added = True
                new_with_newline = '\n%s' % new
                text = text.replace(old, new_with_newline, 1)

        text = text.replace(old, new)

    lines = text.splitlines(True)
    newtext = ''

    for line in lines:
        if '@section' not in line:
            newtext += line
            continue

        # Extract the section header
        splitted = line.split()
        header = ' '.join(splitted[2:])
        header = header.strip()

        newtext += header + '\n'
        newtext += '-'*len(header) + '\n\n'

    # Try and replace True with ``True`` and False with ``False``
    # ``None`` gives trouble sometimes...

    for keyword in ['True', 'False']:
        newtext = re.sub(r'\s%s\s'%keyword, ' ``%s`` '%keyword, newtext)

    return newtext


def GetTopLevelParent(klass):

    parent = klass.parent

    if not parent:
        return klass

    parents = [parent]

    while parent:
        parent = parent.parent
        parents.append(parent)

    return parents[-2]


def findInHierarchy(klass, newlink):

    library = GetTopLevelParent(klass)
    return library.FindItem(newlink)


def findBestLink(klass, newlink):

    parent_class = klass.parent

    if klass.kind in range(object_types.FUNCTION, object_types.INSTANCE_METHOD):
        if parent_class.GetShortName() == newlink:
            return ':class:`%s`'%newlink
        else:
            child_names = [sub.GetShortName() for sub in parent_class.children]
            if newlink in child_names:
                index = child_names.index(newlink)
                child = parent_class.children[index]

                if child.kind in range(object_types.PACKAGE, object_types.PYW_MODULE+1):
                    return ':mod:`~%s`'%child.name
                elif child.kind in range(object_types.FUNCTION, object_types.INSTANCE_METHOD):
                    return ':meth:`~%s`'%child.name
                elif child.kind == object_types.KLASS:
                    return ':class:`~%s`'%child.name
                else:
                    return ':attr:`~%s`'%child.name

    full_loop = findInHierarchy(klass, newlink)

    if full_loop:
        return full_loop

    return ':ref:`%s`'%newlink


def killEpydoc(klass, newtext):

    epydocs = re.findall(EPYDOC_PATTERN, newtext)

    if not epydocs:
        return newtext

    newepydocs = epydocs[:]

    for item in epydocs:
        if '#{' in item:
            # this is for masked stuff
            newepydocs.remove(item)

    if not newepydocs:
        return newtext

    for regex in newepydocs:

        start = regex.index('{')
        end   = regex.index('}')

        if 'U{' in regex:
            # Simple link, leave it as it is
            newlink = regex[start+1:end]

        elif 'C{' in regex:
            # It's an inclined text, but we can attach some
            # class reference to it
            newlink = regex[start+1:end]

            if 'wx.' in regex or 'wx' in regex:
                newlink = ':class:`%s`' % newlink.strip()
            else:
                newlink = '`%s`' % newlink

        elif 'I{' in regex:
            # It's an inclined text
            newlink = regex[start+1:end]
            newlink = ' `%s` ' % newlink

        elif 'L{' in regex:
            # Some kind of link, but we can't figure it out
            # very easily from here... just use :ref:
            newlink = regex[start+1:end]

            if newlink.upper() == newlink:
                # Use double backticks
                newlink = '``%s``' % newlink
            else:
                # Try and reference it
                bestlink = findBestLink(klass, newlink)
                if bestlink:
                    newlink = bestlink

        else:
            # Something else, don't bother for the moment
            continue

        newtext = newtext.replace(regex, newlink)

    return newtext


class ParentBase(object):

    def __init__(self, name, kind):

        self.name = name
        self.kind = kind

        self.docs = ''
        self.comments = ''

        self.is_redundant = False

        self.children = []


    def Add(self, klass):

        if 'lambda' in klass.name:
            return

        for child in self.children:
            if child.name == klass.name:
                return

        klass.parent = self
        self.children.append(klass)


    def Save(self):

        if self.GetShortName().startswith('__test') or '.extern.' in self.name:
            self.is_redundant = True

        self.children = sorted(self.children, key=lambda k: (getattr(k, 'order'), getattr(k, 'name').lower()))

        if self.docs is None:
            self.docs = ''

        if self.comments is None or not self.comments.strip():
            self.comments = ''

        for child in self.children:
            child.Save()


    def GetImage(self):

        return self.kind


    def GetName(self):

        return self.name


    def GetShortName(self):

        return self.name.split('.')[-1]


    def GetObject(self):

        return self.obj_type


    def GetChildren(self):

        return self.children


    def GetChildrenCount(self, recursively=True):
        """
        Gets the number of children of this item.

        :param bool `recursively`: if ``True``, returns the total number of descendants,
         otherwise only one level of children is counted.
        """

        count = len(self.children)

        if not recursively:
            return count

        total = count

        for n in range(count):
            total += self.children[n].GetChildrenCount()

        return total


    def GetKindCount(self, minObj, maxObj=None):

        if maxObj is None:
            maxObj = minObj

        count = 0
        for child in self.children:
            if minObj <= child.kind <= maxObj:
                count += 1

        return count


    def GetItemByKind(self, minObj, maxObj=None, recurse=False):

        if maxObj is None:
            maxObj = minObj

        items = []
        for child in self.children:
            if minObj <= child.kind <= maxObj:
                items.append(child)

                if recurse:
                    items = items + child.GetItemByKind(minObj, maxObj, recurse)

        return items


    def ToRest(self, class_summary):

        pass


class Library(ParentBase):

    def __init__(self, name):

        ParentBase.__init__(self, name, object_types.LIBRARY)

        self.parent = None
        self.filename = ''
        self.order = 0
        self.obj_type = 'Library'
        self.python_version = ''

        self.sphinx_file = makeSphinxFile(name)
        self.base_name = name


    def GetShortName(self):

        return self.name


    def Walk(self, obj, class_summary):

        if obj == self:
            obj.ToRest(class_summary)

        # must have at least root folder
        children = obj.GetChildren()

        if not children:
            return

        # check each name
        for child in children:

            if child.is_redundant:
                continue

            child.ToRest(class_summary)

            # recursively scan other folders, appending results
            self.Walk(child, class_summary)


    def FindItem(self, newlink, obj=None):

        if obj is None:
            obj = self

        # must have at least root folder
        children = obj.GetChildren()
        bestlink = ''

        if not children:
            return bestlink

        # check each name
        for child in children:

            if child.is_redundant:
                continue

            parts = child.name.split('.')
            dotname = '.'.join(parts[-2:])
            if child.name.endswith(newlink) and (child.GetShortName() == newlink or dotname == newlink):
                if child.kind in range(object_types.PACKAGE, object_types.PYW_MODULE+1):
                    return ':mod:`~%s`'%child.name
                elif child.kind in range(object_types.FUNCTION, object_types.INSTANCE_METHOD+1):
                    return ':meth:`~%s`'%child.name
                elif child.kind == object_types.KLASS:
                    return ':class:`~%s`'%child.name
                else:
                    return ':attr:`~%s`'%child.name

            bestlink = self.FindItem(newlink, child)

            if bestlink:
                return bestlink

        return bestlink


    def GetPythonVersion(self):

        return self.python_version


    def ToRest(self, class_summary):

        print('\n\nReST-ifying %s...\n\n' % self.base_name)
        stream = StringIO()

        header = templates.TEMPLATE_DESCRIPTION%(self.base_name, self.base_name)
        stream.write(header)

        newtext = replaceWxDot(self.docs)
        newtext = killEpydoc(self, newtext)

        stream.write(newtext + '\n\n')

        generic_summary(self, stream)
        writeSphinxOutput(stream, self.sphinx_file)


    def ClassesToPickle(self, obj, class_dict):

        # must have at least root folder
        children = obj.GetChildren()

        if not children:
            return class_dict

        # check each name
        for child in children:
            if child.kind == object_types.KLASS:
                if child.is_redundant:
                    continue

                class_dict[child.name] = (child.method_list, child.bases, chopDescription(child.docs))

            # recursively scan other folders, appending results
            class_dict = self.ClassesToPickle(child, class_dict)

        return class_dict


    def Save(self):
        ParentBase.Save(self)

        class_dict = {}
        class_dict = self.ClassesToPickle(self, class_dict)

        pickle_file = os.path.join(SPHINXROOT, 'class_summary.pkl')
        with PickleFile(pickle_file) as pf:
            pf.items.update(class_dict)


class Module(ParentBase):

    def __init__(self, name, kind):

        ParentBase.__init__(self, name, kind)

        self.filename = ''
        self.sphinx_file = makeSphinxFile(name)

        if kind == object_types.PACKAGE:
            self.obj_type = 'Package'
            self.order = kind
            return

        self.order = object_types.PY_MODULE

        for dummy, icon, description in MODULE_TO_ICON:
            if icon == kind:
                self.obj_type = description
                break

        self.inheritance_diagram = None


    def ToRest(self, class_summary):

        if self.is_redundant:
            return

        stream = StringIO()

        label = 'Module'
        if self.kind == object_types.PACKAGE:
            label = 'Package'

        stream.write('.. module:: %s\n\n' % self.name)
        stream.write('.. currentmodule:: %s\n\n' % self.name)
        stream.write('.. highlight:: python\n\n')

        header = templates.TEMPLATE_DESCRIPTION % (self.name, self.name)

        stream.write(header)

        newtext = replaceWxDot(self.docs)
        newtext = killEpydoc(self, newtext)

        stream.write(newtext + '\n\n')

        spacer = '   '*self.name.count('.')

        # IMPORTANT!!
        # Remove this line to get back the inheritance diagram for a module
        #
        self.inheritance_diagram = None

        if self.kind != object_types.PACKAGE:
            print(('%s - %s (module)'%(spacer, self.name)))
            if self.inheritance_diagram:
                png, map = self.inheritance_diagram.makeInheritanceDiagram(class_summary)
                short_name = self.GetShortName()
                image_desc = templates.TEMPLATE_INHERITANCE % ('module', short_name, png, short_name, map)
                stream.write(image_desc)
        else:
            print('%s - %s (package)' % (spacer, self.name))

        generic_summary(self, stream)

        functions = self.GetItemByKind(object_types.FUNCTION)

        count = 0
        for fun in functions:
            if not fun.is_redundant:
                count = 1
                break

        if count > 0:
            stream.write('\n\nFunctions\n------------\n\n')

        for fun in functions:
            if fun.is_redundant:
                continue
            fun.Write(stream)

        writeSphinxOutput(stream, self.sphinx_file)


    def Save(self):

        ParentBase.Save(self)

        if self.GetShortName().startswith('__test') or '.extern.' in self.name:
            self.is_redundant = True


class Class(ParentBase):

    def __init__(self, name, obj):

        ParentBase.__init__(self, name, object_types.KLASS)

        try:
            subs = obj.__subclasses__()
        except (AttributeError, TypeError):
            subs = []

        sups = list(obj.__bases__)

        sortedSubClasses = []
        sortedSupClasses = []

        for item in sups:
            item = repr(item)

            sup = item.replace('<class ', '').replace('>', '').replace('<type ', '')
            sup = sup.strip().replace('"', '').replace("'", '')
            if ' at ' in sup:
                sup = sup[0:sup.index(' at ')].strip()

            if sup.startswith('wx._'):
                # take out the '_core' in things like 'wx._core.Control'
                parts = sup.split('.')
                if parts[1] == '_core':
                    del parts[1]
                else:
                    # or just the '_' otherwise
                    parts[1] = parts[1][1:]
                sup = '.'.join(parts)

            sortedSupClasses.append(sup)

        sortedSupClasses.sort()

        for s in subs:
            s = repr(s)

            if "'" in s:
                start = s.index("'")
                end = s.rindex("'")
                cls = s[start+1:end]
            else:
                cls = s

            sortedSubClasses.append(cls)

        sortedSubClasses.sort()

        if len(sortedSubClasses) == 1 and sortedSubClasses[0] == 'object':
            sortedSubClasses = []

        if len(sortedSupClasses) == 1 and sortedSupClasses[0] == 'object':
            sortedSupClasses = []

        self.class_tree = make_class_tree(getclasstree(getmro(obj)))

        self.subClasses = sortedSubClasses
        self.superClasses = sortedSupClasses

        self.signature = ''
        self.inheritance_diagram = None

        self.order = 3
        self.obj_type = 'Class'
        self.sphinx_file = makeSphinxFile(name)


    def ToRest(self, class_summary):

        if self.is_redundant:
            return

        stream = StringIO()

        parts = self.name.split('.')
        current_module = '.'.join(parts[0:-1])

        stream.write('.. currentmodule:: %s\n\n' % current_module)
        stream.write('.. highlight:: python\n\n')

        class_docs = replaceWxDot(self.docs)
        class_docs = killEpydoc(self, class_docs)

        header = templates.TEMPLATE_DESCRIPTION % (self.name, self.name)
        stream.write(header)
        stream.write(class_docs + '\n\n')

        if self.inheritance_diagram:
            png, map = self.inheritance_diagram.makeInheritanceDiagram(class_summary)
            short_name = self.GetShortName()
            image_desc = templates.TEMPLATE_INHERITANCE % ('class', short_name, png, short_name, map)
            stream.write(image_desc)

        appearance = findControlImages(self.name.lower())
        if appearance:
            appearance_desc = templates.TEMPLATE_APPEARANCE % tuple(appearance)
            stream.write(appearance_desc + '\n\n')

        if self.subClasses:
            subs = [formatExternalLink(cls) for cls in self.subClasses]
            subs = ', '.join(subs)
            subs_desc = templates.TEMPLATE_SUBCLASSES % subs
            stream.write(subs_desc)

        if self.superClasses:
            sups = [formatExternalLink(cls) for cls in self.superClasses]
            sups = ', '.join(sups)
            sups_desc = templates.TEMPLATE_SUPERCLASSES % sups
            stream.write(sups_desc)

        generic_summary(self, stream)

        stream.write(templates.TEMPLATE_API)
        stream.write('\n.. class:: %s\n\n'%self.signature)

        docs = ''
        for line in class_docs.splitlines(True):
            docs += ' '*3 + line

        stream.write(docs + '\n\n')

        methods = self.GetItemByKind(object_types.METHOD, object_types.BUILTIN_FUNCTION)
        properties = self.GetItemByKind(object_types.PROPERTY)

        for meth in methods:
            meth.Write(stream)

        for prop in properties:
            prop.Write(stream, short_name)

        writeSphinxOutput(stream, self.sphinx_file)
        self.bases = self.superClasses


    def Save(self):

        ParentBase.Save(self)
        pop = -1

        for index, child in enumerate(self.children):
            name = child.GetShortName()
            if name == '__init__':
                pop = index
                break

        if pop >= 0:
            init = self.children.pop(pop)
            self.children.insert(0, init)

        #self.signature = self.signature.replace('wx.', '')
        self.signature = self.signature.rstrip(':').lstrip('class ')

        if ' def __init__' in self.signature:
            index = self.signature.index(' def __init__')
            self.signature = self.signature[0:index]

        self.signature = self.signature.strip()

        # if len(self.signature) < 2: # ???
        #     self.is_redundant = True

        if self.GetShortName().startswith('__test') or '.extern.' in self.name:
            self.is_redundant = True

        if self.is_redundant:
            return

        methods = self.GetItemByKind(object_types.METHOD, object_types.BUILTIN_FUNCTION)
        method_list = []

        for meth in methods:
            if not meth.is_redundant:
                method_list.append(meth.GetShortName())

        self.method_list = method_list
        self.bases = self.superClasses


class ChildrenBase(object):

    def __init__(self, name, kind):

        self.name = name
        self.kind = kind

        self.order = 4

        self.docs = ''
        self.comments = ''

        self.is_redundant = False

##        self.id = NewId()


    def GetImage(self):

        return self.kind


    def GetName(self):

        return self.name


    def GetShortName(self):

        return self.name.split('.')[-1]


    def GetChildren(self):

        return []


    def GetChildrenCount(self, recursively=True):

        return 0


    def GetObject(self):

        return self.obj_type


    def Save(self):

        if self.docs is None:
            self.docs = ''

        if self.comments is None or not self.comments.strip():
            self.comments = ''


    def ToRest(self, class_summary):

        pass


class Method(ChildrenBase):

    def __init__(self, name, kind):

        ChildrenBase.__init__(self, name, kind)

        self.order = 5

        self.arguments = []
        self.signature = ''

        self.obj_type = 'Method/Function'


    def Save(self):

        ChildrenBase.Save(self)

        newargs = []
        if self.arguments and any(self.arguments[0]):
            for name, repr_val, eval_val in self.arguments:
                repr_val = (repr_val is not None and [repr_val] or [''])[0]
                eval_val = (eval_val is not None and [eval_val] or [''])[0]
                newargs.append((name, repr_val, eval_val))

        self.arguments = newargs
        self.signature = self.signature.rstrip(':').lstrip()

        if self.signature.startswith('def '):
            self.signature = self.signature[4:]

        if '@staticmethod' in self.signature:
            self.kind = object_types.STATIC_METHOD
        elif '@classmethod' in self.signature:
            self.kind = object_types.CLASS_METHOD

        if ' def ' in self.signature:
            index = self.signature.index(' def ')
            self.signature = self.signature[index+5:].strip()

        if '*' in self.signature:
            self.signature = self.signature.replace('*', r'\*')

        if not self.signature.strip():
            # if there is no signature, then check if the first line of
            # docstring looks like it might be it
            lines = self.docs.split('\n')
            first = lines[0]
            rest = '\n'.join(lines[1:]) if len(lines) > 1 else ''
            sig_start = self.GetShortName() + '('
            if sig_start in first:
                self.signature = first[first.find(sig_start):]
                self.docs = rest.strip()

        # if not self.signature.strip():      # ???
        #     self.is_redundant = True


    def Write(self, stream):

        if self.is_redundant:
            return

        if self.kind == object_types.FUNCTION:
            stream.write('.. function:: %s\n\n'%self.signature)
            indent = 3*' '
        else:
            if self.kind == object_types.STATIC_METHOD:
                stream.write('   .. staticmethod:: %s\n\n'%self.signature)
            elif self.kind == object_types.CLASS_METHOD:
                stream.write('   .. classmethod:: %s\n\n'%self.signature)
            else:
                stream.write('   .. method:: %s\n\n'%self.signature)
            indent = 6*' '

        if not self.docs.strip():
            stream.write('\n')
            return

        text = ''
        newdocs = replaceWxDot(self.docs)

        for line in newdocs.splitlines(True):
            text += indent + line

        text = killEpydoc(self, text)
        text += '\n\n\n'
        stream.write(text)


class Property(ChildrenBase):

    def __init__(self, name, item):

        ChildrenBase.__init__(self, name, object_types.PROPERTY)

        self.getter = self.setter = self.deleter = ''

        # is it a real property?
        if isinstance(item, property):
            try:
                if item.fget:
                    self.getter = item.fget.__name__
                if item.fset:
                    self.setter = item.fset.__name__
                if item.fdel:
                    self.deleter = item.fdel.__name__
            except AttributeError:
                # Thank you for screwing it up, Cython...
                if item.fget:
                    self.getter = item.fget.__class__.__name__
                if item.fset:
                    self.setter = item.fset.__class__.__name__
                if item.fdel:
                    self.deleter = item.fdel.__class__.__name__

        self.docs = getdoc(item)
        self.comments = getcomments(item)

        self.obj_type = 'Property'
        self.order = 6


    def Write(self, stream, class_name):

        if self.is_redundant:
            return

        docs = self.docs
        if not docs:
            for item in [self.setter, self.getter, self.deleter]:
                if item and 'lambda' not in item and not item.startswith('_'):
                    if docs:
                        docs += ', :meth:`~%s.%s` ' % (class_name, item)
                    else:
                        docs += ':meth:`~%s.%s` ' % (class_name, item)

            if docs:
                docs = 'See %s' % docs

        if docs:
            stream.write('   .. attribute:: %s\n\n' % self.GetShortName())
            docs = '\n      '.join(docs.splitlines())
            stream.write('      %s\n\n\n' % docs)


class Attribute(ChildrenBase):

    def __init__(self, name, specs, value):

        if isPython3():
            specs = str(specs)
        else:
            specs = unicode(specs)

        start, end = specs.find("'"), specs.rfind("'")
        specs = specs[start+1:end]

        strValue = repr(value)
        uspecs = specs.upper()

        try:
            kind = getattr(object_types, uspecs)
        except AttributeError:
            try:
                uspecs = uspecs + 'TYPE'
                kind = getattr(object_types, uspecs)
            except AttributeError:
                kind = object_types.UNKNOWNTYPE

        try:
            reprValue = repr(value.__class__)
        except (NameError, AttributeError):
            reprValue = ''

        if 'class' in strValue or 'class' in reprValue:
            kind = object_types.INSTANCETYPE

        ChildrenBase.__init__(self, name, kind)

        self.value = strValue
        self.specs = specs

        try:
            self.docs = getdoc(value)
        except (NameError, AttributeError):
            self.docs = ''

        self.obj_type = 'Attribute'
        self.order = 7


    def ToRest(self, class_summary):

        pass

