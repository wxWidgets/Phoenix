"""
Adapted from wxPython website at http://wiki.wxpython.org/ModelViewController/.

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.
"""

import wx

from pubsub import pub
from pubsub.py2and3 import print_

print_('pubsub API version', pub.VERSION_API)

# notification
from pubsub.utils.notification import useNotifyByWriteFile
import sys
useNotifyByWriteFile(sys.stdout)

# the following two modules don't know about each other yet will
# exchange data via pubsub:
from wx_win1 import View
from wx_win2 import ChangerWidget


class Model:

  def __init__(self):
    self.myMoney = 0

  def addMoney(self, value):
    self.myMoney += value
    #now tell anyone who cares that the value has been changed
    pub.sendMessage("money_changed", money=self.myMoney)

  def removeMoney(self, value):
    self.myMoney -= value
    #now tell anyone who cares that the value has been changed
    pub.sendMessage("money_changed", money=self.myMoney)


class Controller:

  def __init__(self):
    self.model = Model()

    #set up the first frame which displays the current Model value
    self.view1 = View()
    self.view1.setMoney(self.model.myMoney)

    #set up the second frame which allows the user to modify the Model's value
    self.view2 = ChangerWidget()

    self.view1.Show()
    self.view2.Show()

    pub.subscribe(self.changeMoney, 'money_changing')

  def changeMoney(self, amount):
    if amount >= 0:
        self.model.addMoney(amount)
    else:
        self.model.removeMoney(-amount)


if __name__ == "__main__":
    app = wx.App()
    c = Controller()
    sys.stdout = sys.__stdout__

    print_('---- Starting main event loop ----')
    app.MainLoop()
    print_('---- Exited main event loop ----')
    