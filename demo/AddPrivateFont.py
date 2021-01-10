#!/usr/bin/env python

import os
import sys

try:
    gFileDir = os.path.dirname(os.path.abspath(__file__))
except:
    gFileDir = os.path.dirname(os.path.abspath(sys.argv[0]))
gDataDir = os.path.join(gFileDir, 'data')

import wx


FILENAME = 'SourceCodePro-Regular.ttf'

SAMPLETEXT = """
SourceCodePro-Regular.ttf

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

abcdefghijklmnopqrstyvwxyz
ABCDEFGHIJKLMNOPQRSTYVWXYZ
1234567890.:,:\'"([{<\\|/>}])
`~!@#$%^&*_+-=?

Pangrams
The Quick Brown Fox Jumps Over The Lazy Dog.
Grumpy wizards make toxic brew for the evil queen and jack!
"""

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)

        # Show how to add a private font to the application at runtime that
        # doesn't have to be installed on the user's operating system.
        filename = os.path.join(gDataDir, 'SourceCodePro-Regular.ttf')
        wx.Font.AddPrivateFont(filename)

        text1 = "The font used in the text below was dynamically loaded from\n{}.".format(filename)
        st1 = wx.StaticText(self, -1, text1, (15, 15))

        st2 = wx.StaticText(self, -1, SAMPLETEXT, (15, 42))
        f = wx.Font(pointSize=12,
                    family=wx.FONTFAMILY_DEFAULT,
                    style=wx.FONTSTYLE_NORMAL,
                    weight=wx.FONTWEIGHT_NORMAL,
                    underline=False,
                    faceName="Source Code Pro",
                    encoding=wx.FONTENCODING_DEFAULT)
        st2.SetFont(f)


        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st1, 0, wx.ALL, 10)
        sizer.Add(wx.StaticLine(self, style=wx.HORIZONTAL), 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(st2, 0, wx.ALL, 10)
        self.SetSizer(sizer)
        self.Layout()


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
https://wxpython.org/Phoenix/docs/html/wx.Font.html#wx.Font.AddPrivateFont

Specify the name of a file containing a TrueType font to be made available to
the current application.

This method can be used to allow this application to use the font from the
given file even if it is not globally installed on the system.

Under OS X this method actually doesn't do anything other than check for the
existence of the file in the "Fonts" subdirectory of the application bundle
"Resources" directory. You are responsible for actually making the font file
available in this directory and setting ATSApplicationFontsPath to Fonts value
in your Info.plist file. See also wx.StandardPaths.GetResourcesDir .

Under MSW this method must be called before any wx.GraphicsContext objects
have been created, otherwise the private font won't be usable from them.

Under Unix this method requires Pango 1.38 or later and will return False and
log an error message explaining the problem if this requirement is not
satisfied either at compile- or run-time.

Currently this method is implemented for all major platforms (subject to
having Pango 1.38 or later when running configure under Unix) and
USE_PRIVATE_FONTS is always set to 0 under the other platforms, making
this function unavailable at compile-time.

Parameters: filename (string) -
Return type: bool
Returns: True if the font was added and can now be used.

New in version wxWidgets 3.1.1.

</body></html>
"""


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

