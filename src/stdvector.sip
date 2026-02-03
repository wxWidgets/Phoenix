//--------------------------------------------------------------------------
// Name:        stdvector.sip
// Purpose:     MappedType for std::vector
//
// Author:      Scott Talbert
//
// Created:     25-Jan-2026
// Copyright:   (c) 2026 by Scott Talbert
// Licence:     wxWindows license
//--------------------------------------------------------------------------

template<_TYPE_>
%MappedType std::vector<_TYPE_> /TypeHint="List[_TYPE_]"/
{
    %TypeHeaderCode
    #include <vector>
    %End

    %ConvertFromTypeCode
        const sipTypeDef *kpTypeDef = sipFindType("_TYPE_");
        if (!kpTypeDef) {
            return NULL;
        }

        PyObject *l = PyList_New(sipCpp->size());
        if (!l) {
            return NULL;
        }

        for (size_t i = 0; i < sipCpp->size(); ++i) {
            _TYPE_ *cpp = new _TYPE_(sipCpp->at(i));
            PyObject *pobj = sipConvertFromNewType(cpp, kpTypeDef, sipTransferObj);
            if (pobj == NULL) {
                delete cpp;
                Py_XDECREF(l);
                return NULL;
            }

            PyList_SET_ITEM(l, i, pobj);
        }

        return l;
    %End

    %ConvertToTypeCode
        const sipTypeDef *kpTypeDef = sipFindType("_TYPE_");
        if (!kpTypeDef) {
            return 0;
        }

        // Check if type is compatible
        if (sipIsErr == NULL) {
            return PyList_Check(sipPy);
        }

        std::vector<_TYPE_> *v = new std::vector<_TYPE_>();
        v->reserve(PyList_GET_SIZE(sipPy));

        for (Py_ssize_t i = 0; i < PyList_GET_SIZE(sipPy); ++i) {
            int state;
            _TYPE_ *p = static_cast<_TYPE_ *>(sipConvertToType(
                    PyList_GET_ITEM(sipPy, i), kpTypeDef, sipTransferObj,
                    SIP_NOT_NONE, &state, sipIsErr));

            if (*sipIsErr) {
                sipReleaseType(p, kpTypeDef, state);
                delete v;
                return 0;
            }

            v->push_back(*p);
            sipReleaseType(p, kpTypeDef, state);
        }

        *sipCppPtr = v;

        return sipGetState(sipTransferObj);
    %End
};
