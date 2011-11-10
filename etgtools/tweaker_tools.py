#---------------------------------------------------------------------------
# Name:        etgtools/tweaker_tools.py
# Author:      Robin Dunn
#
# Created:     3-Nov-2010
# Copyright:   (c) 2011 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

"""
Some helpers and utility functions that can assist with the tweaker
stage of the ETG scripts.
"""

import extractors
import sys, os

magicMethods = {
    'operator!=' : '__ne__',
    'operator==' : '__eq__',
    # TODO
}


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
        if item.name.startswith('wxEVT_') and 'CATEGORY' not in item.name:
            # give these their actual name so the auto-renamer won't touch them
            item.pyName = item.name
            

def removeWxPrefix(name):
    if name.startswith('wx') and not name.startswith('wxEVT_'):
        name = name[2:]
    return name


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

            
def addAutoProperties(node):
    """
    Call klass.addAutoProperties for all classes in node with
    allowAutoProperties set and which do not already have properties added by
    hand in the tweaker code.
    """
    for item in node.allItems():
        if isinstance(item, extractors.ClassDef):
            if not item.allowAutoProperties:
                continue
            if len([i for i in item if isinstance(i, extractors.PropertyDef)]):
                continue
            item.addAutoProperties()

            
def fixEventClass(klass):
    """
    Add the extra stuff that an event class needs that are lacking from the
    interface headers.
    """
    assert isinstance(klass, extractors.ClassDef)
    if klass.name != 'wxEvent':
        # Clone() in wxEvent is pure virtual, so we need to let the back-end
        # know that the other event classes have an implementation for it so
        # it won't think that they are abstract classes too.
        if not klass.findItem('Clone'):
            klass.addPublic('virtual wxEvent* Clone() const /Factory/;')

    # Add a private assignment operator so the back-end (if it's watching out
    # for this) won't try to make copies by assignment.
    klass.addPrivateAssignOp()

    
def fixWindowClass(klass, hideVirtuals=True):
    """
    Do common tweaks for a window class.
    """
    # The ctor and Create method transfer ownership of the this pointer
    for func in klass.findAll(klass.name) + klass.findAll('Create'):
        if isinstance(func, extractors.MethodDef):
            # if a class has an empty ctor it might not have this
            parent = func.findItem('parent')
            if parent:
                parent.transferThis = True
            # give the id param a default value if it has one
            id = func.findItem('id')
            if id:
                id.default = 'wxID_ANY'

            # if there is a pos or size parameter without a default then give it one.
            p = func.findItem('pos')
            if p and not p.default:
                p.default = 'wxDefaultPosition'
            p = func.findItem('size')
            if p and not p.default:
                p.default = 'wxDefaultSize'

    if hideVirtuals:
        # There is no need to make all the C++ virtuals overridable in Python, and
        # hiding the fact that they are virtual from the back end generator will
        # greatly reduce the amount of code that needs to be generated. Remove all
        # the virtual flags, and then and then add it back to a select few.
        removeVirtuals(klass)
        addWindowVirtuals(klass)

    
def fixTopLevelWindowClass(klass, hideVirtuals=True):
    """
    Tweaks for TLWs 
    """
    # TLW tweaks are a little different. We use the function annotation for
    # TransferThis instead of the argument anotation.
    klass.find(klass.name).findOverload('parent').transfer = True
    item = klass.findItem('Create')
    if item:
        item.transferThis = True
        
    # give the id param a default value
    item = klass.findItem('%s.id' % klass.name)
    if item:
        item.default = 'wxID_ANY'
    item = klass.findItem('Create.id')
    if item:
        item.default = 'wxID_ANY'

    if hideVirtuals:
        removeVirtuals(klass)
        addWindowVirtuals(klass)
    
    
def fixSizerClass(klass):
    """
    Remove all virtuals except for CalcMin and RecalcSizes.
    """
    removeVirtuals(klass)
    klass.find('CalcMin').isVirtual = True
    klass.find('RecalcSizes').isVirtual = True
    
    # in the wxSizer class they are pure-virtual
    if klass.name == 'wxSizer':
        klass.find('CalcMin').isPureVirtual = True
        klass.find('RecalcSizes').isPureVirtual = True
        
    
def removeVirtuals(klass):
    """
    Sometimes methods are marked as virtual but probably don't ever need to be
    overridden from Python. This function will unset the virtual flag for all
    methods in a class, which can save some code-bloat in the wrapper code.
    """
    assert isinstance(klass, extractors.ClassDef)
    for item in klass.allItems():
        if isinstance(item, extractors.MethodDef):
            item.isVirtual = item.isPureVirtual = False

            
