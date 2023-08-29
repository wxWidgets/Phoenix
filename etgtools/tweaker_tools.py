#---------------------------------------------------------------------------
# Name:        etgtools/tweaker_tools.py
# Author:      Robin Dunn
#
# Created:     3-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

"""
Some helpers and utility functions that can assist with the tweaker
stage of the ETG scripts.
"""

import etgtools as extractors
from .generators import textfile_open
import keyword
import re
import sys, os
import copy
import textwrap
from typing import Optional, Tuple


PY3 = sys.version_info[0] == 3
isWindows = sys.platform.startswith('win')

magicMethods = {
    'operator!='    : '__ne__',
    'operator=='    : '__eq__',
    'operator+'     : '__add__',
    'operator-'     : '__sub__',
    'operator*'     : '__mul__',
    'operator/'     : '__div__',
    'operator+='    : '__iadd__',
    'operator-='    : '__isub__',
    'operator*='    : '__imul__',
    'operator/='    : '__idiv__',
    'operator bool' : '__int__',  # Why not __nonzero__?
    # TODO: add more
}


def removeWxPrefixes(node):
    """
    Rename items with a 'wx' prefix to not have the prefix. If the back-end
    generator supports auto-renaming then it can ignore the pyName value for
    those that are changed here. We'll still change them all in case the
    pyNames are needed elsewhere.
    """
    for item in node.allItems():
        if not item.pyName \
           and item.name.startswith('wx') \
           and not item.name.startswith('wxEVT_') \
           and not isinstance(item, (extractors.TypedefDef,
                                     extractors.ParamDef,
                                     extractors.MethodDef )):  # TODO: Any others?
                item.pyName = item.name[2:]
                item.wxDropped = True
        if item.name.startswith('wxEVT_') and 'CATEGORY' not in item.name:
            # give these their actual name so the auto-renamer won't touch them
            item.pyName = item.name


def removeWxPrefix(name):
    """
    Remove the "wx" prefix from a name, except for those which should keep it.
    """
    if name.startswith('wx.') or name.startswith('``wx.'):
        return name

    if name.startswith('wx') and not name.startswith('wxEVT_'):
        name = name[2:]

    if name.startswith('``wx') and not name.startswith('``wxEVT_'):
        name = name[0:2] + name[4:]

    return name



