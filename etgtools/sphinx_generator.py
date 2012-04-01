# -*- coding: utf-8 -*-
#!/usr/bin/env python

#---------------------------------------------------------------------------
# Name:        etgtools/sphinx_generator.py
# Author:      Andrea Gavana
#
# Created:     30-Nov-2010
# Copyright:   (c) 2011 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

"""
This generator will create the docstrings for Sphinx to process, by refactoring
the various XML elements passed by the Phoenix extractors into ReST format.
"""

# Standard library stuff
import os
import operator
import shutil
import textwrap
import glob

from StringIO import StringIO

import xml.etree.ElementTree as et

# Phoenix-specific stuff
import extractors
import generators

# Sphinx-Phoenix specific stuff
from sphinxtools.inheritance import InheritanceDiagram

from sphinxtools import templates

from sphinxtools.utilities import odict
from sphinxtools.utilities import ConvertToPython
from sphinxtools.utilities import RemoveWxPrefix, WriteSphinxOutput
from sphinxtools.utilities import FindControlImages, MakeSummary, PickleItem
from sphinxtools.utilities import ChopDescription, PythonizeType, Wx2Sphinx
from sphinxtools.utilities import PickleClassInfo, IsNumeric
from sphinxtools.utilities import Underscore2Capitals, CountSpaces
from sphinxtools.utilities import FormatContributedSnippets

from sphinxtools.constants import VERSION, REMOVED_LINKS, SECTIONS
from sphinxtools.constants import MAGIC_METHODS, MODULENAME_REPLACE
from sphinxtools.constants import IGNORE
from sphinxtools.constants import SPHINXROOT, DOXYROOT
from sphinxtools.constants import SNIPPETROOT, TABLEROOT, OVERVIEW_IMAGES_ROOT


# ----------------------------------------------------------------------- #

class Node(object):
    """
    This is the base class of all the subsequent classes in this script, and it
    holds information about a XML element coming from doxygen and this `Node`
    parent element (another `Node`).
    """

    # -----------------------------------------------------------------------

    def __init__(self, element, parent):
        """
        Class constructor.

        :param xml.etree.ElementTree.Element `element`: a XML element containing the
         information coming from Doxygen.
        :param Node `parent`: the parent node, or ``None``.
        """

        self.element = element
        self.parent = parent
        
        self.children = []

        if parent is not None:
            parent.Add(self)
        

    # -----------------------------------------------------------------------

    def Add(self, node):
        """
        Adds a node to its children list.

        :param Node `node`: another `Node` class.
        """

        self.children.append(node)


    # -----------------------------------------------------------------------

    def GetParent(self):
        """
        Returns this node parent or ``None`` if it has no parent.

        :rtype: :class:`Node`
        """

        return self.parent


    # -----------------------------------------------------------------------

    def GetTopLevelParent(self):
        """
        Returns the top level ancestor for this node or ``None``. If the ancestor
        is not ``None``, then it should be an instance of :class:`Root`.

        :rtype: :class:`Node`
        """

        parent = self.parent

        while 1:
            
            if parent is None:
                return

            if isinstance(parent, Root):
                return parent

            parent = parent.parent
            
    
    # -----------------------------------------------------------------------

    def GetTag(self, tag_name):
        """
        Given a `tag_name` for the element stored in this node, return the content
        of that tag (or ``None`` if this element has no such tag).

        :param string `tag_name`: the element tag name.

        :returns: The element text for the input `tag_name` or ``None``.
        """

        if isinstance(self.element, basestring):
            return None
        
        return self.element.get(tag_name)


    # -----------------------------------------------------------------------

    def GetHierarchy(self):
        """
        Returns a list of strings representing this node hierarchy up to the :class:`Root`
        node.

        :rtype: `list`
        """

        hierarchy = [self.__class__.__name__]
        parent = self.parent

        while parent:
            hierarchy.append(parent.__class__.__name__)
            parent = parent.parent

        return hierarchy


    # -----------------------------------------------------------------------

    def IsClassDescription(self):
        """
        Returns a non-empty string if this node holds information about a class general description
        (i.e., its `element` attribute does not contain information on a method, a property,
        and so on).

        This is needed to resolve ReST link conflicts in the :class:`XRef` below.

        :rtype: `string`.
        """

        top_level = self.GetTopLevelParent()

        if top_level is None:
            return ''
        
        xml_docs = top_level.xml_docs

        if xml_docs.kind != 'class':
            return ''

        dummy, class_name = Wx2Sphinx(xml_docs.class_name)
        return class_name
    

    # -----------------------------------------------------------------------

    def Find(self, klass, node=None):
        """
        This method returns ``True`` if this node contains a specific class into its
        descendants.

        :param `klass`: can be any of the classes definied in this script except :class:`XMLDocString`.
        :param `node`: another `Node` instance or ``None`` if this is the first invocation of
         this function.

        :rtype: `bool`

        .. note:: This is a recursive method.
        
        """
        

        if node is None:
            node = self
            
        for child in node.children:
            if isinstance(child, klass):
                return True

            return self.Find(klass, child)  

        return False            
                

    # -----------------------------------------------------------------------

    def GetSpacing(self):

        hierarchy = self.GetHierarchy()
        if 'ParameterList' in hierarchy:
            return ' '
        
        elif not isinstance(self, ListItem) and 'List' in hierarchy:
            return ' '*2
        
        return ''
    

    # -----------------------------------------------------------------------

    def Join(self, with_tail=True):
        """
        Join this node `element` attribute text and tail, adding all its children's
        node text and tail in the meanwhile.

        :param `with_tail`: ``True`` if the element tail should be included in the
         text, ``False`` otherwise.

        :rtype: `string`

        :returns: A string containing the ReSTified version of this node `element` text and
         tail plus all its children's element text and tail.

        .. note:: For some of the classes in this script (for example the :class:`Emphasis`,
           :class:`ComputerOutput`) the `with_tail` parameter should be set to ``False`` in order
           to avoid wrong ReST output.
        """

        text = tail = ''

        if self.element is None:
            return text
        
        if isinstance(self.element, basestring):
            text = self.element
        else:
            text, tail = self.element.text, self.element.tail
            text = (text is not None and [text] or [''])[0]
            tail = (tail is not None and [tail] or [''])[0]

        if text.strip() in REMOVED_LINKS:
            return ''
        
        text = ConvertToPython(text)

        for child in self.children:
            text += child.Join(with_tail)
        
        if with_tail and tail:
            text += ConvertToPython(tail)

        if text.strip() and not text.endswith('\n'):
            text += ' '
            
        return text
        

# ----------------------------------------------------------------------- #

class Root(Node):
    """
    This is the root class which has as its children all the other classes in
    this script (excluding :class:`XMLDocString`). It is used to hold information
    about an XML Doxygen item describing a class, a method or a function.
    """

    # -----------------------------------------------------------------------

    def __init__(self, xml_docs, is_overload, share_docstrings):
        """
        Class constructor.

        :param XMLDocString `xml_docs`: an instance of :class:`XMLDocString`.
        :param bool `is_overload`: ``True`` if the root node describes an overloaded
         method/function, ``False`` otherwise.
        :param bool `share_docstrings`: ``True`` if all the overloaded methods/functions
         share the same docstrings.
        """

        Node.__init__(self, '', None)

        self.xml_docs = xml_docs    
        self.is_overload = is_overload
        self.share_docstrings = share_docstrings
        
        self.sections = odict()


    # -----------------------------------------------------------------------

    def Insert(self, node, before=None, after=None, dontcare=True):
        """
        Inserts a node into the root children, depending of the `before` and `after`
        input arguments.
        """

        insert_at = -1
        
        for index, child in enumerate(self.children):
            if (before and child.Find(before)) or (after and child.Find(after)):
                insert_at = index
                break

        node.parent = self

        if insert_at >= 0:
            if before:
                self.children.insert(insert_at, node)
            else:
                self.children.insert(insert_at+1, node)
        else:
            if dontcare:
                self.children.append(node)
            else:
                return False

        return True
    

    # -----------------------------------------------------------------------

    def Join(self, with_tail=True):
        """
        Join this node `element` attribute text and tail, adding all its children's
        node text and tail in the meanwhile.

        :param `with_tail`: ``True`` if the element tail should be included in the
         text, ``False`` otherwise.

        :rtype: `string`

        :returns: A string containing the ReSTified version of this node `element` text and
         tail plus all its children's element text and tail.

        .. note:: For some of the classes in this script (for example the :class:`Emphasis`,
           :class:`ComputerOutput`) the `with_tail` parameter should be set to ``False`` in order
           to avoid wrong ReST output.
        """

        if self.is_overload and self.share_docstrings:
            # If it is an overloaded method and the docstrings are shared, we only return
            # information about the parameter list and admonition sections
            return self.CommonJoin(self, '')

        text = Node.Join(self, with_tail)

        # Health check
        existing_sections = self.sections.keys()[:]

        for section_name, dummy in SECTIONS:
            if section_name not in self.sections:
                continue

            existing_sections.remove(section_name)
            for section in self.sections[section_name]:
                text += '\n\n%s\n\n' % section.Join()

        # Health check
        if any(existing_sections):
            raise Exception('Unconverted sections remain: %s'%(', '.join(existing_sections)))

        return text
    

    # -----------------------------------------------------------------------

    def CommonJoin(self, node, docstrings):
        """
        Selectively join this node `element` attribute text and tail, adding all its children's
        node text and tail in the meanwhile but only if they are instances of :class:`ParameterList`
        or :class:`Section`.

        :param `node`: either `self` or a child node.
        :param string `docstrings`: the resulting docstrings obtained (they will go as output as well).

        :rtype: `string`

        .. note:: This is a recursive method.
        """
        
        for child in node.children:
            if isinstance(child, (ParameterList, Section)):
                docstrings += child.Join()
                
            docstrings = self.CommonJoin(child, docstrings)

        return docstrings
                

    # -----------------------------------------------------------------------

    def AddSection(self, section):
        """
        Adds an admonition section to the root node (i.e., `.. seealso::`, `.. note::`,
        `:returns:` and so on).

        Admonitions are somewhat different from other nodes as they need to be refactored and
        handled differently when, for example, the return value of a method is different in Phoenix
        than in wxWidgets or when the XML docs are a mess and an admonition ends up into
        a tail of an xml element...

        :param Section `section`: an instance of :class:`Section`.        
        
        """

        kind = section.section_type
        
        if kind == 'return':
            self.sections[kind] = [section]

        elif kind == 'available':
            
            if kind not in self.sections:

                text = section.element.text
                text = text.split(',')
                newtext = []
                for t in text:
                    newtext.append(t[2:].upper())

                newtext = ', '.join(newtext)
                newtext = 'Only available for %s'%newtext
                
                if section.element.tail and section.element.tail.strip():
                    newtext += ' ' + section.element.tail.strip() + ' '
                else:
                    newtext += '. '

                section.element.text = newtext
                self.sections[kind] = [section]

            else:

                prevsection = self.sections[kind][0]
                prevtext = prevsection.element.text
                
                currtext = section.element.text

                pos = 1000
                if '.' in currtext:
                    pos = currtext.index('.')
                    
                if currtext and currtext.strip():
                    prevtext = prevtext + currtext[pos+1:].strip()

                prevsection.element.text = prevtext
                self.sections[kind] = [prevsection]
                

        else:
            if kind not in self.sections:
                self.sections[kind] = []

            self.sections[kind].append(section)
            

