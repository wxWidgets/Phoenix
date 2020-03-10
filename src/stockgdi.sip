//--------------------------------------------------------------------------
// Name:        src/stockobj.sip
// Purpose:     Wrapper definition and some Python code for wxStockGDI and
//              using it to initialize the stock objects like wx.BLUE_BRUSH,
//              etc.  We're putting it here because wxStockGDI is not
//              documented, and probably should not be.
//
// Author:      Robin Dunn
//
// Created:     18-Sept-2011
// Copyright:   (c) 2011-2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------


class wxStockGDI
{
public:
    enum Item {
        BRUSH_BLACK,
        BRUSH_BLUE,
        BRUSH_CYAN,
        BRUSH_GREEN,
        BRUSH_YELLOW,
        BRUSH_GREY,
        BRUSH_LIGHTGREY,
        BRUSH_MEDIUMGREY,
        BRUSH_RED,
        BRUSH_TRANSPARENT,
        BRUSH_WHITE,
        COLOUR_BLACK,
        COLOUR_BLUE,
        COLOUR_CYAN,
        COLOUR_GREEN,
        COLOUR_YELLOW,
        COLOUR_LIGHTGREY,
        COLOUR_RED,
        COLOUR_WHITE,
        CURSOR_CROSS,
        CURSOR_HOURGLASS,
        CURSOR_STANDARD,
        FONT_ITALIC,
        FONT_NORMAL,
        FONT_SMALL,
        FONT_SWISS,
        PEN_BLACK,
        PEN_BLACKDASHED,
        PEN_BLUE,
        PEN_CYAN,
        PEN_GREEN,
        PEN_YELLOW,
        PEN_GREY,
        PEN_LIGHTGREY,
        PEN_MEDIUMGREY,
        PEN_RED,
        PEN_TRANSPARENT,
        PEN_WHITE
    };

    wxStockGDI();
    virtual ~wxStockGDI();
    static void DeleteAll();

    static wxStockGDI& instance();

    static const wxBrush* GetBrush(Item item);
    static const wxColour* GetColour(Item item);
    static const wxCursor* GetCursor(Item item);
    static const wxPen* GetPen(Item item);

    const wxFont* GetFont(Item item);

    // Add some methods for fetching the various global gdi object lists so
    // they can be set at app creation time too.
    static wxFontList* _getTheFontList();
    %MethodCode
        sipRes = wxTheFontList;
    %End

    static wxPenList* _getThePenList();
    %MethodCode
        sipRes = wxThePenList;
    %End

    static wxBrushList* _getTheBrushList();
    %MethodCode
        sipRes = wxTheBrushList;
    %End

    static wxColourDatabase* _getTheColourDatabase();
    %MethodCode
        sipRes = wxTheColourDatabase;
    %End


private:
    wxStockGDI(const wxStockGDI&);
    wxStockGDI& operator=(const wxStockGDI&);
};

