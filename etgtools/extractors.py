#---------------------------------------------------------------------------
# Name:        etgtools/extractors.py
# Author:      Robin Dunn
#
# Created:     3-Nov-2010
# Copyright:   (c) 2010 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

"""
Functions and classes that can parse the Doxygen XML files and extract the
wxWidgets API info which we need from them.
"""

import sys
import os
import pprint
import xml.etree.ElementTree as et



#---------------------------------------------------------------------------
# These classes simply hold various bits of information about the classes,
# methods, functions and other items in the C/C++ API being wrapped.
#
# NOTE: Currently very little is being done with the docstrings. They can
# either be reprocessed later by the document generator or we can do more
# tinkering with them here.  It just depends on decisions not yet made...
#---------------------------------------------------------------------------

class BaseDef(object):
    """
    The base class for all element types and provides the common attributes
    and functions that they all share.
    """
    nameTag = 'name'
    def __init__(self, element=None):
        self.name = ''          # name of the item
        self.pyName = ''        # rename to this name
        self.ignored = False    # skip this item
        self.briefDoc = ''      # either a string or a single para Element
        self.detailedDoc = []   # collection of para Elements

        # The items list is used by some subclasses to collect items that are
        # part of that item, like methods of a ClassDef, etc.
        self.items = []       
        
        if element is not None:
            self.extract(element)

    def __iter__(self):
        return iter(self.items)


    def extract(self, element):
        # Pull info from the ElementTree element that is pertinent to this
        # class. Should be overridden in derived classes to get what each one
        # needs in addition to the base.
        self.name = element.find(self.nameTag).text
        bd = element.find('briefdescription')
        if len(bd):
            self.briefDoc = bd[0] # Should be just one <para> element
        self.detailedDoc = list(element.find('detaileddescription'))

        
    def dump(self, indent=0, stream=None):
        # debug helper, prints the extracted items
        txt = ("name:         %s\n" 
               "pyName:       %s\n" 
               "ignored:      %s\n"
               "briefDoc:     %s\n" 
               "detailedDoc:  %s\n" ) % \
            (self.name, self.pyName, self.ignored, self.briefDoc, 
             _pf(self.detailedDoc, indent)) 
        _print(txt, indent, stream)
        
        
    def ignore(self, val=True):
        self.ignored = val
                
        
    def find(self, name):
        """
        Locate and return an item within this item that has a matching name.
        The name string can use a dotted notation to continue the search
        recursively.  Raises ExtractorError if not found.
        """
        try:
            head, tail = name.split('.', 1)
        except ValueError:
            head, tail = name, None
        for item in self._findItems():
            if item.name == head or item.pyName == head:
                if not tail:
                    return item
                else:
                    return item.find(tail)                
        else: # got though all items with no match
            raise ExtractorError("Unable to find item named '%s' within %s named '%s'" %
                                 (head, self.__class__.__name__, self.name))

        
        
    def addItem(self, item):
        self.items.append(item)
        
    def insertItem(self, index, item):
        self.items.insert(index, item)
        
    def insertItemAfter(self, after, item):
        try:
            idx = self.items.index(after)
            self.items.insert(idx+1, item)
        except ValueError:
            self.items.append(item)
    
    def insertItemBefore(self, before, item):
        try:
            idx = self.items.index(before)
            self.items.insert(idx, item)
        except ValueError:
            self.items.insert(0, item)

            
            
    def allItems(self):
        """
        Recursively create a sequence for traversing all items in the
        collection. A generator would be nice but just prebuilding a list will
        be good enough.
        """
        items = [self]
        for item in self.items:
            items.extend(item.allItems())
            if hasattr(item, 'overloads'):
                for o in item.overloads:
                    items.extend(o.allItems())
        return items
                
    
    def findAll(self, name):
        """
        Search recursivly for items that have the given name.
        """
        matches = list()
        for item in self.allItems():
            if item.name == name or item.pyName == name:
                matches.append(item)
        return matches
    
                
    def _findItems(self):
        # If there are more items to be searched than what is in self.items, a
        # subclass can override this to give a different list.
        return self.items
    
        
    
#---------------------------------------------------------------------------