class FixWxPrefix(object):
    """
    A mixin class that can help with removing the wx prefix, or changing it
    in to a "wx.Name" depending on where it is being used from.
    """

    _coreTopLevelNames = None

    def fixWxPrefix(self, name, checkIsCore=False):
        # By default remove the wx prefix like normal
        name = removeWxPrefix(name)
        if not checkIsCore or self.isCore:
            return name

        # Otherwise, if we're not processing the core module currently then check
        # if the name is local or if it resides in core. If it does then return
        # the name as 'wx.Name'
        if FixWxPrefix._coreTopLevelNames is None:
            self._getCoreTopLevelNames()

        testName = name
        if '(' in name:
            testName = name[:name.find('(')]
        testName = testName.split('.')[0]

        if testName in FixWxPrefix._coreTopLevelNames:
            return 'wx.'+name
        else:
            return name

    def _getCoreTopLevelNames(self):
        # Since the real wx.core module may not exist yet, and since actually
        # executing code at this point is probably a bad idea, try parsing the
        # core.pyi file and pulling the top level names from it.
        import ast

        def _processItem(item, names):
            if isinstance(item, ast.Assign):
                for t in item.targets:
                    _processItem(t, names)
            elif isinstance(item, ast.Name):
                names.append(item.id)
            elif isinstance(item, ast.ClassDef):
                names.append(item.name)
            elif isinstance(item, ast.FunctionDef):
                names.append(item.name)
            elif isinstance(item, ast.AnnAssign):
                if isinstance(item.target, ast.Name):
                    names.append(item.target.id)

        names = list()
        filename = 'wx/core.pyi'
        if PY3:
            with open(filename, 'rt', encoding='utf-8') as f:
                text = f.read()
        else:
            with open(filename, 'r') as f:
                text = f.read()
        parseTree = ast.parse(text, filename)
        for item in parseTree.body:
            _processItem(item, names)

        FixWxPrefix._coreTopLevelNames = names

    def cleanName(self, name: str, is_expression: bool = False, fix_wx: bool = True) -> str:
        """Process a C++ name for use in Python code. In all cases, this means
        handling name collisions with Python keywords. For names that will be
        used for an identifier (ex: class, method, constant) - `is_expression`
        is False - this also includes the reserved constant names 'False',
        'True', and 'None'.  When `is_expression` is True, name are allowed to
        include special characters and the reserved constant names - this is
        intended for cleaning up type-hint expressions ans default value
        expressions.

        Finally, the 'wx.' prefix is added if needed.
        """
        for txt in ['const', '*', '&', ' ']:
            name = name.replace(txt, '')
        name = name.replace('::', '.')
        if not is_expression:
            name = re.sub(r'[^a-zA-Z0-9_\.]', '', name)
        if not (is_expression and name in ['True', 'False', 'None']) and keyword.iskeyword(name):
            name = f'_{name}' # Python keyword name collision
        name = name.strip()
        if fix_wx:
            return self.fixWxPrefix(name, True)
        else:
            return removeWxPrefix(name)

    def cleanType(self, type_name: str) -> str:
        """Process a C++ type name for use as a type annotation in Python code.
        Handles translation of common C++ types to Python types, as well as a
        few specific wx types to Python types.
        """
        double_type = 'float' if PY3 else 'double'
        long_type = 'int' if PY3 else 'long'
        type_map = {
            # Some types are guesses, marked with TODO to verify automatic
            # conversion actually happens.  Also, these are the type-names
            # after processing by cleanName (so spaces are removed), or
            # after potentially lopping off an 'Array' prefix.
            # --String types
            'String': 'str',
            'Char': 'str',
            'char': 'str',
            'FileName': 'str', # TODO: check conversion
            # --Int types
            'byte': 'int',
            'short': 'int',
            'Int': 'int',
            'unsigned': 'int',
            'unsignedchar': 'int',
            'unsignedshort': 'int',
            'unsignedint': 'int',
            'time_t': 'int',
            'size_t': 'int',
            'Int32': 'int',
            'long': long_type,
            'unsignedlong': long_type,
            'ulong': long_type,
            'LongLong': long_type,
            # --Float types
            'double': double_type,
            'Double': double_type,
            # --Others
            'void': 'Any',
            'PyObject': 'Any',
            'WindowID': 'int', # defined in wx/defs.h
            'Coord': 'int', # defined in wx/types.h
        }
        type_name = self.cleanName(type_name)
        # Special handling of Vector<type> types -
        if type_name.startswith('Vector<') and type_name.endswith('>'):
            # Special handling for 'Vector<type>' types
            type_name = self.cleanType(type_name[7:-1])
            return f'List[{type_name}]'
        if type_name.startswith('Array'):
            type_name = self.cleanType(type_name[5:])
            if type_name:
                return f'List[{type_name}]'
            else:
                return 'list'
        return type_map.get(type_name, type_name)
    
    def parseNameAndType(self, name_string: str, type_string: Optional[str]) -> Tuple[str, Optional[str]]:
        """Given an identifier name and an optional type annotation, process
        these per cleanName and cleanType. Further performs transforms on the
        identifier name that may be required due to the type annotation.
        Ex. The transformation "any_identifier : ..." -> "*args" requires
        modifying both the identifier name and the annotation.
        """
        name_string = self.cleanName(name_string, fix_wx=False)
        if type_string:
            type_string = self.cleanType(type_string)
            if type_string == '...':
                name_string = '*args'
                type_string = None
        if not type_string:
            type_string = None
        return name_string, type_string


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


def ignoreConstOverloads(node):
    """
    If a method is overloaded and one of them only differs by const-ness,
    then ignore it.
    """
    def _checkOverloads(item):
        overloads = item.all()
        for i in range(len(overloads)):
            for j in range(len(overloads)):
                if i == j:
                    continue
                item1 = overloads[i]
                item2 = overloads[j]
                if item1.ignored or item2.ignored:
                    continue
                if (item1.argsString.replace(' const', '').strip() ==
                    item2.argsString.replace(' const', '').strip()):
                    if item1.isConst:
                        item1.ignore()
                        return
                    elif item2.isConst:
                        item2.ignore()
                        return

    for item in node.items:
        if isinstance(item, extractors.MethodDef) and item.overloads:
            _checkOverloads(item)



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


def fixEventClass(klass, ignoreProtected=True):
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
        else:
            klass.findItem('Clone').factory = True

    # Add a private assignment operator so the back-end (if it's watching out
    # for this) won't try to make copies by assignment.
    klass.addPrivateAssignOp()

    if not ignoreProtected:
        for item in klass.allItems():
            if isinstance(item, extractors.MethodDef) and item.protection == 'protected':
                item.ignore(False)



def fixWindowClass(klass, hideVirtuals=True, ignoreProtected=True):
    """
    Do common tweaks for a window class.
    """
    # NOTE: it may be okay to just do mustHaveApp for top-level windows
    # TODO: look into that possibility
    klass.mustHaveApp()

    # The ctor and Create method transfer ownership of the this pointer to the parent
    for func in klass.findAll(klass.name) + klass.findAll('Create'):
        if isinstance(func, extractors.MethodDef):
            # if a class has an empty ctor it might not have this
            parent = func.findItem('parent')
            if parent:
                parent.transferThis = True
            # if there is an id param give it a default
            id = func.findItem('id') or func.findItem('winid')
            if id and not id.default:
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
        # hiding the fact that they are virtual from the backend generator will
        # greatly reduce the amount of code that needs to be generated. Remove all
        # the virtual flags, and then add it back to a select few.
        removeVirtuals(klass)
        addWindowVirtuals(klass)

    if not ignoreProtected:
        for item in klass.allItems():
            if isinstance(item, extractors.MethodDef) and item.protection == 'protected':
                item.ignore(False)

    fixDefaultAttributesMethods(klass)


