import sys
import os
import operator
import errno
import re

from StringIO import StringIO
from subprocess import Popen, PIPE

from inspect import getmro, getclasstree, getdoc, getcomments

from utilities import MakeSummary, ChopDescription, WriteSphinxOutput
from utilities import FindControlImages, PickleClassInfo
from constants import object_types, MODULE_TO_ICON, DOXY_2_REST
import templates

ENOENT = getattr(errno, 'ENOENT', 0)
EPIPE  = getattr(errno, 'EPIPE', 0)

EPYDOC_PATTERN = re.compile(r'\S+{\S+}', re.DOTALL)

reload(sys)
sys.setdefaultencoding("utf-8")


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

        templ = [templates.TEMPLATE_PACKAGE_SUMMARY, templates.TEMPLATE_MODULE_SUMMARY]
        refs = ['mod', 'mod']
        
    elif libraryItem.kind in range(object_types.PY_MODULE, object_types.PYW_MODULE+1):
        list1 = libraryItem.GetItemByKind(object_types.FUNCTION)
        list2 = libraryItem.GetItemByKind(object_types.KLASS, recurse=True)

        templ = [templates.TEMPLATE_STD_FUNCTION_SUMMARY, templates.TEMPLATE_STD_CLASS_SUMMARY]
        refs = ['func', 'ref']
        add_tilde = [True, False]

    elif libraryItem.kind == object_types.KLASS:
        write_toc = False
        list1 = libraryItem.GetItemByKind(object_types.METHOD, object_types.INSTANCE_METHOD)
        list2 = libraryItem.GetItemByKind(object_types.PROPERTY)

        templ = [templates.TEMPLATE_METHOD_SUMMARY, templates.TEMPLATE_PROPERTY_SUMMARY]
        refs = ['meth', 'attr']
        add_tilde = [True, True]
        
    else:        
        raise Exception('Invalid library item: %s'%libraryItem.GetShortName())
    
    toctree = ''                

    for index, sub_list in enumerate([list1, list2]):
        table = []
        for item in sub_list:
            
            if item.is_redundant or item.GetShortName().startswith('__test') or '.extern.' in item.name:
                continue
            
            docs = ChopDescription(ReplaceWxDot(item.docs))
            table.append((item.name, docs))

            if item.kind != object_types.FUNCTION:
                toctree += '   %s\n'%item.name

        if table:
            summary = MakeSummary(table, templ[index], refs[index], add_tilde[index])
            stream.write(summary)
            
    if toctree and write_toc:
        stream.write(templates.TEMPLATE_TOCTREE%toctree)
        stream.write('\n\n')


def MakeSphinxFile(name):

    return os.path.join(os.getcwd(), 'docs', 'sphinx', '%s.txt'%name)


def ReplaceWxDot(text):

    # Double ticks with 'wx.' in them
    text = re.sub(r'``wx\.(.*?)``', r'``\1``   ', text)
    
    # Signle ticks with 'wx.' in them... try and referencing them
    text = re.sub(r'`wx\.(.*?)`', r'`\1`   ', text)

    # Masked is funny...
    text = text.replace('</LI>', '')

    space_added = False
    for old, new in DOXY_2_REST:

        if old not in text:
            continue
        
        if new in [':keyword', ':param']:
            if not space_added:
                space_added = True
                new_with_newline = '\n%s'%new
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
        header = ' '.join(line[2:])
        header = header.strip()

        newtext += header + '\n'
        newtext += '-'*len(header) + '\n\n'
    
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


def FindInHierarchy(klass, newlink):

    library = GetTopLevelParent(klass)
    return library.FindItem(newlink)


def FindBestLink(klass, newlink):

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
                else:
                    return ':class:`~%s`'%child.name

    full_loop = FindInHierarchy(klass, newlink)

    if full_loop:
        return full_loop

    return ':ref:`%s`'%newlink


