import imp_unittest, unittest
import wtc
import wx
import os

cfgFilename = os.path.join(os.path.dirname(__file__), 'cfgtest')
#---------------------------------------------------------------------------

class ConfigTests(wtc.WidgetTestCase):
    
    def test_Config1(self):
        null = wx.LogNull()
        name = cfgFilename + '_1'
        cfg = wx.Config('unittest_ConfigTests', localFilename=name)
        self.writeStuff(cfg)
        del cfg
        if os.path.exists(name):
            os.remove(name)

    def writeStuff(self, cfg):
        cfg.SetPath('/one/two/three')
        cfg.Write('key', 'value')
        cfg.WriteInt('int', 123)
        cfg.WriteFloat('float', 123.456)
        cfg.WriteBool('bool', True)
        cfg.Flush()

        
        
    def test_Config2(self):
        null = wx.LogNull()
        name = cfgFilename + '_2'
        
        wx.Config.Set(wx.Config('unittest_ConfigTests', localFilename=name))
        cfg = wx.Config.Get()
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

        if os.path.exists(name):
            os.remove(name)

        
       
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