# ----------------------------------------------------------------------- #

class ParameterList(Node):
    """
    This class holds information about XML elements with a ``<parameterlist>`` tag.
    """    

    # -----------------------------------------------------------------------

    def __init__(self, element, parent, xml_item, kind):
        """
        Class constructor.

        :param xml.etree.ElementTree.Element `element`: a XML element containing the
         information coming from Doxygen about the ``<parameterlist>`` tag
        :param Node `parent`: the parent node, must not be ``None``
        :param `xml_item`: one of the classes available in `etgtools/extractors.py`, such as
         `PyMethodDef`, `PyFunctionDef` and so on
        :param string `kind`: one of `class`, `method`, `function`.
        """

        Node.__init__(self, element, parent)
        
        self.xml_item = xml_item
        self.kind = kind

        self.checked = False        
        self.py_parameters = odict()
        
        for pdef in xml_item.items:
            
            if pdef.out:
                continue

            name = pdef.name    
            parameter = Parameter(self, pdef)
            self.py_parameters[name] = parameter
            

    # -----------------------------------------------------------------------

    def Get(self, element_name):
        """
        Returns an instance of :class:`Parameter` if this parameter name (retrieved using
        the input `element_name`) is actually in the list of parameters held by this class.

        :param string `element_name`: the parameter name.

        :rtype: :class:`Parameter` or ``None``

        .. note:: Very often the list of parameters in wxWidgets does not match the Phoenix Python
           signature, as some of the parameters in Python get merged into one or removed altogether.

        """     

        name = element_name.strip()
        
        if name not in self.py_parameters:
            return

        return self.py_parameters[name]        


    # -----------------------------------------------------------------------

    def CheckSignature(self):
        """
        Checks if the function/method signature for items coming from pure C++ implementation
        matches the parameter list itself.

        This is mostly done as health check, as there are some instances (like `wx.Locale.Init`)
        for which the function signature does not match the parameter list (see, for example,
        the `shortName` parameter in the signature against the `name` in the parameter list).

        These kind of mismatches can sometimes break the ReST docstrings.        
        """

        if self.checked:
            return

        self.checked = True        
        xml_item = self.xml_item

        if isinstance(xml_item, (extractors.PyFunctionDef, extractors.CppMethodDef)):
            return
        
        name = xml_item.name or xml_item.pyName
        name = RemoveWxPrefix(name)

        is_overload = self.GetTopLevelParent().is_overload
        
        if xml_item.overloads and not is_overload:
            return

        arguments = xml_item.pyArgsString
        if not arguments:
            return

        if hasattr(xml_item, 'isStatic') and not xml_item.isStatic:
            if arguments[:2] == '()':
                return

            arguments = arguments[1:]
                
        if '->' in arguments:
            arguments, dummy = arguments.split("->")

        arguments = arguments.strip()
        if arguments.endswith(','):
            arguments = arguments[0:-1]

        if arguments.startswith('('):
            arguments = arguments[1:]
        if arguments.endswith(')'):
            arguments = arguments[0:-1]

        signature = name + '(%s)'%arguments            
        arguments = arguments.split(',')
        py_parameters = self.py_parameters.keys()
        
        message = '\nSEVERE: Incompatibility between function/method signature and list of parameters in `%s`:\n\n' \
                  'The parameter `%s` appears in the method signature but could not be found in the parameter list.\n\n' \
                  '  ==> Function/Method signature from `extractors`: %s\n' \
                  '  ==> Parameter list from wxWidgets XML items:     %s\n\n' \
                  'This may be a documentation bug in wxWidgets or a side-effect of removing the `wx` prefix from signatures.\n\n'
        
        for arg in arguments:

            if '*' in arg or ')' in arg:
                continue
            
            arg = arg.split('=')[0].strip()

            if arg and arg not in py_parameters:

                class_name = ''
                if hasattr(xml_item, 'className') and xml_item.className is not None:
                    class_name = Wx2Sphinx(xml_item.className)[1] + '.'

                print message % (class_name + name, arg, signature, py_parameters)
                

    # -----------------------------------------------------------------------

    def Join(self, with_tail=True):
        """
        Join this node `element` attribute text and tail, adding all its children's
        node text and tail in the meanwhile.

        :param `with_tail`: ``True`` if the element tail should be included in the
         text, ``False`` otherwise.

        :rtype: `string`

        :returns: A string containing the ReSTified version of this node `element` text and
         tail plus all its children's element text and tail.

        .. note:: For some of the classes in this script (for example the :class:`Emphasis`,
           :class:`ComputerOutput`) the `with_tail` parameter should be set to ``False`` in order
           to avoid wrong ReST output.
        """

        docstrings = ''
        
        for name, parameter in self.py_parameters.items():
            docstrings += ':param %s `%s`: %s\n'%(parameter.type, name, parameter.Join().lstrip('\n'))

        if docstrings:
            docstrings = '\n\n\n%s\n\n'%docstrings

        for child in self.children:
            if not isinstance(child, Parameter):
                docstrings += child.Join() + '\n\n'
                
        return docstrings            

    
# ----------------------------------------------------------------------- #

class Parameter(Node):
    """
    This class holds information about XML elements with ``<parametername>``
    ``<parameterdescription>`` tags.
    """    

    # -----------------------------------------------------------------------

    def __init__(self, parent, pdef):
        """
        Class constructor.

        :param Node `parent`: the parent node, must not be ``None``
        :param `pdef`: a `ParamDef` class, as described in `etgtools/extractors.py`.
        """

        Node.__init__(self, '', parent)
        
        self.pdef = pdef
        self.name = pdef.name

        self.type = PythonizeType(pdef.type)        
                

# ----------------------------------------------------------------------- # 

class Paragraph(Node):
    """
    This class holds information about XML elements with a ``<para>`` tag.
    """    

    # -----------------------------------------------------------------------

    def __init__(self, element, parent, kind):
        """
        Class constructor.

        :param xml.etree.ElementTree.Element `element`: a XML element containing the
         information coming from Doxygen about the ``<para>`` tag
        :param Node `parent`: the parent node, must not be ``None``
        :param string `kind`: one of `class`, `method`, `function`.
        """

        Node.__init__(self, element, parent)

        self.kind = kind
        

    # -----------------------------------------------------------------------

    def Join(self, with_tail=True):
        """
        Join this node `element` attribute text and tail, adding all its children's
        node text and tail in the meanwhile.

        :param `with_tail`: ``True`` if the element tail should be included in the
         text, ``False`` otherwise.

        :rtype: `string`

        :returns: A string containing the ReSTified version of this node `element` text and
         tail plus all its children's element text and tail.

        .. note:: For some of the classes in this script (for example the :class:`Emphasis`,
           :class:`ComputerOutput`) the `with_tail` parameter should be set to ``False`` in order
           to avoid wrong ReST output.
        """
        
        text = Node.Join(self, with_tail)

        if 'Availability:' not in text:
            return text
        
        newtext = ''

        for line in text.splitlines():

            if 'Availability:' in line:
                
                first = line.index('Availability:')

                element = et.Element('available', kind='available')
                element.text = line[first+13:]

                section = Section(element, None, self.kind)

                root = self.GetTopLevelParent()                
                root.AddSection(section)
                
            else:
                
                newtext += line + '\n'

        return newtext
        
            
# ----------------------------------------------------------------------- #

class ReturnType(Node):
    """
    A special admonition section to customize the `:rtype:` ReST role from
    the XML / Python description.
    """    

    # -----------------------------------------------------------------------

    def __init__(self, element, parent):
        """
        Class constructor.

        :param xml.etree.ElementTree.Element `element`: a XML element
        :param Node `parent`: the parent node, must not be ``None``
        """

        Node.__init__(self, element, parent)


    # -----------------------------------------------------------------------

    def Join(self, with_tail=True):
        """
        Join this node `element` attribute text and tail, adding all its children's
        node text and tail in the meanwhile.

        :param `with_tail`: ``True`` if the element tail should be included in the
         text, ``False`` otherwise.

        :rtype: `string`

        :returns: A string containing the ReSTified version of this node `element` text and
         tail plus all its children's element text and tail.

        .. note:: For some of the classes in this script (for example the :class:`Emphasis`,
           :class:`ComputerOutput`) the `with_tail` parameter should be set to ``False`` in order
           to avoid wrong ReST output.
        """
        
        docstrings = '\n\n:rtype: %s\n\n' % self.element

        return docstrings


# ----------------------------------------------------------------------- #

class List(Node):
    """
    This class holds information about XML elements with the ``<itemizedlist>``
    and ``<orderedlist>`` tags.
    """    

    # -----------------------------------------------------------------------

    def __init__(self, element, parent):
        """
        Class constructor.

        :param xml.etree.ElementTree.Element `element`: a XML element containing the
         information coming from Doxygen about the ``<itemizedlist>`` and ``<orderedlist>`` tags
        :param Node `parent`: the parent node, must not be ``None``
        """

        Node.__init__(self, element, parent)


    # -----------------------------------------------------------------------

    def Join(self, with_tail=True):
        """
        Join this node `element` attribute text and tail, adding all its children's
        node text and tail in the meanwhile.

        :param `with_tail`: ``True`` if the element tail should be included in the
         text, ``False`` otherwise.

        :rtype: `string`

        :returns: A string containing the ReSTified version of this node `element` text and
         tail plus all its children's element text and tail.

        .. note:: For some of the classes in this script (for example the :class:`Emphasis`,
           :class:`ComputerOutput`) the `with_tail` parameter should be set to ``False`` in order
           to avoid wrong ReST output.
        """
        
        docstrings = Node.Join(self, with_tail=False)
        docstrings = '\n\n%s\n'%docstrings

        if self.element.tail:
            spacer = ('ParameterList' in self.GetHierarchy() and [' '] or [''])[0]
            text = '%s%s\n'%(spacer, ConvertToPython(self.element.tail.strip()))
            docstrings += text
        
        return docstrings

        
# ----------------------------------------------------------------------- #

