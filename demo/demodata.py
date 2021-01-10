# demodata.py

"""
Globals for the main.py wxPython demo.
"""

#-------------------------------------------------------------------------------
#
# _demoPngs
#
# These are the images names used in the demo treectrl.
# These come from images.py or bitmaps/imagename.ext
#
# _demoPngs = ["imagename1", "imagename2", "etc"]
#
#-------------------------------------------------------------------------------

_demoPngs = ["overview", "recent", "frame", "dialog", "moredialog", "core",
             "book", "customcontrol", "morecontrols", "layout", "process",
             "clipboard", "images", "miscellaneous"]


#-------------------------------------------------------------------------------
#
# _treeList
#
# These are the Demo Category Headers
# and Demo Module Names(Ex: Frame.py without ext)
#
# ('Demo Category Name String', [
#       'DemoModuleName1',
#       'DemoModuleName2',
#       'Etc',
#       ]),
#
#-------------------------------------------------------------------------------

_treeList = [
    # new stuff
    ('Recent Additions/Updates', [
        'Simplebook',
        'LEDNumberCtrl',
        'DynamicSashWindow',
        'TreeListCtrl',
        'NotificationMessage',
        'AddPrivateFont',
        'ScrolledThumbnail',
        'SVGImage_Bitmap',
        'SVGImage_Render',
        'ActivityIndicator',
        'GenericCheckBox',
        'CheckListCtrl',
    ]),

    # managed windows == things with a (optional) caption you can close
    ('Frames and Dialogs', [
        'AUI_DockingWindowMgr',
        'AUI_MDI',
        'Dialog',
        'Frame',
        'MDIWindows',
        'MiniFrame',
        'Wizard',
    ]),

    # the common dialogs
    ('Common Dialogs', [
        'AboutBox',
        'ColourDialog',
        'DirDialog',
        'FileDialog',
        'FindReplaceDialog',
        'FontDialog',
        'MessageDialog',
        'MultiChoiceDialog',
        'PageSetupDialog',
        'PrintDialog',
        'ProgressDialog',
        'SingleChoiceDialog',
        'TextEntryDialog',
        'RearrangeDialog',
        'RichMessageDialog',
    ]),

    # dialogs from libraries
    ('More Dialogs', [
        'ImageBrowser',
        'ScrolledMessageDialog',
    ]),

    # core controls
    ('Core Windows/Controls', [
        'ActivityIndicator',
        'BitmapButton',
        'Button',
        'CheckBox',
        'CheckListBox',
        'Choice',
        'ComboBox',
        'CommandLinkButton',
        'DVC_CustomRenderer',
        'DVC_DataViewModel',
        'DVC_IndexListModel',
        'DVC_ListCtrl',
        'DVC_TreeCtrl',
        'Gauge',
        'Grid',
        'Grid_MegaExample',
        'GridLabelRenderer',
        'ListBox',
        'ListCtrl',
        'ListCtrl_virtual',
        'ListCtrl_edit',
        'Menu',
        'PopupMenu',
        'PopupWindow',
        'RadioBox',
        'RadioButton',
        'SashWindow',
        'ScrolledWindow',
        'SearchCtrl',
        'Slider',
        'SpinButton',
        'SpinCtrl',
        'SpinCtrlDouble',
        'SplitterWindow',
        'StaticBitmap',
        'StaticBox',
        'StaticText',
        'StatusBar',
        'StockButtons',
        'TextCtrl',
        'ToggleButton',
        'ToolBar',
        'TreeCtrl',
        'Validator',
    ]),

    ('"Book" Controls', [
        'AUI_Notebook',
        'Choicebook',
        'FlatNotebook',
        'Listbook',
        'Notebook',
        'Simplebook',
        'Toolbook',
        'Treebook',
    ]),

    ('Custom Controls', [
        'AnalogClock',
        'ColourSelect',
        'ComboTreeBox',
        'Editor',
        'FileCtrl',
        'GenericButtons',
        'GenericCheckBox',
        'GenericDirCtrl',
        'ItemsPicker',
        'LEDNumberCtrl',
        'MultiSash',
        'PlateButton',
        'PopupControl',
        'PyColourChooser',
        'TreeListCtrl',
    ]),

    # controls coming from other libraries
    ('More Windows/Controls', [
        'ActiveX_FlashWindow',
        'ActiveX_IEHtmlWindow',
        'ActiveX_PDFWindow',
        'BitmapComboBox',
        'Calendar',
        'CalendarCtrl',
        'CheckListCtrl',
        'CollapsiblePane',
        'ComboCtrl',
        'ContextHelp',
        'DatePickerCtrl',
        'DynamicSashWindow',
        'EditableListBox',
        'ExpandoTextCtrl',
        'FancyText',
        'FileBrowseButton',
        'FloatCanvas',
        'HtmlWindow',
        'HTML2_WebView',
        'InfoBar',
        'IntCtrl',
        'MaskedEditControls',
        'MaskedNumCtrl',
        'MediaCtrl',
        'MultiSplitterWindow',
        'NotificationMessage',
        'OwnerDrawnComboBox',
        'Pickers',
        'PropertyGrid',
        'PyCrust',
        'PyPlot',
        'PyShell',
        'ResizeWidget',
        'RichTextCtrl',
        'ScrolledPanel',
        'StyledTextCtrl_1',
        'StyledTextCtrl_2',
        'TablePrint',
        'Throbber',
        'Ticker',
        'TimeCtrl',
        'TimePickerCtrl',
        'TreeMixin',
        'VListBox',
    ]),

    # How to lay out the controls in a frame/dialog
    ('Window Layout', [
        'GridBagSizer',
        'LayoutAnchors',
        'LayoutConstraints',
        'Layoutf',
        'ScrolledPanel',
        'SizedControls',
        'Sizers',
        'WrapSizer',
        'XmlResource',
        'XmlResourceHandler',
        'XmlResourceSubclass',
    ]),

    # ditto
    ('Process and Events', [
        'DelayedResult',
        'EventManager',
        'KeyEvents',
        'Process',
        'PythonEvents',
        'Threads',
        'Timer',
        ##'infoframe',    # needs better explanation and some fixing
    ]),

    # Clipboard and DnD
    ('Clipboard and DnD', [
        'CustomDragAndDrop',
        'DragAndDrop',
        'URLDragAndDrop',
    ]),

    # Images
    ('Using Images', [
        'AdjustChannels',
        'AlphaDrawing',
        'AnimationCtrl',
        'ArtProvider',
        'BitmapFromBuffer',
        'Cursor',
        'DragImage',
        'Image',
        'ImageAlpha',
        'ImageFromStream',
        'Img2PyArtProvider',
        'Mask',
        'RawBitmapAccess',
        'SVGImage_Bitmap',
        'SVGImage_Render',
        'Throbber',
    ]),

    # Other stuff
    ('Miscellaneous', [
        'AlphaDrawing',
        'BannerWindow',
        'Cairo',
        'Cairo_Snippets',
        'ColourDB',
        'DragScroller',
        'DrawXXXList',
        'FileHistory',
        'FontEnumerator',
        'AddPrivateFont',
        'GetMouseState',
        'GraphicsContext',
        'GraphicsGradient',
        'GLCanvas',
        'I18N',
        'Joystick',
        'MimeTypesManager',
        'MouseGestures',
        'OGL',
        'Overlay',
        'PDFViewer',
        'PenAndBrushStyles',
        'PrintFramework',
        'PseudoDC',
        'RendererNative',
        'ShapedWindow',
        'Sound',
        'StandardPaths',
        'SVGImage_Bitmap',
        'SVGImage_Render',
        'SystemSettings',
        'ToolTip',
        'UIActionSimulator',
        'Unicode',
    ]),

    ('Check out the samples dir too', []),

]
