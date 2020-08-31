#----------------------------------------------------------------------
# Name:        wx.lib.softwareupdate
# Purpose:     A mixin class using Esky that allows a frozen application
#              to update itself when new versions of the software become
#              available.
#
# Author:      Robin Dunn
#
# Created:     1-Aug-2011
# Copyright:   (c) 2011-2020 by Total Control Software
# Licence:     wxWindows license
#
# Tags:        py3-port??
#----------------------------------------------------------------------

"""
This module provides a class designed to be mixed with wx.App to form a
derived class which is able to auto-self-update the application when new
versions are released. It is built upon the Esky package, available in PyPi at
http://pypi.python.org/pypi/esky.

In order for the software update to work the application must be put into an
esky bundle using the bdist_esky distutils command, which in turn will use
py2app, py2exe or etc. to freeze the actual application. See Esky's docs for
more details. The code in this module will only have effect if the application
is frozen, and is silently ignored otherwise.
"""

import wx
import sys
import os
import atexit
import six

if six.PY3:
    from urllib.request import urlopen
    from urllib.error import URLError
else:
    from urllib2 import urlopen
    from urllib2 import URLError

from wx.lib.dialogs import MultiMessageBox

isFrozenApp = hasattr(sys, 'frozen')
if isFrozenApp:
    import esky
    import esky.util

# wx 2.8 doesn't have [SG]etAppDisplayname...
try:
    wx.App.GetAppDisplayName
except AttributeError:
    wx.App.GetAppDisplayName = wx.App.GetAppName
    wx.App.SetAppDisplayName = wx.App.SetAppName


SOT = 0
#if 'wxMac' in wx.PlatformInfo:
#    SOT = wx.STAY_ON_TOP

#----------------------------------------------------------------------


class UpdateAbortedError(RuntimeError):
    pass