class ListItem(Node):
    """
    This class holds information about XML elements with the ``<listitem>`` tag.
    """    

    # -----------------------------------------------------------------------

    def __init__(self, element, parent):
        """
        Class constructor.

        :param xml.etree.ElementTree.Element `element`: a XML element containing the
         information coming from Doxygen about the ``<listitem>`` tag
        :param Node `parent`: the parent node, must not be ``None``
        """

        Node.__init__(self, element, parent)

        self.level =  parent.GetHierarchy().count('List') - 1


    # -----------------------------------------------------------------------

    def GetSpacing(self):

        hierarchy = self.GetHierarchy()
        
        if 'ParameterList' in hierarchy:
            return ' '

        elif 'Section' in hierarchy:
            return ' '*3
        
        return '  ' * self.level


    # -----------------------------------------------------------------------

    def Join(self, with_tail=True):
        """
        Join this node `element` attribute text and tail, adding all its children's
        node text and tail in the meanwhile.

        :param `with_tail`: ``True`` if the element tail should be included in the
         text, ``False`` otherwise.

        :rtype: `string`

        :returns: A string containing the ReSTified version of this node `element` text and
         tail plus all its children's element text and tail.

        .. note:: For some of the classes in this script (for example the :class:`Emphasis`,
           :class:`ComputerOutput`) the `with_tail` parameter should be set to ``False`` in order
           to avoid wrong ReST output.
        """
        
        spacer = self.GetSpacing()

        to_remove = ['(id, event, func)', '(id1, id2, event, func)', '(id1, id2, func)',
                     '(id, func)', '(func)',
                     '(id,  event,  func)', '(id1,  id2,  event,  func)', '(id1,  id2,  func)',
                     '(id,  func)']
        
        docstrings = ''

        for child in self.children:
            child_text = child.Join(with_tail)
            for rem in to_remove:
                child_text = child_text.replace(rem, '')

            if '_:' in child_text:
                child_text = child_text.replace('_:', '_*:')
            
            docstrings += child_text
                
        docstrings = '%s- %s\n'%(spacer, docstrings)
        return docstrings


# ----------------------------------------------------------------------- #

class Section(Node):
    """
    This class holds information about XML elements with the ``<xrefsect>`` and
    ``<simplesect>`` tags.
    """    

    # -----------------------------------------------------------------------

    def __init__(self, element, parent, kind, is_overload=False, share_docstrings=False):
        """
        Class constructor.

        :param xml.etree.ElementTree.Element `element`: a XML element containing the
         information coming from Doxygen about the ``<xrefsect>`` and ``<simplesect>`` tags
        :param Node `parent`: the parent node, can be ``None``
        :param string `kind`: one of `class`, `method`, `function`
        :param bool `is_overload`: ``True`` if the root node describes an overloaded
         method/function, ``False`` otherwise.
        :param bool `share_docstrings`: ``True`` if all the overloaded methods/functions
         share the same docstrings.
        """

        Node.__init__(self, element, parent)
        
        self.kind = kind
        self.is_overload = is_overload
        self.share_docstrings = share_docstrings

        dummy, section_type = self.element.items()[0]
        self.section_type = section_type.split("_")[0]


    # -----------------------------------------------------------------------

    def Join(self, with_tail=True):
        """
        Join this node `element` attribute text and tail, adding all its children's
        node text and tail in the meanwhile.

        :param `with_tail`: ``True`` if the element tail should be included in the
         text, ``False`` otherwise.

        :rtype: `string`

        :returns: A string containing the ReSTified version of this node `element` text and
         tail plus all its children's element text and tail.

        .. note:: For some of the classes in this script (for example the :class:`Emphasis`,
           :class:`ComputerOutput`) the `with_tail` parameter should be set to ``False`` in order
           to avoid wrong ReST output.
        """
        
        section_type = self.section_type

        text = Node.Join(self, with_tail=False)
            
        if not text.strip() or len(text.strip()) < 3:
            # Empy text or just trailing commas
            return ''

        if self.is_overload and self.share_docstrings:
            return ''

        sub_spacer = ' '*3

        if section_type == 'since':
            # Special treatment for the versionadded
            if len(text) > 6:
                version, remainder = text[0:6], text[6:]
                text = '%s\n%s%s'%(version, sub_spacer, remainder)

        elif section_type == 'deprecated':
            # Special treatment for deprecated, wxWidgets devs do not put the version number
            text = '%s\n%s%s'%(VERSION, sub_spacer, text.lstrip('Deprecated'))
            
        if section_type in ['note', 'remark', 'remarks', 'return']:
            text = '\n\n' + sub_spacer + text

        for section, replacement in SECTIONS:
            if section == section_type:
                break
            
        docstrings = ''
        section_spacer = ''
        
        if section_type != 'return':
            section_spacer = self.GetSpacing()
        
        docstrings = '\n%s%s %s\n\n'%(section_spacer, replacement, text)

        return '\n' + docstrings
    

# ----------------------------------------------------------------------- #

class Image(Node):
    """
    This class holds information about XML elements with the ``<image>`` tag.
    """    

    # -----------------------------------------------------------------------

    def __init__(self, element, parent):
        """
        Class constructor.

        :param xml.etree.ElementTree.Element `element`: a XML element containing the
         information coming from Doxygen about the ``<image>`` tag
        :param Node `parent`: the parent node, must not be ``None``
        """

        Node.__init__(self, element, parent)


    # -----------------------------------------------------------------------

    def Join(self, with_tail=True):
        """
        Join this node `element` attribute text and tail, adding all its children's
        node text and tail in the meanwhile.

        :param `with_tail`: ``True`` if the element tail should be included in the
         text, ``False`` otherwise.

        :rtype: `string`

        :returns: A string containing the ReSTified version of this node `element` text and
         tail plus all its children's element text and tail.

        .. note:: For some of the classes in this script (for example the :class:`Emphasis`,
           :class:`ComputerOutput`) the `with_tail` parameter should be set to ``False`` in order
           to avoid wrong ReST output.
        """
        
        for key, value in self.element.items():
            if key == 'name':
                break

        image_path = os.path.normpath(os.path.join(DOXYROOT, 'images', value))
        static_path = os.path.join(OVERVIEW_IMAGES_ROOT, os.path.split(image_path)[1])

        if not os.path.isfile(static_path):
            shutil.copyfile(image_path, static_path)

        rel_path_index = static_path.rfind('_static')
        rel_path = os.path.normpath(static_path[rel_path_index:])
        
        docstrings = '\n\n'
        docstrings += '.. figure:: %s\n' % rel_path
        docstrings += '   :align: center\n\n\n'
        docstrings += '|\n\n'

        if self.element.tail and self.element.tail.strip():
            docstrings += ConvertToPython(self.element.tail.rstrip())

        return docstrings

# ----------------------------------------------------------------------- #

class Table(Node):
    """
    This class holds information about XML elements with the ``<table>`` tag.
    """    

    # -----------------------------------------------------------------------

    def __init__(self, element, parent, xml_item_name):
        """
        Class constructor.

        :param xml.etree.ElementTree.Element `element`: a XML element containing the
         information coming from Doxygen about the ``<table>`` tag
        :param Node `parent`: the parent node, must not be ``None``
        :param string `xml_item_name`: if a custom version of a table has been created
         inside the ``TABLEROOT`` folder, the `xml_item_name` string will match the
         ``*.rst`` file name for the custom table.

        .. note:: 

                  There are 3 customized versions of 3 XML tables up to now, for various reasons:
        
                  1. The `wx.Sizer` flags table is a flexible grid table, very difficult to ReSTify automatically
                  2. The `wx.ColourDatabase` table of colour comes up all messy when ReSTified from XML
                  3. The "wxWidgets 2.8 Compatibility Functions" table for `wx.VScrolledWindow`
         
        """

        Node.__init__(self, element, parent)
        
        self.xml_item_name = xml_item_name


    # -----------------------------------------------------------------------

    def Join(self, with_tail=True): 
        """
        Join this node `element` attribute text and tail, adding all its children's
        node text and tail in the meanwhile.

        :param `with_tail`: ``True`` if the element tail should be included in the
         text, ``False`` otherwise.

        :rtype: `string`

        :returns: A string containing the ReSTified version of this node `element` text and
         tail plus all its children's element text and tail.

        .. note:: For some of the classes in this script (for example the :class:`Emphasis`,
           :class:`ComputerOutput`) the `with_tail` parameter should be set to ``False`` in order
           to avoid wrong ReST output.
        """

        needs_space = 'ParameterList' in self.GetHierarchy()        
        spacer = (needs_space and [' '] or [''])[0]

        rows, cols = int(self.element.get('rows')), int(self.element.get('cols'))

        longest = [0]*cols
        has_title = False

        count = 0        
        for row in xrange(rows):
            for col in xrange(cols):
                child = self.children[count]
                
                text = child.Join(with_tail)
                longest[col] = max(len(text), longest[col])

                if (row == 0 and col == 0 and '**' in text) or child.GetTag('thead') == 'yes':
                    has_title = True

                count += 1
                
        table = '\n\n'
        table += spacer
        formats = []

        for lng in longest:
            table += '='* lng + ' '
            formats.append('%-' + '%ds'%(lng+1))
            
        table += '\n'

        count = 0
        
        for row in xrange(rows):

            table += spacer
            
            for col in xrange(cols):
                table += formats[col] % (self.children[count].Join(with_tail).strip())
                count += 1

            table += '\n'

            if row == 0 and has_title:

                table += spacer
                
                for lng in longest:
                    table += '='* lng + ' '

                table += '\n'

        table += spacer
        
        for lng in longest:
            table += '='* lng + ' '

        table += '\n\n%s|\n\n'%spacer

        possible_rest_input = os.path.join(TABLEROOT, self.xml_item_name)
        
        if os.path.isfile(possible_rest_input):
            table = '\n\n' + spacer + '.. include:: %s\n\n'%possible_rest_input

        if self.element.tail and self.element.tail.strip():
            table += ConvertToPython(self.element.tail.rstrip())

        return table

# ----------------------------------------------------------------------- #

class TableEntry(Node):
    """
    This class holds information about XML elements with the ``<entry>`` tag.
    """    
    pass

# ----------------------------------------------------------------------- #