def addWindowVirtuals(klass):
    """
    Either turn the virtual flag back on or add a delcaration for the subset of
    the C++ virtuals in wxWindow classes that we will be supporting.
    """
    publicWindowVirtuals = [      
        ('GetClientAreaOrigin',      'wxPoint GetClientAreaOrigin() const'),
        ('Validate',                 'bool Validate()'),
        ('TransferDataToWindow',     'bool TransferDataToWindow()'),
        ('TransferDataFromWindow',   'bool TransferDataFromWindow()'),
        ('InitDialog',               'void InitDialog()'),
        ('AcceptsFocus',             'bool AcceptsFocus() const'),
        ('AcceptsFocusRecursively',  'bool AcceptsFocusRecursively() const'),
        ('AcceptsFocusFromKeyboard', 'bool AcceptsFocusFromKeyboard() const'),
        ('AddChild',                 'void AddChild( wxWindowBase *child )'),
        ('RemoveChild',              'void RemoveChild( wxWindowBase *child )'),
        ('InheritAttributes',        'void InheritAttributes()'),
        ('ShouldInheritColours',     'bool ShouldInheritColours() const'),
        ('HasTransparentBackground', 'bool HasTransparentBackground()'),
        ('OnInternalIdle',           'void OnInternalIdle()'),
        ('GetMainWindowOfCompositeControl', 
                                     'wxWindow *GetMainWindowOfCompositeControl()'),
        ('InformFirstDirection',     'bool InformFirstDirection(int direction, int size, int availableOtherDir)'),
        ('SetCanFocus',              'void SetCanFocus(bool canFocus)'),
        
        ## What about these?
        #bool HasMultiplePages() const 
        #void UpdateWindowUI(long flags = wxUPDATE_UI_NONE);
        #void DoUpdateWindowUI(wxUpdateUIEvent& event) ;
    ]
    
    protectedWindowVirtuals = [    
        ('ProcessEvent',        'bool ProcessEvent(wxEvent & event)'),
        ('DoEnable',            'void DoEnable(bool enable)'),
        ('OnEnabled',           'void OnEnabled(bool enabled)'),
        ('DoGetPosition',       'void DoGetPosition(int *x, int *y) const'),
        ('DoGetSize',           'void DoGetSize(int *width, int *height) const'),
        ('DoGetClientSize',     'void DoGetClientSize(int *width, int *height) const'),
        ('DoGetBestSize',       'wxSize DoGetBestSize() const'),
        ('DoGetBestClientSize', 'wxSize DoGetBestClientSize() const'),
        ('DoSetSize',           'void DoSetSize(int x, int y, int width, int height, int sizeFlags)'),
        ('DoSetClientSize',     'void DoSetClientSize(int width, int height)'),
        ('DoSetSizeHints',      'void DoSetSizeHints( int minW, int minH, int maxW, int maxH, int incW, int incH )'),
        ('DoGetBorderSize',     'wxSize DoGetBorderSize() const'),
        ('DoMoveWindow',        'void DoMoveWindow(int x, int y, int width, int height)'),
        ('DoSetWindowVariant',  'void DoSetWindowVariant( wxWindowVariant variant)'),
        ('GetDefaultBorder',    'wxBorder GetDefaultBorder() const'),
        ('GetDefaultBorderForControl', 
                                'wxBorder GetDefaultBorderForControl() const'),
        ('DoFreeze',            'void DoFreeze()'),
        ('DoThaw',              'void DoThaw()'),

        ## What about these?
        #('DoGetScreenPosition', 'void DoGetScreenPosition(int *x, int *y) const'),
        #('DoSetVirtualSize',    'void DoSetVirtualSize( int x, int y )'),
        #('DoGetVirtualSize',    'wxSize DoGetVirtualSize() const'),
    ]
    
    def _processItems(klass, prot, virtuals):
        txt = ''
        for name, decl in virtuals:
            m = klass.findItem(name)
            if m:
                m.ignore(False)
                m.isVirtual = True
            else:
                txt += 'virtual %s;\n' % decl
        if txt:
            txt = prot + txt
        return txt
    
    txt = _processItems(klass, 'public:\n', publicWindowVirtuals)
    klass.addItem(extractors.WigCode(txt))
    txt = _processItems(klass, 'protected:\n', protectedWindowVirtuals)
    klass.addItem(extractors.WigCode(txt))
    klass.addPublic()
                  
    
    
