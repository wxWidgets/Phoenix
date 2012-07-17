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
AboutBox                                                     :func:`adv.AboutBox <AboutBox>`
AboutDialogInfo                                              :class:`adv.AboutDialogInfo`
AcceleratorEntry_Create                                      ``MISSING``
AlphaPixelData                                               ``MISSING``
AlphaPixelData_Accessor                                      ``MISSING``
ANIHandler                                                   ``MISSING``
App_CleanUp                                                  ``MISSING``
ArtProvider_Delete                                           :meth:`ArtProvider.Delete`
ArtProvider_GetBitmap                                        :meth:`ArtProvider.GetBitmap`
ArtProvider_GetIcon                                          :meth:`ArtProvider.GetIcon`
ArtProvider_GetIconBundle                                    :meth:`ArtProvider.GetIconBundle`
ArtProvider_GetMessageBoxIcon                                ``MISSING``
ArtProvider_GetMessageBoxIconId                              ``MISSING``
ArtProvider_GetNativeSizeHint                                :meth:`ArtProvider.GetNativeSizeHint`
ArtProvider_GetSizeHint                                      :meth:`ArtProvider.GetSizeHint`
ArtProvider_HasNativeProvider                                :meth:`ArtProvider.HasNativeProvider`
ArtProvider_Insert                                           :meth:`ArtProvider.Insert`
ArtProvider_Pop                                              :meth:`ArtProvider.Pop`
ArtProvider_Push                                             :meth:`ArtProvider.Push`
ArtProvider_PushBack                                         :meth:`ArtProvider.PushBack`
AutoBufferedPaintDCFactory                                   ``MISSING``
BitmapFromBits                                               :class:`Bitmap`
BitmapFromIcon                                               :class:`Bitmap`
BitmapFromImage                                              :class:`Bitmap`
BitmapFromXPMData                                            :class:`Bitmap`
BMPHandler                                                   ``MISSING``
BookCtrlBase_GetClassDefaultAttributes                       :meth:`BookCtrl.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
BrushFromBitmap                                              :class:`Brush`
Button_GetClassDefaultAttributes                             :meth:`Button.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
Button_GetDefaultSize                                        :meth:`Button.GetDefaultSize`
CalculateLayoutEvent                                         :class:`adv.CalculateLayoutEvent`
Caret_GetBlinkTime                                           :meth:`Caret.GetBlinkTime`
Caret_SetBlinkTime                                           :meth:`Caret.SetBlinkTime`
CheckBox_GetClassDefaultAttributes                           :meth:`CheckBox.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
Choice_GetClassDefaultAttributes                             :meth:`Choice.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
ChoicebookEvent                                              :class:`BookCtrlEvent`
Clipboard_Get                                                :meth:`Clipboard.Get`
ClipboardEvent                                               :class:`ClipboardTextEvent`
ClipboardLocker                                              ``MISSING``
ColourRGB                                                    :class:`Colour`
ComboBox_GetClassDefaultAttributes                           :meth:`ComboBox.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
CommandLinkButton                                            :class:`adv.CommandLinkButton`
ConfigBase_Create                                            :meth:`ConfigBase.Create`
ConfigBase_DontCreateOnDemand                                :meth:`ConfigBase.DontCreateOnDemand`
ConfigBase_Get                                               :meth:`ConfigBase.Get`
ConfigBase_Set                                               :meth:`ConfigBase.Set`
Control_Ellipsize                                            :meth:`Control.Ellipsize`
Control_EscapeMnemonics                                      :meth:`Control.EscapeMnemonics`
Control_FindAccelIndex                                       ``MISSING``
Control_GetClassDefaultAttributes                            :meth:`Control.GetClassDefaultAttributes`
Control_GetCompositeControlsDefaultAttributes                ``MISSING``
Control_RemoveMnemonics                                      :meth:`Control.RemoveMnemonics`
CPPFileSystemHandler                                         ``MISSING``
CreateFileTipProvider                                        :func:`adv.CreateFileTipProvider <CreateFileTipProvider>`
CURHandler                                                   ``MISSING``
CursorFromImage                                              :class:`Cursor`
CustomDataFormat                                             ``MISSING``
DateEvent                                                    :class:`adv.DateEvent`
DatePickerCtrl                                               :class:`adv.DatePickerCtrl`
DatePickerCtrlBase                                           :class:`adv.DatePickerCtrl`
DateSpan_Day                                                 :meth:`DateSpan.Day`
DateSpan_Days                                                :meth:`DateSpan.Days`
DateSpan_Month                                               :meth:`DateSpan.Month`
DateSpan_Months                                              :meth:`DateSpan.Months`
DateSpan_Week                                                :meth:`DateSpan.Week`
DateSpan_Weeks                                               :meth:`DateSpan.Weeks`
DateSpan_Year                                                :meth:`DateSpan.Year`
DateSpan_Years                                               :meth:`DateSpan.Years`
DateTime_ConvertYearToBC                                     :meth:`DateTime.ConvertYearToBC`
DateTime_GetAmPmStrings                                      :meth:`DateTime.GetAmPmStrings`
DateTime_GetBeginDST                                         :meth:`DateTime.GetBeginDST`
DateTime_GetCentury                                          :meth:`DateTime.GetCentury`
DateTime_GetCountry                                          :meth:`DateTime.GetCountry`
DateTime_GetCurrentMonth                                     :meth:`DateTime.GetCurrentMonth`
DateTime_GetCurrentYear                                      :meth:`DateTime.GetCurrentYear`
DateTime_GetEndDST                                           :meth:`DateTime.GetEndDST`
DateTime_GetEnglishMonthName                                 :meth:`DateTime.GetEnglishMonthName`
DateTime_GetEnglishWeekDayName                               :meth:`DateTime.GetEnglishWeekDayName`
DateTime_GetMonthName                                        :meth:`DateTime.GetMonthName`
DateTime_GetNumberOfDaysInMonth                              ``MISSING``
DateTime_GetNumberOfDaysinYear                               ``MISSING``
DateTime_GetWeekDayName                                      :meth:`DateTime.GetWeekDayName`
DateTime_IsDSTApplicable                                     :meth:`DateTime.IsDSTApplicable`
DateTime_IsLeapYear                                          :meth:`DateTime.IsLeapYear`
DateTime_IsWestEuropeanCountry                               :meth:`DateTime.IsWestEuropeanCountry`
DateTime_Now                                                 :meth:`DateTime.Now`
DateTime_SetCountry                                          :meth:`DateTime.SetCountry`
DateTime_SetToWeekOfYear                                     :meth:`DateTime.SetToWeekOfYear`
DateTime_Today                                               :meth:`DateTime.Today`
DateTime_UNow                                                :meth:`DateTime.UNow`
DateTimeFromDateTime                                         :class:`DateTime`
Dialog_EnableLayoutAdaptation                                :meth:`Dialog.EnableLayoutAdaptation`
Dialog_GetClassDefaultAttributes                             :meth:`Dialog.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
Dialog_GetLayoutAdapter                                      :meth:`Dialog.GetLayoutAdapter`
Dialog_IsLayoutAdaptationEnabled                             :meth:`Dialog.IsLayoutAdaptationEnabled`
Dialog_SetLayoutAdapter                                      :meth:`Dialog.SetLayoutAdapter`
DirItemData                                                  ``MISSING``
Display_GetCount                                             :meth:`Display.GetCount`
Display_GetFromPoint                                         :meth:`Display.GetFromPoint`
Display_GetFromWindow                                        :meth:`Display.GetFromWindow`
DragIcon                                                     ``MISSING``
DragListItem                                                 ``MISSING``
DragString                                                   ``MISSING``
DragTreeItem                                                 ``MISSING``
DROP_ICON                                                    ``MISSING``
EmptyBitmap                                                  :class:`Bitmap`
EmptyIcon                                                    :class:`Icon`
EncodingConverter                                            ``MISSING``
EncodingConverter_CanConvert                                 ``MISSING``
EncodingConverter_GetAllEquivalents                          ``MISSING``
EncodingConverter_GetPlatformEquivalents                     ``MISSING``
EventLoopBase_GetActive                                      :meth:`EventLoopBase.GetActive`
EventLoopBase_SetActive                                      :meth:`EventLoopBase.SetActive`
EventProcessInHandlerOnly                                    ``MISSING``
EVT_COMMAND                                                  ``MISSING``
EVT_COMMAND_RANGE                                            ``MISSING``
ExpandEnvVars                                                ``MISSING``
FFontFromPixelSize                                           :class:`Font`
FileConfig_GetGlobalFileName                                 :meth:`FileConfig.GetGlobalFileName`
FileConfig_GetLocalFileName                                  :meth:`FileConfig.GetLocalFileName`
FileHistory                                                  ``MISSING``
FileSystem_AddHandler                                        :meth:`FileSystem.AddHandler`
FileSystem_CleanUpHandlers                                   ``MISSING``
FileSystem_FileNameToURL                                     :meth:`FileSystem.FileNameToURL`
FileSystem_RemoveHandler                                     :meth:`FileSystem.RemoveHandler`
FileSystem_URLToFileName                                     :meth:`FileSystem.URLToFileName`
FileSystemHandler_GetAnchor                                  ``MISSING``
FileSystemHandler_GetLeftLocation                            ``MISSING``
FileSystemHandler_GetMimeTypeFromExt                         :meth:`FileSystemHandler.GetMimeTypeFromExt`
FileSystemHandler_GetProtocol                                ``MISSING``
FileSystemHandler_GetRightLocation                           ``MISSING``
FileType_ExpandCommand                                       :meth:`FileType.ExpandCommand`
FileTypeInfoSequence                                         ``MISSING``
FindWindowById                                               ``MISSING``
Font2                                                        :class:`Font`
Font_AdjustToSymbolicSize                                    ``MISSING``
Font_GetDefaultEncoding                                      :meth:`Font.GetDefaultEncoding`
Font_SetDefaultEncoding                                      :meth:`Font.SetDefaultEncoding`
FontEnumerator_GetEncodings                                  :meth:`FontEnumerator.GetEncodings`
FontEnumerator_GetFacenames                                  :meth:`FontEnumerator.GetFacenames`
FontEnumerator_IsValidFacename                               :meth:`FontEnumerator.IsValidFacename`
FontFromNativeInfo                                           :class:`Font`
FontFromNativeInfoString                                     :class:`Font`
FontFromPixelSize                                            :class:`Font`
FontMapper_Get                                               :meth:`FontMapper.Get`
FontMapper_GetDefaultConfigPath                              ``MISSING``
FontMapper_GetEncoding                                       :meth:`FontMapper.GetEncoding`
FontMapper_GetEncodingDescription                            :meth:`FontMapper.GetEncodingDescription`
FontMapper_GetEncodingFromName                               :meth:`FontMapper.GetEncodingFromName`
FontMapper_GetEncodingName                                   :meth:`FontMapper.GetEncodingName`
FontMapper_GetSupportedEncodingsCount                        :meth:`FontMapper.GetSupportedEncodingsCount`
FontMapper_Set                                               :meth:`FontMapper.Set`
Frame_GetClassDefaultAttributes                              :meth:`Frame.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
FutureCall                                                   :class:`CallLater`
Gauge_GetClassDefaultAttributes                              :meth:`Gauge.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
GBSizerItemList                                              ``MISSING``
GBSizerItemList_iterator                                     ``MISSING``
GBSizerItemSizer                                             ``MISSING``
GBSizerItemSpacer                                            ``MISSING``
GBSizerItemWindow                                            ``MISSING``
GDIObjListBase                                               ``MISSING``
GenericFindWindowAtPoint                                     :func:`FindWindowAtPoint`
GetAccelFromString                                           ``MISSING``
GetCurrentId                                                 ``MISSING``
GetCurrentTime                                               ``MISSING``
GetDefaultPyEncoding                                         ``MISSING``
GetDisplayDepth                                              :func:`DisplayDepth`
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
GraphicsContext_Create                                       :meth:`GraphicsContext.Create`
GraphicsContext_CreateFromNative                             :meth:`GraphicsContext.CreateFromNative`
GraphicsContext_CreateFromNativeWindow                       :meth:`GraphicsContext.CreateFromNativeWindow`
GraphicsContext_CreateMeasuringContext                       ``MISSING``
GraphicsRenderer_GetCairoRenderer                            :meth:`GraphicsRenderer.GetCairoRenderer`
GraphicsRenderer_GetDefaultRenderer                          :meth:`GraphicsRenderer.GetDefaultRenderer`
HelpProvider_Get                                             :meth:`HelpProvider.Get`
HelpProvider_Set                                             :meth:`HelpProvider.Set`
HtmlListBox                                                  ``MISSING``
HyperlinkCtrl                                                :class:`adv.HyperlinkCtrl`
HyperlinkEvent                                               :class:`adv.HyperlinkEvent`
ICOHandler                                                   ``MISSING``
IconBundleFromFile                                           :class:`IconBundle`
IconBundleFromIcon                                           :class:`IconBundle`
IconBundleFromStream                                         :class:`IconBundle`
IconFromBitmap                                               :class:`Icon`
IconFromLocation                                             :class:`Icon`
IconFromXPMData                                              :class:`Icon`
IdleEvent_GetMode                                            :meth:`IdleEvent.GetMode`
IdleEvent_SetMode                                            :meth:`IdleEvent.SetMode`
Image_AddHandler                                             :meth:`Image.AddHandler`
Image_CanRead                                                :meth:`Image.CanRead`
Image_CanReadStream                                          ``MISSING``
Image_GetHandlers                                            ``MISSING``
Image_GetImageCount                                          :meth:`Image.GetImageCount`
Image_GetImageExtWildcard                                    :meth:`Image.GetImageExtWildcard`
Image_HSVtoRGB                                               :meth:`Image.HSVtoRGB`
Image_HSVValue                                               :class:`HSVValue`
Image_InsertHandler                                          :meth:`Image.InsertHandler`
Image_RemoveHandler                                          :meth:`Image.RemoveHandler`
Image_RGBtoHSV                                               :meth:`Image.RGBtoHSV`
Image_RGBValue                                               :class:`RGBValue`
ImageFromMime                                                :class:`Image`
ImageFromStream                                              :class:`Image`
ImageFromStreamMime                                          :class:`Image`
ImageHistogram_MakeKey                                       :meth:`ImageHistogram.MakeKey`
IntersectRect                                                ``MISSING``
IsStockID                                                    ``MISSING``
IsStockLabel                                                 ``MISSING``
Joystick                                                     :class:`adv.Joystick`
JPEGHandler                                                  ``MISSING``
LayoutAlgorithm                                              :class:`adv.LayoutAlgorithm`
ListbookEvent                                                :class:`BookCtrlEvent`
ListBox_GetClassDefaultAttributes                            :meth:`ListBox.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
ListCtrl_GetClassDefaultAttributes                           :meth:`ListCtrl.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
ListCtrl_HasColumnOrderSupport                               :meth:`ListCtrl.HasColumnOrderSupport`
Locale_AddCatalogLookupPathPrefix                            :meth:`Locale.AddCatalogLookupPathPrefix`
Locale_AddLanguage                                           :meth:`Locale.AddLanguage`
Locale_FindLanguageInfo                                      :meth:`Locale.FindLanguageInfo`
Locale_GetInfo                                               :meth:`Locale.GetInfo`
Locale_GetLanguageCanonicalName                              :meth:`Locale.GetLanguageCanonicalName`
Locale_GetLanguageInfo                                       :meth:`Locale.GetLanguageInfo`
Locale_GetLanguageName                                       :meth:`Locale.GetLanguageName`
Locale_GetSystemEncoding                                     :meth:`Locale.GetSystemEncoding`
Locale_GetSystemEncodingName                                 :meth:`Locale.GetSystemEncodingName`
Locale_GetSystemLanguage                                     :meth:`Locale.GetSystemLanguage`
Locale_IsAvailable                                           :meth:`Locale.IsAvailable`
Log_AddTraceMask                                             :meth:`Log.AddTraceMask`
Log_ClearTraceMasks                                          :meth:`Log.ClearTraceMasks`
Log_DoCreateOnDemand                                         ``MISSING``
Log_DontCreateOnDemand                                       :meth:`Log.DontCreateOnDemand`
Log_EnableLogging                                            :meth:`Log.EnableLogging`
Log_FlushActive                                              :meth:`Log.FlushActive`
Log_GetActiveTarget                                          :meth:`Log.GetActiveTarget`
Log_GetComponentLevel                                        ``MISSING``
Log_GetLogLevel                                              :meth:`Log.GetLogLevel`
Log_GetRepetitionCounting                                    :meth:`Log.GetRepetitionCounting`
Log_GetTimestamp                                             :meth:`Log.GetTimestamp`
Log_GetTraceMask                                             ``MISSING``
Log_GetTraceMasks                                            :meth:`Log.GetTraceMasks`
Log_GetVerbose                                               :meth:`Log.GetVerbose`
Log_IsAllowedTraceMask                                       :meth:`Log.IsAllowedTraceMask`
Log_IsEnabled                                                :meth:`Log.IsEnabled`
Log_IsLevelEnabled                                           :meth:`Log.IsLevelEnabled`
Log_RemoveTraceMask                                          :meth:`Log.RemoveTraceMask`
Log_Resume                                                   :meth:`Log.Resume`
Log_SetActiveTarget                                          :meth:`Log.SetActiveTarget`
Log_SetComponentLevel                                        :meth:`Log.SetComponentLevel`
Log_SetLogLevel                                              :meth:`Log.SetLogLevel`
Log_SetRepetitionCounting                                    :meth:`Log.SetRepetitionCounting`
Log_SetTimestamp                                             :meth:`Log.SetTimestamp`
Log_SetTraceMask                                             ``MISSING``
Log_SetVerbose                                               :meth:`Log.SetVerbose`
Log_Suspend                                                  :meth:`Log.Suspend`
Log_TimeStamp                                                ``MISSING``
LogInfo                                                      :func:`LogMessage`
LogStatusFrame                                               :func:`LogStatus`
LogTrace                                                     ``MISSING``
MaskColour                                                   :class:`Colour`
MemoryDCFromDC                                               :class:`MemoryDC`
MemoryFSHandler_AddFile                                      :meth:`MemoryFSHandler.AddFile`
MemoryFSHandler_AddFileWithMimeType                          :meth:`MemoryFSHandler.AddFileWithMimeType`
MemoryFSHandler_RemoveFile                                   :meth:`MemoryFSHandler.RemoveFile`
MenuBar_GetAutoWindowMenu                                    ``MISSING``
MenuBar_MacSetCommonMenuBar                                  :meth:`MenuBar.MacSetCommonMenuBar`
MenuBar_SetAutoWindowMenu                                    ``MISSING``
MenuItem_GetDefaultMarginWidth                               ``MISSING``
MenuItem_GetLabelText                                        :meth:`MenuItem.GetLabelText`
MetaFile                                                     ``MISSING``
MetafileDataObject                                           ``MISSING``
MetaFileDC                                                   ``MISSING``
MimeTypesManager_IsOfType                                    :meth:`MimeTypesManager.IsOfType`
ModalEventLoop                                               ``MISSING``
MutexGuiEnter                                                ``MISSING``
MutexGuiLeave                                                ``MISSING``
MutexGuiLocker                                               ``MISSING``
NamedColour                                                  :class:`Colour`
NativeEncodingInfo                                           ``MISSING``
NativePixelData                                              ``MISSING``
NativePixelData_Accessor                                     ``MISSING``
NcPaintEvent                                                 ``MISSING``
Notebook_GetClassDefaultAttributes                           :meth:`Notebook.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
NotebookEvent                                                :class:`BookCtrlEvent`
NotebookPage                                                 ``MISSING``
NotificationMessage                                          :class:`adv.NotificationMessage`
NullFileTypeInfo                                             ``MISSING``
NumberEntryDialog                                            ``MISSING``
Panel_GetClassDefaultAttributes                              :meth:`Panel.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
PasswordEntryDialog                                          ``MISSING``
PCXHandler                                                   ``MISSING``
PixelDataBase                                                ``MISSING``
PlatformInformation_GetOperatingSystemDirectory              :meth:`PlatformInfo.GetOperatingSystemDirectory`
PNGHandler                                                   ``MISSING``
PNMHandler                                                   ``MISSING``
Point2DCopy                                                  :class:`Point2DDouble`
Point2DFromPoint                                             :class:`Point2DDouble`
PreBitmapButton                                              :class:`BitmapButton`
PreButton                                                    :class:`Button`
PreCheckBox                                                  :class:`CheckBox`
PreCheckListBox                                              :class:`CheckListBox`
PreChoice                                                    :class:`Choice`
PreChoicebook                                                :class:`Choicebook`
PreCollapsiblePane                                           :class:`CollapsiblePane`
PreColourPickerCtrl                                          :class:`ColourPickerCtrl`
PreComboBox                                                  :class:`ComboBox`
PreCommandLinkButton                                         :class:`adv.CommandLinkButton`
PreControl                                                   :class:`Control`
PreDatePickerCtrl                                            :class:`adv.DatePickerCtrl`
PreDialog                                                    :class:`Dialog`
PreDirFilterListCtrl                                         :class:`DirFilterListCtrl`
PreDirPickerCtrl                                             :class:`DirPickerCtrl`
PreFileCtrl                                                  :class:`FileCtrl`
PreFilePickerCtrl                                            :class:`FilePickerCtrl`
PreFindReplaceDialog                                         :class:`FindReplaceDialog`
PreFontPickerCtrl                                            :class:`FontPickerCtrl`
PreFrame                                                     :class:`Frame`
PreGauge                                                     :class:`Gauge`
PreGenericDirCtrl                                            :class:`GenericDirCtrl`
PreHScrolledWindow                                           :class:`HScrolledWindow`
PreHtmlListBox                                               ``MISSING``
PreHVScrolledWindow                                          :class:`HVScrolledWindow`
PreHyperlinkCtrl                                             :class:`adv.HyperlinkCtrl`
PreInfoBar                                                   :class:`InfoBar`
PreListbook                                                  :class:`Listbook`
PreListBox                                                   :class:`ListBox`
PreListCtrl                                                  :class:`ListCtrl`
PreListView                                                  :class:`ListView`
PreMDIChildFrame                                             :class:`MDIChildFrame`
PreMDIClientWindow                                           :class:`MDIClientWindow`
PreMDIParentFrame                                            :class:`MDIParentFrame`
PreMiniFrame                                                 :class:`MiniFrame`
PreNotebook                                                  :class:`Notebook`
PrePanel                                                     :class:`Panel`
PrePopupTransientWindow                                      :class:`PopupTransientWindow`
PrePopupWindow                                               :class:`PopupWindow`
PrePyAxBaseWindow                                            ``MISSING``
PrePyControl                                                 :class:`Control`
PrePyPanel                                                   :class:`Panel`
PrePyPickerBase                                              :class:`PickerBase`
PrePyScrolledWindow                                          :class:`ScrolledWindow`
PrePyWindow                                                  :class:`Window`
PreRadioBox                                                  :class:`RadioBox`
PreRadioButton                                               :class:`RadioButton`
PreSashLayoutWindow                                          :class:`adv.SashLayoutWindow`
PreSashWindow                                                :class:`adv.SashWindow`
PreScrollBar                                                 :class:`ScrollBar`
PreScrolledWindow                                            :class:`ScrolledWindow`
PreSearchCtrl                                                :class:`SearchCtrl`
PreSimpleHtmlListBox                                         ``MISSING``
PreSingleInstanceChecker                                     :class:`SingleInstanceChecker`
PreSlider                                                    :class:`Slider`
PreSpinButton                                                :class:`SpinButton`
PreSpinCtrl                                                  :class:`SpinCtrl`
PreSpinCtrlDouble                                            :class:`SpinCtrlDouble`
PreSplitterWindow                                            :class:`SplitterWindow`
PreStaticBitmap                                              :class:`StaticBitmap`
PreStaticBox                                                 :class:`StaticBox`
PreStaticLine                                                :class:`StaticLine`
PreStaticText                                                :class:`StaticText`
PreStatusBar                                                 :class:`StatusBar`
PreTextCtrl                                                  :class:`TextCtrl`
PreToggleButton                                              :class:`ToggleButton`
PreToolBar                                                   :class:`ToolBar`
PreToolbook                                                  :class:`Toolbook`
PreTreebook                                                  :class:`Treebook`
PreTreeCtrl                                                  :class:`TreeCtrl`
PreVListBox                                                  ``MISSING``
PreVScrolledWindow                                           :class:`VScrolledWindow`
PreWindow                                                    :class:`Window`
Printer_GetLastError                                         :meth:`Printer.GetLastError`
Process_Exists                                               :meth:`Process.Exists`
Process_Kill                                                 :meth:`Process.Kill`
Process_Open                                                 :meth:`Process.Open`
PseudoDC                                                     ``MISSING``
PyApp_GetComCtl32Version                                     ``MISSING``
PyApp_GetMacAboutMenuItemId                                  :meth:`PyApp.GetMacAboutMenuItemId`
PyApp_GetMacExitMenuItemId                                   :meth:`PyApp.GetMacExitMenuItemId`
PyApp_GetMacHelpMenuTitleName                                :meth:`PyApp.GetMacHelpMenuTitleName`
PyApp_GetMacPreferencesMenuItemId                            :meth:`PyApp.GetMacPreferencesMenuItemId`
PyApp_GetMacSupportPCMenuShortcuts                           ``MISSING``
PyApp_GetShell32Version                                      ``MISSING``
PyApp_GetTraitsIfExists                                      ``MISSING``
PyApp_IsDisplayAvailable                                     :meth:`PyApp.IsDisplayAvailable`
PyApp_IsMainLoopRunning                                      :meth:`PyApp.IsMainLoopRunning`
PyApp_SetMacAboutMenuItemId                                  :meth:`PyApp.SetMacAboutMenuItemId`
PyApp_SetMacExitMenuItemId                                   :meth:`PyApp.SetMacExitMenuItemId`
PyApp_SetMacHelpMenuTitleName                                :meth:`PyApp.SetMacHelpMenuTitleName`
PyApp_SetMacPreferencesMenuItemId                            :meth:`PyApp.SetMacPreferencesMenuItemId`
PyApp_SetMacSupportPCMenuShortcuts                           ``MISSING``
PyAxBaseWindow_FromHWND                                      ``MISSING``
PyBitmapDataObject                                           :class:`BitmapDataObject`
PyCommandEvent                                               :class:`CommandEvent`
PyControl                                                    :class:`Control`
PyDataObjectSimple                                           :class:`DataObjectSimple`
PyDeadObjectError                                            `RuntimeError`
PyDropTarget                                                 :class:`DropTarget`
PyEvent                                                      :class:`Event`
PyEvtHandler                                                 :class:`EvtHandler`
PyImageHandler                                               :class:`ImageHandler`
PyLocale                                                     :class:`Locale`
PyLog                                                        :class:`Log`
PyPanel                                                      :class:`Panel`
PyPickerBase                                                 :class:`PickerBase`
PyPreviewControlBar                                          :class:`PreviewControlBar`
PyPreviewFrame                                               :class:`PreviewFrame`
PyPrintPreview                                               :class:`PrintPreview`
PyScrolledWindow                                             :class:`ScrolledWindow`
PySimpleApp                                                  :class:`App`
PyTextDataObject                                             :class:`TextDataObject`
PyTimer                                                      :class:`Timer`
PyTipProvider                                                :class:`adv.TipProvider`
PyValidator                                                  :class:`Validator`
PyWindow                                                     :class:`Window`
Quantize                                                     ``MISSING``
Quantize_Quantize                                            ``MISSING``
QueryLayoutInfoEvent                                         :class:`adv.QueryLayoutInfoEvent`
RadioBox_GetClassDefaultAttributes                           :meth:`RadioBox.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
RadioButton_GetClassDefaultAttributes                        :meth:`RadioButton.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
RectPP                                                       :class:`Rect`
RectPS                                                       :class:`Rect`
RectS                                                        :class:`Rect`
RegionFromBitmap                                             :class:`Region`
RegionFromBitmapColour                                       :class:`Region`
RegionFromPoints                                             :class:`Region`
RendererNative_Get                                           :meth:`RendererNative.Get`
RendererNative_GetDefault                                    :meth:`RendererNative.GetDefault`
RendererNative_GetGeneric                                    :meth:`RendererNative.GetGeneric`
RendererNative_Set                                           :meth:`RendererNative.Set`
RendererVersion_IsCompatible                                 :meth:`RendererVersion.IsCompatible`
SashEvent                                                    :class:`adv.SashEvent`
SashLayoutWindow                                             :class:`adv.SashLayoutWindow`
SashWindow                                                   :class:`adv.SashWindow`
ScrollBar_GetClassDefaultAttributes                          :meth:`ScrollBar.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
ScrolledWindow_GetClassDefaultAttributes                     :meth:`ScrolledWindow.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
ScrollHelper                                                 :class:`VarHVScrollHelper`
SearchCtrlBase                                               :class:`SearchCtrl`
SetCursor                                                    ``MISSING``
SetDefaultPyEncoding                                         ``MISSING``
ShowTip                                                      :func:`adv.ShowTip <ShowTip>`
SimpleHtmlListBox                                            ``MISSING``
SizerFlags_GetDefaultBorder                                  :meth:`SizerFlags.GetDefaultBorder`
SizerItemSizer                                               ``MISSING``
SizerItemSpacer                                              ``MISSING``
SizerItemWindow                                              ``MISSING``
Slider_GetClassDefaultAttributes                             :meth:`Slider.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
Sound                                                        :class:`adv.Sound`
Sound_PlaySound                                              :meth:`adv.Sound.PlaySound`
Sound_Stop                                                   :meth:`adv.Sound.Stop`
SoundFromData                                                :class:`adv.Sound`
SpinButton_GetClassDefaultAttributes                         :meth:`SpinButton.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
SpinCtrl_GetClassDefaultAttributes                           :meth:`SpinCtrl.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
SplashScreen                                                 :class:`adv.SplashScreen`
SplashScreenWindow                                           ``MISSING``
SplitterWindow_GetClassDefaultAttributes                     :meth:`SplitterWindow.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
StandardDialogLayoutAdapter                                  ``MISSING``
StandardDialogLayoutAdapter_DoFitWithScrolling               ``MISSING``
StandardDialogLayoutAdapter_DoMustScroll                     ``MISSING``
StandardDialogLayoutAdapter_DoReparentControls               ``MISSING``
StandardPaths_Get                                            :meth:`StandardPaths.Get`
StaticBitmap_GetClassDefaultAttributes                       :meth:`StaticBitmap.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
StaticBox_GetClassDefaultAttributes                          :meth:`StaticBox.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
StaticLine_GetClassDefaultAttributes                         :meth:`StaticLine.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
StaticLine_GetDefaultSize                                    :meth:`StaticLine.GetDefaultSize`
StaticText_GetClassDefaultAttributes                         :meth:`StaticText.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
StatusBar_GetClassDefaultAttributes                          :meth:`StatusBar.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
StockCursor                                                  :class:`Cursor`
StockGDI_DeleteAll                                           :meth:`StockGDI.DeleteAll`
StockGDI_GetBrush                                            :meth:`StockGDI.GetBrush`
StockGDI_GetColour                                           :meth:`StockGDI.GetColour`
StockGDI_GetCursor                                           :meth:`StockGDI.GetCursor`
StockGDI_GetPen                                              :meth:`StockGDI.GetPen`
StockGDI_instance                                            :meth:`StockGDI.instance`
StopWatch                                                    ``MISSING``
SystemOptions_GetOption                                      :meth:`SystemOptions.GetOption`
SystemOptions_GetOptionInt                                   :meth:`SystemOptions.GetOptionInt`
SystemOptions_HasOption                                      :meth:`SystemOptions.HasOption`
SystemOptions_IsFalse                                        :meth:`SystemOptions.IsFalse`
SystemOptions_SetOption                                      :meth:`SystemOptions.SetOption`
SystemOptions_SetOptionInt                                   ``MISSING``
SystemSettings_GetColour                                     :meth:`SystemSettings.GetColour`
SystemSettings_GetFont                                       :meth:`SystemSettings.GetFont`
SystemSettings_GetMetric                                     :meth:`SystemSettings.GetMetric`
SystemSettings_GetScreenType                                 :meth:`SystemSettings.GetScreenType`
SystemSettings_HasFeature                                    :meth:`SystemSettings.HasFeature`
SystemSettings_SetScreenType                                 ``MISSING``
TaskBarIcon                                                  :class:`adv.TaskBarIcon`
TaskBarIcon_IsAvailable                                      :meth:`adv.TaskBarIcon.IsAvailable`
TaskBarIconEvent                                             :class:`adv.TaskBarIconEvent`
TestFontEncoding                                             ``MISSING``
TextAreaBase                                                 ``MISSING``
TextAttr_BitlistsEqPartial                                   ``MISSING``
TextAttr_Combine                                             ``MISSING``
TextAttr_CombineBitlists                                     ``MISSING``
TextAttr_RemoveStyle                                         ``MISSING``
TextAttr_SplitParaCharStyles                                 ``MISSING``
TextAttr_TabsEq                                              ``MISSING``
TextCtrl_GetClassDefaultAttributes                           :meth:`TextCtrl.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
TextCtrlBase                                                 ``MISSING``
TextCtrlIface                                                ``MISSING``
TextEntryBase                                                ``MISSING``
TextEntryDialog                                              ``MISSING``
TextUrlEvent                                                 ``MISSING``
TGAHandler                                                   ``MISSING``
Thread_IsMain                                                ``MISSING``
ThreadEvent                                                  ``MISSING``
TIFFHandler                                                  ``MISSING``
TimeSpan_Day                                                 :meth:`TimeSpan.Day`
TimeSpan_Days                                                :meth:`TimeSpan.Days`
TimeSpan_Hour                                                :meth:`TimeSpan.Hour`
TimeSpan_Hours                                               :meth:`TimeSpan.Hours`
TimeSpan_Millisecond                                         :meth:`TimeSpan.Millisecond`
TimeSpan_Milliseconds                                        :meth:`TimeSpan.Milliseconds`
TimeSpan_Minute                                              :meth:`TimeSpan.Minute`
TimeSpan_Minutes                                             :meth:`TimeSpan.Minutes`
TimeSpan_Second                                              :meth:`TimeSpan.Second`
TimeSpan_Seconds                                             :meth:`TimeSpan.Seconds`
TimeSpan_Week                                                :meth:`TimeSpan.Week`
TimeSpan_Weeks                                               :meth:`TimeSpan.Weeks`
TipProvider                                                  :class:`adv.TipProvider`
ToggleButton_GetClassDefaultAttributes                       :meth:`ToggleButton.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
ToolBar_GetClassDefaultAttributes                            :meth:`ToolBar.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
ToolbookEvent                                                :class:`BookCtrlEvent`
ToolTip_Enable                                               :meth:`ToolTip.Enable`
ToolTip_SetAutoPop                                           :meth:`ToolTip.SetAutoPop`
ToolTip_SetDelay                                             :meth:`ToolTip.SetDelay`
ToolTip_SetMaxWidth                                          :meth:`ToolTip.SetMaxWidth`
ToolTip_SetReshow                                            :meth:`ToolTip.SetReshow`
TopLevelWindow_GetDefaultSize                                :meth:`TopLevelWindow.GetDefaultSize`
Trap                                                         ``MISSING``
TreebookEvent                                                :class:`BookCtrlEvent`
TreeCtrl_GetClassDefaultAttributes                           :meth:`TreeCtrl.GetClassDefaultAttributes <Window.GetClassDefaultAttributes>`
TreeItemData                                                 ``MISSING``
UpdateUIEvent_CanUpdate                                      :meth:`UpdateUIEvent.CanUpdate`
UpdateUIEvent_GetMode                                        :meth:`UpdateUIEvent.GetMode`
UpdateUIEvent_GetUpdateInterval                              :meth:`UpdateUIEvent.GetUpdateInterval`
UpdateUIEvent_ResetUpdateTime                                :meth:`UpdateUIEvent.ResetUpdateTime`
UpdateUIEvent_SetMode                                        :meth:`UpdateUIEvent.SetMode`
UpdateUIEvent_SetUpdateInterval                              :meth:`UpdateUIEvent.SetUpdateInterval`
Validator_IsSilent                                           ``MISSING``
Validator_SetBellOnError                                     ``MISSING``
Validator_SuppressBellOnError                                :meth:`Validator.SuppressBellOnError`
VListBox                                                     ``MISSING``
WakeUpMainThread                                             ``MISSING``
Window_FindFocus                                             :meth:`Window.FindFocus`
Window_FromHWND                                              ``MISSING``
Window_GetCapture                                            :meth:`Window.GetCapture`
Window_GetClassDefaultAttributes                             :meth:`Window.GetClassDefaultAttributes`
Window_NewControlId                                          :meth:`Window.NewControlId`
Window_UnreserveControlId                                    :meth:`Window.UnreserveControlId`
XPMHandler                                                   ``MISSING``
YieldIfNeeded                                                ``MISSING``
===========================================================  ===========================================================


