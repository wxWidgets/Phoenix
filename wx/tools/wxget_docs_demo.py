#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# Name:        wx.tools.wxget_docs_demo
# Purpose:     wx fetch & launch demo or docs
#
# Author:      Steve Barnes
#
# Created:     06-Aug-2017
# Copyright:   (c) 2017 by Steve Barnes
# Licence:     wxWindows license
# Tags:        phoenix-port, py3-port
#
# Module to allow the correct version of the documents &/or demos to be
# launched after, if necessarily being fetched.
#----------------------------------------------------------------------

"""
wxget_docs_demo.py -- Launch the appropriate wx Docs or Demo.

Usage:
    wxget_docs_demo [docs|demo]

Will install if missing, the requested item for the current version and then
launch it.
"""
from __future__ import (division, absolute_import, print_function, unicode_literals)

import sys
import os
import subprocess
import webbrowser
import tarfile
if sys.version_info >= (3,):
    from urllib.error import HTTPError
    import urllib.request as urllib2
    import urllib.parse as urlparse
    from urllib.request import pathname2url
else:
    import urllib2
    from urllib2 import HTTPError
    import urlparse
    from urllib import pathname2url

import wx

import wxget

APP = None
WXVERSION = wx.version().split(' ')[0]
MAJOR = WXVERSION.split('.')[0]
if MAJOR != '4':
    raise ValueError("wx Versions other than 4 not supported!")

def endsure_wx_app():
    """ Ensure that there is a wx.App instance."""
    global APP
    if APP is None and not wx.GetApp():
        APP = wx.App()
        APP.SetAppName("wxPython")
    return (APP is not None)

def get_paths_dict():
    """ Get a dictionary of the required paths."""
    global APP
    endsure_wx_app()
    sp = wx.StandardPaths.Get()
    pathdict = {}
    pathdict['TempDir'] = sp.GetTempDir()
    pathdict['Cache'] = os.path.join(sp.GetUserLocalDataDir(), 'wxDocsDemoCache',
                                     WXVERSION)
    pathdict['Docs_URL'] = wxget.get_docs_demo_url(False)
    #pathdict['wxDocs'] = os.path.join(sp.GetAppDocumentsDir(), 'wxDocs', WXVERSION)
    pathdict['wxDocs'] = sp.GetAppDocumentsDir()
    pathdict['Docs_Name'] = "wxPython-docs-%s" % WXVERSION
    pathdict['Demo_URL'] = wxget.get_docs_demo_url(True)
    #pathdict['wxDemo'] = os.path.join(sp.GetUserLocalDataDir(), 'wxDemo', WXVERSION)
    pathdict['wxDemo'] = sp.GetUserLocalDataDir()
    pathdict['Demo_Name'] = "wxPython-demo-%s" % WXVERSION
    pathdict['Ext'] = 'tar.gz'
    return pathdict

def unpack_cached(cached, dest_dir):
    """ Unpack from the cache."""
    print('Unpack', cached, 'to', dest_dir)
    tf = tarfile.open(cached, "r:*")
    tf.extractall(dest_dir)
    dest_dir = os.listdir(dest_dir)[0]
    return dest_dir

def get_item(final, url, cache, name, ext):
    """ Get the item """
    print('Looking for', name, 'at', final)
    fullpath = os.path.join(final, name)
    if os.path.exists(fullpath):  # Already exists
        return fullpath

    cached = os.path.join(cache, name)
    cached = os.path.extsep.join([cached, ext])
    print('Looking for cashed', cached)
    if not os.path.exists(cached):  # No cached copy
        cached = wxget.download_file(url, cache, True)

    if os.path.exists(cached):  # We now have a cached copy
        unpack_cached(cached, final)
    else:
        fullpath = None
    return fullpath

def report_error(err_text):
    """ Report a problem."""
    endsure_wx_app()
    wx.MessageBox(err_text, caption='ERROR!',
                  style=wx.OK|wx.CENTRE|wx.ICON_ERROR)

def done(result=0):
    """ Tidy up and exit."""
    global APP
    if APP:
        print("Closing Launcher App!")  # Debug
        APP.Destroy()
    print("Done!")
    sys.exit(result)

def docs_main(args=sys.argv):
    """ Get/Launch Docs."""
    endsure_wx_app()
    result = 0
    print("Launch Docs for wxPython V%s" % WXVERSION)
    pd = get_paths_dict()
    location = get_item(pd['wxDocs'], pd['Docs_URL'], pd['Cache'],
                        pd['Docs_Name'], pd['Ext'])
    if location:
        location = os.path.join(location, 'docs', 'html', 'index.html')
        location_url = urlparse.urljoin('file:', pathname2url(location))
        print("Show Docs at:", location)
        webbrowser.open(location_url)
    else:
        result = 'Unable to find wx.Docs'
        report_error(result)
    done(result)

def demo_main(args=sys.argv):
    """ Get/Launch Demo."""
    result = 0
    endsure_wx_app()
    print("Launch Demo for wxPython V%s" % WXVERSION)
    pd = get_paths_dict()
    location = get_item(pd['wxDemo'], pd['Demo_URL'], pd['Cache'],
                        pd['Demo_Name'], pd['Ext'])
    if location:
        cmds = [sys.executable, os.path.join(location, "demo", "demo.py")]
        print("Launching", cmds[1])
        pid = subprocess.Popen(cmds).pid
        #subprocess.check_call(cmds) # Use instead for debug
        print("Demo starting as PID %s - may take a few seconds!" % pid)
    else:
        result = 'Unable to find wx.Demo'
        report_error(result)
    done(result)

def main(args=sys.argv):
    """ Command line main."""
    if len(args) > 1:
        if "demo" in args[1].lower():
            return demo_main()
        elif "docs" in args[1].lower():
            return docs_main()
        #else:
    print(__doc__)
    #else:
        #APP = wx.App()

if __name__ == "__main__":
    main()
