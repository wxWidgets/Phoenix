# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------
# Name:        sphinxtools/utilities.py
# Author:      Andrea Gavana
#
# Created:     30-Nov-2010
# Copyright:   (c) 2013 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

# Standard library imports
import sys
import os
import codecs
import shutil
import glob
import imp
import re

if sys.version_info < (3,):
    import cPickle as pickle
    from UserDict import UserDict
    string_base = basestring
else:
    import pickle
    from collections import UserDict
    string_base = str

# Phoenix-specific imports
from buildtools.config import phoenixDir

from .templates import TEMPLATE_CONTRIB

from .constants import IGNORE, PUNCTUATION, MODULENAME_REPLACE
from .constants import CPP_ITEMS, VERSION, VALUE_MAP, NO_MODULE
from .constants import RE_KEEP_SPACES, EXTERN_INHERITANCE
from .constants import DOXYROOT, SPHINXROOT, WIDGETS_IMAGES_ROOT


# ----------------------------------------------------------------------- #
class odict(UserDict):
    """
    An ordered dict (odict). This is a dict which maintains an order to its items;
    the order is rather like that of a list, in that new items are, by default,
    added to the end, but items can be rearranged.

    .. note:: Note that updating an item (setting a value where the key is already
       in the dict) is not considered to create a new item, and does not affect the
       position of that key in the order. However, if an item is deleted, then a
       new item with the same key is added, this is considered a new item.
        
    """
    
    def __init__(self, dict = None):
        self._keys = []
        UserDict.__init__(self, dict)

    def __delitem__(self, key):
        UserDict.__delitem__(self, key)
        self._keys.remove(key)

    def __setitem__(self, key, item):
        UserDict.__setitem__(self, key, item)
        if key not in self._keys: self._keys.append(key)

    def clear(self):
        UserDict.clear(self)
        self._keys = []

    def copy(self):
        dict = UserDict.copy(self)
        dict._keys = self._keys[:]
        return dict

    def items(self):
        return list(zip(self._keys, list(self.values())))

    def keys(self):
        return self._keys

    def popitem(self):
        try:
            key = self._keys[-1]
        except IndexError:
            raise KeyError('dictionary is empty')

        val = self[key]
        del self[key]

        return (key, val)

    def setdefault(self, key, failobj = None):
        UserDict.setdefault(self, key, failobj)
        if key not in self._keys: self._keys.append(key)

    def update(self, dict):
        UserDict.update(self, dict)
        for key in list(dict.keys()):
            if key not in self._keys: self._keys.append(key)

    def values(self):
        return list(map(self.get, self._keys))


# ----------------------------------------------------------------------- #

def RemoveWxPrefix(name):
    """
    Removes the `wx` prefix from a string.

    :param string `name`: a string, possibly starting with "wx" or "``wx".

    :rtype: `string`

    .. note:: This function is similar to the one already present in `tweaker_tools`
       but I had to extend it a bit to suite the ReSTification of the XML docs.

    """       

    if name.startswith('wx') and not name.startswith('wxEVT_') and not name.startswith('wx.'):
        name = name[2:]

    if name.startswith('``wx') and not name.startswith('``wxEVT_') and not name.startswith('``wx.'):
        name = name[0:2] + name[4:]
        
    return name


# ----------------------------------------------------------------------- #

def IsNumeric(input_string):
    """
    Checks if the string `input_string` actually represents a number.

    :param string `input_string`: any string.

    :rtype: `bool`

    :returns: ``True`` if the `input_string` can be converted to a number (any number),
     ``False`` otherwise.
    """

    try:
        float(input_string)
        return True
    except ValueError:
        return False


# ----------------------------------------------------------------------- #

def CountSpaces(text):
    """
    Counts the number of spaces before and after a string.

    :param string `text`: any string.

    :rtype: `tuple`

    :returns: a tuple representing the number of spaces before and after the text.
    """

    space_before = ' '*(len(text) - len(text.lstrip(' ')))
    space_after = ' '*(len(text) - len(text.rstrip(' ')))

    return space_before, space_after


