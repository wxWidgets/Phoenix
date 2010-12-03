#---------------------------------------------------------------------------
# Name:        etg/window.py
# Author:      Robin Dunn
#
# Created:     27-Nov-2010
# Copyright:   (c) 2010 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "window"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxVisualAttributes',
           'wxWindow' ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.    
    
    c = module.find('wxWindow')
    assert isinstance(c, etgtools.ClassDef)

    # ignore some overloads that will be ambiguous afer wrapping
    c.find('GetChildren').overloads = []
    c.find('GetClientSize').findOverload('int *').ignore()
    c.find('GetSize').findOverload('int *').ignore()
    c.find('GetVirtualSize').findOverload('int *').ignore()
    c.find('GetPosition').findOverload('int *').ignore()
    c.find('GetScreenPosition').findOverload('int *').ignore()
    c.find('ClientToScreen').findOverload('int *').ignore()
    c.find('ScreenToClient').findOverload('int *').ignore()
    
    m = c.find('GetTextExtent').findOverload('int *')
    m.pyName = 'GetFullTextExtent'
    m.find('w').out = True
    m.find('h').out = True
    m.find('descent').out = True
    m.find('externalLeading').out = True
    
    c.find('GetHandle').type = 'void*'
    
    # Rename these overloads for symmetry with the getters of the same name
    c.find('SetSize').findOverload('wxRect').pyName = 'SetRect'
    c.find('SetClientSize').findOverload('wxRect').pyName = 'SetClientRect'
    
    # Add this method
    c.addCppMethod('wxWindow*', 'GetTopLevelParent', '()',
                   'sipRes =  wxGetTopLevelParent(sipCpp);')
    
    # TODO: make these be available on Windows, and empty stubs otherwise
    c.find('RegisterHotKey').ignore()
    c.find('UnregisterHotKey').ignore()

    # maybe these too
    c.find('GetAccessible').ignore()
    c.find('SetAccessible').ignore()

    # Make some of the protected methods overridable from Python
    c.find('DoCentre').ignore(False)
    c.find('DoGetBestSize').ignore(False)
    c.find('SetInitialBestSize').ignore(False)
    c.find('SendDestroyEvent').ignore(False)
    c.find('ProcessEvent').ignore(False)
    
    
    # Define some properties using the getters and setters
    c.addProperty('AcceleratorTable GetAcceleratorTable SetAcceleratorTable')
    c.addProperty('AutoLayout GetAutoLayout SetAutoLayout')
    c.addProperty('BackgroundColour GetBackgroundColour SetBackgroundColour')
    c.addProperty('BackgroundStyle GetBackgroundStyle SetBackgroundStyle')
    c.addProperty('EffectiveMinSize GetEffectiveMinSize')
    c.addProperty('BestSize GetBestSize')
    c.addProperty('BestVirtualSize GetBestVirtualSize')
    c.addProperty('Border GetBorder')
    c.addProperty('Caret GetCaret SetCaret')
    c.addProperty('CharHeight GetCharHeight')
    c.addProperty('CharWidth GetCharWidth')
    c.addProperty('Children GetChildren')
    c.addProperty('ClientAreaOrigin GetClientAreaOrigin')
    c.addProperty('ClientRect GetClientRect SetClientRect')
    c.addProperty('ClientSize GetClientSize SetClientSize')
    c.addProperty('Constraints GetConstraints SetConstraints')
    c.addProperty('ContainingSizer GetContainingSizer SetContainingSizer')
    c.addProperty('Cursor GetCursor SetCursor')
    c.addProperty('DefaultAttributes GetDefaultAttributes')
    c.addProperty('DropTarget GetDropTarget SetDropTarget')
    c.addProperty('EventHandler GetEventHandler SetEventHandler')
    c.addProperty('ExtraStyle GetExtraStyle SetExtraStyle')
    c.addProperty('Font GetFont SetFont')
    c.addProperty('ForegroundColour GetForegroundColour SetForegroundColour')
    c.addProperty('GrandParent GetGrandParent')
    c.addProperty('TopLevelParent GetTopLevelParent')
    c.addProperty('Handle GetHandle')
    c.addProperty('HelpText GetHelpText SetHelpText')
    c.addProperty('Id GetId SetId')
    c.addProperty('Label GetLabel SetLabel')
    c.addProperty('LayoutDirection GetLayoutDirection SetLayoutDirection')
    c.addProperty('MaxHeight GetMaxHeight')
    c.addProperty('MaxSize GetMaxSize SetMaxSize')
    c.addProperty('MaxWidth GetMaxWidth')
    c.addProperty('MinHeight GetMinHeight')
    c.addProperty('MinSize GetMinSize SetMinSize')
    c.addProperty('MinWidth GetMinWidth')
    c.addProperty('Name GetName SetName')
    c.addProperty('Parent GetParent')
    c.addProperty('Position GetPosition SetPosition')
    c.addProperty('Rect GetRect SetRect')
    c.addProperty('ScreenPosition GetScreenPosition')
    c.addProperty('ScreenRect GetScreenRect')
    c.addProperty('Size GetSize SetSize')
    c.addProperty('Sizer GetSizer SetSizer')
    c.addProperty('ThemeEnabled GetThemeEnabled SetThemeEnabled')
    c.addProperty('ToolTip GetToolTip SetToolTip')
    c.addProperty('UpdateClientRect GetUpdateClientRect')
    c.addProperty('UpdateRegion GetUpdateRegion')
    c.addProperty('Validator GetValidator SetValidator')
    c.addProperty('VirtualSize GetVirtualSize SetVirtualSize')
    c.addProperty('WindowStyle GetWindowStyle SetWindowStyle')
    c.addProperty('WindowStyleFlag GetWindowStyleFlag SetWindowStyleFlag')
    c.addProperty('WindowVariant GetWindowVariant SetWindowVariant')

    c.addProperty('Shown IsShown Show')
    c.addProperty('Enabled IsEnabled Enable')
    c.addProperty('TopLevel IsTopLevel')

    ##c.addProperty('GtkWidget GetGtkWidget')

    c.addProperty('MinClientSize GetMinClientSize SetMinClientSize')
    c.addProperty('MaxClientSize GetMaxClientSize SetMaxClientSize')
    

    
    
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

