# -*- coding: utf-8 -*-
#
# Author:   Werner F. Bruhin
# Purpose:  how to I18N enable an application
#
# Inspired by the I18N wxPython demo and the Internationalization page on
# the wxPython wiki.
#

import sys
import os

import wx

# Install a custom displayhook to keep Python from setting the global
# _ (underscore) to the value of the last evaluated expression.  If
# we don't do this, our mapping of _ to gettext can get overwritten.
# This is useful/needed in interactive debugging with PyShell.

def _displayHook(obj):
    if obj is not None:
        print (repr(obj))

# add translation macro to builtin similar to what gettext does
import builtins
builtins.__dict__['_'] = wx.GetTranslation

import app_const as appC

from wx.lib.mixins.inspection import InspectionMixin

class BaseApp(wx.App, InspectionMixin):
    def OnInit(self):
        self.Init() # InspectionMixin
        # work around for Python stealing "_"
        sys.displayhook = _displayHook

        self.appName = "I18N sample application"

        self.doConfig()

        self.locale = None
        wx.Locale.AddCatalogLookupPathPrefix('locale')
        self.updateLanguage(self.appConfig.Read(u"Language"))

        return True

    def doConfig(self):
        """Setup an application configuration file"""
        # configuration folder
        sp = wx.StandardPaths.Get()
        self.configLoc = sp.GetUserConfigDir()
        self.configLoc = os.path.join(self.configLoc, self.appName)
        # win: C:\Users\userid\AppData\Roaming\appName
        # nix: \home\userid\appName

        if not os.path.exists(self.configLoc):
            os.mkdir(self.configLoc)

        # AppConfig stuff is here
        self.appConfig = wx.FileConfig(appName=self.appName,
                                       vendorName=u'who you wish',
                                       localFilename=os.path.join(
                                       self.configLoc, "AppConfig"))

        if not self.appConfig.HasEntry(u'Language'):
            # on first run we default to German
            self.appConfig.Write(key=u'Language', value=u'de')

        self.appConfig.Flush()

    def updateLanguage(self, lang):
        """
        Update the language to the requested one.

        Make *sure* any existing locale is deleted before the new
        one is created.  The old C++ object needs to be deleted
        before the new one is created, and if we just assign a new
        instance to the old Python variable, the old C++ locale will
        not be destroyed soon enough, likely causing a crash.

        :param string `lang`: one of the supported language codes

        """
        # if an unsupported language is requested default to English
        if lang in appC.supLang:
            selLang = appC.supLang[lang]
        else:
            selLang = wx.LANGUAGE_ENGLISH

        if self.locale:
            assert sys.getrefcount(self.locale) <= 2
            del self.locale

        # create a locale object for this language
        self.locale = wx.Locale(selLang)
        if self.locale.IsOk():
            self.locale.AddCatalog(appC.langDomain)
        else:
            self.locale = None