# ----------------------------------------------------------------------- #

def Underscore2Capitals(string):
    """
    Replaces the underscore letter in a string with the following letter capitalized.

    :param string `string`: the string to be analyzed.

    :rtype: `string`    
    """

    items = string.split('_')[1:]
    newstr = ''

    for item in items:
        newstr += item.capitalize()
        
    return newstr


# ----------------------------------------------------------------------- #

def ReplaceCppItems(line):
    """
    Replaces various C++ specific stuff with more Pythonized version of them.

    :param string `line`: any string.

    :rtype: `string`
    """

    items = RE_KEEP_SPACES.split(line)
    newstr = []

    for n, item in enumerate(items):

        if item in CPP_ITEMS:
            continue

        if 'wxString' in item:
            item = 'string'
        elif item == 'char':
            item = 'int'
        elif item == 'double':
            if len(items) > n+2 and not items[n+2].lower().startswith("click"):
                item = 'float'

        if len(item.replace('``', '')) > 2:
            if '*' in item:
                try:
                    eval(item)
                    item = item.replace('*', 'x')
                except:
                    # Avoid replacing standalone '&&' and similar
                    for cpp in CPP_ITEMS[0:2]:
                        item = item.replace(cpp, '')
            
        newstr.append(item)

    newstr = ''.join(newstr)
    newstr = newstr.replace(' *)', ' )')
    return newstr


# ----------------------------------------------------------------------- #

def PythonizeType(ptype, is_param):
    """
    Replaces various C++ specific stuff with more Pythonized version of them,
    for parameter lists and return types (i.e., the `:param:` and `:rtype:`
    ReST roles).

    :param string `ptype`: any string;
    :param bool `is_param`: ``True`` if this is a parameter description, ``False``
     if it is a return type.

    :rtype: `string`
    """

    if 'size_t' in ptype:
        ptype = 'int'
    elif 'wx.' in ptype:
        ptype = ptype[3:]
    else:
        ptype = Wx2Sphinx(ReplaceCppItems(ptype))[1]
        
    ptype = ptype.replace('::', '.').replace('*&', '')
    ptype = ptype.replace('int const', 'int')
    ptype = ptype.replace('Uint32', 'int').replace('**', '').replace('Int32', 'int')
    ptype = ptype.replace('FILE', 'file')
    ptype = ptype.replace('boolean', 'bool')

    for item in ['unsignedchar', 'unsignedint', 'unsignedlong', 'unsigned']:
        ptype = ptype.replace(item, 'int')
    
    ptype = ptype.strip()        
    ptype = RemoveWxPrefix(ptype)

    if '. wx' in ptype:
        ptype = ptype.replace('. wx', '.')

    plower = ptype.lower()
    
    if plower == 'double':
        ptype = 'float'

    if plower in ['string', 'char', 'artid', 'artclient']:
        ptype = 'string'

    if plower in ['coord', 'byte', 'fileoffset', 'short', 'time_t', 'intptr', 'uintptr', 'windowid']:
        ptype = 'int'
        
    if plower in ['longlong']:
        ptype = 'long'
                  
    cpp =    ['ArrayString', 'ArrayInt', 'ArrayDouble']
    python = ['list of strings', 'list of integers', 'list of floats']
    
    for c, p in zip(cpp, python):
        ptype = ptype.replace(c, p)

    if 'Image.' in ptype:
        ptype = ptype.split('.')[-1]

    if 'FileName' in ptype:
        ptype = 'string'
        
    if ptype.endswith('&'):
        ptype = ptype[0:-1]
        if ' ' not in ptype:
            ptype = ':class:`%s`'%ptype

    else:
        if is_param and '.' in ptype:
            modules = MODULENAME_REPLACE.values()
            modules.sort()
            modules = modules[1:]
            if ptype.split('.')[0] + '.' in modules:
                ptype = ':ref:`%s`'%ptype

    return ptype


# ----------------------------------------------------------------------- #

