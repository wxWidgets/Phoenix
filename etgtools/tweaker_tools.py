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
import sys, os


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
            # give these their actual name so the auto-renamer won't touch them
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

    
def fixWindowClass(klass):
    """
    Do common tweaks for a window class.
    """
    # The ctor and Create method transfer ownership of the this pointer
    klass.find('%s.parent' % klass.name).transferThis = True
    klass.find('Create.parent').transferThis = True
    # give the id param a default value
    klass.find('%s.id' % klass.name).default = 'wxID_ANY'
    klass.find('Create.id').default = 'wxID_ANY'
            
            
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
        #('Enable', ''),   We have DoEnable now...
        
        ## What about these?
        #bool HasMultiplePages() const 
        #void UpdateWindowUI(long flags = wxUPDATE_UI_NONE);
        #void DoUpdateWindowUI(wxUpdateUIEvent& event) ;
    ]
    
    protectedWindowVirtuals = [    
        ('ProcessEvent',        'bool ProcessEvent(wxEvent & event)'),
        ('DoEnable',            'void DoEnable(bool enable)'),
        ('OnEnabled',           'void OnEnabled(bool enabled)'),
        ('DoGetPosition',        'void DoGetPosition(int *x, int *y) const'),
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
        # The default is sip, at least for now...
        import sip_generator
        gClass = sip_generator.SipWrapperGenerator
    
    return gClass()


def getDocsGenerator():
    import generators    
    g = generators.StubbedDocsGenerator()
    return g



def runGenerators(module):
    # Create the code generator and make the wrapper code
    wg = getWrapperGenerator()
    wg.generate(module)
    
    # Create a documentation generator and let it do its thing
    dg = getDocsGenerator()
    dg.generate(module)



#---------------------------------------------------------------------------


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
    return sipGetState(sipTransferObj);
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
    return sipGetState(sipTransferObj);
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
    return sipGetState(sipTransferObj);
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
    return sipGetState(sipTransferObj);
    """.format(**locals())



#---------------------------------------------------------------------------
# Templates for creating wrappers for type-specific wxList and wxArray classes


def wxListWrapperTemplate(ListClass, ItemClass, RealItemClass=None):
    if RealItemClass is None:
        RealItemClass = ItemClass    
        
    # *** TODO: This can probably be done in a way that is not SIP-specfic. Try
    # creating extractor objects from scratch and attach cppMethods to them.
        
    return extractors.WigCode('''\
class {ListClass}_iterator /Abstract/ 
{{
    // the C++ implementation of this class
    %TypeHeaderCode
        class {ListClass}_iterator {{
        public:
            {ListClass}_iterator({ListClass}::compatibility_iterator start)
                : m_node(start) {{}}
            
            {ItemClass}* next() {{
                {RealItemClass}* obj = NULL;
                if (m_node) {{
                    obj = m_node->GetData();
                    m_node = m_node->GetNext();
                }}
                else PyErr_SetString(PyExc_StopIteration, "");
                return ({ItemClass}*)obj;
            }}
        private:
            {ListClass}::compatibility_iterator m_node;
        }};
    %End
public:
    {ItemClass}* next();
}};       

class {ListClass} 
{{
public:
    int __len__();
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
        PyErr_SetString(PyExc_IndexError, "sequence index out of range");
        sipError = sipErrorFail;
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
}};

%Extract(id=pycode)
def _{ListClass}___repr__(self):
    return "{ListClass}: " + repr(list(self))
{ListClass}.__repr__ = _{ListClass}___repr__
del _{ListClass}___repr__
%End
'''.format(**locals()))




#---------------------------------------------------------------------------
