.. include:: headings.inc


.. _classic vs phoenix:

=======================================
|phoenix_title|  **Classic vs Phoenix**
=======================================

Introduction
------------

This document contains a list of the most common wxPython functions, classes and :class:`Window` / :class:`Sizer`
methods which need to be changed to a new syntax in Phoenix; it presents the modification in a 2-columns,
space-separated table containing the old wxPython (Classic) name on the left and the new (if it exists)
Phoenix name on the right. I found it impressively useful while porting AGW to Phoenix.


Functions and Classes Modifications
-----------------------------------

===========================================================  ===========================================================
`Classic` Name                                               `Phoenix` Name
===========================================================  ===========================================================
AboutBox                                                     :func:`wx.adv.AboutBox <AboutBox>`
AboutDialogInfo                                              :class:`wx.adv.AboutDialogInfo`
AcceleratorEntry_Create                                      ``MISSING``
ANIHandler                                                   ``MISSING``
App_CleanUp                                                  ``MISSING``
ArtProvider_Delete                                           :meth:`wx.ArtProvider.Delete`
ArtProvider_GetBitmap                                        :meth:`wx.ArtProvider.GetBitmap`
ArtProvider_GetIcon                                          :meth:`wx.ArtProvider.GetIcon`
ArtProvider_GetIconBundle                                    :meth:`wx.ArtProvider.GetIconBundle`
ArtProvider_GetMessageBoxIcon                                :meth:`wx.ArtProvider.GetMessageBoxIcon`
ArtProvider_GetMessageBoxIconId                              :meth:`wx.ArtProvider.GetMessageBoxIconId`
ArtProvider_GetNativeSizeHint                                :meth:`wx.ArtProvider.GetNativeSizeHint`
ArtProvider_GetSizeHint                                      :meth:`wx.ArtProvider.GetSizeHint`
ArtProvider_HasNativeProvider                                :meth:`wx.ArtProvider.HasNativeProvider`
ArtProvider_Insert                                           :meth:`wx.ArtProvider.Insert`
ArtProvider_Pop                                              :meth:`wx.ArtProvider.Pop`
ArtProvider_Push                                             :meth:`wx.ArtProvider.Push`
ArtProvider_PushBack                                         :meth:`wx.ArtProvider.PushBack`
Bitmap.SetBitmapSelected                                     :meth:`wx.Bitmap.SetBitmapPressed`
BitmapFromBits                                               :class:`wx.Bitmap`
BitmapFromIcon                                               :class:`wx.Bitmap`
BitmapFromImage                                              :class:`wx.Bitmap`
BitmapFromXPMData                                            :class:`wx.Bitmap`
BMPHandler                                                   ``MISSING``
BookCtrlBase_GetClassDefaultAttributes                       :meth:`wx.BookCtrl.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
BrushFromBitmap                                              :class:`wx.Brush`
Button_GetClassDefaultAttributes                             :meth:`wx.Button.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
Button_GetDefaultSize                                        :meth:`wx.Button.GetDefaultSize`
CalculateLayoutEvent                                         :class:`wx.adv.CalculateLayoutEvent`
Caret_GetBlinkTime                                           :meth:`wx.Caret.GetBlinkTime`
Caret_SetBlinkTime                                           :meth:`wx.Caret.SetBlinkTime`
CheckBox_GetClassDefaultAttributes                           :meth:`wx.CheckBox.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
Choice_GetClassDefaultAttributes                             :meth:`wx.Choice.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
ChoicebookEvent                                              :class:`wx.BookCtrlEvent`
Clipboard_Get                                                :meth:`wx.Clipboard.Get`
ClipboardEvent                                               :class:`wx.ClipboardTextEvent`
ClipboardLocker                                              ``MISSING``
Colour.SetFromString                                         :meth:`wx.Colour.Set`
ColourRGB                                                    :class:`wx.Colour`
ComboBox_GetClassDefaultAttributes                           :meth:`wx.ComboBox.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
CommandLinkButton                                            :class:`wx.adv.CommandLinkButton`
ConfigBase_Create                                            :meth:`wx.ConfigBase.Create`
ConfigBase_DontCreateOnDemand                                :meth:`wx.ConfigBase.DontCreateOnDemand`
ConfigBase_Get                                               :meth:`wx.ConfigBase.Get`
ConfigBase_Set                                               :meth:`wx.ConfigBase.Set`
Control_Ellipsize                                            :meth:`wx.Control.Ellipsize`
Control_EscapeMnemonics                                      :meth:`wx.Control.EscapeMnemonics`
Control_FindAccelIndex                                       ``MISSING``
Control_GetClassDefaultAttributes                            :meth:`wx.Control.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
Control_GetCompositeControlsDefaultAttributes                ``MISSING``
Control_RemoveMnemonics                                      :meth:`wx.Control.RemoveMnemonics`
CPPFileSystemHandler                                         ``REMOVED``
CreateFileTipProvider                                        :func:`wx.adv.CreateFileTipProvider <CreateFileTipProvider>`
CURHandler                                                   ``MISSING``
CursorFromImage                                              :class:`wx.Cursor`
CustomDataFormat                                             :class:`wx.DataFormat`
DateEvent                                                    :class:`wx.adv.DateEvent`
DatePickerCtrl                                               :class:`wx.adv.DatePickerCtrl`
DatePickerCtrlBase                                           :class:`wx.adv.DatePickerCtrl`
DateSpan_Day                                                 :meth:`wx.DateSpan.Day`
DateSpan_Days                                                :meth:`wx.DateSpan.Days`
DateSpan_Month                                               :meth:`wx.DateSpan.Month`
DateSpan_Months                                              :meth:`wx.DateSpan.Months`
DateSpan_Week                                                :meth:`wx.DateSpan.Week`
DateSpan_Weeks                                               :meth:`wx.DateSpan.Weeks`
DateSpan_Year                                                :meth:`wx.DateSpan.Year`
DateSpan_Years                                               :meth:`wx.DateSpan.Years`
DateTime_ConvertYearToBC                                     :meth:`wx.DateTime.ConvertYearToBC`
DateTime_GetAmPmStrings                                      :meth:`wx.DateTime.GetAmPmStrings`
DateTime_GetBeginDST                                         :meth:`wx.DateTime.GetBeginDST`
DateTime_GetCentury                                          :meth:`wx.DateTime.GetCentury`
DateTime_GetCountry                                          :meth:`wx.DateTime.GetCountry`
DateTime_GetCurrentMonth                                     :meth:`wx.DateTime.GetCurrentMonth`
DateTime_GetCurrentYear                                      :meth:`wx.DateTime.GetCurrentYear`
DateTime_GetEndDST                                           :meth:`wx.DateTime.GetEndDST`
DateTime_GetEnglishMonthName                                 :meth:`wx.DateTime.GetEnglishMonthName`
DateTime_GetEnglishWeekDayName                               :meth:`wx.DateTime.GetEnglishWeekDayName`
DateTime_GetMonthName                                        :meth:`wx.DateTime.GetMonthName`
DateTime_GetNumberOfDaysInMonth                              ``MISSING``
DateTime_GetNumberOfDaysinYear                               ``MISSING``
DateTime_GetWeekDayName                                      :meth:`wx.DateTime.GetWeekDayName`
DateTime_IsDSTApplicable                                     :meth:`wx.DateTime.IsDSTApplicable`
DateTime_IsLeapYear                                          :meth:`wx.DateTime.IsLeapYear`
DateTime_IsWestEuropeanCountry                               :meth:`wx.DateTime.IsWestEuropeanCountry`
DateTime_Now                                                 :meth:`wx.DateTime.Now`
DateTime_SetCountry                                          :meth:`wx.DateTime.SetCountry`
DateTime_SetToWeekOfYear                                     :meth:`wx.DateTime.SetToWeekOfYear`
DateTime_Today                                               :meth:`wx.DateTime.Today`
DateTime_UNow                                                :meth:`wx.DateTime.UNow`
DateTimeFromDateTime                                         :class:`wx.DateTime`
Dialog_EnableLayoutAdaptation                                :meth:`wx.Dialog.EnableLayoutAdaptation`
Dialog_GetClassDefaultAttributes                             :meth:`wx.Dialog.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
Dialog_GetLayoutAdapter                                      :meth:`wx.Dialog.GetLayoutAdapter`
Dialog_IsLayoutAdaptationEnabled                             :meth:`wx.Dialog.IsLayoutAdaptationEnabled`
Dialog_SetLayoutAdapter                                      :meth:`wx.Dialog.SetLayoutAdapter`
DirItemData                                                  ``MISSING``
Display_GetCount                                             :meth:`wx.Display.GetCount`
Display_GetFromPoint                                         :meth:`wx.Display.GetFromPoint`
Display_GetFromWindow                                        :meth:`wx.Display.GetFromWindow`
DragIcon                                                     ``MISSING``
DragListItem                                                 ``MISSING``
DragString                                                   ``MISSING``
DragTreeItem                                                 ``MISSING``
DROP_ICON                                                    ``MISSING``
EmptyBitmap                                                  :class:`wx.Bitmap`
EmptyIcon                                                    :class:`wx.Icon`
EmptyImage                                                   :class:`wx.Image`
EncodingConverter                                            ``MISSING``
EncodingConverter_CanConvert                                 ``MISSING``
EncodingConverter_GetAllEquivalents                          ``MISSING``
EncodingConverter_GetPlatformEquivalents                     ``MISSING``
EventLoopBase_GetActive                                      :meth:`wx.EventLoopBase.GetActive`
EventLoopBase_SetActive                                      :meth:`wx.EventLoopBase.SetActive`
EventProcessInHandlerOnly                                    ``MISSING``
EVT_COMMAND                                                  ``MISSING``
EVT_COMMAND_RANGE                                            ``MISSING``
ExpandEnvVars                                                ``MISSING``
FFontFromPixelSize                                           :class:`wx.Font`
FileConfig_GetGlobalFileName                                 :meth:`wx.FileConfig.GetGlobalFileName`
FileConfig_GetLocalFileName                                  :meth:`wx.FileConfig.GetLocalFileName`
FileSystem_AddHandler                                        :meth:`wx.FileSystem.AddHandler`
FileSystem_CleanUpHandlers                                   ``MISSING``
FileSystem_FileNameToURL                                     :meth:`wx.FileSystem.FileNameToURL`
FileSystem_RemoveHandler                                     :meth:`wx.FileSystem.RemoveHandler`
FileSystem_URLToFileName                                     :meth:`wx.FileSystem.URLToFileName`
FileSystemHandler_GetAnchor                                  ``MISSING``
FileSystemHandler_GetLeftLocation                            ``MISSING``
FileSystemHandler_GetMimeTypeFromExt                         :meth:`wx.FileSystemHandler.GetMimeTypeFromExt`
FileSystemHandler_GetProtocol                                ``MISSING``
FileSystemHandler_GetRightLocation                           ``MISSING``
FileType_ExpandCommand                                       :meth:`wx.FileType.ExpandCommand`
FileTypeInfoSequence                                         ``MISSING``
FindWindowById                                               :meth:`wx.Window.FindWindowById`
Font2                                                        :class:`wx.Font`
Font_AdjustToSymbolicSize                                    ``MISSING``
Font_GetDefaultEncoding                                      :meth:`wx.Font.GetDefaultEncoding`
Font_SetDefaultEncoding                                      :meth:`wx.Font.SetDefaultEncoding`
FontEnumerator_GetEncodings                                  :meth:`wx.FontEnumerator.GetEncodings`
FontEnumerator_GetFacenames                                  :meth:`wx.FontEnumerator.GetFacenames`
FontEnumerator_IsValidFacename                               :meth:`wx.FontEnumerator.IsValidFacename`
FontFromNativeInfo                                           :class:`wx.Font`
FontFromNativeInfoString                                     :class:`wx.Font`
FontFromPixelSize                                            :class:`wx.Font`
FontMapper_Get                                               :meth:`wx.FontMapper.Get`
FontMapper_GetDefaultConfigPath                              ``MISSING``
FontMapper_GetEncoding                                       :meth:`wx.FontMapper.GetEncoding`
FontMapper_GetEncodingDescription                            :meth:`wx.FontMapper.GetEncodingDescription`
FontMapper_GetEncodingFromName                               :meth:`wx.FontMapper.GetEncodingFromName`
FontMapper_GetEncodingName                                   :meth:`wx.FontMapper.GetEncodingName`
FontMapper_GetSupportedEncodingsCount                        :meth:`wx.FontMapper.GetSupportedEncodingsCount`
FontMapper_Set                                               :meth:`wx.FontMapper.Set`
Frame_GetClassDefaultAttributes                              :meth:`wx.Frame.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
FutureCall                                                   :class:`wx.CallLater`
Gauge_GetClassDefaultAttributes                              :meth:`wx.Gauge.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
GBSizerItemSizer                                             :class:`wx.GbSizerItem`
GBSizerItemSpacer                                            :class:`wx.GbSizerItem`
GBSizerItemWindow                                            :class:`wx.GbSizerItem`
GDIObjListBase                                               ``MISSING``
GenericFindWindowAtPoint                                     :func:`wx.FindWindowAtPoint`
GetAccelFromString                                           ``MISSING``
GetCurrentId                                                 ``MISSING``
GetCurrentTime                                               ``MISSING``
GetDefaultPyEncoding                                         ``REMOVED``
GetDisplayDepth                                              :func:`wx.DisplayDepth`
GetFreeMemory                                                ``MISSING``
GetLocale                                                    ``MISSING``
GetLocalTime                                                 ``MISSING``
GetLocalTimeMillis                                           ``MISSING``
GetNativeFontEncoding                                        ``MISSING``
GetNumberFromUser                                            ``MISSING``
GetPasswordFromUser                                          ``MISSING``
GetSingleChoiceIndex                                         ``MISSING``
GetStockHelpString                                           ``MISSING``
GetStockLabel                                                ``MISSING``
GetTextFromUser                                              ``MISSING``
GetUTCTime                                                   ``MISSING``
GetXDisplay                                                  ``MISSING``
GIFHandler                                                   ``MISSING``
GraphicsContext_Create                                       :meth:`wx.GraphicsContext.Create`
GraphicsContext_CreateFromNative                             :meth:`wx.GraphicsContext.CreateFromNative`
GraphicsContext_CreateFromNativeWindow                       :meth:`wx.GraphicsContext.CreateFromNativeWindow`
GraphicsContext_CreateMeasuringContext                       :meth:`wx.GraphicsContext.Create`
GraphicsRenderer_GetCairoRenderer                            :meth:`wx.GraphicsRenderer.GetCairoRenderer`
GraphicsRenderer_GetDefaultRenderer                          :meth:`wx.GraphicsRenderer.GetDefaultRenderer`
HelpProvider_Get                                             :meth:`wx.HelpProvider.Get`
HelpProvider_Set                                             :meth:`wx.HelpProvider.Set`
HtmlListBox                                                  ``MISSING``
HyperlinkCtrl                                                :class:`wx.adv.HyperlinkCtrl`
HyperlinkEvent                                               :class:`wx.adv.HyperlinkEvent`
ICOHandler                                                   ``MISSING``
IconBundleFromFile                                           :class:`wx.IconBundle`
IconBundleFromIcon                                           :class:`wx.IconBundle`
IconBundleFromStream                                         :class:`wx.IconBundle`
IconFromBitmap                                               :class:`wx.Icon`
IconFromLocation                                             :class:`wx.Icon`
IconFromXPMData                                              :class:`wx.Icon`
IdleEvent_GetMode                                            :meth:`wx.IdleEvent.GetMode`
IdleEvent_SetMode                                            :meth:`wx.IdleEvent.SetMode`
Image_AddHandler                                             :meth:`wx.Image.AddHandler`
Image_CanRead                                                :meth:`wx.Image.CanRead`
Image_CanReadStream                                          :meth:`wx.Image.CanRead`
Image_GetHandlers                                            ``MISSING``
Image_GetImageCount                                          :meth:`wx.Image.GetImageCount`
Image_GetImageExtWildcard                                    :meth:`wx.Image.GetImageExtWildcard`
Image_HSVtoRGB                                               :meth:`wx.Image.HSVtoRGB`
Image_HSVValue                                               :class:`wx.HSVValue`
Image_InsertHandler                                          :meth:`wx.Image.InsertHandler`
Image_RemoveHandler                                          :meth:`wx.Image.RemoveHandler`
Image_RGBtoHSV                                               :meth:`wx.Image.RGBtoHSV`
Image_RGBValue                                               :class:`wx.RGBValue`
ImageFromMime                                                :class:`wx.Image`
ImageFromStream                                              :class:`wx.Image`
ImageFromStreamMime                                          :class:`wx.Image`
ImageHistogram_MakeKey                                       :meth:`wx.ImageHistogram.MakeKey`
IsStockID                                                    ``MISSING``
IsStockLabel                                                 ``MISSING``
Joystick                                                     :class:`wx.adv.Joystick`
JPEGHandler                                                  ``MISSING``
KeyEvent.m_altDown                                           :meth:`wx.KeyboardState.GetModifiers`
KeyEvent.m_controlDown                                       :meth:`wx.KeyboardState.GetModifiers`
KeyEvent.m_keyCode                                           :attr:`wx.KeyEvent.KeyCode`
KeyEvent.m_metaDown                                          :meth:`wx.KeyboardState.GetModifiers`
KeyEvent.m_shiftDown                                         :meth:`wx.KeyboardState.GetModifiers`
KeyEvent.m_x                                                 :attr:`wx.KeyEvent.X`
KeyEvent.m_y                                                 :attr:`wx.KeyEvent.Y`
LayoutAlgorithm                                              :class:`wx.adv.LayoutAlgorithm`
ListbookEvent                                                :class:`wx.BookCtrlEvent`
ListBox_GetClassDefaultAttributes                            :meth:`wx.ListBox.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
ListCtrl_GetClassDefaultAttributes                           :meth:`wx.ListCtrl.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
ListCtrl_HasColumnOrderSupport                               :meth:`wx.ListCtrl.HasColumnOrderSupport`
ListEvent.m_code                                             :attr:`wx.ListEvent.KeyCode`
ListEvent.m_col                                              :attr:`wx.ListEvent.Column`
ListEvent.m_item                                             :attr:`wx.ListEvent.Item`
ListEvent.m_itemIndex                                        :attr:`wx.ListEvent.Index`
ListEvent.m_oldItemIndex                                     :attr:`wx.ListEvent.CacheFrom`
ListEvent.m_pointDrag                                        :attr:`wx.ListEvent.Point`
ListItem.m_col                                               :attr:`wx.ListItem.Column`
ListItem.m_data                                              :attr:`wx.ListItem.Data`
ListItem.m_format                                            :attr:`wx.ListItem.Align`
ListItem.m_image                                             :attr:`wx.ListItem.Image`
ListItem.m_itemId                                            :attr:`wx.ListItem.Id`
ListItem.m_mask                                              :attr:`wx.ListItem.Mask`
ListItem.m_state                                             :attr:`wx.ListItem.State`
ListItem.m_stateMask                                         :attr:`wx.ListItem.State`
ListItem.m_text                                              :attr:`wx.ListItem.Text`
ListItem.m_width                                             :attr:`wx.ListItem.Width`
Locale_AddCatalogLookupPathPrefix                            :meth:`wx.Locale.AddCatalogLookupPathPrefix`
Locale_AddLanguage                                           :meth:`wx.Locale.AddLanguage`
Locale_FindLanguageInfo                                      :meth:`wx.Locale.FindLanguageInfo`
Locale_GetInfo                                               :meth:`wx.Locale.GetInfo`
Locale_GetLanguageCanonicalName                              :meth:`wx.Locale.GetLanguageCanonicalName`
Locale_GetLanguageInfo                                       :meth:`wx.Locale.GetLanguageInfo`
Locale_GetLanguageName                                       :meth:`wx.Locale.GetLanguageName`
Locale_GetSystemEncoding                                     :meth:`wx.Locale.GetSystemEncoding`
Locale_GetSystemEncodingName                                 :meth:`wx.Locale.GetSystemEncodingName`
Locale_GetSystemLanguage                                     :meth:`wx.Locale.GetSystemLanguage`
Locale_IsAvailable                                           :meth:`wx.Locale.IsAvailable`
Log_AddTraceMask                                             :meth:`wx.Log.AddTraceMask`
Log_ClearTraceMasks                                          :meth:`wx.Log.ClearTraceMasks`
Log_DoCreateOnDemand                                         ``MISSING``
Log_DontCreateOnDemand                                       :meth:`wx.Log.DontCreateOnDemand`
Log_EnableLogging                                            :meth:`wx.Log.EnableLogging`
Log_FlushActive                                              :meth:`wx.Log.FlushActive`
Log_GetActiveTarget                                          :meth:`wx.Log.GetActiveTarget`
Log_GetComponentLevel                                        ``MISSING``
Log_GetLogLevel                                              :meth:`wx.Log.GetLogLevel`
Log_GetRepetitionCounting                                    :meth:`wx.Log.GetRepetitionCounting`
Log_GetTimestamp                                             :meth:`wx.Log.GetTimestamp`
Log_GetTraceMask                                             ``MISSING``
Log_GetTraceMasks                                            :meth:`wx.Log.GetTraceMasks`
Log_GetVerbose                                               :meth:`wx.Log.GetVerbose`
Log_IsAllowedTraceMask                                       :meth:`wx.Log.IsAllowedTraceMask`
Log_IsEnabled                                                :meth:`wx.Log.IsEnabled`
Log_IsLevelEnabled                                           :meth:`wx.Log.IsLevelEnabled`
Log_RemoveTraceMask                                          :meth:`wx.Log.RemoveTraceMask`
Log_Resume                                                   :meth:`wx.Log.Resume`
Log_SetActiveTarget                                          :meth:`wx.Log.SetActiveTarget`
Log_SetComponentLevel                                        :meth:`wx.Log.SetComponentLevel`
Log_SetLogLevel                                              :meth:`wx.Log.SetLogLevel`
Log_SetRepetitionCounting                                    :meth:`wx.Log.SetRepetitionCounting`
Log_SetTimestamp                                             :meth:`wx.Log.SetTimestamp`
Log_SetTraceMask                                             ``MISSING``
Log_SetVerbose                                               :meth:`wx.Log.SetVerbose`
Log_Suspend                                                  :meth:`wx.Log.Suspend`
Log_TimeStamp                                                ``MISSING``
LogInfo                                                      :func:`wx.LogMessage`
LogStatusFrame                                               :func:`wx.LogStatus`
LogTrace                                                     ``MISSING``
MaskColour                                                   :class:`wx.Colour`
MemoryDCFromDC                                               :class:`wx.MemoryDC`
MemoryFSHandler_AddFile                                      :meth:`wx.MemoryFSHandler.AddFile`
MemoryFSHandler_AddFileWithMimeType                          :meth:`wx.MemoryFSHandler.AddFileWithMimeType`
MemoryFSHandler_RemoveFile                                   :meth:`wx.MemoryFSHandler.RemoveFile`
MenuBar_GetAutoWindowMenu                                    ``MISSING``
MenuBar_MacSetCommonMenuBar                                  :meth:`wx.MenuBar.MacSetCommonMenuBar`
MenuBar_SetAutoWindowMenu                                    ``MISSING``
MenuItem_GetDefaultMarginWidth                               ``MISSING``
MenuItem_GetLabelText                                        :meth:`wx.MenuItem.GetLabelText`
MetaFile                                                     :class:`wx.msw.MemoryDC`
MetafileDataObject                                           ``MISSING``
MetaFileDC                                                   :class:`wx.msw.MetafileDC`
MimeTypesManager_IsOfType                                    :meth:`wx.MimeTypesManager.IsOfType`
ModalEventLoop                                               ``MISSING``
MutexGuiEnter                                                ``MISSING``
MutexGuiLeave                                                ``MISSING``
MutexGuiLocker                                               ``MISSING``
NamedColour                                                  :class:`wx.Colour`
NativeEncodingInfo                                           ``MISSING``
NcPaintEvent                                                 ``MISSING``
Notebook_GetClassDefaultAttributes                           :meth:`wx.Notebook.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
NotebookEvent                                                :class:`wx.BookCtrlEvent`
NotebookPage                                                 ``MISSING``
NotificationMessage                                          :class:`wx.adv.NotificationMessage`
NullFileTypeInfo                                             ``MISSING``
Panel_GetClassDefaultAttributes                              :meth:`wx.Panel.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
PCXHandler                                                   ``MISSING``
PlatformInformation_GetOperatingSystemDirectory              :meth:`wx.PlatformInfo.GetOperatingSystemDirectory`
PNGHandler                                                   ``MISSING``
PNMHandler                                                   ``MISSING``
Point2DCopy                                                  :class:`wx.Point2DDouble`
Point2DFromPoint                                             :class:`wx.Point2DDouble`
PreBitmapButton                                              :class:`wx.BitmapButton`
PreButton                                                    :class:`wx.Button`
PreCheckBox                                                  :class:`wx.CheckBox`
PreCheckListBox                                              :class:`wx.CheckListBox`
PreChoice                                                    :class:`wx.Choice`
PreChoicebook                                                :class:`wx.Choicebook`
PreCollapsiblePane                                           :class:`wx.CollapsiblePane`
PreColourPickerCtrl                                          :class:`wx.ColourPickerCtrl`
PreComboBox                                                  :class:`wx.ComboBox`
PreCommandLinkButton                                         :class:`wx.adv.CommandLinkButton`
PreControl                                                   :class:`wx.Control`
PreDatePickerCtrl                                            :class:`wx.adv.DatePickerCtrl`
PreDialog                                                    :class:`wx.Dialog`
PreDirFilterListCtrl                                         :class:`wx.DirFilterListCtrl`
PreDirPickerCtrl                                             :class:`wx.DirPickerCtrl`
PreFileCtrl                                                  :class:`wx.FileCtrl`
PreFilePickerCtrl                                            :class:`wx.FilePickerCtrl`
PreFindReplaceDialog                                         :class:`wx.FindReplaceDialog`
PreFontPickerCtrl                                            :class:`wx.FontPickerCtrl`
PreFrame                                                     :class:`wx.Frame`
PreGauge                                                     :class:`wx.Gauge`
PreGenericDirCtrl                                            :class:`wx.GenericDirCtrl`
PreHScrolledWindow                                           :class:`wx.HScrolledWindow`
PreHtmlListBox                                               ``MISSING``
PreHVScrolledWindow                                          :class:`wx.HVScrolledWindow`
PreHyperlinkCtrl                                             :class:`wx.adv.HyperlinkCtrl`
PreInfoBar                                                   :class:`wx.InfoBar`
PreListbook                                                  :class:`wx.Listbook`
PreListBox                                                   :class:`wx.ListBox`
PreListCtrl                                                  :class:`wx.ListCtrl`
PreListView                                                  :class:`wx.ListView`
PreMDIChildFrame                                             :class:`wx.MDIChildFrame`
PreMDIClientWindow                                           :class:`wx.MDIClientWindow`
PreMDIParentFrame                                            :class:`wx.MDIParentFrame`
PreMiniFrame                                                 :class:`wx.MiniFrame`
PreNotebook                                                  :class:`wx.Notebook`
PrePanel                                                     :class:`wx.Panel`
PrePopupTransientWindow                                      :class:`wx.PopupTransientWindow`
PrePopupWindow                                               :class:`wx.PopupWindow`
PrePyAxBaseWindow                                            ``MISSING``
PrePyControl                                                 :class:`wx.Control`
PrePyPanel                                                   :class:`wx.Panel`
PrePyPickerBase                                              :class:`wx.PickerBase`
PrePyScrolledWindow                                          :class:`wx.ScrolledWindow`
PrePyWindow                                                  :class:`wx.Window`
PreRadioBox                                                  :class:`wx.RadioBox`
PreRadioButton                                               :class:`wx.RadioButton`
PreSashLayoutWindow                                          :class:`wx.adv.SashLayoutWindow`
PreSashWindow                                                :class:`wx.adv.SashWindow`
PreScrollBar                                                 :class:`wx.ScrollBar`
PreScrolledWindow                                            :class:`wx.ScrolledWindow`
PreSearchCtrl                                                :class:`wx.SearchCtrl`
PreSimpleHtmlListBox                                         ``MISSING``
PreSingleInstanceChecker                                     :class:`wx.SingleInstanceChecker`
PreSlider                                                    :class:`wx.Slider`
PreSpinButton                                                :class:`wx.SpinButton`
PreSpinCtrl                                                  :class:`wx.SpinCtrl`
PreSpinCtrlDouble                                            :class:`wx.SpinCtrlDouble`
PreSplitterWindow                                            :class:`wx.SplitterWindow`
PreStaticBitmap                                              :class:`wx.StaticBitmap`
PreStaticBox                                                 :class:`wx.StaticBox`
PreStaticLine                                                :class:`wx.StaticLine`
PreStaticText                                                :class:`wx.StaticText`
PreStatusBar                                                 :class:`wx.StatusBar`
PreTextCtrl                                                  :class:`wx.TextCtrl`
PreToggleButton                                              :class:`wx.ToggleButton`
PreToolBar                                                   :class:`wx.ToolBar`
PreToolbook                                                  :class:`wx.Toolbook`
PreTreebook                                                  :class:`wx.Treebook`
PreTreeCtrl                                                  :class:`wx.TreeCtrl`
PreVListBox                                                  :class:`wx.VListBox`
PreVScrolledWindow                                           :class:`wx.VScrolledWindow`
PreWindow                                                    :class:`wx.Window`
Printer_GetLastError                                         :meth:`wx.Printer.GetLastError`
Process_Exists                                               :meth:`wx.Process.Exists`
Process_Kill                                                 :meth:`wx.Process.Kill`
Process_Open                                                 :meth:`wx.Process.Open`
PseudoDC                                                     :class:`wx.adv.PseudoDC`
PyApp_GetComCtl32Version                                     :meth:`wx.PyApp.GetComCtl32Version`
PyApp_GetMacAboutMenuItemId                                  :meth:`wx.PyApp.GetMacAboutMenuItemId`
PyApp_GetMacExitMenuItemId                                   :meth:`wx.PyApp.GetMacExitMenuItemId`
PyApp_GetMacHelpMenuTitleName                                :meth:`wx.PyApp.GetMacHelpMenuTitleName`
PyApp_GetMacPreferencesMenuItemId                            :meth:`wx.PyApp.GetMacPreferencesMenuItemId`
PyApp_GetMacSupportPCMenuShortcuts                           ``MISSING``
PyApp_GetShell32Version                                      :meth:`wx.PyApp.GetShell32Version`
PyApp_GetTraitsIfExists                                      ``MISSING``
PyApp_IsDisplayAvailable                                     :meth:`wx.PyApp.IsDisplayAvailable`
PyApp_IsMainLoopRunning                                      :meth:`wx.PyApp.IsMainLoopRunning <AppConsole.IsMainLoopRunning>`
PyApp_SetMacAboutMenuItemId                                  :meth:`wx.PyApp.SetMacAboutMenuItemId`
PyApp_SetMacExitMenuItemId                                   :meth:`wx.PyApp.SetMacExitMenuItemId`
PyApp_SetMacHelpMenuTitleName                                :meth:`wx.PyApp.SetMacHelpMenuTitleName`
PyApp_SetMacPreferencesMenuItemId                            :meth:`wx.PyApp.SetMacPreferencesMenuItemId`
PyApp_SetMacSupportPCMenuShortcuts                           ``MISSING``
PyAxBaseWindow_FromHWND                                      ``MISSING``
PyBitmapDataObject                                           :class:`wx.BitmapDataObject`
PyControl                                                    :class:`wx.Control`
PyDataObjectSimple                                           :class:`wx.DataObjectSimple`
PyDeadObjectError                                            `RuntimeError`
PyDropTarget                                                 :class:`wx.DropTarget`
PyEvtHandler                                                 :class:`wx.EvtHandler`
PyImageHandler                                               :class:`wx.ImageHandler`
PyLocale                                                     :class:`wx.Locale`
PyLog                                                        :class:`wx.Log`
PyPanel                                                      :class:`wx.Panel`
PyPickerBase                                                 :class:`wx.PickerBase`
PyPreviewControlBar                                          :class:`wx.PreviewControlBar`
PyPreviewFrame                                               :class:`wx.PreviewFrame`
PyPrintPreview                                               :class:`wx.PrintPreview`
PyScrolledWindow                                             :class:`wx.ScrolledWindow`
PySimpleApp                                                  :class:`wx.App`
PyTextDataObject                                             :class:`wx.TextDataObject`
PyTimer                                                      :class:`wx.Timer`
PyTipProvider                                                :class:`wx.adv.TipProvider`
PyValidator                                                  :class:`wx.Validator`
PyWindow                                                     :class:`wx.Window`
Quantize                                                     ``MISSING``
Quantize_Quantize                                            ``MISSING``
QueryLayoutInfoEvent                                         :class:`wx.adv.QueryLayoutInfoEvent`
RadioBox_GetClassDefaultAttributes                           :meth:`wx.RadioBox.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
RadioButton_GetClassDefaultAttributes                        :meth:`wx.RadioButton.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
RectPP                                                       :class:`wx.Rect`
RectPS                                                       :class:`wx.Rect`
RectS                                                        :class:`wx.Rect`
Rect.OffsetXY                                                :meth:`wx.Rect.Offset`
RegionFromBitmap                                             :class:`wx.Region`
RegionFromBitmapColour                                       :class:`wx.Region`
RegionFromPoints                                             :class:`wx.Region`
RendererNative_Get                                           :meth:`wx.RendererNative.Get`
RendererNative_GetDefault                                    :meth:`wx.RendererNative.GetDefault`
RendererNative_GetGeneric                                    :meth:`wx.RendererNative.GetGeneric`
RendererNative_Set                                           :meth:`wx.RendererNative.Set`
RendererVersion_IsCompatible                                 :meth:`wx.RendererVersion.IsCompatible`
SashEvent                                                    :class:`wx.adv.SashEvent`
SashLayoutWindow                                             :class:`wx.adv.SashLayoutWindow`
SashWindow                                                   :class:`wx.adv.SashWindow`
ScrollBar_GetClassDefaultAttributes                          :meth:`wx.ScrollBar.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
ScrolledWindow_GetClassDefaultAttributes                     :meth:`wx.ScrolledWindow.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
ScrollHelper                                                 :class:`wx.VarHVScrollHelper`
SearchCtrlBase                                               :class:`wx.SearchCtrl`
SetCursor                                                    ``MISSING``
SetDefaultPyEncoding                                         ``REMOVED``
SetBitmapSelected                                            :meth:`wx.AnyButton.SetBitmapPressed`
ShowTip                                                      :func:`wx.adv.ShowTip`
SimpleHtmlListBox                                            ``MISSING``
SizerFlags_GetDefaultBorder                                  :meth:`wx.SizerFlags.GetDefaultBorder`
SizerItemSizer                                               :class:`wx.SizerItem`
SizerItemSpacer                                              :class:`wx.SizerItem`
SizerItemWindow                                              :class:`wx.SizerItem`
Slider_GetClassDefaultAttributes                             :meth:`wx.Slider.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
Sound                                                        :class:`wx.adv.Sound`
Sound_PlaySound                                              :meth:`wx.adv.Sound.PlaySound`
Sound_Stop                                                   :meth:`wx.adv.Sound.Stop`
SoundFromData                                                :class:`wx.adv.Sound`
SpinButton_GetClassDefaultAttributes                         :meth:`wx.SpinButton.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
SpinCtrl_GetClassDefaultAttributes                           :meth:`wx.SpinCtrl.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
SplashScreen                                                 :class:`wx.adv.SplashScreen`
SplashScreenWindow                                           ``MISSING``
SplitterWindow.SetSashSize                                   ``REMOVED``
SplitterWindow_GetClassDefaultAttributes                     :meth:`wx.SplitterWindow.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
StandardDialogLayoutAdapter                                  ``MISSING``
StandardDialogLayoutAdapter_DoFitWithScrolling               ``MISSING``
StandardDialogLayoutAdapter_DoMustScroll                     ``MISSING``
StandardDialogLayoutAdapter_DoReparentControls               ``MISSING``
StandardPaths_Get                                            :meth:`wx.StandardPaths.Get`
StaticBitmap_GetClassDefaultAttributes                       :meth:`wx.StaticBitmap.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
StaticBox_GetClassDefaultAttributes                          :meth:`wx.StaticBox.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
StaticLine_GetClassDefaultAttributes                         :meth:`wx.StaticLine.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
StaticLine_GetDefaultSize                                    :meth:`wx.StaticLine.GetDefaultSize`
StaticText_GetClassDefaultAttributes                         :meth:`wx.StaticText.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
StatusBar_GetClassDefaultAttributes                          :meth:`wx.StatusBar.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
StockCursor                                                  :class:`wx.Cursor`
StockGDI_DeleteAll                                           :meth:`wx.StockGDI.DeleteAll`
StockGDI_GetBrush                                            :meth:`wx.StockGDI.GetBrush`
StockGDI_GetColour                                           :meth:`wx.StockGDI.GetColour`
StockGDI_GetCursor                                           :meth:`wx.StockGDI.GetCursor`
StockGDI_GetPen                                              :meth:`wx.StockGDI.GetPen`
StockGDI_instance                                            :meth:`wx.StockGDI.instance`
StopWatch                                                    ``MISSING``
StyledTextCtrl.SetUseAntiAliasing						     ``REMOVED``
SystemOptions_GetOption                                      :meth:`wx.SystemOptions.GetOption`
SystemOptions_GetOptionInt                                   :meth:`wx.SystemOptions.GetOptionInt`
SystemOptions_HasOption                                      :meth:`wx.SystemOptions.HasOption`
SystemOptions_IsFalse                                        :meth:`wx.SystemOptions.IsFalse`
SystemOptions_SetOption                                      :meth:`wx.SystemOptions.SetOption`
SystemOptions_SetOptionInt                                   :meth:`wx.SystemOptions.SetOption`
SystemSettings_GetColour                                     :meth:`wx.SystemSettings.GetColour`
SystemSettings_GetFont                                       :meth:`wx.SystemSettings.GetFont`
SystemSettings_GetMetric                                     :meth:`wx.SystemSettings.GetMetric`
SystemSettings_GetScreenType                                 :meth:`wx.SystemSettings.GetScreenType`
SystemSettings_HasFeature                                    :meth:`wx.SystemSettings.HasFeature`
SystemSettings_SetScreenType                                 ``MISSING``
TaskBarIcon                                                  :class:`wx.adv.TaskBarIcon`
TaskBarIcon_IsAvailable                                      :meth:`wx.adv.TaskBarIcon.IsAvailable`
TaskBarIconEvent                                             :class:`wx.adv.TaskBarIconEvent`
TestFontEncoding                                             ``MISSING``
TextAreaBase                                                 ``NONE (implementation detail)``
TextAttr_BitlistsEqPartial                                   ``MISSING``
TextAttr_Combine                                             ``MISSING``
TextAttr_CombineBitlists                                     ``MISSING``
TextAttr_RemoveStyle                                         ``MISSING``
TextAttr_SplitParaCharStyles                                 ``MISSING``
TextAttr_TabsEq                                              ``MISSING``
TextCtrl_GetClassDefaultAttributes                           :meth:`wx.TextCtrl.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
TextCtrlBase                                                 ``NONE (implementation detail)``
TextCtrlIface                                                ``NONE (implementation detail)``
TextEntryBase                                                ``NONE (implementation detail)``
TextUrlEvent                                                 ``MISSING``
TGAHandler                                                   ``MISSING``
Thread_IsMain                                                :meth:`wx.IsMainThread`
ThreadEvent                                                  ``MISSING``
TIFFHandler                                                  ``MISSING``
TimeSpan_Day                                                 :meth:`wx.TimeSpan.Day`
TimeSpan_Days                                                :meth:`wx.TimeSpan.Days`
TimeSpan_Hour                                                :meth:`wx.TimeSpan.Hour`
TimeSpan_Hours                                               :meth:`wx.TimeSpan.Hours`
TimeSpan_Millisecond                                         :meth:`wx.TimeSpan.Millisecond`
TimeSpan_Milliseconds                                        :meth:`wx.TimeSpan.Milliseconds`
TimeSpan_Minute                                              :meth:`wx.TimeSpan.Minute`
TimeSpan_Minutes                                             :meth:`wx.TimeSpan.Minutes`
TimeSpan_Second                                              :meth:`wx.TimeSpan.Second`
TimeSpan_Seconds                                             :meth:`wx.TimeSpan.Seconds`
TimeSpan_Week                                                :meth:`wx.TimeSpan.Week`
TimeSpan_Weeks                                               :meth:`wx.TimeSpan.Weeks`
TipProvider                                                  :class:`wx.adv.TipProvider`
ToggleButton_GetClassDefaultAttributes                       :meth:`wx.ToggleButton.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
ToolBar_GetClassDefaultAttributes                            :meth:`wx.ToolBar.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
ToolbookEvent                                                :class:`wx.BookCtrlEvent`
ToolTip_Enable                                               :meth:`wx.ToolTip.Enable`
ToolTip_SetAutoPop                                           :meth:`wx.ToolTip.SetAutoPop`
ToolTip_SetDelay                                             :meth:`wx.ToolTip.SetDelay`
ToolTip_SetMaxWidth                                          :meth:`wx.ToolTip.SetMaxWidth`
ToolTip_SetReshow                                            :meth:`wx.ToolTip.SetReshow`
TopLevelWindow_GetDefaultSize                                :meth:`wx.TopLevelWindow.GetDefaultSize`
Trap                                                         ``MISSING``
TreebookEvent                                                :class:`wx.BookCtrlEvent`
TreeCtrl_GetClassDefaultAttributes                           :meth:`wx.TreeCtrl.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
TreeItemData                                                 ``REMOVED`` (a MappedType is being used instead to handle setting any PyObject as item data.)
UpdateUIEvent_CanUpdate                                      :meth:`wx.UpdateUIEvent.CanUpdate`
UpdateUIEvent_GetMode                                        :meth:`wx.UpdateUIEvent.GetMode`
UpdateUIEvent_GetUpdateInterval                              :meth:`wx.UpdateUIEvent.GetUpdateInterval`
UpdateUIEvent_ResetUpdateTime                                :meth:`wx.UpdateUIEvent.ResetUpdateTime`
UpdateUIEvent_SetMode                                        :meth:`wx.UpdateUIEvent.SetMode`
UpdateUIEvent_SetUpdateInterval                              :meth:`wx.UpdateUIEvent.SetUpdateInterval`
Validator_IsSilent                                           :meth:`wx.Validator.IsSilent`
Validator_SetBellOnError                                     ``REMOVED``
Validator_SuppressBellOnError                                :meth:`wx.Validator.SuppressBellOnError`
WakeUpMainThread                                             ``MISSING``
Window_FindFocus                                             :meth:`wx.Window.FindFocus`
Window_FromHWND                                              ``MISSING``
Window_GetCapture                                            :meth:`wx.Window.GetCapture`
Window_GetClassDefaultAttributes                             :meth:`wx.Window.GetClassDefaultAttributes`
Window_NewControlId                                          :meth:`wx.Window.NewControlId`
Window_UnreserveControlId                                    :meth:`wx.Window.UnreserveControlId`
XPMHandler                                                   ``MISSING``
YieldIfNeeded                                                :meth:`wx.App.Yield` wx.GetApp().Yield(onlyIfNeeded=True)
===========================================================  ===========================================================