def ConvertToPython(text):
    """
    Converts the input `text` into a more ReSTified version of it.

    This involves the following steps:

    1. Any C++ specific declaration (like ``unsigned``, ``size_t`` and so on
       is removed.
    2. Lines starting with "Include file" or "#include" are ignored.
    3. Uppercase constants (i.e., like ID_ANY, HORIZONTAL and so on) are converted
       into inline literals (i.e., ``ID_ANY``, ``HORIZONTAL``).
    4. The "wx" prefix is removed from all the words in the input `text`.
    
    :param string `text`: any string.

    :rtype: `string`
    """

    newlines = []
    unwanted = ['Include file', '#include']
    
    for line in text.splitlines():

        newline = []

        for remove in unwanted:
            if remove in line:
                line = line[0:line.index(remove)]
                break

        spacer = ' '*(len(line) - len(line.lstrip()))

        line = ReplaceCppItems(line)
        
        for word in RE_KEEP_SPACES.split(line):

            if word == VERSION:
                newline.append(word)
                continue
            
            newword = word
            for s in PUNCTUATION:
                newword = newword.replace(s, "")
            
            if newword in VALUE_MAP:
                word = word.replace(newword, VALUE_MAP[newword])
                newline.append(word)
                continue
                
            if newword not in IGNORE and not newword.startswith('wx.'):
                word = RemoveWxPrefix(word)
                newword = RemoveWxPrefix(newword)

            if "::" in word and not word.endswith("::"):
                # Bloody SetCursorEvent...
                word = word.replace("::wx", ".")
                word = word.replace("::", ".")
                word = "`%s`"%word
                newline.append(word)
                continue
                
            if newword.upper() == newword and newword not in PUNCTUATION and \
               newword not in IGNORE and len(newword.strip()) > 1 and \
               not IsNumeric(newword) and newword not in ['DC', 'GCDC']:

                if '``' not in newword and '()' not in word and '**' not in word:
                    word = word.replace(newword, "``%s``"%newword)

            word = word.replace('->', '.')
            newline.append(word)

        newline = spacer + ''.join(newline)
        newline = newline.replace(':see:', '.. seealso::')
        newline = newline.replace(':note:', '.. note::')
        newlines.append(newline)

    formatted = "\n".join(newlines)
    formatted = formatted.replace('\\', '\\\\')

    return formatted
            

# ----------------------------------------------------------------------- #

def FindDescendants(element, tag, descendants=None):
    """
    Finds and returns all descendants of a specific `xml.etree.ElementTree.Element`
    whose tag matches the input `tag`.

    :param xml.etree.ElementTree.Element `element`: the XML element we want to examine.
    :param string `tag`: the target tag we are looking for.
    :param list `descendants`: a list of already-found descendants or ``None`` if this
     is the first call to the function.

    :rtype: `list`
    
    .. note:: This is a recursive function, and it is only used in the `etgtools.extractors.py`
       script.

    """
    
    if descendants is None:
        descendants = []
        
    for childElement in element:
        if childElement.tag == tag:
            descendants.append(childElement)

        descendants = FindDescendants(childElement, tag, descendants)

    return descendants
    

# ----------------------------------------------------------------------- #

