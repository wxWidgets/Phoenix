.. include:: headings.inc


.. _standard event identifiers:

===============================================
|phoenix_title|  **Standard event identifiers**
===============================================

wxPython defines a special identifier value ``ID_ANY`` (-1) which is used in the following two situations:

- When creating a new window you may specify ``ID_ANY`` to let wxPython assign an unused identifier to it automatically
- When installing an event handler using :meth:`EvtHandler.Bind`, you may use it to indicate that you want to handle 
  the events coming from any control, regardless of its identifier
  
  
Another standard special identifier value is ``ID_NONE``: this is a value which is not matched by any other id.

wxPython also defines a few standard command identifiers which may be used by the user code and also are sometimes 
used by wxPython itself. These reserved identifiers are all in the range between ``ID_LOWEST`` and ``ID_HIGHEST`` and, 
accordingly, the user code should avoid defining its own constants in this range (e.g. by using :func:`NewId` ()).

Refer to :ref:`the list of stock items <stock items>` for the subset of standard IDs which are stock IDs as well.