:class:`wx.DC` Modifications
-------------------------

===========================================================  ===========================================================
`Classic` Name                                               `Phoenix` Name
===========================================================  ===========================================================
BeginDrawing                                                 ``REMOVED``
BlitPointSize                                                :meth:`wx.DC.Blit`
CalcBoundingBoxPoint                                         :meth:`wx.DC.CalcBoundingBox`
CrossHairPoint                                               :meth:`wx.DC.CrossHair`
DrawArcPoint                                                 :meth:`wx.DC.DrawArc`
DrawBitmapPoint                                              :meth:`wx.DC.DrawBitmap`
DrawCheckMarkRect                                            :meth:`wx.DC.DrawCheckMark`
DrawCirclePoint                                              :meth:`wx.DC.DrawCircle`
DrawEllipsePointSize                                         :meth:`wx.DC.DrawEllipse`
DrawEllipseRect                                              :meth:`wx.DC.DrawEllipse`
DrawEllipticArcPointSize                                     :meth:`wx.DC.DrawEllipticArc`
DrawIconPoint                                                :meth:`wx.DC.DrawIcon`
DrawLinePoint                                                :meth:`wx.DC.DrawLine`
DrawPointPoint                                               :meth:`wx.DC.DrawPoint`
DrawRectanglePointSize                                       :meth:`wx.DC.DrawRectangle`
DrawRectangleRect                                            :meth:`wx.DC.DrawRectangle`
DrawRotatedTextPoint                                         :meth:`wx.DC.DrawRotatedText`
DrawRoundedRectanglePointSize                                :meth:`wx.DC.DrawRoundedRectangle`
DrawRoundedRectangleRect                                     :meth:`wx.DC.DrawRoundedRectangle`
DrawTextPoint                                                :meth:`wx.DC.DrawText`
EndDrawing                                                   ``REMOVED``
FloodFillPoint                                               :meth:`wx.DC.FloodFill`
GetDeviceOriginTuple                                         :meth:`wx.DC.GetDeviceOrigin`
GetImpl                                                      ``REMOVED``
GetLogicalOriginTuple                                        :meth:`wx.DC.GetLogicalOrigin`
GetMultiLineTextExtent                                       :meth:`wx.DC.GetFullMultiLineTextExtent`
GetOptimization                                              ``REMOVED``
GetPixelPoint                                                :meth:`wx.DC.GetPixel`
GetResolution                                                :meth:`wx.DC.GetPPI`
GetSizeMMTuple                                               :meth:`wx.DC.GetSizeMM`
Ok                                                           :meth:`wx.DC.IsOk`
SetClippingRect                                              :meth:`wx.DC.SetClippingRegion`
SetClippingRegionAsRegion                                    :meth:`wx.DC.SetClippingRegion`
SetClippingRegionPointSize                                   :meth:`wx.DC.SetClippingRegion`
SetDeviceOriginPoint                                         :meth:`wx.DC.SetDeviceOrigin`
SetLogicalOriginPoint                                        :meth:`wx.DC.SetLogicalOrigin`
SetOptimization                                              ``REMOVED``
StretchBlitPointSize                                         :meth:`wx.DC.StretchBlit`
===========================================================  ===========================================================


