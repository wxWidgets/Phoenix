#---------------------------------------------------------------------------
# Name:        etgtools/tweaker_tools.py
# Author:      Robin Dunn
#
# Created:     3-Nov-2010
# Copyright:   (c) 2010 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

"""
Some helpers and utility functions that can assist with the tweaker
stage of the ETG scripts.
"""

import extractors



def removeWxPrefixes(node):
    """
    Rename items with a 'wx' prefix to not have the prefix. If the back-end
    generator supports auto-renaming then it can ignore the pyName value for
    those that are changed here. We'll still change them all incase the
    pyNames are needed elsewhere.
    """
    for item in node.allItems():
        if not item.pyName \
           and item.name.startswith('wx') \
           and not item.name.startswith('wxEVT_') \
           and not isinstance(item, (extractors.TypedefDef,
                                     extractors.MethodDef )):  # TODO: Any others?
                item.pyName = item.name[2:]
                item.wxDropped = True
        if item.name.startswith('wxEVT_'):
            # give these theire actual name so the auto-renamer won't touch them
            item.pyName = item.name
            

    
def ignoreAssignmentOperators(node):
    """
    Set the ignored flag for all class methods that are assignment operators
    """
    for item in node.allItems():
        if isinstance(item, extractors.MethodDef) and item.name == 'operator=':
            item.ignore()

            
def ignoreAllOperators(node):
    """
    Set the ignored flag for all class methods that are any kind of operator
    """
    for item in node.allItems():
        if isinstance(item, extractors.MethodDef) and item.name.startswith('operator'):
            item.ignore()

            
def createPyArgsStrings(node):
    """
    TODO: Create a pythonized version of the argsString in function and method
    items that can be used as part of the docstring.
    """
    pass


def convertTwoIntegersTemplate(CLASS):
    return """\
   // is it just a typecheck?
   if (!sipIsErr) {{
       if (sipCanConvertToType(sipPy, sipType_{CLASS}, SIP_NO_CONVERTORS))
           return 1;

       if (PySequence_Check(sipPy) && PySequence_Size(sipPy) == 2) {{
           int rval = 1;
           PyObject* o1 = PySequence_ITEM(sipPy, 0);
           PyObject* o2 = PySequence_ITEM(sipPy, 1);
           if (!PyNumber_Check(o1) || !PyNumber_Check(o2)) 
               rval = 0;
           Py_DECREF(o1);
           Py_DECREF(o2);
           return rval;
       }}
       return 0;
   }}   
   
   // otherwise do the conversion
   if (PySequence_Check(sipPy)) {{
       PyObject* o1 = PySequence_ITEM(sipPy, 0);
       PyObject* o2 = PySequence_ITEM(sipPy, 1);
       *sipCppPtr = new {CLASS}(PyInt_AsLong(o1), PyInt_AsLong(o2));
       Py_DECREF(o1);
       Py_DECREF(o2);
       return sipGetState(sipTransferObj);
    }}    
    *sipCppPtr = reinterpret_cast<{CLASS}*>(sipConvertToType(
                sipPy, sipType_{CLASS}, sipTransferObj, SIP_NO_CONVERTORS, 0, sipIsErr));
    return 0;
    """.format(**locals())


def convertFourIntegersTemplate(CLASS):
    return """\
   // is it just a typecheck?
   if (!sipIsErr) {{
       if (sipCanConvertToType(sipPy, sipType_{CLASS}, SIP_NO_CONVERTORS))
           return 1;

       if (PySequence_Check(sipPy) && PySequence_Size(sipPy) == 4) {{
           int rval = 1;
           PyObject* o1 = PySequence_ITEM(sipPy, 0);
           PyObject* o2 = PySequence_ITEM(sipPy, 1);
           PyObject* o3 = PySequence_ITEM(sipPy, 2);
           PyObject* o4 = PySequence_ITEM(sipPy, 3);
           if (!PyNumber_Check(o1) || !PyNumber_Check(o2) || !PyNumber_Check(o3) || !PyNumber_Check(o4)) 
               rval = 0;
           Py_DECREF(o1);
           Py_DECREF(o2);
           Py_DECREF(o3);
           Py_DECREF(o4);
           return rval;
       }}
       return 0;
   }}   
   
   // otherwise do the conversion
   if (PySequence_Check(sipPy)) {{
       PyObject* o1 = PySequence_ITEM(sipPy, 0);
       PyObject* o2 = PySequence_ITEM(sipPy, 1);
       PyObject* o3 = PySequence_ITEM(sipPy, 2);
       PyObject* o4 = PySequence_ITEM(sipPy, 3);       
       *sipCppPtr = new {CLASS}(PyInt_AsLong(o1), PyInt_AsLong(o2),
                                PyInt_AsLong(o3), PyInt_AsLong(o4));
       Py_DECREF(o1);
       Py_DECREF(o2);
       return sipGetState(sipTransferObj);
    }}    
    *sipCppPtr = reinterpret_cast<{CLASS}*>(sipConvertToType(
                sipPy, sipType_{CLASS}, sipTransferObj, SIP_NO_CONVERTORS, 0, sipIsErr));
    return 0;
    """.format(**locals())



