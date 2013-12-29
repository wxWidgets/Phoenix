These two examples demonstrate a simple use of pubsub with the *arg1*
messaging protocol. There are two examples that can be run from this folder:

**console_main.py**: basic console based, uses the console_senders.py and
    console_listeners.py modules, giving basic example of the *arg1*
    messaging protocol.

**wx.py**: basic wxPython GUI application that uses the *arg1* messaging
    protocol. Note that it imports pubsub from
    wxPython's wx.lib package. Therefore you must have (a copy of)
    pubsub installed there for this example to work (pubsub can be
    installed in multiple places independently and they will all work
    without interfering with each other).

    Note that this example is copied almost
    verbatim from the wxPython wiki site and is probably not a
    good model of how an application should be structured.