def getEtgFiles(names):
    """
    Create a list of the files from the basenames in the names list that
    corespond to files in the etg folder.
    """
    return getMatchingFiles(names, 'etg/%s.py')


def getNonEtgFiles(names, template='src/%s.sip'):
    """
    Get the files other than the ETG scripts from the list of names that match
    the template. By default gets the SIP files in src.
    """
    return getMatchingFiles(names, template)

    
def getMatchingFiles(names, template):
    """
    Create a list of files from the basenames in names that match the template
    and actually exist.
    """
    files = list()
    for name in names:
        name = template % name
        if os.path.exists(name):
            files.append(name)
    return files
            

            
def doCommonTweaks(module):
    """
    A collection of tweaks that should probably be done to all modules.
    """
    ignoreAssignmentOperators(module)
    removeWxPrefixes(module)
    addAutoProperties(module)
    
    
def changeTypeNames(module, oldName, newName, skipTypedef=False):
    """
    Changes the matching type names for functions and parameters to a new
    name, and optionally adds typedefs for the new name as well.
    """
    if not skipTypedef:
        module.addHeaderCode("typedef {old} {new};".format(old=oldName, new=newName))
        module.addItem(extractors.TypedefDef(type=oldName, name=newName))
    for item in module.allItems():
        if isinstance(item, (extractors.FunctionDef, extractors.ParamDef)) and \
                 hasattr(item, 'type') and oldName in item.type:
            item.type = item.type.replace(oldName, newName)


#---------------------------------------------------------------------------


def getWrapperGenerator():
    """
    A simple factory function to create a wrapper generator class of the desired type.
    """
    if '--swig' in sys.argv:
        import swig_generator
        gClass = swig_generator.SwigWrapperGenerator
    elif '--sip' in sys.argv:
        import sip_generator
        gClass = sip_generator.SipWrapperGenerator
    else:
        # The default is sip
        import sip_generator
        gClass = sip_generator.SipWrapperGenerator    
    return gClass()


def getDocsGenerator():
    import generators    
    g = generators.StubbedDocsGenerator()
    return g



def runGenerators(module):
    checkForUnitTestModule(module)

    generators = list()
    
    # Create the code generator selected from command line args
    generators.append(getWrapperGenerator())
    
    # Toss in the PI generator too
    import pi_generator
    generators.append(pi_generator.PiWrapperGenerator())    
    
    # And finally add the documentation generator
    generators.append(getDocsGenerator())

    # run them
    for g in generators:
        g.generate(module)
        


def checkForUnitTestModule(module):
    pathname = 'unittests/test_%s.py' % module.name
    if os.path.exists(pathname) or not module.check4unittest:
        return
    print 'WARNING: Unittest module (%s) not found!' % pathname


#---------------------------------------------------------------------------


def convertTwoIntegersTemplate(CLASS):
    return """\
   // is it just a typecheck?
   if (!sipIsErr) {{
       // is it already an instance of {CLASS}?
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
    if (sipCanConvertToType(sipPy, sipType_{CLASS}, SIP_NO_CONVERTORS)) {{
        // Just fetch the existing instance
        *sipCppPtr = reinterpret_cast<{CLASS}*>(sipConvertToType(
                sipPy, sipType_{CLASS}, sipTransferObj, SIP_NO_CONVERTORS, 0, sipIsErr));
        return 0;  // not a new instance
    }}
    
    // or create a new instance
    PyObject* o1 = PySequence_ITEM(sipPy, 0);
    PyObject* o2 = PySequence_ITEM(sipPy, 1);
    *sipCppPtr = new {CLASS}(PyInt_AsLong(o1), PyInt_AsLong(o2));
    Py_DECREF(o1);
    Py_DECREF(o2);
    return SIP_TEMPORARY;
    """.format(**locals())


