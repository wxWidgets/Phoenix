import unittest
from unittests import wtc
import wx
import os

cfgFilename = os.path.join(os.path.dirname(__file__), 'cfgtest')

#---------------------------------------------------------------------------

class ConfigTests(wtc.WidgetTestCase):

    def writeStuff(self, cfg):
        cfg.SetPath('/one/two/three')
        cfg.Write('key', 'value')
        cfg.WriteInt('int', 123)
        cfg.WriteFloat('float', 123.456)
        cfg.WriteBool('bool', True)
        cfg.Flush()


    def test_Config1(self):
        null = wx.LogNull()
        name = cfgFilename + '_1'
        cfg = wx.Config('unittest_ConfigTests', localFilename=name)
        self.writeStuff(cfg)
        del cfg
        if os.path.exists(name):
            os.remove(name)


    def test_Config2(self):
        null = wx.LogNull()
        name = cfgFilename + '_2'

        cfg = wx.Config('unittest_ConfigTests', localFilename=name)
        self.writeStuff(cfg)

        cfg.SetPath('/before')
        self.assertTrue(cfg.GetPath() == '/before')
        changer = wx.ConfigPathChanger(cfg, '/one/two/three/')
        self.assertTrue(cfg.GetPath() == '/one/two/three')
        del changer
        self.assertTrue(cfg.GetPath() == '/before')

        del cfg
        if os.path.exists(name):
            os.remove(name)


    def test_Config3(self):
        null = wx.LogNull()
        name = cfgFilename + '_3'

        cfg = wx.Config('unittest_ConfigTests', localFilename=name)
        self.writeStuff(cfg)

        cfg.SetPath('/before')
        self.assertTrue(cfg.GetPath() == '/before')
        with wx.ConfigPathChanger(cfg, '/one/two/three/'):
            self.assertTrue(cfg.GetPath() == '/one/two/three')
        self.assertTrue(cfg.GetPath() == '/before')

        del cfg
        if os.path.exists(name):
            os.remove(name)


    def test_Config4(self):
        null = wx.LogNull()
        name = cfgFilename + '_4'

        cfg0 = wx.Config('unittest_ConfigTests', localFilename=name)
        wx.Config.Set(cfg0)

        cfg = wx.Config.Get(False)
        #self.assertTrue(cfg is cfg0)
        self.writeStuff(cfg)
        del cfg

        cfg = wx.Config.Get()
        cfg.SetPath('/one/two/three')
        self.assertTrue(cfg.GetPath() == '/one/two/three')
        self.assertTrue(cfg.GetNumberOfEntries() == 4)
        self.assertTrue(cfg.Read('key') == 'value')
        self.assertTrue(cfg.ReadInt('int') == 123)
        self.assertTrue(cfg.ReadFloat('float') == 123.456)
        self.assertTrue(cfg.ReadBool('bool') == True)
        self.assertTrue(cfg.Read('no-value', 'defvalue') == 'defvalue')

        wx.Config.Set(None)
        self.myYield()
        if os.path.exists(name):
            os.remove(name)


    def test_Config5(self):
        null = wx.LogNull()
        name = cfgFilename + '_5'

        cfg = wx.Config('unittest_ConfigTests', localFilename=name)
        cfg.SetPath('/zero')
        cfg.Write('key1', 'value')
        cfg.Write('key2', 'value')
        cfg.Write('key3', 'value')

        cfg.SetPath('/one')
        cfg.Write('key1', 'value')
        cfg.Write('key2', 'value')
        cfg.Write('key3', 'value')

        cfg.SetPath('/two')
        cfg.Write('key1', 'value')
        cfg.Write('key2', 'value')
        cfg.Write('key3', 'value')

        cfg.SetPath('/three')
        cfg.Write('key1', 'value')
        cfg.Write('key2', 'value')
        cfg.Write('key3', 'value')

        cfg.Flush()

        cfg.SetPath('/')
        count = 0
        more, group, index = cfg.GetFirstGroup()
        while more:
            count += 1
            more, group, index = cfg.GetNextGroup(index)
        self.assertEqual(count, 4)

        cfg.SetPath('/two')
        count = 0
        more, entry, index = cfg.GetFirstEntry()
        while more:
            count += 1
            more, entry, index = cfg.GetNextEntry(index)
        self.assertEqual(count, 3)

        del cfg
        if os.path.exists(name):
            os.remove(name)


    def test_Config6(self):
        null = wx.LogNull()
        name = cfgFilename + '_6'

        cfg = wx.FileConfig('unittest_ConfigTests', localFilename=name)
        cfg.SetPath('/zero')
        cfg.Write('key1', 'value')
        cfg.Write('key2', 'value')
        cfg.Write('key3', 'value')

        cfg.SetPath('/one')
        cfg.Write('key1', 'value')
        cfg.Write('key2', 'value')
        cfg.Write('key3', 'value')

        cfg.SetPath('/two')
        cfg.Write('key1', 'value')
        cfg.Write('key2', 'value')
        cfg.Write('key3', 'value')

        cfg.SetPath('/three')
        cfg.Write('key1', 'value')
        cfg.Write('key2', 'value')
        cfg.Write('key3', 'value')

        cfg.Flush()

        cfg.SetPath('/')
        count = 0
        more, group, index = cfg.GetFirstGroup()
        while more:
            count += 1
            more, group, index = cfg.GetNextGroup(index)
        self.assertEqual(count, 4)

        cfg.SetPath('/two')
        count = 0
        more, entry, index = cfg.GetFirstEntry()
        while more:
            count += 1
            more, entry, index = cfg.GetNextEntry(index)
        self.assertEqual(count, 3)

        del cfg
        if os.path.exists(name):
            os.remove(name)

    def test_ConfigEnums(self):
        # Test for presence of config enums
        wx.CONFIG_USE_LOCAL_FILE
        wx.CONFIG_USE_GLOBAL_FILE
        wx.CONFIG_USE_RELATIVE_PATH
        wx.CONFIG_USE_NO_ESCAPE_CHARACTERS
        wx.CONFIG_USE_SUBDIR

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
