import unittest
from unittests import wtc
import wx
import wx.adv
import sys, os

wavFile = os.path.join(os.path.dirname(__file__), 'sound.wav')

#---------------------------------------------------------------------------

class sound_Tests(wtc.WidgetTestCase):

    def test_sound1(self):
        wx.adv.SOUND_SYNC
        wx.adv.SOUND_ASYNC
        wx.adv.SOUND_LOOP

    def test_sound2(self):
        sound = wx.adv.Sound(wavFile)
        self.assertTrue(sound.IsOk())
        rv = sound.Play(wx.adv.SOUND_SYNC)

    @unittest.skipIf(sys.platform == 'darwin', 'CreateFromBuffer not implemented on Mac')
    def test_sound3(self):
        sound = wx.adv.Sound()
        self.assertTrue(not sound.IsOk())
        with open(wavFile, 'rb') as f:
            data = f.read()
        sound.CreateFromData(data)
        self.assertTrue(sound.IsOk())
        rv = sound.Play(wx.adv.SOUND_SYNC)

    def test_sound4(self):
        rv = wx.adv.Sound.PlaySound(wavFile, wx.adv.SOUND_SYNC)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