def FindControlImages(elementOrString):
    """
    Given the input `element` (an instance of `xml.etree.ElementTree.Element`
    or a plain string)
    representing a Phoenix class description, this function will scan the
    doxygen image folder ``DOXYROOT`` to look for a widget screenshot.

    If this class indeed represents a widget and a screenshot is found, it is
    then copied to the appropriate Sphinx input folder ``WIDGETS_IMAGES_ROOT``
    in one of its sub-folders (``wxmsw``, ``wxgtk``, ``wxmac``) depending on
    which platform the screenshot was taken.

    :param `elementOrString`: the XML element we want to examine (an instance of
     xml.etree.ElementTree.Element) or a plain string (usually for wx.lib).

    :rtype: `list`

    :returns: A list of image paths, every element of it representing a screenshot on
     a different platform. An empty list if returned if no screenshots have been found.
     
    .. note:: If a screenshot doesn't exist for one (or more) platform but it
       exists for others, the missing images will be replaced by the "no_appearance.png"
       file (you can find it inside the ``WIDGETS_IMAGES_ROOT`` folder.

    """       

    if isinstance(elementOrString, string_base):
        class_name = py_class_name = elementOrString.lower()
    else:
        element = elementOrString
        class_name = RemoveWxPrefix(element.name) or element.pyName
        py_class_name = Wx2Sphinx(class_name)[1]

        class_name = class_name.lower()
        py_class_name = py_class_name.lower()

    image_folder = os.path.join(DOXYROOT, 'images')

    appearance = odict()

    for sub_folder in ['wxmsw', 'wxmac', 'wxgtk']:

        png_file = class_name + '.png'
        appearance[sub_folder] = ''
        
        possible_image = os.path.join(image_folder, sub_folder, png_file)
        new_path = os.path.join(WIDGETS_IMAGES_ROOT, sub_folder)

        py_png_file = py_class_name + '.png'        
        new_file = os.path.join(new_path, py_png_file)

        if os.path.isfile(new_file):

            appearance[sub_folder] = py_png_file
        
        elif os.path.isfile(possible_image):

            if not os.path.isdir(new_path):
                os.makedirs(new_path)
                            
            if not os.path.isfile(new_file):
                shutil.copyfile(possible_image, new_file)

            appearance[sub_folder] = py_png_file
            
    if not any(list(appearance.values())):
        return []
    
    for sub_folder, image in list(appearance.items()):
        if not image:
            appearance[sub_folder] = '../no_appearance.png'

    return list(appearance.values())


# ----------------------------------------------------------------------- #

def MakeSummary(class_name, item_list, template, kind, add_tilde=True):
    """
    This function generates a table containing a method/property name
    and a shortened version of its docstrings.

    :param string `class_name`: the class name containing the method/property lists;
    :param list `item_list`: a list of tuples like `(method/property name, short docstrings)`;
    :param string `template`: the template to use (from `sphinxtools/templates.py`, can
     be the ``TEMPLATE_METHOD_SUMMARY`` or the ``TEMPLATE_PROPERTY_SUMMARY``;
    :param string `kind`: can be ``:meth:`` or ``:attr:`` or ``:ref:`` or ``:mod:``;
    :param bool `add_tilde`: ``True`` to add the ``~`` character in front of the first
     summary table column, ``False`` otherwise.

    :rtype: `string`
    """

    maxlen = 0
    for method, simple_docs in item_list:
        substr = ':%s:`~%s`'%(kind, method)
        maxlen = max(maxlen, len(substr))

    maxlen = max(80, maxlen)        
    
    summary = '='*maxlen + ' ' + '='*80 + "\n"
    format = '%-' + str(maxlen) + 's %s'

    for method, simple_docs in item_list:
        if add_tilde:
            substr = ':%s:`~%s`'%(kind, method)
        else:
            substr = ':%s:`%s`'%(kind, method)

        new_docs = simple_docs

        if kind == 'meth':
            regex = re.findall(r':meth:\S+', simple_docs)
            for regs in regex:
                if '.' in regs:
                    continue

                meth_name = regs[regs.index('`')+1:regs.rindex('`')]
                newstr = ':meth:`~%s.%s`'%(class_name, meth_name)
                new_docs = new_docs.replace(regs, newstr, 1)

        if '===' in new_docs:
            new_docs = ''
            
        elif new_docs.rstrip().endswith(':'):
            # Avoid Sphinx warnings
            new_docs = new_docs.rstrip(':')
                            
        summary += format%(substr, new_docs) + '\n'

    summary += '='*maxlen + ' ' + '='*80 + "\n"

    return template % summary
    

# ----------------------------------------------------------------------- #

def WriteSphinxOutput(stream, filename, append=False):
    """
    Writes the text contained in the `stream` to the `filename` output file.

    :param StringIO.StringIO `stream`: the stream where the text lives.
    :param string `filename`: the output file we want to write the text in;
    :param bool `append`: ``True`` to append to the file, ``False`` to simply
     write to it.
    """

    text_file = os.path.join(SPHINXROOT, filename)
    text = stream.getvalue()

    mode = 'a' if append else 'w'
    fid = codecs.open(text_file, mode, encoding='utf-8')        
    if mode == 'w':
        fid.write('.. include:: headings.inc\n\n')

    fid.write(text)
    fid.close()