:class:`wx.Window` Modifications
-----------------------------

===========================================================  ===========================================================
`Classic` Name                                               `Phoenix` Name
===========================================================  ===========================================================
ClientToScreenXY                                             :meth:`wx.Window.ClientToScreen`
ConvertDialogPointToPixels                                   :meth:`wx.Window.ConvertDialogToPixels`
ConvertDialogSizeToPixels                                    :meth:`wx.Window.ConvertDialogToPixels`
GetAdjustedBestSize                                          :meth:`wx.Window.GetEffectiveMinSize`
GetBestFittingSize                                           :meth:`wx.Window.GetEffectiveMinSize`
GetBestSizeTuple                                             :meth:`wx.Window.GetBestSize`
GetClientSizeTuple                                           :meth:`wx.Window.GetClientSize`
GetScreenPositionTuple                                       :meth:`wx.Window.GetScreenPosition`
GetSizeTuple                                                 :meth:`wx.Window.GetSize`
GetToolTipString                                             :meth:`wx.Window.GetToolTipText`
HitTestXY                                                    :meth:`wx.Window.HitTest`
IsExposedPoint                                               :meth:`wx.Window.IsExposed`
IsExposedRect                                                :meth:`wx.Window.IsExposed`
MakeModal                                                    ``REMOVED``
PopupMenuXY                                                  :meth:`wx.Window.PopupMenu`
ScreenToClientXY                                             :meth:`wx.Window.ScreenToClient`
SetBestFittingSize                                           :meth:`wx.Window.SetInitialSize`
SetClientSizeWH                                              :meth:`wx.Window.SetClientSize`
SetDimensions                                                :meth:`wx.Window.SetSize`
SetHelpTextForId                                             :meth:`wx.Window.SetHelpText`
SetSizeHintsSz                                               :meth:`wx.Window.SetSizeHints`
SetToolTipString                                             :meth:`wx.Window.SetToolTip`
SetVirtualSizeHints                                          ``REMOVED``
SetVirtualSizeHintsSz                                        ``REMOVED``
===========================================================  ===========================================================