def convertFourIntegersTemplate(CLASS):
    return """\
    // is it just a typecheck?
    if (!sipIsErr) {{
        // is it already an instance of {CLASS}?
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
    if (sipCanConvertToType(sipPy, sipType_{CLASS}, SIP_NO_CONVERTORS)) {{
        // Just fetch the existing instance
        *sipCppPtr = reinterpret_cast<{CLASS}*>(sipConvertToType(
                sipPy, sipType_{CLASS}, sipTransferObj, SIP_NO_CONVERTORS, 0, sipIsErr));
        return 0; // not a new instance
    }}
    // or create a new instance
    PyObject* o1 = PySequence_ITEM(sipPy, 0);
    PyObject* o2 = PySequence_ITEM(sipPy, 1);
    PyObject* o3 = PySequence_ITEM(sipPy, 2);
    PyObject* o4 = PySequence_ITEM(sipPy, 3);       
    *sipCppPtr = new {CLASS}(PyInt_AsLong(o1), PyInt_AsLong(o2),
                             PyInt_AsLong(o3), PyInt_AsLong(o4));
    Py_DECREF(o1);
    Py_DECREF(o2);
    return SIP_TEMPORARY;
    """.format(**locals())



def convertTwoDoublesTemplate(CLASS):
    return """\
    // is it just a typecheck?
    if (!sipIsErr) {{
        // is it already an instance of {CLASS}?
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
    if (sipCanConvertToType(sipPy, sipType_{CLASS}, SIP_NO_CONVERTORS)) {{
        // Just fetch the existing instance
        *sipCppPtr = reinterpret_cast<{CLASS}*>(sipConvertToType(
                sipPy, sipType_{CLASS}, sipTransferObj, SIP_NO_CONVERTORS, 0, sipIsErr));
        return 0; // not a new instance
    }}
   
    // or create a new instance
    PyObject* o1 = PySequence_ITEM(sipPy, 0);
    PyObject* o2 = PySequence_ITEM(sipPy, 1);
    *sipCppPtr = new {CLASS}(PyFloat_AsDouble(o1), PyFloat_AsDouble(o2));
    Py_DECREF(o1);
    Py_DECREF(o2);
    return SIP_TEMPORARY;
    """.format(**locals())


def convertFourDoublesTemplate(CLASS):
    return """\
    // is it just a typecheck?
    if (!sipIsErr) {{
        // is it already an instance of {CLASS}?
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
    if (sipCanConvertToType(sipPy, sipType_{CLASS}, SIP_NO_CONVERTORS)) {{
        // Just fetch the existing instance
        *sipCppPtr = reinterpret_cast<{CLASS}*>(sipConvertToType(
                sipPy, sipType_{CLASS}, sipTransferObj, SIP_NO_CONVERTORS, 0, sipIsErr));
        return 0; // not a new instance
    }}
    
    // or create a new instance
    PyObject* o1 = PySequence_ITEM(sipPy, 0);
    PyObject* o2 = PySequence_ITEM(sipPy, 1);
    PyObject* o3 = PySequence_ITEM(sipPy, 2);
    PyObject* o4 = PySequence_ITEM(sipPy, 3);       
    *sipCppPtr = new {CLASS}(PyFloat_AsDouble(o1), PyFloat_AsDouble(o2),
    PyFloat_AsDouble(o3), PyFloat_AsDouble(o4));
    Py_DECREF(o1);
    Py_DECREF(o2);
    return SIP_TEMPORARY;
    """.format(**locals())



#---------------------------------------------------------------------------
# Templates for creating wrappers for type-specific wxList and wxArray classes


