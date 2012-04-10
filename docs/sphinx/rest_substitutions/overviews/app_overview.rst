.. include:: headings.inc


.. _app overview:

=================================
|phoenix_title|  **App Overview**
=================================


Introduction
------------

A wxPython application does not have a main procedure; the equivalent is the :meth:`AppConsole.OnInit` member defined for a class derived from :ref:`App`.

`OnInit` will usually create a top window as a bare minimum. Unlike in earlier versions of wxPython, `OnInit` does not return a frame. 
Instead it returns a boolean value which indicates whether processing should continue (``True``) or not (``False``).

An application closes by destroying all windows. Because all frames must be destroyed for the application to exit, it is advisable to use 
parent frames wherever possible when creating new frames, so that deleting the top level frame will automatically delete child frames. 
The alternative is to explicitly delete child frames in the top-level frame's :ref:`CloseEvent` handler.

In emergencies the :func:`Exit` function can be called to kill the application however normally the application shuts down automatically, 
see :ref:`Application Shutdown <application shutdown>`.

An example of defining an application follows::


	class DerivedApp(wx.App):

	    def OnInit(self):

	        the_frame = wx.Frame(None, -1)
  	    
  	        # Other initialization code...
  	        
   	        the_frame.Show(True)

	        return True



.. _application shutdown:

Application Shutdown
--------------------

The application normally shuts down when the last of its top level windows is closed. This is normally the expected behaviour and means 
that it is enough to call :meth:`Window.Close` () in response to the "Exit" menu command if your program has a single top level window. 
If this behaviour is not desirable :meth:`PyApp.SetExitOnFrameDelete` can be called to change it.

.. note:: Note that such logic doesn't apply for the windows shown before the program enters the main loop: in other words, you can
   safely show a dialog from :meth:`AppConsole.OnInit` and not be afraid that your application terminates when this dialog -- which is the last 
   top level window for the moment -- is closed.


Another aspect of the application shutdown is :meth:`AppConsole.OnExit` which is called when the application exits but before wxPython cleans up
its internal structures. 