def KillEpydoc(klass, newtext):

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
                newlink = newlink.replace('wx.', '')
                newlink = newlink.replace('wx', '')
                newlink = ':class:`%s`'%newlink.strip()
            else:
                newlink = '`%s`'%newlink

        elif 'I{' in regex:
            # It's an inclined text
            newlink = regex[start+1:end]
            newlink = ' `%s` '%newlink

        elif 'L{' in regex:
            # Some kind of link, but we can't figure it out
            # very easily from here... just use :ref:
            newlink = regex[start+1:end]

            if newlink.upper() == newlink:
                # Use double backticks
                newlink = '``%s``'%newlink
            else:
                # Try and reference it
                bestlink = FindBestLink(klass, newlink)
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

        self.docs = u''
        self.comments = u''

        self.is_redundant = False

        self.children = []


    def Add(self, klass):

        if u'lambda' in klass.name:
            return

        for child in self.children:
            if child.name == klass.name:
                return
            
        klass.parent = self
        self.children.append(klass)


    def Save(self):

        self.children = sorted(self.children, key=lambda k: (getattr(k, "order"), getattr(k, "name").lower()))

        if self.docs is None:
            self.docs = u''

        if self.comments is None or not self.comments.strip():
            self.comments = u''
            
        for child in self.children:
            child.Save()


    def GetImage(self):

        return self.kind


    def GetName(self):

        return self.name


    def GetShortName(self):

        return self.name.split(".")[-1]


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

        for n in xrange(count):
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


    def ToRest(self):

        pass
    

class Library(ParentBase):

    def __init__(self, name):

        ParentBase.__init__(self, name, object_types.LIBRARY)

        self.parent = None
        self.filename = u''
        self.order = 0
        self.obj_type = u"Library"
        self.python_version = u''

        self.sphinx_file = MakeSphinxFile(name)
        self.base_name = name


    def GetShortName(self):

        return self.name        
    

    def Walk(self, obj):

        if obj == self:
            obj.ToRest()

        # must have at least root folder
        children = obj.GetChildren()

        if not children:
            return 

        # check each name
        for child in children:

            if child.is_redundant:
                continue

            child.ToRest()

            # recursively scan other folders, appending results
            self.Walk(child)


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
                else:
                    return ':class:`~%s`'%child.name

            bestlink = self.FindItem(newlink, child)
            
            if bestlink:
                return bestlink

        return bestlink
            

    def GetPythonVersion(self):

        return self.python_version


    def ToRest(self):

        print '\n\nReST-ifying %s...\n\n'%self.base_name
        stream = StringIO()

        header = templates.TEMPLATE_DESCRIPTION%(self.base_name, self.base_name)
        stream.write(header)

        newtext = ReplaceWxDot(self.docs)
        stream.write(newtext + '\n\n')

        newtext = KillEpydoc(self, newtext)

        generic_summary(self, stream)
        WriteSphinxOutput(stream, self.sphinx_file)

                
