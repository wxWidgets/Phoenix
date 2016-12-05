import unittest
from unittests import wtc
import wx
import wx.media

#---------------------------------------------------------------------------

class mediactrl_Tests(wtc.WidgetTestCase):

    def test_mediactrl1(self):
        wx.media.MEDIASTATE_STOPPED
        wx.media.MEDIASTATE_PAUSED
        wx.media.MEDIASTATE_PLAYING
        wx.media.MEDIACTRLPLAYERCONTROLS_NONE
        wx.media.MEDIACTRLPLAYERCONTROLS_STEP
        wx.media.MEDIACTRLPLAYERCONTROLS_VOLUME
        wx.media.MEDIACTRLPLAYERCONTROLS_DEFAULT

        wx.media.MEDIABACKEND_DIRECTSHOW
        wx.media.MEDIABACKEND_MCI
        wx.media.MEDIABACKEND_QUICKTIME
        wx.media.MEDIABACKEND_GSTREAMER
        wx.media.MEDIABACKEND_REALPLAYER
        wx.media.MEDIABACKEND_WMP10

    def test_mediactrl2(self):
        mc = wx.media.MediaCtrl()
        mc.Create(self.frame)

    def test_mediactrl3(self):
        mc = wx.media.MediaCtrl(self.frame)


    def test_mediactrl4(self):
        evt = wx.media.MediaEvent()


    def test_mediactrl5(self):
        wx.media.wxEVT_MEDIA_LOADED
        wx.media.wxEVT_MEDIA_STOP
        wx.media.wxEVT_MEDIA_FINISHED
        wx.media.wxEVT_MEDIA_STATECHANGED
        wx.media.wxEVT_MEDIA_PLAY
        wx.media.wxEVT_MEDIA_PAUSE

        wx.media.EVT_MEDIA_LOADED
        wx.media.EVT_MEDIA_STOP
        wx.media.EVT_MEDIA_FINISHED
        wx.media.EVT_MEDIA_STATECHANGED
        wx.media.EVT_MEDIA_PLAY
        wx.media.EVT_MEDIA_PAUSE

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