class VariableDef(BaseDef):
    """
    Represents a basic variable declaration.
    """
    def __init__(self, element=None, **kw):
        super(VariableDef, self).__init__()
        self.type = None
        self.definition = ''
        self.argsString = '' 
        self.__dict__.update(**kw)
        if element is not None:
            self.extract(element)
            
    def extract(self, element):
        super(VariableDef, self).extract(element)
        self.type = flattenNode(element.find('type'))
        self.definition = element.find('definition').text
        self.argsString = element.find('argsstring').text

    def dump(self, indent=0, stream=None):
        super(VariableDef, self).dump(indent, stream)
        txt = ("type:         %s\n"
               "definition:   %s\n"
               "argsString:   %s\n"
               ) % (self.type, self.definition, self.argsString)
        _print(txt, indent, stream)

        
#---------------------------------------------------------------------------
# These need the same attributes as VariableDef, but we use separate classes
# so we can identify what kind of element it came from originally.

class GlobalVarDef(VariableDef):
    pass

class TypedefDef(VariableDef):
    pass

#---------------------------------------------------------------------------

class MemberVarDef(VariableDef):
    """
    Represents a variable declaration in a class.
    """
    def __init__(self, element=None, **kw):
        super(MemberVarDef, self).__init__()
        self.isStatic = False
        self.protection = ''
        self.__dict__.update(kw)
        if element is not None:
            self.extract(element)
        
    def extract(self, element):
        super(MemberVarDef, self).extract(element)
        self.isStatic = element.get('static') == 'yes'
        self.protection = element.get('prot')
        assert self.protection in ['public', 'protected']
        # TODO: Should protected items be ignored by default or should we
        #       leave that up to the tweaker code or the generators?
        if self.protection == 'protected':
            self.ignore()

    def dump(self, indent=0, stream=None):
        super(MemberVarDef, self).dump(indent, stream)
        txt = ("isStatic:     %s\n"
               "protection:   %s\n"
               ) % (self.isStatic, self.protection)
        _print(txt, indent, stream)
            
#---------------------------------------------------------------------------

class FunctionDef(BaseDef):
    """
    Information about a standalone function.
    """
    def __init__(self, element=None, **kw):
        super(FunctionDef, self).__init__()
        self.type = None
        self.definition = ''
        self.argsString = ''
        self.pyArgsString = ''
        self.isOverloaded = False
        self.overloads = []
        self.deprecated = False       # is the function deprecated
        self.factory = False          # a factory function that creates a new instance of the return value
        self.pyReleaseGIL = False     # release the Python GIL for this function call
        self.noCopy = False           # don't make a copy of the return value, just wrap the original
        self.pyInt = False            # treat char types as integers
        self.transfer = False         # transfer ownership of return value to C++?
        self.transferBack = False     # transfer ownership of return value from C++ to Python?
        self.transferThis = False     # ownership of 'this' pointer transfered to C++ 
        self.__dict__.update(kw)
        if element is not None:
            self.extract(element)
            
    def releaseGIL(self, release=True):
        self.pyReleaseGIL = hold
                    
    def extract(self, element):
        super(FunctionDef, self).extract(element)
        self.type = flattenNode(element.find('type'))
        self.definition = element.find('definition').text
        self.argsString = element.find('argsstring').text
        for node in element.findall('param'):
            p = ParamDef(node)
            self.items.append(p)
            # TODO: Look at self.detailedDoc and pull out any matching
            # parameter description items and assign that value as the
            # briefDoc for this ParamDef object.

            
    def dump(self, indent=0, stream=None):
        super(FunctionDef, self).dump(indent, stream)
        txt = ("type:         %s\n"
               "definition:   %s\n"
               "argsString:   %s\n"
               "pyArgsString: %s\n"
               "isOverloaded: %s\n"
               "deprecated:   %s\n"
               "factory:      %s\n"
               "releaseGIL:   %s\n"
               "noCopy:       %s\n"
               "transfer:     %s\n"  
               "transferBack: %s\n"  
               "transferThis: %s\n"  
               ) % (self.type, self.definition, self.argsString, self.pyArgsString,
                    self.isOverloaded, self.deprecated, self.factory, self.pyReleaseGIL,
                    self.noCopy,
                    self.transfer, self.transferBack, self.transferThis)
        _print(txt, indent, stream)
        if self.items:
            for p in self.items:
                assert isinstance(p, ParamDef)
                _print("ParamDef:", indent, stream)
                p.dump(indent+4, stream)
                _print("\n", indent, stream)
        if self.overloads:
            _print("Overloaded functions:", indent, stream)
            for f in self.overloads:
                _print("MethodDef:", indent+4, stream)
                f.dump(indent+8, stream)
                _print("\n", indent, stream)

                
    def checkForOverload(self, methods):
        for m in methods:
            if isinstance(m, MethodDef) and m.name == self.name:
                m.overloads.append(self)
                m.isOverloaded = self.isOverloaded = True
                return True
        return False

    
    def all(self):
        return [self] + self.overloads
    
    
    def findOverload(self, matchText):
        """
        Search for an overloaded method that has matchText in its C++ argsString.
        """
        for o in self.all():
            if matchText in o.argsString:
                return o
        return None
    
        
    def _findItems(self):
        items = list(self.items)
        for o in self.overloads:
            items.extend(o.items)
        return items
               