:class:`wx.Sizer` Modifications
----------------------------

===========================================================  ===========================================================
`Classic` Name                                               `Phoenix` Name
===========================================================  ===========================================================
AddF                                                         :meth:`wx.Sizer.Add`
AddItem                                                      :meth:`wx.Sizer.Add`
AddSizer                                                     :meth:`wx.Sizer.Add`
AddWindow                                                    :meth:`wx.Sizer.Add`
DeleteWindows                                                :meth:`wx.Sizer.Clear`
GetItemIndex                                                 :meth:`wx.Sizer.GetItem`
GetMinSizeTuple                                              :meth:`wx.Sizer.GetMinSize`
GetPositionTuple                                             :meth:`wx.Sizer.GetPosition`
InsertF                                                      :meth:`wx.Sizer.Insert`
InsertItem                                                   :meth:`wx.Sizer.Insert`
InsertSizer                                                  :meth:`wx.Sizer.Insert`
InsertWindow                                                 :meth:`wx.Sizer.Insert`
PrependF                                                     :meth:`wx.Sizer.Prepend`
PrependItem                                                  :meth:`wx.Sizer.Prepend`
PrependSizer                                                 :meth:`wx.Sizer.Prepend`
PrependWindow                                                :meth:`wx.Sizer.Prepend`
RemovePos                                                    :meth:`wx.Sizer.Remove`
RemoveSizer                                                  :meth:`wx.Sizer.Remove`
RemoveWindow                                                 :meth:`wx.Sizer.Remove`
===========================================================  ===========================================================