def convertTwoDoublesTemplate(CLASS):
    return """\
   // is it just a typecheck?
   if (!sipIsErr) {{
       if (sipCanConvertToType(sipPy, sipType_{CLASS}, SIP_NO_CONVERTORS))
           return 1;

       if (PySequence_Check(sipPy) && PySequence_Size(sipPy) == 2) {{
           int rval = 1;
           PyObject* o1 = PySequence_ITEM(sipPy, 0);
           PyObject* o2 = PySequence_ITEM(sipPy, 1);
           if (!PyNumber_Check(o1) || !PyNumber_Check(o2)) 
               rval = 0;
           Py_DECREF(o1);
           Py_DECREF(o2);
           return rval;
       }}
       return 0;
   }}   
   
   // otherwise do the conversion
   if (PySequence_Check(sipPy)) {{
       PyObject* o1 = PySequence_ITEM(sipPy, 0);
       PyObject* o2 = PySequence_ITEM(sipPy, 1);
       *sipCppPtr = new {CLASS}(PyFloat_AsDouble(o1), PyFloat_AsDouble(o2));
       Py_DECREF(o1);
       Py_DECREF(o2);
       return sipGetState(sipTransferObj);
    }}    
    *sipCppPtr = reinterpret_cast<{CLASS}*>(sipConvertToType(
                sipPy, sipType_{CLASS}, sipTransferObj, SIP_NO_CONVERTORS, 0, sipIsErr));
    return 0;
    """.format(**locals())


def convertFourDoublesTemplate(CLASS):
    return """\
   // is it just a typecheck?
   if (!sipIsErr) {{
       if (sipCanConvertToType(sipPy, sipType_{CLASS}, SIP_NO_CONVERTORS))
           return 1;

       if (PySequence_Check(sipPy) && PySequence_Size(sipPy) == 4) {{
           int rval = 1;
           PyObject* o1 = PySequence_ITEM(sipPy, 0);
           PyObject* o2 = PySequence_ITEM(sipPy, 1);
           PyObject* o3 = PySequence_ITEM(sipPy, 2);
           PyObject* o4 = PySequence_ITEM(sipPy, 3);
           if (!PyNumber_Check(o1) || !PyNumber_Check(o2) || !PyNumber_Check(o3) || !PyNumber_Check(o4)) 
               rval = 0;
           Py_DECREF(o1);
           Py_DECREF(o2);
           Py_DECREF(o3);
           Py_DECREF(o4);
           return rval;
       }}
       return 0;
   }}   
   
   // otherwise do the conversion
   if (PySequence_Check(sipPy)) {{
       PyObject* o1 = PySequence_ITEM(sipPy, 0);
       PyObject* o2 = PySequence_ITEM(sipPy, 1);
       PyObject* o3 = PySequence_ITEM(sipPy, 2);
       PyObject* o4 = PySequence_ITEM(sipPy, 3);       
       *sipCppPtr = new {CLASS}(PyFloat_AsDouble(o1), PyFloat_AsDouble(o2),
                                PyFloat_AsDouble(o3), PyFloat_AsDouble(o4));
       Py_DECREF(o1);
       Py_DECREF(o2);
       return sipGetState(sipTransferObj);
    }}    
    *sipCppPtr = reinterpret_cast<{CLASS}*>(sipConvertToType(
                sipPy, sipType_{CLASS}, sipTransferObj, SIP_NO_CONVERTORS, 0, sipIsErr));
    return 0;
    """.format(**locals())