#---------------------------------------------------------------------------
        
class MethodDef(FunctionDef):
    """
    Represents a class method, ctor or dtor declaration.
    """
    def __init__(self, element=None, className=None, **kw):
        super(MethodDef, self).__init__()
        self.isVirtual = False
        self.isStatic = False
        self.isCtor = False
        self.isDtor = False
        self.protection = ''
        self.defaultCtor = False      # use this ctor as the default one
        self.noDerivedCtor = False    # don't generate a ctor in the derived class for this ctor
        self.__dict__.update(kw)        
        if element is not None:
            self.extract(element, className)

    def extract(self, element, className):
        super(MethodDef, self).extract(element)
        self.isStatic = element.get('static') == 'yes'
        self.isVirtual = element.get('virt') in ['virtual', 'pure-virtual']
        self.isPureVirtual = element.get('virt') == 'pure-virtual'
        self.isCtor = self.name == className
        self.isDtor = self.name == '~' + className
        self.protection = element.get('prot')
        assert self.protection in ['public', 'protected']
        # TODO: Should protected items be ignored by default or should we
        #       leave that up to the tweaker code or the generators?
        if self.protection == 'protected':
            self.ignore()
        
    
    def dump(self, indent=0, stream=None):
        super(MethodDef, self).dump(indent, stream)
        txt = ("isCtor:       %s\n"
               "isDtor:       %s\n"
               "isStatic:     %s\n"
               "isVirtual:    %s\n"
               "protection:   %s\n"
               "defaultCtor:  %s\n"
               ) % (self.isCtor, self.isDtor, self.isStatic, self.isVirtual, 
                    self.protection, self.defaultCtor)
        _print(txt, indent, stream)
                

#---------------------------------------------------------------------------

class ParamDef(BaseDef):
    """
    A parameter of a function or method.
    """
    def __init__(self, element=None, **kw):
        super(ParamDef, self).__init__()
        self.type = ''                # data type
        self.default = ''             # default value
        self.out = False              # is it an output arg?
        self.inOut = False            # is it both input and output?
        self.pyInt = False            # treat char types as integers
        self.array = False            # the param is to be treated as an array
        self.arraySize = False        # the param is the size of the array
        self.transfer = False         # transfer ownership of arg to C++?
        self.transferBack = False     # transfer ownership of arg from C++ to Python?
        self.transferThis = False     # ownership of 'this' pointer transfered to this arg 
        self.__dict__.update(kw)
        if element is not None:
            self.extract(element)
        
    def extract(self, element):
        self.name = element.find('declname').text
        self.type = flattenNode(element.find('type'))
        if element.find('defval') is not None:
            self.default = flattenNode(element.find('defval'))
        
    def dump(self, indent=0, stream=None):
        #super(ParamDef, self).dump(indent, stream)
        txt = ("name:         %s\n"
               "type:         %s\n"
               "default:      %s\n"
               "out:          %s\n"  
               "inOut:        %s\n"  
               "array:        %s\n"
               "arraySize:    %s\n"
               "transfer:     %s\n"  
               "transferBack: %s\n"  
               "transferThis: %s\n"  
               ) % (self.name, self.type, self.default, self.out, self.inOut,
                    self.array, self.arraySize,
                    self.transfer, self.transferBack, self.transferThis)
        _print(txt, indent, stream)