class Module(ParentBase):

    def __init__(self, name, kind):

        ParentBase.__init__(self, name, kind)
        
        self.filename = u''
        self.sphinx_file = MakeSphinxFile(name)

        if kind == object_types.PACKAGE:
            self.obj_type = u"Package"
            self.order = kind
            return

        self.order = object_types.PY_MODULE
                    
        for dummy, icon, description in MODULE_TO_ICON:
            if icon == kind:
                self.obj_type = description
                break

        self.inheritance_diagram = None


    def ToRest(self):

        if self.is_redundant or self.GetShortName().startswith('__test') or '.extern.' in self.name:
            return
        
        stream = StringIO()

        label = 'Module'
        if self.kind == object_types.PACKAGE:
            label = 'Package'

        stream.write('.. module:: %s\n\n'%self.name)
        stream.write('.. currentmodule:: %s\n\n'%self.name)
        stream.write('.. highlight:: python\n\n')
            
        header = templates.TEMPLATE_DESCRIPTION%(self.name, '%s'%self.GetShortName())
        
        stream.write(header)
        
        newtext = ReplaceWxDot(self.docs)
        stream.write(newtext + '\n\n')

        newtext = KillEpydoc(self, newtext)

        spacer = '   '*self.name.count('.')
        
        if self.kind != object_types.PACKAGE:
            print '%s - %s (module)'%(spacer, self.name)
            if self.inheritance_diagram:
                png, map = self.inheritance_diagram.MakeInheritanceDiagram()
                short_name = self.GetShortName()
                image_desc = templates.TEMPLATE_INHERITANCE % (short_name, png, short_name, map)
                stream.write(image_desc)
        else:
            print '%s - %s (package)'%(spacer, self.name)

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

        WriteSphinxOutput(stream, self.sphinx_file)

                

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
            
            sup = item.replace("<class ", "").replace(">", "").replace("<type ", "")
            sup = sup.strip().replace('"', "").replace("'", "")
            if " at " in sup:
                sup = sup[0:sup.index(" at ")].strip()

            if 'wx._' in sup:
                name_parts = sup.split('.')
                sup = name_parts[-1]

            sortedSupClasses.append(sup.replace('wx.', ''))

        sortedSupClasses.sort()    
           
        for s in subs:
            s = repr(s)

            if "'" in s:
                start = s.index("'")
                end = s.rindex("'")
                cls = s[start+1:end]
            else:
                cls = s

            if 'wx._' in cls:
                name_parts = cls.split('.')
                cls = name_parts[-1]

            sortedSubClasses.append(cls.replace('wx.', ''))

        sortedSubClasses.sort()

        if len(sortedSubClasses) == 1 and sortedSubClasses[0] == 'object':
            sortedSubClasses = []
        
        if len(sortedSupClasses) == 1 and sortedSupClasses[0] == 'object':
            sortedSupClasses = []

        self.class_tree = make_class_tree(getclasstree(getmro(obj)))
        
        self.subClasses = sortedSubClasses
        self.superClasses = sortedSupClasses

        self.signature = ""
        self.inheritance_diagram = None
        
        self.order = 3
        self.obj_type = u"Class"
        self.sphinx_file = MakeSphinxFile(name)


    def ToRest(self):

        if self.is_redundant or self.GetShortName().startswith('__test') or '.extern.' in self.name:
            return

        stream = StringIO()

        parts = self.name.split('.')
        current_module = '.'.join(parts[0:-1])

        stream.write('.. currentmodule:: %s\n\n'%current_module)
        stream.write('.. highlight:: python\n\n')

        class_docs = ReplaceWxDot(self.docs)
        class_docs = KillEpydoc(self, class_docs)
        
        header = templates.TEMPLATE_DESCRIPTION%(self.name, self.GetShortName())
        stream.write(header)
        stream.write(class_docs + '\n\n')

        if self.inheritance_diagram:
            png, map = self.inheritance_diagram.MakeInheritanceDiagram()
            short_name = self.GetShortName()
            image_desc = templates.TEMPLATE_INHERITANCE % (short_name, png, short_name, map)
            stream.write(image_desc)

        appearance = FindControlImages(self.name.lower())
        if appearance:
            appearance_desc = templates.TEMPLATE_APPEARANCE % tuple(appearance)
            stream.write(appearance_desc + '\n\n')

        if self.subClasses:
            subs = [':ref:`%s`'%cls for cls in self.subClasses]
            subs = ', '.join(subs)
            subs_desc = templates.TEMPLATE_SUBCLASSES % subs
            stream.write(subs_desc)

        if self.superClasses:
            sups = [':ref:`%s`'%cls for cls in self.superClasses]
            sups = ', '.join(sups)
            sups_desc = templates.TEMPLATE_SUPERCLASSES % sups
            stream.write(sups_desc)

        generic_summary(self, stream)

        stream.write(templates.TEMPLATE_API)
        stream.write("\n.. class:: %s\n\n"%self.signature)

        docs = ''
        for line in class_docs.splitlines(True):
            docs += ' '*3 + line
            
        stream.write(docs + '\n\n')

        methods = self.GetItemByKind(object_types.METHOD, object_types.INSTANCE_METHOD)
        properties = self.GetItemByKind(object_types.PROPERTY)
        method_list = []
        
        for meth in methods:
            meth.Write(stream)
            if not meth.is_redundant:
                method_list.append((meth.GetShortName(), ''))
                    
        for prop in properties:
            prop.Write(stream, short_name)
            
        WriteSphinxOutput(stream, self.sphinx_file)

        self.bases = self.superClasses
        self.method_list = method_list
        
        PickleClassInfo(self.name, self)


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

        self.signature = self.signature.replace('wx.', '')
        self.signature = self.signature.rstrip(':').lstrip('class ')

        if ' def __init__' in self.signature:
            index = self.signature.index(' def __init__')
            self.signature = self.signature[0:index]

        self.signature = self.signature.strip()

        if len(self.signature) < 2:
            self.is_redundant = True


