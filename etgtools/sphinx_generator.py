# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Name:        etgtools/sphinx_generator.py
# Author:      Andrea Gavana
#
# Created:     30-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

"""
This generator will create the docstrings for Sphinx to process, by refactoring
the various XML elements passed by the Phoenix extractors into ReST format.
"""

# Standard library stuff
import os
import operator
import sys
import shutil
import textwrap

if sys.version_info < (3, ):
    from StringIO import StringIO
    string_base = basestring
else:
    from io import StringIO
    string_base = str

import xml.etree.ElementTree as et

# Phoenix-specific stuff
import etgtools.extractors as extractors
import etgtools.generators as generators
from etgtools.item_module_map import ItemModuleMap
from etgtools.tweaker_tools import removeWxPrefix

# Sphinx-Phoenix specific stuff
from sphinxtools.inheritance import InheritanceDiagram
from sphinxtools import templates

from sphinxtools.utilities import ODict
from sphinxtools.utilities import convertToPython
from sphinxtools.utilities import writeSphinxOutput
from sphinxtools.utilities import findControlImages, makeSummary, pickleItem
from sphinxtools.utilities import chopDescription, pythonizeType, wx2Sphinx
from sphinxtools.utilities import pickleClassInfo, pickleFunctionInfo, isNumeric
from sphinxtools.utilities import underscore2Capitals, countSpaces
from sphinxtools.utilities import formatContributedSnippets
from sphinxtools.utilities import PickleFile
from sphinxtools.utilities import textfile_open