def fixDefaultAttributesMethods(klass):
    if not klass.findItem('GetClassDefaultAttributes'):
        m = extractors.MethodDef(
            type='wxVisualAttributes', name='GetClassDefaultAttributes',
            isStatic=True, protection='public',
            items=[extractors.ParamDef(
                type='wxWindowVariant', name='variant', default='wxWINDOW_VARIANT_NORMAL')]
        )
        klass.addItem(m)

    if klass.findItem('GetDefaultAttributes'):
        klass.find('GetDefaultAttributes').mustHaveApp()
    klass.find('GetClassDefaultAttributes').mustHaveApp()


def fixTopLevelWindowClass(klass, hideVirtuals=True, ignoreProtected=True):
    """
    Tweaks for TLWs
    """
    klass.mustHaveApp()

    # TLW tweaks are a little different. We use the function annotation for
    # TransferThis instead of the argument annotation.
    klass.find(klass.name).findOverload('parent').transfer = True
    item = klass.findItem('Create')
    if item:
        item.transferThis = True

    # give the id param a default value
    for name in ['id', 'winid']:
        for item in [klass.findItem('%s.%s' % (klass.name, name)),
                     klass.findItem('Create.%s' % name)]:
            if item:
                item.default = 'wxID_ANY'

    # give title param a default too if it needs it
    for item in [klass.findItem('%s.title' % klass.name), klass.findItem('Create.title')]:
        if item and not item.default:
            item.default = 'wxEmptyString'

    if hideVirtuals:
        removeVirtuals(klass)
        addWindowVirtuals(klass)

    if not ignoreProtected:
        for item in klass.allItems():
            if isinstance(item, extractors.MethodDef) and item.protection == 'protected':
                item.ignore(False)

    fixDefaultAttributesMethods(klass)



def fixSizerClass(klass):
    """
    Remove all virtuals except for CalcMin and RecalcSizes.
    """
    removeVirtuals(klass)
    klass.find('CalcMin').isVirtual = True
    klass.find('RepositionChildren').isVirtual = True
    try:
        klass.find('InformFirstDirection').isVirtual = True
    except extractors.ExtractorError:
        pass

    # in the wxSizer class it is pure-virtual
    if klass.name == 'wxSizer':
        klass.find('CalcMin').isPureVirtual = True


def fixBookctrlClass(klass):
    """
    Add declarations of the pure virtual methods from the base class.
    """
    methods = [
        ("GetPageImage", "virtual int GetPageImage(size_t nPage) const;"),
        ("SetPageImage", "virtual bool SetPageImage(size_t page, int image);"),
        ("GetPageText", "virtual wxString GetPageText(size_t nPage) const;"),
        ("SetPageText", "virtual bool SetPageText(size_t page, const wxString& text);"),
        ("GetSelection", "virtual int GetSelection() const;"),
        ("SetSelection", "virtual int SetSelection(size_t page);"),
        ("ChangeSelection", "virtual int ChangeSelection(size_t page);"),
        ("HitTest", "virtual int HitTest(const wxPoint& pt, long* flags /Out/ = NULL) const;"),
        ("InsertPage", "virtual bool InsertPage(size_t index, wxWindow * page, const wxString & text, bool select = false, int imageId = NO_IMAGE);"),
        ("DeleteAllPages", "virtual bool DeleteAllPages();")
        ]

    for name, decl in methods:
        if not klass.findItem(name):
            klass.addItem(extractors.WigCode(decl))

def fixItemContainerClass(klass, addIsSelected=True):
    """
    Add declarations of the pure virtual methods from the base class.
    """
    methods = [
        ("GetCount", "virtual unsigned int GetCount() const;"),
        ("GetString", "virtual wxString GetString(unsigned int n) const;"),
        ("SetString", "virtual void SetString(unsigned int n, const wxString& s);"),
        ("SetSelection", "virtual void SetSelection(int n);"),
        ("GetSelection", "virtual int GetSelection() const;"),
    ]
    if addIsSelected:
        methods += [
            ("IsSelected", "virtual bool IsSelected(int n) const;"),
            ]

    for name, decl in methods:
        if not klass.findItem(name):
            klass.addItem(extractors.WigCode(decl))


def fixHtmlSetFonts(klass):
    # Use wxArrayInt instead of a C array of ints.
    m = klass.find('SetFonts')
    m.find('sizes').type = 'const wxArrayInt&'
    m.find('sizes').default = ''
    m.argsString = '(const wxString & normal_face, const wxString & fixed_face, const wxArrayInt& sizes)'
    m.setCppCode("""\
        if (sizes->GetCount() != 7) {
            wxPyErr_SetString(PyExc_ValueError, "Sequence of 7 integers expected.");
            return;
        }
        self->SetFonts(*normal_face, *fixed_face, &sizes->Item(0));
        """)