class Snippet(Node):
    """
    This class holds information about XML elements with the ``<programlisting>``,
    ``<sp>``, ``<codeline>``, ``<highlight>`` and ``<ref>`` (but only when the
    ``<ref>`` tags appears as a child of ``<programlisting>``) tags.
    """    

    # -----------------------------------------------------------------------

    def __init__(self, element, parent, cpp_file, python_file, converted_py):
        """
        Class constructor.

        :param xml.etree.ElementTree.Element `element`: a XML element containing the
         information coming from Doxygen about the aforementioned tags
        :param Node `parent`: the parent node, must not be ``None``
        :param string `cpp_file`: the path to the C++ snippet of code found in the XML
         wxWidgets docstring, saved into the ``SNIPPETROOT/cpp`` folder
        :param string `python_file`: the path to the roughly-converted to Python
         snippet of code found in the XML wxWidgets docstring, saved into the
         ``SNIPPETROOT/python`` folder
        :param string `converted_py`: the path to the fully-converted to Python
         snippet of code found in the XML wxWidgets docstring, saved into the
         ``SNIPPETROOT/python/converted`` folder.         
        """
        
        Node.__init__(self, element, parent)
        
        self.cpp_file = cpp_file
        self.python_file = python_file
        self.converted_py = converted_py

        self.snippet = ''
        

    # -----------------------------------------------------------------------

    def AddCode(self, element):
        """
        Adds a C++ part of the code snippet.

        :param xml.etree.ElementTree.Element `element`: a XML element containing the
         information coming from Doxygen about the aforementioned tags.
        """

        tag = element.tag
        
        if tag == 'codeline':
            self.snippet += '\n'
            
        elif tag in ['highlight', 'ref', 'sp']:

            if tag == 'sp':
                self.snippet += ' '
                
            if isinstance(element, basestring):
                self.snippet += element
            else:
                if element.text:
                    self.snippet += element.text.strip(' ')
                if element.tail:
                    self.snippet += element.tail.strip(' ')
                    
        else:
            raise Exception('Unhandled tag in class Snippet: %s'%tag)
        

    # -----------------------------------------------------------------------

    def Join(self, with_tail=True):
        """
        Join this node `element` attribute text and tail, adding all its children's
        node text and tail in the meanwhile.

        :param `with_tail`: ``True`` if the element tail should be included in the
         text, ``False`` otherwise.

        :rtype: `string`

        :returns: A string containing the ReSTified version of this node `element` text and
         tail plus all its children's element text and tail.

        .. note:: For some of the classes in this script (for example the :class:`Emphasis`,
           :class:`ComputerOutput`) the `with_tail` parameter should be set to ``False`` in order
           to avoid wrong ReST output.
        """
        
        docstrings = ''
        
        fid = open(self.cpp_file, 'wt')
        fid.write(self.snippet)
        fid.close()

        if not os.path.isfile(self.converted_py):

            message = '\nWARNING: Missing C++ => Python conversion of the snippet of code for %s'%(os.path.split(self.cpp_file)[1])
            message += '\n\nA slightly Pythonized version of this snippet has been saved into:\n\n  ==> %s\n\n'%self.python_file

            print message
            
            py_code = self.snippet.replace(';', '')
            py_code = py_code.replace('{', '').replace('}', '')
            py_code = py_code.replace('->', '.').replace('//', '#')
            py_code = py_code.replace('m_', 'self.')
            py_code = py_code.replace('::', '.')
            py_code = py_code.replace('wx', 'wx.')
            py_code = py_code.replace('new ', '').replace('this', 'self')
            py_code = py_code.replace('( ', '(').replace(' )', ')')
            py_code = py_code.replace('||', 'or').replace('&&', 'and')

            spacer = ' '*4
            new_py_code = ''
            
            for code in py_code.splitlines():
                new_py_code += spacer + code + '\n'

            fid = open(self.python_file, 'wt')
            fid.write(new_py_code)
            fid.close()

        else:

            fid = open(self.converted_py, 'rt')
            
            while 1:
                tline = fid.readline()
                if not tline.strip():
                    continue

                code = tline + fid.read()
                fid.close()
                break

            docstrings += '::\n\n'
            docstrings += code.rstrip() + '\n\n'

        if self.element.tail and len(self.element.tail.strip()) > 1:
            spacer = ('Section' in self.GetHierarchy() and ['   '] or [''])[0]
            tail = ConvertToPython(self.element.tail.lstrip())
            tail = tail.replace('\n', ' ')
            docstrings += spacer + tail.replace('  ', ' ')

        return docstrings
        

# ----------------------------------------------------------------------- #

class XRef(Node):
    """
    This class holds information about XML elements with the ``<ref>`` tag, excluding
    when these elements are children of a ``<programlisting>`` element.
    """    

    # -----------------------------------------------------------------------

    def __init__(self, element, parent):
        """
        Class constructor.

        :param xml.etree.ElementTree.Element `element`: a XML element containing the
         information coming from Doxygen about the aforementioned tags
        :param Node `parent`: the parent node, must not be ``None``.
        """

        Node.__init__(self, element, parent)


    # -----------------------------------------------------------------------

    def Join(self, with_tail=True):
        """
        Join this node `element` attribute text and tail, adding all its children's
        node text and tail in the meanwhile.

        :param `with_tail`: ``True`` if the element tail should be included in the
         text, ``False`` otherwise.

        :rtype: `string`

        :returns: A string containing the ReSTified version of this node `element` text and
         tail plus all its children's element text and tail.

        .. note:: For some of the classes in this script (for example the :class:`Emphasis`,
           :class:`ComputerOutput`) the `with_tail` parameter should be set to ``False`` in order
           to avoid wrong ReST output.
        """

        element = self.element
        text = element.text

        tail = element.tail
        tail = (tail is not None and [tail] or [''])[0]
        
        hascomma = '::' in text

        original = text        
        text = RemoveWxPrefix(text)
        text = text.replace("::", ".")
        
        if "(" in text:
            text = text[0:text.index("(")]

        refid, link = element.items()[0]
        remainder = link.split('_')[-1]

        space_before, space_after = CountSpaces(text)
        stripped = text.strip()
            
        if stripped in IGNORE:
            return space_before + text + space_after + tail
        
        if ' ' in stripped or 'overview' in link:
            if 'classwx_' in link:
                ref = 1000
                if '_1' in link:
                    ref = link.index('_1')

                ref = Underscore2Capitals(link[6:ref])
                text = ':ref:`%s <%s>`'%(stripped, ref)

            elif 'funcmacro' in link or 'samples' in link or 'debugging' in text.lower() or \
                 'unix' in text.lower() or 'page_libs' in link:
                text = space_before + space_after
            elif 'library list' in stripped.lower():
                text = space_before + text + space_after
            else:
                backlink = stripped.lower()
                if 'device context' in backlink:
                    backlink = 'device contexts'
                elif 'reference count' in backlink or 'refcount' in link:
                    backlink = 'reference counting'
                elif 'this list' in backlink:
                    backlink = 'stock items'
                elif 'window deletion' in backlink:
                    backlink = 'window deletion'
                elif 'programming with wxboxsizer' in backlink:
                    stripped = 'Programming with BoxSizer'
                    backlink = 'programming with boxsizer'
                    
                text = ':ref:`%s <%s>`'%(stripped, backlink)
        
        elif (text.upper() == text and len(stripped) > 4):

            if not original.strip().startswith('wx') or ' ' in stripped:
                text = ''
            
            elif not IsNumeric(text):
                text = '``%s``'%text
                
        elif 'funcmacro' in link:
            if '(' in stripped:
                stripped = stripped[0:stripped.index('(')].strip()
                
            text =  ':func:`%s`'%stripped

        elif hascomma or len(remainder) > 30:
            if '.m_' in text:
                text = '``%s``'%stripped
            else:
                # it was :meth:
                if '.wx' in text:
                    prev = text.split('.')
                    text = '.'.join(prev[:-1]) + '.__init__'
                    text =  ':meth:`%s` '%text.strip()

                else:
                    stripped = text.strip()

                    if '(' in stripped:
                        stripped = stripped[0:stripped.index('(')].strip()
                    
                    if '.' not in stripped:
                        klass = self.IsClassDescription()
                        if klass:
                            text = ':meth:`~%s.%s`'%(klass, stripped)
                        else:
                            text =  ':meth:`%s` '%stripped
                    else:
                        text =  ':meth:`%s` '%stripped

        else:
            text = ':ref:`%s`'%Wx2Sphinx(stripped)[1]

        return space_before + text + space_after + ConvertToPython(tail)
    

# ----------------------------------------------------------------------- #

class ComputerOutput(Node):
    """
    This class holds information about XML elements with the ``<computeroutput>`` tag.
    """    

    def __init__(self, element, parent):
        """
        Class constructor.

        :param xml.etree.ElementTree.Element `element`: a XML element containing the
         information coming from Doxygen about the aforementioned tags
        :param Node `parent`: the parent node, must not be ``None``.
        """

        Node.__init__(self, element, parent)


    # -----------------------------------------------------------------------

    def Join(self, with_tail=True):
        """
        Join this node `element` attribute text and tail, adding all its children's
        node text and tail in the meanwhile.

        :param `with_tail`: ``True`` if the element tail should be included in the
         text, ``False`` otherwise.

        :rtype: `string`

        :returns: A string containing the ReSTified version of this node `element` text and
         tail plus all its children's element text and tail.

        .. note:: For some of the classes in this script (for example the :class:`Emphasis`,
           :class:`ComputerOutput`) the `with_tail` parameter should be set to ``False`` in order
           to avoid wrong ReST output.
        """

        text = self.element.text
        if not text and not self.children:
            return ''

        if text is not None:
            stripped = text.strip()
            space_before, space_after = CountSpaces(text)
        
            text = RemoveWxPrefix(text.strip())

        else:
            text = ''

        for child in self.children:
            text += child.Join(with_tail=False)

        if '`' not in text:
            text = "``%s`` "%text

        if self.element.tail:
            text += ConvertToPython(self.element.tail)

        space_before, space_after = CountSpaces(text)
        if space_before == '':
            space_before = ' '

        return space_before + text + space_after


# ----------------------------------------------------------------------- #

class Emphasis(Node):
    """
    This class holds information about XML elements with the ``<emphasis>`` and
    ``<bold>`` tags.
    """    

    # -----------------------------------------------------------------------

    def __init__(self, element, parent):
        """
        Class constructor.

        :param xml.etree.ElementTree.Element `element`: a XML element containing the
         information coming from Doxygen about the aforementioned tags
        :param Node `parent`: the parent node, must not be ``None``.
        """

        Node.__init__(self, element, parent)


    # -----------------------------------------------------------------------

    def Join(self, with_tail=True):
        """
        Join this node `element` attribute text and tail, adding all its children's
        node text and tail in the meanwhile.

        :param `with_tail`: ``True`` if the element tail should be included in the
         text, ``False`` otherwise.

        :rtype: `string`

        :returns: A string containing the ReSTified version of this node `element` text and
         tail plus all its children's element text and tail.

        .. note:: For some of the classes in this script (for example the :class:`Emphasis`,
           :class:`ComputerOutput`) the `with_tail` parameter should be set to ``False`` in order
           to avoid wrong ReST output.
        """

        if self.element.tag == 'emphasis':
            format = '`%s`'
            emphasys = '`'
        elif self.element.tag == 'bold':
            format = '**%s**'
            emphasys = '**'

        spacing = ('ParameterList' in self.GetHierarchy() and [' '] or [''])[0]

        text = Node.Join(self, with_tail=False)

        if self.children:

            startPos = 0
            newText = spacing

            for child in self.children:
                childText = child.Join()

                tail = child.element.tail
                tail = (tail is not None and [tail] or [''])[0]

                childText = childText.replace(ConvertToPython(tail), '')
                fullChildText = child.Join()
                endPos = text.index(childText)

                newText += ' ' + emphasys + text[startPos:endPos].strip() + emphasys + ' '
                newText += childText + ' '
                remaining = fullChildText.replace(childText, '')
                newText += emphasys + remaining.strip() + emphasys + ' '
                
                startPos = endPos

            text = newText
            
        else:
            
            if text.strip():
                text = spacing + format % text.strip()

        if self.element.tail:
            text += ConvertToPython(self.element.tail)

        return text