:class:`DC` Modifications
-------------------------

===========================================================  ===========================================================
`Classic` Name                                               `Phoenix` Name
===========================================================  ===========================================================
BeginDrawing                                                 ``REMOVED``
BlitPointSize                                                :meth:`~DC.Blit`
CalcBoundingBoxPoint                                         :meth:`~DC.CalcBoundingBox`
CanDrawBitmap                                                ``MISSING``
CanGetTextExtent                                             ``MISSING``
CrossHairPoint                                               :meth:`~DC.CrossHair`
DrawArcPoint                                                 :meth:`~DC.DrawArc`
DrawBitmapPoint                                              :meth:`~DC.DrawBitmap`
DrawCheckMarkRect                                            :meth:`~DC.DrawCheckMark`
DrawCirclePoint                                              :meth:`~DC.DrawCircle`
DrawEllipseList                                              ``MISSING``
DrawEllipsePointSize                                         :meth:`~DC.DrawEllipse`
DrawEllipseRect                                              :meth:`~DC.DrawEllipse`
DrawEllipticArcPointSize                                     :meth:`~DC.DrawEllipticArc`
DrawIconPoint                                                :meth:`~DC.DrawIcon`
DrawLineList                                                 ``MISSING``
DrawLinePoint                                                :meth:`~DC.DrawLine`
DrawPointList                                                ``MISSING``
DrawPointPoint                                               :meth:`~DC.DrawPoint`
DrawPolygonList                                              ``MISSING``
DrawRectangleList                                            ``MISSING``
DrawRectanglePointSize                                       :meth:`~DC.DrawRectangle`
DrawRectangleRect                                            :meth:`~DC.DrawRectangle`
DrawRotatedTextPoint                                         :meth:`~DC.DrawRotatedText`
DrawRoundedRectanglePointSize                                :meth:`~DC.DrawRoundedRectangle`
DrawRoundedRectangleRect                                     :meth:`~DC.DrawRoundedRectangle`
DrawTextList                                                 ``MISSING``
DrawTextPoint                                                :meth:`~DC.DrawText`
EndDrawing                                                   ``REMOVED``
FloodFillPoint                                               :meth:`~DC.FloodFill`
GetAsBitmap                                                  ``MISSING``
GetDeviceOriginTuple                                         :meth:`~DC.GetDeviceOrigin`
GetImpl                                                      ``MISSING``
GetLogicalOriginTuple                                        :meth:`~DC.GetLogicalOrigin`
GetMultiLineTextExtent                                       :meth:`~DC.GetFullMultiLineTextExtent`
GetOptimization                                              ``MISSING``
GetPixelPoint                                                ``MISSING``
GetResolution                                                ``MISSING``
GetSizeMMTuple                                               :meth:`~DC.GetSizeMM`
Ok                                                           :meth:`~DC.IsOk`
SetClippingRect                                              :meth:`~DC.SetClippingRegion`
SetClippingRegionAsRegion                                    :meth:`~DC.SetClippingRegion`
SetClippingRegionPointSize                                   :meth:`~DC.SetClippingRegion`
SetDeviceOriginPoint                                         :meth:`~DC.SetDeviceOrigin`
SetLogicalOriginPoint                                        :meth:`~DC.SetLogicalOrigin`
SetOptimization                                              ``MISSING``
StretchBlitPointSize                                         :meth:`~DC.StretchBlit`
===========================================================  ===========================================================