#---------------------------------------------------------------------------

class ClassDef(BaseDef):
    """
    The information about a class that is needed to generate wrappers for it.
    """
    nameTag = 'compoundname'
    def __init__(self, element=None, kind='class', **kw):
        super(ClassDef, self).__init__()
        self.kind = kind
        self.bases = []             # base class names
        self.includes = []          # .h file for this class
        self.abstract = False       # is it an abstract base class?
        self.deprecated = False     # mark all methods as deprecated
        self.external = False       # class is in another module
        self.noDefCtor = False      # do not generate a default constructor
        self.singlton = False       # class is a singleton so don't call the dtor until the interpreter exits
        self.headerCode = []
        self.cppCode = []
        self.convertToPyObject = None
        self.convertFromPyObject = None
        self.allowNone = False      # Allow the convertFrom code to handle None too.
        
        # Stuff that needs to be generated after the class instead of within
        # it. Some back-end generators need to put stuff inside the class, and
        # others need to do it outside the class definition. The generators
        # can move things here for later processing when they encounter those
        # items.
        self.generateAfterClass = [] 
        
        self.__dict__.update(kw)
        if element is not None:
            self.extract(element)

            
    def extract(self, element):
        super(ClassDef, self).extract(element)

        for node in element.findall('basecompoundref'):
            self.bases.append(node.text)
        for node in element.findall('includes'):
            self.includes.append(node.text)
            
        # TODO: Is it possible for there to be memberdef's w/o a sectiondef?
        for node in element.findall('sectiondef/memberdef'):
            # skip any private items
            if node.get('prot') == 'private':
                continue
            kind = node.get('kind')
            if kind == 'function':
                m = MethodDef(node, self.name)
                if not m.checkForOverload(self.items):
                    self.items.append(m)
            elif kind == 'variable':
                v = MemberVarDef(node)
                self.items.append(v)
            elif kind == 'enum':
                e = EnumDef(node)
                self.items.append(e)
            else:
                raise ExtractorError('Unknown memberdef kind: %s' % kind)
            
            # TODO: do we need support for nested classes?
                
            
    def dump(self, indent=0, stream=None):
        super(ClassDef, self).dump(indent, stream)
        txt = ("bases:        %s\n"
               "includes:     %s\n"
               "abstract:     %s\n"
               "deprecated:   %s\n"
               "external:     %s\n"
               "noDefCtor:    %s\n"
               "singleton:    %s\n"
               ) % (_pf(self.bases, indent), _pf(self.includes, indent),
                    self.abstract, self.deprecated, self.external, self.noDefCtor, self.singlton)
        _print(txt, indent, stream)
        for item in self.items:
            _print("%s:" % item.__class__.__name__, indent, stream)
            item.dump(indent+4, stream)
            _print("\n", indent, stream)

            
    def addHeaderCode(self, code):
        if isinstance(code, list):
            self.headerCode.extend(code)
        else:
            self.headerCode.append(code)
        
    def addCppCode(self, code):
        if isinstance(code, list):
            self.cppCode.extend(code)
        else:
            self.cppCode.append(code)

            
    def insertCppCode(self, filename):
        self.addCppCode(file(filename).read())
        
        
    def addProperty(self, *args, **kw):
        """
        Add a property to a class, with a name, getter function and optionally
        a setter method.
        """
        # As a convenience allow the name, getter and (optionally) the setter
        # to be passed as a single string. Otherwise the args will be passed
        # as-is to PropertyDef
        if len(args) == 1:
            name = getter = setter = ''
            split = args[0].split()
            assert len(split) in [2 ,3]
            if len(split) == 2:
                name, getter = split
            else:
                name, getter, setter = split
            p = PropertyDef(name, getter, setter, **kw)
        else:
            p = PropertyDef(*args, **kw)
        self.items.append(p)
        return p
    
        
    def addCppMethod(self, type, name, argsString, body, doc=None, **kw):
        """
        Add a new C++ method to a class. This method doesn't have to actually
        exist in the real C++ class. Instead it will be grafted on by the
        back-end wrapper generator such that it is visible in the class in the
        target language.
        """
        md = CppMethodDef(type, name, argsString, body, doc, **kw)
        self.items.append(md)
        return md

    
    def addCppCtor(self, argsString, body, doc=None, noDerivedCtor=True, **kw):
        """
        Add a C++ method that is a constructor.
        """
        md = CppMethodDef('', self.name, argsString, body, doc=doc, 
                          isCtor=True, noDerivedCtor=noDerivedCtor, **kw)
        self.items.append(md)
        return md
        
    
    def addPyMethod(self, name, argsString, body, doc=None, **kw):
        """
        Add a (monkey-patched) Python method to this class.
        """
        pm = PyMethodDef(self, name, argsString, body, doc, **kw)
        self.items.append(pm)
        return pm

    
    def addPyCode(self, code):
        """
        Add a snippet of Python code which is to be associated with this class.
        """        
        pc = PyCodeDef(code, klass=self, protection = 'public')
        self.items.append(pc)
        return pc

    
    def addPublic(self, code=''):
        """
        Adds a 'public:' protection keyword to the class, optionally followed
        by some additional code.
        """
        text = 'public:'
        if code:
            text = text + '\n' + code
        self.addItem(WigCode(text))
         
    def addProtected(self, code=''):
        """
        Adds a 'protected:' protection keyword to the class, optionally followed
        by some additional code.
        """
        text = 'protected:'
        if code:
            text = text + '\n' + code
        self.addItem(WigCode(text))

        
    def addPrivate(self, code=''):
        """
        Adds a 'private:' protection keyword to the class, optionally followed
        by some additional code.
        """
        text = 'private:'
        if code:
            text = text + '\n' + code
        self.addItem(WigCode(text))

        
    def addCopyCtor(self, prot='protected'):
        # add declaration of a copy constructor to this class
        wig = WigCode("""\
{PROT}:
    {CLASS}(const {CLASS}&);""".format(CLASS=self.name, PROT=prot))
        self.addItem(wig)

    def addPrivateCopyCtor(self):
        self.addCopyCtor('private')
        
    def addPrivateAssignOp(self):
        # add declaration of an assignment opperator to this class
        wig = WigCode("""\
private:
    {CLASS}& operator=(const {CLASS}&);""".format(CLASS=self.name))
        self.addItem(wig)

    def addDtor(self, prot='protected'):
        # add declaration of a destructor to this class
        wig = WigCode("""\
{PROT}:
    ~{CLASS}();""".format(CLASS=self.name, PROT=prot))
        self.addItem(wig)