%Extract(id=pycode_core)
def _initStockObjects():
    import wx
    wx.NORMAL_FONT._copyFrom(       StockGDI.instance().GetFont(StockGDI.FONT_NORMAL))
    wx.SMALL_FONT._copyFrom(        StockGDI.instance().GetFont(StockGDI.FONT_SMALL))
    wx.SWISS_FONT._copyFrom(        StockGDI.instance().GetFont(StockGDI.FONT_SWISS))
    wx.ITALIC_FONT._copyFrom(       StockGDI.instance().GetFont(StockGDI.FONT_ITALIC))

    wx.BLACK_DASHED_PEN._copyFrom(  StockGDI.GetPen(StockGDI.PEN_BLACKDASHED))
    wx.BLACK_PEN._copyFrom(         StockGDI.GetPen(StockGDI.PEN_BLACK))
    wx.BLUE_PEN._copyFrom(          StockGDI.GetPen(StockGDI.PEN_BLUE))
    wx.CYAN_PEN._copyFrom(          StockGDI.GetPen(StockGDI.PEN_CYAN))
    wx.GREEN_PEN._copyFrom(         StockGDI.GetPen(StockGDI.PEN_GREEN))
    wx.YELLOW_PEN._copyFrom(        StockGDI.GetPen(StockGDI.PEN_YELLOW))
    wx.GREY_PEN._copyFrom(          StockGDI.GetPen(StockGDI.PEN_GREY))
    wx.LIGHT_GREY_PEN._copyFrom(    StockGDI.GetPen(StockGDI.PEN_LIGHTGREY))
    wx.MEDIUM_GREY_PEN._copyFrom(   StockGDI.GetPen(StockGDI.PEN_MEDIUMGREY))
    wx.RED_PEN._copyFrom(           StockGDI.GetPen(StockGDI.PEN_RED))
    wx.TRANSPARENT_PEN._copyFrom(   StockGDI.GetPen(StockGDI.PEN_TRANSPARENT))
    wx.WHITE_PEN._copyFrom(         StockGDI.GetPen(StockGDI.PEN_WHITE))

    wx.BLACK_BRUSH._copyFrom(       StockGDI.GetBrush(StockGDI.BRUSH_BLACK))
    wx.BLUE_BRUSH._copyFrom(        StockGDI.GetBrush(StockGDI.BRUSH_BLUE))
    wx.CYAN_BRUSH._copyFrom(        StockGDI.GetBrush(StockGDI.BRUSH_CYAN))
    wx.GREEN_BRUSH._copyFrom(       StockGDI.GetBrush(StockGDI.BRUSH_GREEN))
    wx.YELLOW_BRUSH._copyFrom(      StockGDI.GetBrush(StockGDI.BRUSH_YELLOW))
    wx.GREY_BRUSH._copyFrom(        StockGDI.GetBrush(StockGDI.BRUSH_GREY))
    wx.LIGHT_GREY_BRUSH._copyFrom(  StockGDI.GetBrush(StockGDI.BRUSH_LIGHTGREY))
    wx.MEDIUM_GREY_BRUSH._copyFrom( StockGDI.GetBrush(StockGDI.BRUSH_MEDIUMGREY))
    wx.RED_BRUSH._copyFrom(         StockGDI.GetBrush(StockGDI.BRUSH_RED))
    wx.TRANSPARENT_BRUSH._copyFrom( StockGDI.GetBrush(StockGDI.BRUSH_TRANSPARENT))
    wx.WHITE_BRUSH._copyFrom(       StockGDI.GetBrush(StockGDI.BRUSH_WHITE))

    wx.BLACK._copyFrom(             StockGDI.GetColour(StockGDI.COLOUR_BLACK))
    wx.BLUE._copyFrom(              StockGDI.GetColour(StockGDI.COLOUR_BLUE))
    wx.CYAN._copyFrom(              StockGDI.GetColour(StockGDI.COLOUR_CYAN))
    wx.GREEN._copyFrom(             StockGDI.GetColour(StockGDI.COLOUR_GREEN))
    wx.YELLOW._copyFrom(            StockGDI.GetColour(StockGDI.COLOUR_YELLOW))
    wx.LIGHT_GREY._copyFrom(        StockGDI.GetColour(StockGDI.COLOUR_LIGHTGREY))
    wx.RED._copyFrom(               StockGDI.GetColour(StockGDI.COLOUR_RED))
    wx.WHITE._copyFrom(             StockGDI.GetColour(StockGDI.COLOUR_WHITE))

    wx.CROSS_CURSOR._copyFrom(      StockGDI.GetCursor(StockGDI.CURSOR_CROSS))
    wx.HOURGLASS_CURSOR._copyFrom(  StockGDI.GetCursor(StockGDI.CURSOR_HOURGLASS))
    wx.STANDARD_CURSOR._copyFrom(   StockGDI.GetCursor(StockGDI.CURSOR_STANDARD))

    wx.TheFontList       = StockGDI._getTheFontList()
    wx.ThePenList        = StockGDI._getThePenList()
    wx.TheBrushList      = StockGDI._getTheBrushList()
    wx.TheColourDatabase = StockGDI._getTheColourDatabase()


StockGDI._initStockObjects = staticmethod(_initStockObjects)
%End