:class:`Window` Modifications
-----------------------------

===========================================================  ===========================================================
`Classic` Name                                               `Phoenix` Name
===========================================================  ===========================================================
AdjustForLayoutDirection                                     ``MISSING``
CanAcceptFocus                                               ``MISSING``
CanAcceptFocusFromKeyboard                                   ``MISSING``
CanApplyThemeBorder                                          ``MISSING``
CanBeOutsideClientArea                                       ``MISSING``
ClientToScreenXY                                             :meth:`~Window.ClientToScreen`
ConvertDialogPointToPixels                                   :meth:`~Window.ConvertDialogToPixels`
ConvertDialogSizeToPixels                                    :meth:`~Window.ConvertDialogToPixels`
GetAdjustedBestSize                                          ``REMOVED``
GetBestFittingSize                                           ``REMOVED``
GetBestSizeTuple                                             :meth:`~Window.GetBestSize`
GetClientSizeTuple                                           :meth:`~Window.GetClientSize`
GetScreenPositionTuple                                       :meth:`~Window.GetScreenPosition`
GetSizeTuple                                                 :meth:`~Window.GetSize`
GetToolTipString                                             :meth:`~Window.GetToolTipText`
HitTestXY                                                    :meth:`~Window.HitTest`
InheritsBackgroundColour                                     ``MISSING``
IsExposedPoint                                               :meth:`~Window.IsExposed`
IsExposedRect                                                :meth:`~Window.IsExposed`
MakeModal                                                    ``MISSING``
PopupMenuXY                                                  :meth:`~Window.PopupMenu`
ScreenToClientXY                                             :meth:`~Window.ScreenToClient`
SendIdleEvents                                               ``MISSING``
SetBestFittingSize                                           ``REMOVED``
SetClientSizeWH                                              :meth:`~Window.SetClientSize`
SetDimensions                                                :meth:`~Window.SetSize`
SetHelpTextForId                                             :meth:`~Window.SetHelpText`
SetSizeHintsSz                                               :meth:`~Window.SetSizeHints`
SetToolTipString                                             :meth:`~Window.SetToolTip`
SetVirtualSizeHints                                          ``MISSING``
SetVirtualSizeHintsSz                                        ``MISSING``
UseBgCol                                                     ``MISSING``
===========================================================  ===========================================================


