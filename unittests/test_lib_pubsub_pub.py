import unittest

from wx.lib.pubsub import pub
from wx.lib.pubsub.utils.xmltopicdefnprovider import XmlTopicDefnProvider

#---------------------------------------------------------------------------

class lib_pubsub_pub_Tests(unittest.TestCase):

    def test_lib_pubsub_pubAll(self):
        for name in pub.__all__:
            self.assertTrue(hasattr(pub, name), name)

    def test_lib_pubsub_pubXmlProviderBadFormat(self):
        with self.assertRaises(XmlTopicDefnProvider.UnrecognizedSourceFormatError):
            XmlTopicDefnProvider('<x/>', format='unknown')

    def test_lib_pubsub_pubXmlProviderTopicWithoutId(self):
        with self.assertRaises(XmlTopicDefnProvider.XmlParserError):
            XmlTopicDefnProvider('<topicdefntree><topic></topic></topicdefntree>')

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
