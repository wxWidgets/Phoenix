This folder contains Cairo header files and DLLs for Windows, which enable
building Cairo support in wxWidgets on Windows, (in wx.GraphicsContext) as
well as using Cairo directly from Python, integrated with wxPython using the
wx.lib.wxcairo package. These DLLs will be included by default in the binary
builds for Windows.

These files were originally extracted from a zip file available from the
following location:

    https://github.com/preshing/cairo-windows

Note that the projects represented by these DLLs are released under the LGPL
or similar licenses. The DLLs are able to be included with wxPython because
they are not statically linked, and because end users are able to replace them
with newer or rebuilt versions if desired so long as they use a compatible
API/ABI, (for example a replacement libcairo would need to be compatible with
Cairo 1.15.12).  Source code is available at their respective project pages.