# ----------------------------------------------------------------------- #

def ChopDescription(text):
    """
    Given the (possibly multiline) input text, this function will get the
    first non-blank line up to the next newline character.

    :param string `text`: any string.

    :rtype: `string`
    """

    description = ''
    
    for line in text.splitlines():
        line = line.strip()
        
        if not line or line.startswith('..') or line.startswith('|'):
            continue

        description = line
        break
    
    return description


# ----------------------------------------------------------------------- #

def PickleItem(description, current_module, name, kind):
    """
    This function pickles/unpickles a dictionary containing class names as keys
    and class brief description (chopped docstrings) as values to build the
    main class index for Sphinx **or** the Phoenix standalone function names
    as keys and their full description as values to build the function page.

    This step is necessary as the function names/description do not come out
    in alphabetical order from the ``etg`` process.

    :param string `description`: the function/class description.
    :param string `current_module`: the harmonized module name for this class
     or function (see ``MODULENAME_REPLACE`` in `sphinxtools/constants.py`).
    :param string `name`: the function/class name.
    :param string `kind`: can be `function` or `class`.
    """
    
    if kind == 'function':
        pickle_file = os.path.join(SPHINXROOT, current_module + 'functions.pkl')
    else:
        pickle_file = os.path.join(SPHINXROOT, current_module + '1classindex.pkl')
        
    if os.path.isfile(pickle_file):
        fid = open(pickle_file, 'rb')
        items = pickle.load(fid)
        fid.close()
    else:
        items = {}

    items[name] = description
    fid = open(pickle_file, 'wb')
    pickle.dump(items, fid)
    fid.close()


# ----------------------------------------------------------------------- #

def PickleClassInfo(class_name, element, short_description):
    """
    Saves some information about a class in a pickle-compatible file., i.e. the
    list of methods in that class and its super-classes.

    :param string `class_name`: the name of the class we want to pickle;
    :param xml.etree.ElementTree.Element `element`: the XML element we want to examine;
    :param string `short_description`: the class short description (if any).
    """

    pickle_file = os.path.join(SPHINXROOT, 'class_summary.lst')
        
    if os.path.isfile(pickle_file):
        fid = open(pickle_file, 'rb')
        items = pickle.load(fid)
        fid.close()
    else:
        items = {}

    method_list, bases = [], []
    for method, description in element.method_list:
        method_list.append(method)

    for base in element.bases:
        bases.append(Wx2Sphinx(base)[1])

    items[class_name] = (method_list, bases, short_description)
    fid = open(pickle_file, 'wb')
    pickle.dump(items, fid)
    fid.close()


# ----------------------------------------------------------------------- #

global ALL_ITEMS
ALL_ITEMS = {}

def Class2Module():

    global ALL_ITEMS
    
    if ALL_ITEMS:
        return ALL_ITEMS

    etg_files = glob.glob(os.path.join(phoenixDir(), 'etg') + '/*.py')
    etg_files = [files for files in etg_files if not files.startswith('_')]

    for files in etg_files:
        split = os.path.split(os.path.splitext(files)[0])[1]
        module = imp.load_source(split, files)

        current_module = MODULENAME_REPLACE.get(module.MODULE, '')

        for item in module.ITEMS:
            
            item = RemoveWxPrefix(item)
            ALL_ITEMS[item] = current_module

    ALL_ITEMS.update(NO_MODULE)

    return ALL_ITEMS            
    
    
def Wx2Sphinx(name):
    """
    Converts a wxWidgets specific string into a Phoenix-ReST-ready string.

    :param string `name`: any string.
    """

    if '<' in name:
        name = name[0:name.index('<')]

    name = name.strip()    
    newname = fullname = RemoveWxPrefix(name)

    if '.' in newname and len(newname) > 3:
        lookup, remainder = newname.split('.')
        remainder = '.%s'%remainder
    else:
        lookup = newname
        remainder = ''

    all_items = Class2Module()
    if lookup in all_items:
        fullname = all_items[lookup] + lookup + remainder
        
    return newname, fullname