from sphinxtools.constants import VERSION, REMOVED_LINKS, SECTIONS
from sphinxtools.constants import MAGIC_METHODS, MODULENAME_REPLACE
from sphinxtools.constants import IGNORE
from sphinxtools.constants import SPHINXROOT, DOXYROOT
from sphinxtools.constants import SNIPPETROOT, TABLEROOT, OVERVIEW_IMAGES_ROOT
from sphinxtools.constants import DOCSTRING_KEY


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

        if isinstance(self.element, string_base):
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

        dummy, class_name = wx2Sphinx(xml_docs.class_name)
        return class_name


    # -----------------------------------------------------------------------

    def Find(self, klass, node=None):
        """
        This method returns ``True`` if this node contains a specific class into its
        descendants.

        :param `klass`: can be any of the classes defined in this script except :class:`XMLDocString`.
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

        if isinstance(self.element, string_base):
            text = self.element
        else:
            text, tail = self.element.text, self.element.tail
            text = (text is not None and [text] or [''])[0]
            tail = (tail is not None and [tail] or [''])[0]

        for link in REMOVED_LINKS:
            if link in text.strip():
                return ''

        text = convertToPython(text)

        for child in self.children:
            text += child.Join(with_tail)

        if with_tail and tail:
            text += convertToPython(tail)

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

        self.sections = ODict()


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
        existing_sections = list(self.sections)

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
        self.py_parameters = ODict()

        for pdef in xml_item.items:
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

        if name in self.py_parameters:
            return self.py_parameters[name]

        if '_' in name:
            name = name[0:name.index('_')]
            if name in self.py_parameters:
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

        name = xml_item.pyName if xml_item.pyName else removeWxPrefix(xml_item.name)

        parent = self.GetTopLevelParent()
        is_overload = parent.is_overload if parent else False

        if xml_item.hasOverloads() and not is_overload:
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

        py_parameters = []
        for key, parameter in self.py_parameters.items():
            pdef = parameter.pdef
            if pdef.out or pdef.ignored or pdef.docsIgnored:
                continue

            py_parameters.append(key)

        message = '\nSEVERE: Incompatibility between function/method signature and list of parameters in `%s`:\n\n' \
                  'The parameter `%s` appears in the method signature but could not be found in the parameter list.\n\n' \
                  '  ==> Function/Method signature from `extractors`: %s\n' \
                  '  ==> Parameter list from wxWidgets XML items:     %s\n\n' \
                  'This may be a documentation bug in wxWidgets or a side-effect of removing the `wx` prefix from signatures.\n\n'

        theargs = []

        for arg in arguments:

            myarg = arg.split('=')[0].strip()
            if myarg:
                theargs.append(myarg)

            if '*' in arg or ')' in arg:
                continue

            arg = arg.split('=')[0].strip()

            if arg and arg not in py_parameters:

                class_name = ''
                if hasattr(xml_item, 'className') and xml_item.className is not None:
                    class_name = wx2Sphinx(xml_item.className)[1] + '.'

                print((message % (class_name + name, arg, signature, py_parameters)))

##        for param in py_parameters:
##            if param not in theargs:
##                class_name = ''
##                if hasattr(xml_item, 'className') and xml_item.className is not None:
##                    class_name = wx2Sphinx(xml_item.className)[1] + '.'
##
##                print '\n      |||  %s;%s;%s  |||\n'%(class_name[0:-1], signature, param)
##                with open('mismatched.txt', 'a') as fid:
##                    fid.write('%s;%s;%s\n'%(class_name[0:-1], signature, param))


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

        for name, parameter in list(self.py_parameters.items()):

            pdef = parameter.pdef

            if pdef.out or pdef.ignored or pdef.docsIgnored:
                continue

##            print name
##            print parameter.Join()
##            print
            if parameter.type.strip():
                docstrings += ':param `%s`: %s\n'%(name, parameter.Join().lstrip('\n'))
                docstrings += ':type `%s`: %s\n'%(name, parameter.type)
            else:
                docstrings += ':param `%s`: %s\n'%(name, parameter.Join().lstrip('\n'))


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

        self.type = pythonizeType(pdef.type, is_param=True)


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
                # TODO: Why is there sometimes not a top-level parent node?
                if root is not None:
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
            text = '%s%s\n'%(spacer, convertToPython(self.element.tail.strip()))
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

        dummy, section_type = list(self.element.items())[0]
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
            # Empty text or just trailing commas
            return ''

        if self.is_overload and self.share_docstrings:
            return ''

        sub_spacer = ' '*3

        if section_type == 'since':
            # Special treatment for the versionadded
            if len(text) > 6:
                version, remainder = text[0:6], text[6:]
                if '.' in version:
                    text = '%s\n%s%s'%(version, sub_spacer, remainder)
                else:
                    target = (' 2.' in text and [' 2.'] or [' 3.'])[0]
                    vindex1 = text.index(target)
                    vindex2 = text[vindex1+2:].index(' ') + vindex1 + 2
                    version = text[vindex1:vindex2].strip()
                    if version.endswith('.'):
                        version = version[0:-1]
                    text = '%s\n%s%s'%(version, sub_spacer, text)

                # Show both the wxPython and the wxWidgets version numbers for
                # versions >= 3. That's not entirely accurate, but close enough.
                if text.startswith('3.'):
                    wx_ver = text[:5]
                    text = '4.{}/wxWidgets-{} {}'.format(wx_ver[2], wx_ver, text[5:])

        elif section_type == 'deprecated':
            # Special treatment for deprecated, wxWidgets devs do not put the version number
            text = '\n%s%s'%(sub_spacer, text.lstrip('Deprecated'))

        elif section_type == 'par':
            # Horrible hack... Why is there a </para> end tag inside the @par tag???
            text = Node.Join(self, with_tail=True)
            split = text.split('\n')
            current = 0
            for index, line in enumerate(split):
                if '---' in line:
                    current = index-1
                    break

            return '\n\n' + '\n'.join(split[current:]) + '\n\n'

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

        for key, value in list(self.element.items()):
            if key == 'name':
                break

        if 'appear-' in value:
            return ''

        image_path = os.path.normpath(os.path.join(DOXYROOT, 'images', value))
        static_path = os.path.join(OVERVIEW_IMAGES_ROOT, os.path.split(image_path)[1])

        if not os.path.exists(image_path):
            return ''

        if not os.path.isfile(static_path):
            shutil.copyfile(image_path, static_path)

        rel_path_index = static_path.rfind('_static')
        rel_path = os.path.normpath(static_path[rel_path_index:])

        docstrings = '\n\n'
        docstrings += '.. figure:: %s\n' % rel_path
        docstrings += '   :align: center\n\n\n'
        docstrings += '|\n\n'

        if self.element.tail and self.element.tail.strip():
            docstrings += convertToPython(self.element.tail.rstrip())

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
           There are 4 customized versions of 4 XML tables up to now, for various
           reasons:

           1. The `wx.Sizer` flags table is a flexible grid table, very difficult
              to ReSTify automatically due to embedded newlines messing up the col
              width calculations.
           2. The `wx.ColourDatabase` table of colour comes up all messy when
              ReSTified from XML
           3. The "wxWidgets 2.8 Compatibility Functions" table for `wx.VScrolledWindow`
           4. The `wx.ArtProvider` IDs table

           The customized versions of those tables are located in
           ``docs/sphinx/rest_substitutions/tables``
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
        for row in range(rows):
            for col in range(cols):
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

        for row in range(rows):

            table += spacer

            for col in range(cols):
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
            # Work around for the buildbot sphinx generator which seems unable
            # to find the tables...
            rst_file = os.path.split(possible_rest_input)[1]
            rst_folder = os.path.normpath(os.path.relpath(TABLEROOT, SPHINXROOT))
            table = '\n\n' + spacer + '.. include:: %s\n\n'%os.path.join(rst_folder, rst_file)

        if self.element.tail and self.element.tail.strip():
            rest = convertToPython(self.element.tail.rstrip())
            split = rest.splitlines()
            for index, r in enumerate(split):
                table += spacer + r
                if index < len(split)-1:
                    table += '\n'

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

            if isinstance(element, string_base):
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

        if not os.path.exists(os.path.dirname(self.cpp_file)):
            os.makedirs(os.path.dirname(self.cpp_file))

        with open(self.cpp_file, 'wt') as fid:
            fid.write(self.snippet)

        if not os.path.isfile(self.converted_py):

            message = '\nWARNING: Missing C++ => Python conversion of the snippet of code for %s'%(os.path.split(self.cpp_file)[1])
            message += '\n\nA slightly Pythonized version of this snippet has been saved into:\n\n  ==> %s\n\n'%self.python_file

            print(message)

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

            with open(self.python_file, 'wt') as fid:
                fid.write(new_py_code)
        else:

            highlight = None

            with open(self.converted_py, 'rt') as fid:
                while True:
                    tline = fid.readline()

                    if not tline:  # end of file
                        code = ""
                        break

                    if 'code-block::' in tline:
                        highlight = tline.replace('#', '').strip()
                        continue

                    if not tline.strip():
                        continue

                    code = tline + fid.read()
                    break

            if highlight:
                docstrings += '\n\n%s\n\n'%highlight
            else:
                docstrings += '::\n\n'

            docstrings += code.rstrip() + '\n\n'

        if self.element.tail and len(self.element.tail.strip()) > 1:
            hierarchy = self.GetHierarchy()
            spacer = ''
            if 'Section' in hierarchy:
                spacer = ' '*3
            elif 'Parameter' in hierarchy:
                spacer = ' '
            elif 'List' in hierarchy:
                spacer = '  '

            tail = convertToPython(self.element.tail.lstrip())
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
        imm = ItemModuleMap()

        element = self.element
        text = element.text

        tail = element.tail
        tail = (tail is not None and [tail] or [''])[0]

        hascomma = '::' in text

        original = text
        text = removeWxPrefix(text)
        text = text.replace("::", ".")

        if "(" in text:
            text = text[0:text.index("(")]

        refid = element.get('refid', '')
        remainder = refid.split('_')[-1]
        values = [v for k,v in element.items()]

        space_before, space_after = countSpaces(text)
        stripped = text.strip()

        if stripped in IGNORE:
            return space_before + text + space_after + tail

        if ' ' in stripped or 'overview' in values:
            if 'classwx_' in refid:
                ref = 1000
                if '_1' in refid:
                    ref = refid.index('_1')

                ref = underscore2Capitals(refid[6:ref])
                ref = imm.get_fullname(ref)
                text = ':ref:`%s <%s>`'%(stripped, ref)

            elif 'funcmacro' in values or 'samples' in values or 'debugging' in text.lower() or \
                 'unix' in text.lower() or 'page_libs' in values:
                text = space_before + space_after
            elif 'library list' in stripped.lower():
                text = space_before + text + space_after
            else:
                backlink = stripped.lower()
                if 'device context' in backlink:
                    backlink = 'device contexts'
                elif 'reference count' in backlink or 'refcount' in values:
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

            elif not isNumeric(text):
                text = '``%s``'%text

        elif 'funcmacro' in values:
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

                    if stripped in imm:
                        text = ':ref:`%s`' % (imm.get_fullname(stripped))
                    else:
                        if '.' not in stripped:
                            klass = self.IsClassDescription()
                            if klass:
                                text = ':meth:`~%s.%s`' % (klass, stripped)
                            else:
                                text =  ':meth:`%s` ' % stripped
                        else:
                            scope, item_name = stripped.split('.', 1)
                            scope = wx2Sphinx(scope)[1]
                            text =  ':meth:`%s.%s` ' % (scope, item_name)

        else:
            text = ':ref:`%s`' % wx2Sphinx(stripped)[1]

        return space_before + text + space_after + convertToPython(tail)


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
            space_before, space_after = countSpaces(text)

            text = removeWxPrefix(text.strip())

        else:
            text = ''

        for child in self.children:
            text += child.Join(with_tail=False)

        if '`' not in text:
            text = "``%s`` "%text

        if self.element.tail:
            text += convertToPython(self.element.tail)

        space_before, space_after = countSpaces(text)
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


        text = Node.Join(self, with_tail=False)

        if '``' in text:
            format = '%s'
            emphasis = ''
        elif self.element.tag == 'emphasis':
            format = '`%s`'
            emphasys = '`'
        elif self.element.tag == 'bold':
            format = '**%s**'
            emphasys = '**'

        spacing = ('ParameterList' in self.GetHierarchy() and [' '] or [''])[0]

        if self.children:

            startPos = 0
            newText = spacing

            for child in self.children:
                childText = child.Join()

                tail = child.element.tail
                tail = (tail is not None and [tail] or [''])[0]

                if tail.strip() != ':':
                    childText = childText.replace(convertToPython(tail), '')

                fullChildText = child.Join()
                endPos = text.index(childText)

                if text[startPos:endPos].strip():
                    newText += ' ' + emphasys + text[startPos:endPos].strip() + emphasys + ' '
                else:
                    newText += ' ' + emphasys + ' '

                newText += childText + ' '
                remaining = fullChildText.replace(childText, '')
                if remaining.strip():
                    newText += emphasys + remaining.strip() + emphasys + ' '
                else:
                    newText += emphasys + ' '

                startPos = endPos

            text = newText

        else:

            if text.strip():
                text = spacing + format % text.strip()

        if self.element.tail:
            text += convertToPython(self.element.tail)

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

        if isinstance(self.parent, Section) and self.parent.section_type == 'par':
            # Sub-title in a @par doxygen tag
            text = convertToPython(self.element.text)
            underline = '-'
        else:
            # Normal big title
            text = '|phoenix_title| ' + convertToPython(self.element.text)
            underline = '='

        lentext = len(text)
        text = '\n\n%s\n%s\n\n'%(text.rstrip('.'), underline*lentext)

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

        dummy, link = list(self.element.items())[0]
        text = self.element.text

        text = '`%s <%s>`_'%(text, link)

        if self.element.tail:
            text += convertToPython(self.element.tail)

        return text


# ----------------------------------------------------------------------- #

class DashBase(Node):
    dash_text = '-'

    def Join(self, with_tail=True):
        text = self.dash_text
        if self.element.text:
            text += self.element.text
        if with_tail and self.element.tail:
            text += convertToPython(self.element.tail)
        return text


class EnDash(DashBase):
    dash_text = u'\u2013'

class EmDash(DashBase):
    dash_text = u'\u2014'


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
        elif isinstance(xml_item, (extractors.ClassDef, extractors.PyClassDef, extractors.TypedefDef)):
            self.kind = 'class'
            self.appearance = findControlImages(xml_item)
            self.class_name = xml_item.pyName if xml_item.pyName else removeWxPrefix(xml_item.name)
            self.isInner = getattr(xml_item, 'isInner', False)
        elif isinstance(xml_item, extractors.EnumDef):
            self.kind = 'enum'
        elif isinstance(xml_item, extractors.MemberVarDef):
            self.kind = 'memberVar'
        else:
            raise Exception('Unhandled docstring kind for %s'%xml_item.__class__.__name__)

        # Some of the Extractors (xml item) will set deprecated themselves, in which case it is set as a
        # non-empty string. In such cases, this branch will insert a deprecated section into the xml tree
        # so that the Node Tree (see classes above) will generate the deprecated  tag on their own in self.RecurseXML
        if hasattr(xml_item, 'deprecated') and xml_item.deprecated and isinstance(xml_item.deprecated, string_base):
            element = et.Element('deprecated', kind='deprecated')
            element.text = xml_item.deprecated

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

            if sub_item.ignored or sub_item.docsIgnored:
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

        snippet_count = 0
        for sub_item in [self.xml_item] + self.xml_item.overloads:

            if sub_item.ignored or sub_item.docsIgnored:
                continue

            sub_item.name = self.xml_item.pyName or removeWxPrefix(self.xml_item.name)
            docstring = XMLDocString(sub_item, is_overload=True, share_docstrings=share_docstrings)
            docstring.class_name = self.class_name
            docstring.current_module = self.current_module
            docstring.snippet_count = snippet_count

            docs = docstring.Dump()
            self.overloads.append(docs)
            snippet_count = docstring.snippet_count

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

        if isinstance(element, string_base):
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
                dummy, section_type = list(element.items())[0]
                section_type = section_type.split("_")[0]

                if element.tail and section_type != 'par':
                    Node(element.tail, parent)

                if section_type == 'par':
                    # doxygen @par stuff
                    rest_class = Section(element, parent, self.kind, self.is_overload, self.share_docstrings)
                    if element.tail:
                        Node(element.tail, rest_class)
                else:
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
            text = convertToPython(element.text)
            rest_class = Title(element, parent)

        elif tag == 'para':
            rest_class = Paragraph(element, parent, self.kind)

        elif tag == 'linebreak':
            spacer = ('ParameterList' in parent.GetHierarchy() and [' '] or [''])[0]
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

        elif tag == 'ndash':
            rest_class = EnDash(element, parent)
        elif tag == 'mdash':
            rest_class = EmDash(element, parent)

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

        imm = ItemModuleMap()

        if self.kind == 'class':
            klass = self.xml_item
            name = klass.pyName if klass.pyName else removeWxPrefix(klass.name)
            fullname = imm.get_fullname(name)

        elif self.kind == 'method':
            method = self.xml_item
            if hasattr(method, 'isCtor') and method.isCtor:
                method_name = '__init__'
            else:
                method_name = method.pyName if method.pyName else method.name

            if hasattr(method, 'className') and method.className is not None:
                klass = removeWxPrefix(method.className)
            else:
                klass = method.klass.pyName if method.klass.pyName else removeWxPrefix(method.klass.name)

            fullname = '%s.%s' % (imm.get_fullname(klass), method_name)

        elif self.kind == 'function':
            function = self.xml_item
            name = function.pyName if function.pyName else function.name
            fullname = self.current_module + 'functions.%s'%name

        if not fullname.strip():
            dummy = xml_item.name or xml_item.pyName
            raise Exception('Invalid item name for %s (kind=%s)'%(dummy, self.kind))

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

        possible_py = []

        for suffix in range(1, 101):

            sample = os.path.join(contrib_folder, '%s.%d.py'%(fullname, suffix))

            if not os.path.isfile(sample):
                break

            possible_py.append(sample)

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
        dummy, fullname = wx2Sphinx(name)

        # if '.' in fullname:
        #     module = self.current_module[:-1]
        #     stream.write('\n\n.. currentmodule:: %s\n\n' % module)

        stream.write(templates.TEMPLATE_DESCRIPTION % (fullname, fullname))

        self.Reformat(stream)

        inheritance_diagram = InheritanceDiagram(klass.nodeBases)
        png, map = inheritance_diagram.makeInheritanceDiagram()

        image_desc = templates.TEMPLATE_INHERITANCE % ('class', name, png, name, map)
        stream.write(image_desc)

        if self.appearance:
            appearance_desc = templates.TEMPLATE_APPEARANCE % tuple(self.appearance)
            stream.write(appearance_desc)

        if klass.subClasses:
            subs = [':ref:`%s`' % wx2Sphinx(cls)[1] for cls in klass.subClasses]
            subs = ', '.join(subs)
            subs_desc = templates.TEMPLATE_SUBCLASSES % subs
            stream.write(subs_desc)

        possible_py = self.HuntContributedSnippets()

        if possible_py:
            possible_py.sort()
            snippets = formatContributedSnippets(self.kind, possible_py)
            stream.write(snippets)

        if klass.method_list:
            summary = makeSummary(name, klass.method_list, templates.TEMPLATE_METHOD_SUMMARY, 'meth')
            stream.write(summary)

        if klass.property_list or klass.memberVar_list:
            allAttrs = klass.property_list + klass.memberVar_list
            summary = makeSummary(name, allAttrs, templates.TEMPLATE_PROPERTY_SUMMARY, 'attr')
            stream.write(summary)

        stream.write(templates.TEMPLATE_API)
        stream.write("\n.. class:: %s" % fullname)

        bases = klass.bases or ['object']

        if bases:
            stream.write('(')
            bases = [removeWxPrefix(b) for b in bases]  # ***
            stream.write(', '.join(bases))
            stream.write(')')

        stream.write('\n\n')

        py_docs = klass.pyDocstring

        if isinstance(self.xml_item, (extractors.PyClassDef, extractors.TypedefDef)):
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
                    newlines.append(convertToPython(line))

                if found:
                    line = line.replace('wx.EmptyString', '""')
                    line = line.replace('wx.', '')  # ***
                    newlines = self.CodeIndent(line, newlines)

        newdocs = ''
        for line in newlines:
            newdocs += ' '*3 + line + "\n"

        stream.write(newdocs + "\n\n")

        if write:
            writeSphinxOutput(stream, self.output_file)
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
            name = removeWxPrefix(name)

            if method.hasOverloads() and not self.is_overload:
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
            name = function.pyName if function.pyName else function.name
            name = removeWxPrefix(name)

            if function.hasOverloads() and not self.is_overload:
                arguments = '(*args, **kw)'
            else:
                if "->" in function.pyArgsString:
                    arguments, after = function.pyArgsString.split("->")
                    self.AddReturnType(after, name)
                else:
                    arguments = function.pyArgsString

            if self.is_overload:
                arguments = '`%s`'%arguments.strip()

        arguments = arguments.replace('wx.', '')
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

        if not self.xml_item.hasOverloads() or self.is_overload:
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
                stripped = ret.strip()
                imm = ItemModuleMap()
                if stripped in imm:
                    ret = imm[stripped] + stripped
                    new_section.append(':ref:`%s`' % ret)
                else:
                    if ret[0].isupper():
                        new_section.append(':ref:`%s`' % stripped)
                    else:
                        new_section.append('`%s`' % stripped)

            element = et.Element('return', kind='return')
            element.text = '( %s )'%(', '.join(new_section))

            return_section = Section(element, None, self.kind, self.is_overload, self.share_docstrings)
            self.root.AddSection(return_section)

        else:

            rtype = pythonizeType(after, is_param=False)

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
        name = method.pyName if method.pyName else method.name
        name = removeWxPrefix(name)

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
            snippets = formatContributedSnippets(self.kind, possible_py)
            stream.write(snippets)

        stream.write("\n\n")

        if not self.is_overload and write:
            writeSphinxOutput(stream, self.output_file, append=True)

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
        fullname = ItemModuleMap().get_fullname(name)

        if self.is_overload:
            definition = '**%s** ' % name
        else:
            definition = '.. function:: ' + fullname

        stream.write('\n%s' % definition)

        stream.write(self.arguments.strip())
        stream.write('\n\n')

        self.Reformat(stream)

        possible_py = self.HuntContributedSnippets()

        if possible_py:
            possible_py.sort()
            snippets = formatContributedSnippets(self.kind, possible_py)
            stream.write(snippets)

        if not self.is_overload and write:
            pickleItem(stream.getvalue(), self.current_module, name, 'function')

        return stream.getvalue()


    # -----------------------------------------------------------------------

    def DumpEnum(self, write):
        """
        Dumps a ReSTified enumeration description and returns its correct ReST representation.

        :param bool `write`: ``True`` to write the resulting docstrings to a file, ``False``
         otherwise.

        :rtype: `string`
        """

        enum_name, fullname = wx2Sphinx(self.xml_item.name)

        if '@' in enum_name:
            return

        if self.current_class:
            self.current_class.enum_list.append(fullname)

        stream = StringIO()
        self.output_file = "%s.enumeration.txt" % fullname

        # if self.current_module.strip():
        #     module = self.current_module.strip()[:-1]
        #     stream.write('\n\n.. currentmodule:: %s\n\n' % module)

        stream.write(templates.TEMPLATE_DESCRIPTION % (fullname, fullname))
        stream.write('\n\nThe `%s` enumeration provides the following values:\n\n' % enum_name)

        stream.write('\n\n' + '='*80 + ' ' + '='*80 + '\n')
        stream.write('%-80s **Value**\n'%'**Description**')
        stream.write('='*80 + ' ' + '='*80 + '\n')

        count = 0

        for v in self.xml_item.items:
            if v.ignored or v.docsIgnored:
                continue

            docstrings = v.briefDoc
            name = v.pyName if v.pyName else removeWxPrefix(v.name)
            name = convertToPython(name)
            stream.write('%-80s' % name)

            if not isinstance(docstrings, string_base):
                rest_class = self.RecurseXML(docstrings, self.root)
                docstrings = rest_class.Join()

            stream.write(' %s\n'%docstrings)
            count += 1

        stream.write('='*80 + ' ' + '='*80 + '\n\n|\n\n')

        text_file = os.path.join(SPHINXROOT, self.output_file)

        if count > 0 and write:
            writeSphinxOutput(stream, self.output_file)

        return stream.getvalue()


    # -----------------------------------------------------------------------

    def EventsInStyle(self, line, class_name, added):

        docstrings = ''
        newline = line

        if 'supports the following styles:' in line:
            if class_name is not None:
                # Crappy wxWidgets docs!!! They put the Window Styles inside the
                # constructor!!!
                docstrings += templates.TEMPLATE_WINDOW_STYLES % class_name

        elif 'The following event handler macros' in line and not added:
            index = line.index('The following event handler macros')
            newline1 = line[0:index] + '\n\n'
            macro_line = line[index:]
            last = macro_line.index(':')
            line = macro_line[last+1:].strip()

            if line.count(':') > 2:
                newline = 'Handlers bound for the following event types will receive one of the %s parameters.'%line
            else:
                newline = 'Handlers bound for the following event types will receive a %s parameter.'%line

            docstrings += newline1 + templates.TEMPLATE_EVENTS % class_name
            docstrings = docstrings.replace('Event macros for events emitted by this class: ', '')
            newline = newline.replace('Event macros for events emitted by this class: ', '')
            added = True

        elif 'Event macros for events' in line:
            if added:
                newline = ''
            else:
                docstrings += templates.TEMPLATE_EVENTS % class_name

            added = True

        elif 'following extra styles:' in line:
            docstrings += templates.TEMPLATE_WINDOW_EXTRASTYLES % class_name

        return docstrings, newline, added


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

        added = False
        for line in item.splitlines():
            if line.strip():
                newdocs, newline, added = self.EventsInStyle(line, class_name, added)
                if newline.strip():
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

            docstrings = self.Indent(None, self.docstrings, spacer, '')

        else:

            class_name = None

            if self.kind == 'class':
                class_name = self.class_name

            if isinstance(self.xml_item, (extractors.PyFunctionDef, extractors.PyClassDef)):
                docstrings = self.xml_item.briefDoc
                if docstrings:
                    docstrings = self.Indent(class_name, docstrings, spacer, '')
                else:
                    docstrings = ''
            else:
                docstrings = self.Indent(class_name, self.docstrings, spacer, '')

            if self.kind == 'class':
                desc = chopDescription(docstrings)
                self.short_description = desc
                pickleItem(desc, self.current_module, self.class_name, 'class')

        if self.overloads:
            docstrings += '\n\n%s|overload| Overloaded Implementations:\n\n'%spacer
            docstrings += '%s:html:`<hr class="overloadsep" /><br />`\n\n'%spacer

            for index, over in enumerate(self.overloads):
                for line in over.splitlines():
                    docstrings += spacer + line + '\n'
                docstrings += '%s:html:`<hr class="overloadsep" /><br />`\n\n'%spacer

        if '**Perl Note:**' in docstrings:
            index = docstrings.index('**Perl Note:**')
            docstrings = docstrings[0:index]

        stream.write(docstrings + "\n\n")

# ---------------------------------------------------------------------------

class SphinxGenerator(generators.DocsGeneratorBase):

    def generate(self, module):
        self.current_module = MODULENAME_REPLACE[module.module]
        self.module_name = module.name
        self.current_class = None

        self.generateModule(module)

    # -----------------------------------------------------------------------

    def removeDuplicated(self, class_name, class_items):

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
                print((message % (kind, name, class_name, name, item.__class__.__name__)))
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

        if module.isARealModule:
            filename = os.path.join(SPHINXROOT, self.current_module+'1moduleindex.pkl')
            with PickleFile(filename) as pf:
                pf.items[DOCSTRING_KEY] = module.docstring

        for item in module:
            if item.ignored or item.docsIgnored:
                continue

            function = methodMap[item.__class__]
            function(item)


    # -----------------------------------------------------------------------

    def generatePyFunction(self, function):
        name = function.pyName if function.pyName else removeWxPrefix(function.name)
        imm = ItemModuleMap()
        fullname = imm.get_fullname(name)

        function.overloads = []
        function.pyArgsString = function.argsString

        self.unIndent(function)

        # docstring
        docstring = XMLDocString(function)
        docstring.kind = 'function'
        docstring.current_module = self.current_module
        docstring.Dump()

        desc = chopDescription(docstring.docstrings)
        pickleFunctionInfo(fullname, desc)

    # -----------------------------------------------------------------------

    def generateFunction(self, function):
        name = function.pyName if function.pyName else removeWxPrefix(function.name)
        if name.startswith('operator'):
            return

        imm = ItemModuleMap()
        fullname = imm.get_fullname(name)

        # docstring
        docstring = XMLDocString(function)
        docstring.kind = 'function'
        docstring.current_module = self.current_module
        docstring.Dump()

        desc = chopDescription(docstring.docstrings)
        pickleFunctionInfo(fullname, desc)


    def unIndent(self, item):

        if not item.briefDoc:
            return

        newdocs = ''
        for line in item.briefDoc.splitlines():
            if line.strip():
                stripped = len(line) - len(line.lstrip())
                break

        newdocs = ''
        for line in item.briefDoc.splitlines():
            if line.strip():
                line = line[stripped:]

            newdocs += line + '\n'

        item.briefDoc = newdocs


    # -----------------------------------------------------------------------

    def generatePyClass(self, klass):

        self.fixNodeBaseNames(klass, ItemModuleMap())

        klass.module = self.current_module
        self.current_class = klass

        class_name = klass.name
        class_fullname = ItemModuleMap().get_fullname(class_name)
        self.current_class.method_list = []
        self.current_class.property_list = []
        self.current_class.memberVar_list = []

        class_items = [i for i in klass if not (i.ignored or i.docsIgnored)]
        class_items = sorted(class_items, key=operator.attrgetter('name'))

        class_items = self.removeDuplicated(class_fullname, class_items)

        init_position = -1

        for index, item in enumerate(class_items):
            if isinstance(item, extractors.PyFunctionDef):
                method_name, simple_docs = self.getName(item)
                if method_name == '__init__':
                    init_position = index
                    self.current_class.method_list.insert(0, ('%s.%s'%(class_fullname, method_name), simple_docs))
                else:
                    self.current_class.method_list.append(('%s.%s'%(class_fullname, method_name), simple_docs))
            elif isinstance(item, extractors.PyPropertyDef):
                simple_docs = self.createPropertyLinks(class_fullname, item)
                self.current_class.property_list.append(('%s.%s'%(class_fullname, item.name), simple_docs))

        if init_position >= 0:
            init_method = class_items.pop(init_position)
            class_items.insert(0, init_method)

        self.unIndent(klass)

        docstring = XMLDocString(klass)
        docstring.kind = 'class'

        filename = "%s.txt" % class_fullname
        docstring.output_file = filename
        docstring.current_module = self.current_module

        docstring.Dump()

        pickleClassInfo(class_fullname, self.current_class, docstring.short_description)

        # these are the only kinds of items allowed to be items in a PyClass
        dispatch = [(extractors.PyFunctionDef, self.generateMethod),
                    (extractors.PyPropertyDef, self.generatePyProperty),
                    (extractors.PyCodeDef,     self.generatePyCode),
                    (extractors.PyClassDef,    self.generatePyClass)]

        for kind, function in dispatch:
            for item in class_items:
                if kind == item.__class__:
                    item.klass = klass
                    function(item)


    # -----------------------------------------------------------------------

    def generatePyProperty(self, prop):

        c = self.current_class
        name = c.pyName if c.pyName else removeWxPrefix(c.name)
        fullname = ItemModuleMap().get_fullname(name)
        getter_setter = self.createPropertyLinks(fullname, prop)

        stream = StringIO()
        stream.write('\n   .. attribute:: %s\n\n' % prop.name)
        stream.write('      %s\n\n'%getter_setter)

        filename = "%s.txt" % fullname

        writeSphinxOutput(stream, filename, append=True)

    # -----------------------------------------------------------------------
    def generateClass(self, klass):

        assert isinstance(klass, extractors.ClassDef)

        if klass.ignored or klass.docsIgnored:
            return

        imm = ItemModuleMap()

        self.fixNodeBaseNames(klass, imm)

        # generate nested classes
        for item in klass.innerclasses:
            self.generateClass(item)

        name = klass.pyName if klass.pyName else removeWxPrefix(klass.name)
        fullname = imm.get_fullname(name)

        klass.module = self.current_module
        self.current_class = klass

        klass.method_list = []
        klass.property_list = []
        klass.memberVar_list = []
        klass.enum_list = []

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
            extractors.TypedefDef       : (lambda a: None,          5),
            }

        # Build a list to check if there are any properties
        properties = (extractors.PropertyDef, extractors.PyPropertyDef)
        methods = (extractors.MethodDef, extractors.CppMethodDef, extractors.CppMethodDef_sip, extractors.PyMethodDef)

        # Split the items documenting the __init__ methods first
        ctors = [i for i in klass if
                 isinstance(i, extractors.MethodDef) and
                 i.protection == 'public' and (i.isCtor or i.isDtor)]

        class_items = [i for i in klass if i not in ctors and not (i.ignored or i.docsIgnored)]

        for item in class_items:
            item.sort_order = dispatch[item.__class__][1]

        class_items = sorted(class_items, key=operator.attrgetter('sort_order', 'name'))
        class_items = self.removeDuplicated(fullname, class_items)

        for item in class_items:
            if isinstance(item, methods) and not self.IsFullyDeprecated(item):
                method_name, simple_docs = self.getName(item)
                klass.method_list.append(('%s.%s' % (fullname, method_name), simple_docs))
            elif isinstance(item, properties):
                simple_docs = self.createPropertyLinks(fullname, item)
                klass.property_list.append(('%s.%s' % (fullname, item.name), simple_docs))
            elif isinstance(item, extractors.MemberVarDef):
                description = self.createMemberVarDescription(item)
                klass.memberVar_list.append(('%s.%s' % (fullname, item.name), description))

        for item in ctors:
            if item.isCtor:
                method_name, simple_docs = self.getName(item)
                klass.method_list.insert(0, ('%s.__init__'%fullname, simple_docs))

        docstring = XMLDocString(klass)

        filename = "%s.txt" % fullname
        docstring.output_file = filename
        docstring.current_module = self.current_module

        docstring.Dump()

        pickleClassInfo(fullname, self.current_class, docstring.short_description)

        for item in ctors:
            if item.isCtor:
                self.generateMethod(item, name='__init__', docstring=klass.pyDocstring)

        for item in class_items:
            f = dispatch[item.__class__][0]
            f(item)

        if klass.postProcessReST is not None:
            full_name = os.path.join(SPHINXROOT, filename)
            with textfile_open(full_name) as f:
                text = f.read()
            text = klass.postProcessReST(text)
            with textfile_open(full_name, 'wt') as f:
                f.write(text)

        if klass.enum_list:
            stream = StringIO()
            stream.write("\n.. toctree::\n   :maxdepth: 1\n   :hidden:\n\n")
            for enum_name in klass.enum_list:
                stream.write("   {}.enumeration\n".format(enum_name))
            writeSphinxOutput(stream, filename, True)


    # -----------------------------------------------------------------------

    def fixNodeBaseNames(self, klass, imm):
        # convert the names in nodeBases to fullnames
        def _fix(name):
            return imm.get_fullname(removeWxPrefix(name))

        if not klass.nodeBases:
            name = klass.pyName if klass.pyName else klass.name
            name = _fix(name)
            klass.nodeBases = ([(name, [])], [name])
            return

        bases, specials = klass.nodeBases
        bases = list(bases.values())
        specials = [_fix(s) for s in specials]
        for idx, (name, baselist) in enumerate(bases):
            name = _fix(name)
            baselist = [_fix(b) for b in baselist]
            bases[idx] = (name, baselist)
        klass.nodeBases = (bases, specials)

    # -----------------------------------------------------------------------

    def generateMethod(self, method, name=None, docstring=None):

        if method.ignored or method.docsIgnored:
            return

        name = name or self.getName(method)[0]
##        if name.startswith("__") and "__init__" not in name:
##            return

        if isinstance(method, extractors.PyFunctionDef):
            self.unIndent(method)

        imm = ItemModuleMap()
        c = self.current_class
        class_name = c.pyName if c.pyName else removeWxPrefix(c.name)
        fullname = imm.get_fullname(class_name)

        # docstring
        method.name = name
        method.pyArgsString = method.pyArgsString.replace('(self)', ' ').replace('(self, ', ' ')
        docstring = XMLDocString(method)
        docstring.kind = 'method'

        filename = "%s.txt" % fullname

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

        if pm.ignored or pm.docsIgnored:
            return

        if self.IsFullyDeprecated(pm):
            return

        stream = StringIO()
        stream.write('\n   .. method:: %s%s\n\n' % (pm.name, pm.argsString))

        docstrings = return_type = ''

        for line in pm.pyDocstring.splitlines():
            if '->' in line:
                arguments, after = line.strip().split("->")
                return_type = self.returnSection(after)
            else:
                docstrings += line + '\n'

        docstrings = convertToPython(docstrings)

        newdocs = ''
        spacer = ' '*6

        for line in docstrings.splitlines():
            if not line.startswith(spacer):
                newdocs += spacer + line + "\n"
            else:
                newdocs += line + "\n"

        stream.write(newdocs + '\n\n')

        c = self.current_class
        name = c.pyName if c.pyName else removeWxPrefix(c.name)
        imm = ItemModuleMap()
        filename = "%s.txt" % imm.get_fullname(name)

        writeSphinxOutput(stream, filename, append=True)

    # -----------------------------------------------------------------------

    def generateMemberVar(self, memberVar):
        assert isinstance(memberVar, extractors.MemberVarDef)
        if memberVar.ignored or memberVar.docsIgnored or memberVar.protection != 'public':
            return

        c = self.current_class
        name = c.pyName if c.pyName else removeWxPrefix(c.name)
        fullname = ItemModuleMap().get_fullname(name)

        description = self.createMemberVarDescription(memberVar)

        stream = StringIO()
        stream.write('\n   .. attribute:: %s\n\n' % memberVar.name)
        stream.write('      %s\n\n' % description)

        filename = "%s.txt" % fullname
        writeSphinxOutput(stream, filename, append=True)


    def createMemberVarDescription(self, memberVar):
        varType = pythonizeType(memberVar.type, False)
        if varType.startswith('wx.'):
            varType = ':ref:`~%s`' % varType
        else:
            varType = '``%s``' % varType

        description = 'A public C++ attribute of type %s.' % varType

        brief = memberVar.briefDoc
        briefDoc = None
        if not isinstance(brief, string_base):
            docstring = XMLDocString(memberVar)
            #docstring.current_module = self.current_module
            briefDoc = docstring.GetBrief()
        elif brief is not None:
            briefDoc = convertToPython(brief)

        if briefDoc:
            description += ' ' + briefDoc

        return description


    # -----------------------------------------------------------------------

    def generateProperty(self, prop):

        if prop.ignored or prop.docsIgnored:
            return

        c = self.current_class
        name = c.pyName if c.pyName else removeWxPrefix(c.name)
        fullname = ItemModuleMap().get_fullname(name)

        getter_setter = self.createPropertyLinks(fullname, prop)

        stream = StringIO()
        stream.write('\n   .. attribute:: %s\n\n' % prop.name)
        stream.write('      %s\n\n' % getter_setter)

        filename = "%s.txt" % fullname
        writeSphinxOutput(stream, filename, append=True)


    def createPropertyLinks(self, name, prop):

        if prop.getter and prop.setter:
            return 'See :meth:`~%s.%s` and :meth:`~%s.%s`' % (name, prop.getter, name, prop.setter)
        else:
            method = (prop.getter and [prop.getter] or [prop.setter])[0]
            return 'See :meth:`~%s.%s`' % (name, method)


    # -----------------------------------------------------------------------
    def generateEnum(self, enum):

        assert isinstance(enum, extractors.EnumDef)
        if enum.ignored or enum.docsIgnored:
            return

        docstring = XMLDocString(enum)
        docstring.current_module = self.current_module
        docstring.current_class = self.current_class if hasattr(self, 'current_class') else None

        docstring.Dump()


    # -----------------------------------------------------------------------
    def generateGlobalVar(self, globalVar):
        assert isinstance(globalVar, extractors.GlobalVarDef)
        if globalVar.ignored or globalVar.docsIgnored:
            return
        name = globalVar.pyName or globalVar.name
        if guessTypeInt(globalVar):
            valTyp = '0'
        elif guessTypeFloat(globalVar):
            valTyp = '0.0'
        elif guessTypeStr(globalVar):
            valTyp = '""'
        else:
            valTyp = removeWxPrefix(globalVar.type) + '()'

    # -----------------------------------------------------------------------
    def generateDefine(self, define):
        assert isinstance(define, extractors.DefineDef)
        # write nothing for this one

    # -----------------------------------------------------------------------
    def generateTypedef(self, typedef):
        assert isinstance(typedef, extractors.TypedefDef)

        if typedef.ignored or typedef.docsIgnored or not typedef.docAsClass:
            return

        name = typedef.pyName if typedef.pyName else removeWxPrefix(typedef.name)
        typedef.module = self.current_module

        all_classes = {}
        fullname = name
        specials = [fullname]

        baselist = [base for base in typedef.bases if base != 'object']
        all_classes[fullname] = (fullname, baselist)

        for base in baselist:
            all_classes[base] = (base, [])

        self.unIndent(typedef)

        typedef.nodeBases = all_classes, specials
        self.fixNodeBaseNames(typedef, ItemModuleMap())
        typedef.subClasses = []
        typedef.method_list = []
        typedef.property_list = []
        typedef.memberVar_list = []
        typedef.pyDocstring = typedef.briefDoc

        self.current_class = typedef

        docstring = XMLDocString(typedef)
        docstring.kind = 'class'

        filename = self.current_module + "%s.txt"%name
        docstring.output_file = filename
        docstring.current_module = self.current_module

        docstring.Dump()

        pickleClassInfo(self.current_module + name, self.current_class, docstring.short_description)


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
            simple_docs = convertToPython(method.pyDocstring)
        else:
            brief = method.briefDoc
            if not isinstance(brief, string_base):
                docstring = XMLDocString(method)
                docstring.kind = 'method'
                docstring.current_module = self.current_module
                simple_docs = docstring.GetBrief()
            elif brief is not None:
                simple_docs = convertToPython(brief)

        simple_docs = chopDescription(simple_docs)

        return method_name, simple_docs

    # ---------------------------------------------------------------------------
    def returnSection(self, after):

        if '(' in after:

            rtype1 = ReturnType('`tuple`', None)

            return_section = after.strip().lstrip('(').rstrip(')')
            return_section = return_section.split(',')
            new_section = []

            for ret in return_section:
                stripped = ret.strip()
                imm = ItemModuleMap()
                if stripped in imm:
                    ret = imm[stripped] + stripped
                    new_section.append(':ref:`%s`'%ret)
                else:
                    if ret[0].isupper():
                        new_section.append(':ref:`%s`'%stripped)
                    else:
                        new_section.append('`%s`'%stripped)

            element = et.Element('return', kind='return')
            element.text = '( %s )'%(', '.join(new_section))

            rtype2 = Section(element, None, 'method')
            rtype = rtype1.Join() + rtype2.Join()

        else:

            rtype = pythonizeType(after, is_param=False)

            if not rtype:
                return ''

            if rtype[0].isupper() or '.' in rtype:
                rtype = ':ref:`%s`'%rtype
            else:
                rtype = '`%s`'%rtype

            rtype = ReturnType(rtype, None)
            rtype = rtype.Join()

        out = ''
        for r in rtype.splitlines():
            out += 6*' ' + r + '\n'

        return out


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