def wxListWrapperTemplate(ListClass, ItemClass, module, RealItemClass=None, 
                          includeConvertToType=False):
    if RealItemClass is None:
        RealItemClass = ItemClass    
        
    moduleName = module.module        
    ListClass_pyName = removeWxPrefix(ListClass)
    
    # *** TODO: This can probably be done in a way that is not SIP-specfic.
    # Try creating extractor objects from scratch and attach cppMethods to
    # them as needed, etc..
        
    klassCode = '''\
class {ListClass}_iterator /Abstract/ 
{{
    // the C++ implementation of this class
    %TypeHeaderCode
        class {ListClass}_iterator {{
        public:
            {ListClass}_iterator({ListClass}::compatibility_iterator start)
                : m_node(start) {{}}
            
            {ItemClass}* __next__() {{
                {RealItemClass}* obj = NULL;
                if (m_node) {{
                    obj = m_node->GetData();
                    m_node = m_node->GetNext();
                }}
                else {{
                    PyErr_SetString(PyExc_StopIteration, "");
                }}
                return ({ItemClass}*)obj;
            }}
        private:
            {ListClass}::compatibility_iterator m_node;
        }};
    %End
public:
    {ItemClass}* __next__();
    %MethodCode
        sipRes = sipCpp->__next__();
        if (PyErr_Occurred())
            return NULL;
    %End
}};       

class {ListClass} 
{{
public:
    SIP_SSIZE_T __len__();
    %MethodCode
        sipRes = sipCpp->size();
    %End

    {ItemClass}* __getitem__(size_t index);
    %MethodCode
        if (index < sipCpp->size()) {{
            {ListClass}::compatibility_iterator node = sipCpp->Item(index);
            if (node) 
                sipRes = ({ItemClass}*)node->GetData();
        }}
        else {{
            PyErr_SetString(PyExc_IndexError, "sequence index out of range");
            sipError = sipErrorFail;
        }}
    %End

    int __contains__(const {ItemClass}* obj);
    %MethodCode
        {ListClass}::compatibility_iterator node;
        node = sipCpp->Find(({RealItemClass}*)obj);
        sipRes = node != NULL;
    %End

    {ListClass}_iterator* __iter__() /Factory/;
    %MethodCode
        sipRes =  new {ListClass}_iterator(sipCpp->GetFirst());
    %End

    // TODO:  add support for index(value, [start, [stop]])
    int index({ItemClass}* obj);
    %MethodCode
        int idx = sipCpp->IndexOf(({RealItemClass}*)obj);
        if (idx == wxNOT_FOUND) {{
            sipError = sipErrorFail;
            PyErr_SetString(PyExc_ValueError,
                            "sequence.index(x): x not in sequence");
            }}
        sipRes = idx;
    %End
    
    @ConvertToTypeCode@
}};

%Extract(id=pycode{moduleName})
def _{ListClass_pyName}___repr__(self):
    return "{ListClass_pyName}: " + repr(list(self))
{ListClass_pyName}.__repr__ = _{ListClass_pyName}___repr__
del _{ListClass_pyName}___repr__
%End
'''

    convertToTypeCode = '''\
%ConvertToTypeCode
    // Code to test a PyObject for compatibility
    if (!sipIsErr) {{
        int success = TRUE;
        // is it already a {ListClass}?
        if (sipCanConvertToType(sipPy, sipType_{ListClass}, SIP_NO_CONVERTORS))
            return success;
        // otherwise ensure that it is a sequence
        if (! PySequence_Check(sipPy)) 
            success = FALSE;
        // ensure it is not a string or unicode object (they are sequences too)
        else if (PyString_Check(sipPy) || PyUnicode_Check(sipPy))
            success = FALSE;
        // ensure each item can be converted to {ItemClass}
        else {{
            Py_ssize_t i, len = PySequence_Length(sipPy);
            for (i=0; i<len; i++) {{
                PyObject* item = PySequence_ITEM(sipPy, i);
                if (!sipCanConvertToType(item, sipType_{ItemClass}, SIP_NOT_NONE)) {{
                    Py_DECREF(item);
                    success = FALSE;
                    break;
                }}
                Py_DECREF(item);
            }}    
        }}
        if (!success)            
            PyErr_SetString(PyExc_TypeError, "Sequence of {ItemClass} compatible objects expected.");
        return success;
    }}

    // Is it already a {ListClass}? Return the exiting instance if so
    if (sipCanConvertToType(sipPy, sipType_{ListClass}, SIP_NO_CONVERTORS)) {{
        *sipCppPtr = reinterpret_cast<{ListClass}*>(
                     sipConvertToType(sipPy, sipType_{ListClass}, NULL, 
                                      SIP_NO_CONVERTORS, 0, sipIsErr));
        return 0;
    }}
    
    // Create a new {ListClass} and convert compatible PyObjects from the sequence
    {ListClass} *list = new {ListClass};
    list->DeleteContents(true); // tell the list to take ownership of the items
    Py_ssize_t i, len = PySequence_Length(sipPy);
    for (i=0; i<len; i++) {{
        int state;
        PyObject* pyItem = PySequence_ITEM(sipPy, i);
        {ItemClass}* cItem = reinterpret_cast<{ItemClass}*>(
                             sipConvertToType(pyItem, sipType_{ItemClass}, 
                             NULL, 0, &state, sipIsErr));
        if (!state)  // a temporary was not created for us, make one now
            cItem = new {ItemClass}(*cItem);
        list->Append(cItem);
        Py_DECREF(pyItem);
    }}
    *sipCppPtr = list;
    return SIP_TEMPORARY;
%End
'''
    if includeConvertToType:
        klassCode = klassCode.replace('@ConvertToTypeCode@', convertToTypeCode)
    else:
        klassCode = klassCode.replace('@ConvertToTypeCode@', '')
    return extractors.WigCode(klassCode.format(**locals()))



