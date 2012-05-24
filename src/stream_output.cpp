//--------------------------------------------------------------------------

static PyObject* wxPyGetMethod(PyObject* py, char* name)
{
    if (!PyObject_HasAttrString(py, name))
        return NULL;
    PyObject* o = PyObject_GetAttrString(py, name);
    if (!PyMethod_Check(o) && !PyCFunction_Check(o)) {
        Py_DECREF(o);
        return NULL;
    }
    return o;
}

#define wxPyBlock_t_default PyGILState_UNLOCKED


// This class can wrap a Python file-like object and allow it to be used 
// as a wxInputStream.
class wxPyOutputStream : public wxOutputStream
{
public:

    // Make sure there is at least a write method
    static bool Check(PyObject* fileObj) 
    {
        PyObject* method = wxPyGetMethod(fileObj, "write");
        bool rval = method != NULL;
        Py_XDECREF(method);
        return rval;
    }

    wxPyOutputStream(PyObject* fileObj, bool block=true) 
    {
        m_block = block;
        wxPyBlock_t blocked = wxPyBlock_t_default;
        if (block) blocked = wxPyBeginBlockThreads();
    
        m_write = wxPyGetMethod(fileObj, "write");
        m_seek = wxPyGetMethod(fileObj, "seek");
        m_tell = wxPyGetMethod(fileObj, "tell");
    
        if (block) wxPyEndBlockThreads(blocked);
    }
    
    virtual ~wxPyOutputStream()
    {
        wxPyBlock_t blocked = wxPyBlock_t_default;
        if (m_block) blocked = wxPyBeginBlockThreads();
        Py_XDECREF(m_write);
        Py_XDECREF(m_seek);
        Py_XDECREF(m_tell);
        if (m_block) wxPyEndBlockThreads(blocked);
    }
    
    wxPyOutputStream(const wxPyOutputStream& other)
    {
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        m_write  = other.m_write;
        m_seek  = other.m_seek;
        m_tell  = other.m_tell;
        m_block = other.m_block;
        Py_INCREF(m_write);
        Py_INCREF(m_seek);
        Py_INCREF(m_tell);
        wxPyEndBlockThreads(blocked);
    }
    
protected:

    // implement base class virtuals
    
    wxFileOffset GetLength() const 
    {
        wxPyOutputStream* self = (wxPyOutputStream*)this; // cast off const
        if (m_seek && m_tell) {
            wxFileOffset temp = self->OnSysTell();
            wxFileOffset ret = self->OnSysSeek(0, wxFromEnd);
            self->OnSysSeek(temp, wxFromStart);
            return ret;
        }
        else
            return wxInvalidOffset;
    }

    size_t OnSysRead(void *buffer, size_t bufsize) 
    {
        m_lasterror = wxSTREAM_READ_ERROR;
        return 0;
    }
    
    size_t OnSysWrite(const void *buffer, size_t bufsize) 
    {        
        if (bufsize == 0)
            return 0;
        
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        PyObject* arglist = PyTuple_New(1);
        PyTuple_SET_ITEM(arglist, 0, PyBytes_FromStringAndSize((char*)buffer, bufsize));
        
        PyObject* result = PyEval_CallObject(m_write, arglist);
        Py_DECREF(arglist);
    
        if (result != NULL)
            Py_DECREF(result);
        else
            m_lasterror = wxSTREAM_WRITE_ERROR;
        wxPyEndBlockThreads(blocked);
        return bufsize;            
    }
    
    wxFileOffset OnSysSeek(wxFileOffset off, wxSeekMode mode) 
    {
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        PyObject* arglist = PyTuple_New(2);
    
        if (sizeof(wxFileOffset) > sizeof(long))
            // wxFileOffset is a 64-bit value...
            PyTuple_SET_ITEM(arglist, 0, PyLong_FromLongLong(off));
        else
            PyTuple_SET_ITEM(arglist, 0, wxPyInt_FromLong(off));
    
        PyTuple_SET_ITEM(arglist, 1, wxPyInt_FromLong(mode));
    
    
        PyObject* result = PyEval_CallObject(m_seek, arglist);
        Py_DECREF(arglist);
        Py_XDECREF(result);
        wxPyEndBlockThreads(blocked);
        return OnSysTell();
    }
    
    wxFileOffset OnSysTell() const 
    {
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        PyObject* arglist = Py_BuildValue("()");
        PyObject* result = PyEval_CallObject(m_tell, arglist);
        Py_DECREF(arglist);
        wxFileOffset o = 0;
        if (result != NULL) {
            if (PyLong_Check(result))
                o = PyLong_AsLongLong(result);
            else
                o = wxPyInt_AsLong(result);
            Py_DECREF(result);
        };
        wxPyEndBlockThreads(blocked);
        return o;
    }
        
    bool IsSeekable() const 
    {
        return (m_seek != NULL);
    }
    
private:
    PyObject* m_write;
    PyObject* m_seek;
    PyObject* m_tell;
    bool      m_block;
};
        
//--------------------------------------------------------------------------
