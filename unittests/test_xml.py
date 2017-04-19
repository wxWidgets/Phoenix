import unittest
from unittests import wtc
import wx
import wx.xml as xml

#---------------------------------------------------------------------------

class xml_Tests(wtc.WidgetTestCase):

    def test_xml1(self):
        doc = xml.XmlDocument()
        node = xml.XmlNode(xml.XML_DOCUMENT_NODE, 'document')
        doc.SetDocumentNode(node)
        root = xml.XmlNode(xml.XML_ELEMENT_NODE, 'root')
        node.AddChild(root)
        root.AddAttribute('name1', 'value1')
        root.AddAttribute(xml.XmlAttribute('name2', 'value2'))


    def test_xml2(self):
        xml.XML_ELEMENT_NODE
        xml.XML_ATTRIBUTE_NODE
        xml.XML_TEXT_NODE
        xml.XML_CDATA_SECTION_NODE
        xml.XML_ENTITY_REF_NODE
        xml.XML_ENTITY_NODE
        xml.XML_PI_NODE
        xml.XML_COMMENT_NODE
        xml.XML_DOCUMENT_NODE
        xml.XML_DOCUMENT_TYPE_NODE
        xml.XML_DOCUMENT_FRAG_NODE
        xml.XML_NOTATION_NODE
        xml.XML_HTML_DOCUMENT_NODE

        xml.XML_NO_INDENTATION
        xml.XMLDOC_NONE
        xml.XMLDOC_KEEP_WHITESPACE_NODES

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
