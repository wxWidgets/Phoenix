import unittest
import xml.dom.minidom as minidom

from wx.tools import pywxrc

#---------------------------------------------------------------------------

XRC = """\
<?xml version="1.0" ?>
<resource>
  <object class="wxPanel" name="panel">
    <object class="wxListCtrl">
      <object class="listcol"><text>Column</text></object>
    </object>
    <object class="wxTextCtrl"><hint>Type here</hint><value>42</value></object>
    <object class="wxDatePickerCtrl"><null-text>No date</null-text></object>
    <object class="wxStaticText"><label translate="0">Fixed</label></object>
  </object>
</resource>
"""


class tools_pywxrc_Tests(unittest.TestCase):

    def test_pywxrc_gettextStrings(self):
        doc = minidom.parseString(XRC)
        strings = pywxrc.XmlResourceCompiler().FindStringsInNode(doc.firstChild)
        self.assertEqual(strings, ['Column', 'Type here', 'No date'])

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