# ----------------------------------------------------------------------- #

class Title(Node):
    """
    This class holds information about XML elements with the ``<title>`` tag.
    """    

    # -----------------------------------------------------------------------

    def __init__(self, element, parent):
        """
        Class constructor.

        :param xml.etree.ElementTree.Element `element`: a XML element containing the
         information coming from Doxygen about the aforementioned tags
        :param Node `parent`: the parent node, must not be ``None``.
        """

        Node.__init__(self, element, parent)


    # -----------------------------------------------------------------------

    def Join(self, with_tail=True):
        """
        Join this node `element` attribute text and tail, adding all its children's
        node text and tail in the meanwhile.

        :param `with_tail`: ``True`` if the element tail should be included in the
         text, ``False`` otherwise.

        :rtype: `string`

        :returns: A string containing the ReSTified version of this node `element` text and
         tail plus all its children's element text and tail.

        .. note:: For some of the classes in this script (for example the :class:`Emphasis`,
           :class:`ComputerOutput`) the `with_tail` parameter should be set to ``False`` in order
           to avoid wrong ReST output.
        """

        text = '|phoenix_title| ' + ConvertToPython(self.element.text)
        lentext = len(text)
        text = '\n\n%s\n%s\n\n'%(text.rstrip('.'), '='*lentext)

        return text


# ----------------------------------------------------------------------- #

class ULink(Node):
    """
    This class holds information about XML elements with the ``<ulink>`` tag.
    """    

    # -----------------------------------------------------------------------

    def __init__(self, element, parent):
        """
        Class constructor.

        :param xml.etree.ElementTree.Element `element`: a XML element containing the
         information coming from Doxygen about the aforementioned tags
        :param Node `parent`: the parent node, must not be ``None``.
        """

        Node.__init__(self, element, parent)


    # -----------------------------------------------------------------------

    def Join(self, with_tail=True):
        """
        Join this node `element` attribute text and tail, adding all its children's
        node text and tail in the meanwhile.

        :param `with_tail`: ``True`` if the element tail should be included in the
         text, ``False`` otherwise.

        :rtype: `string`

        :returns: A string containing the ReSTified version of this node `element` text and
         tail plus all its children's element text and tail.

        .. note:: For some of the classes in this script (for example the :class:`Emphasis`,
           :class:`ComputerOutput`) the `with_tail` parameter should be set to ``False`` in order
           to avoid wrong ReST output.
        """

        dummy, link = self.element.items()[0]
        text = self.element.text
        
        text = '`%s <%s>`_'%(text, link)

        if self.element.tail:
            text += ConvertToPython(self.element.tail)

        return text

            
# ----------------------------------------------------------------------- #