def fixSetStatusWidths(m):
    # We already have a MappedType for wxArrayInt, so just tweak the
    # interface to use that instead of an array size and a const int pointer.
    m.find('n').ignore()
    m.find('widths_field').type = 'const wxArrayInt&'
    m.find('widths_field').name = 'widths'
    m.argsString = '(int n, const wxArrayInt& widths)'
    m.setCppCode("""\
        const int* ptr = &widths->front();
        self->SetStatusWidths(widths->size(), ptr);
        """)


def fixRefCountedClass(klass):
    # Set the Transfer annotation on the ctors, because the C++ objects
    # own themselves and will delete themselves when their C++ refcount
    # drops to zero.
    for item in klass.allItems():
        if isinstance(item, extractors.MethodDef) and item.isCtor:
            item.transfer = True

def fixTextClipboardMethods(klass):
    """
    Adds virtual behavior to Copy/Cut/Paste/Undo/Redo methods, and their Can*
    counterparts, of the given class.

    :param ClassDef klass: The class to modify.
    """
    for name in ('Cut', 'Copy', 'Paste', 'Undo', 'Redo'):
        for method in (name, "Can{}".format(name)):
            try:
                klass.find(method).isVirtual = True
            except extractors.ExtractorError:
                pass


def fixDialogProperty(klass):
    """
    Fix classes derived from EditorDialogProperty to ensure that their
    DisplayEditorDialog method is visible.
    """
    m = klass.find('DisplayEditorDialog')
    m.ignore(False)
    m.find('value').inOut = True


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
    Either turn the virtual flag back on or add a declaration for the subset of
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
        ('OnInternalIdle',           'void OnInternalIdle()'),
        ('GetMainWindowOfCompositeControl',
                                     'wxWindow *GetMainWindowOfCompositeControl()'),
        ('InformFirstDirection',     'bool InformFirstDirection(int direction, int size, int availableOtherDir)'),
        ('SetCanFocus',              'void SetCanFocus(bool canFocus)'),
        ('Destroy',                  'bool Destroy()'),
        ('SetValidator',             'void SetValidator( const wxValidator &validator )'),
        ('GetValidator',             'wxValidator* GetValidator()'),
        ('EnableVisibleFocus',       'void EnableVisibleFocus(bool enabled)'),

        ## What about these?
        #bool HasMultiplePages() const
        #void UpdateWindowUI(long flags = wxUPDATE_UI_NONE);
        #void DoUpdateWindowUI(wxUpdateUIEvent& event) ;
    ]
    if isWindows:
        # does not compile on GTK and macOS.
        publicWindowVirtuals.append( ('CreateAccessible', 'wxAccessible* CreateAccessible()') )

    protectedWindowVirtuals = [
        ('ProcessEvent',              'bool ProcessEvent(wxEvent & event)'),
        ('DoEnable',                  'void DoEnable(bool enable)'),
        ('DoGetPosition',             'void DoGetPosition(int *x, int *y) const'),
        ('DoGetSize',                 'void DoGetSize(int *width, int *height) const'),
        ('DoGetClientSize',           'void DoGetClientSize(int *width, int *height) const'),
        ('DoGetBestSize',             'wxSize DoGetBestSize() const'),
        ('DoGetBestClientSize',       'wxSize DoGetBestClientSize() const'),
        ('DoSetSize',                 'void DoSetSize(int x, int y, int width, int height, int sizeFlags)'),
        ('DoSetClientSize',           'void DoSetClientSize(int width, int height)'),
        ('DoSetSizeHints',            'void DoSetSizeHints( int minW, int minH, int maxW, int maxH, int incW, int incH )'),
        ('DoMoveWindow',              'void DoMoveWindow(int x, int y, int width, int height)'),
        ('DoSetWindowVariant',        'void DoSetWindowVariant( wxWindowVariant variant)'),
        ('GetDefaultBorder',          'wxBorder GetDefaultBorder() const'),
        ('GetDefaultBorderForControl','wxBorder GetDefaultBorderForControl() const'),
        ('DoFreeze',                  'void DoFreeze()'),
        ('DoThaw',                    'void DoThaw()'),
        ('HasTransparentBackground',  'bool HasTransparentBackground()'),
        ('TryBefore',                 'bool TryBefore(wxEvent& event)'),
        ('TryAfter',                  'bool TryAfter(wxEvent& event)'),

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


def addSipConvertToSubClassCode(klass):
    """
    Teach SIP how to convert to specific subclass types
    """
    klass.addItem(extractors.WigCode("""\
    %ConvertToSubClassCode
        const wxClassInfo* info   = sipCpp->GetClassInfo();
        wxString           name   = info->GetClassName();
        bool               exists = sipFindType(name.c_str()) != NULL;
        while (info && !exists) {
            info = info->GetBaseClass1();
            name = info->GetClassName();
            exists = sipFindType(name.c_str()) != NULL;
        }
        if (info)
            sipType = sipFindType(name.c_str());
        else
            sipType = NULL;
    %End
    """))


def getEtgFiles(names):
    """
    Create a list of the files from the basenames in the names list that
    correspond to files in the etg folder.
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



def copyClassDef(klass, newName):
    """
    Make a copy of a class object and give it a new name.
    """
    oldName = klass.name
    klass = copy.deepcopy(klass)
    assert isinstance(klass, extractors.ClassDef)
    klass.name = newName
    for ctor in klass.find(oldName).all():
        ctor.name = newName
    if klass.findItem('~'+oldName):
        klass.find('~'+oldName).name = '~'+newName
    return klass

#---------------------------------------------------------------------------


def getWrapperGenerator():
    """
    A simple factory function to create a wrapper generator class of the desired type.
    """
    if '--swig' in sys.argv:
        from etgtools import swig_generator
        gClass = swig_generator.SwigWrapperGenerator
    elif '--sip' in sys.argv:
        from etgtools import sip_generator
        gClass = sip_generator.SipWrapperGenerator
    else:
        # The default is sip
        from etgtools import sip_generator
        gClass = sip_generator.SipWrapperGenerator
    return gClass()


def getDocsGenerator():
    if '--nodoc' in sys.argv:
        from etgtools import generators
        return generators.StubbedDocsGenerator()
    elif '--sphinx' in sys.argv:
        from etgtools import sphinx_generator
        return sphinx_generator.SphinxGenerator()
    else:
        # the current default is sphinx
        from etgtools import sphinx_generator
        return sphinx_generator.SphinxGenerator()



def runGenerators(module):
    checkForUnitTestModule(module)

    generators = list()

    # Create the code generator selected from command line args
    generators.append(getWrapperGenerator())

    # Toss in the PI generator too
    from etgtools import pi_generator
    generators.append(pi_generator.PiWrapperGenerator())

    # Now the item map generator
    from etgtools import map_generator
    generators.append((map_generator.ItemMapGenerator()))

    # And finally add the documentation generator
    generators.append(getDocsGenerator())

    # run the generators
    for g in generators:
        g.generate(module)



def checkForUnitTestModule(module):
    pathname = 'unittests/test_%s.py' % module.name
    if os.path.exists(pathname) or not module.check4unittest:
        return
    print('WARNING: Unittest module (%s) not found!' % pathname)



def addEnableSystemTheme(klass, klassName):
    m = extractors.MethodDef(name='EnableSystemTheme', type='void',
        items=[extractors.ParamDef(type='bool', name='enable', default='true')])
    m.briefDoc = "Can be used to disable the system theme of controls using it by default."
    m.detailedDoc = [textwrap.dedent("""\
        On Windows there an alternative theme available for the list and list-like
        controls since Windows Vista. This theme is used by Windows Explorer list
        and tree view and so is arguably more familiar to the users than the standard
        appearance of these controls. This class automatically uses the new theme,
        but if that is not desired then this method can be used to turn it off.

        Please note that this method should be called before the widget is
        actually created, using the 2-phase create pattern. Something like this::

            # This creates the object, but not the window
            widget = {}()

            # Disable the system theme
            widget.EnableSystemTheme(False)

            # Now create the window
            widget.Create(parent, wx.ID_ANY)

        This method has no effect on other platorms
        """.format(klassName))]

    klass.addItem(m)


#---------------------------------------------------------------------------

def addGetIMMethodTemplate(module, klass, fields):
    """
    Add a bit of code to the module, and add a GetIM method to the klass which
    returns an immutable representation self.
    """
    name = klass.pyName or klass.name
    if name.startswith('wx'):
        name = name[2:]

    module.addPyCode("""\
        from collections import namedtuple
        _im_{name} = namedtuple('_im_{name}', {fields})
        del namedtuple
        """.format(name=name, fields=str(fields)))

    klass.addPyMethod('GetIM', '(self)',
        doc="""\
            Returns an immutable representation of the ``wx.{name}`` object, based on ``namedtuple``.

            This new object is hashable and can be used as a dictionary key,
            be added to sets, etc.  It can be converted back into a real ``wx.{name}``
            with a simple statement like this: ``obj = wx.{name}(imObj)``.
            """.format(name=name),
        body="return _im_{name}(*self.Get())".format(name=name)
        )

#---------------------------------------------------------------------------

def convertTwoIntegersTemplate(CLASS):
    # Note: The GIL is already acquired where this code is used.
    return """\
   // is it just a typecheck?
   if (!sipIsErr) {{
       // is it already an instance of {CLASS}?
       if (sipCanConvertToType(sipPy, sipType_{CLASS}, SIP_NO_CONVERTORS))
           return 1;

       if (wxPyNumberSequenceCheck(sipPy, 2)) {{
           return 1;
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
    *sipCppPtr = new {CLASS}(wxPyInt_AsLong(o1), wxPyInt_AsLong(o2));
    Py_DECREF(o1);
    Py_DECREF(o2);
    return SIP_TEMPORARY;
    """.format(**locals())


def convertFourIntegersTemplate(CLASS):
    # Note: The GIL is already acquired where this code is used.
    return """\
    // is it just a typecheck?
    if (!sipIsErr) {{
        // is it already an instance of {CLASS}?
        if (sipCanConvertToType(sipPy, sipType_{CLASS}, SIP_NO_CONVERTORS))
            return 1;

        if (wxPyNumberSequenceCheck(sipPy, 4)) {{
            return 1;
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
    *sipCppPtr = new {CLASS}(wxPyInt_AsLong(o1), wxPyInt_AsLong(o2),
                             wxPyInt_AsLong(o3), wxPyInt_AsLong(o4));
    Py_DECREF(o1);
    Py_DECREF(o2);
    Py_DECREF(o3);
    Py_DECREF(o4);
    return SIP_TEMPORARY;
    """.format(**locals())



def convertTwoDoublesTemplate(CLASS):
    # Note: The GIL is already acquired where this code is used.
    return """\
    // is it just a typecheck?
    if (!sipIsErr) {{
        // is it already an instance of {CLASS}?
        if (sipCanConvertToType(sipPy, sipType_{CLASS}, SIP_NO_CONVERTORS))
            return 1;

       if (wxPyNumberSequenceCheck(sipPy, 2)) {{
           return 1;
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
    # Note: The GIL is already acquired where this code is used.
    return """\
    // is it just a typecheck?
    if (!sipIsErr) {{
        // is it already an instance of {CLASS}?
        if (sipCanConvertToType(sipPy, sipType_{CLASS}, SIP_NO_CONVERTORS))
            return 1;

        if (wxPyNumberSequenceCheck(sipPy, 4)) {{
            return 1;
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
    Py_DECREF(o3);
    Py_DECREF(o4);
    return SIP_TEMPORARY;
    """.format(**locals())



#---------------------------------------------------------------------------
# Templates for creating wrappers for type-specific wxList and wxArray classes


def wxListWrapperTemplate(ListClass, ItemClass, module, RealItemClass=None,
                          includeConvertToType=False, fakeListClassName=None,
                          header_extra=''):
    if RealItemClass is None:
        RealItemClass = ItemClass

    if fakeListClassName:
        TypeDef = "typedef %s %s;" % (ListClass, fakeListClassName)
        ListClass = fakeListClassName
    else:
        TypeDef = ""

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
        {header_extra}
        {TypeDef}
        class {ListClass}_iterator {{
        public:
            {ListClass}_iterator({ListClass}::compatibility_iterator start)
                : m_node(start) {{}}

            {ItemClass}* __next__() {{
                {RealItemClass}* obj = NULL;
                if (m_node) {{
                    obj = ({RealItemClass}*) m_node->GetData();
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

    PyObject* __iter__();
    %MethodCode
        return PyObject_SelfIter(sipSelf);
    %End
}};

class {ListClass}
{{
    %TypeHeaderCode
        {header_extra}
        {TypeDef}
    %End
public:
    Py_ssize_t __len__();
    %MethodCode
        sipRes = sipCpp->size();
    %End

    {ItemClass}* __getitem__(long index);
    %MethodCode
        if (0 > index)
            index += sipCpp->size();

        if (index < sipCpp->size() && (0 <= index)) {{
            {ListClass}::compatibility_iterator node = sipCpp->Item(index);
            if (node)
                sipRes = ({ItemClass}*)node->GetData();
        }}
        else {{
            wxPyErr_SetString(PyExc_IndexError, "sequence index out of range");
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
            wxPyErr_SetString(PyExc_ValueError,
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
        else if (PyBytes_Check(sipPy) || PyUnicode_Check(sipPy))
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



def wxArrayWrapperTemplate(ArrayClass, ItemClass, module, itemIsPtr=False, getItemCopy=False):
    moduleName = module.module
    ArrayClass_pyName = removeWxPrefix(ArrayClass)
    itemRef = '*' if itemIsPtr else '&'
    itemDeref = '' if itemIsPtr else '*'
    addrOf = '' if itemIsPtr else '&'

    # *** TODO: This can probably be done in a way that is not SIP-specific.
    # Try creating extractor objects from scratch and attach cppMethods to
    # them as needed, etc..

    if not getItemCopy:
        getitemMeth = '''\
        {ItemClass}{itemRef} __getitem__(long index);
        %MethodCode
            if (0 > index)
                index += sipCpp->GetCount();

            if ((index < sipCpp->GetCount()) && (0 <= index)) {{
                sipRes = {addrOf}sipCpp->Item(index);
            }}
            else {{
                wxPyErr_SetString(PyExc_IndexError, "sequence index out of range");
                sipError = sipErrorFail;
            }}
        %End
        '''.format(**locals())
    else:
        getitemMeth = '''\
        {ItemClass}* __getitem__(long index) /Factory/;
        %MethodCode
            if (0 > index)
                index += sipCpp->GetCount();
            if ((index < sipCpp->GetCount()) && (0 <= index)) {{
                sipRes = new {ItemClass}(sipCpp->Item(index));
            }}
            else {{
                wxPyErr_SetString(PyExc_IndexError, "sequence index out of range");
                sipError = sipErrorFail;
            }}
        %End
        '''.format(**locals())


    return extractors.WigCode('''\
class {ArrayClass}
{{
public:
    Py_ssize_t __len__();
    %MethodCode
        sipRes = sipCpp->GetCount();
    %End

    {getitemMeth}

    int __contains__({ItemClass}{itemRef} obj);
    %MethodCode
        int idx = sipCpp->Index({itemDeref}obj, false);
        sipRes = idx != wxNOT_FOUND;
    %End

    void append({ItemClass}{itemRef} obj);
    %MethodCode
        sipCpp->Add({itemDeref}obj);
    %End

    // TODO:  add support for index(value, [start, [stop]])
    int index({ItemClass}{itemRef} obj);
    %MethodCode
        int idx = sipCpp->Index({itemDeref}obj, false);
        if (idx == wxNOT_FOUND) {{
            sipError = sipErrorFail;
            wxPyErr_SetString(PyExc_ValueError,
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



# Same as the above, but for use with  WX_DEFINE_ARRAY_PTR
def wxArrayPtrWrapperTemplate(ArrayClass, ItemClass, module):
    moduleName = module.module
    ArrayClass_pyName = removeWxPrefix(ArrayClass)

    # *** TODO: This can probably be done in a way that is not SIP-specfic.
    # Try creating extractor objects from scratch and attach cppMethods to
    # them as needed, etc..

    return extractors.WigCode('''\
class {ArrayClass}
{{
public:
    Py_ssize_t __len__();
    %MethodCode
        sipRes = sipCpp->GetCount();
    %End

    {ItemClass}* __getitem__(long index);
    %MethodCode
        if (0 > index)
            index += sipCpp->GetCount();

        if ((index < sipCpp->GetCount()) && (0 <= index)) {{
            sipRes = sipCpp->Item(index);
        }}
        else {{
            wxPyErr_SetString(PyExc_IndexError, "sequence index out of range");
            sipError = sipErrorFail;
        }}
    %End

    int __contains__({ItemClass}* obj);
    %MethodCode
        int idx = sipCpp->Index(obj, false);
        sipRes = idx != wxNOT_FOUND;
    %End

    void append({ItemClass}* obj);
    %MethodCode
        sipCpp->Add(obj);
    %End

    // TODO:  add support for index(value, [start, [stop]])
    int index({ItemClass}* obj);
    %MethodCode
        int idx = sipCpp->Index(obj, false);
        if (idx == wxNOT_FOUND) {{
            sipError = sipErrorFail;
            wxPyErr_SetString(PyExc_ValueError,
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
    that uses one of those types then the C array overload should just be
    ignored. But for those cases where the C array is the only option then this
    helper can be used to make the array from a sequence.
    """

    cppCode = """\
// Convert a Python sequence of {objType} objects, or items that can be converted
// to {objType} into a C array of {objType} instances.
static
{objType}* {objType}_array_helper(PyObject* source, size_t *count)
{{
    {objType}* array;
    Py_ssize_t idx, len;
    wxPyThreadBlocker blocker;

    // ensure that it is a sequence
    if (! PySequence_Check(source))
        goto error0;
    // ensure it is not a string or unicode object (they are sequences too)
    else if (PyBytes_Check(source) || PyUnicode_Check(source))
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
# type helpers

def guessTypeInt(v):
    if isinstance(v, extractors.EnumValueDef):
        return True
    if isinstance(v, extractors.DefineDef) and '"' not in v.value:
        return True
    type = v.type.replace('const', '')
    type = type.replace(' ', '')
    if type in ['int', 'long', 'byte', 'size_t', 'wxCoord', 'wxEventType']:
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
    for t in ['wxString', 'wxChar', 'char*', 'char *', 'wchar_t*', 'wchar_t *']:
        if t in v.type:
            return True
    return False

#---------------------------------------------------------------------------
# Tweakers to generate C++ stubs for cases where a feature is optional. By
# generating stubs then we can still provide the wrapper classes but simply
# have them raise NotImplemented errors or whatnot.

def generateStubs(cppFlag, module, excludes=[], typeValMap={},
                  extraHdrCode=None, extraCppCode=None):
    """
    Generate C++ stubs for all items in the module, except those that are
    in the optional excludes list.
    """
    # First add a define for the cppFlag (like wxUSE_SOME_FEATURE) so the user
    # code has a way to check if an optional classis available before using it
    # and getting an exception.
    assert isinstance(module, extractors.ModuleDef)
    if not module.findItem(cppFlag):
        module.addItem(extractors.DefineDef(name=cppFlag, value='0'))
        excludes.append(cppFlag)

    # Copy incoming typeValMap so it can be updated with some stock types
    import copy
    typeValMap = copy.copy(typeValMap)
    typeValMap.update({
        'int': '0',
        'long': '0',
        'unsigned int': '0',
        'bool': 'false',
        'double': '0.0',
        'wxString': 'wxEmptyString',
        'const wxString &': 'wxEmptyString',
        'wxString &': 'wxEmptyString',
        'wxSize': 'wxDefaultSize',
        'wxPoint': 'wxDefaultPosition',
        'wxFileOffset': '0',
        'wxColour': 'wxNullColour',
        'wxBitmap': 'wxNullBitmap',
        'wxBitmap &': 'wxNullBitmap',
        'wxImage': 'wxNullImage',
        'wxVisualAttributes': 'wxVisualAttributes()',
        })

    code = _StubCodeHolder(cppFlag)

    # Next add forward declarations of all classes in case they refer to
    # each other.
    for item in module:
        if isinstance(item, extractors.ClassDef):
            code.hdr.append('class {};'.format(item.name))

    if extraHdrCode:
        code.hdr.append(extraHdrCode)

    if extraCppCode:
        code.cpp.append(extraCppCode)

    # Now write code for all the items in the module.
    for item in module:
        if item.name in excludes:
            continue

        dispatchMap = {
            extractors.DefineDef    : _generateDefineStub,
            extractors.GlobalVarDef : _generateGlobalStub,
            extractors.EnumDef      : _generateEnumStub,
            extractors.ClassDef     : _generateClassStub,
            extractors.PyCodeDef    : _ignore,
            }
        func = dispatchMap.get(type(item), None)
        if func is None:
            print('WARNING: Unable to generate stub for {}, type {}'.format(
                item.name, type(item)))
        else:
            func(code, item, typeValMap)

    # Add the code to the module header
    module.addHeaderCode(code.renderHdr())
    if code.cpp:
        # and possibly the module's C++ file
        module.addCppCode(code.renderCpp())


# A simple class for holding lists of code snippets for the header and
# possibly the C++ file.
class _StubCodeHolder:
    def __init__(self, flag):
        self.flag = flag
        self.hdr = []
        self.cpp = []

    def renderHdr(self):
        return self.doRender(self.hdr)

    def renderCpp(self):
        return self.doRender(self.cpp)

    def doRender(self, lst):
        if not lst:
            return ''
        code = ('#if !{}\n'.format(self.flag) +
                '\n'.join(lst) +
                '\n#endif //!{}\n'.format(self.flag))
        return code



def _ignore(*args):
    pass


def _generateDefineStub(code, define, typeValMap):
    code.hdr.append('#define {}  {}'.format(define.name, define.value))


def _generateGlobalStub(code, glob, typeValMap):
    code.hdr.append('extern {} {};'.format(glob.type, glob.name))
    if glob.type == 'const char*':
        code.cpp.append('{} {} = "";'.format(glob.type, glob.name))
    else:
        code.cpp.append('{} {};'.format(glob.type, glob.name))


def _generateEnumStub(code, enum, typeValMap):
    name = '' if enum.name.startswith('@') else enum.name
    code.hdr.append('\nenum {} {{'.format(name))
    for item in enum:
        code.hdr.append('    {},'.format(item.name))
    code.hdr.append('};')


def _generateClassStub(code, klass, typeValMap):
    if not klass.bases:
        code.hdr.append('\nclass {} {{'.format(klass.name))
    else:
        code.hdr.append('\nclass {} : {} {{'.format(klass.name,
            ', '.join(['public ' + base for base in klass.bases])))
    code.hdr.append('public:')

    for item in klass:
        dispatchMap = {
            extractors.MethodDef : _generateMethodStub,
            extractors.WigCode   : lambda c, i, t: None,  # ignore this type
            }
        func = dispatchMap.get(type(item), None)
        if func is None:
            print('WARNING: Unable to generate stub for {}.{}, type {}'.format(
                klass.name, item.name, type(item)))
        else:
            func(code, item, typeValMap)

    code.hdr.append('};')


def _generateMethodStub(code, method, typeValMap):
    assert isinstance(method, extractors.MethodDef)
    if method.ignored:
        return
    decl = '    '
    if method.isVirtual:
        decl += 'virtual '
    if method.isStatic:
        decl += 'static '
    if method.isCtor or method.isDtor:
        decl += '{}'.format(method.name)
    else:
        decl += '{} {}'.format(method.type, method.name)
    decl += method.argsString
    if method.isPureVirtual:
        decl += ';'
    code.hdr.append(decl)

    if not method.isPureVirtual:
        impl = '        { '
        if method.isCtor or method.isStatic:
            impl += 'wxPyRaiseNotImplemented(); '

        if not (method.isCtor or method.isDtor):
            if not method.type == 'void':
                rval = typeValMap.get(method.type, None)
                if rval is None and '*' in method.type:
                    rval = 'NULL'
                if rval is None:
                    print("WARNING: I don't know how to return a '{}' value.".format(method.type))
                    rval = '0'
                impl += 'return {}; '.format(rval)

        impl += '}\n'
        code.hdr.append(impl)

    for overload in method.overloads:
        _generateMethodStub(code, overload, typeValMap)

#---------------------------------------------------------------------------