#---------------------------------------------------------------------------

class EnumDef(BaseDef):
    """
    A named or anonymous enumeration.
    """
    def __init__(self, element=None, inClass=False, **kw):
        super(EnumDef, self).__init__()
        prot = element.get('prot')
        if prot is not None:
            self.protection = prot
            assert self.protection in ['public', 'protected']
            # TODO: Should protected items be ignored by default or should we
            #       leave that up to the tweaker code or the generators?
            if self.protection == 'protected':
                self.ignore()
        self.__dict__.update(kw)
        if element is not None:
            self.extract(element)
        
    def extract(self, element):
        super(EnumDef, self).extract(element)
        for node in element.findall('enumvalue'):
            value = EnumValueDef(node)
            self.items.append(value)
            
    def dump(self, indent=0, stream=None):
        super(EnumDef, self).dump(indent, stream)
        for v in self.items:
            _print("EnumValueDef:", indent, stream)
            v.dump(indent+4, stream)
            _print("\n", indent, stream)
            


class EnumValueDef(BaseDef):
    """
    An item in an enumeration.
    """
    def __init__(self, element=None, **kw):
        super(EnumValueDef, self).__init__()
        if element is not None:
            self.extract(element)
        self.__dict__.update(kw)

            
#---------------------------------------------------------------------------

