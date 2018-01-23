This folder contains a copy of the SIP runtime library code.  It is
here so we can make it part of the wxPython build instead of needing
to have a dependency upon SIP already being installed on user
machines.

3rd party extension modules that need to use or interact with wxPython
types or other items will need to ensure that they #include the sip.h
located in this folder so they will know the proper module name to
import to find this version of the runtime library.  This feature was
added in SIP 4.12.