class SoftwareUpdate(object):
    """
    Mix this class with :class:`App` and call :meth:`InitForUpdates` from the derived class'
    OnInit method. Be sure that the :class:`App` has set a display name
    (self.SetAppDisplayName) as that value will be used in the update dialogs.
    """

    _caption = "Software Update"
    _networkFailureMsg = (
        "Unable to connect to %s to check for updates.\n\n"
        "Perhaps your network is not enabled, the update server is down, or your"
        "firewall is blocking the connection.")


    def InitUpdates(self, updatesURL, changelogURL=None, icon=None):
        """
        Set up the Esky object for doing software updates. Passing either the
        base URL (with a trailing '/') for the location of the update
        packages, or an instance of a class derived from the
        esky.finder.VersionFinder class is required. A custom VersionFinder
        can be used to find and fetch the newer verison of the software in
        some other way, if desired.

        Call this method from the app's OnInit method.
        """
        if isFrozenApp:
            self._esky = esky.Esky(sys.executable, updatesURL)
            self._updatesURL = updatesURL
            self._changelogURL = changelogURL
            self._icon = icon
            self._pd = None
            self._checkInProgress = False
            try:
                # get rid of the prior version if it is still here.
                if self._esky.needs_cleanup():
                    self._esky.cleanup()
            except:
                pass
            self._fixSysExecutable()


    def AutoCheckForUpdate(self, frequencyInDays, parentWindow=None, cfg=None):
        """
        If it has been `frequencyInDays` since the last auto-check then check if
        a software update is available and prompt the user to download and
        install it. This can be called after a application has started up, and
        if there is no update available the user will not be bothered.
        """
        if not isFrozenApp:
            return
        if cfg is None:
            cfg = wx.Config.Get()
        oldPath = cfg.GetPath()
        cfg.SetPath('/autoUpdate')
        lastCheck = cfg.ReadInt('lastCheck', 0)
        lastCheckVersion = cfg.Read('lastCheckVersion', '')
        today = int(wx.DateTime.Today().GetJulianDayNumber())
        active = self._esky.active_version

        if (today - lastCheck >= frequencyInDays
            or lastCheckVersion != active):
                self.CheckForUpdate(True, parentWindow, cfg)
        cfg.SetPath(oldPath)


    def CheckForUpdate(self, silentUnlessUpdate=False, parentWindow=None, cfg=None):
        """
        This method will check for the availability of a new update, and will
        prompt the user with details if there is one there. By default it will
        also tell the user if there is not a new update, but you can pass
        silentUnlessUpdate=True to not bother the user if there isn't a new
        update available.

        This method should be called from an event handler for a "Check for
        updates" menu item, or something similar. The actual update check
        will be run in a background thread and this function will return
        immediately after starting the thread so the application is not
        blocked if there is network communication problems. A callback to the
        GUI thread will be made to do the update or report problems as
        needed.
        """
        if not isFrozenApp or self._checkInProgress:
            return
        self._checkInProgress = True


        def doFindUpdate():
            try:
                newest = self._esky.find_update()
                chLogTxt = ''
                if newest is not None and self._changelogURL:
                    with urlopen(self._changelogURL, timeout=4) as req:
                        chLogTxt = req.read()
                return (newest, chLogTxt)

            except URLError:
                return 'URLError'


        def processResults(result):
            result = result.get()
            self._checkInProgress = False
            if result == 'URLError':
                if not silentUnlessUpdate:
                    MultiMessageBox(
                        self._networkFailureMsg % self._updatesURL,
                        self._caption, parent=parentWindow, icon=self._icon,
                        style=wx.OK|SOT)
                return

            active = self._esky.active_version
            if cfg:
                oldPath = cfg.GetPath()
                cfg.SetPath('/autoUpdate')
                today = int(wx.DateTime.Today().GetJulianDayNumber())
                cfg.WriteInt('lastCheck', today)
                cfg.Write('lastCheckVersion', active)
                cfg.Flush()
                cfg.SetPath(oldPath)

            newest, chLogTxt = result
            if newest is None:
                if not silentUnlessUpdate:
                    MultiMessageBox("You are already running the newest verison of %s." %
                                    self.GetAppDisplayName(),
                                    self._caption, parent=parentWindow, icon=self._icon,
                                    style=wx.OK|SOT)
                return
            self._parentWindow = parentWindow

            resp = MultiMessageBox("A new version of %s is available.\n\n"
                   "You are currently running verison %s; version %s is now "
                   "available for download.  Do you wish to install it now?"
                   % (self.GetAppDisplayName(), active, newest),
                   self._caption, msg2=chLogTxt, style=wx.YES_NO|SOT,
                   parent=parentWindow, icon=self._icon,
                   btnLabels={wx.ID_YES:"Yes, install now",
                              wx.ID_NO:"No, maybe later"})
            if resp != wx.YES:
                return

            # Ok, there is a little trickery going on here. We don't know yet if
            # the user wants to restart the application after the update is
            # complete, but since atexit functions are executed in a LIFO order we
            # need to registar our function before we call auto_update and Esky
            # possibly registers its own atexit function, because we want ours to
            # be run *after* theirs. So we'll create an instance of an info object
            # and register its method now, and then fill in the details below
            # once we decide what we want to do.
            class RestartInfo(object):
                def __init__(self):
                    self.exe = None
                def restart(self):
                    if self.exe is not None:
                        # Execute the program, replacing this process
                        os.execv(self.exe, [self.exe] + sys.argv[1:])
            info = RestartInfo()
            atexit.register(info.restart)

            try:
                # Let Esky handle all the rest of the update process so we can
                # take advantage of the error checking and priviledge elevation
                # (if neccessary) that they have done so we don't have to worry
                # about that ourselves like we would if we broke down the proccess
                # into component steps.
                self._esky.auto_update(self._updateProgress)

            except UpdateAbortedError:
                MultiMessageBox("Update canceled.", self._caption,
                                parent=parentWindow, icon=self._icon,
                                style=wx.OK|SOT)
                if self._pd:
                    self._pd.Destroy()

                self.InitUpdates(self._updatesURL, self._changelogURL, self._icon)
                return

            # Ask the user if they want the application to be restarted.
            resp = MultiMessageBox("The upgrade to %s %s is ready to use; the application will "
                                   "need to be restarted to begin using the new release.\n\n"
                                   "Restart %s now?"
                                   % (self.GetAppDisplayName(), newest, self.GetAppDisplayName()),
                                   self._caption, style=wx.YES_NO|SOT,
                                   parent=parentWindow, icon=self._icon,
                                   btnLabels={wx.ID_YES:"Yes, restart now",
                                              wx.ID_NO:"No, I'll restart later"})

            if resp == wx.YES:
                # Close all windows in this application...
                for w in wx.GetTopLevelWindows():
                    if isinstance(w, wx.Dialog):
                        w.Destroy()
                    elif isinstance(w, wx.Frame):
                        w.Close(True) # force close (can't be cancelled)
                wx.Yield()

                # ...find the path of the esky bootstrap/wrapper program...
                exe = esky.util.appexe_from_executable(sys.executable)

                # ...and tell our RestartInfo object about it.
                info.exe = exe

                # Make sure the CWD not in the current version's appdir, so it can
                # hopefully be cleaned up either as we exit or as the next verison
                # is starting.
                os.chdir(os.path.dirname(exe))

                # With all the top level windows closed the MainLoop should exit
                # automatically, but just in case tell it to exit so we can have a
                # normal-as-possible shutdown of this process. Hopefully there
                # isn't anything happening after we return from this function that
                # matters.
                self.ExitMainLoop()

            return

        # Start the worker thread that will check for an update, it will call
        # processResults when it is finished.
        import wx.lib.delayedresult as dr
        dr.startWorker(processResults, doFindUpdate)



    def _updateProgress(self, status):
        # Show progress of the download and install. This function is passed to Esky
        # functions to use as a callback.
        if self._pd is None and status.get('status') != 'done':
            self._pd = wx.ProgressDialog('Software Update', ' '*40,
                                          style=wx.PD_CAN_ABORT|wx.PD_APP_MODAL,
                                          parent=self._parentWindow)
            self._pd.Update(0, '')

            if self._parentWindow:
                self._pd.CenterOnParent()

        simpleMsgMap = { 'searching'   : 'Searching...',
                         'retrying'    : 'Retrying...',
                         'ready'       : 'Download complete...',
                         'installing'  : 'Installing...',
                         'cleaning up' : 'Cleaning up...',}

        if status.get('status') in simpleMsgMap:
            self._doUpdateProgress(True, simpleMsgMap[status.get('status')])

        elif status.get('status') == 'found':
            self._doUpdateProgress(True, 'Found version %s...' % status.get('new_version'))

        elif status.get('status') == 'downloading':
            received = status.get('received')
            size = status.get('size')
            currentPercentage = 1.0 * received / size * 100
            if currentPercentage > 99.5:
                self._doUpdateProgress(False, "Unzipping...", int(currentPercentage))
            else:
                self._doUpdateProgress(False, "Downloading...", int(currentPercentage))

        elif status.get('status') == 'done':
            if self._pd:
                self._pd.Destroy()
            self._pd = None

        wx.Yield()


    def _doUpdateProgress(self, pulse, message, value=0):
        if pulse:
            keepGoing, skip = self._pd.Pulse(message)
        else:
            keepGoing, skip = self._pd.Update(value, message)
        if not keepGoing: # user pressed the cancel button
            self._pd.Destroy()
            self._pd = None
            raise UpdateAbortedError()


    def _fixSysExecutable(self):
        # It looks like at least some versions of py2app are setting
        # sys.executable to ApplicationName.app/Contents/MacOS/python instead
        # of ApplicationName.app/Contents/MacOS/applicationname, which is what
        # should be used to relaunch the application. Other freezer tools set
        # sys.executable to the actual executable as expected, so we'll tweak
        # the setting here for Macs too.
        if sys.platform == "darwin" and hasattr(sys, 'frozen') \
           and sys.frozen == 'macosx_app' and sys.executable.endswith('MacOS/python'):
                names = os.listdir(os.path.dirname(sys.executable))
                assert len(names) == 2  # there should be only 2
                for name in names:
                    if name != 'python':
                        sys.executable = os.path.join(os.path.dirname(sys.executable), name)
                        break

#----------------------------------------------------------------------