class PropertyDef(BaseDef):
    """
    Use the C++ methods of a class to make a Python property.

    NOTE: This one is not automatically extracted, but can be added to
          classes in the tweaker stage
    """
    def __init__(self, name, getter, setter=None, doc=None, **kw):
        super(PropertyDef, self).__init__()
        self.name = name
        self.getter = getter
        self.setter = setter
        self.briefDoc = doc
        self.protection = 'public'
        self.__dict__.update(kw)
        
    def dump(self, indent=0, stream=None):
        # debug helper, prints the extracted items
        txt = ("name:         %s\n"
               "getter:       %s\n"
               "setter:       %s\n"
               "briefDoc:     %s\n") % \
            (self.name, self.getter, self.setter, self.briefDoc) 
        _print(txt, indent, stream)

        
#---------------------------------------------------------------------------

class CppMethodDef(MethodDef):
    """
    This class provides information that can be used to add the code for a new
    method to a wrapper class that does not actually exist in the real C++
    class, or it can be used to provide an alternate implementation for a
    method that does exist. The backend generator support for this feature
    would be things like %extend in SWIG or %MethodCode in SIP.

    NOTE: This one is not automatically extracted, but can be added to
          classes in the tweaker stage
    """
    def __init__(self, type, name, argsString, body, doc=None, **kw):
        super(CppMethodDef, self).__init__()
        self.type = type
        self.name = name
        self.argsString = argsString
        self.body = body
        self.briefDoc = doc
        self.protection = 'public'
        self.__dict__.update(kw)

        
    def dump(self, indent=0, stream=None):
        # debug helper, prints the extracted items
        txt = ("type:         %s\n"
               "name:         %s\n"
               "argsString:   %s\n"
               "briefDoc:     %s\n"
               "body:         %s\n") % \
            (self.type, self.name, self.argsString, self.briefDoc, self.body) 
        _print(txt, indent, stream)
    
        
#---------------------------------------------------------------------------

class WigCode(BaseDef):
    """
    This class allows code defined by the triggers to be injected into the
    generated Wrapper Interface Generator file. 
    """
    def __init__(self, code, **kw):
        super(WigCode, self).__init__()
        self.code = code
        self.protection = 'public'
        self.__dict__.update(kw)

#---------------------------------------------------------------------------

class PyCodeDef(BaseDef):
    """
    This code held by this class will be written to a Python module
    that wraps the import of the extension module.
    """
    def __init__(self, code, order=None, **kw):
        super(PyCodeDef, self).__init__()
        self.code = code
        self.order = order
        self.__dict__.update(kw)

#---------------------------------------------------------------------------

class PyMethodDef(BaseDef):
    """
    A PyMethodDef can be used to define Python functions that will then be
    monkey-patched in to the extension module Types as if they belonged there.
    """
    def __init__(self, klass, name, argsString, body, doc=None, **kw):
        super(PyMethodDef, self).__init__()
        self.klass = klass
        self.name = name
        self.argsString = argsString
        self.body = body
        self.briefDoc = doc
        self.protection = 'public'
        self.__dict__.update(kw)
    
#---------------------------------------------------------------------------

