#---------------------------------------------------------------------------
# Name:        etg/printfw.py
# Author:      Robin Dunn
#
# Created:     20-Apr-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "printfw"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxPreviewControlBar",
           "wxPreviewCanvas",
           "wxPreviewFrame",
           "wxPrintPreview",
           "wxPrinter",
           "wxPrintout",
           "wxPrintAbortDialog",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxPreviewControlBar')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)
    c.find('CreateButtons').isVirtual = True
    c.find('GetZoomControl').isVirtual = True
    c.find('SetZoomControl').isVirtual = True

    #c.find('GetPrintPreview').isVirtual = True
    c.find('GetPrintPreview').type = 'wxPrintPreview*'
    c.find('GetPrintPreview').setCppCode("return static_cast<wxPrintPreview*>(self->GetPrintPreview());")


    c = module.find('wxPreviewCanvas')
    tools.fixWindowClass(c)
    c.bases = ['wxScrolledWindow']


    c = module.find('wxPreviewFrame')
    tools.fixTopLevelWindowClass(c)
    c.find('wxPreviewFrame.preview').type = 'wxPrintPreview*'
    c.find('wxPreviewFrame.preview').transfer = True
    c.find('CreateCanvas').isVirtual = True
    c.find('CreateControlBar').isVirtual = True
    c.find('Initialize').isVirtual = True



    c = module.find('wxPrintPreview')
    c.mustHaveApp()
    for ctor in [c.find('wxPrintPreview').findOverload('wxPrintDialogData'),
                 c.find('wxPrintPreview').findOverload('wxPrintData')]:
        ctor.find('printout').transfer = True
        ctor.find('printoutForPrinting').transfer = True
    c.addPrivateCopyCtor()
    c.addCppMethod('int', '__nonzero__', '()', "return self->IsOk();")
    c.addCppMethod('int', '__bool__', '()', "return self->IsOk();")

    c.addPyCode("PrintPreview.Ok = wx.deprecated(PrintPreview.IsOk, 'Use IsOk instead.')")

    c = module.find('wxPrinter')
    c.addPrivateCopyCtor()



    c = module.find('wxPrintout')
    c.mustHaveApp()
    c.addPrivateCopyCtor()
    c.find('GetPPIPrinter.w').out = True
    c.find('GetPPIPrinter.h').out = True
    c.find('GetPPIScreen.w').out = True
    c.find('GetPPIScreen.h').out = True
    c.find('GetPageSizePixels.w').out = True
    c.find('GetPageSizePixels.h').out = True
    c.find('GetPageSizeMM.w').out = True
    c.find('GetPageSizeMM.h').out = True

    c.find('GetPageInfo.minPage').out = True
    c.find('GetPageInfo.maxPage').out = True
    c.find('GetPageInfo.pageFrom').out = True
    c.find('GetPageInfo.pageTo').out = True


    c = module.find('wxPrintAbortDialog')
    tools.fixTopLevelWindowClass(c)


    module.find('wxPrinter').mustHaveApp()


    # deprecated classes
    module.addPyCode("PyPrintPreview = wx.deprecated(PrintPreview, 'Use PrintPreview instead.')")
    module.addPyCode("PyPreviewFrame = wx.deprecated(PreviewFrame, 'Use PreviewFrame instead.')")
    module.addPyCode("PyPreviewControlBar = wx.deprecated(PreviewControlBar, 'Use PreviewControlBar instead.')")
    module.addPyCode("PyPrintout = wx.deprecated(Printout, 'Use Printout instead.')")

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