wx.lib Modifications
--------------------

===========================================================  ===========================================================
`Classic` Name                                               `Phoenix` Name
===========================================================  ===========================================================
wx.lib.buttonpanel                                           :mod:`wx.lib.agw.buttonpanel`
wx.lib.customtreectrl                                        :mod:`wx.lib.agw.customtreectrl`
wx.lib.flatnotebook                                          :mod:`wx.lib.agw.flatnotebook`
wx.lib.foldpanelbar                                          :mod:`wx.lib.agw.foldpanelbar`
wx.lib.hyperlink                                             :mod:`wx.lib.agw.hyperlink`
wx.lib.grids                                                 ``REMOVED``
wx.lib.pyshell                                               ``REMOVED``
wx.lib.rightalign                                            ``REMOVED``
wx.lib.shell                                                 ``REMOVED``
wx.lib.splashscreen                                          ``REMOVED``
wx.lib.wxPlotCanvas                                          ``REMOVED``
===========================================================  ===========================================================




Modules which have moved
------------------------

===========================================================  ===========================================================
`Classic` Name                                               `Phoenix` Name
===========================================================  ===========================================================
wx.calendar.CalendarCtrl                                     :mod:`wx.adv.CalendarCtrl`
wx.animate.Animation                                         :mod:`wx.adv.Animation`
wx.animate.AnimationCtrl                                     :mod:`wx.adv.AnimationCtrl`
wx.combo.OwnerDrawnComboBox                                  :mod:`wx.adv.OwnerDrawnComboBox`
wx.gizmos.EditableListBox                                    :mod:`wx.adv.EditableListBox`
wx.gizmos.TreeListCtrl                                       :mod:`wx.lib.gizmos.TreeListCtrl`
wx.AboutBox                                                  :meth:`wx.adv.AboutBox`
wx.AboutDialogInfo                                           :mod:`wx.adv.AboutDialogInfo`
wx.DatePickerCtrl                                            :mod:`wx.adv.DatePickerCtrl`
wx.GenericDatePickerCtrl                                     :mod:`wx.adv.GenericDatePickerCtrl`
wx.TaskBarIcon                                               :mod:`wx.adv.TaskBarIcon`
wx.SplashScreen                                              :mod:`wx.adv.SplashScreen`
wx.wizard.Wizard                                             :mod:`wx.adv.Wizard`
===========================================================  ===========================================================