class ModuleDef(BaseDef):
    """
    This class holds all the items that will be in the generated module
    """
    def __init__(self, package, module, name, docstring=''):
        super(ModuleDef, self).__init__()
        self.package = package
        self.module = module
        self.name = name
        self.docstring = docstring
        self.headerCode = []
        self.cppCode = []
        self.initializerCode = []
        self.preInitializerCode = []
        self.postInitializerCode = []
        self.includes = []
        self.imports = []

    def addHeaderCode(self, code):
        if isinstance(code, list):
            self.headerCode.extend(code)
        else:
            self.headerCode.append(code)
        
    def addCppCode(self, code):
        if isinstance(code, list):
            self.cppCode.extend(code)
        else:
            self.cppCode.append(code)
        
    def addInitializerCode(self, code):
        if isinstance(code, list):
            self.initializerCode.extend(code)
        else:
            self.initializerCode.append(code)
        
    def addPreInitializerCode(self, code):
        if isinstance(code, list):
            self.preInitializerCode.extend(code)
        else:
            self.preInitializerCode.append(code)
        
    def addPostInitializerCode(self, code):
        if isinstance(code, list):
            self.postInitializerCode.extend(code)
        else:
            self.postInitializerCode.append(code)
        
    def addInclude(self, name):
        if isinstance(name, list):
            self.includes.extend(name)
        else:
            self.includes.append(name)
        
    def addImport(self, name):
        if isinstance(name, list):
            self.imports.extend(name)
        else:
            self.imports.append(name)
        
            
    def addElement(self, element):
        item = None
        kind = element.get('kind')
        if kind == 'class':
            extractingMsg(kind, element, ClassDef.nameTag)
            item = ClassDef(element)
            self.items.append(item)

        elif kind == 'struct':
            extractingMsg(kind, element, ClassDef.nameTag)
            item = ClassDef(element, kind='struct')
            self.items.append(item)

        elif kind == 'function':
            extractingMsg(kind, element)
            item = FunctionDef(element)
            if not item.checkForOverload(self.items):
                self.items.append(item)
            
        elif kind == 'enum':
            extractingMsg(kind, element)
            item = EnumDef(element)
            self.items.append(item)
            
        elif kind == 'variable':
            extractingMsg(kind, element)
            item = GlobalVarDef(element)
            self.items.append(item)

        elif kind == 'typedef': 
            extractingMsg(kind, element)
            item = TypedefDef(element)
            self.items.append(item)
            
        elif kind == 'define':
            skippingMsg(kind, element)

        elif kind == 'file':
            for node in element.findall('sectiondef/memberdef'):
                self.addElement(node)

        else:
            raise ExtractorError('Unknown module item kind: %s' % kind)
        
        return item
    
        
    def dump(self, indent=0, stream=None):
        super(ModuleDef, self).dump(indent, stream)
        txt = ("includes:        %s\n"
               "imports:         %s\n"
               "headerCode:      %s\n"
               "cppCode:         %s\n"
               "initializerCode: %s\n"
               ) % (_pf(self.includes, indent), 
                    _pf(self.imports, indent), 
                    _pf(self.headerCode, indent), 
                    _pf(self.cppCode, indent), 
                    _pf(self.initializerCode, indent))
        _print(txt, indent, stream)
        _print('\n', indent, stream)

        for item in self.items:
            _print(item.__class__.__name__+":", indent, stream)
            item.dump(indent+4, stream)
            _print('\n', indent, stream)
         
            
    def addCppFunction(self, type, name, argsString, body, doc=None, **kw):
        """
        Add a new C++ function into the module that is written by hand, not
        wrapped.
        """
        md = CppMethodDef(type, name, argsString, body, doc, **kw)
        self.items.append(md)
        return md


    def addPyCode(self, code, order=None):
        """
        Add a snippet of Python code to the wrapper module.
        """        
        pc = PyCodeDef(code, order)
        self.items.append(pc)
        return pc
    
    
    def includePyCode(self, filename, order=None):
        """
        Add a snippet of Python code from a file to the wrapper module.
        """
        text = file(filename).read()
        return self.addPyCode(
            "#" + '-=' * 38 + '\n' +
            ("# This code block was included from %s\n%s\n" % (filename, text)) + 
            "# End of included code block\n"
            "#" + '-=' * 38 + '\n'            ,
            order
            )
    
    
#---------------------------------------------------------------------------
# Some helper functions and such
#---------------------------------------------------------------------------

def flattenNode(node):
    """
    Extract just the text from a node and its children, tossing out any child
    node tags and attributes.
    """
    text = node.text or ""
    for n in node:
        text += flattenNode(n)
    if node.tail: 
        text += node.tail.rstrip()
    return text.rstrip()          


class ExtractorError(RuntimeError):
    pass


def _print(value, indent, stream):
    if stream is None:
        stream = sys.stdout
    indent = ' ' * indent
    for line in str(value).splitlines():
        stream.write("%s%s\n" % (indent, line))

def _pf(item, indent):
    if indent == 0:
        indent = 4
    txt =  pprint.pformat(item, indent)
    if '\n' in txt:
        txt = '\n' + txt
    return txt
        

def verbose():
    return '--verbose' in sys.argv

def extractingMsg(kind, element, nameTag='name'):
    if verbose():
        print 'Extracting %s: %s' % (kind, element.find(nameTag).text)
                                     
def skippingMsg(kind, element):
    if verbose():
        print 'Skipping %s: %s' % (kind, element.find('name').text)
        
    
#---------------------------------------------------------------------------

