"""
Widget from which money can be added or removed from account.

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.
"""

import wx
from pubsub import pub
from pubsub.py2and3 import print_


class ChangerWidget(wx.Frame):

  CHANGE = 10 # by how much money changes every time click

  def __init__(self, parent=None):
    wx.Frame.__init__(self, parent, -1, "Changer View")

    sizer = wx.BoxSizer(wx.VERTICAL)
    self.add = wx.Button(self, -1, "Add Money")
    self.remove = wx.Button(self, -1, "Remove Money")
    sizer.Add(self.add, 0, wx.EXPAND|wx.ALL)
    sizer.Add(self.remove, 0, wx.EXPAND|wx.ALL)
    self.SetSizer(sizer)

    self.add.Bind(wx.EVT_BUTTON, self.onAdd)
    self.remove.Bind(wx.EVT_BUTTON, self.onRemove)

  def onAdd(self, evt):
      print_('-----')
      pub.sendMessage("money_changing", amount = self.CHANGE)

  def onRemove(self, evt):
      print_('-----')
      pub.sendMessage("money_changing", amount = - self.CHANGE)