class ChildrenBase(object):
    
    def __init__(self, name, kind):

        self.name = name
        self.kind = kind

        self.order = 4        

        self.docs = u''
        self.comments = u''

        self.is_redundant = False

##        self.id = NewId()


    def GetImage(self):

        return self.kind


    def GetName(self):

        return self.name


    def GetShortName(self):

        return self.name.split(".")[-1]


    def GetChildren(self):

        return []
    

    def GetChildrenCount(self, recursively=True):

        return 0        


    def GetObject(self):

        return self.obj_type


    def Save(self):
        
        if self.docs is None:
            self.docs = u''

        if self.comments is None or not self.comments.strip():
            self.comments = u''


    def ToRest(self):

        pass
    

class Method(ChildrenBase):

    def __init__(self, name, kind):

        ChildrenBase.__init__(self, name, kind)
        
        self.order = 5
        
        self.arguments = []
        self.signature = u''

        self.obj_type = u"Method/Function"
        

    def Save(self):

        ChildrenBase.Save(self)        

        newargs = []
        if self.arguments and any(self.arguments[0]):
            for name, repr_val, eval_val in self.arguments:
                repr_val = (repr_val is not None and [repr_val] or [""])[0]
                eval_val = (eval_val is not None and [eval_val] or [""])[0]
                newargs.append((name, repr_val, eval_val))

        self.arguments = newargs

        self.signature = self.signature.replace('wx.', '')
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
            self.is_redundant = True            


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
        newdocs = ReplaceWxDot(self.docs)
        
        for line in newdocs.splitlines(True):
            text += indent + line

        text = KillEpydoc(self, text)
        text += '\n\n\n'
        stream.write(text)


class Property(ChildrenBase):

    def __init__(self, name, item):

        ChildrenBase.__init__(self, name, object_types.PROPERTY)
        
        self.getter = self.setter = self.deleter = ""

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
        
        self.obj_type = u"Property"
        self.order = 6


    def Write(self, stream, class_name):

        if self.is_redundant:
            return

        docs = ''
        for item in [self.setter, self.getter, self.deleter]:
            if item and 'lambda' not in item and not item.startswith('_'):
                if docs:
                    docs += ', :meth:`~%s.%s` '%(class_name, item)
                else:
                    docs += ':meth:`~%s.%s` '%(class_name, item)
                
        if docs:
            docs = 'See %s'%docs
            
            stream.write('   .. attribute:: %s\n\n'%self.GetShortName())
            stream.write('      %s\n\n\n'%docs)


class Attribute(ChildrenBase):

    def __init__(self, name, specs, value):

        specs = unicode(specs)        
        start, end = specs.find("'"), specs.rfind("'")
        specs = specs[start+1:end]

        strValue = repr(value)
        uspecs = specs.upper()

        try:
            kind = getattr(object_types, uspecs)
        except AttributeError:
            try:
                uspecs = uspecs + u"TYPE"
                kind = getattr(object_types, uspecs)
            except AttributeError:                
                kind = object_types.UNKNOWNTYPE
        
        try:
            reprValue = repr(value.__class__)
        except (NameError, AttributeError):
            reprValue = ""
            
        if u"class" in strValue or u"class" in reprValue:
            kind = object_types.INSTANCETYPE

        ChildrenBase.__init__(self, name, kind)
        
        self.value = strValue
        self.specs = specs

        try:
            self.docs = getdoc(value)
        except (NameError, AttributeError):
            self.docs = u''

        self.obj_type = u"Attribute"
        self.order = 7
        

    def ToRest(self):

        pass