class XMLDocString(object):
    """
    This is the main class of this script, and it uses heavily the :class:`Node`
    subclasses documented above.

    The :class:`XMLDocString` is responsible for building function/method signatures,
    class descriptions, window styles and events and so on. 
    """    

    # -----------------------------------------------------------------------

    def __init__(self, xml_item, is_overload=False, share_docstrings=False):
        """
        Class constructor.

        :param `xml_item`: one of the classes available in `etgtools/extractors.py`, such as
         `PyMethodDef`, `PyFunctionDef` and so on
        :param bool `is_overload`: ``True`` if this class describes an overloaded
         method/function, ``False`` otherwise.
        :param bool `share_docstrings`: ``True`` if all the overloaded methods/functions
         share the same docstrings.
        """

        self.xml_item = xml_item
        self.is_overload = is_overload
        self.share_docstrings = share_docstrings
                
        self.docstrings = ''

        self.class_name = ''
        
        self.snippet_count = 0
        self.contrib_snippets = []

        self.table_count = 0

        self.list_level = 1        
        self.list_order = {}

        self.parameter_list = None

        self.root = Root(self, is_overload, share_docstrings)
        
        self.appearance = []
        self.overloads = []
        
        if isinstance(xml_item, extractors.MethodDef):
            self.kind = 'method'
        elif isinstance(xml_item, (extractors.FunctionDef, extractors.PyFunctionDef)):
            self.kind = 'function'
        elif isinstance(xml_item, (extractors.ClassDef, extractors.PyClassDef)):
            self.kind = 'class'
            self.appearance = FindControlImages(xml_item)
            self.class_name = RemoveWxPrefix(xml_item.name) or xml_item.pyName
        elif isinstance(xml_item, extractors.EnumDef):
            self.kind = 'enum'
        else:
            raise Exception('Unhandled docstring kind for %s'%xml_item.__class__.__name__)

        if hasattr(xml_item, 'deprecated') and xml_item.deprecated:
            element = et.Element('deprecated', kind='deprecated')
            element.text = VERSION
            
            deprecated_section = Section(element, None, self.kind, self.is_overload, self.share_docstrings)
            self.root.AddSection(deprecated_section)
            

    # -----------------------------------------------------------------------

    def ToReST(self):
        """ Auxiliary method. """

        brief, detailed = self.xml_item.briefDoc, self.xml_item.detailedDoc

        self.RecurseXML(brief, self.root)
                
        for detail in detailed:
            blank_element = Node('\n\n\n', self.root)
            self.RecurseXML(detail, self.root)

        self.InsertParameterList()
        self.BuildSignature()
        self.docstrings = self.root.Join()
        
        self.LoadOverLoads()


    # -----------------------------------------------------------------------

    def GetBrief(self):
        """
        Returns a ReSTified version of the `briefDoc` attribute for the XML docstrings.

        :rtype: `string`
        """

        brief = self.xml_item.briefDoc

        dummy_root = Root(self, False, False)
        rest_class = self.RecurseXML(brief, dummy_root)
        return rest_class.Join()
                

    # -----------------------------------------------------------------------

    def LoadOverLoads(self):
        """
        Extracts the overloaded implementations of a method/function, unless this
        class is itself an overload or the current method/function has no overloads.
        """
        
        if self.is_overload:
            return
                
        if self.kind not in ['method', 'function'] or not self.xml_item.overloads:
            return

        share_docstrings = True
        all_docs = []

        for sub_item in [self.xml_item] + self.xml_item.overloads:

            if sub_item.ignored:
                continue

            dummy_root = Root(self, False, False)
            self.RecurseXML(sub_item.briefDoc, dummy_root)

            for det in sub_item.detailedDoc:
                self.RecurseXML(det, dummy_root)

            all_docs.append(dummy_root.Join())
                
        if len(all_docs) == 1:
            # Only one overload, don't act like there were more
            self.xml_item.overloads = []
            return
        
        zero = all_docs[0]
        for docs in all_docs[1:]:
            if docs != zero:
                share_docstrings = False
                break
        
        self.share_docstrings = share_docstrings
        
        for sub_item in [self.xml_item] + self.xml_item.overloads:

            if sub_item.ignored:
                continue
            
            sub_item.name = self.xml_item.pyName or RemoveWxPrefix(self.xml_item.name)
            docstring = XMLDocString(sub_item, is_overload=True, share_docstrings=share_docstrings)
            docstring.class_name = self.class_name
            docstring.current_module = self.current_module

            docs = docstring.Dump()
            self.overloads.append(docs)
        

    # -----------------------------------------------------------------------

    def RecurseXML(self, element, parent):
        """
        Scan recursively all the XML elements which make up the whole documentation for
        a particular class/method/function.

        :param xml.etree.ElementTree.Element `element`: a XML element containing the
         information coming from Doxygen about the aforementioned tags
        :param Node `parent`: the parent node, a subclass of the :class:`Node` class.

        :rtype: a subclass of :class:`Node`

        .. note: This is a recursive method.        
        """

        if element is None:
            return Node('', parent)            

        if isinstance(element, basestring):
            rest_class = Paragraph(element, parent, self.kind)
            return rest_class
        
        tag, text, tail = element.tag, element.text, element.tail

        text = (text is not None and [text] or [''])[0]
        tail = (tail is not None and [tail] or [''])[0]
        
        if tag == 'parameterlist':
            rest_class = ParameterList(element, parent, self.xml_item, self.kind)
            self.parameter_list = rest_class

        elif tag == 'parametername':
            self.parameter_name = text
            rest_class = self.parameter_list

        elif tag == 'parameterdescription':
            parameter_class = self.parameter_list.Get(self.parameter_name)
            if parameter_class:
                rest_class = parameter_class
                parameter_class.element = element
            else:
                rest_class = self.parameter_list
                
        elif tag in ['itemizedlist', 'orderedlist']:
            rest_class = List(element, parent)

        elif tag == 'listitem':
            rest_class = ListItem(element, parent)

        elif tag in ['simplesect', 'xrefsect']:
            if 'ListItem' in parent.GetHierarchy():
                rest_class = Section(element, parent, self.kind, self.is_overload, self.share_docstrings)
            else:
                if element.tail:
                    Node(element.tail, parent)
                    
                rest_class = Section(element, None, self.kind, self.is_overload, self.share_docstrings)
                self.root.AddSection(rest_class)
                        
        elif tag == 'image':
            rest_class = Image(element, parent)

        elif tag == 'table':
            fullname = self.GetFullName()
            self.table_count += 1
            fullname = '%s.%d.rst'%(fullname, self.table_count)
            rest_class = Table(element, parent, fullname)
            self.table = rest_class

        elif tag == 'entry':
            rest_class = TableEntry(element, self.table)

        elif tag == 'row':
            rest_class = self.table
            
        elif tag == 'programlisting':
            cpp_file, python_file, converted_py = self.SnippetName()
            rest_class = Snippet(element, parent, cpp_file, python_file, converted_py)
            self.code = rest_class

        elif tag in ['codeline', 'highlight', 'sp']:
            self.code.AddCode(element)
            rest_class = self.code
            
        elif tag == 'ref':
            if 'Snippet' in parent.GetHierarchy():
                self.code.AddCode(element)
                rest_class = self.code
            else:
                rest_class = XRef(element, parent)
                
        elif tag == 'computeroutput':
            rest_class = ComputerOutput(element, parent)
            
        elif tag in ['emphasis', 'bold']:
            rest_class = Emphasis(element, parent)

        elif tag == 'title':
            text = ConvertToPython(element.text)
            rest_class = Title(element, parent)

        elif tag == 'para':
            rest_class = Paragraph(element, parent, self.kind)

        elif tag == 'linebreak':
            spacer = ''
            dummy = Node('\n\n%s%s'%(spacer, tail.strip()), parent)
            rest_class = parent
            
        elif tag == 'ulink':
            rest_class = ULink(element, parent)
            
        elif tag == 'onlyfor':
            onlyfor = et.Element('available', kind='available')
            onlyfor.text = text
            onlyfor.tail = tail

            section = Section(onlyfor, None, self.kind)

            self.root.AddSection(section)
            rest_class = parent
                
        else:                
            rest_class = Node('', parent)

        for child_element in element:
            self.RecurseXML(child_element, rest_class)

        return rest_class        
                            

    # -----------------------------------------------------------------------

    def GetFullName(self):
        """
        Returns the complete name for a class/method/function, including
        its module/package.

        :rtype: `string`
        """

        if self.kind == 'class':
            klass = self.xml_item
            name = RemoveWxPrefix(klass.name) or klass.pyName
            dummy, fullname = Wx2Sphinx(name)
        elif self.kind == 'method':
            method = self.xml_item
            if hasattr(method, 'isCtor') and method.isCtor:
                method_name = '__init__'
                
                if hasattr(method, 'className') and method.className is not None:
                    klass = RemoveWxPrefix(method.className)
                else:
                    klass = RemoveWxPrefix(method.klass.name)
                    
                method_name = '%s.%s'%(klass, method_name)
            else:
                method_name = method.name or method.pyName
                if hasattr(method, 'className') and method.className is not None:
                    klass = RemoveWxPrefix(method.className)
                    method_name = '%s.%s'%(klass, method_name)
                elif hasattr(method, 'klass'):
                    klass = RemoveWxPrefix(method.klass.name)
                    method_name = '%s.%s'%(klass, method_name)
                else:
                    method_name = RemoveWxPrefix(method_name)
                    method_name = '%s'%method_name
                    klass = None

            dummy, fullname = Wx2Sphinx(method_name)
        elif self.kind == 'function':
            function = self.xml_item
            name = function.pyName or function.name
            fullname = self.current_module + 'functions.%s'%name

        return fullname            


    # -----------------------------------------------------------------------

    def SnippetName(self):
        """
        Returns a tuple of 3 elements (3 file paths), representing the following:

        1. `cpp_file`: the path to the C++ snippet of code found in the XML
           wxWidgets docstring, saved into the ``SNIPPETROOT/cpp`` folder
        2. `python_file`: the path to the roughly-converted to Python
           snippet of code found in the XML wxWidgets docstring, saved into the
           ``SNIPPETROOT/python`` folder
        3. `converted_py`: the path to the fully-converted to Python
           snippet of code found in the XML wxWidgets docstring, saved into the
           ``SNIPPETROOT/python/converted`` folder.               
        """

        fullname = self.GetFullName()

        self.snippet_count += 1
        
        cpp_file = os.path.join(SNIPPETROOT, 'cpp', fullname + '.%d.cpp'%self.snippet_count)
        python_file = os.path.join(SNIPPETROOT, 'python', fullname + '.%d.py'%self.snippet_count)
        converted_py = os.path.join(SNIPPETROOT, 'python', 'converted', fullname + '.%d.py'%self.snippet_count)
        
        return cpp_file, python_file, converted_py


    def HuntContributedSnippets(self):
        
        fullname = self.GetFullName()
        contrib_folder = os.path.join(SNIPPETROOT, 'python', 'contrib')

        possible_py = glob.glob(os.path.normpath(contrib_folder + '/' + fullname + '*.py'))

        return possible_py
                

    # -----------------------------------------------------------------------

    def Dump(self, write=True):
        """
        Dumps the whole ReSTified docstrings and returns its correct ReST representation.

        :param bool `write`: ``True`` to write the resulting docstrings to a file, ``False``
         otherwise.

        :rtype: `string`
        """

        self.ToReST()
        
        methodMap = {
            'class'         : self.DumpClass,
            'method'        : self.DumpMethod,
            'function'      : self.DumpFunction,
            'enum'          : self.DumpEnum,
            }

        function = methodMap[self.kind]
        return function(write)


    # -----------------------------------------------------------------------

    def DumpClass(self, write):
        """
        Dumps a ReSTified class description and returns its correct ReST representation.

        :param bool `write`: ``True`` to write the resulting docstrings to a file, ``False``
         otherwise.

        :rtype: `string`
        """

        stream = StringIO()        

        # class declaration
        klass = self.xml_item
        name = self.class_name
        dummy, fullname = Wx2Sphinx(name)
        
        stream.write(templates.TEMPLATE_DESCRIPTION % (fullname, name))

        self.Reformat(stream)

        if not klass.nodeBases:
            klass.nodeBases = ({name: (name, name, [])}, [name])
            
        inheritance_diagram = InheritanceDiagram(klass.nodeBases)
        png, map = inheritance_diagram.MakeInheritanceDiagram()

        image_desc = templates.TEMPLATE_INHERITANCE % (name, png, name, map)
        stream.write(image_desc)

        if self.appearance:
            appearance_desc = templates.TEMPLATE_APPEARANCE % tuple(self.appearance)
            stream.write(appearance_desc)

        if klass.subClasses:
            subs = [':ref:`%s`'%Wx2Sphinx(cls)[1] for cls in klass.subClasses]
            subs = ', '.join(subs)
            subs_desc = templates.TEMPLATE_SUBCLASSES % subs
            stream.write(subs_desc)

        possible_py = self.HuntContributedSnippets()
        
        if possible_py:
            possible_py.sort()
            snippets = FormatContributedSnippets(self.kind, possible_py)
            stream.write(snippets)

        if klass.method_list:
            summary = MakeSummary(name, klass.method_list, templates.TEMPLATE_METHOD_SUMMARY, 'meth')
            stream.write(summary)

        if klass.property_list:
            summary = MakeSummary(name, klass.property_list, templates.TEMPLATE_PROPERTY_SUMMARY, 'attr')
            stream.write(summary)

        stream.write(templates.TEMPLATE_API)
        stream.write("\n.. class:: %s"%name)

        bases = klass.bases or ['object']
        
        if bases:
            stream.write('(')
            bases = [RemoveWxPrefix(b) for b in bases]
            stream.write(', '.join(bases))
            stream.write(')')

        stream.write('\n\n')

        py_docs = klass.pyDocstring

        if isinstance(self.xml_item, extractors.PyClassDef):
            newlines = self.xml_item.briefDoc.splitlines()
        else:
            newlines = []

            found = False
            for line in py_docs.splitlines():

                if line.startswith(name):
                    if not found:
                        newlines.append("**Possible constructors**::\n")
                        found = True
                else:
                    found = False
                    newlines.append(ConvertToPython(line))

                if found:
                    newlines = self.CodeIndent(line, newlines)

        newdocs = u''
        for line in newlines:
            newdocs += ' '*3 + line + "\n"

        stream.write(newdocs + "\n\n")
        
        if write:
            WriteSphinxOutput(stream, self.output_file)
        else:
            return stream.getvalue()
        

    # -----------------------------------------------------------------------

    def BuildSignature(self):
        """ Builds a function/method signature. """
        
        if self.kind not in ['method', 'function']:
            return
        
        if self.kind == 'method':

            method = self.xml_item
            name = method.name or method.pyName
            name = RemoveWxPrefix(name)            

            if method.overloads and not self.is_overload:
                if not method.isStatic:
                    arguments = '(self, *args, **kw)'
                else:
                    arguments = '(*args, **kw)'
            else:
                arguments = method.pyArgsString
                if not arguments:
                    arguments = '()'
                if not method.isStatic:
                    if arguments[:2] == '()':
                        arguments = '(self)' + arguments[2:]
                    else:
                        arguments = '(self, ' + arguments[1:]
                        
                if '->' in arguments:
                    arguments, after = arguments.split("->")
                    self.AddReturnType(after, name)

            arguments = arguments.rstrip()
            if arguments.endswith(','):
                arguments = arguments[0:-1]
            
            if not arguments.endswith(')'):
                arguments += ')'

            if self.is_overload:
                arguments = '`%s`'%arguments.strip()

        elif self.kind == 'function':

            function = self.xml_item
            name = function.name or function.pyName
            name = RemoveWxPrefix(name)

            if function.overloads and not self.is_overload:
                arguments = '(*args, **kw)'
            else:
                if "->" in function.pyArgsString:
                    arguments, after = function.pyArgsString.split("->")
                    self.AddReturnType(after, name)
                else:
                    arguments = function.pyArgsString
            
            if self.is_overload:
                arguments = '`%s`'%arguments.strip()

        self.arguments = arguments


    # -----------------------------------------------------------------------

    def InsertParameterList(self):
        """
        Inserts a :class:`ParameterList` item in the correct position into the
        :class:`Root` hierarchy, and checks the signature validity against the
        parameter list itself.
        """

        if self.kind not in ['method', 'function']:
            return

        if self.parameter_list is not None:
            self.parameter_list.CheckSignature()
            return

        if not self.xml_item.overloads or self.is_overload:
            self.parameter_list = ParameterList('', None, self.xml_item, self.kind)            
            self.root.Insert(self.parameter_list, before=Section)
            self.parameter_list.CheckSignature()
        

    # -----------------------------------------------------------------------

    def AddReturnType(self, after, name):

        after = after.strip()
        
        if not after:
            return
        
        if '(' in after:

            rtype = ReturnType('`tuple`', None)
            
            return_section = after.lstrip('(').rstrip(')')
            return_section = return_section.split(',')
            new_section = []
            
            for ret in return_section:
                if ret[0].isupper():
                    new_section.append(':ref:`%s`'%ret.strip())
                else:
                    new_section.append('`%s`'%ret.strip())

            element = et.Element('return', kind='return')
            element.text = '( %s )'%(', '.join(new_section))
            
            return_section = Section(element, None, self.kind, self.is_overload, self.share_docstrings)
            self.root.AddSection(return_section)
                    
        else:

            rtype = PythonizeType(after)

            if not rtype:
                return
            
            if rtype[0].isupper() or '.' in rtype:
                rtype = ':ref:`%s`'%rtype
            else:
                rtype = '`%s`'%rtype

            rtype = ReturnType(rtype, None)

        if self.parameter_list:
            self.parameter_list.Add(rtype)
        else:
            self.root.Insert(rtype, before=Section)


    # -----------------------------------------------------------------------

    def DumpMethod(self, write):
        """
        Dumps a ReSTified method description and returns its correct ReST representation.

        :param bool `write`: ``True`` to write the resulting docstrings to a file, ``False``
         otherwise.

        :rtype: `string`
        """

        stream = StringIO()
        
        method = self.xml_item
        name = method.name or method.pyName
        name = RemoveWxPrefix(name)

        if self.is_overload:
            definition = '**%s** '%name
        else:
            if method.isStatic:
                definition = '   .. staticmethod:: ' + name
            else:
                definition = '   .. method:: ' + name
                
        # write the method declaration
        stream.write('\n%s'%definition)
            
        stream.write(self.arguments)
        stream.write('\n\n')

        self.Reformat(stream)

        possible_py = self.HuntContributedSnippets()
        
        if possible_py:
            possible_py.sort()
            snippets = FormatContributedSnippets(self.kind, possible_py)
            stream.write(snippets)

        stream.write("\n\n")

        if not self.is_overload and write:
            WriteSphinxOutput(stream, self.output_file, append=True)

        return stream.getvalue()


    # -----------------------------------------------------------------------

    def DumpFunction(self, write):
        """
        Dumps a ReSTified function description and returns its correct ReST representation.

        :param bool `write`: ``True`` to write the resulting docstrings to a file, ``False``
         otherwise.

        :rtype: `string`
        """

        stream = StringIO()
        
        function = self.xml_item
        name = function.pyName or function.name

        if self.is_overload:
            definition = '**%s** '%name
        else:
            definition = '.. function:: ' + name

        stream.write('\n%s'%definition)
                    
        stream.write(self.arguments.strip())
        stream.write('\n\n')                    

        self.Reformat(stream)

        possible_py = self.HuntContributedSnippets()
        
        if possible_py:
            possible_py.sort()
            snippets = FormatContributedSnippets(self.kind, possible_py)
            stream.write(snippets)

        if not self.is_overload and write:        
            PickleItem(stream.getvalue(), self.current_module, name, 'function')

        return stream.getvalue()


    # -----------------------------------------------------------------------

    def DumpEnum(self, write):
        """
        Dumps a ReSTified enumeration description and returns its correct ReST representation.

        :param bool `write`: ``True`` to write the resulting docstrings to a file, ``False``
         otherwise.

        :rtype: `string`
        """

        enum_name, fullname = Wx2Sphinx(self.xml_item.name)

        if '@' in enum_name:
            return
        
        stream = StringIO()
        self.output_file = self.current_module + "%s.enumeration.txt"%enum_name
        
        stream.write(templates.TEMPLATE_DESCRIPTION % (fullname, enum_name))
        stream.write('\n\nThe `%s` enumeration provides the following values:\n\n'%enum_name)
        
        stream.write('\n\n' + '='*80 + ' ' + '='*80 + '\n')
        stream.write('%-80s **Value**\n'%'**Description**')
        stream.write('='*80 + ' ' + '='*80 + '\n')

        count = 0
        
        for v in self.xml_item.items:
            if v.ignored:
                continue

            docstrings = v.briefDoc
            name = ConvertToPython(RemoveWxPrefix(v.name))
            stream.write('%-80s'%name)
            
            if not isinstance(docstrings, basestring):
                rest_class = self.RecurseXML(docstrings, self.root)
                docstrings = rest_class.Join()

            stream.write(' %s\n'%docstrings)
            count += 1

        stream.write('='*80 + ' ' + '='*80 + '\n\n|\n\n')

        text_file = os.path.join(SPHINXROOT, self.output_file)

        #if os.path.isfile(text_file):
        #    message = '\nWARNING: Duplicated description for `%s` enumeration.\n\n' \
        #              'The duplicated instance will still be written to its output ReST file but\n' \
        #              'Sphinx/Docutils will issue a warning when building the HTML docs.\n\n'
        #
        #    duplicated = self.output_file.replace('.enumeration.txt', '')
        #    print message % duplicated

        if count > 0 and write:
            WriteSphinxOutput(stream, self.output_file)

        return stream.getvalue()
    

    # -----------------------------------------------------------------------

    def EventsInStyle(self, line, class_name):

        docstrings = ''
        newline = line

        if 'supports the following styles:' in line:
            if class_name is not None:
                # Crappy wxWidgets docs!!! They put the Window Styles inside the
                # constructor!!!
                docstrings += templates.TEMPLATE_WINDOW_STYLES % class_name
                
        elif 'The following event handler macros' in line:
            last = line.index(':')
            line = line[last+1:].strip()

            if line.count(':') > 2:            
                newline = 'Handlers bound for the following event types will receive one of the %s parameters.'%line
            else:
                newline = 'Handlers bound for the following event types will receive a %s parameter.'%line
                
            docstrings += templates.TEMPLATE_EVENTS % class_name

        elif 'Event macros for events' in line:
            docstrings += templates.TEMPLATE_EVENTS % class_name

        elif 'following extra styles:' in line:
            docstrings += templates.TEMPLATE_WINDOW_EXTRASTYLES % class_name

        return docstrings, newline
        

    # -----------------------------------------------------------------------

    def CodeIndent(self, code, newlines):

        if len(code) < 72:
            newlines.append('    %s'%code)
            newlines.append('    ')
            return newlines

        start = code.index('(')
        wrapped = textwrap.wrap(code, width=72)  

        newcode = ''
        for indx, line in enumerate(wrapped):
            if indx == 0:
                newlines.append('    %s'%line)
            else:
                newlines.append(' '*(start+5) + line)

        newlines.append('    ')

        return newlines


    # -----------------------------------------------------------------------
    
    def Indent(self, class_name, item, spacer, docstrings):

        for line in item.splitlines():
            if line.strip():
                newdocs, newline = self.EventsInStyle(line, class_name) 
                docstrings += newdocs
                docstrings += spacer + newline + '\n'
            else:
                docstrings += line + '\n'
        
        return docstrings
    

    # -----------------------------------------------------------------------
        
    def Reformat(self, stream):

        spacer = ''

        if not self.is_overload:
            if self.kind == 'function':
                spacer = 3*' '
            elif self.kind == 'method':
                spacer = 6*' '

        if self.overloads and not self.share_docstrings:

            docstrings = ''

        elif self.is_overload and self.share_docstrings:
            
            docstrings = self.Indent(None, self.docstrings, spacer, u'')

        else:

            class_name = None

            if self.kind == 'class':
                class_name = self.class_name

            if isinstance(self.xml_item, (extractors.PyFunctionDef, extractors.PyClassDef)):
                docstrings = self.xml_item.briefDoc
                if docstrings:
                    docstrings = self.Indent(class_name, docstrings, spacer, u'')
                else:
                    docstrings = ''
            else:
                docstrings = self.Indent(class_name, self.docstrings, spacer, u'')
            
            if self.kind == 'class':
                desc = ChopDescription(docstrings)
                class_name = self.class_name.lower()
                PickleItem(desc, self.current_module, self.class_name, 'class')
                        
        if self.overloads:

            docstrings += '\n\n%s|overload| **Overloaded Implementations**:\n\n'%spacer
            docstrings += '%s**~~~**\n\n'%spacer

            for index, over in enumerate(self.overloads):
                for line in over.splitlines():
                    docstrings += spacer + line + '\n'

                docstrings += '%s**~~~**\n\n'%spacer
                                                        
        stream.write(docstrings + "\n\n")
            
    
