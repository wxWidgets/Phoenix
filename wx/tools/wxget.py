#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# Name:        wx.tools.wxget
# Purpose:     wx Based alternative to wget
#
# Author:      Steve Barnes
#
# Created:     06-Aug-2017
# Copyright:   (c) 2017 by Steve Barnes
# Licence:     wxWindows license
# Tags:        phoenix-port, py3-port
#----------------------------------------------------------------------
"""
wx Version of wget utility for platform that don't have it already.

Module to allow cross platform downloads originally from answers to:
https://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
by Stan and PabloG then converted to wx.
"""
from __future__ import (division, absolute_import, print_function, unicode_literals)

import sys
import os
import wx

if sys.version_info >= (3,):
    from urllib.error import HTTPError
    import urllib.request as urllib2
    import urllib.parse as urlparse
else:
    import urllib2
    from urllib2 import HTTPError
    import urlparse

def get_save_path(url, dest_dir, force=False):
    """ Get the file save location."""
    if not dest_dir:
        dest = os.getcwd()
    filename = os.path.basename(urlparse.urlsplit(url)[2])
    if not filename:
        filename = 'downloaded.file'

    if not force:
        dlg = wx.FileDialog(
            None, message="Save As ...", defaultDir=dest,
            defaultFile=filename, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        )
        if dlg.ShowModal() == wx.ID_OK:
            dest, filename = os.path.split(dlg.GetPath())
        else:
            url = None
        del dlg
    else:
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        elif not os.path.isdir(dest_dir):
            url = None

    if dest:
        filename = os.path.join(dest, filename)

    return (url, filename)

def download_file(url, dest=None, force=False):
    """
    Download and save a file specified by url to dest directory, with force will
    operate silently and overwrite any existing file.
    """
    url, filename = get_save_path(url, dest, force)
    if url is None:
        return 'Aborted!'

    if url:
        try:
            url_res = urllib2.urlopen(url)
            keep_going = True
        except HTTPError as err:
            return "Error: %s" % err

    with open(filename, 'wb') as outfile:
        block_sz = 8192
        meta = url_res.info()
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
        meta_length = meta_func("Content-Length")
        file_size = None
        if meta_length:
            file_size = int(meta_length[0])
        message = "Downloading: {0}\nBytes: {1}\n".format(url, file_size)
        dstyle = wx.PD_APP_MODAL | wx.PD_CAN_ABORT | wx.PD_AUTO_HIDE
        if file_size:
            progress = wx.ProgressDialog('Downloading', message,
                                         maximum=1+file_size/block_sz, style=dstyle)
        else:
            progress = wx.ProgressDialog('Downloading', message, style=dstyle)

        file_size_dl = 0
        while keep_going:
            read_buffer = url_res.read(block_sz)
            if not read_buffer:
                progress.Update(file_size_dl / block_sz, "message+\nDONE!")
                wx.Sleep(0.2)
                break

            file_size_dl += len(read_buffer)
            outfile.write(read_buffer)

            status = "{0:16}".format(file_size_dl)
            if file_size:
                status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
            (keep_going, dummy_skip) = progress.Update(file_size_dl / block_sz,
                                                       message+status)
            wx.Sleep(0.08)  # Give the GUI some update time
        progress.Destroy()

    return filename

if __name__ == "__main__":  # Only run if this file is called directly
    APP = wx.App()
    MESSAGE = '\n'.join([
        "USAGE:\n\twxget URL [dest_dir]",
        "Will get a file from a file URL and save it to the destinaton or ."
    ])
    if len(sys.argv) > 2:
        DEST_DIR = sys.argv[2]
    else:
        DEST_DIR = None
    if len(sys.argv) > 1:
        URL = sys.argv[1]
    else:
        print(MESSAGE)
        YES_NO = wx.MessageBox(MESSAGE+"\nRUN TEST?", "wxget",
                               wx.YES_NO|wx.CENTER)
        if YES_NO == wx.YES:
            print("Testing with wxDemo")
            URL = "https://extras.wxpython.org/wxPython4/extras/4.0.0a3/wxPython-demo-4.0.0a3.tar.gz"
        else:
            URL = None
    if URL:
        FILENAME = download_file(URL)
        print(FILENAME)
