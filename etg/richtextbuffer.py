#---------------------------------------------------------------------------
# Name:        etg/richtextbuffer.py
# Author:      Robin Dunn
#
# Created:     23-Mar-2013
# Copyright:   (c) 2013-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_richtext"
NAME      = "richtextbuffer"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxTextAttrDimension",
           "wxTextAttrDimensions",
           "wxTextAttrSize",
           "wxTextAttrDimensionConverter",
           "wxTextAttrBorder",
           "wxTextAttrBorders",
           "wxTextAttrShadow",
           "wxTextBoxAttr",
           "wxRichTextAttr",
           "wxRichTextProperties",
           "wxRichTextFontTable",
           "wxRichTextRange",
           "wxRichTextSelection",
           "wxRichTextDrawingContext",
           "wxRichTextObject",
           "wxRichTextCompositeObject",
           "wxRichTextParagraphLayoutBox",
           "wxRichTextBox",
           "wxRichTextField",
           "wxRichTextFieldType",
           "wxRichTextFieldTypeStandard",
           "wxRichTextLine",
           "wxRichTextParagraph",
           "wxRichTextPlainText",
           "wxRichTextImageBlock",
           "wxRichTextImage",
           "wxRichTextBuffer",
           "wxRichTextCell",
           "wxRichTextTable",
           "wxRichTextObjectAddress",
           "wxRichTextCommand",
           "wxRichTextAction",
           "wxRichTextFileHandler",
           "wxRichTextPlainTextHandler",
           "wxRichTextDrawingHandler",
           "wxRichTextBufferDataObject",
           "wxRichTextRenderer",
           "wxRichTextStdRenderer",

           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/richtext/richtextbuffer.h>')

    module.addItem(
        tools.wxArrayWrapperTemplate('wxRichTextRangeArray', 'wxRichTextRange', module))
    module.addItem(
        tools.wxArrayWrapperTemplate('wxRichTextAttrArray', 'wxRichTextAttr', module))
    module.addItem(
        tools.wxArrayWrapperTemplate('wxRichTextVariantArray', 'wxVariant', module))
    module.addItem(
        tools.wxListWrapperTemplate('wxRichTextObjectList', 'wxRichTextObject', module))

    # Can this even work?  Apparently it does.
    module.addItem(
        tools.wxArrayPtrWrapperTemplate('wxRichTextObjectPtrArray', 'wxRichTextObject', module))
    module.addItem(
        tools.wxArrayWrapperTemplate('wxRichTextObjectPtrArrayArray', 'wxRichTextObjectPtrArray', module))


    module.find('wxRICHTEXT_ALL').ignore()
    module.find('wxRICHTEXT_NONE').ignore()
    module.find('wxRICHTEXT_NO_SELECTION').ignore()
    code = etgtools.PyCodeDef("""\
        RICHTEXT_ALL = RichTextRange(-2, -2)
        RICHTEXT_NONE = RichTextRange(-1, -1)
        RICHTEXT_NO_SELECTION = RichTextRange(-2, -2)
        """)
    module.insertItemAfter(module.find('wxRichTextRange'), code)

    module.insertItem(0, etgtools.WigCode("""\
        // forward declarations
        class wxRichTextFloatCollector;
        """))


    #-------------------------------------------------------
    c = module.find('wxTextAttrDimension')
    assert isinstance(c, etgtools.ClassDef)
    c.find('SetValue').findOverload('units').ignore()
    c.addCppMethod('int', '__nonzero__', '()', "return self->IsValid();")
    c.addCppMethod('int', '__bool__', '()', "return self->IsValid();")

    #-------------------------------------------------------
    c = module.find('wxTextAttrDimensions')
    tools.ignoreConstOverloads(c)
    c.addCppMethod('int', '__nonzero__', '()', "return self->IsValid();")
    c.addCppMethod('int', '__bool__', '()', "return self->IsValid();")

    #-------------------------------------------------------
    c = module.find('wxTextAttrSize')
    tools.ignoreConstOverloads(c)
    c.find('SetWidth').findOverload('units').ignore()
    c.find('SetHeight').findOverload('units').ignore()
    c.addCppMethod('int', '__nonzero__', '()', "return self->IsValid();")
    c.addCppMethod('int', '__bool__', '()', "return self->IsValid();")

    #-------------------------------------------------------
    c = module.find('wxTextAttrBorder')
    tools.ignoreConstOverloads(c)
    c.addCppMethod('int', '__nonzero__', '()', "return self->IsValid();")
    c.addCppMethod('int', '__bool__', '()', "return self->IsValid();")


    #-------------------------------------------------------
    c = module.find('wxTextAttrBorders')
    tools.ignoreConstOverloads(c)
    c.addCppMethod('int', '__nonzero__', '()', "return self->IsValid();")
    c.addCppMethod('int', '__bool__', '()', "return self->IsValid();")


    #-------------------------------------------------------
    c = module.find('wxTextAttrShadow')
    tools.ignoreConstOverloads(c)


    #-------------------------------------------------------
    c = module.find('wxTextBoxAttr')
    tools.ignoreConstOverloads(c)


    #-------------------------------------------------------
    c = module.find('wxRichTextAttr')
    tools.ignoreConstOverloads(c)


    #-------------------------------------------------------
    c = module.find('wxRichTextProperties')
    tools.ignoreConstOverloads(c)

    c.find('SetProperty').findOverload('bool').ignore()
    c.find('operator[]').ignore()

    #-------------------------------------------------------
    c = module.find('wxRichTextSelection')
    tools.ignoreConstOverloads(c)
    c.addCppMethod('int', '__nonzero__', '()', "return self->IsValid();")
    c.addCppMethod('int', '__bool__', '()', "return self->IsValid();")
    c.find('operator[]').ignore()


    #-------------------------------------------------------
    c = module.find('wxRichTextRange')
    tools.addAutoProperties(c)

    # wxRichTextRange typemap
    c.convertFromPyObject = tools.convertTwoIntegersTemplate('wxRichTextRange')

    c.addCppMethod('PyObject*', 'Get', '()', """\
        wxPyThreadBlocker blocker;
        return sipBuildResult(0, "(ii)", self->GetStart(), self->GetEnd());
        """,
        pyArgsString="() -> (start, end)",
        briefDoc="Return the start and end properties as a tuple.")

    tools.addGetIMMethodTemplate(module, c, ['Start', 'End'])

    # Add sequence protocol methods and other goodies
    c.addPyMethod('__str__', '(self)',             'return str(self.Get())')
    c.addPyMethod('__repr__', '(self)',            'return "RichTextRange"+str(self.Get())')
    c.addPyMethod('__len__', '(self)',             'return len(self.Get())')
    c.addPyMethod('__nonzero__', '(self)',         'return self.Get() != (0,0)')
    c.addPyMethod('__bool__', '(self)',            'return self.Get() != (0,0)')
    c.addPyMethod('__reduce__', '(self)',          'return (RichTextRange, self.Get())')
    c.addPyMethod('__getitem__', '(self, idx)',    'return self.Get()[idx]')
    c.addPyMethod('__setitem__', '(self, idx, val)',
                  """\
                  if idx == 0: self.Start = val
                  elif idx == 1: self.End = val
                  else: raise IndexError
                  """)
    c.addPyCode('RichTextRange.__safe_for_unpickling__ = True')


    #-------------------------------------------------------
    def _fixDrawObject(c, addMissingVirtuals=True):
        assert isinstance(c, etgtools.ClassDef)
        if c.findItem('HitTest'):
            c.find('HitTest.textPosition').out = True
            c.find('HitTest.obj').out = True
            c.find('HitTest.contextObj').out = True

        if c.findItem('FindPosition'):
            c.find('FindPosition.pt').out = True
            c.find('FindPosition.height').out = True

        if c.findItem('GetBoxRects'):
            c.find('GetBoxRects.marginRect').out = True
            c.find('GetBoxRects.borderRect').out = True
            c.find('GetBoxRects.contentRect').out = True
            c.find('GetBoxRects.paddingRect').out = True
            c.find('GetBoxRects.outlineRect').out = True

        if c.findItem('GetTotalMargin'):
            c.find('GetTotalMargin.leftMargin').out = True
            c.find('GetTotalMargin.rightMargin').out = True
            c.find('GetTotalMargin.topMargin').out = True
            c.find('GetTotalMargin.bottomMargin').out = True

        if c.findItem('CalculateRange'):
            c.find('CalculateRange.end').out = True  # TODO: should it be an inOut?

        if c.findItem('Clone'):
            c.find('Clone').factory = True
        else:
            c.addItem(etgtools.WigCode("""\
            virtual wxRichTextObject* Clone() const /Factory/;
            """))

        # These are the pure virtuals in the base class. SIP needs to see that
        # all the derived classes have an implementation, otherwise it will
        # consider them to be ABCs.
        if not c.findItem('Draw') and addMissingVirtuals:
            c.addItem(etgtools.WigCode("""\
                virtual bool Draw(wxDC& dc, wxRichTextDrawingContext& context,
                                  const wxRichTextRange& range,
                                  const wxRichTextSelection& selection,
                                  const wxRect& rect, int descent, int style);"""))
        if not c.findItem('Layout') and addMissingVirtuals:
            c.addItem(etgtools.WigCode("""\
                virtual bool Layout(wxDC& dc, wxRichTextDrawingContext& context,
                                    const wxRect& rect, const wxRect& parentRect,
                                    int style);"""))

        # TODO: Some of these args are output parameters.  How should they be dealt with?
        if not c.findItem('GetRangeSize') and addMissingVirtuals:
            c.addItem(etgtools.WigCode("""\
                virtual bool GetRangeSize(const wxRichTextRange& range, wxSize& size,
                              int& descent,
                              wxDC& dc, wxRichTextDrawingContext& context, int flags,
                              const wxPoint& position = wxPoint(0,0),
                              const wxSize& parentSize = wxDefaultSize,
                              wxArrayInt* partialExtents = NULL) const;"""))


    #-------------------------------------------------------
    c = module.find('wxRichTextObject')
    #c.find('ImportFromXML').ignore()
    tools.ignoreConstOverloads(c)
    _fixDrawObject(c)


    #-------------------------------------------------------
    c = module.find('wxRichTextCompositeObject')
    tools.ignoreConstOverloads(c)
    _fixDrawObject(c, addMissingVirtuals=False)


    #-------------------------------------------------------
    c = module.find('wxRichTextParagraphLayoutBox')
    tools.ignoreConstOverloads(c)
    _fixDrawObject(c)

    c.find('MoveAnchoredObjectToParagraph.from').name = 'from_'
    c.find('MoveAnchoredObjectToParagraph.to').name = 'to_'
    c.find('DoNumberList.def').name = 'styleDef'
    c.find('SetListStyle.def').name = 'styleDef'

    #-------------------------------------------------------
    c = module.find('wxRichTextBox')
    _fixDrawObject(c)

    #-------------------------------------------------------
    c = module.find('wxRichTextCell')
    _fixDrawObject(c)

    #-------------------------------------------------------
    c = module.find('wxRichTextField')
    _fixDrawObject(c)


    #-------------------------------------------------------
    c = module.find('wxRichTextLine')
    tools.ignoreConstOverloads(c)
    c.find('SetRange.from').name = 'from_'
    c.find('SetRange.to').name = 'to_'
    c.find('Clone').factory = True

    #-------------------------------------------------------
    c = module.find('wxRichTextParagraph')
    _fixDrawObject(c)

    # These methods use an untyped wxList, but since we know what is in it
    # we'll make a fake typed list for wxPython so we can know what kinds of
    # values to get from it.
    module.addItem(
        tools.wxListWrapperTemplate('wxList', 'wxRichTextObject', module,
                                    fakeListClassName='wxRichTextObjectList_'))
    c.find('MoveToList.list').type = 'wxRichTextObjectList_&'
    c.find('MoveFromList.list').type = 'wxRichTextObjectList_&'
    # TODO: figure out why wxvector.sip doesn't work for this
    c.find('GetLines').type = 'PyObject*'
    c.find('GetLines').setCppCode("""\
        wxPyThreadBlocker blocker;
        PyObject* result = PyList_New(0);
        const wxRichTextLineVector& vector = self->GetLines();
        for (size_t idx=0; idx < vector.size(); idx++) {{
            PyObject* obj;
            wxRichTextLine* item = new wxRichTextLine(*vector.at(idx));
            obj = wxPyConstructObject((void*)item, "wxRichTextLine", true);
            PyList_Append(result, obj);
            Py_DECREF(obj);
        }}
        return result;
        """)


    #-------------------------------------------------------
    c = module.find('wxRichTextPlainText')
    _fixDrawObject(c)

    #-------------------------------------------------------
    c = module.find('wxRichTextImage')
    _fixDrawObject(c)
    c.find('LoadAndScaleImageCache.changed').inOut = True

    #-------------------------------------------------------
    c = module.find('wxRichTextBuffer')
    tools.ignoreConstOverloads(c)
    _fixDrawObject(c)

    # More untyped wxLists
    module.addItem(
        tools.wxListWrapperTemplate('wxList', 'wxRichTextFileHandler', module,
                                    fakeListClassName='wxRichTextFileHandlerList'))
    c.find('GetHandlers').type = 'wxRichTextFileHandlerList&'
    c.find('GetHandlers').noCopy = True

    module.addItem(
        tools.wxListWrapperTemplate('wxList', 'wxRichTextDrawingHandler', module,
                                    fakeListClassName='wxRichTextDrawingHandlerList'))
    c.find('GetDrawingHandlers').type = 'wxRichTextDrawingHandlerList&'
    c.find('GetDrawingHandlers').noCopy = True

    # TODO: Need a template to wrap STRING_HASH_MAP
    c.find('GetFieldTypes').ignore()

    c.find('AddHandler.handler').transfer = True
    c.find('InsertHandler.handler').transfer = True

    c.find('AddDrawingHandler.handler').transfer = True
    c.find('InsertDrawingHandler.handler').transfer = True

    c.find('AddFieldType.fieldType').transfer = True

    # TODO:  Transfer ownership with AddEventHandler?  TransferBack with Remove?


    c.find('FindHandler').renameOverload('name', 'FindHandlerByName')
    c.find('FindHandler').renameOverload('extension', 'FindHandlerByExtension')
    c.find('FindHandler').pyName = 'FindHandlerByType'

    c.find('FindHandlerFilenameOrType').pyName = 'FindHandlerByFilename'

    c.find('GetExtWildcard').ignore()
    c.addCppMethod('PyObject*', 'GetExtWildcard', '(bool combine=false, bool save=false)',
        doc="""\
            Gets a wildcard string for the file dialog based on all the currently
            loaded richtext file handlers, and a list that can be used to map
            those filter types to the file handler type.""",
        body="""\
            wxString wildcards;
            wxArrayInt types;
            wildcards = wxRichTextBuffer::GetExtWildcard(combine, save, &types);

            wxPyThreadBlocker blocker;
            PyObject* list = PyList_New(0);
            for (size_t i=0; i < types.GetCount(); i++) {
                PyObject* number = wxPyInt_FromLong(types[i]);
                PyList_Append(list, number);
                Py_DECREF(number);
            }
            PyObject* tup = PyTuple_New(2);
            PyTuple_SET_ITEM(tup, 0, wx2PyString(wildcards));
            PyTuple_SET_ITEM(tup, 1, list);
            return tup;
            """,
        isStatic=True)

    #-------------------------------------------------------
    c = module.find('wxRichTextTable')
    tools.ignoreConstOverloads(c)
    _fixDrawObject(c)


    #-------------------------------------------------------
    c = module.find('wxRichTextObjectAddress')
    tools.ignoreConstOverloads(c)


    #-------------------------------------------------------
    c = module.find('wxRichTextCommand')

    module.addItem(
        tools.wxListWrapperTemplate('wxList', 'wxRichTextAction', module,
                                    fakeListClassName='wxRichTextActionList'))
    c.find('GetActions').type = 'wxRichTextActionList&'
    c.find('GetActions').noCopy = True

    c.find('AddAction.action').transfer = True


    #-------------------------------------------------------
    c = module.find('wxRichTextAction')
    tools.ignoreConstOverloads(c)


    #-------------------------------------------------------
    c = module.find('wxRichTextFileHandler')
    c.find('DoLoadFile').ignore(False)
    c.find('DoSaveFile').ignore(False)

    c = module.find('wxRichTextPlainTextHandler')
    c.find('DoLoadFile').ignore(False)
    c.find('DoSaveFile').ignore(False)




    #-------------------------------------------------------
    # Ignore all Dump() methods since we don't wrap wxTextOutputStream.

    # TODO: try switching the parameter type to wxOutputStream and then in
    # the wrapper code create a wxTextOutputStream from that to pass on to
    # Dump.

    for m in module.findAll('Dump'):
        if m.findItem('stream'):
            m.ignore()



    # Correct the type for this define as it is a float
    module.find('wxSCRIPT_MUL_FACTOR').type = 'float'

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