# ---------------------------------------------------------------------------

class SphinxGenerator(generators.DocsGeneratorBase):
        
    def generate(self, module):

        self.current_module = MODULENAME_REPLACE[module.module]
        self.module_name = module.name
        self.current_class = None

        self.generateModule(module)

    # -----------------------------------------------------------------------

    def RemoveDuplicated(self, class_name, class_items):

        duplicated_indexes = []
        done = []

        properties = (extractors.PropertyDef, extractors.PyPropertyDef)
        methods = (extractors.MethodDef, extractors.CppMethodDef, extractors.CppMethodDef_sip,
                   extractors.PyMethodDef, extractors.PyFunctionDef)

        message = '\nWARNING: Duplicated instance of %s `%s` encountered in class `%s`.\n' \
                  'The last occurrence of `%s` (an instance of `%s`) will be discarded.\n\n'
        
        for index, item in enumerate(class_items):
            if isinstance(item, methods):
                name, dummy = self.getName(item)
                kind = 'method'
            elif isinstance(item, properties):
                name = item.name
                kind = 'property'
            else:
                continue

            if name in done:
                print message % (kind, name, class_name, name, item.__class__.__name__)
                duplicated_indexes.append(index)
                continue

            done.append(name)            

        duplicated_indexes.reverse()                
        for index in duplicated_indexes:
            class_items.pop(index)

        return class_items                

                
    # -----------------------------------------------------------------------
    
    def generateModule(self, module):
        """
        Generate code for each of the top-level items in the module.
        """
        assert isinstance(module, extractors.ModuleDef)
        
        methodMap = {
            extractors.ClassDef         : self.generateClass,
            extractors.DefineDef        : self.generateDefine,
            extractors.FunctionDef      : self.generateFunction,
            extractors.EnumDef          : self.generateEnum,
            extractors.GlobalVarDef     : self.generateGlobalVar,
            extractors.TypedefDef       : self.generateTypedef,
            extractors.WigCode          : self.generateWigCode,
            extractors.PyCodeDef        : self.generatePyCode,
            extractors.CppMethodDef     : self.generateFunction,
            extractors.CppMethodDef_sip : self.generateFunction,
            extractors.PyFunctionDef    : self.generatePyFunction,
            extractors.PyClassDef       : self.generatePyClass,
            }
        
        for item in module:
            if item.ignored:
                continue

            function = methodMap[item.__class__]
            function(item)


    # -----------------------------------------------------------------------
            
    def generatePyFunction(self, function):

        function.overloads = []
        function.pyArgsString = function.argsString
        # docstring
        docstring = XMLDocString(function)
        docstring.kind = 'function'
        docstring.current_module = self.current_module

        docstring.Dump()

        
    # -----------------------------------------------------------------------
        
    def generateFunction(self, function):
        
        # docstring
        docstring = XMLDocString(function)
        docstring.kind = 'function'
        docstring.current_module = self.current_module

        docstring.Dump()
                        
                
    # -----------------------------------------------------------------------
        
    def generatePyClass(self, klass):

        klass.module = self.current_module
        self.current_class = klass

        name = klass.name
        self.current_class.method_list = []
        self.current_class.property_list = []

        class_items = [i for i in klass if not i.ignored]
        class_items = sorted(class_items, key=operator.attrgetter('name'))

        class_items = self.RemoveDuplicated(name, class_items)

        init_position = -1
        
        for index, item in enumerate(class_items):
            if isinstance(item, extractors.PyFunctionDef):
                method_name, simple_docs = self.getName(item)
                if method_name == '__init__':
                    init_position = index
                    self.current_class.method_list.insert(0, (method_name, simple_docs))
                else:
                    self.current_class.method_list.append((method_name, simple_docs))
            elif isinstance(item, extractors.PyPropertyDef):
                simple_docs = self.createPropertyLinks(name, item)
                self.current_class.property_list.append((item.name, simple_docs))

        PickleClassInfo(self.current_module + name, self.current_class)

        if init_position >= 0:
            init_method = class_items.pop(init_position)
            class_items.insert(0, init_method)

        docstring = XMLDocString(klass)
        docstring.kind = 'class'

        filename = self.current_module + "%s.txt"%name
        docstring.output_file = filename
        docstring.current_module = self.current_module

        docstring.Dump()

        # these are the only kinds of items allowed to be items in a PyClass
        dispatch = {
            extractors.PyFunctionDef    : self.generateMethod,
            extractors.PyPropertyDef    : self.generatePyProperty,
            extractors.PyCodeDef        : self.generatePyCode,
            extractors.PyClassDef       : self.generatePyClass,
        }

        for item in class_items:
            item.klass = klass                
            f = dispatch[item.__class__]
            f(item)


    # -----------------------------------------------------------------------

    def generatePyProperty(self, prop):

        name = RemoveWxPrefix(self.current_class.name) or self.current_class.pyName
        getter_setter = self.createPropertyLinks(name, prop)

        stream = StringIO()
        stream.write('\n   .. attribute:: %s\n\n' % prop.name)
        stream.write('      %s\n\n'%getter_setter)

        filename = self.current_module + "%s.txt"%name

        WriteSphinxOutput(stream, filename, append=True)
    
    # -----------------------------------------------------------------------
        
    def generateClass(self, klass):

        assert isinstance(klass, extractors.ClassDef)
                
        if klass.ignored:
            return

        # generate nested classes
        for item in klass.innerclasses:
            self.generateClass(item)

        name = RemoveWxPrefix(klass.name) or klass.pyName

