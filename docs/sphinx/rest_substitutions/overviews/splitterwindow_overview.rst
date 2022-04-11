.. include:: headings.inc


.. _splitterwindow overview:

=================================================
|phoenix_title|  **Splitter Windows Overview**
=================================================


The following screenshot shows the appearance of a splitter window
with a horizontal split.

The style ``wx.SP_3D`` has been used to show a 3D border and 3D sash.

.. figure:: _static/images/overviews/overview_splitter_3d.png
   :align: center



Example
-------

The following fragment shows how to create a splitter window, creating
two subwindows and hiding one of them::

	splitter = wx.SplitterWindow(self, -1, wx.Point(0, 0),
				     wx.Size(400, 400), wx.SP_3D)

	leftWindow = MyWindow(splitter)
	leftWindow.SetScrollbars(20, 20, 50, 50)

	rightWindow = MyWindow(splitter)
	rightWindow.SetScrollbars(20, 20, 50, 50)
	rightWindow.Show(False)

	splitter.Initialize(leftWindow)

	# Set this to prevent unsplitting
	# splitter.SetMinimumPaneSize(20)


The next fragment shows how the splitter window can be manipulated
after creation::

	def OnSplitVertical(self, event):

	    if splitter.IsSplit():
		splitter.Unsplit()

	    leftWindow.Show(True)
	    rightWindow.Show(True)
	    splitter.SplitVertically(leftWindow, rightWindow)


	def OnSplitHorizontal(self, event):

	    if splitter.IsSplit():
		splitter.Unsplit()

	    leftWindow.Show(True)
	    rightWindow.Show(True)
	    splitter.SplitHorizontally(leftWindow, rightWindow)


	def OnUnsplit(self, event):

	    if splitter.IsSplit():
		splitter.Unsplit()



