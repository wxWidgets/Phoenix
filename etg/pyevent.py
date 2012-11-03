#---------------------------------------------------------------------------
# Name:        etg/pyevent.py
# Author:      Robin Dunn
#
# Created:     02-Nov-2012
# Copyright:   (c) 2012 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools.extractors import ClassDef, MethodDef, ParamDef

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
            wx.PyEvent can be used as a base class for implementing custom
            event types in Python. You should derive from this class instead
            of `wx.Event` because this class is Python-aware and is able to
            transport its Python bits safely through the wxWidgets event
            system and have them still be there when the event handler is
            invoked. Note that since wx.PyEvent is taking care of preserving
            the extra attributes that have been set then you do not need to
            override the Clone method in your derived classes.
            
            :see: `wx.PyCommandEvent`""",
        items=[
            MethodDef(name='wxPyEvent', isCtor=True, items=[
                ParamDef(type='int', name='id', default='0'),
                ParamDef(type='wxEventType', name='evenType', default='wxEVT_NULL'),
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
            
            MethodDef(name='Clone', type='wxEvent*', isVirtual=True, isConst=True, factory=True),
            MethodDef(name='_getAttrDict', type='PyObject*'),
            ])
    
    module.addItem(cls)
    cls.addCppCode("IMPLEMENT_DYNAMIC_CLASS(wxPyEvent, wxEvent);")
    cls.addHeaderCode('#include "pyevent.h"')


    
    cls = ClassDef(name='wxPyCommandEvent', bases=['wxCommandEvent'], 
        briefDoc="""\
            wx.PyCommandEvent can be used as a base class for implementing
            custom event types in Python. You should derive from this class
            instead of `wx.CommandEvent` because this class is Python-aware
            and is able to transport its Python bits safely through the
            wxWidgets event system and have them still be there when the
            event handler is invoked. Note that since wx.PyCommandEvent is
            taking care of preserving the extra attributes that have been set
            then you do not need to override the Clone method in your
            derived classes.
            
            :see: `wx.PyEvent`""",
        items=[
            MethodDef(name='wxPyCommandEvent', isCtor=True, items=[
                ParamDef(type='wxEventType', name='evenType', default='wxEVT_NULL'),
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
            
            MethodDef(name='Clone', type='wxEvent*', isVirtual=True, isConst=True, factory=True),
            MethodDef(name='_getAttrDict', type='PyObject*'),
            ])
    
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

