#---------------------------------------------------------------------------
# Name:        etg/htmlwinpars.py
# Author:      Robin Dunn
#
# Created:     29-Oct-2012
# Copyright:   (c) 2012-2017 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_html"
NAME      = "htmlwinpars"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ #"wxHtmlTagsModule",
           "wxHtmlWinTagHandler",
           "wxHtmlWinParser",
           ]


#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxHtmlWinTagHandler')
    assert isinstance(c, etgtools.ClassDef)

    c.addCppMethod('wxHtmlWinParser*', 'GetParser', '()',
        body="return (wxHtmlWinParser*)self->GetParser();")

    c.addPrivateCopyCtor()


    c = module.find('wxHtmlWinParser')
    c.find('GetEncodingConverter').ignore()
    c.find('GetInputEncoding').ignore()
    c.find('GetOutputEncoding').ignore()
    c.find('SetInputEncoding').ignore()

    tools.fixHtmlSetFonts(c)

    c.find('AddModule').ignore()

    c.addItem(etgtools.WigCode("""\
        virtual wxObject* GetProduct();
        """))


    module.addCppCode("""\
        class wxPyHtmlTagsModule : public wxHtmlTagsModule {
        public:
            wxPyHtmlTagsModule(PyObject* thc) : wxHtmlTagsModule() {
                m_tagHandlerClass = thc;
                wxPyThreadBlocker blocker;
                Py_INCREF(m_tagHandlerClass);
                RegisterModule(this);
                wxHtmlWinParser::AddModule(this);
            }

            void OnExit() {
                wxPyThreadBlocker blocker;
                Py_DECREF(m_tagHandlerClass);
                m_tagHandlerClass = NULL;
                for (size_t x=0; x < m_objArray.GetCount(); x++) {
                    PyObject* obj = (PyObject*)m_objArray.Item(x);
                    Py_DECREF(obj);
                }
            }

            void FillHandlersTable(wxHtmlWinParser *parser) {
                wxPyThreadBlocker blocker;
                wxHtmlWinTagHandler* thPtr = 0;
                // First, make a new instance of the tag handler
                PyObject* arg = PyTuple_New(0);
                PyObject* obj = PyObject_CallObject(m_tagHandlerClass, arg);
                Py_DECREF(arg);

                // Make sure it succeeded
                if (!obj) {
                    PyErr_Print();
                    return;
                }

                // now figure out where it's C++ object is...
                if (! wxPyConvertWrappedPtr(obj, (void **)&thPtr, wxT("wxHtmlWinTagHandler"))) {
                    return;
                }

                // add it,
                parser->AddTagHandler(thPtr);

                // and track it.
                m_objArray.Add(obj);
            }

        private:
            PyObject*           m_tagHandlerClass;
            wxArrayPtrVoid      m_objArray;

        };
        """)


    module.addCppFunction('void', 'HtmlWinParser_AddTagHandler', '(PyObject* tagHandlerClass)',
        body="""\
            // Dynamically create a new wxModule.  Refcounts tagHandlerClass
            // and adds itself to the wxModules list and to the wxHtmlWinParser.
            new wxPyHtmlTagsModule(tagHandlerClass);
            wxModule::InitializeModules();
            """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