##        # Hack for App/PyApp...
##        if name == 'PyApp':
##            klass.name = name = 'App'

        klass.module = self.current_module
        self.current_class = klass

        self.current_class.method_list = []
        self.current_class.property_list = []
        
        #   Inspected class               Method to call           Sort order
        dispatch = {
            extractors.MethodDef        : (self.generateMethod,     1),
            extractors.CppMethodDef     : (self.generateMethod,     1),
            extractors.CppMethodDef_sip : (self.generateMethod,     1),
            extractors.PyMethodDef      : (self.generatePyMethod,   1),
            extractors.MemberVarDef     : (self.generateMemberVar,  2),
            extractors.PropertyDef      : (self.generateProperty,   2),
            extractors.PyPropertyDef    : (self.generateProperty,   2),
            extractors.EnumDef          : (self.generateEnum,       0),
            extractors.PyCodeDef        : (self.generatePyCode,     3),
            extractors.WigCode          : (self.generateWigCode,    4),
            }

        # Build a list to check if there are any properties
        properties = (extractors.PropertyDef, extractors.PyPropertyDef)
        methods = (extractors.MethodDef, extractors.CppMethodDef, extractors.CppMethodDef_sip, extractors.PyMethodDef)
        
        # Split the items documenting the __init__ methods first
        ctors = [i for i in klass if
                 isinstance(i, extractors.MethodDef) and
                 i.protection == 'public' and (i.isCtor or i.isDtor)]

        class_items = [i for i in klass if i not in ctors and not i.ignored]

        for item in class_items:
            item.sort_order = dispatch[item.__class__][1]

        class_items = sorted(class_items, key=operator.attrgetter('sort_order', 'name'))
        class_items = self.RemoveDuplicated(name, class_items)

        for item in class_items:
            if isinstance(item, methods) and not self.IsFullyDeprecated(item):
                method_name, simple_docs = self.getName(item)
                self.current_class.method_list.append((method_name, simple_docs))
            elif isinstance(item, properties):
                simple_docs = self.createPropertyLinks(name, item)
                self.current_class.property_list.append((item.name, simple_docs))

        for item in ctors: 
            if item.isCtor:
                method_name, simple_docs = self.getName(item)
                self.current_class.method_list.insert(0, ('__init__', simple_docs))

        PickleClassInfo(self.current_module + name, self.current_class)
                
        docstring = XMLDocString(klass)

        filename = self.current_module + "%s.txt"%name
        docstring.output_file = filename
        docstring.current_module = self.current_module

        docstring.Dump()
        
        for item in ctors: 
            if item.isCtor:
                self.generateMethod(item, name='__init__', docstring=klass.pyDocstring)
        
        for item in class_items:
            f = dispatch[item.__class__][0]
            f(item)
        
    # -----------------------------------------------------------------------
        
    def generateMethod(self, method, name=None, docstring=None):

        if method.ignored:
            return

        name = name or self.getName(method)[0]
##        if name.startswith("__") and "__init__" not in name:
##            return

        class_name = RemoveWxPrefix(self.current_class.name) or self.current_class.pyName
            
        # docstring
        method.name = name
        method.pyArgsString = method.pyArgsString.replace('(self)', ' ').replace('(self, ', ' ')
        docstring = XMLDocString(method)
        docstring.kind = 'method'

        name = RemoveWxPrefix(self.current_class.name) or self.current_class.pyName
        filename = self.current_module + "%s.txt"%class_name

        docstring.output_file = filename
        docstring.class_name = class_name
        docstring.current_module = self.current_module

        docstring.Dump()
                
    # -----------------------------------------------------------------------

    def IsFullyDeprecated(self, pyMethod):

        if not isinstance(pyMethod, extractors.PyMethodDef):
            return False
        
        if pyMethod.deprecated:
            brief, detailed = pyMethod.briefDoc, pyMethod.detailedDoc
            if not brief and not detailed:
                # Skip simple wrappers unless they have a brief or a detailed doc
                return True

        return False            
        

    def generatePyMethod(self, pm):

        assert isinstance(pm, extractors.PyMethodDef)

        if pm.ignored:
            return

        if self.IsFullyDeprecated(pm):
            return
        
        stream = StringIO()
        stream.write('\n   .. method:: %s%s\n\n' % (pm.name, pm.argsString))

##        docstrings = ConvertToPython(pm.pyDocstring).replace('\n', ' ')
        docstrings = ConvertToPython(pm.pyDocstring)

        newdocs = ''
        spacer = ' '*6
        
        for line in docstrings.splitlines():
            if not line.startswith(spacer):
                newdocs += spacer + line + "\n"
            else:
                newdocs += line + "\n"
                
        stream.write(newdocs + '\n\n')

        name = RemoveWxPrefix(self.current_class.name) or self.current_class.pyName
        filename = self.current_module + "%s.txt"%name

        WriteSphinxOutput(stream, filename, append=True)
           
    # -----------------------------------------------------------------------

    def generateMemberVar(self, memberVar):
        assert isinstance(memberVar, extractors.MemberVarDef)
        if memberVar.ignored:
            return

    # -----------------------------------------------------------------------

    def generateProperty(self, prop):

        if prop.ignored:
            return

        name = RemoveWxPrefix(self.current_class.name) or self.current_class.pyName

        getter_setter = self.createPropertyLinks(name, prop)

        stream = StringIO()
        stream.write('\n   .. attribute:: %s\n\n' % prop.name)
        stream.write('      %s\n\n'%getter_setter)

        filename = self.current_module + "%s.txt"%name

        WriteSphinxOutput(stream, filename, append=True)


    def createPropertyLinks(self, name, prop):

        if prop.getter and prop.setter:
            return 'See :meth:`~%s.%s` and :meth:`~%s.%s`'%(name, prop.getter, name, prop.setter)
        else:
            method = (prop.getter and [prop.getter] or [prop.setter])[0]            
            return 'See :meth:`~%s.%s`'%(name, method)
            

    # -----------------------------------------------------------------------
    def generateEnum(self, enum):
        
        assert isinstance(enum, extractors.EnumDef)
        if enum.ignored:
            return

        docstring = XMLDocString(enum)
        docstring.current_module = self.current_module

        docstring.Dump()


    # -----------------------------------------------------------------------
    def generateGlobalVar(self, globalVar):
        assert isinstance(globalVar, extractors.GlobalVarDef)
        if globalVar.ignored:
            return
        name = globalVar.pyName or globalVar.name
        if guessTypeInt(globalVar):
            valTyp = '0'
        elif guessTypeFloat(globalVar):
            valTyp = '0.0'
        elif guessTypeStr(globalVar):
            valTyp = '""'
        else:
            valTyp = RemoveWxPrefix(globalVar.type) + '()'

    # -----------------------------------------------------------------------
    def generateDefine(self, define):
        assert isinstance(define, extractors.DefineDef)
        # write nothing for this one
        
    # -----------------------------------------------------------------------
    def generateTypedef(self, typedef):
        assert isinstance(typedef, extractors.TypedefDef)
        # write nothing for this one

    # -----------------------------------------------------------------------
    def generateWigCode(self, wig):
        assert isinstance(wig, extractors.WigCode)
        # write nothing for this one
        
    # -----------------------------------------------------------------------
    def generatePyCode(self, pc):

        assert isinstance(pc, extractors.PyCodeDef)

    # -----------------------------------------------------------------------
    def getName(self, method):

        if hasattr(method, 'isCtor') and method.isCtor:
            method_name = '__init__'
        else:
            method_name = method.pyName or method.name
            if method_name in MAGIC_METHODS:
                method_name = MAGIC_METHODS[method_name]

        simple_docs = ''
        
        if isinstance(method, extractors.PyMethodDef):
            simple_docs = ConvertToPython(method.pyDocstring)
        else:
            brief = method.briefDoc
            if not isinstance(brief, basestring):
                docstring = XMLDocString(method)
                docstring.kind = 'method'
                docstring.current_module = self.current_module
                simple_docs = docstring.GetBrief()
            elif brief is not None:
                simple_docs = ConvertToPython(brief)

        simple_docs = ChopDescription(simple_docs)

        return method_name, simple_docs

        
# ---------------------------------------------------------------------------
# helpers

def guessTypeInt(v):
    if isinstance(v, extractors.EnumValueDef):
        return True
    if isinstance(v, extractors.DefineDef) and '"' not in v.value:
        return True
    type = v.type.replace('const', '')
    type = type.replace(' ', '')
    if type in ['int', 'long', 'byte', 'size_t']:
        return True
    if 'unsigned' in type:
        return True
    return False


def guessTypeFloat(v):
    type = v.type.replace('const', '')
    type = type.replace(' ', '')
    if type in ['float', 'double', 'wxDouble']:
        return True
    return False

def guessTypeStr(v):
    if hasattr(v, 'value') and '"' in v.value:
        return True
    if 'wxString' in v.type:
        return True
    return False

# ---------------------------------------------------------------------------
