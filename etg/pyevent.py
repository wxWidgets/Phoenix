#---------------------------------------------------------------------------
# Name:        etg/pyevent.py
# Author:      Robin Dunn
#
# Created:     02-Nov-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools.extractors import ClassDef, MethodDef, ParamDef

import copy

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "pyevent"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    cls = ClassDef(name='wxPyEvent', bases=['wxEvent'],
        briefDoc="""\
            :class:`PyEvent` can be used as a base class for implementing custom
            event types in Python. You should derive from this class instead
            of :class:`Event` because this class is Python-aware and is able to
            transport its Python bits safely through the wxWidgets event
            system and have them still be there when the event handler is
            invoked. Note that since :class:`PyEvent` is taking care of preserving
            the extra attributes that have been set then you do not need to
            override the Clone method in your derived classes.

            :see: :class:`PyCommandEvent`""",
        items=[
            MethodDef(name='wxPyEvent', isCtor=True, items=[
                ParamDef(type='int', name='id', default='0'),
                ParamDef(type='wxEventType', name='eventType', default='wxEVT_NULL'),
                ]),

            MethodDef(name='__getattr__', type='PyObject*', items=[
                ParamDef(type='PyObject*', name='name'),],
                cppCode=("sipRes = sipCpp->__getattr__(name);", "sip")),

            MethodDef(name='__delattr__', type='void', items=[
                ParamDef(type='PyObject*', name='name'),],
                cppCode=("sipCpp->__delattr__(name);", "sip")),

            MethodDef(name='__setattr__', type='void', items=[
                ParamDef(type='PyObject*', name='name'),
                ParamDef(type='PyObject*', name='value'),],
                cppCode=("sipCpp->__setattr__(name, value);", "sip")),

            MethodDef(name='Clone', type='wxEvent*', isVirtual=True, isConst=True,
                factory=True, docsIgnored=True),
            MethodDef(name='_getAttrDict', type='PyObject*',
                briefDoc="Gives access to the internal object that is tracking the event's python attributes."),
            ])

    cls.addPyMethod('Clone', '(self)',
        doc="""\
            Make a new instance of the event that is a copy of self.

            Through the magic of Python this implementation should work for
            this and all derived classes.""",
        body="""\
            # Create a new instance of the same type as this instance and
            # then invoke the C++ copy constructor to copy the C++ parts and
            # any custom attributes.
            clone = wx.PyEvent.__new__(self.__class__)
            wx.PyEvent.__init__(clone, self)
            return clone
            """)


    module.addItem(cls)
    cls.addCppCode("IMPLEMENT_DYNAMIC_CLASS(wxPyEvent, wxEvent);")
    cls.addHeaderCode('#include "pyevent.h"')



    cls = ClassDef(name='wxPyCommandEvent', bases=['wxCommandEvent'],
        briefDoc="""\
            :class:`PyCommandEvent` can be used as a base class for implementing
            custom event types in Python. You should derive from this class
            instead of :class:`CommandEvent` because this class is Python-aware
            and is able to transport its Python bits safely through the
            wxWidgets event system and have them still be there when the
            event handler is invoked. Note that since :class:`PyCommandEvent` is
            taking care of preserving the extra attributes that have been set
            then you do not need to override the Clone method in your
            derived classes.

            :see: :class:`PyEvent`""",
        items=[
            MethodDef(name='wxPyCommandEvent', isCtor=True, items=[
                ParamDef(type='wxEventType', name='eventType', default='wxEVT_NULL'),
                ParamDef(type='int', name='id', default='0'),
                ]),

            MethodDef(name='__getattr__', type='PyObject*', items=[
                ParamDef(type='PyObject*', name='name'),],
                cppCode=("sipRes = sipCpp->__getattr__(name);", "sip")),

            MethodDef(name='__delattr__', type='void', items=[
                ParamDef(type='PyObject*', name='name'),],
                cppCode=("sipCpp->__delattr__(name);", "sip")),

            MethodDef(name='__setattr__', type='void', items=[
                ParamDef(type='PyObject*', name='name'),
                ParamDef(type='PyObject*', name='value'),],
                cppCode=("sipCpp->__setattr__(name, value);", "sip")),

            MethodDef(name='Clone', type='wxEvent*', isVirtual=True, isConst=True,
                factory=True, docsIgnored=True),
            MethodDef(name='_getAttrDict', type='PyObject*',
                briefDoc="Gives access to the internal object that is tracking the event's python attributes."),
            ])

    cls.addPyMethod('Clone', '(self)',
        doc="""\
            Make a new instance of the event that is a copy of self.

            Through the magic of Python this implementation should work for
            this and all derived classes.""",
        body="""\
            # Create a new instance of the same type as this instance and
            # then invoke the C++ copy constructor to copy the C++ parts and
            # any custom attributes.
            clone = wx.PyCommandEvent.__new__(self.__class__)
            wx.PyCommandEvent.__init__(clone, self)
            return clone
            """)


    module.addItem(cls)
    cls.addCppCode("IMPLEMENT_DYNAMIC_CLASS(wxPyCommandEvent, wxCommandEvent);")
    cls.addHeaderCode('#include "pyevent.h"')



    # TODO: Temporary testing code, get rid of this later
    module.addCppCode("""\
        wxEvent* testCppClone(wxEvent& evt) {
            return evt.Clone();
        }""")
    module.addItem(etgtools.WigCode("wxEvent* testCppClone(wxEvent& evt);"))


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()
