/*
 * Thread support for the SIP library.  This module provides the hooks for
 * C++ classes that provide a thread interface to interact properly with the
 * Python threading infrastructure.
 *
 * Copyright (c) 2010 Riverbank Computing Limited <info@riverbankcomputing.com>
 *
 * This file is part of SIP.
 *
 * This copy of SIP is licensed for use under the terms of the SIP License
 * Agreement.  See the file LICENSE for more details.
 *
 * This copy of SIP may also used under the terms of the GNU General Public
 * License v2 or v3 as published by the Free Software Foundation which can be
 * found in the files LICENSE-GPL2 and LICENSE-GPL3 included in this package.
 *
 * SIP is supplied WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 */


#include "sip.h"
#include "sipint.h"


/*
 * The data associated with pending request to wrap an object.
 */
typedef struct _pendingDef {
    void *cpp;                      /* The C/C++ object ot be wrapped. */
    sipWrapper *owner;              /* The owner of the object. */
    int flags;                      /* The flags. */
} pendingDef;


#ifdef WITH_THREAD

#include <pythread.h>


/*
 * The per thread data we need to maintain.
 */
typedef struct _threadDef {
    long thr_ident;                 /* The thread identifier. */
    pendingDef pending;             /* An object waiting to be wrapped. */
    struct _threadDef *next;        /* Next in the list. */
} threadDef;


static threadDef *threads = NULL;   /* Linked list of threads. */


static threadDef *currentThreadDef(void);

#endif


static pendingDef pending;          /* An object waiting to be wrapped. */


/*
 * Get the address of any C/C++ object waiting to be wrapped.
 */
void *sipGetPending(sipWrapper **op, int *fp)
{
    pendingDef *pp;

#ifdef WITH_THREAD
    threadDef *thread;

    if ((thread = currentThreadDef()) != NULL)
        pp = &thread->pending;
    else
        pp = &pending;
#else
    pp = &pending;
#endif

    if (pp->cpp != NULL)
    {
        if (op != NULL)
            *op = pp->owner;

        if (fp != NULL)
            *fp = pp->flags;
    }

    return pp->cpp;
}


/*
 * Convert a new C/C++ pointer to a Python instance.
 */
PyObject *sipWrapSimpleInstance(void *cppPtr, const sipTypeDef *td,
        sipWrapper *owner, int flags)
{
    static PyObject *nullargs = NULL;

    pendingDef old_pending;
    PyObject *self;
#ifdef WITH_THREAD
    threadDef *thread;
#endif

    if (nullargs == NULL && (nullargs = PyTuple_New(0)) == NULL)
        return NULL;

    if (cppPtr == NULL)
    {
        Py_INCREF(Py_None);
        return Py_None;
    }

    /*
     * Object creation can trigger the Python garbage collector which in turn
     * can execute arbitrary Python code which can then call this function
     * recursively.  Therefore we save any existing pending object before
     * setting the new one.
     */
#ifdef WITH_THREAD
    if ((thread = currentThreadDef()) != NULL)
    {
        old_pending = thread->pending;

        thread->pending.cpp = cppPtr;
        thread->pending.owner = owner;
        thread->pending.flags = flags;
    }
    else
    {
        old_pending = pending;

        pending.cpp = cppPtr;
        pending.owner = owner;
        pending.flags = flags;
    }
#else
    old_pending = pending;

    pending.cpp = cppPtr;
    pending.owner = owner;
    pending.flags = flags;
#endif

    self = PyObject_Call((PyObject *)sipTypeAsPyTypeObject(td), nullargs, NULL);

#ifdef WITH_THREAD
    if (thread != NULL)
        thread->pending = old_pending;
    else
        pending = old_pending;
#else
    pending = old_pending;
#endif

    return self;
}


/*
 * This is called from a newly created thread to initialise some thread local
 * storage.
 */
void sip_api_start_thread(void)
{
#ifdef WITH_THREAD
    threadDef *thread;

    /* Save the thread ID.  First, find an empty slot in the list. */
    for (thread = threads; thread != NULL; thread = thread->next)
        if (thread->thr_ident == 0)
            break;

    if (thread == NULL)
    {
        thread = sip_api_malloc(sizeof (threadDef));
        thread->next = threads;
        threads = thread;
    }

    if (thread != NULL)
    {
        thread->thr_ident = PyThread_get_thread_ident();
        thread->pending.cpp = NULL;
    }
#endif
}


/*
 * Handle the termination of a thread.  The thread state should already have
 * been handled by the last call to PyGILState_Release().
 */
void sip_api_end_thread(void)
{
#ifdef WITH_THREAD
    threadDef *thread;

    /* We have the GIL at this point. */
    if ((thread = currentThreadDef()) != NULL)
        thread->thr_ident = 0;
#endif
}


#ifdef WITH_THREAD

/*
 * Return the thread data for the current thread or NULL if it wasn't
 * recognised.
 */
static threadDef *currentThreadDef(void)
{
    threadDef *thread;
    long ident = PyThread_get_thread_ident();

    for (thread = threads; thread != NULL; thread = thread->next)
        if (thread->thr_ident == ident)
            break;

    return thread;
}

#endif
