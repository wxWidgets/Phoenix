#---------------------------------------------------------------------------
# Name:        etg/htmlwinpars.py
# Author:      Robin Dunn
#
# Created:     29-Oct-2012
# Copyright:   (c) 2012-2020 by Total Control Software
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
            wxPyHtmlTagsModule() : wxHtmlTagsModule() {
            }

            bool OnInit() {
                wxHtmlWinParser::AddModule(this);
                return true;
            }

            void OnExit() {
                wxPyThreadBlocker blocker;
                for (size_t x=0; x < m_tagHandlersArray.GetCount(); x++) {
                    PyObject* obj = (PyObject*)m_tagHandlersArray.Item(x);
                    Py_DECREF(obj);
                }
                m_tagHandlersArray.Clear();
                wxHtmlWinParser::RemoveModule(this);
            }

            void FillHandlersTable(wxHtmlWinParser *parser) {
                wxPyThreadBlocker blocker;

                // make a new instance of each handler class and register it with the parser
                for (size_t cls=0; cls < s_tagHandlerClasses.GetCount(); cls++) {
                    PyObject* pyClass = (PyObject*)s_tagHandlerClasses.Item(cls);

                    wxHtmlWinTagHandler* thPtr = NULL;

                    PyObject* arg = PyTuple_New(0);
                    PyObject* obj = PyObject_CallObject(pyClass, arg);
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

                    // and track it
                    m_tagHandlersArray.Add(obj);
                }
            }

            static void AddPyTagHandler(PyObject* tagHandlerClass) {
                wxPyThreadBlocker blocker;
                Py_INCREF(tagHandlerClass);
                s_tagHandlerClasses.Add(tagHandlerClass);
            }

        private:
            wxDECLARE_DYNAMIC_CLASS(wxPyHtmlTagsModule);

            static wxArrayPtrVoid       s_tagHandlerClasses;
            wxArrayPtrVoid              m_tagHandlersArray;
        };

        wxIMPLEMENT_DYNAMIC_CLASS(wxPyHtmlTagsModule, wxHtmlTagsModule)
        wxArrayPtrVoid wxPyHtmlTagsModule::s_tagHandlerClasses;
        """)


    module.addCppFunction('void', 'HtmlWinParser_AddTagHandler', '(PyObject* tagHandlerClass)',
        body="""\
            wxPyHtmlTagsModule::AddPyTagHandler(tagHandlerClass);
            wxPyReinitializeModules();
            """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

