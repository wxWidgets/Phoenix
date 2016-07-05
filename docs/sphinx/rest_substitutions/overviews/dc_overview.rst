.. include:: headings.inc


.. _device contexts:

====================================
|phoenix_title|  **Device Contexts**
====================================


A :ref:`wx.DC` is a device context onto which graphics and text can be
drawn. The device context is intended to represent a number of output
devices in a generic way, with the same API being used throughout.

Some device contexts are created temporarily in order to draw on a
window. This is true of :ref:`wx.ScreenDC`, :ref:`wx.ClientDC`,
:ref:`wx.PaintDC`, and :ref:`wx.WindowDC`. The following describes the
differences between these device contexts and when you should use
them.

- :ref:`wx.ScreenDC`. Use this to paint on the screen, as opposed to an
  individual window.

- :ref:`wx.ClientDC`. Use this to paint on the client area of window (the
  part without borders and other decorations), but do not use it from
  within an :ref:`wx.PaintEvent`.

- :ref:`wx.PaintDC`. Use this to paint on the client area of a window,
  but only from within a :ref:`wx.PaintEvent`.

- :ref:`wx.WindowDC`. Use this to paint on the whole area of a window,
  including decorations. This may not be available on non-Windows
  platforms.


To use a client, paint or window device context, create an object on
the stack with the window as argument, for example::

	def OnMyCmd(self, event):
	    dc = wx.ClientDC(window)
	    DrawMyPicture(dc)


Try to write code so it is parameterised by :ref:`wx.DC` - if you do
this, the same piece of code may write to a number of different
devices, by passing a different device context. This doesn't work for
everything (for example not all device contexts support bitmap
drawing) but will work most of the time.