def wxArrayWrapperTemplate(ArrayClass, ItemClass, module):
    moduleName = module.module        
    ArrayClass_pyName = removeWxPrefix(ArrayClass)
    
    # *** TODO: This can probably be done in a way that is not SIP-specfic.
    # Try creating extractor objects from scratch and attach cppMethods to
    # them as needed, etc..
        
    return extractors.WigCode('''\
class {ArrayClass} 
{{
public:
    SIP_SSIZE_T __len__();
    %MethodCode
        sipRes = sipCpp->GetCount();
    %End

    {ItemClass}& __getitem__(size_t index);
    %MethodCode
        if (index < sipCpp->GetCount()) {{
            sipRes = &sipCpp->Item(index);
        }}
        else {{
            PyErr_SetString(PyExc_IndexError, "sequence index out of range");
            sipError = sipErrorFail;
        }}
    %End

    int __contains__(const {ItemClass}& obj);
    %MethodCode
        int idx = sipCpp->Index(*obj, false);
        sipRes = idx != wxNOT_FOUND;
    %End

    void append(const {ItemClass}& obj);
    %MethodCode
        sipCpp->Add(*obj);
    %End

    // TODO:  add support for index(value, [start, [stop]])
    int index(const {ItemClass}& obj);
    %MethodCode
        int idx = sipCpp->Index(*obj, false);
        if (idx == wxNOT_FOUND) {{
            sipError = sipErrorFail;
            PyErr_SetString(PyExc_ValueError,
                            "sequence.index(x): x not in sequence");
            }}
        sipRes = idx;
    %End
}};

%Extract(id=pycode{moduleName})
def _{ArrayClass_pyName}___repr__(self):
    return "{ArrayClass_pyName}: " + repr(list(self))
{ArrayClass_pyName}.__repr__ = _{ArrayClass_pyName}___repr__
del _{ArrayClass_pyName}___repr__
%End
'''.format(**locals()))




def ObjArrayHelperTemplate(objType, sipType, errmsg):
    """
    Generates a helper function that can convert from a Python sequence of
    objects (or items that can be converted to the target type) into a C
    array of values. Copies are made of the items so the object types should
    support implicit or explicit copies and the copy should be cheap.  
    
    This kind of helper is useful for situations where the C/C++ API takes a
    simple pointer and a count, and there is no higher level container object
    (like a wxList or wxArray) being used. If there is an overloaded method
    that uses one of those types then the array overload should just be
    ignored. But for those cases where the array is the only option then this
    helper can be used to make the array.
    """
    
    cppCode = """\
// Convert a Python sequence of {objType} objects, or items that can be converted 
// to {objType} into a C array of {objType} instances.
static
{objType}* {objType}_array_helper(PyObject* source, size_t *count)
{{
    {objType}* array;
    Py_ssize_t idx, len;
    
    // ensure that it is a sequence
    if (! PySequence_Check(source)) 
        goto error0;
    // ensure it is not a string or unicode object (they are sequences too)
    else if (PyString_Check(source) || PyUnicode_Check(source))
        goto error0;
    // ensure each item can be converted to {objType}
    else {{
        len = PySequence_Length(source);
        for (idx=0; idx<len; idx++) {{
            PyObject* item = PySequence_ITEM(source, idx);
            if (!sipCanConvertToType(item, {sipType}, SIP_NOT_NONE)) {{
                Py_DECREF(item);
                goto error0;
            }}
            Py_DECREF(item);
        }}
    }}
    
    // The length of the sequence is returned in count.
    *count = len;
    array = new {objType}[*count];
    if (!array) {{
        PyErr_SetString(PyExc_MemoryError, "Unable to allocate temporary array");
        return NULL;
    }}
    for (idx=0; idx<len; idx++) {{
        PyObject* obj = PySequence_ITEM(source, idx);
        int state = 0;
        int err = 0;
        {objType}* item = reinterpret_cast<{objType}*>(
                        sipConvertToType(obj, {sipType}, NULL, 0, &state, &err));
        array[idx] = *item;
        sipReleaseType((void*)item, {sipType}, state); // delete temporary instances
        Py_DECREF(obj);
    }}
    return array;

error0:
    PyErr_SetString(PyExc_TypeError, "{errmsg}");
    return NULL;
}}
""".format(**locals())

    return cppCode


#---------------------------------------------------------------------------