:class:`Sizer` Modifications
----------------------------

===========================================================  ===========================================================
`Classic` Name                                               `Phoenix` Name
===========================================================  ===========================================================
AddF                                                         :meth:`~Sizer.Add`
AddItem                                                      :meth:`~Sizer.Add`
AddSizer                                                     :meth:`~Sizer.Add`
AddWindow                                                    :meth:`~Sizer.Add`
DeleteWindows                                                ``MISSING``
GetItemIndex                                                 :meth:`~Sizer.GetItem`
GetMinSizeTuple                                              :meth:`~Sizer.GetMinSize`
GetPositionTuple                                             :meth:`~Sizer.GetPosition`
InsertF                                                      :meth:`~Sizer.Insert`
InsertItem                                                   :meth:`~Sizer.Insert`
InsertSizer                                                  :meth:`~Sizer.Insert`
InsertWindow                                                 :meth:`~Sizer.Insert`
PrependF                                                     :meth:`~Sizer.Prepend`
PrependItem                                                  :meth:`~Sizer.Prepend`
PrependSizer                                                 :meth:`~Sizer.Prepend`
PrependWindow                                                :meth:`~Sizer.Prepend`
RemovePos                                                    :meth:`~Sizer.Remove`
RemoveSizer                                                  :meth:`~Sizer.Remove`
RemoveWindow                                                 :meth:`~Sizer.Remove`
SetContainingWindow                                          ``MISSING``
ShowItems                                                    ``MISSING``
===========================================================  ===========================================================


Miscellaneous Modifications
---------------------------

===========================================================  ===========================================================
`Classic` Name                                               `Phoenix` Name
===========================================================  ===========================================================
Rect.OffsetXY                                                :meth:`Rect.Offset`
===========================================================  ===========================================================



wx.lib Modifications
--------------------

===========================================================  ===========================================================
`Classic` Name                                               `Phoenix` Name
===========================================================  ===========================================================
wx.lib.buttonpanel                                           :mod:`lib.agw.buttonpanel`
wx.lib.customtreectrl                                        :mod:`lib.agw.customtreectrl`
wx.lib.flatnotebook                                          :mod:`lib.agw.flatnotebook`
wx.lib.foldpanelbar                                          :mod:`lib.agw.foldpanelbar`
wx.lib.hyperlink                                             :mod:`lib.agw.hyperlink`
wx.lib.grids                                                 ``REMOVED``
wx.lib.pyshell                                               ``REMOVED``
wx.lib.rightalign                                            ``REMOVED``
wx.lib.shell                                                 ``REMOVED``
wx.lib.splashscreen                                          ``REMOVED``
wx.lib.wxPlotCanvas                                          ``REMOVED``
===========================================================  ===========================================================