# ----------------------------------------------------------------------- #

RAW_1 = """

%s.. raw:: html

%s    <div class="codeexpander">

"""

RAW_2 = """

%s.. raw:: html

%s    </div>

"""

def FormatContributedSnippets(kind, contrib_snippets):
    """
    This method will include and properly ReST-ify contributed snippets
    of wxPython code (at the moment only 2 snippets are available), by
    including the Python code into the ReST files and allowing the user to
    show/hide the snippets using a JavaScript "Accordion" script thanks to
    the ``.. raw::`` directive (default for snippets is to be hidden).

    :param string `kind`: can be "method", "function" or "class" depending on the
     current item being scanned by the `sphinxgenerator.py` tool;
    :param list `contrib_snippets`: a list of file names (with the ``*.py`` extension)
     containing the contributed snippets of code. Normally these snippets live
     in the ``SPHINXROOT/rest_substitutions/snippets/python/contrib`` folder.
    """

    spacer = ''
    if kind == 'function':
        spacer = 3*' '
    elif kind == 'method':
        spacer = 6*' '

    if kind == 'class':
        text = TEMPLATE_CONTRIB
    else:
        text = '\n' + spacer + '|contributed| **Contributed Examples:**\n\n'
    
    for indx, snippet in enumerate(contrib_snippets):
        fid = open(snippet, 'rt')
        lines = fid.readlines()
        fid.close()
        user = lines[0].replace('##', '').strip()
        onlyfile = os.path.split(snippet)[1]

        download = os.path.join(SPHINXROOT, '_downloads', onlyfile)
        if not os.path.isfile(download):
            shutil.copyfile(snippet, download)

        text += RAW_1%(spacer, spacer)
        text += '\n' + spacer + 'Example %d - %s (:download:`download <_downloads/%s>`):\n\n'%(indx+1, user, onlyfile)

        text += spacer + '.. literalinclude:: _downloads/%s\n'%onlyfile
        text += spacer + '   :lines: 2-\n\n'

        text += RAW_2%(spacer, spacer)

        text += '\n\n%s|\n\n'%spacer
        
    return text


def FormatExternalLink(fullname, inheritance=False):
    """
    Analyzes the input `fullname` string to check whether a class description
    is actually coming from an external documentation tool
    (like http://docs.python.org/library/ or http://docs.scipy.org/doc/numpy/reference/generated/).

    If the method finds such an external link, the associated inheritance
    diagram (if `inheritance` is ``True``) or the ``:ref:`` directive are
    modified accordingly to link it to the correct external documentation.

    :param string `fullname`: the fully qualified name for a class, method or function,
     i.e. `exceptions.Exception` or `threading.Thread`;
    :param bool `inheritance`: ``True`` if the call is coming from :mod:`inheritance`,
     ``False`` otherwise.
    """    

    if fullname.count('.') == 0:
        if not inheritance:
            return ':class:`%s`'%fullname
        return ''

    parts = fullname.split('.')
    possible_external = parts[-2] + '.'
    real_name = '.'.join(parts[-2:])
    
    if possible_external.startswith('_'):
        # funny ctypes...
        possible_external = possible_external[1:]
        real_name = real_name[1:]

    if possible_external not in EXTERN_INHERITANCE:
        if not inheritance:
            return ':class:`%s`'%fullname

        return ''
    
    base_address = EXTERN_INHERITANCE[possible_external]

    if 'numpy' in real_name:
        htmlpage = '%s.html#%s'%(real_name.lower(), real_name)
    else:
        htmlpage = '%shtml#%s'%(possible_external.lower(), real_name)

    if inheritance:
        full_page = '"%s"'%(base_address + htmlpage)
    else:
        full_page = '`%s <%s>`_'%(fullname, base_address + htmlpage)

    return full_page


def IsPython3():
    """ Returns ``True`` if we are using Python 3.x. """

    return sys.version_info >= (3, )    

