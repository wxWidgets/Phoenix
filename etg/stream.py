#---------------------------------------------------------------------------
# Name:        etg/stream.py
# Author:      Robin Dunn
#
# Created:     18-Nov-2011
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "stream"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxStreamBase',
           'wxInputStream',
           'wxOutputStream',
           ]


OTHERDEPS = [ 'src/stream_input.cpp',
              'src/stream_output.cpp',
              ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    # These enums are declared in files that we will not be using because
    # wxPython does not need the classes that are in those files. So just
    # inject the enums here instead.
    from etgtools import EnumDef, EnumValueDef
    e = EnumDef(name='wxStreamError')
    e.items.extend([ EnumValueDef(name='wxSTREAM_NO_ERROR'),
                     EnumValueDef(name='wxSTREAM_EOF'),
                     EnumValueDef(name='wxSTREAM_WRITE_ERROR'),
                     EnumValueDef(name='wxSTREAM_READ_ERROR'),
                     ])
    module.insertItem(0, e)

    e = EnumDef(name='wxSeekMode')
    e.items.extend([ EnumValueDef(name='wxFromStart'),
                     EnumValueDef(name='wxFromCurrent'),
                     EnumValueDef(name='wxFromEnd'),
                     ])
    module.insertItem(1, e)


    #-----------------------------------------------------------------
    c = module.find('wxStreamBase')
    assert isinstance(c, etgtools.ClassDef)
    c.abstract = True
    tools.removeVirtuals(c)
    c.find('operator!').ignore()


    #-----------------------------------------------------------------
    c = module.find('wxInputStream')
    c.abstract = True
    tools.removeVirtuals(c)

    # Include a C++ class that can wrap a Python file-like object so it can
    # be used as a wxInputStream
    c.includeCppCode('src/stream_input.cpp')

    # Use that class for the convert code
    c.convertFromPyObject = """\
        // is it just a typecheck?
        if (!sipIsErr) {
            if (wxPyInputStream::Check(sipPy))
                return 1;
            return 0;
        }
        // otherwise do the conversion
        *sipCppPtr = new wxPyInputStream(sipPy);
        return 0; //sipGetState(sipTransferObj);
        """

    # Add Python file-like methods so a wx.InputStream can be used as if it
    # was any other Python file object.
    c.addCppMethod('void', 'seek', '(wxFileOffset offset, int whence=0)', """\
        self->SeekI(offset, (wxSeekMode)whence);
        """)
    c.addCppMethod('wxFileOffset', 'tell', '()', """\
        return self->TellI();
        """);
    c.addCppMethod('void', 'close', '()', """\
        // ignored for now
        """)
    c.addCppMethod('void', 'flush', '()', """\
        // ignored for now
        """)
    c.addCppMethod('bool', 'eof', '()', """\
        return self->Eof();
        """)

    c.addCppCode("""\
        // helper used by the read and readline methods to make a PyObject
        static PyObject* _makeReadBufObj(wxInputStream* self, wxMemoryBuffer& buf) {
            PyObject* obj = NULL;

            wxPyThreadBlocker blocker;
            wxStreamError err = self->GetLastError();  // error check
            if (err != wxSTREAM_NO_ERROR && err != wxSTREAM_EOF) {
                PyErr_SetString(PyExc_IOError,"IOError in wxInputStream");
            }
            else {
                // Return the data as a string object.  TODO: Py3
                obj = PyBytes_FromStringAndSize(buf, buf.GetDataLen());
            }
            return obj;
        }
        """)


    c.addCppMethod('PyObject*', 'read', '()', """\
        wxMemoryBuffer buf;
        const ulong BUFSIZE = 1024;

        // read while bytes are available on the stream
        while ( self->CanRead() ) {
            self->Read(buf.GetAppendBuf(BUFSIZE), BUFSIZE);
            buf.UngetAppendBuf(self->LastRead());
        }
        return _makeReadBufObj(self, buf);
        """)

    c.addCppMethod('PyObject*', 'read', '(ulong size)', """\
        wxMemoryBuffer buf;

        // Read only size number of characters
        self->Read(buf.GetWriteBuf(size), size);
        buf.UngetWriteBuf(self->LastRead());
        return _makeReadBufObj(self, buf);
        """)

    c.addCppMethod('PyObject*', 'readline', '()', """\
        wxMemoryBuffer buf;
        char ch = 0;

        // read until \\n
        while ((ch != '\\n') && (self->CanRead())) {
            ch = self->GetC();
            buf.AppendByte(ch);
        }
        return _makeReadBufObj(self, buf);
        """)

    c.addCppMethod('PyObject*', 'readline', '(ulong size)', """\
        wxMemoryBuffer buf;
        int i;
        char ch;

        // read until \\n or byte limit reached
        for (i=ch=0; (ch != '\\n') && (self->CanRead()) && (i < size); i++) {
            ch = self->GetC();
            buf.AppendByte(ch);
        }
        return _makeReadBufObj(self, buf);
        """)


    c.addCppCode("""\
        PyObject* _wxInputStream_readline(wxInputStream* self);

        // This does the real work of the readlines methods
        static PyObject* _readlinesHelper(wxInputStream* self,
                                          bool useSizeHint=false, ulong sizehint=0) {
            PyObject* pylist;

            // init list
            {
                wxPyThreadBlocker blocker;
                pylist = PyList_New(0);

                if (!pylist) {
                    PyErr_NoMemory();
                    return NULL;
                }
            }

            // read sizehint bytes or until EOF
            ulong i;
            for (i=0; (self->CanRead()) && (useSizeHint || (i < sizehint));) {
                PyObject* s = _wxInputStream_readline(self);
                if (s == NULL) {
                    wxPyThreadBlocker blocker;
                    Py_DECREF(pylist);
                    return NULL;
                }
                wxPyThreadBlocker blocker;
                PyList_Append(pylist, s);
                i += PyBytes_Size(s);
            }

            // error check
            wxStreamError err = self->GetLastError();
            if (err != wxSTREAM_NO_ERROR && err != wxSTREAM_EOF) {
                wxPyThreadBlocker blocker;
                Py_DECREF(pylist);
                PyErr_SetString(PyExc_IOError,"IOError in wxInputStream");
                return NULL;
            }
            return pylist;
        }
        """)

    c.addCppMethod('PyObject*', 'readlines', '()', """\
        return _readlinesHelper(self);
        """)
    c.addCppMethod('PyObject*', 'readlines', '(ulong sizehint)', """\
        return _readlinesHelper(self, true, sizehint);
        """)


    #-----------------------------------------------------------------
    c = module.find('wxOutputStream')
    c.abstract = True
    tools.removeVirtuals(c)


    # Include a C++ class that can wrap a Python file-like object so it can
    # be used as a wxOutputStream
    c.includeCppCode('src/stream_output.cpp')

    # Use that class for the convert code
    c.convertFromPyObject = """\
        // is it just a typecheck?
        if (!sipIsErr) {
            if (wxPyOutputStream::Check(sipPy))
                return 1;
            return 0;
        }
        // otherwise do the conversion
        *sipCppPtr = new wxPyOutputStream(sipPy);
        return sipGetState(sipTransferObj);
        """


    # Add Python file-like methods so a wx.OutputStream can be used as if it
    # was any other Python file object.
    c.addCppMethod('void', 'seek', '(wxFileOffset offset, int whence=0)', """\
        self->SeekO(offset, (wxSeekMode)whence);
        """)
    c.addCppMethod('wxFileOffset', 'tell', '()', """\
        return self->TellO();
        """);
    c.addCppMethod('void', 'close', '()', """\
        self->Close();
        """)
    c.addCppMethod('void', 'flush', '()', """\
        self->Sync();
        """)
    c.addCppMethod('bool', 'eof', '()', """\
        return false; //self->Eof();
        """)

    c.addCppMethod('PyObject*', 'write', '(PyObject* data)', """\
        // We use only bytes objects (strings in 2.7) for the streams, never unicode
        wxPyThreadBlocker blocker;
        if (!PyBytes_Check(data)) {
            PyErr_SetString(PyExc_TypeError, "Bytes object expected");
            return NULL;
        }
        self->Write(PyBytes_AS_STRING(data), PyBytes_GET_SIZE(data));
        RETURN_NONE();
        """)

    # TODO: Add a writelines(sequence) method

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

